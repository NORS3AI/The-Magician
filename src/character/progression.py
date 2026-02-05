"""Character progression system: experience points and leveling."""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import math


@dataclass
class LevelInfo:
    """Information about a character level."""
    level: int
    xp_required: int
    stat_points: int
    ability_unlocks: List[str]

    def __str__(self) -> str:
        """String representation."""
        return f"Level {self.level} (XP: {self.xp_required})"


class ExperienceSystem:
    """Manages experience points and leveling."""

    # Maximum character level
    MAX_LEVEL = 50

    # Base XP required for level 2
    BASE_XP = 100

    # XP scaling factor
    XP_SCALE = 1.5

    # Stat points gained per level
    STAT_POINTS_PER_LEVEL = 3

    @staticmethod
    def calculate_xp_for_level(level: int) -> int:
        """
        Calculate total XP required to reach a level.

        Args:
            level: Target level

        Returns:
            Total XP required
        """
        if level <= 1:
            return 0

        # Formula: BASE_XP * (level - 1) ^ XP_SCALE
        return int(ExperienceSystem.BASE_XP * math.pow(level - 1, ExperienceSystem.XP_SCALE))

    @staticmethod
    def calculate_xp_for_next_level(current_level: int) -> int:
        """
        Calculate XP needed from current level to next.

        Args:
            current_level: Current character level

        Returns:
            XP needed for next level
        """
        current_xp = ExperienceSystem.calculate_xp_for_level(current_level)
        next_xp = ExperienceSystem.calculate_xp_for_level(current_level + 1)
        return next_xp - current_xp

    @staticmethod
    def get_level_from_xp(total_xp: int) -> int:
        """
        Determine character level from total XP.

        Args:
            total_xp: Total experience points

        Returns:
            Character level
        """
        level = 1
        while level < ExperienceSystem.MAX_LEVEL:
            xp_for_next = ExperienceSystem.calculate_xp_for_level(level + 1)
            if total_xp < xp_for_next:
                break
            level += 1

        return level

    @staticmethod
    def get_progress_to_next_level(total_xp: int, current_level: int) -> Tuple[int, int]:
        """
        Get progress toward next level.

        Args:
            total_xp: Total experience points
            current_level: Current character level

        Returns:
            Tuple of (current progress XP, XP needed for next level)
        """
        current_level_xp = ExperienceSystem.calculate_xp_for_level(current_level)
        next_level_xp = ExperienceSystem.calculate_xp_for_level(current_level + 1)

        progress = total_xp - current_level_xp
        needed = next_level_xp - current_level_xp

        return (progress, needed)

    @staticmethod
    def get_progress_percentage(total_xp: int, current_level: int) -> float:
        """
        Get percentage progress to next level.

        Args:
            total_xp: Total experience points
            current_level: Current character level

        Returns:
            Progress percentage (0-100)
        """
        progress, needed = ExperienceSystem.get_progress_to_next_level(total_xp, current_level)
        if needed == 0:
            return 100.0
        return (progress / needed) * 100.0


class AbilitySystem:
    """Manages ability unlocks per level."""

    # Tomas (Warrior) ability unlocks
    TOMAS_ABILITIES = {
        1: [],  # Starting abilities
        2: ["Power Strike"],
        3: ["Shield Bash"],
        5: ["Whirlwind Attack"],
        7: ["Battle Cry"],
        10: ["Berserk Rage"],
        12: ["Disarm"],
        15: ["Second Wind"],
        18: ["Weapon Master"],
        20: ["Valheru's Might"],
        25: ["Dragon's Fury"],
        30: ["Ashen-Shugar's Legacy"]
    }

    # Pug (Mage) ability unlocks
    PUG_ABILITIES = {
        1: ["Minor Fireball", "Light"],
        2: ["Shield"],
        3: ["Heal"],
        5: ["Lightning Bolt"],
        7: ["Invisibility"],
        10: ["Greater Fireball"],
        12: ["Telekinesis"],
        15: ["Dispel Magic"],
        18: ["Rift Magic"],
        20: ["Master's Power"],
        25: ["Time Stop"],
        30: ["Milamber's Fury"]
    }

    @staticmethod
    def get_abilities_for_level(path: str, level: int) -> List[str]:
        """
        Get all abilities unlocked up to a level.

        Args:
            path: Character path ("tomas" or "pug")
            level: Character level

        Returns:
            List of ability names
        """
        abilities = []
        ability_tree = (
            AbilitySystem.TOMAS_ABILITIES if path.lower() == "tomas"
            else AbilitySystem.PUG_ABILITIES
        )

        for unlock_level, unlocked_abilities in ability_tree.items():
            if unlock_level <= level:
                abilities.extend(unlocked_abilities)

        return abilities

    @staticmethod
    def get_new_abilities_at_level(path: str, level: int) -> List[str]:
        """
        Get abilities newly unlocked at a specific level.

        Args:
            path: Character path ("tomas" or "pug")
            level: Character level

        Returns:
            List of newly unlocked ability names
        """
        ability_tree = (
            AbilitySystem.TOMAS_ABILITIES if path.lower() == "tomas"
            else AbilitySystem.PUG_ABILITIES
        )

        return ability_tree.get(level, [])

    @staticmethod
    def get_next_ability_unlock(path: str, current_level: int) -> Optional[Tuple[int, List[str]]]:
        """
        Get next ability unlock information.

        Args:
            path: Character path ("tomas" or "pug")
            current_level: Current character level

        Returns:
            Tuple of (level, abilities) or None if no more unlocks
        """
        ability_tree = (
            AbilitySystem.TOMAS_ABILITIES if path.lower() == "tomas"
            else AbilitySystem.PUG_ABILITIES
        )

        for level in sorted(ability_tree.keys()):
            if level > current_level and ability_tree[level]:
                return (level, ability_tree[level])

        return None


class LevelUpManager:
    """Manages level up process and rewards."""

    def __init__(self):
        """Initialize level up manager."""
        self.pending_stat_points = 0
        self.new_abilities: List[str] = []

    def check_level_up(self, old_xp: int, new_xp: int, current_level: int) -> Optional[int]:
        """
        Check if XP gain results in level up.

        Args:
            old_xp: Previous total XP
            new_xp: New total XP
            current_level: Current level before XP gain

        Returns:
            New level if leveled up, None otherwise
        """
        old_level = ExperienceSystem.get_level_from_xp(old_xp)
        new_level = ExperienceSystem.get_level_from_xp(new_xp)

        if new_level > old_level:
            return new_level
        return None

    def process_level_up(
        self,
        old_level: int,
        new_level: int,
        path: str
    ) -> Dict[str, any]:
        """
        Process level up and return rewards.

        Args:
            old_level: Previous level
            new_level: New level
            path: Character path

        Returns:
            Dict with level up rewards
        """
        levels_gained = new_level - old_level

        # Calculate rewards
        stat_points = levels_gained * ExperienceSystem.STAT_POINTS_PER_LEVEL

        # Get new abilities
        new_abilities = []
        for level in range(old_level + 1, new_level + 1):
            abilities = AbilitySystem.get_new_abilities_at_level(path, level)
            new_abilities.extend(abilities)

        return {
            'levels_gained': levels_gained,
            'new_level': new_level,
            'stat_points': stat_points,
            'new_abilities': new_abilities
        }

    def allocate_stat_points(
        self,
        points_to_allocate: Dict[str, int],
        available_points: int
    ) -> Tuple[bool, str]:
        """
        Validate stat point allocation.

        Args:
            points_to_allocate: Dict of stat name to points
            available_points: Total points available

        Returns:
            Tuple of (success, message)
        """
        total_allocated = sum(points_to_allocate.values())

        if total_allocated > available_points:
            return False, f"Not enough points (have {available_points}, trying to spend {total_allocated})"

        if total_allocated < available_points:
            return False, f"You have {available_points - total_allocated} unspent points"

        # All points allocated correctly
        return True, "Stat points allocated successfully"

    @staticmethod
    def get_level_info(level: int, path: str) -> LevelInfo:
        """
        Get information about a specific level.

        Args:
            level: Level to get info for
            path: Character path

        Returns:
            LevelInfo object
        """
        xp_required = ExperienceSystem.calculate_xp_for_level(level)
        stat_points = ExperienceSystem.STAT_POINTS_PER_LEVEL
        ability_unlocks = AbilitySystem.get_new_abilities_at_level(path, level)

        return LevelInfo(
            level=level,
            xp_required=xp_required,
            stat_points=stat_points,
            ability_unlocks=ability_unlocks
        )
