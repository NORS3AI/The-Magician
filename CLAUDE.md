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
- [x] app.py - Flask web interface (working)
- [x] Basic game loop with state machine
- [x] Character selection (Tomas/Pug)
- [x] HTML templates with dark theme
- [x] Configuration system (YAML)
- [x] Character base data (tomas_base.json, pug_base.json)

### In Progress
- Phase 1: Authentication system (skeleton exists, needs implementation)
- Web interface needs public access solution for iPad testing

### Not Started
- Phases 2-10 (see todo.md for full breakdown)

## Key Files

```
main.py          - CLI game entry point
app.py           - Flask web server (port 5000)
config/game.yaml - Game configuration
src/engine/game_loop.py - Core game loop
src/config/settings.py  - Config loader
data/characters/ - Tomas and Pug base stats
templates/       - HTML templates for web UI
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

Currently on: `claude/review-readme-B7Lvc`

## Next Steps

1. **For iPad access:** Set up ngrok or deploy to cloud hosting
2. **Phase 1 completion:** Implement actual authentication (bcrypt, tokens, email)
3. **Phase 2:** Expand game engine with more commands
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
