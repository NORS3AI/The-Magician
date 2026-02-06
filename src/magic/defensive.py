"""Defensive and healing spell implementations."""

from typing import Dict, Any
from .spells import Spell, SpellCategory, ElementType, TargetType


class MinorHeal(Spell):
    """Basic healing spell."""

    def __init__(self):
        super().__init__(
            name="Minor Heal",
            description="Restore a small amount of health",
            category=SpellCategory.DEFENSIVE,
            element=ElementType.LIGHT,
            target_type=TargetType.SELF,
            base_mana_cost=12,
            min_level=1,
            intelligence_requirement=8,
            willpower_requirement=10,
            scaling_stat="willpower"
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        target = target or caster
        power = self.get_power(caster.attributes.willpower, caster.level)
        healing = int(power * 1.0)

        return {
            'success': True,
            'message': f"{caster.name} casts {self.name}!",
            'healing': healing,
            'target': target
        }


class Heal(Spell):
    """Medium healing spell."""

    def __init__(self):
        super().__init__(
            name="Heal",
            description="Restore a moderate amount of health",
            category=SpellCategory.DEFENSIVE,
            element=ElementType.LIGHT,
            target_type=TargetType.SINGLE_ALLY,
            base_mana_cost=25,
            min_level=5,
            intelligence_requirement=12,
            willpower_requirement=14,
            scaling_stat="willpower"
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        target = target or caster
        power = self.get_power(caster.attributes.willpower, caster.level)
        healing = int(power * 2.0)

        return {
            'success': True,
            'message': f"{caster.name} heals {target.name}!",
            'healing': healing,
            'target': target
        }


class GreaterHeal(Spell):
    """Powerful healing spell."""

    def __init__(self):
        super().__init__(
            name="Greater Heal",
            description="Restore a large amount of health",
            category=SpellCategory.DEFENSIVE,
            element=ElementType.LIGHT,
            target_type=TargetType.SINGLE_ALLY,
            base_mana_cost=45,
            min_level=12,
            intelligence_requirement=18,
            willpower_requirement=20,
            scaling_stat="willpower"
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        target = target or caster
        power = self.get_power(caster.attributes.willpower, caster.level)
        healing = int(power * 3.5)

        return {
            'success': True,
            'message': f"{caster.name} channels powerful healing energy!",
            'healing': healing,
            'target': target
        }


class Regeneration(Spell):
    """Healing over time spell."""

    def __init__(self):
        super().__init__(
            name="Regeneration",
            description="Gradually restore health over several turns",
            category=SpellCategory.DEFENSIVE,
            element=ElementType.NATURE,
            target_type=TargetType.SINGLE_ALLY,
            base_mana_cost=30,
            min_level=8,
            intelligence_requirement=15,
            willpower_requirement=16,
            scaling_stat="willpower"
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        target = target or caster
        power = self.get_power(caster.attributes.willpower, caster.level)
        heal_per_turn = int(power * 0.5)

        return {
            'success': True,
            'message': f"{caster.name} grants regeneration to {target.name}!",
            'effect_type': 'regeneration',
            'heal_per_turn': heal_per_turn,
            'duration': 5,
            'target': target
        }


class MagicShield(Spell):
    """Creates a protective barrier."""

    def __init__(self):
        super().__init__(
            name="Magic Shield",
            description="Create a barrier that absorbs damage",
            category=SpellCategory.DEFENSIVE,
            element=ElementType.ARCANE,
            target_type=TargetType.SELF,
            base_mana_cost=20,
            min_level=3,
            intelligence_requirement=12,
            willpower_requirement=12
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        target = target or caster
        power = self.get_power(caster.attributes.intelligence, caster.level)
        shield_strength = int(power * 1.5)

        return {
            'success': True,
            'message': f"{caster.name} conjures a magic shield!",
            'effect_type': 'shielded',
            'shield_value': shield_strength,
            'duration': 3,
            'target': target
        }


class IceBarrier(Spell):
    """Ice-based shield that slows attackers."""

    def __init__(self):
        super().__init__(
            name="Ice Barrier",
            description="A barrier of ice that slows attackers",
            category=SpellCategory.DEFENSIVE,
            element=ElementType.ICE,
            target_type=TargetType.SELF,
            base_mana_cost=28,
            min_level=7,
            intelligence_requirement=15,
            willpower_requirement=14
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        target = target or caster
        power = self.get_power(caster.attributes.intelligence, caster.level)
        shield_strength = int(power * 1.3)

        return {
            'success': True,
            'message': f"{caster.name} forms a barrier of ice!",
            'effect_type': 'ice_barrier',
            'shield_value': shield_strength,
            'duration': 3,
            'counter_effect': 'slow',
            'target': target
        }


class Bless(Spell):
    """Increases attack and defense."""

    def __init__(self):
        super().__init__(
            name="Bless",
            description="Increase strength and defense temporarily",
            category=SpellCategory.DEFENSIVE,
            element=ElementType.LIGHT,
            target_type=TargetType.SINGLE_ALLY,
            base_mana_cost=22,
            min_level=4,
            intelligence_requirement=12,
            willpower_requirement=13,
            scaling_stat="willpower"
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        target = target or caster
        buff_amount = max(3, caster.level // 2)

        return {
            'success': True,
            'message': f"{caster.name} blesses {target.name}!",
            'effect_type': 'blessed',
            'buff_stats': {
                'strength': buff_amount,
                'constitution': buff_amount
            },
            'duration': 4,
            'target': target
        }


class Haste(Spell):
    """Increases agility and speed."""

    def __init__(self):
        super().__init__(
            name="Haste",
            description="Greatly increase agility and speed",
            category=SpellCategory.DEFENSIVE,
            element=ElementType.ARCANE,
            target_type=TargetType.SINGLE_ALLY,
            base_mana_cost=26,
            min_level=6,
            intelligence_requirement=14,
            willpower_requirement=13
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        target = target or caster
        buff_amount = max(4, caster.level // 2)

        return {
            'success': True,
            'message': f"{caster.name} grants haste to {target.name}!",
            'effect_type': 'hasted',
            'buff_stats': {
                'agility': buff_amount
            },
            'duration': 4,
            'target': target
        }


class Clarity(Spell):
    """Increases intelligence and willpower."""

    def __init__(self):
        super().__init__(
            name="Clarity",
            description="Enhance mental capabilities",
            category=SpellCategory.DEFENSIVE,
            element=ElementType.ARCANE,
            target_type=TargetType.SELF,
            base_mana_cost=20,
            min_level=5,
            intelligence_requirement=13,
            willpower_requirement=14
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        target = target or caster
        buff_amount = max(3, caster.level // 3)

        return {
            'success': True,
            'message': f"{caster.name} gains mental clarity!",
            'effect_type': 'clarity',
            'buff_stats': {
                'intelligence': buff_amount,
                'willpower': buff_amount
            },
            'duration': 5,
            'target': target
        }


class Cleanse(Spell):
    """Removes negative status effects."""

    def __init__(self):
        super().__init__(
            name="Cleanse",
            description="Remove negative status effects",
            category=SpellCategory.DEFENSIVE,
            element=ElementType.LIGHT,
            target_type=TargetType.SINGLE_ALLY,
            base_mana_cost=18,
            min_level=4,
            intelligence_requirement=11,
            willpower_requirement=12,
            scaling_stat="willpower"
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        target = target or caster

        return {
            'success': True,
            'message': f"{caster.name} cleanses {target.name}!",
            'effect_type': 'cleanse',
            'remove_effects': ['poison', 'burning', 'bleeding', 'weakness', 'slow', 'stunned'],
            'target': target
        }


class Dispel(Spell):
    """Removes magical effects."""

    def __init__(self):
        super().__init__(
            name="Dispel",
            description="Remove magical effects from target",
            category=SpellCategory.DEFENSIVE,
            element=ElementType.ARCANE,
            target_type=TargetType.SINGLE_ENEMY,
            base_mana_cost=24,
            min_level=9,
            intelligence_requirement=17,
            willpower_requirement=15
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        if not target:
            return {'success': False, 'message': 'No target specified'}

        return {
            'success': True,
            'message': f"{caster.name} dispels magic from {target.name}!",
            'effect_type': 'dispel',
            'remove_effects': 'all_magical',
            'target': target
        }


class Revitalize(Spell):
    """Restores mana and stamina."""

    def __init__(self):
        super().__init__(
            name="Revitalize",
            description="Restore mana and stamina",
            category=SpellCategory.DEFENSIVE,
            element=ElementType.NATURE,
            target_type=TargetType.SELF,
            base_mana_cost=15,
            min_level=10,
            intelligence_requirement=16,
            willpower_requirement=17,
            scaling_stat="willpower"
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        target = target or caster
        power = self.get_power(caster.attributes.willpower, caster.level)
        restore_amount = int(power * 0.8)

        return {
            'success': True,
            'message': f"{caster.name} feels revitalized!",
            'mana_restore': restore_amount,
            'stamina_restore': restore_amount * 2,
            'target': target
        }
