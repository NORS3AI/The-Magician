"""Greater Magic - Story-locked powerful spells."""

from typing import Dict, Any
from .spells import Spell, SpellCategory, ElementType, TargetType


class RiftOpening(Spell):
    """Open a small rift between worlds (early rift magic)."""

    def __init__(self):
        super().__init__(
            name="Rift Opening",
            description="Open a small rift between worlds",
            category=SpellCategory.GREATER,
            element=ElementType.ARCANE,
            target_type=TargetType.AREA,
            base_mana_cost=50,
            min_level=15,
            intelligence_requirement=22,
            willpower_requirement=20
        )
        self.story_locked = True
        self.unlock_requirement = "kelewan_training"

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        return {
            'success': True,
            'message': f"{caster.name} tears open a rift in reality!",
            'effect_type': 'rift_opening',
            'duration': 2,
            'escape_chance': 1.0  # Guaranteed escape
        }


class RiftTravel(Spell):
    """Travel through the rift between worlds."""

    def __init__(self):
        super().__init__(
            name="Rift Travel",
            description="Travel instantly through the rift between worlds",
            category=SpellCategory.GREATER,
            element=ElementType.ARCANE,
            target_type=TargetType.AREA,
            base_mana_cost=80,
            min_level=18,
            intelligence_requirement=24,
            willpower_requirement=23
        )
        self.story_locked = True
        self.unlock_requirement = "mastery_of_rifts"

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        destination = kwargs.get('destination')

        if not destination:
            return {'success': False, 'message': 'No destination specified'}

        return {
            'success': True,
            'message': f"{caster.name} steps through a rift and vanishes!",
            'effect_type': 'rift_travel',
            'destination': destination,
            'instant': True
        }


class RiftStorm(Spell):
    """Ultimate offensive rift magic."""

    def __init__(self):
        super().__init__(
            name="Rift Storm",
            description="Summon a devastating storm of rift energy",
            category=SpellCategory.GREATER,
            element=ElementType.ARCANE,
            target_type=TargetType.ALL_ENEMIES,
            base_mana_cost=100,
            min_level=20,
            intelligence_requirement=26,
            willpower_requirement=25
        )
        self.story_locked = True
        self.unlock_requirement = "milamber_power"

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        power = self.get_power(caster.attributes.intelligence, caster.level)
        damage = int(power * 4.0)

        return {
            'success': True,
            'message': f"{caster.name} unleashes the fury of the rift!",
            'damage': damage,
            'element': self.element,
            'target': 'all',
            'effect_type': 'rift_damage',
            'ignores_resistance': True
        }


class TimeStop(Spell):
    """Momentarily stop time."""

    def __init__(self):
        super().__init__(
            name="Time Stop",
            description="Briefly halt the flow of time itself",
            category=SpellCategory.GREATER,
            element=ElementType.ARCANE,
            target_type=TargetType.AREA,
            base_mana_cost=120,
            min_level=25,
            intelligence_requirement=28,
            willpower_requirement=28
        )
        self.story_locked = True
        self.unlock_requirement = "ultimate_power"

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        return {
            'success': True,
            'message': f"{caster.name} stops time itself!",
            'effect_type': 'time_stop',
            'extra_turns': 2,
            'enemies_frozen': True
        }


class MindControl(Spell):
    """Dominate the mind of an enemy."""

    def __init__(self):
        super().__init__(
            name="Mind Control",
            description="Dominate the mind of a target creature",
            category=SpellCategory.GREATER,
            element=ElementType.ARCANE,
            target_type=TargetType.SINGLE_ENEMY,
            base_mana_cost=60,
            min_level=16,
            intelligence_requirement=23,
            willpower_requirement=22
        )
        self.story_locked = True
        self.unlock_requirement = "advanced_training"

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        if not target:
            return {'success': False, 'message': 'No target specified'}

        power = self.get_power(caster.attributes.willpower, caster.level)
        success_chance = min(0.8, 0.3 + (power / 200))

        return {
            'success': True,
            'message': f"{caster.name} attempts to dominate {target.name}'s mind!",
            'effect_type': 'mind_control',
            'target': target,
            'success_chance': success_chance,
            'duration': 3
        }


class Polymorph(Spell):
    """Transform a creature into another form."""

    def __init__(self):
        super().__init__(
            name="Polymorph",
            description="Transform a creature into a different form",
            category=SpellCategory.GREATER,
            element=ElementType.ARCANE,
            target_type=TargetType.SINGLE_ENEMY,
            base_mana_cost=55,
            min_level=17,
            intelligence_requirement=24,
            willpower_requirement=21
        )
        self.story_locked = True
        self.unlock_requirement = "transformation_magic"

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        if not target:
            return {'success': False, 'message': 'No target specified'}

        return {
            'success': True,
            'message': f"{caster.name} polymorphs {target.name}!",
            'effect_type': 'polymorph',
            'target': target,
            'new_form': 'harmless_creature',
            'duration': 4,
            'stat_reduction': 0.5
        }


class Disintegrate(Spell):
    """Completely destroy a target."""

    def __init__(self):
        super().__init__(
            name="Disintegrate",
            description="Utterly destroy a target with raw magical power",
            category=SpellCategory.GREATER,
            element=ElementType.ARCANE,
            target_type=TargetType.SINGLE_ENEMY,
            base_mana_cost=90,
            min_level=22,
            intelligence_requirement=27,
            willpower_requirement=26
        )
        self.story_locked = True
        self.unlock_requirement = "ultimate_destruction"

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        if not target:
            return {'success': False, 'message': 'No target specified'}

        power = self.get_power(caster.attributes.intelligence, caster.level)
        damage = int(power * 5.0)

        return {
            'success': True,
            'message': f"{caster.name} disintegrates {target.name}!",
            'damage': damage,
            'element': self.element,
            'target': target,
            'instant_kill_chance': 0.15,
            'ignores_armor': True
        }


class Wish(Spell):
    """Alter reality itself (most powerful spell)."""

    def __init__(self):
        super().__init__(
            name="Wish",
            description="Alter reality itself with a single wish",
            category=SpellCategory.GREATER,
            element=ElementType.ARCANE,
            target_type=TargetType.AREA,
            base_mana_cost=200,
            min_level=30,
            intelligence_requirement=30,
            willpower_requirement=30
        )
        self.story_locked = True
        self.unlock_requirement = "godlike_power"

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        wish_type = kwargs.get('wish_type', 'heal_all')

        return {
            'success': True,
            'message': f"{caster.name} bends reality to their will!",
            'effect_type': 'wish',
            'wish_type': wish_type,
            'reality_alteration': True
        }


class DragonBreath(Spell):
    """Summon dragon fire (Tomas-specific)."""

    def __init__(self):
        super().__init__(
            name="Dragon Breath",
            description="Channel the fire breath of ancient dragons",
            category=SpellCategory.GREATER,
            element=ElementType.FIRE,
            target_type=TargetType.ALL_ENEMIES,
            base_mana_cost=70,
            min_level=20,
            intelligence_requirement=18,
            willpower_requirement=22
        )
        self.story_locked = True
        self.unlock_requirement = "valheru_armor"

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        power = self.get_power(caster.attributes.willpower, caster.level)
        damage = int(power * 3.5)

        return {
            'success': True,
            'message': f"{caster.name} breathes ancient dragon fire!",
            'damage': damage,
            'element': self.element,
            'target': 'all',
            'effect_type': 'dragon_fire',
            'armor_penetration': 0.5
        }


class VoidMagic(Spell):
    """Harness the power of the void."""

    def __init__(self):
        super().__init__(
            name="Void Magic",
            description="Channel the destructive power of the void itself",
            category=SpellCategory.GREATER,
            element=ElementType.DARK,
            target_type=TargetType.SINGLE_ENEMY,
            base_mana_cost=85,
            min_level=21,
            intelligence_requirement=26,
            willpower_requirement=24
        )
        self.story_locked = True
        self.unlock_requirement = "void_knowledge"

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        if not target:
            return {'success': False, 'message': 'No target specified'}

        power = self.get_power(caster.attributes.intelligence, caster.level)
        damage = int(power * 4.2)

        return {
            'success': True,
            'message': f"{caster.name} channels the void!",
            'damage': damage,
            'element': self.element,
            'target': target,
            'life_drain': 0.3,
            'max_health_damage': True  # Also damages max health
        }


class EmpowerRift(Spell):
    """Empower yourself with rift energy."""

    def __init__(self):
        super().__init__(
            name="Empower: Rift",
            description="Channel rift energy to enhance all abilities",
            category=SpellCategory.GREATER,
            element=ElementType.ARCANE,
            target_type=TargetType.SELF,
            base_mana_cost=65,
            min_level=19,
            intelligence_requirement=25,
            willpower_requirement=24
        )
        self.story_locked = True
        self.unlock_requirement = "rift_mastery"

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        buff_amount = max(8, caster.level // 2)

        return {
            'success': True,
            'message': f"{caster.name} channels rift energy!",
            'effect_type': 'rift_empowerment',
            'buff_stats': {
                'intelligence': buff_amount,
                'willpower': buff_amount,
                'constitution': buff_amount // 2
            },
            'spell_power_bonus': 0.5,
            'duration': 5
        }
