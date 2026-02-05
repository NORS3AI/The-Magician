# CLAUDE.md

Project context and instructions for Claude Code sessions.

## Project Overview

**The-Magician** is a text adventure RPG based on Raymond E. Feist's *Magician: Apprentice* and *Magician: Master* from the Riftwar Saga.

- **Genre:** Text Adventure RPG with survival elements
- **Platform:** Python (CLI + Flask web interface)
- **Two playable paths:** Tomas (Warrior) or Pug (Mage)

## Current Status

### Completed
- [x] README.md - Base project description
- [x] features.md - Complete feature documentation
- [x] todo.md - All 10 development phases with detailed tasks
- [x] Project structure created (src/, data/, tests/, config/)
- [x] main.py - CLI entry point (working)
- [x] app.py - Flask web interface (working with full authentication)
- [x] Basic game loop with state machine
- [x] Character selection (Tomas/Pug)
- [x] HTML templates with dark theme
- [x] Configuration system (YAML)
- [x] Character base data (tomas_base.json, pug_base.json)
- [x] **Phase 1: Authentication System (COMPLETE)**
  - [x] Password hashing with bcrypt
  - [x] Token generation and management
  - [x] User storage system (JSON-based)
  - [x] Account registration with validation
  - [x] Login/logout with session management
  - [x] Email service (dev mode with logging)
  - [x] Password reset functionality
  - [x] Username reminder functionality
  - [x] Comprehensive unit tests (36 tests passing)
- [x] Deployment configuration (Render, Railway, Fly.io)

### In Progress
- None

### Not Started
- Phases 2-10 (see todo.md for full breakdown)

## Key Files

```
main.py                     - CLI game entry point
app.py                      - Flask web server with full auth (port 5000)
config/game.yaml            - Game configuration
src/auth/                   - Authentication system
  ├── account.py            - Account management
  ├── password.py           - Password hashing/validation
  ├── token.py              - Token generation/management
  ├── user_storage.py       - User data persistence
  └── email_service.py      - Email notifications
src/engine/game_loop.py     - Core game loop
src/config/settings.py      - Config loader
src/utils/validation.py     - Input validation
data/characters/            - Tomas and Pug base stats
data/users/                 - User account storage
templates/                  - HTML templates for web UI
tests/test_auth.py          - Authentication unit tests
DEPLOYMENT.md               - Deployment guide for cloud hosting
```

## Running the Game

### CLI Mode
```bash
source venv/bin/activate
python main.py
```

### Web Mode
```bash
source venv/bin/activate
python app.py
# Opens at http://localhost:5000
```

## Development Branch

Currently on: `claude/update-play-link-gnIsm`

## Next Steps

1. **For iPad access:** Deploy to Render.com (see DEPLOYMENT.md)
2. **Phase 2:** Expand game engine with more commands and text interface
3. **Phase 3:** Implement character progression system
4. **Phase 8:** Start story content for Chapter 1

## User Preferences

- User is on iPad, needs web interface for testing
- Python is the chosen language
- Dark theme UI preferred
- Game should stay faithful to Feist's world

## Notes

- venv is set up with all dependencies installed
- Flask server runs on 0.0.0.0:5000 (accessible on local network)
- Tests pass: `pytest tests/ -v`
