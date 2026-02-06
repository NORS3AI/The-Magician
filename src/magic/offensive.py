"""Offensive spell implementations."""

from typing import Dict, Any
from .spells import Spell, SpellCategory, ElementType, TargetType, SpellEffect


class MinorFirebolt(Spell):
    """Basic fire damage spell."""

    def __init__(self):
        super().__init__(
            name="Minor Firebolt",
            description="Launch a small bolt of fire at an enemy",
            category=SpellCategory.OFFENSIVE,
            element=ElementType.FIRE,
            target_type=TargetType.SINGLE_ENEMY,
            base_mana_cost=10,
            min_level=1,
            intelligence_requirement=8,
            willpower_requirement=6
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        if not target:
            return {'success': False, 'message': 'No target specified'}

        power = self.get_power(caster.attributes.intelligence, caster.level)
        damage = int(power * 0.8)  # 80% of power as damage

        return {
            'success': True,
            'message': f"{caster.name} casts {self.name}!",
            'damage': damage,
            'element': self.element,
            'target': target
        }


class Fireball(Spell):
    """Medium fire damage spell."""

    def __init__(self):
        super().__init__(
            name="Fireball",
            description="Hurl an explosive ball of flame at an enemy",
            category=SpellCategory.OFFENSIVE,
            element=ElementType.FIRE,
            target_type=TargetType.SINGLE_ENEMY,
            base_mana_cost=20,
            min_level=3,
            intelligence_requirement=12,
            willpower_requirement=10
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        if not target:
            return {'success': False, 'message': 'No target specified'}

        power = self.get_power(caster.attributes.intelligence, caster.level)
        damage = int(power * 1.5)

        # 15% chance to burn
        burn_chance = 0.15

        return {
            'success': True,
            'message': f"{caster.name} hurls a fireball!",
            'damage': damage,
            'element': self.element,
            'target': target,
            'effect_chance': burn_chance,
            'effect_type': 'burning'
        }


class GreaterFireball(Spell):
    """Powerful fire damage spell."""

    def __init__(self):
        super().__init__(
            name="Greater Fireball",
            description="Unleash a devastating explosion of fire",
            category=SpellCategory.OFFENSIVE,
            element=ElementType.FIRE,
            target_type=TargetType.SINGLE_ENEMY,
            base_mana_cost=35,
            min_level=10,
            intelligence_requirement=18,
            willpower_requirement=15
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        if not target:
            return {'success': False, 'message': 'No target specified'}

        power = self.get_power(caster.attributes.intelligence, caster.level)
        damage = int(power * 2.5)

        return {
            'success': True,
            'message': f"{caster.name} unleashes a devastating fireball!",
            'damage': damage,
            'element': self.element,
            'target': target,
            'effect_chance': 0.3,
            'effect_type': 'burning'
        }


class IceShard(Spell):
    """Ice damage spell that can slow enemies."""

    def __init__(self):
        super().__init__(
            name="Ice Shard",
            description="Fire a shard of ice that may slow the target",
            category=SpellCategory.OFFENSIVE,
            element=ElementType.ICE,
            target_type=TargetType.SINGLE_ENEMY,
            base_mana_cost=15,
            min_level=2,
            intelligence_requirement=10,
            willpower_requirement=8
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        if not target:
            return {'success': False, 'message': 'No target specified'}

        power = self.get_power(caster.attributes.intelligence, caster.level)
        damage = int(power * 1.2)

        return {
            'success': True,
            'message': f"{caster.name} fires a shard of ice!",
            'damage': damage,
            'element': self.element,
            'target': target,
            'effect_chance': 0.25,
            'effect_type': 'slow'
        }


class LightningBolt(Spell):
    """Lightning damage spell with high crit chance."""

    def __init__(self):
        super().__init__(
            name="Lightning Bolt",
            description="Strike an enemy with a bolt of lightning",
            category=SpellCategory.OFFENSIVE,
            element=ElementType.LIGHTNING,
            target_type=TargetType.SINGLE_ENEMY,
            base_mana_cost=25,
            min_level=5,
            intelligence_requirement=14,
            willpower_requirement=12
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        if not target:
            return {'success': False, 'message': 'No target specified'}

        power = self.get_power(caster.attributes.intelligence, caster.level)
        damage = int(power * 1.8)

        return {
            'success': True,
            'message': f"{caster.name} calls down lightning!",
            'damage': damage,
            'element': self.element,
            'target': target,
            'crit_bonus': 0.15,  # 15% extra crit chance
            'effect_chance': 0.20,
            'effect_type': 'stunned'
        }


class ChainLightning(Spell):
    """Lightning that hits multiple enemies."""

    def __init__(self):
        super().__init__(
            name="Chain Lightning",
            description="Lightning that arcs between multiple enemies",
            category=SpellCategory.OFFENSIVE,
            element=ElementType.LIGHTNING,
            target_type=TargetType.ALL_ENEMIES,
            base_mana_cost=40,
            min_level=12,
            intelligence_requirement=20,
            willpower_requirement=17
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        power = self.get_power(caster.attributes.intelligence, caster.level)
        damage = int(power * 1.3)  # Lower per-target damage for AoE

        return {
            'success': True,
            'message': f"{caster.name} unleashes chain lightning!",
            'damage': damage,
            'element': self.element,
            'target': 'all',
            'damage_falloff': 0.3  # Each jump reduces damage by 30%
        }


class ArcaneMissile(Spell):
    """Pure arcane damage, never misses."""

    def __init__(self):
        super().__init__(
            name="Arcane Missile",
            description="Fire magical missiles that never miss",
            category=SpellCategory.OFFENSIVE,
            element=ElementType.ARCANE,
            target_type=TargetType.SINGLE_ENEMY,
            base_mana_cost=18,
            min_level=4,
            intelligence_requirement=13,
            willpower_requirement=10
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        if not target:
            return {'success': False, 'message': 'No target specified'}

        power = self.get_power(caster.attributes.intelligence, caster.level)
        damage = int(power * 1.3)

        return {
            'success': True,
            'message': f"{caster.name} launches arcane missiles!",
            'damage': damage,
            'element': self.element,
            'target': target,
            'guaranteed_hit': True
        }


class DarkBolt(Spell):
    """Dark magic that drains life."""

    def __init__(self):
        super().__init__(
            name="Dark Bolt",
            description="Dark energy that damages and weakens enemies",
            category=SpellCategory.OFFENSIVE,
            element=ElementType.DARK,
            target_type=TargetType.SINGLE_ENEMY,
            base_mana_cost=22,
            min_level=7,
            intelligence_requirement=16,
            willpower_requirement=14
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        if not target:
            return {'success': False, 'message': 'No target specified'}

        power = self.get_power(caster.attributes.intelligence, caster.level)
        damage = int(power * 1.6)

        return {
            'success': True,
            'message': f"{caster.name} fires a bolt of dark energy!",
            'damage': damage,
            'element': self.element,
            'target': target,
            'effect_chance': 0.30,
            'effect_type': 'weakness',
            'life_steal': 0.2  # Heal caster for 20% of damage
        }


class Meteor(Spell):
    """Ultimate fire spell hitting all enemies."""

    def __init__(self):
        super().__init__(
            name="Meteor",
            description="Call down a meteor to devastate all enemies",
            category=SpellCategory.OFFENSIVE,
            element=ElementType.FIRE,
            target_type=TargetType.ALL_ENEMIES,
            base_mana_cost=60,
            min_level=18,
            intelligence_requirement=24,
            willpower_requirement=22
        )

    def cast(self, caster, target=None, **kwargs) -> Dict[str, Any]:
        power = self.get_power(caster.attributes.intelligence, caster.level)
        damage = int(power * 3.0)

        return {
            'success': True,
            'message': f"{caster.name} calls down a meteor!",
            'damage': damage,
            'element': self.element,
            'target': 'all',
            'effect_chance': 0.40,
            'effect_type': 'burning'
        }
