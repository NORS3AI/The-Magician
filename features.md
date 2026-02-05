# Features

Complete feature documentation for The-Magician text adventure RPG.

## Character Paths

Players choose one of two protagonists at the start of the game. Each path offers a unique gameplay experience while following the events of the Riftwar Saga.

### Tomas - The Warrior Path

- Focus on physical combat and martial prowess
- Action-based abilities (melee attacks, defensive maneuvers)
- Equipment-focused progression
- Storyline follows Tomas's transformation and battles

### Pug - The Mage Path

- Focus on magical study and spellcasting
- Spell-based abilities (offensive, defensive, utility magic)
- Knowledge and mana-focused progression
- Storyline follows Pug's journey from apprentice to master

## RPG Stats

Characters have attributes that affect gameplay outcomes.

### Core Attributes

- **Strength** - Physical power, melee damage, carrying capacity
- **Constitution** - Health pool, resistance to damage and fatigue
- **Agility** - Speed, dodge chance, initiative in combat
- **Intelligence** - Spell power, learning rate, puzzle-solving
- **Willpower** - Mana pool, mental resistance, concentration
- **Charisma** - NPC interactions, persuasion, leadership

### Derived Stats

- **Health (HP)** - Based on Constitution; reaching zero means death or capture
- **Mana (MP)** - Based on Willpower; powers spells and magical abilities
- **Stamina** - Based on Constitution and Agility; affects sustained actions

## Combat System

Turn-based combat with strategic choices.

### Action Abilities (Warrior Focus)

- Basic attacks (light, heavy, precise strikes)
- Defensive stances (block, parry, dodge)
- Special techniques (unlocked through progression)
- Weapon-specific moves

### Spell Abilities (Mage Focus)

- Offensive spells (damage, status effects)
- Defensive spells (shields, wards, healing)
- Utility spells (light, detection, telekinesis)
- Greater magic (unlocked through story progression)

### Combat Flow

1. Initiative determines turn order
2. Choose action: Attack, Defend, Use Item, Cast Spell, Flee
3. Actions resolve based on stats and dice rolls
4. Status effects and conditions apply
5. Victory or defeat triggers story consequences

## Health System

- Health depletes from combat damage, environmental hazards, and survival failures
- Healing through rest, consumables, and (for Pug) healing magic
- Critical health triggers warnings and potential story consequences
- Death may result in game over or capture scenarios depending on story context

## Survival Aspects

The world presents challenges beyond combat.

### Resource Management

- **Food & Water** - Required for long journeys; starvation affects stats
- **Rest** - Fatigue accumulates; rest restores stamina and health
- **Supplies** - Torches, rope, tools needed for exploration

### Environmental Challenges

- Weather conditions (storms, cold, heat)
- Terrain hazards (cliffs, rivers, hostile environments)
- Time-sensitive situations

## Inventory System

### Item Categories

- **Weapons** - Swords, daggers, staves, bows
- **Armor** - Protection gear affecting defense and mobility
- **Consumables** - Food, potions, scrolls
- **Key Items** - Story-critical objects
- **Tools** - Utility items for survival and exploration
- **Valuables** - Currency and trade goods

### Inventory Management

- Weight/capacity limits based on Strength
- Equipment slots (weapon, armor, accessories)
- Quick-use slots for consumables in combat

## Story and Choices

### Narrative Structure

- Story chapters following the events of the books
- Branching dialogue with NPCs
- Player choices affect relationships and minor story variations
- Major plot points remain faithful to source material

### Consequence System

- Choices remembered throughout the game
- NPC relationships tracked (ally, neutral, hostile)
- Some paths open or close based on previous decisions

## Progression

### Experience and Leveling

- Gain experience from combat, quests, and discoveries
- Level up to improve stats and unlock abilities
- Skill points for customizing playstyle

### Story Progression

- Chapter-based advancement
- Key story events unlock new abilities and areas
- Character growth mirrors their development in the novels

## Technical Design

### Interface

- Command-line text interface
- Clear prompts for player input
- Formatted text for readability (descriptions, dialogue, combat)
- Save/load system for progress

### Architecture (Planned)

- Python 3.x
- Modular design (story, combat, inventory, stats as separate systems)
- Data-driven content (story text, items, enemies in external files)
- State management for game saves
