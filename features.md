# Features

Complete feature documentation for The-Magician text adventure RPG.

## Play Now

**[Launch Game](https://NORS3AI.github.io/The-Magician/)** - Play instantly in your browser!

### Run Locally
```bash
git clone https://github.com/NORS3AI/The-Magician.git
cd The-Magician
npm install
npm run dev
```

---

## Technology

| Component | Technology |
|-----------|------------|
| Build Tool | Vite |
| Styling | Tailwind CSS v4 |
| Language | TypeScript |
| Hosting | GitHub Pages |
| Storage | localStorage / IndexedDB |
| State | Custom state machine |

---

## Character Paths

Players choose one of two protagonists at the start of the game. Each path offers a unique gameplay experience while following the events of the Riftwar Saga.

### Tomas - The Warrior Path

- Focus on physical combat and martial prowess
- Action-based abilities (melee attacks, defensive maneuvers)
- Equipment-focused progression
- Storyline follows Tomas's transformation and the power of the Valheru

### Pug - The Mage Path

- Focus on magical study and spellcasting
- Spell-based abilities (offensive, defensive, utility magic)
- Knowledge and mana-focused progression
- Storyline follows Pug's journey from apprentice to master magician

---

## RPG Stats

Characters have attributes that affect gameplay outcomes.

### Core Attributes

| Stat | Description | Primary Use |
|------|-------------|-------------|
| **Strength** | Physical power | Melee damage, carry capacity |
| **Constitution** | Endurance | Health pool, fatigue resistance |
| **Agility** | Speed & reflexes | Dodge, initiative, ranged attacks |
| **Intelligence** | Mental acuity | Spell power, puzzle-solving |
| **Willpower** | Mental fortitude | Mana pool, resist effects |
| **Charisma** | Social presence | NPC relations, persuasion |

### Derived Stats

- **Health (HP)** - Constitution × 10; reaching zero triggers defeat
- **Mana (MP)** - Willpower × 10 (Mage) or × 2 (Warrior)
- **Stamina** - Constitution + Agility; affects sustained actions
- **Initiative** - Agility-based; determines combat turn order

---

## Combat System

Turn-based tactical combat with strategic depth.

### Combat UI Features

- Animated health/mana bars
- Action button panel with cooldown indicators
- Combat log with scrollable history
- Enemy status display
- Visual effects for hits, misses, and criticals

### Action Abilities (Warrior Focus)

| Action | Type | Effect |
|--------|------|--------|
| Strike | Attack | Standard damage |
| Power Attack | Attack | +50% damage, -20% accuracy |
| Defensive Stance | Defense | +30% block, reduced damage |
| Parry | Defense | Counter-attack on block |
| Charge | Special | Gap close + stun |

### Spell Abilities (Mage Focus)

| Spell | Type | Cost | Effect |
|-------|------|------|--------|
| Fire Bolt | Offensive | 10 MP | Direct damage |
| Shield | Defensive | 15 MP | Absorb damage |
| Heal | Utility | 20 MP | Restore HP |
| Detect | Utility | 5 MP | Reveal hidden |
| Greater Magic | Story | Variable | Unlocked via progression |

### Combat Flow

1. **Initiative** - Agility determines turn order
2. **Action Selection** - Attack, Defend, Cast, Item, Flee
3. **Resolution** - Dice rolls modified by stats
4. **Effects** - Status conditions apply
5. **Outcome** - Victory rewards / defeat consequences

---

## Inventory System

### Item Categories

| Category | Examples | Features |
|----------|----------|----------|
| **Weapons** | Swords, staves, bows | Equippable, stat bonuses |
| **Armor** | Helmets, robes, boots | Defense, mobility effects |
| **Consumables** | Potions, food, scrolls | Single-use effects |
| **Key Items** | Quest objects | Story triggers |
| **Materials** | Crafting components | Combine for items |

### Inventory UI

- Grid-based inventory with drag-and-drop
- Equipment slots with paper-doll display
- Quick-access bar for combat items
- Weight/capacity indicator
- Item comparison tooltips

---

## Story & Narrative

### Narrative Structure

- **Chapters** following the events of the books
- **Branching dialogue** with meaningful choices
- **Relationship tracking** with NPCs
- **Consequence system** - choices affect future events

### Locations

| Area | Description |
|------|-------------|
| Castle Crydee | Starting location, training grounds |
| Sorcerer's Isle | Kulgan's domain |
| Elvandar | Elven kingdom in the forest |
| Kelewan | The Tsurani homeworld |
| The Rift | Gateway between worlds |

---

## User Interface

### Design Principles

- **Dark theme** - Immersive fantasy atmosphere
- **Responsive** - Works on desktop, tablet, and mobile
- **Accessible** - Keyboard navigation, screen reader support
- **Animated** - Smooth transitions and micro-interactions

### UI Components

- Glassmorphism cards with backdrop blur
- Gradient backgrounds (midnight → ocean)
- Crimson accent color for actions
- Custom scrollbars matching theme
- Loading states and skeleton screens

---

## Save System

### Features

- **Auto-save** - Progress saved automatically
- **Multiple slots** - Up to 5 save games
- **Cloud sync** - Optional account-based saves
- **Export/Import** - Download save files

### Data Stored

- Character stats and level
- Inventory contents
- Story progress flags
- NPC relationship values
- Playtime statistics

---

## Development Phases

| Phase | Name | Features |
|-------|------|----------|
| 1 | Core UI & Auth | Login, register, JWT tokens, forms |
| 2 | Character System | Stats, leveling, creation wizard |
| 3 | Game Engine | Commands, state machine, locations |
| 4 | Combat System | Turn-based battles, enemy AI |
| 5 | Magic System | Spells, mana, effects |
| 6 | Inventory | Items, equipment, drag-drop |
| 7 | Story Engine | Dialogue, quests, branching |
| 8 | Save/Load | Cloud sync, multiple slots |
| 9 | Polish | Animations, sounds, particles |
| 10 | Deploy | PWA, offline, optimization |

---

## Accessibility

- Keyboard navigation throughout
- High contrast mode option
- Adjustable text size
- Screen reader compatible
- Reduced motion option
- Color-blind friendly palette
