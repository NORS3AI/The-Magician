"""Spell base classes and spell casting mechanics."""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable, Any
import logging

logger = logging.getLogger(__name__)


class SpellCategory(Enum):
    """Categories of spells."""
    OFFENSIVE = auto()
    DEFENSIVE = auto()
    UTILITY = auto()
    GREATER = auto()


class ElementType(Enum):
    """Elemental types for spells."""
    FIRE = auto()
    ICE = auto()
    LIGHTNING = auto()
    ARCANE = auto()
    NATURE = auto()
    DARK = auto()
    LIGHT = auto()
    NONE = auto()


class TargetType(Enum):
    """Spell targeting types."""
    SELF = auto()
    SINGLE_ENEMY = auto()
    ALL_ENEMIES = auto()
    SINGLE_ALLY = auto()
    ALL_ALLIES = auto()
    AREA = auto()


@dataclass
class SpellEffect:
    """Effect produced by a spell."""
    effect_type: str
    value: int
    duration: int = 0
    element: ElementType = ElementType.NONE


class Spell:
    """
    Base spell class.

    All spells inherit from this class and implement their specific effects.
    """

    def __init__(
        self,
        name: str,
        description: str,
        category: SpellCategory,
        element: ElementType,
        target_type: TargetType,
        base_mana_cost: int,
        min_level: int = 1,
        intelligence_requirement: int = 0,
        willpower_requirement: int = 0,
        scaling_stat: str = "intelligence"
    ):
        """
        Initialize a spell.

        Args:
            name: Spell name
            description: Spell description
            category: Spell category
            element: Elemental type
            target_type: Targeting type
            base_mana_cost: Base mana cost to cast
            min_level: Minimum level required to learn
            intelligence_requirement: Minimum intelligence required
            willpower_requirement: Minimum willpower required
            scaling_stat: Which stat scales spell power
        """
        self.name = name
        self.description = description
        self.category = category
        self.element = element
        self.target_type = target_type
        self.base_mana_cost = base_mana_cost
        self.min_level = min_level
        self.intelligence_requirement = intelligence_requirement
        self.willpower_requirement = willpower_requirement
        self.scaling_stat = scaling_stat

    def can_learn(self, player_level: int, intelligence: int, willpower: int) -> bool:
        """
        Check if a player can learn this spell.

        Args:
            player_level: Player's current level
            intelligence: Player's intelligence
            willpower: Player's willpower

        Returns:
            True if player meets requirements
        """
        return (
            player_level >= self.min_level and
            intelligence >= self.intelligence_requirement and
            willpower >= self.willpower_requirement
        )

    def get_mana_cost(self, caster_level: int) -> int:
        """
        Calculate mana cost based on caster level.

        Higher level casters use spells more efficiently.

        Args:
            caster_level: Caster's level

        Returns:
            Mana cost to cast
        """
        # Cost reduces slightly with level (min 70% of base cost)
        reduction = min(0.3, (caster_level - self.min_level) * 0.02)
        return max(int(self.base_mana_cost * (1 - reduction)), 1)

    def get_power(self, scaling_value: int, caster_level: int) -> int:
        """
        Calculate spell power based on scaling stat and level.

        Args:
            scaling_value: Value of the scaling stat (int or will)
            caster_level: Caster's level

        Returns:
            Spell power value
        """
        # Base power from stat
        stat_power = scaling_value * 2

        # Level scaling
        level_power = caster_level * 3

        return stat_power + level_power

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        """
        Cast the spell.

        This should be overridden by specific spell implementations.

        Args:
            caster: The character casting the spell
            target: The target of the spell (if applicable)
            **kwargs: Additional parameters

        Returns:
            Dictionary with cast results
        """
        return {
            'success': False,
            'message': f"{self.name} has no implementation",
            'effects': []
        }


class SpellBook:
    """Manages a character's known spells."""

    def __init__(self):
        """Initialize an empty spellbook."""
        self.known_spells: List[Spell] = []
        self.equipped_spells: List[Spell] = []
        self.max_equipped: int = 8

    def learn_spell(self, spell: Spell) -> bool:
        """
        Learn a new spell.

        Args:
            spell: Spell to learn

        Returns:
            True if spell was learned, False if already known
        """
        if spell in self.known_spells:
            return False

        self.known_spells.append(spell)

        # Auto-equip if slots available
        if len(self.equipped_spells) < self.max_equipped:
            self.equipped_spells.append(spell)

        return True

    def forget_spell(self, spell: Spell) -> bool:
        """
        Forget a spell.

        Args:
            spell: Spell to forget

        Returns:
            True if spell was forgotten
        """
        if spell not in self.known_spells:
            return False

        self.known_spells.remove(spell)

        if spell in self.equipped_spells:
            self.equipped_spells.remove(spell)

        return True

    def equip_spell(self, spell: Spell) -> bool:
        """
        Equip a spell for quick access.

        Args:
            spell: Spell to equip

        Returns:
            True if spell was equipped
        """
        if spell not in self.known_spells:
            return False

        if spell in self.equipped_spells:
            return False

        if len(self.equipped_spells) >= self.max_equipped:
            return False

        self.equipped_spells.append(spell)
        return True

    def unequip_spell(self, spell: Spell) -> bool:
        """
        Unequip a spell.

        Args:
            spell: Spell to unequip

        Returns:
            True if spell was unequipped
        """
        if spell not in self.equipped_spells:
            return False

        self.equipped_spells.remove(spell)
        return True

    def get_spell_by_name(self, name: str) -> Optional[Spell]:
        """
        Get a spell by name from known spells.

        Args:
            name: Spell name (case-insensitive)

        Returns:
            Spell if found, None otherwise
        """
        name_lower = name.lower()
        for spell in self.known_spells:
            if spell.name.lower() == name_lower:
                return spell
        return None

    def get_spells_by_category(self, category: SpellCategory) -> List[Spell]:
        """
        Get all known spells of a category.

        Args:
            category: Spell category

        Returns:
            List of spells in category
        """
        return [s for s in self.known_spells if s.category == category]


class SpellRegistry:
    """Registry for all available spells in the game."""

    def __init__(self):
        """Initialize empty spell registry."""
        self._spells: Dict[str, Spell] = {}

    def register(self, spell: Spell) -> None:
        """
        Register a spell.

        Args:
            spell: Spell to register
        """
        self._spells[spell.name.lower()] = spell
        logger.debug(f"Registered spell: {spell.name}")

    def get(self, name: str) -> Optional[Spell]:
        """
        Get a spell by name.

        Args:
            name: Spell name (case-insensitive)

        Returns:
            Spell if found, None otherwise
        """
        return self._spells.get(name.lower())

    def get_all(self) -> List[Spell]:
        """
        Get all registered spells.

        Returns:
            List of all spells
        """
        return list(self._spells.values())

    def get_by_category(self, category: SpellCategory) -> List[Spell]:
        """
        Get all spells of a category.

        Args:
            category: Spell category

        Returns:
            List of spells in category
        """
        return [s for s in self._spells.values() if s.category == category]

    def get_learnable(
        self,
        player_level: int,
        intelligence: int,
        willpower: int
    ) -> List[Spell]:
        """
        Get all spells a player can currently learn.

        Args:
            player_level: Player's level
            intelligence: Player's intelligence
            willpower: Player's willpower

        Returns:
            List of learnable spells
        """
        return [
            s for s in self._spells.values()
            if s.can_learn(player_level, intelligence, willpower)
        ]


# Global spell registry
_spell_registry = SpellRegistry()


def get_spell_registry() -> SpellRegistry:
    """Get the global spell registry."""
    return _spell_registry
