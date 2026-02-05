# Project Todo

Development tasks and requirements for The-Magician.

---

## Player Account System

### Requirements

- [ ] **Encrypted Account Storage**
  - [ ] Hash passwords using secure algorithm (bcrypt or argon2)
  - [ ] Generate unique key tokens for session management
  - [ ] Store credentials securely (never plain text)

- [ ] **Password Requirements**
  - [ ] Minimum 8 characters
  - [ ] English characters only (a-z, A-Z, 0-9, common symbols)
  - [ ] Validate on registration and password change

- [ ] **Email Integration**
  - [ ] Email field required at registration
  - [ ] Password reset via email link
  - [ ] Username reminder via email
  - [ ] Email verification (optional but recommended)

- [ ] **Account Features**
  - [ ] Create new account (register)
  - [ ] Login with username/password
  - [ ] Logout and session cleanup
  - [ ] Forgot password flow
  - [ ] Forgot username flow
  - [ ] Change password (when logged in)

### System Structure (Skeleton)

```
src/
├── auth/
│   ├── __init__.py
│   ├── account.py          # Account creation, login, logout
│   ├── password.py         # Hashing, validation, reset logic
│   ├── token.py            # Session tokens, key generation
│   └── email_service.py    # Email sending for reset/reminder
├── data/
│   └── users/              # Encrypted user data storage
├── config/
│   └── auth_config.py      # Auth settings (token expiry, hash rounds)
└── utils/
    └── validation.py       # Input validation (password rules, email format)
```

### Implementation Notes

1. **Password Hashing**
   - Use `bcrypt` or `argon2-cffi` library
   - Salt automatically included with bcrypt
   - Cost factor of 12+ recommended

2. **Token Generation**
   - Use `secrets` module for cryptographic tokens
   - Tokens should expire (configurable, e.g., 24 hours for reset)
   - Store token hashes, not raw tokens

3. **Email Service**
   - For localhost/dev: use `smtplib` with a test SMTP server or logging
   - Production: integrate with service (SendGrid, Mailgun, etc.)
   - Templates for reset and reminder emails

4. **Validation Rules**
   ```
   Password:
   - Length: 8+ characters
   - Allowed: a-z, A-Z, 0-9, !@#$%^&*()_+-=
   - Not allowed: Unicode, spaces, non-English characters

   Username:
   - Length: 3-20 characters
   - Allowed: a-z, A-Z, 0-9, underscore
   - Must be unique

   Email:
   - Valid email format
   - Must be unique
   ```

5. **Security Considerations**
   - Rate limit login attempts
   - Rate limit password reset requests
   - Secure token transmission (HTTPS in production)
   - Don't reveal if username/email exists on reset requests

---

## Phase 1: Foundation & Authentication

*Status: Planning*

### 1.1 Project Setup
- [ ] Initialize Python project structure
- [ ] Create virtual environment
- [ ] Set up requirements.txt with dependencies
- [ ] Configure development environment
- [ ] Create main entry point (main.py)

### 1.2 Account System (Details Above)
- [ ] Implement password hashing module
- [ ] Implement token generation module
- [ ] Create account registration flow
- [ ] Create login/logout flow
- [ ] Implement email service (dev mode: logging)
- [ ] Password reset functionality
- [ ] Username reminder functionality

### 1.3 Configuration System
- [ ] Create config loader (JSON/YAML)
- [ ] Game settings configuration
- [ ] Auth settings configuration
- [ ] Environment-specific configs (dev/prod)

---

## Phase 2: Core Game Engine

*Status: Not Started*

### 2.1 Game Loop
- [ ] Main game loop implementation
- [ ] State machine for game states (menu, playing, combat, dialogue)
- [ ] Input handler for player commands
- [ ] Output formatter for text display
- [ ] Command parser (interpret player input)

### 2.2 Text Interface
- [ ] Clear screen and display functions
- [ ] Text formatting utilities (colors, styles)
- [ ] Menu system (main menu, pause menu, options)
- [ ] Prompt system for player input
- [ ] Help command and command listing

### 2.3 Data Management
- [ ] JSON/YAML loader for game data
- [ ] Data validation on load
- [ ] Caching system for frequently accessed data
- [ ] Error handling for corrupted data

### Structure
```
src/
├── engine/
│   ├── __init__.py
│   ├── game_loop.py        # Main loop and state management
│   ├── state_machine.py    # Game state transitions
│   ├── input_handler.py    # Command parsing
│   ├── output.py           # Text display and formatting
│   └── commands.py         # Command definitions
├── data/
│   ├── loader.py           # Data file loading
│   └── validator.py        # Data validation
```

---

## Phase 3: Character System

*Status: Not Started*

### 3.1 Character Creation
- [ ] Path selection (Tomas/Warrior or Pug/Mage)
- [ ] Character naming (or use canonical names)
- [ ] Initial stat allocation
- [ ] Starting equipment assignment
- [ ] Character creation summary display

### 3.2 Core Attributes
- [ ] Strength implementation
- [ ] Constitution implementation
- [ ] Agility implementation
- [ ] Intelligence implementation
- [ ] Willpower implementation
- [ ] Charisma implementation

### 3.3 Derived Stats
- [ ] Health (HP) calculation from Constitution
- [ ] Mana (MP) calculation from Willpower
- [ ] Stamina calculation
- [ ] Carry capacity from Strength
- [ ] Initiative calculation from Agility

### 3.4 Character Progression
- [ ] Experience points system
- [ ] Level up mechanics
- [ ] Stat point allocation on level up
- [ ] Ability unlocks per level
- [ ] Level caps and scaling

### Structure
```
src/
├── character/
│   ├── __init__.py
│   ├── player.py           # Player character class
│   ├── stats.py            # Attribute and stat calculations
│   ├── creation.py         # Character creation flow
│   └── progression.py      # XP and leveling
├── data/
│   └── characters/
│       ├── tomas_base.json # Tomas starting stats
│       └── pug_base.json   # Pug starting stats
```

---

## Phase 4: Combat System

*Status: Not Started*

### 4.1 Combat Engine
- [ ] Turn-based combat loop
- [ ] Initiative and turn order
- [ ] Action point system (if using)
- [ ] Combat state management
- [ ] Victory/defeat conditions

### 4.2 Actions - Warrior (Tomas)
- [ ] Basic attack (light, heavy, precise)
- [ ] Defensive stance (block, parry)
- [ ] Dodge action
- [ ] Special techniques (unlockable)
- [ ] Weapon-specific moves

### 4.3 Actions - Mage (Pug)
- [ ] Basic magical attack
- [ ] Defensive spells
- [ ] Staff/physical attack fallback
- [ ] Mana management in combat
- [ ] Spell preparation/casting time

### 4.4 Combat Mechanics
- [ ] Damage calculation (attack vs defense)
- [ ] Hit/miss chance based on stats
- [ ] Critical hits
- [ ] Status effects (stunned, bleeding, burning, etc.)
- [ ] Flee mechanics

### 4.5 Enemies
- [ ] Enemy base class
- [ ] Enemy stat templates
- [ ] Enemy AI (action selection)
- [ ] Enemy special abilities
- [ ] Boss mechanics

### Structure
```
src/
├── combat/
│   ├── __init__.py
│   ├── battle.py           # Combat loop and management
│   ├── actions.py          # Combat action definitions
│   ├── damage.py           # Damage calculations
│   ├── effects.py          # Status effects
│   └── enemy_ai.py         # Enemy behavior
├── data/
│   └── enemies/
│       ├── enemies.json    # Enemy definitions
│       └── bosses.json     # Boss definitions
```

---

## Phase 5: Magic System

*Status: Not Started*

### 5.1 Spell Framework
- [ ] Spell base class
- [ ] Spell categories (offensive, defensive, utility)
- [ ] Mana cost system
- [ ] Spell learning/unlocking
- [ ] Spell level/power scaling

### 5.2 Offensive Spells
- [ ] Direct damage spells
- [ ] Area effect spells
- [ ] Damage over time spells
- [ ] Element types (fire, ice, lightning, etc.)

### 5.3 Defensive Spells
- [ ] Shield/ward spells
- [ ] Healing spells
- [ ] Buff spells (stat increases)
- [ ] Cleanse/cure spells

### 5.4 Utility Spells
- [ ] Light spell (for dark areas)
- [ ] Detection spells
- [ ] Telekinesis
- [ ] Communication/translation

### 5.5 Greater Magic (Story-locked)
- [ ] Rift magic (late game)
- [ ] Powerful spells tied to story events
- [ ] Pug's unique abilities from training

### Structure
```
src/
├── magic/
│   ├── __init__.py
│   ├── spells.py           # Spell base class and casting
│   ├── offensive.py        # Attack spells
│   ├── defensive.py        # Defense and healing
│   ├── utility.py          # Utility spells
│   └── greater.py          # Story-unlocked magic
├── data/
│   └── spells/
│       └── spells.json     # Spell definitions
```

---

## Phase 6: Inventory System

*Status: Not Started*

### 6.1 Inventory Core
- [ ] Inventory container class
- [ ] Weight/capacity limits
- [ ] Add/remove items
- [ ] Stack management for consumables
- [ ] Inventory display

### 6.2 Item Types
- [ ] Weapons (swords, daggers, staves, bows)
- [ ] Armor (head, chest, hands, feet)
- [ ] Consumables (food, potions, scrolls)
- [ ] Key items (story objects)
- [ ] Tools (torch, rope, lockpicks)
- [ ] Valuables (gold, gems, trade goods)

### 6.3 Equipment System
- [ ] Equipment slots definition
- [ ] Equip/unequip mechanics
- [ ] Stat bonuses from equipment
- [ ] Equipment requirements (level, stats, class)
- [ ] Equipment comparison display

### 6.4 Item Interactions
- [ ] Use consumables
- [ ] Examine items (descriptions)
- [ ] Drop items
- [ ] Trade/shop interface
- [ ] Item crafting (if applicable)

### Structure
```
src/
├── inventory/
│   ├── __init__.py
│   ├── inventory.py        # Inventory management
│   ├── items.py            # Item base classes
│   ├── equipment.py        # Equipment slots and bonuses
│   └── shop.py             # Trading interface
├── data/
│   └── items/
│       ├── weapons.json
│       ├── armor.json
│       ├── consumables.json
│       └── key_items.json
```

---

## Phase 7: Survival System

*Status: Not Started*

### 7.1 Basic Needs
- [ ] Hunger system
- [ ] Thirst system
- [ ] Fatigue/rest system
- [ ] Need decay over time
- [ ] Stat penalties when needs critical

### 7.2 Resource Consumption
- [ ] Food consumption mechanics
- [ ] Water consumption mechanics
- [ ] Rest/camp mechanics
- [ ] Resource scarcity in certain areas

### 7.3 Environmental Hazards
- [ ] Weather effects (storm, cold, heat)
- [ ] Terrain hazards
- [ ] Time-based events
- [ ] Environmental damage

### 7.4 Survival Actions
- [ ] Forage for food/water
- [ ] Set up camp
- [ ] Rest and recovery
- [ ] Craft basic survival items

### Structure
```
src/
├── survival/
│   ├── __init__.py
│   ├── needs.py            # Hunger, thirst, fatigue
│   ├── environment.py      # Weather and hazards
│   └── camping.py          # Rest and recovery
```

---

## Phase 8: Story & Narrative System

*Status: Not Started*

### 8.1 Story Engine
- [ ] Chapter/scene management
- [ ] Story state tracking
- [ ] Branching dialogue system
- [ ] Choice and consequence system
- [ ] Story flags and triggers

### 8.2 Dialogue System
- [ ] NPC dialogue trees
- [ ] Player response options
- [ ] Skill/stat checks in dialogue
- [ ] Relationship tracking
- [ ] Dialogue history/log

### 8.3 Quest System
- [ ] Quest tracking
- [ ] Quest objectives
- [ ] Quest completion and rewards
- [ ] Side quests vs main story

### 8.4 World and Locations
- [ ] Location definitions
- [ ] Navigation between locations
- [ ] Location descriptions
- [ ] Location-specific events
- [ ] Points of interest

### 8.5 NPCs
- [ ] NPC definitions
- [ ] NPC schedules/availability
- [ ] NPC relationships/attitudes
- [ ] Companion system (if applicable)

### 8.6 Story Content - Tomas Path
- [ ] Chapter 1: Crydee and the Shipwreck
- [ ] Chapter 2: The Tsurani Invasion
- [ ] Chapter 3: Tomas and the Dragon
- [ ] Chapter 4: The Valheru Armor
- [ ] Chapter 5: Elvandar
- [ ] (Additional chapters per book events)

### 8.7 Story Content - Pug Path
- [ ] Chapter 1: Crydee and Apprenticeship
- [ ] Chapter 2: The Tsurani Invasion
- [ ] Chapter 3: Capture and Slavery
- [ ] Chapter 4: Kelewan and the Assembly
- [ ] Chapter 5: Becoming Milamber
- [ ] (Additional chapters per book events)

### Structure
```
src/
├── story/
│   ├── __init__.py
│   ├── engine.py           # Story state and flow
│   ├── dialogue.py         # Dialogue system
│   ├── quests.py           # Quest tracking
│   ├── locations.py        # World navigation
│   └── npcs.py             # NPC management
├── data/
│   └── story/
│       ├── tomas/
│       │   ├── chapter1.json
│       │   └── ...
│       ├── pug/
│       │   ├── chapter1.json
│       │   └── ...
│       ├── locations.json
│       ├── npcs.json
│       └── dialogues/
```

---

## Phase 9: Save/Load System

*Status: Not Started*

### 9.1 Save System
- [ ] Save game state to file
- [ ] Multiple save slots
- [ ] Auto-save functionality
- [ ] Save file encryption (prevent tampering)
- [ ] Save metadata (timestamp, location, chapter)

### 9.2 Load System
- [ ] Load game from save file
- [ ] Save file validation
- [ ] Corrupted save handling
- [ ] Save file listing/selection

### 9.3 Game State Serialization
- [ ] Player character state
- [ ] Inventory state
- [ ] Story progress state
- [ ] World state (NPC positions, events triggered)
- [ ] Statistics (playtime, kills, etc.)

### Structure
```
src/
├── save/
│   ├── __init__.py
│   ├── save_manager.py     # Save/load operations
│   ├── serializer.py       # State serialization
│   └── encryption.py       # Save file security
├── data/
│   └── saves/              # Save file storage
```

---

## Phase 10: Polish & Testing

*Status: Not Started*

### 10.1 Testing
- [ ] Unit tests for core systems
- [ ] Integration tests
- [ ] Combat balance testing
- [ ] Story playthrough testing
- [ ] Edge case handling

### 10.2 Balance
- [ ] Stat balance (Tomas vs Pug viability)
- [ ] Combat difficulty curve
- [ ] Economy balance (gold, items)
- [ ] Survival difficulty tuning
- [ ] XP and level progression rate

### 10.3 Quality of Life
- [ ] Tutorial/help system
- [ ] Command shortcuts
- [ ] Quick save/load
- [ ] Settings menu (text speed, colors)
- [ ] Accessibility options

### 10.4 Documentation
- [ ] Player manual/guide
- [ ] Code documentation
- [ ] API documentation (for modding)
- [ ] Installation instructions

### 10.5 Release Preparation
- [ ] Final bug fixes
- [ ] Performance optimization
- [ ] Package for distribution
- [ ] Create release notes

---

## Complete Project Structure

```
The-Magician/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── README.md
├── features.md
├── todo.md
├── src/
│   ├── __init__.py
│   ├── auth/               # Phase 1: Authentication
│   ├── engine/             # Phase 2: Core Engine
│   ├── character/          # Phase 3: Character System
│   ├── combat/             # Phase 4: Combat System
│   ├── magic/              # Phase 5: Magic System
│   ├── inventory/          # Phase 6: Inventory System
│   ├── survival/           # Phase 7: Survival System
│   ├── story/              # Phase 8: Story System
│   ├── save/               # Phase 9: Save/Load
│   ├── config/             # Configuration
│   └── utils/              # Shared utilities
├── data/
│   ├── users/              # Player accounts
│   ├── saves/              # Save files
│   ├── characters/         # Character templates
│   ├── enemies/            # Enemy definitions
│   ├── items/              # Item definitions
│   ├── spells/             # Spell definitions
│   └── story/              # Story content
│       ├── tomas/
│       ├── pug/
│       ├── locations.json
│       ├── npcs.json
│       └── dialogues/
└── tests/                  # Phase 10: Testing
    ├── test_auth.py
    ├── test_combat.py
    ├── test_inventory.py
    └── ...
```

---

## Development Priority

1. **Phase 1** - Foundation (accounts, config) - *Required for any gameplay*
2. **Phase 2** - Core Engine (game loop, text interface) - *Required for any gameplay*
3. **Phase 3** - Character System - *Required for gameplay*
4. **Phase 8** - Story System (basic) - *Required for narrative*
5. **Phase 6** - Inventory System - *Core gameplay*
6. **Phase 4** - Combat System - *Core gameplay*
7. **Phase 5** - Magic System - *Pug path requirement*
8. **Phase 7** - Survival System - *Enhancement*
9. **Phase 9** - Save/Load - *Critical for playability*
10. **Phase 10** - Polish & Testing - *Pre-release*
