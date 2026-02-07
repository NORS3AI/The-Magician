# CLAUDE.md

Project context and instructions for Claude Code sessions.

## Project Overview

**The-Magician** is a text adventure RPG based on Raymond E. Feist's *Magician: Apprentice* and *Magician: Master* from the Riftwar Saga.

- **Genre:** Text Adventure RPG with survival elements
- **Platform:** Vite + Tailwind CSS (static site for GitHub Pages)
- **Two playable paths:** Tomas (Warrior) or Pug (Mage)

## Tech Stack

- **Vite** - Build tool and dev server
- **Tailwind CSS v4** - Styling
- **Vanilla JavaScript** - Game logic (no framework)
- **GitHub Pages** - Hosting
- **localStorage** - Game saves

## Current Status

### Completed
- [x] README.md - Base project description
- [x] features.md - Complete feature documentation
- [x] todo.md - All 10 development phases with detailed tasks
- [x] Vite + Tailwind project setup
- [x] index.html - Main entry point
- [x] src/main.js - Complete game logic with state machine
- [x] src/style.css - Tailwind styles with custom components
- [x] GitHub Actions workflow for deployment
- [x] Character selection (Tomas/Pug)
- [x] Basic commands (look, inventory, stats, help)
- [x] localStorage save/load system
- [x] Dark theme responsive UI

### In Progress
- Deploying to GitHub Pages

### Not Started
- Phases 2-10 from todo.md (see for full breakdown)
- Story content for chapters
- Combat system
- More game commands

## Key Files

```
index.html           - Main HTML entry point
src/main.js          - Game logic (state machine, commands, save/load)
src/style.css        - Tailwind CSS with custom components
vite.config.js       - Vite config (base path for GitHub Pages)
postcss.config.js    - PostCSS config for Tailwind
tailwind.config.js   - Tailwind theme customization
.github/workflows/deploy.yml - GitHub Pages deployment
```

## Running the Game

### Development
```bash
npm install
npm run dev
# Opens at http://localhost:5173
```

### Build for Production
```bash
npm run build
npm run preview  # Preview the build locally
```

### Deploy
Push to main/master branch - GitHub Actions will build and deploy automatically.

**Live URL:** https://NORS3AI.github.io/The-Magician/

## Development Branch

Currently on: `claude/review-readme-B7Lvc`

## Next Steps

1. **Merge to main** - Trigger GitHub Pages deployment
2. **Enable GitHub Pages** - Settings > Pages > Source: GitHub Actions
3. **Test on iPad** - Visit the live URL
4. **Expand game** - Add more commands, story content, combat

## User Preferences

- User is on iPad, needs web access (GitHub Pages solves this)
- Dark theme UI preferred
- Game should stay faithful to Feist's world

## Legacy Python Files

The Python files (main.py, app.py, src/, etc.) are from the original implementation.
They can be removed or kept for reference. The game now runs entirely in the browser.

## Notes

- Build output goes to `dist/` folder
- Game state saved to localStorage
- Tailwind v4 uses `@tailwindcss/postcss` plugin
- Base path set to `/The-Magician/` for GitHub Pages
