"""Combat loop and battle management."""

from typing import Optional, List, Dict, Any, TYPE_CHECKING
from enum import Enum
import random

from .enemy import Enemy, EnemyAI
from .actions import ActionRegistry, CombatAction, WarriorActions, MageActions
from .damage import DamageCalculator, AttackType
from .effects import StatusEffect, create_bleeding, create_stun

if TYPE_CHECKING:
    from ..character import PlayerCharacter


class BattleResult(Enum):
    """Possible battle outcomes."""
    VICTORY = "victory"
    DEFEAT = "defeat"
    FLED = "fled"
    ONGOING = "ongoing"


class BattleTurn:
    """Represents one turn in combat."""

    def __init__(self, actor: str, action: str, target: str, damage: int, effects: List[str]):
        """
        Initialize battle turn.

        Args:
            actor: Who acted
            action: What action was taken
            target: Who was targeted
            damage: Damage dealt
            effects: Status effects applied
        """
        self.actor = actor
        self.action = action
        self.target = target
        self.damage = damage
        self.effects = effects


class Battle:
    """Manages a combat encounter."""

    def __init__(self, player: 'PlayerCharacter', enemies: List[Enemy]):
        """
        Initialize battle.

        Args:
            player: Player character
            enemies: List of enemy combatants
        """
        self.player = player
        self.enemies = enemies
        self.turn_number = 0
        self.battle_log: List[BattleTurn] = []
        self.result = BattleResult.ONGOING

        self.action_registry = ActionRegistry()

        # Initialize enemy AI
        self.enemy_ais = [EnemyAI(enemy) for enemy in enemies]

        # Combat state
        self.player_defending = False

    def start(self) -> Dict[str, Any]:
        """
        Start the battle.

        Returns:
            Battle start info
        """
        # Determine initiative order
        player_initiative = self.player.derived_stats.initiative
        enemy_names = [enemy.name for enemy in self.enemies]

        return {
            'player_initiative': player_initiative,
            'enemies': enemy_names,
            'enemy_count': len(self.enemies),
            'message': f"Battle begins against {len(self.enemies)} enemies!"
        }

    def player_turn(self, action_name: str, target_index: int = 0) -> Dict[str, Any]:
        """
        Execute player's turn.

        Args:
            action_name: Name of action to perform
            target_index: Index of enemy to target

        Returns:
            Turn result dictionary
        """
        if self.result != BattleResult.ONGOING:
            return {'error': 'Battle is already over'}

        # Get action
        action = self.action_registry.get_action_by_name(action_name, self.player)
        if not action:
            return {'error': f'Unknown or unavailable action: {action_name}'}

        # Check if can use
        can_use, reason = action.can_use(self.player)
        if not can_use:
            return {'error': reason}

        # Get target
        if action.requires_target:
            if target_index >= len(self.enemies) or target_index < 0:
                return {'error': 'Invalid target'}
            target = self.enemies[target_index]
        else:
            target = None

        # Execute action
        result = self._execute_player_action(action, target)

        # Check for victory
        if all(not enemy.is_alive() for enemy in self.enemies):
            self.result = BattleResult.VICTORY
            result['battle_result'] = BattleResult.VICTORY
            result['rewards'] = self._calculate_rewards()

        return result

    def _execute_player_action(self, action: CombatAction, target: Optional[Enemy]) -> Dict[str, Any]:
        """Execute a player combat action."""
        result = {
            'action': action.name,
            'damage': 0,
            'effects': [],
            'message': ''
        }

        # Handle different action types
        if action.name in ["Light Attack", "Attack", "Heavy Attack", "Staff Attack"]:
            attack_type_map = {
                "Light Attack": AttackType.LIGHT,
                "Attack": AttackType.NORMAL,
                "Heavy Attack": AttackType.HEAVY,
                "Staff Attack": AttackType.NORMAL
            }
            attack_type = attack_type_map.get(action.name, AttackType.NORMAL)

            # Base weapon damage
            base_damage = 15  # TODO: Get from equipped weapon

            damage, hit, crit = DamageCalculator.calculate_physical_damage(
                self.player.attributes.strength,
                target.get_combat_stats()['defense'],
                base_damage,
                attack_type
            )

            if hit:
                target.take_damage(damage)
                result['damage'] = damage
                result['hit'] = True
                result['critical'] = crit
                result['target'] = target.name

                if crit:
                    result['message'] = f"CRITICAL HIT! You deal {damage} damage to {target.name}!"
                else:
                    result['message'] = f"You deal {damage} damage to {target.name}!"
            else:
                result['hit'] = False
                result['message'] = "Your attack misses!"

        elif action.name == "Power Strike":
            base_damage = 25
            damage, hit, crit = DamageCalculator.calculate_physical_damage(
                self.player.attributes.strength,
                target.get_combat_stats()['defense'],
                base_damage,
                AttackType.HEAVY
            )

            if hit:
                target.take_damage(damage)
                result['damage'] = damage
                result['hit'] = True
                result['critical'] = crit
                result['target'] = target.name

                # 30% chance to cause bleeding
                if random.random() < 0.3:
                    bleeding = create_bleeding()
                    target.effect_manager.add_effect(bleeding)
                    result['effects'].append('bleeding')

                result['message'] = f"Powerful strike! {damage} damage to {target.name}!"
            else:
                result['hit'] = False
                result['message'] = "Your power strike misses!"

        elif action.name == "Shield Bash":
            damage, hit, crit = DamageCalculator.calculate_physical_damage(
                self.player.attributes.strength,
                target.get_combat_stats()['defense'],
                10,  # Low damage
                AttackType.NORMAL
            )

            if hit:
                target.take_damage(damage)
                result['damage'] = damage
                result['hit'] = True
                result['target'] = target.name

                # 50% chance to stun
                if random.random() < 0.5:
                    stun = create_stun()
                    target.effect_manager.add_effect(stun)
                    result['effects'].append('stunned')
                    result['message'] = f"Shield bash! {damage} damage and {target.name} is stunned!"
                else:
                    result['message'] = f"Shield bash! {damage} damage to {target.name}!"
            else:
                result['hit'] = False
                result['message'] = "Your shield bash misses!"

        elif action.name == "Defend":
            self.player_defending = True
            result['message'] = "You take a defensive stance!"

        elif action.name in ["Minor Fireball", "Greater Fireball", "Lightning Bolt"]:
            base_damage_map = {
                "Minor Fireball": 20,
                "Greater Fireball": 40,
                "Lightning Bolt": 35
            }
            base_damage = base_damage_map[action.name]

            damage, crit = DamageCalculator.calculate_magical_damage(
                self.player.attributes.intelligence,
                self.player.attributes.willpower,
                target.attributes.willpower,
                base_damage
            )

            target.take_damage(damage)
            result['damage'] = damage
            result['critical'] = crit
            result['target'] = target.name

            if crit:
                result['message'] = f"CRITICAL! Your {action.name} deals {damage} damage!"
            else:
                result['message'] = f"Your {action.name} deals {damage} damage to {target.name}!"

        elif action.name == "Heal":
            healing = DamageCalculator.calculate_healing(
                self.player.attributes.willpower,
                30  # Base healing
            )
            self.player.heal(healing)
            result['healing'] = healing
            result['message'] = f"You restore {healing} health!"

        elif action.name == "Shield":
            from .effects import create_shield
            shield = create_shield()
            self.player.effect_manager.add_effect(shield)
            result['effects'].append('shielded')
            result['message'] = "A magical shield surrounds you!"

        else:
            result['message'] = f"You use {action.name}! (not fully implemented)"

        return result

    def enemy_turn(self, enemy_index: int) -> Dict[str, Any]:
        """
        Execute an enemy's turn.

        Args:
            enemy_index: Index of enemy taking turn

        Returns:
            Turn result dictionary
        """
        enemy = self.enemies[enemy_index]
        ai = self.enemy_ais[enemy_index]

        if not enemy.is_alive():
            return {'skipped': True, 'reason': 'Enemy is defeated'}

        # Apply status effects
        effect_results = enemy.effect_manager.tick_effects()
        effect_damage = sum(dmg for dmg in effect_results.values() if dmg > 0)

        if effect_damage > 0:
            enemy.take_damage(effect_damage)

        # Check if incapacitated
        if enemy.effect_manager.is_incapacitated():
            return {
                'enemy': enemy.name,
                'action': 'incapacitated',
                'message': f"{enemy.name} is incapacitated and cannot act!"
            }

        # Choose and execute action
        player_health_pct = self.player.derived_stats.current_health / self.player.derived_stats.max_health
        action = ai.choose_action(player_health_pct)

        combat_stats = self.player.get_combat_stats()
        result = ai.execute_action(action, combat_stats['defense'])
        result['enemy'] = enemy.name

        # Apply damage to player if any
        if result.get('damage', 0) > 0 and result.get('hit', True):
            # Apply defense reduction if player is defending
            damage = result['damage']
            if self.player_defending:
                damage = int(damage * 0.5)  # 50% damage reduction
                result['message'] += " (reduced by defense)"

            self.player.take_damage(damage)

        return result

    def attempt_flee(self) -> Dict[str, Any]:
        """
        Attempt to flee from battle.

        Returns:
            Flee attempt result
        """
        # Calculate average enemy agility
        avg_enemy_agi = sum(e.attributes.agility for e in self.enemies if e.is_alive()) / len([e for e in self.enemies if e.is_alive()])

        flee_chance = DamageCalculator.calculate_flee_chance(
            self.player.attributes.agility,
            int(avg_enemy_agi)
        )

        if random.random() < flee_chance:
            self.result = BattleResult.FLED
            return {
                'success': True,
                'message': "You successfully flee from battle!",
                'battle_result': BattleResult.FLED
            }
        else:
            return {
                'success': False,
                'message': "Failed to escape! The enemies block your path!"
            }

    def _calculate_rewards(self) -> Dict[str, Any]:
        """Calculate rewards for victory."""
        total_xp = sum(enemy.xp_reward for enemy in self.enemies)
        total_gold = sum(enemy.gold_reward for enemy in self.enemies)

        return {
            'xp': total_xp,
            'gold': total_gold
        }

    def get_battle_state(self) -> Dict[str, Any]:
        """Get current battle state."""
        return {
            'turn': self.turn_number,
            'result': self.result,
            'player': {
                'health': f"{self.player.derived_stats.current_health}/{self.player.derived_stats.max_health}",
                'mana': f"{self.player.derived_stats.current_mana}/{self.player.derived_stats.max_mana}",
                'stamina': f"{self.player.derived_stats.current_stamina}/{self.player.derived_stats.max_stamina}",
                'effects': [e.effect_type.value for e in self.player.effect_manager.get_all_effects()]
            },
            'enemies': [
                {
                    'name': enemy.name,
                    'health': f"{enemy.derived_stats.current_health}/{enemy.derived_stats.max_health}",
                    'alive': enemy.is_alive(),
                    'effects': [e.effect_type.value for e in enemy.effect_manager.get_all_effects()]
                }
                for enemy in self.enemies
            ]
        }

    def next_turn(self):
        """Advance to next turn."""
        self.turn_number += 1
        self.player_defending = False  # Reset defense stance
