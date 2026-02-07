/**
 * The Magician - Text Adventure RPG
 * Based on Raymond E. Feist's Magician series
 */

// Game State
const GameState = {
  MENU: 'menu',
  LOGIN: 'login',
  REGISTER: 'register',
  CHARACTER_SELECT: 'character_select',
  PLAYING: 'playing'
};

// Character Data
const characters = {
  tomas: {
    name: 'Tomas',
    path: 'Warrior',
    description: 'Follow the path of martial prowess and ancient power. Face the Tsurani invasion and discover the secrets of the Valheru.',
    stats: { strength: 14, constitution: 13, agility: 12, intelligence: 10, willpower: 11, charisma: 12 },
    startingLocation: 'You stand in the courtyard of Castle Crydee. The morning sun casts long shadows across the stone walls. The sound of wooden practice swords clashing echoes from the training grounds.',
    inventory: ['Wooden Practice Sword', 'Leather Jerkin', 'Bread Loaf x2', 'Waterskin', 'Copper Coins x10']
  },
  pug: {
    name: 'Pug',
    path: 'Mage',
    description: 'Follow the path of magic and knowledge. From apprentice to master, across two worlds, become the greatest magician of the age.',
    stats: { strength: 9, constitution: 10, agility: 11, intelligence: 15, willpower: 14, charisma: 11 },
    startingLocation: 'You are in Kulgan\'s study, surrounded by towering shelves of ancient books and mysterious scrolls. Dust motes dance in the light streaming through the window.',
    inventory: ['Wooden Staff', 'Apprentice Robes', 'Candle x3', 'Bread Loaf x2', 'Waterskin', 'Copper Coins x5']
  }
};

// Game class
class Game {
  constructor() {
    this.state = GameState.MENU;
    this.player = null;
    this.character = null;
    this.messageHistory = [];
    this.app = document.getElementById('app');
    this.load();
    this.render();
  }

  // Save game state to localStorage
  save() {
    const saveData = {
      player: this.player,
      character: this.character,
      messageHistory: this.messageHistory.slice(-20) // Keep last 20 messages
    };
    localStorage.setItem('magician_save', JSON.stringify(saveData));
  }

  // Load game state from localStorage
  load() {
    const saveData = localStorage.getItem('magician_save');
    if (saveData) {
      const data = JSON.parse(saveData);
      this.player = data.player;
      this.character = data.character;
      this.messageHistory = data.messageHistory || [];
      if (this.player && this.character) {
        this.state = GameState.PLAYING;
      }
    }
  }

  // Clear save data
  clearSave() {
    localStorage.removeItem('magician_save');
    this.player = null;
    this.character = null;
    this.messageHistory = [];
    this.state = GameState.MENU;
    this.render();
  }

  // Render current state
  render() {
    switch (this.state) {
      case GameState.MENU:
        this.renderMenu();
        break;
      case GameState.LOGIN:
        this.renderLogin();
        break;
      case GameState.REGISTER:
        this.renderRegister();
        break;
      case GameState.CHARACTER_SELECT:
        this.renderCharacterSelect();
        break;
      case GameState.PLAYING:
        this.renderGame();
        break;
    }
  }

  renderMenu() {
    this.app.innerHTML = `
      <div class="text-center mb-12">
        <h1 class="text-5xl font-bold text-red-500 mb-4">THE MAGICIAN</h1>
        <p class="text-xl text-gray-400">A Text Adventure RPG</p>
        <p class="text-sm text-gray-500 mt-2">Based on the works of Raymond E. Feist</p>
      </div>

      <div class="card">
        <div class="space-y-4">
          <button id="btn-login" class="btn w-full">Continue Journey</button>
          <button id="btn-register" class="btn-secondary w-full">New Adventure</button>
        </div>
      </div>

      <p class="text-center text-gray-500 mt-8 text-sm">
        Choose your path: Warrior or Mage
      </p>
    `;

    document.getElementById('btn-login').addEventListener('click', () => {
      this.state = GameState.LOGIN;
      this.render();
    });

    document.getElementById('btn-register').addEventListener('click', () => {
      this.state = GameState.REGISTER;
      this.render();
    });
  }

  renderLogin() {
    this.app.innerHTML = `
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-red-500 mb-2">Continue Journey</h1>
        <p class="text-gray-400">Welcome back, adventurer</p>
      </div>

      <div class="card">
        <form id="login-form" class="space-y-4">
          <div>
            <label class="block text-gray-300 mb-2">Username</label>
            <input type="text" id="username" class="input" placeholder="Enter your name" required>
          </div>
          <div>
            <label class="block text-gray-300 mb-2">Password</label>
            <input type="password" id="password" class="input" placeholder="Enter password" required>
          </div>
          <button type="submit" class="btn w-full mt-6">Enter</button>
        </form>
        <button id="btn-back" class="btn-secondary w-full mt-4">Back</button>
      </div>
    `;

    document.getElementById('login-form').addEventListener('submit', (e) => {
      e.preventDefault();
      const username = document.getElementById('username').value.trim();
      if (username) {
        this.player = { username };
        this.state = GameState.CHARACTER_SELECT;
        this.render();
      }
    });

    document.getElementById('btn-back').addEventListener('click', () => {
      this.state = GameState.MENU;
      this.render();
    });
  }

  renderRegister() {
    this.app.innerHTML = `
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-red-500 mb-2">New Adventure</h1>
        <p class="text-gray-400">Begin your journey through Midkemia</p>
      </div>

      <div class="card">
        <form id="register-form" class="space-y-4">
          <div>
            <label class="block text-gray-300 mb-2">Choose Your Name</label>
            <input type="text" id="username" class="input" placeholder="Your adventurer name" required minlength="3">
          </div>
          <div>
            <label class="block text-gray-300 mb-2">Email</label>
            <input type="email" id="email" class="input" placeholder="your@email.com" required>
          </div>
          <div>
            <label class="block text-gray-300 mb-2">Password</label>
            <input type="password" id="password" class="input" placeholder="Min 8 characters" required minlength="8">
          </div>
          <button type="submit" class="btn w-full mt-6">Begin Adventure</button>
        </form>
        <button id="btn-back" class="btn-secondary w-full mt-4">Back</button>
      </div>
    `;

    document.getElementById('register-form').addEventListener('submit', (e) => {
      e.preventDefault();
      const username = document.getElementById('username').value.trim();
      if (username) {
        this.player = { username };
        this.state = GameState.CHARACTER_SELECT;
        this.render();
      }
    });

    document.getElementById('btn-back').addEventListener('click', () => {
      this.state = GameState.MENU;
      this.render();
    });
  }

  renderCharacterSelect() {
    this.app.innerHTML = `
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-red-500 mb-2">Choose Your Path</h1>
        <p class="text-gray-400">Two boys from Crydee will shape the fate of two worlds</p>
      </div>

      <div class="grid gap-6 md:grid-cols-2">
        <div class="card hover:border-red-500 transition-colors cursor-pointer" id="select-tomas">
          <h2 class="text-2xl font-bold text-red-400 mb-2">TOMAS</h2>
          <p class="text-amber-400 mb-4">The Warrior</p>
          <p class="text-gray-300 text-sm">${characters.tomas.description}</p>
          <div class="mt-4 text-xs text-gray-500">
            STR ${characters.tomas.stats.strength} | CON ${characters.tomas.stats.constitution} | AGI ${characters.tomas.stats.agility}
          </div>
        </div>

        <div class="card hover:border-red-500 transition-colors cursor-pointer" id="select-pug">
          <h2 class="text-2xl font-bold text-red-400 mb-2">PUG</h2>
          <p class="text-blue-400 mb-4">The Mage</p>
          <p class="text-gray-300 text-sm">${characters.pug.description}</p>
          <div class="mt-4 text-xs text-gray-500">
            INT ${characters.pug.stats.intelligence} | WIL ${characters.pug.stats.willpower} | CHA ${characters.pug.stats.charisma}
          </div>
        </div>
      </div>

      <button id="btn-back" class="btn-secondary w-full mt-6">Back</button>
    `;

    document.getElementById('select-tomas').addEventListener('click', () => {
      this.selectCharacter('tomas');
    });

    document.getElementById('select-pug').addEventListener('click', () => {
      this.selectCharacter('pug');
    });

    document.getElementById('btn-back').addEventListener('click', () => {
      this.state = GameState.MENU;
      this.render();
    });
  }

  selectCharacter(charKey) {
    this.character = { ...characters[charKey], key: charKey };
    this.messageHistory = [];
    this.addMessage(this.character.startingLocation);
    this.state = GameState.PLAYING;
    this.save();
    this.render();
  }

  addMessage(text, isCommand = false) {
    this.messageHistory.push({ text, isCommand, timestamp: Date.now() });
    if (this.messageHistory.length > 50) {
      this.messageHistory = this.messageHistory.slice(-50);
    }
  }

  renderGame() {
    const stats = this.character.stats;
    const hp = stats.constitution * 10;
    const mp = stats.willpower * (this.character.key === 'pug' ? 10 : 2);

    this.app.innerHTML = `
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-2xl font-bold text-red-500">${this.character.name}</h1>
          <p class="text-gray-400 text-sm">${this.character.path} | ${this.player.username}</p>
        </div>
        <div class="text-right text-sm">
          <span class="text-red-400">HP: ${hp}</span> |
          <span class="text-blue-400">MP: ${mp}</span>
        </div>
      </div>

      <div class="game-text mb-6 max-h-96 overflow-y-auto" id="game-output">
        ${this.messageHistory.map(m => `
          <p class="${m.isCommand ? 'text-amber-400' : 'text-gray-300'} mb-3">
            ${m.isCommand ? '> ' : ''}${m.text}
          </p>
        `).join('')}
      </div>

      <form id="command-form" class="flex gap-3 mb-6">
        <input type="text" id="command-input" class="input flex-1"
               placeholder="Enter command (try: look, inventory, stats, help)"
               autocomplete="off" autofocus>
        <button type="submit" class="btn">Enter</button>
      </form>

      <div class="flex flex-wrap gap-2 mb-6">
        <button class="btn-secondary text-sm py-2 px-4" data-cmd="look">Look</button>
        <button class="btn-secondary text-sm py-2 px-4" data-cmd="inventory">Inventory</button>
        <button class="btn-secondary text-sm py-2 px-4" data-cmd="stats">Stats</button>
        <button class="btn-secondary text-sm py-2 px-4" data-cmd="help">Help</button>
      </div>

      <div class="flex gap-4 text-sm">
        <button id="btn-menu" class="text-gray-400 hover:text-red-400">Main Menu</button>
        <button id="btn-clear" class="text-gray-400 hover:text-red-400">New Game</button>
      </div>
    `;

    // Scroll to bottom of output
    const output = document.getElementById('game-output');
    output.scrollTop = output.scrollHeight;

    // Command form
    document.getElementById('command-form').addEventListener('submit', (e) => {
      e.preventDefault();
      const input = document.getElementById('command-input');
      const command = input.value.trim();
      if (command) {
        this.processCommand(command);
        input.value = '';
      }
    });

    // Quick command buttons
    document.querySelectorAll('[data-cmd]').forEach(btn => {
      btn.addEventListener('click', () => {
        this.processCommand(btn.dataset.cmd);
      });
    });

    // Menu buttons
    document.getElementById('btn-menu').addEventListener('click', () => {
      this.state = GameState.MENU;
      this.render();
    });

    document.getElementById('btn-clear').addEventListener('click', () => {
      if (confirm('Start a new game? Current progress will be lost.')) {
        this.clearSave();
      }
    });
  }

  processCommand(command) {
    const cmd = command.toLowerCase().trim();
    this.addMessage(command, true);

    let response = '';

    switch (cmd) {
      case 'help':
        response = 'Available commands: look, inventory, stats, help, about';
        break;

      case 'look':
        response = this.character.startingLocation;
        break;

      case 'inventory':
      case 'inv':
      case 'i':
        response = 'Inventory: ' + this.character.inventory.join(', ');
        break;

      case 'stats':
        const s = this.character.stats;
        response = `Stats: Strength ${s.strength}, Constitution ${s.constitution}, Agility ${s.agility}, Intelligence ${s.intelligence}, Willpower ${s.willpower}, Charisma ${s.charisma}`;
        break;

      case 'about':
        response = 'The Magician is a text adventure RPG based on Raymond E. Feist\'s Magician: Apprentice and Magician: Master. You are playing as ' + this.character.name + ', following the ' + this.character.path + ' path.';
        break;

      default:
        response = `Unknown command: "${command}". Type "help" for available commands.`;
    }

    this.addMessage(response);
    this.save();
    this.render();
  }
}

// Start the game
const game = new Game();
