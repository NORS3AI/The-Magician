"""Enemy classes and AI behavior."""

from typing import Optional, Dict, Any, List
import random

from ..character.stats import CoreAttributes, DerivedStats, StatCalculator
from .effects import EffectManager, StatusEffect
from .damage import DamageCalculator, AttackType


class Enemy:
    """Represents an enemy combatant."""

    def __init__(
        self,
        name: str,
        level: int,
        attributes: CoreAttributes,
        base_damage: int = 10,
        xp_reward: int = None,
        gold_reward: int = None,
        abilities: List[str] = None
    ):
        """
        Initialize enemy.

        Args:
            name: Enemy name
            level: Enemy level
            attributes: Core attributes
            base_damage: Base attack damage
            xp_reward: XP rewarded on defeat
            gold_reward: Gold rewarded on defeat
            abilities: List of special abilities
        """
        self.name = name
        self.level = level
        self.attributes = attributes
        self.base_damage = base_damage
        self.abilities = abilities or []

        # Calculate derived stats
        self.derived_stats = StatCalculator.calculate_all_derived_stats(attributes, level)

        # Rewards
        self.xp_reward = xp_reward if xp_reward is not None else 50 * level
        self.gold_reward = gold_reward if gold_reward is not None else 10 * level

        # Combat state
        self.effect_manager = EffectManager()
        self.is_defending = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Enemy':
        """
        Create enemy from dictionary data.

        Args:
            data: Enemy data dict

        Returns:
            Enemy instance
        """
        attributes = CoreAttributes.from_dict(data.get('attributes', {}))

        return cls(
            name=data['name'],
            level=data.get('level', 1),
            attributes=attributes,
            base_damage=data.get('base_damage', 10),
            xp_reward=data.get('xp_reward'),
            gold_reward=data.get('gold_reward'),
            abilities=data.get('abilities', [])
        )

    def is_alive(self) -> bool:
        """Check if enemy is alive."""
        return self.derived_stats.current_health > 0

    def take_damage(self, amount: int) -> bool:
        """
        Take damage.

        Args:
            amount: Damage amount

        Returns:
            True if still alive
        """
        # Apply defense modifier from effects
        defense_mod = self.effect_manager.get_defense_modifier()
        modified_damage = int(amount / defense_mod)

        self.derived_stats.current_health = max(0, self.derived_stats.current_health - modified_damage)
        return self.is_alive()

    def heal(self, amount: int):
        """Heal the enemy."""
        self.derived_stats.current_health = min(
            self.derived_stats.max_health,
            self.derived_stats.current_health + amount
        )

    def get_combat_stats(self) -> Dict[str, int]:
        """Get combat-relevant stats."""
        return {
            'physical_damage_bonus': StatCalculator.calculate_physical_damage_bonus(self.attributes.strength),
            'defense': StatCalculator.calculate_defense(self.attributes.agility, self.attributes.constitution),
            'initiative': self.derived_stats.initiative
        }


class EnemyAI:
    """AI behavior for enemies."""

    def __init__(self, enemy: Enemy):
        """
        Initialize enemy AI.

        Args:
            enemy: Enemy to control
        """
        self.enemy = enemy
        self.aggression = 0.7  # 70% chance to attack vs defend

    def choose_action(self, player_health_percent: float) -> str:
        """
        Choose an action for the enemy.

        Args:
            player_health_percent: Player's health as percentage (0.0 to 1.0)

        Returns:
            Action name
        """
        # Check if incapacitated
        if self.enemy.effect_manager.is_incapacitated():
            return "incapacitated"

        # If enemy is low health, higher chance to defend or use special
        enemy_health_percent = (
            self.enemy.derived_stats.current_health /
            self.enemy.derived_stats.max_health
        )

        # Low health defensive behavior
        if enemy_health_percent < 0.3:
            if random.random() < 0.4:  # 40% chance to defend when low
                return "defend"

        # Check for special abilities
        if self.enemy.abilities and random.random() < 0.3:  # 30% chance to use special
            return random.choice(["special"] + ["attack", "attack"])  # Weighted toward attack

        # Normal behavior based on aggression
        if random.random() < self.aggression:
            # Choose attack type
            attack_roll = random.random()
            if attack_roll < 0.1:
                return "heavy_attack"
            elif attack_roll < 0.3:
                return "light_attack"
            else:
                return "attack"
        else:
            return "defend"

    def execute_action(
        self,
        action: str,
        target_defense: int
    ) -> Dict[str, Any]:
        """
        Execute chosen action.

        Args:
            action: Action to execute
            target_defense: Target's defense value

        Returns:
            Dict with action results
        """
        if action == "incapacitated":
            return {
                'action': action,
                'damage': 0,
                'message': f"{self.enemy.name} is incapacitated!"
            }

        if action == "defend":
            self.enemy.is_defending = True
            return {
                'action': action,
                'damage': 0,
                'message': f"{self.enemy.name} takes a defensive stance!"
            }

        if action in ["attack", "light_attack", "heavy_attack"]:
            attack_type = {
                "light_attack": AttackType.LIGHT,
                "attack": AttackType.NORMAL,
                "heavy_attack": AttackType.HEAVY
            }[action]

            # Get damage modifier from effects
            damage_mod = self.enemy.effect_manager.get_damage_modifier()

            damage, hit, crit = DamageCalculator.calculate_physical_damage(
                self.enemy.attributes.strength,
                target_defense,
                int(self.enemy.base_damage * damage_mod),
                attack_type
            )

            message = f"{self.enemy.name} attacks!"
            if not hit:
                message = f"{self.enemy.name}'s attack misses!"
            elif crit:
                message = f"{self.enemy.name} lands a CRITICAL hit!"

            return {
                'action': action,
                'damage': damage,
                'hit': hit,
                'critical': crit,
                'message': message
            }

        if action == "special":
            # Generic special ability
            damage, crit = DamageCalculator.calculate_magical_damage(
                self.enemy.attributes.intelligence,
                self.enemy.attributes.willpower,
                10,  # Base resistance
                int(self.enemy.base_damage * 1.5),  # 150% damage
            )

            return {
                'action': action,
                'damage': damage,
                'critical': crit,
                'message': f"{self.enemy.name} uses a special ability!"
            }

        return {
            'action': 'unknown',
            'damage': 0,
            'message': f"{self.enemy.name} does nothing."
        }


# Predefined enemy templates
def create_goblin(level: int = 1) -> Enemy:
    """Create a goblin enemy."""
    attributes = CoreAttributes(
        strength=8 + level,
        constitution=7 + level,
        agility=12 + level,
        intelligence=6,
        willpower=5,
        charisma=4
    )

    return Enemy(
        name="Goblin",
        level=level,
        attributes=attributes,
        base_damage=5 + level * 2,
        abilities=["Quick Strike"]
    )


def create_orc(level: int = 3) -> Enemy:
    """Create an orc enemy."""
    attributes = CoreAttributes(
        strength=14 + level,
        constitution=12 + level,
        agility=8 + level,
        intelligence=6,
        willpower=7,
        charisma=5
    )

    return Enemy(
        name="Orc Warrior",
        level=level,
        attributes=attributes,
        base_damage=10 + level * 3,
        abilities=["Brutal Strike", "War Cry"]
    )


def create_troll(level: int = 5) -> Enemy:
    """Create a troll enemy."""
    attributes = CoreAttributes(
        strength=16 + level,
        constitution=18 + level,
        agility=6 + level,
        intelligence=4,
        willpower=8,
        charisma=3
    )

    return Enemy(
        name="Troll",
        level=level,
        attributes=attributes,
        base_damage=15 + level * 4,
        abilities=["Regeneration", "Smash"]
    )


def create_dark_mage(level: int = 7) -> Enemy:
    """Create a dark mage enemy."""
    attributes = CoreAttributes(
        strength=8 + level,
        constitution=10 + level,
        agility=10 + level,
        intelligence=16 + level,
        willpower=14 + level,
        charisma=8
    )

    return Enemy(
        name="Dark Mage",
        level=level,
        attributes=attributes,
        base_damage=8 + level * 2,
        abilities=["Shadow Bolt", "Dark Shield", "Life Drain"]
    )


def create_dragon(level: int = 15) -> Enemy:
    """Create a dragon boss."""
    attributes = CoreAttributes(
        strength=22 + level,
        constitution=24 + level,
        agility=12 + level,
        intelligence=18 + level,
        willpower=20 + level,
        charisma=16
    )

    return Enemy(
        name="Ancient Dragon",
        level=level,
        attributes=attributes,
        base_damage=30 + level * 5,
        xp_reward=500 * level,
        gold_reward=100 * level,
        abilities=["Fire Breath", "Tail Sweep", "Dragon Fear", "Ancient Magic"]
    )
