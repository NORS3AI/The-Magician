"""Character attributes and stat calculations."""

from dataclasses import dataclass
from typing import Dict
import math


@dataclass
class CoreAttributes:
    """Core character attributes."""
    strength: int
    constitution: int
    agility: int
    intelligence: int
    willpower: int
    charisma: int

    def to_dict(self) -> Dict[str, int]:
        """Convert to dictionary."""
        return {
            'strength': self.strength,
            'constitution': self.constitution,
            'agility': self.agility,
            'intelligence': self.intelligence,
            'willpower': self.willpower,
            'charisma': self.charisma
        }

    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> 'CoreAttributes':
        """Create from dictionary."""
        return cls(
            strength=data.get('strength', 10),
            constitution=data.get('constitution', 10),
            agility=data.get('agility', 10),
            intelligence=data.get('intelligence', 10),
            willpower=data.get('willpower', 10),
            charisma=data.get('charisma', 10)
        )

    def get_total(self) -> int:
        """Get total of all attributes."""
        return sum([
            self.strength,
            self.constitution,
            self.agility,
            self.intelligence,
            self.willpower,
            self.charisma
        ])


@dataclass
class DerivedStats:
    """Derived character statistics."""
    max_health: int
    current_health: int
    max_mana: int
    current_mana: int
    max_stamina: int
    current_stamina: int
    carry_capacity: int
    initiative: int

    def to_dict(self) -> Dict[str, int]:
        """Convert to dictionary."""
        return {
            'max_health': self.max_health,
            'current_health': self.current_health,
            'max_mana': self.max_mana,
            'current_mana': self.current_mana,
            'max_stamina': self.max_stamina,
            'current_stamina': self.current_stamina,
            'carry_capacity': self.carry_capacity,
            'initiative': self.initiative
        }


class StatCalculator:
    """Calculates derived stats from core attributes."""

    # Base values for calculations
    BASE_HEALTH = 50
    HEALTH_PER_CON = 5

    BASE_MANA = 30
    MANA_PER_WILL = 3

    BASE_STAMINA = 100
    STAMINA_PER_CON = 3
    STAMINA_PER_AGI = 2

    BASE_CARRY = 50
    CARRY_PER_STR = 10

    @staticmethod
    def calculate_max_health(constitution: int, level: int = 1) -> int:
        """
        Calculate maximum health.

        Args:
            constitution: Constitution attribute
            level: Character level

        Returns:
            Maximum health points
        """
        base = StatCalculator.BASE_HEALTH
        from_con = constitution * StatCalculator.HEALTH_PER_CON
        from_level = (level - 1) * 10  # +10 HP per level

        return base + from_con + from_level

    @staticmethod
    def calculate_max_mana(willpower: int, level: int = 1) -> int:
        """
        Calculate maximum mana.

        Args:
            willpower: Willpower attribute
            level: Character level

        Returns:
            Maximum mana points
        """
        base = StatCalculator.BASE_MANA
        from_will = willpower * StatCalculator.MANA_PER_WILL
        from_level = (level - 1) * 5  # +5 MP per level

        return base + from_will + from_level

    @staticmethod
    def calculate_max_stamina(constitution: int, agility: int, level: int = 1) -> int:
        """
        Calculate maximum stamina.

        Args:
            constitution: Constitution attribute
            agility: Agility attribute
            level: Character level

        Returns:
            Maximum stamina points
        """
        base = StatCalculator.BASE_STAMINA
        from_con = constitution * StatCalculator.STAMINA_PER_CON
        from_agi = agility * StatCalculator.STAMINA_PER_AGI
        from_level = (level - 1) * 5  # +5 stamina per level

        return base + from_con + from_agi + from_level

    @staticmethod
    def calculate_carry_capacity(strength: int) -> int:
        """
        Calculate carrying capacity in pounds.

        Args:
            strength: Strength attribute

        Returns:
            Carry capacity in pounds
        """
        return StatCalculator.BASE_CARRY + (strength * StatCalculator.CARRY_PER_STR)

    @staticmethod
    def calculate_initiative(agility: int, intelligence: int) -> int:
        """
        Calculate initiative (turn order in combat).

        Args:
            agility: Agility attribute
            intelligence: Intelligence attribute

        Returns:
            Initiative value
        """
        # Initiative is primarily agility-based with small intelligence bonus
        return agility + (intelligence // 4)

    @staticmethod
    def calculate_all_derived_stats(
        attributes: CoreAttributes,
        level: int = 1,
        current_health: int = None,
        current_mana: int = None,
        current_stamina: int = None
    ) -> DerivedStats:
        """
        Calculate all derived stats from attributes.

        Args:
            attributes: Core attributes
            level: Character level
            current_health: Current health (defaults to max)
            current_mana: Current mana (defaults to max)
            current_stamina: Current stamina (defaults to max)

        Returns:
            DerivedStats object
        """
        max_health = StatCalculator.calculate_max_health(attributes.constitution, level)
        max_mana = StatCalculator.calculate_max_mana(attributes.willpower, level)
        max_stamina = StatCalculator.calculate_max_stamina(
            attributes.constitution,
            attributes.agility,
            level
        )
        carry_capacity = StatCalculator.calculate_carry_capacity(attributes.strength)
        initiative = StatCalculator.calculate_initiative(attributes.agility, attributes.intelligence)

        return DerivedStats(
            max_health=max_health,
            current_health=current_health if current_health is not None else max_health,
            max_mana=max_mana,
            current_mana=current_mana if current_mana is not None else max_mana,
            max_stamina=max_stamina,
            current_stamina=current_stamina if current_stamina is not None else max_stamina,
            carry_capacity=carry_capacity,
            initiative=initiative
        )

    @staticmethod
    def calculate_physical_damage_bonus(strength: int) -> int:
        """
        Calculate bonus physical damage from strength.

        Args:
            strength: Strength attribute

        Returns:
            Damage bonus
        """
        # +1 damage per 2 strength above 10
        return max(0, (strength - 10) // 2)

    @staticmethod
    def calculate_magical_damage_bonus(intelligence: int) -> int:
        """
        Calculate bonus magical damage from intelligence.

        Args:
            intelligence: Intelligence attribute

        Returns:
            Damage bonus
        """
        # +1 damage per 2 intelligence above 10
        return max(0, (intelligence - 10) // 2)

    @staticmethod
    def calculate_defense(agility: int, constitution: int) -> int:
        """
        Calculate defense value (dodge/block chance).

        Args:
            agility: Agility attribute
            constitution: Constitution attribute

        Returns:
            Defense value
        """
        # Defense is primarily agility with small constitution bonus
        return agility + (constitution // 3)

    @staticmethod
    def calculate_spell_power(intelligence: int, willpower: int) -> int:
        """
        Calculate spell power (affects spell effectiveness).

        Args:
            intelligence: Intelligence attribute
            willpower: Willpower attribute

        Returns:
            Spell power value
        """
        # Equal contribution from intelligence and willpower
        return intelligence + willpower
