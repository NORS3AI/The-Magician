"""Magic system - spells, spell casting, and spell management."""

from .spells import (
    Spell,
    SpellCategory,
    ElementType,
    TargetType,
    SpellEffect,
    SpellBook,
    SpellRegistry,
    get_spell_registry
)

# Import all spell implementations
from .offensive import (
    MinorFirebolt,
    Fireball,
    GreaterFireball,
    IceShard,
    LightningBolt,
    ChainLightning,
    ArcaneMissile,
    DarkBolt,
    Meteor
)

from .defensive import (
    MinorHeal,
    Heal,
    GreaterHeal,
    Regeneration,
    MagicShield,
    IceBarrier,
    Bless,
    Haste,
    Clarity,
    Cleanse,
    Dispel,
    Revitalize
)

from .utility import (
    Light,
    DetectMagic,
    DetectLife,
    Telekinesis,
    Levitate,
    Invisibility,
    Translate,
    Scry,
    Identify,
    WaterWalk,
    Breathe,
    Featherfall
)

from .greater import (
    RiftOpening,
    RiftTravel,
    RiftStorm,
    TimeStop,
    MindControl,
    Polymorph,
    Disintegrate,
    Wish,
    DragonBreath,
    VoidMagic,
    EmpowerRift
)

__all__ = [
    # Base classes
    'Spell',
    'SpellCategory',
    'ElementType',
    'TargetType',
    'SpellEffect',
    'SpellBook',
    'SpellRegistry',
    'get_spell_registry',

    # Offensive spells
    'MinorFirebolt',
    'Fireball',
    'GreaterFireball',
    'IceShard',
    'LightningBolt',
    'ChainLightning',
    'ArcaneMissile',
    'DarkBolt',
    'Meteor',

    # Defensive spells
    'MinorHeal',
    'Heal',
    'GreaterHeal',
    'Regeneration',
    'MagicShield',
    'IceBarrier',
    'Bless',
    'Haste',
    'Clarity',
    'Cleanse',
    'Dispel',
    'Revitalize',

    # Utility spells
    'Light',
    'DetectMagic',
    'DetectLife',
    'Telekinesis',
    'Levitate',
    'Invisibility',
    'Translate',
    'Scry',
    'Identify',
    'WaterWalk',
    'Breathe',
    'Featherfall',

    # Greater magic
    'RiftOpening',
    'RiftTravel',
    'RiftStorm',
    'TimeStop',
    'MindControl',
    'Polymorph',
    'Disintegrate',
    'Wish',
    'DragonBreath',
    'VoidMagic',
    'EmpowerRift',

    'initialize_spells'
]


def initialize_spells():
    """Initialize and register all spells in the game."""
    registry = get_spell_registry()

    # Register offensive spells
    registry.register(MinorFirebolt())
    registry.register(Fireball())
    registry.register(GreaterFireball())
    registry.register(IceShard())
    registry.register(LightningBolt())
    registry.register(ChainLightning())
    registry.register(ArcaneMissile())
    registry.register(DarkBolt())
    registry.register(Meteor())

    # Register defensive spells
    registry.register(MinorHeal())
    registry.register(Heal())
    registry.register(GreaterHeal())
    registry.register(Regeneration())
    registry.register(MagicShield())
    registry.register(IceBarrier())
    registry.register(Bless())
    registry.register(Haste())
    registry.register(Clarity())
    registry.register(Cleanse())
    registry.register(Dispel())
    registry.register(Revitalize())

    # Register utility spells
    registry.register(Light())
    registry.register(DetectMagic())
    registry.register(DetectLife())
    registry.register(Telekinesis())
    registry.register(Levitate())
    registry.register(Invisibility())
    registry.register(Translate())
    registry.register(Scry())
    registry.register(Identify())
    registry.register(WaterWalk())
    registry.register(Breathe())
    registry.register(Featherfall())

    # Register greater magic
    registry.register(RiftOpening())
    registry.register(RiftTravel())
    registry.register(RiftStorm())
    registry.register(TimeStop())
    registry.register(MindControl())
    registry.register(Polymorph())
    registry.register(Disintegrate())
    registry.register(Wish())
    registry.register(DragonBreath())
    registry.register(VoidMagic())
    registry.register(EmpowerRift())
