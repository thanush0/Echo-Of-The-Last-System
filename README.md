# Echo of the Last System

A narrative-driven adventure RPG set in a ruined fantasy world where reality itself is managed by a failing System operating at 12% integrity.

## Overview

You awaken with no memories, designated only as "Unknown," and must navigate a world where quests can fail, stats can randomly shift, and the AI managing reality might be lying to you. You are User #10,392—the previous 10,391 failed to escape the cycle.

## Features

- **Five Distinct Endings** based on corruption level, choices, and discovered truths
- **Turn-based Combat** with enemy evolution and hidden mechanics
- **System Glitches** that alter stats, quests, and reality itself
- **Action-based Stat Progression** - Your playstyle shapes your character
- **Persistent NPC Memory** - Characters remember your choices
- **Three Save Slots** with full game state preservation
- **Four Interface Options** - Terminal, Basic GUI, Advanced GUI, and Pygame GUI
- **Zero-install GUI** using Python's built-in Tkinter

## Quick Start

### Windows (Recommended)

1. Download the latest release
2. Extract the zip file
3. Run `EchoOfTheLastSystem-GUI.exe`

### Python Source (All Platforms)

**Requirements:**
- Python 3.6+
- No additional libraries for CLI and Tkinter GUIs
- Pygame 2.0+ (optional, only for Pygame GUI)

**Installation:**

```bash
git clone https://github.com/yourusername/echo-of-the-last-system.git
cd echo-of-the-last-system
cd adventure_game
```

**Run the game:**

```bash
# Advanced Modern GUI (Recommended)
python gui_advanced.py

# Basic Tkinter GUI
python gui_tkinter.py

# Terminal/CLI version
python main.py

# Pygame GUI (requires: pip install pygame)
python gui_main.py
```

## Interface Options

### CLI (Terminal)
- Pure text interface
- Runs in any terminal
- Zero dependencies
- Complete gameplay experience

### Basic Tkinter GUI
- Simple windowed interface
- Built-in (no pip install)
- Status panel and buttons
- Mouse and keyboard controls

### Advanced Modern GUI (Recommended)
- Cyberpunk-inspired design
- Animated status bars
- Character customization
- Save slot previews
- Still zero-install (uses Tkinter)

### Pygame GUI
- Visual glitch effects
- CRT scanline simulation
- Screen distortion effects
- Requires `pip install pygame`

## Gameplay

### Combat
- **Attack** - Deal damage (builds Strength)
- **Analyze** - Reveal enemy info (builds Intelligence)
- **Skill** - Use special abilities
- **Flee** - Escape combat (builds Agility)

### System Mechanics
The broken System at 12% integrity causes:
- Text corruption and glitches
- Random stat modifications
- Quest mutations and failures
- Reality shifts
- Forbidden skill unlocks

### Endings
Five distinct endings available:
1. **Survival** - Outlast the System
2. **System Takeover** - Merge with the broken AI
3. **World Collapse** - Witness final failure
4. **Godless Freedom** - Destroy the System and escape
5. **True Ending** - Hidden, requires balance and discovery

## Building from Source

### Create Standalone Executables

**Windows:**
```bash
cd adventure_game
BUILD_BOTH.bat
```

**Manual:**
```bash
pip install pyinstaller
python -m PyInstaller --onefile --name="EchoOfTheLastSystem-CLI" --console main.py
python -m PyInstaller --onefile --name="EchoOfTheLastSystem-GUI" --windowed gui_advanced.py
```

Executables will be in the `dist/` folder.

## Project Structure

```
adventure_game/
├── main.py              # CLI game loop
├── player.py            # Player stats and progression
├── system.py            # System AI and glitch mechanics
├── world.py             # World exploration
├── combat.py            # Combat engine
├── enemies.py           # Enemy definitions
├── dialogue.py          # NPC dialogue system
├── quests.py            # Quest management
├── save_load.py         # Save/load functionality
├── gui_advanced.py      # Modern GUI (recommended)
├── gui_tkinter.py       # Basic GUI
├── gui_main.py          # Pygame GUI
├── test_game.py         # Test suite
└── automated_test.py    # Automated tests
```

## Testing

Run automated tests:

```bash
cd adventure_game
python automated_test.py
```

All core systems are covered by automated tests.

## Technical Details

### Architecture
- Modular design with separated concerns
- Game logic independent of interface
- Four complete interfaces sharing core systems
- JSON-based save system with full state persistence

### Code Statistics
- ~7,500 lines of Python
- 16 core modules
- 5 enemy types
- 6+ skills
- 15+ glitch types
- 12+ story flags

## Documentation

See `adventure_game/docs/` folder for:
- Complete walkthrough
- Quick start guide
- Build instructions
- Distribution guide

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Developed as a complete adventure RPG demonstrating narrative design, modular architecture, and multiple interface implementations.

## Project Status

Version 1.0.0 - Feature complete and stable. This is a finished game, not early access.

## Save Files

Save files are stored in `adventure_game/saves/` and are automatically managed by the game. Three save slots are available, and progress is preserved between sessions.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**"You are Unknown because you refused to be Known."** — The Oracle.
