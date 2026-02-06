"""Combat system - battles, actions, enemies."""

from .damage import DamageCalculator, DamageType, AttackType
from .effects import (
    StatusEffect,
    EffectType,
    EffectManager,
    create_bleeding,
    create_burning,
    create_poison,
    create_stun,
    create_shield,
    create_strength_buff,
    create_agility_buff,
    create_weakness,
    create_slow
)
from .actions import (
    CombatAction,
    ActionCategory,
    ActionRegistry,
    WarriorActions,
    MageActions
)
from .enemy import (
    Enemy,
    EnemyAI,
    create_goblin,
    create_orc,
    create_troll,
    create_dark_mage,
    create_dragon
)
from .battle import Battle, BattleResult, BattleTurn

__all__ = [
    # Damage
    'DamageCalculator',
    'DamageType',
    'AttackType',

    # Effects
    'StatusEffect',
    'EffectType',
    'EffectManager',
    'create_bleeding',
    'create_burning',
    'create_poison',
    'create_stun',
    'create_shield',
    'create_strength_buff',
    'create_agility_buff',
    'create_weakness',
    'create_slow',

    # Actions
    'CombatAction',
    'ActionCategory',
    'ActionRegistry',
    'WarriorActions',
    'MageActions',

    # Enemies
    'Enemy',
    'EnemyAI',
    'create_goblin',
    'create_orc',
    'create_troll',
    'create_dark_mage',
    'create_dragon',

    # Battle
    'Battle',
    'BattleResult',
    'BattleTurn'
]
