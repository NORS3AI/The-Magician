"""Damage calculations and combat formulas."""

import random
from typing import TYPE_CHECKING, Tuple, Dict
from enum import Enum

if TYPE_CHECKING:
    from ..character import PlayerCharacter


class DamageType(Enum):
    """Types of damage."""
    PHYSICAL = "physical"
    MAGICAL = "magical"
    FIRE = "fire"
    COLD = "cold"
    LIGHTNING = "lightning"
    POISON = "poison"
    TRUE = "true"  # Ignores defense


class AttackType(Enum):
    """Types of attacks."""
    LIGHT = "light"
    NORMAL = "normal"
    HEAVY = "heavy"
    CRITICAL = "critical"


class DamageCalculator:
    """Calculates damage for attacks and spells."""

    # Critical hit chance and multiplier
    BASE_CRIT_CHANCE = 0.05  # 5% base
    CRIT_MULTIPLIER = 2.0

    # Hit chance base
    BASE_HIT_CHANCE = 0.85  # 85% base hit chance

    @staticmethod
    def calculate_physical_damage(
        attacker_strength: int,
        defender_defense: int,
        base_damage: int,
        attack_type: AttackType = AttackType.NORMAL
    ) -> Tuple[int, bool, bool]:
        """
        Calculate physical damage.

        Args:
            attacker_strength: Attacker's strength
            defender_defense: Defender's defense
            base_damage: Base weapon/attack damage
            attack_type: Type of attack

        Returns:
            Tuple of (damage, is_hit, is_critical)
        """
        # Check if attack hits
        hit_chance = DamageCalculator._calculate_hit_chance(attacker_strength, defender_defense)
        is_hit = random.random() < hit_chance

        if not is_hit:
            return 0, False, False

        # Check for critical hit
        crit_chance = DamageCalculator._calculate_crit_chance(attacker_strength)
        is_critical = random.random() < crit_chance

        # Calculate base damage with attack type modifier
        damage = base_damage
        if attack_type == AttackType.LIGHT:
            damage = int(damage * 0.7)  # 70% damage, faster
        elif attack_type == AttackType.HEAVY:
            damage = int(damage * 1.3)  # 130% damage, slower

        # Add strength bonus
        str_bonus = max(0, (attacker_strength - 10) // 2)
        damage += str_bonus

        # Apply defense reduction
        damage = DamageCalculator._apply_defense(damage, defender_defense, DamageType.PHYSICAL)

        # Apply critical multiplier
        if is_critical:
            damage = int(damage * DamageCalculator.CRIT_MULTIPLIER)

        # Add variance (±10%)
        variance = random.uniform(0.9, 1.1)
        damage = int(damage * variance)

        return max(1, damage), True, is_critical

    @staticmethod
    def calculate_magical_damage(
        caster_intelligence: int,
        caster_willpower: int,
        defender_willpower: int,
        base_damage: int,
        damage_type: DamageType = DamageType.MAGICAL
    ) -> Tuple[int, bool]:
        """
        Calculate magical damage.

        Args:
            caster_intelligence: Caster's intelligence
            caster_willpower: Caster's willpower
            defender_willpower: Defender's willpower (magical resistance)
            base_damage: Base spell damage
            damage_type: Type of magical damage

        Returns:
            Tuple of (damage, is_critical)
        """
        # Magic always hits (use willpower for resistance)
        is_hit = True

        # Calculate spell power bonus
        spell_power = caster_intelligence + caster_willpower
        spell_bonus = max(0, (spell_power - 20) // 3)

        damage = base_damage + spell_bonus

        # Apply magical resistance
        resistance = max(0, (defender_willpower - 10) // 2)
        damage = max(1, damage - resistance)

        # Check for critical (int-based for mages)
        crit_chance = DamageCalculator._calculate_crit_chance(caster_intelligence)
        is_critical = random.random() < crit_chance

        if is_critical:
            damage = int(damage * DamageCalculator.CRIT_MULTIPLIER)

        # Add variance (±10%)
        variance = random.uniform(0.9, 1.1)
        damage = int(damage * variance)

        return max(1, damage), is_critical

    @staticmethod
    def _calculate_hit_chance(attacker_stat: int, defender_defense: int) -> float:
        """Calculate hit chance based on attacker vs defender."""
        # Base hit chance modified by stat difference
        stat_diff = attacker_stat - defender_defense
        hit_mod = stat_diff * 0.02  # ±2% per point difference

        hit_chance = DamageCalculator.BASE_HIT_CHANCE + hit_mod
        return max(0.1, min(0.95, hit_chance))  # Clamp between 10% and 95%

    @staticmethod
    def _calculate_crit_chance(primary_stat: int) -> float:
        """Calculate critical hit chance based on primary stat."""
        # +1% crit per 10 points above 10
        crit_bonus = max(0, (primary_stat - 10)) * 0.01
        return min(0.5, DamageCalculator.BASE_CRIT_CHANCE + crit_bonus)  # Cap at 50%

    @staticmethod
    def _apply_defense(damage: int, defense: int, damage_type: DamageType) -> int:
        """Apply defense reduction to damage."""
        if damage_type == DamageType.TRUE:
            return damage  # True damage ignores defense

        # Defense reduces damage by a percentage
        reduction = defense / (defense + 100)  # Diminishing returns
        reduced_damage = damage * (1 - reduction)

        return max(1, int(reduced_damage))

    @staticmethod
    def calculate_healing(caster_willpower: int, base_healing: int) -> int:
        """
        Calculate healing amount.

        Args:
            caster_willpower: Healer's willpower
            base_healing: Base healing amount

        Returns:
            Total healing
        """
        # Willpower bonus to healing
        will_bonus = max(0, (caster_willpower - 10) // 2)
        healing = base_healing + will_bonus

        # Add variance (±15%)
        variance = random.uniform(0.85, 1.15)
        healing = int(healing * variance)

        return max(1, healing)

    @staticmethod
    def calculate_flee_chance(player_agility: int, enemy_agility: int) -> float:
        """
        Calculate chance to successfully flee from combat.

        Args:
            player_agility: Player's agility
            enemy_agility: Enemy's agility

        Returns:
            Flee success chance (0.0 to 1.0)
        """
        base_chance = 0.5
        agi_diff = player_agility - enemy_agility
        flee_mod = agi_diff * 0.05  # ±5% per point difference

        flee_chance = base_chance + flee_mod
        return max(0.2, min(0.9, flee_chance))  # Clamp between 20% and 90%

    @staticmethod
    def get_xp_reward(enemy_level: int, player_level: int) -> int:
        """
        Calculate XP reward for defeating an enemy.

        Args:
            enemy_level: Enemy's level
            player_level: Player's level

        Returns:
            XP reward amount
        """
        base_xp = 50 * enemy_level

        # Level difference modifier
        level_diff = enemy_level - player_level
        if level_diff > 0:
            # Bonus for higher level enemies
            multiplier = 1.0 + (level_diff * 0.1)
        else:
            # Penalty for lower level enemies
            multiplier = max(0.1, 1.0 + (level_diff * 0.05))

        xp = int(base_xp * multiplier)
        return max(10, xp)  # Minimum 10 XP
