"""Utility spell implementations."""

from typing import Dict, Any
from .spells import Spell, SpellCategory, ElementType, TargetType


class Light(Spell):
    """Creates magical light."""

    def __init__(self):
        super().__init__(
            name="Light",
            description="Create magical light to illuminate dark areas",
            category=SpellCategory.UTILITY,
            element=ElementType.LIGHT,
            target_type=TargetType.SELF,
            base_mana_cost=5,
            min_level=1,
            intelligence_requirement=6,
            willpower_requirement=6
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        duration = max(10, caster.level * 2)

        return {
            'success': True,
            'message': f"{caster.name} creates a magical light!",
            'effect_type': 'light',
            'duration': duration,
            'radius': 20
        }


class DetectMagic(Spell):
    """Reveals magical auras and enchantments."""

    def __init__(self):
        super().__init__(
            name="Detect Magic",
            description="Sense magical auras and enchantments nearby",
            category=SpellCategory.UTILITY,
            element=ElementType.ARCANE,
            target_type=TargetType.AREA,
            base_mana_cost=10,
            min_level=2,
            intelligence_requirement=10,
            willpower_requirement=8
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        power = self.get_power(caster.attributes.intelligence, caster.level)
        detection_range = min(50, 10 + power // 5)

        return {
            'success': True,
            'message': f"{caster.name} senses magical energies...",
            'effect_type': 'detect_magic',
            'range': detection_range,
            'duration': 3
        }


class DetectLife(Spell):
    """Senses living beings nearby."""

    def __init__(self):
        super().__init__(
            name="Detect Life",
            description="Sense the presence of living creatures",
            category=SpellCategory.UTILITY,
            element=ElementType.NATURE,
            target_type=TargetType.AREA,
            base_mana_cost=12,
            min_level=3,
            intelligence_requirement=11,
            willpower_requirement=10
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        power = self.get_power(caster.attributes.willpower, caster.level)
        detection_range = min(60, 15 + power // 4)

        return {
            'success': True,
            'message': f"{caster.name} senses nearby life forms...",
            'effect_type': 'detect_life',
            'range': detection_range,
            'duration': 4
        }


class Telekinesis(Spell):
    """Move objects with mind power."""

    def __init__(self):
        super().__init__(
            name="Telekinesis",
            description="Move objects from a distance using mental power",
            category=SpellCategory.UTILITY,
            element=ElementType.ARCANE,
            target_type=TargetType.AREA,
            base_mana_cost=15,
            min_level=5,
            intelligence_requirement=14,
            willpower_requirement=13
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        power = self.get_power(caster.attributes.intelligence, caster.level)
        max_weight = min(200, 10 + power * 2)

        return {
            'success': True,
            'message': f"{caster.name} channels telekinetic force!",
            'effect_type': 'telekinesis',
            'max_weight': max_weight,
            'range': 15,
            'duration': 2
        }


class Levitate(Spell):
    """Float above the ground."""

    def __init__(self):
        super().__init__(
            name="Levitate",
            description="Float above the ground to avoid hazards",
            category=SpellCategory.UTILITY,
            element=ElementType.ARCANE,
            target_type=TargetType.SELF,
            base_mana_cost=18,
            min_level=6,
            intelligence_requirement=14,
            willpower_requirement=14
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        duration = max(5, caster.level // 2)

        return {
            'success': True,
            'message': f"{caster.name} begins to levitate!",
            'effect_type': 'levitate',
            'duration': duration,
            'height': 5
        }


class Invisibility(Spell):
    """Become invisible."""

    def __init__(self):
        super().__init__(
            name="Invisibility",
            description="Become invisible to avoid detection",
            category=SpellCategory.UTILITY,
            element=ElementType.ARCANE,
            target_type=TargetType.SELF,
            base_mana_cost=35,
            min_level=10,
            intelligence_requirement=18,
            willpower_requirement=17
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        duration = max(3, caster.level // 3)

        return {
            'success': True,
            'message': f"{caster.name} fades from view!",
            'effect_type': 'invisible',
            'duration': duration,
            'breaks_on_action': True
        }


class Translate(Spell):
    """Understand foreign languages."""

    def __init__(self):
        super().__init__(
            name="Translate",
            description="Understand and speak any language",
            category=SpellCategory.UTILITY,
            element=ElementType.ARCANE,
            target_type=TargetType.SELF,
            base_mana_cost=20,
            min_level=7,
            intelligence_requirement=16,
            willpower_requirement=14
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        duration = max(10, caster.level)

        return {
            'success': True,
            'message': f"{caster.name} gains the gift of tongues!",
            'effect_type': 'translate',
            'duration': duration,
            'languages': 'all'
        }


class Scry(Spell):
    """View distant locations."""

    def __init__(self):
        super().__init__(
            name="Scry",
            description="View distant locations through magical sight",
            category=SpellCategory.UTILITY,
            element=ElementType.ARCANE,
            target_type=TargetType.AREA,
            base_mana_cost=40,
            min_level=13,
            intelligence_requirement=20,
            willpower_requirement=19
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        power = self.get_power(caster.attributes.intelligence, caster.level)
        max_distance = min(1000, 100 + power * 5)

        return {
            'success': True,
            'message': f"{caster.name} peers into the distance...",
            'effect_type': 'scry',
            'max_distance': max_distance,
            'duration': 3
        }


class Identify(Spell):
    """Reveal properties of magical items."""

    def __init__(self):
        super().__init__(
            name="Identify",
            description="Reveal the magical properties of an item",
            category=SpellCategory.UTILITY,
            element=ElementType.ARCANE,
            target_type=TargetType.SINGLE_ENEMY,
            base_mana_cost=25,
            min_level=8,
            intelligence_requirement=17,
            willpower_requirement=15
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        item = kwargs.get('item')

        if not item:
            return {'success': False, 'message': 'No item to identify'}

        return {
            'success': True,
            'message': f"{caster.name} examines the item magically...",
            'effect_type': 'identify',
            'item': item,
            'reveal_all': True
        }


class WaterWalk(Spell):
    """Walk on water surfaces."""

    def __init__(self):
        super().__init__(
            name="Water Walk",
            description="Walk across water as if it were solid ground",
            category=SpellCategory.UTILITY,
            element=ElementType.NATURE,
            target_type=TargetType.SELF,
            base_mana_cost=16,
            min_level=5,
            intelligence_requirement=12,
            willpower_requirement=13
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        duration = max(8, caster.level)

        return {
            'success': True,
            'message': f"{caster.name} walks upon the water!",
            'effect_type': 'water_walk',
            'duration': duration
        }


class Breathe(Spell):
    """Breathe underwater."""

    def __init__(self):
        super().__init__(
            name="Water Breathing",
            description="Breathe underwater for extended periods",
            category=SpellCategory.UTILITY,
            element=ElementType.NATURE,
            target_type=TargetType.SELF,
            base_mana_cost=22,
            min_level=6,
            intelligence_requirement=13,
            willpower_requirement=14
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        duration = max(15, caster.level * 2)

        return {
            'success': True,
            'message': f"{caster.name} can now breathe underwater!",
            'effect_type': 'water_breathing',
            'duration': duration
        }


class Featherfall(Spell):
    """Slow falling to prevent damage."""

    def __init__(self):
        super().__init__(
            name="Featherfall",
            description="Slow your fall to prevent damage",
            category=SpellCategory.UTILITY,
            element=ElementType.ARCANE,
            target_type=TargetType.SELF,
            base_mana_cost=14,
            min_level=4,
            intelligence_requirement=11,
            willpower_requirement=10
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        return {
            'success': True,
            'message': f"{caster.name} floats down gently!",
            'effect_type': 'featherfall',
            'duration': 5,
            'negate_fall_damage': True
        }
