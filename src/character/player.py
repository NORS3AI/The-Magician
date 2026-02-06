"""Player character class and management."""

from typing import Dict, List, Optional, Any
from datetime import datetime

from .stats import CoreAttributes, DerivedStats, StatCalculator
from .progression import ExperienceSystem, AbilitySystem, LevelUpManager
from ..magic import SpellBook, get_spell_registry


class PlayerCharacter:
    """Represents the player's character."""

    def __init__(
        self,
        username: str,
        character_name: str,
        path: str,
        attributes: CoreAttributes,
        level: int = 1,
        xp: int = 0
    ):
        """
        Initialize player character.

        Args:
            username: Account username
            character_name: Display name (Tomas/Pug)
            path: Character path ("tomas" or "pug")
            attributes: Core attributes
            level: Starting level
            xp: Starting experience points
        """
        self.username = username
        self.character_name = character_name
        self.path = path.lower()

        # Core stats
        self.attributes = attributes
        self.level = level
        self.xp = xp

        # Derived stats
        self.derived_stats = StatCalculator.calculate_all_derived_stats(self.attributes, self.level)

        # Progression
        self.unspent_stat_points = 0
        self.abilities = AbilitySystem.get_abilities_for_level(self.path, self.level)

        # Magic system
        self.spellbook = SpellBook()
        self._learn_starting_spells()

        # Inventory
        self.inventory: List[Dict] = []
        self.equipped: Dict[str, Optional[str]] = {
            'weapon': None,
            'armor': None,
            'accessory': None
        }

        # Location and state
        self.location = "crydee"
        self.gold = 0

        # Timestamps
        self.created_at = datetime.utcnow().isoformat()
        self.last_played = datetime.utcnow().isoformat()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PlayerCharacter':
        """
        Create PlayerCharacter from dictionary.

        Args:
            data: Character data dict

        Returns:
            PlayerCharacter instance
        """
        attributes = CoreAttributes.from_dict(data.get('attributes', {}))

        player = cls(
            username=data['username'],
            character_name=data['character_name'],
            path=data['path'],
            attributes=attributes,
            level=data.get('level', 1),
            xp=data.get('xp', 0)
        )

        # Load derived stats
        if 'derived_stats' in data:
            derived_data = data['derived_stats']
            player.derived_stats.current_health = derived_data.get('current_health', player.derived_stats.max_health)
            player.derived_stats.current_mana = derived_data.get('current_mana', player.derived_stats.max_mana)
            player.derived_stats.current_stamina = derived_data.get('current_stamina', player.derived_stats.max_stamina)

        # Load progression
        player.unspent_stat_points = data.get('unspent_stat_points', 0)
        player.abilities = data.get('abilities', player.abilities)

        # Load spells
        if 'known_spells' in data:
            registry = get_spell_registry()
            for spell_name in data['known_spells']:
                spell = registry.get(spell_name)
                if spell:
                    player.spellbook.learn_spell(spell)

        if 'equipped_spells' in data:
            registry = get_spell_registry()
            # Clear auto-equipped spells first
            player.spellbook.equipped_spells.clear()
            for spell_name in data['equipped_spells']:
                spell = registry.get(spell_name)
                if spell:
                    player.spellbook.equip_spell(spell)

        # Load inventory
        player.inventory = data.get('inventory', [])
        player.equipped = data.get('equipped', player.equipped)

        # Load state
        player.location = data.get('location', 'crydee')
        player.gold = data.get('gold', 0)

        # Load timestamps
        player.created_at = data.get('created_at', player.created_at)
        player.last_played = data.get('last_played', player.last_played)

        return player

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert player character to dictionary.

        Returns:
            Character data dict
        """
        return {
            'username': self.username,
            'character_name': self.character_name,
            'path': self.path,
            'level': self.level,
            'xp': self.xp,
            'attributes': self.attributes.to_dict(),
            'derived_stats': self.derived_stats.to_dict(),
            'unspent_stat_points': self.unspent_stat_points,
            'abilities': self.abilities,
            'known_spells': [spell.name for spell in self.spellbook.known_spells],
            'equipped_spells': [spell.name for spell in self.spellbook.equipped_spells],
            'inventory': self.inventory,
            'equipped': self.equipped,
            'location': self.location,
            'gold': self.gold,
            'created_at': self.created_at,
            'last_played': self.last_played
        }

    def gain_xp(self, amount: int) -> Optional[Dict[str, Any]]:
        """
        Gain experience points and check for level up.

        Args:
            amount: XP to gain

        Returns:
            Level up info dict if leveled up, None otherwise
        """
        old_xp = self.xp
        self.xp += amount

        level_up_mgr = LevelUpManager()
        new_level = level_up_mgr.check_level_up(old_xp, self.xp, self.level)

        if new_level:
            return self.level_up(new_level)

        return None

    def level_up(self, new_level: int) -> Dict[str, Any]:
        """
        Level up character.

        Args:
            new_level: New character level

        Returns:
            Level up info dict
        """
        old_level = self.level
        self.level = new_level

        level_up_mgr = LevelUpManager()
        level_up_info = level_up_mgr.process_level_up(old_level, new_level, self.path)

        # Grant stat points
        self.unspent_stat_points += level_up_info['stat_points']

        # Grant new abilities
        new_abilities = level_up_info['new_abilities']
        self.abilities.extend(new_abilities)

        # Recalculate derived stats
        self._recalculate_derived_stats()

        # Restore health, mana, and stamina on level up
        self.derived_stats.current_health = self.derived_stats.max_health
        self.derived_stats.current_mana = self.derived_stats.max_mana
        self.derived_stats.current_stamina = self.derived_stats.max_stamina

        # Learn new spells if available
        new_spells = self.learn_new_spells_for_level()
        if new_spells:
            level_up_info['new_spells'] = new_spells

        return level_up_info

    def spend_stat_points(self, allocations: Dict[str, int]) -> bool:
        """
        Spend stat points to increase attributes.

        Args:
            allocations: Dict of attribute name to points to spend

        Returns:
            True if successful
        """
        total_spent = sum(allocations.values())

        if total_spent > self.unspent_stat_points:
            return False

        # Apply stat increases
        for stat, points in allocations.items():
            if stat == 'strength':
                self.attributes.strength += points
            elif stat == 'constitution':
                self.attributes.constitution += points
            elif stat == 'agility':
                self.attributes.agility += points
            elif stat == 'intelligence':
                self.attributes.intelligence += points
            elif stat == 'willpower':
                self.attributes.willpower += points
            elif stat == 'charisma':
                self.attributes.charisma += points

        # Deduct spent points
        self.unspent_stat_points -= total_spent

        # Recalculate derived stats
        self._recalculate_derived_stats()

        return True

    def _recalculate_derived_stats(self):
        """Recalculate all derived stats from current attributes and level."""
        # Store current values as percentages
        health_pct = self.derived_stats.current_health / self.derived_stats.max_health if self.derived_stats.max_health > 0 else 1.0
        mana_pct = self.derived_stats.current_mana / self.derived_stats.max_mana if self.derived_stats.max_mana > 0 else 1.0
        stamina_pct = self.derived_stats.current_stamina / self.derived_stats.max_stamina if self.derived_stats.max_stamina > 0 else 1.0

        # Recalculate maximums
        self.derived_stats = StatCalculator.calculate_all_derived_stats(self.attributes, self.level)

        # Restore percentages
        self.derived_stats.current_health = int(self.derived_stats.max_health * health_pct)
        self.derived_stats.current_mana = int(self.derived_stats.max_mana * mana_pct)
        self.derived_stats.current_stamina = int(self.derived_stats.max_stamina * stamina_pct)

    def take_damage(self, amount: int) -> bool:
        """
        Take damage.

        Args:
            amount: Damage amount

        Returns:
            True if still alive, False if dead
        """
        self.derived_stats.current_health = max(0, self.derived_stats.current_health - amount)
        return self.derived_stats.current_health > 0

    def heal(self, amount: int):
        """
        Heal health.

        Args:
            amount: Heal amount
        """
        self.derived_stats.current_health = min(
            self.derived_stats.max_health,
            self.derived_stats.current_health + amount
        )

    def use_mana(self, amount: int) -> bool:
        """
        Use mana.

        Args:
            amount: Mana cost

        Returns:
            True if enough mana, False otherwise
        """
        if self.derived_stats.current_mana >= amount:
            self.derived_stats.current_mana -= amount
            return True
        return False

    def restore_mana(self, amount: int):
        """
        Restore mana.

        Args:
            amount: Mana to restore
        """
        self.derived_stats.current_mana = min(
            self.derived_stats.max_mana,
            self.derived_stats.current_mana + amount
        )

    def use_stamina(self, amount: int) -> bool:
        """
        Use stamina.

        Args:
            amount: Stamina cost

        Returns:
            True if enough stamina, False otherwise
        """
        if self.derived_stats.current_stamina >= amount:
            self.derived_stats.current_stamina -= amount
            return True
        return False

    def restore_stamina(self, amount: int):
        """
        Restore stamina.

        Args:
            amount: Stamina to restore
        """
        self.derived_stats.current_stamina = min(
            self.derived_stats.max_stamina,
            self.derived_stats.current_stamina + amount
        )

    def rest(self):
        """Fully restore health, mana, and stamina."""
        self.derived_stats.current_health = self.derived_stats.max_health
        self.derived_stats.current_mana = self.derived_stats.max_mana
        self.derived_stats.current_stamina = self.derived_stats.max_stamina

    def is_alive(self) -> bool:
        """Check if character is alive."""
        return self.derived_stats.current_health > 0

    def has_ability(self, ability_name: str) -> bool:
        """
        Check if character has an ability.

        Args:
            ability_name: Ability name

        Returns:
            True if character has ability
        """
        return ability_name in self.abilities

    def get_xp_progress(self) -> Dict[str, Any]:
        """
        Get XP progress information.

        Returns:
            Dict with XP progress info
        """
        progress, needed = ExperienceSystem.get_progress_to_next_level(self.xp, self.level)
        percentage = ExperienceSystem.get_progress_percentage(self.xp, self.level)

        return {
            'total_xp': self.xp,
            'current_level': self.level,
            'progress_xp': progress,
            'needed_xp': needed,
            'percentage': percentage
        }

    def get_combat_stats(self) -> Dict[str, int]:
        """
        Get combat-relevant stats.

        Returns:
            Dict of combat stats
        """
        return {
            'physical_damage_bonus': StatCalculator.calculate_physical_damage_bonus(self.attributes.strength),
            'magical_damage_bonus': StatCalculator.calculate_magical_damage_bonus(self.attributes.intelligence),
            'defense': StatCalculator.calculate_defense(self.attributes.agility, self.attributes.constitution),
            'spell_power': StatCalculator.calculate_spell_power(self.attributes.intelligence, self.attributes.willpower),
            'initiative': self.derived_stats.initiative
        }

    def _learn_starting_spells(self):
        """Learn starting spells based on path."""
        if self.path != "pug":
            return  # Only Pug starts with spells

        registry = get_spell_registry()

        # Pug starts with basic spells
        starting_spells = ["Minor Firebolt", "Minor Heal", "Light"]

        for spell_name in starting_spells:
            spell = registry.get(spell_name)
            if spell:
                self.spellbook.learn_spell(spell)

    def learn_new_spells_for_level(self):
        """Check and learn new spells available at current level."""
        if self.path != "pug":
            return []

        registry = get_spell_registry()
        learnable = registry.get_learnable(
            self.level,
            self.attributes.intelligence,
            self.attributes.willpower
        )

        # Filter out already known spells
        new_spells = []
        for spell in learnable:
            if spell not in self.spellbook.known_spells:
                # Auto-learn spells that meet requirements
                if self.spellbook.learn_spell(spell):
                    new_spells.append(spell.name)

        return new_spells

    def can_cast_spell(self, spell_name: str) -> tuple[bool, str]:
        """
        Check if can cast a spell.

        Args:
            spell_name: Name of the spell

        Returns:
            Tuple of (can_cast, reason)
        """
        spell = self.spellbook.get_spell_by_name(spell_name)

        if not spell:
            return False, "You don't know that spell"

        mana_cost = spell.get_mana_cost(self.level)

        if self.derived_stats.current_mana < mana_cost:
            return False, f"Not enough mana (need {mana_cost}, have {self.derived_stats.current_mana})"

        return True, ""

    def cast_spell(self, spell_name: str, target=None, **kwargs) -> Dict[str, Any]:
        """
        Cast a spell.

        Args:
            spell_name: Name of the spell
            target: Target of the spell
            **kwargs: Additional spell parameters

        Returns:
            Dict with cast results
        """
        can_cast, reason = self.can_cast_spell(spell_name)

        if not can_cast:
            return {'success': False, 'message': reason}

        spell = self.spellbook.get_spell_by_name(spell_name)
        mana_cost = spell.get_mana_cost(self.level)

        # Cast the spell
        result = spell.cast(self, target, **kwargs)

        # Deduct mana if successful
        if result.get('success'):
            self.use_mana(mana_cost)

        return result

    def update_last_played(self):
        """Update last played timestamp."""
        self.last_played = datetime.utcnow().isoformat()
