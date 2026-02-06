"""Combat action definitions for warrior and mage abilities."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Callable, Any, Dict
from enum import Enum

from .damage import DamageCalculator, DamageType, AttackType
from .effects import StatusEffect, EffectType, create_bleeding, create_stun, create_strengthen, create_shield

if TYPE_CHECKING:
    from ..character import PlayerCharacter


class ActionCategory(Enum):
    """Categories of combat actions."""
    ATTACK = "attack"
    DEFEND = "defend"
    SPELL = "spell"
    ITEM = "item"
    FLEE = "flee"


@dataclass
class CombatAction:
    """Represents a combat action."""
    name: str
    category: ActionCategory
    description: str
    stamina_cost: int = 0
    mana_cost: int = 0
    requires_target: bool = True
    is_unlocked: Callable[[Any], bool] = lambda player: True

    def can_use(self, player: 'PlayerCharacter') -> tuple[bool, str]:
        """
        Check if player can use this action.

        Args:
            player: Player character

        Returns:
            Tuple of (can_use, reason_if_not)
        """
        # Check if unlocked
        if not self.is_unlocked(player):
            return False, "Ability not unlocked"

        # Check stamina
        if self.stamina_cost > 0 and not player.use_stamina(self.stamina_cost):
            return False, "Not enough stamina"

        # Check mana
        if self.mana_cost > 0 and not player.use_mana(self.mana_cost):
            return False, "Not enough mana"

        return True, ""


class WarriorActions:
    """Combat actions for warrior path (Tomas)."""

    @staticmethod
    def light_attack() -> CombatAction:
        """Quick, light attack with higher accuracy."""
        return CombatAction(
            name="Light Attack",
            category=ActionCategory.ATTACK,
            description="A quick, light attack (70% damage, more accurate)",
            stamina_cost=5
        )

    @staticmethod
    def normal_attack() -> CombatAction:
        """Standard attack."""
        return CombatAction(
            name="Attack",
            category=ActionCategory.ATTACK,
            description="A standard attack",
            stamina_cost=10
        )

    @staticmethod
    def heavy_attack() -> CombatAction:
        """Powerful heavy attack with lower accuracy."""
        return CombatAction(
            name="Heavy Attack",
            category=ActionCategory.ATTACK,
            description="A powerful heavy attack (130% damage, less accurate)",
            stamina_cost=20
        )

    @staticmethod
    def power_strike() -> CombatAction:
        """Powerful strike with chance to cause bleeding."""
        return CombatAction(
            name="Power Strike",
            category=ActionCategory.ATTACK,
            description="A mighty strike that may cause bleeding",
            stamina_cost=25,
            is_unlocked=lambda p: p.has_ability("Power Strike")
        )

    @staticmethod
    def shield_bash() -> CombatAction:
        """Bash with shield to stun enemy."""
        return CombatAction(
            name="Shield Bash",
            category=ActionCategory.ATTACK,
            description="Bash enemy with shield, chance to stun",
            stamina_cost=20,
            is_unlocked=lambda p: p.has_ability("Shield Bash")
        )

    @staticmethod
    def whirlwind() -> CombatAction:
        """Area attack hitting all enemies."""
        return CombatAction(
            name="Whirlwind Attack",
            category=ActionCategory.ATTACK,
            description="Spin attack hitting all enemies (80% damage each)",
            stamina_cost=40,
            requires_target=False,
            is_unlocked=lambda p: p.has_ability("Whirlwind Attack")
        )

    @staticmethod
    def battle_cry() -> CombatAction:
        """Buff that increases damage."""
        return CombatAction(
            name="Battle Cry",
            category=ActionCategory.DEFEND,
            description="Rallying cry that strengthens your attacks",
            stamina_cost=15,
            requires_target=False,
            is_unlocked=lambda p: p.has_ability("Battle Cry")
        )

    @staticmethod
    def defend() -> CombatAction:
        """Defensive stance."""
        return CombatAction(
            name="Defend",
            category=ActionCategory.DEFEND,
            description="Take a defensive stance, reducing damage",
            stamina_cost=5,
            requires_target=False
        )

    @staticmethod
    def berserk() -> CombatAction:
        """Berserk rage for massive damage boost."""
        return CombatAction(
            name="Berserk Rage",
            category=ActionCategory.ATTACK,
            description="Enter a rage, greatly increasing damage but reducing defense",
            stamina_cost=50,
            requires_target=False,
            is_unlocked=lambda p: p.has_ability("Berserk Rage")
        )


class MageActions:
    """Combat actions for mage path (Pug)."""

    @staticmethod
    def staff_attack() -> CombatAction:
        """Basic physical attack with staff."""
        return CombatAction(
            name="Staff Attack",
            category=ActionCategory.ATTACK,
            description="Strike with your staff (physical attack)",
            stamina_cost=8
        )

    @staticmethod
    def minor_fireball() -> CombatAction:
        """Basic fire spell."""
        return CombatAction(
            name="Minor Fireball",
            category=ActionCategory.SPELL,
            description="Hurl a small ball of fire at the enemy",
            mana_cost=10,
            is_unlocked=lambda p: p.has_ability("Minor Fireball")
        )

    @staticmethod
    def shield_spell() -> CombatAction:
        """Protective shield spell."""
        return CombatAction(
            name="Shield",
            category=ActionCategory.SPELL,
            description="Conjure a magical shield for protection",
            mana_cost=15,
            requires_target=False,
            is_unlocked=lambda p: p.has_ability("Shield")
        )

    @staticmethod
    def heal() -> CombatAction:
        """Healing spell."""
        return CombatAction(
            name="Heal",
            category=ActionCategory.SPELL,
            description="Restore health with healing magic",
            mana_cost=20,
            requires_target=False,
            is_unlocked=lambda p: p.has_ability("Heal")
        )

    @staticmethod
    def lightning_bolt() -> CombatAction:
        """Lightning spell."""
        return CombatAction(
            name="Lightning Bolt",
            category=ActionCategory.SPELL,
            description="Strike enemy with a bolt of lightning",
            mana_cost=25,
            is_unlocked=lambda p: p.has_ability("Lightning Bolt")
        )

    @staticmethod
    def greater_fireball() -> CombatAction:
        """Powerful fire spell."""
        return CombatAction(
            name="Greater Fireball",
            category=ActionCategory.SPELL,
            description="Unleash a massive fireball (high damage, may burn)",
            mana_cost=35,
            is_unlocked=lambda p: p.has_ability("Greater Fireball")
        )

    @staticmethod
    def invisibility() -> CombatAction:
        """Invisibility spell for escaping."""
        return CombatAction(
            name="Invisibility",
            category=ActionCategory.SPELL,
            description="Turn invisible, greatly improving flee chance",
            mana_cost=30,
            requires_target=False,
            is_unlocked=lambda p: p.has_ability("Invisibility")
        )

    @staticmethod
    def rift_magic() -> CombatAction:
        """Powerful rift magic."""
        return CombatAction(
            name="Rift Magic",
            category=ActionCategory.SPELL,
            description="Tear open a rift in space (massive damage)",
            mana_cost=60,
            is_unlocked=lambda p: p.has_ability("Rift Magic")
        )


class ActionRegistry:
    """Registry of all available combat actions."""

    def __init__(self):
        """Initialize action registry."""
        self.warrior_actions = [
            WarriorActions.light_attack(),
            WarriorActions.normal_attack(),
            WarriorActions.heavy_attack(),
            WarriorActions.power_strike(),
            WarriorActions.shield_bash(),
            WarriorActions.whirlwind(),
            WarriorActions.battle_cry(),
            WarriorActions.defend(),
            WarriorActions.berserk()
        ]

        self.mage_actions = [
            MageActions.staff_attack(),
            MageActions.minor_fireball(),
            MageActions.shield_spell(),
            MageActions.heal(),
            MageActions.lightning_bolt(),
            MageActions.greater_fireball(),
            MageActions.invisibility(),
            MageActions.rift_magic()
        ]

    def get_available_actions(self, player: 'PlayerCharacter') -> list[CombatAction]:
        """
        Get all actions available to a player.

        Args:
            player: Player character

        Returns:
            List of available actions
        """
        if player.path == "tomas":
            actions = self.warrior_actions
        else:  # pug
            actions = self.mage_actions

        # Filter to only unlocked actions
        return [action for action in actions if action.is_unlocked(player)]

    def get_action_by_name(self, name: str, player: 'PlayerCharacter') -> Optional[CombatAction]:
        """
        Get a specific action by name.

        Args:
            name: Action name
            player: Player character

        Returns:
            CombatAction if found and available, None otherwise
        """
        available = self.get_available_actions(player)
        name_lower = name.lower()

        for action in available:
            if action.name.lower() == name_lower:
                return action

        return None
