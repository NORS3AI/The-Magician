"""Status effects and conditions."""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any


class EffectType(Enum):
    """Types of status effects."""
    # Damage over time
    BLEEDING = "bleeding"
    BURNING = "burning"
    POISON = "poisoned"

    # Control
    STUNNED = "stunned"
    FROZEN = "frozen"
    PARALYZED = "paralyzed"

    # Stat modifiers
    WEAKENED = "weakened"      # Reduced damage
    SLOWED = "slowed"          # Reduced agility
    CONFUSED = "confused"      # May attack self

    # Buffs
    STRENGTHENED = "strengthened"  # Increased damage
    SHIELDED = "shielded"          # Damage reduction
    HASTENED = "hastened"          # Increased agility
    REGENERATING = "regenerating"  # Health over time


@dataclass
class StatusEffect:
    """Represents a status effect on a combatant."""
    effect_type: EffectType
    duration: int  # Turns remaining
    potency: int   # Strength of effect
    source: str    # What caused it

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'effect_type': self.effect_type.value,
            'duration': self.duration,
            'potency': self.potency,
            'source': self.source
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StatusEffect':
        """Create from dictionary."""
        return cls(
            effect_type=EffectType(data['effect_type']),
            duration=data['duration'],
            potency=data['potency'],
            source=data['source']
        )


class EffectManager:
    """Manages status effects on combatants."""

    def __init__(self):
        """Initialize effect manager."""
        self.active_effects: Dict[EffectType, StatusEffect] = {}

    def add_effect(self, effect: StatusEffect) -> bool:
        """
        Add a status effect.

        Args:
            effect: Status effect to add

        Returns:
            True if effect was added/refreshed
        """
        # If effect already exists, take the stronger one
        if effect.effect_type in self.active_effects:
            existing = self.active_effects[effect.effect_type]
            if effect.potency > existing.potency or effect.duration > existing.duration:
                self.active_effects[effect.effect_type] = effect
                return True
            return False

        self.active_effects[effect.effect_type] = effect
        return True

    def remove_effect(self, effect_type: EffectType) -> bool:
        """
        Remove a status effect.

        Args:
            effect_type: Type of effect to remove

        Returns:
            True if effect was removed
        """
        if effect_type in self.active_effects:
            del self.active_effects[effect_type]
            return True
        return False

    def has_effect(self, effect_type: EffectType) -> bool:
        """Check if has a specific effect."""
        return effect_type in self.active_effects

    def get_effect(self, effect_type: EffectType) -> Optional[StatusEffect]:
        """Get a specific effect."""
        return self.active_effects.get(effect_type)

    def tick_effects(self) -> Dict[EffectType, int]:
        """
        Process one turn of all effects.

        Returns:
            Dict of effect type to damage/healing dealt
        """
        results = {}
        expired = []

        for effect_type, effect in list(self.active_effects.items()):
            # Apply effect
            if effect_type in [EffectType.BLEEDING, EffectType.BURNING, EffectType.POISON]:
                results[effect_type] = effect.potency  # Damage
            elif effect_type == EffectType.REGENERATING:
                results[effect_type] = -effect.potency  # Healing (negative damage)

            # Decrement duration
            effect.duration -= 1
            if effect.duration <= 0:
                expired.append(effect_type)

        # Remove expired effects
        for effect_type in expired:
            del self.active_effects[effect_type]

        return results

    def is_incapacitated(self) -> bool:
        """Check if combatant is unable to act."""
        return any(
            self.has_effect(effect)
            for effect in [EffectType.STUNNED, EffectType.FROZEN, EffectType.PARALYZED]
        )

    def get_damage_modifier(self) -> float:
        """Get damage multiplier from effects."""
        multiplier = 1.0

        if self.has_effect(EffectType.STRENGTHENED):
            multiplier *= 1.5
        if self.has_effect(EffectType.WEAKENED):
            multiplier *= 0.5

        return multiplier

    def get_defense_modifier(self) -> float:
        """Get defense multiplier from effects."""
        multiplier = 1.0

        if self.has_effect(EffectType.SHIELDED):
            effect = self.get_effect(EffectType.SHIELDED)
            # Potency determines shield strength
            multiplier *= (1.0 + effect.potency / 100.0)

        return multiplier

    def get_agility_modifier(self) -> float:
        """Get agility multiplier from effects."""
        multiplier = 1.0

        if self.has_effect(EffectType.HASTENED):
            multiplier *= 1.5
        if self.has_effect(EffectType.SLOWED):
            multiplier *= 0.5
        if self.has_effect(EffectType.FROZEN):
            multiplier *= 0.0  # Can't move

        return multiplier

    def clear_all(self):
        """Remove all effects."""
        self.active_effects.clear()

    def get_all_effects(self) -> list[StatusEffect]:
        """Get list of all active effects."""
        return list(self.active_effects.values())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for saving."""
        return {
            'effects': [effect.to_dict() for effect in self.active_effects.values()]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EffectManager':
        """Create from dictionary."""
        manager = cls()
        for effect_data in data.get('effects', []):
            effect = StatusEffect.from_dict(effect_data)
            manager.active_effects[effect.effect_type] = effect
        return manager


# Predefined common effects
def create_bleeding(duration: int = 3, damage_per_turn: int = 5) -> StatusEffect:
    """Create a bleeding effect."""
    return StatusEffect(EffectType.BLEEDING, duration, damage_per_turn, "bleeding wound")


def create_burning(duration: int = 2, damage_per_turn: int = 8) -> StatusEffect:
    """Create a burning effect."""
    return StatusEffect(EffectType.BURNING, duration, damage_per_turn, "fire")


def create_poison(duration: int = 4, damage_per_turn: int = 4) -> StatusEffect:
    """Create a poison effect."""
    return StatusEffect(EffectType.POISON, duration, damage_per_turn, "poison")


def create_stun(duration: int = 1) -> StatusEffect:
    """Create a stun effect."""
    return StatusEffect(EffectType.STUNNED, duration, 0, "stunning blow")


def create_strengthen(duration: int = 3, bonus: int = 50) -> StatusEffect:
    """Create a strengthen buff."""
    return StatusEffect(EffectType.STRENGTHENED, duration, bonus, "battle cry")


def create_shield(duration: int = 3, defense_bonus: int = 30) -> StatusEffect:
    """Create a shield buff."""
    return StatusEffect(EffectType.SHIELDED, duration, defense_bonus, "defensive shield")


def create_regeneration(duration: int = 3, heal_per_turn: int = 10) -> StatusEffect:
    """Create a regeneration buff."""
    return StatusEffect(EffectType.REGENERATING, duration, heal_per_turn, "regeneration")
