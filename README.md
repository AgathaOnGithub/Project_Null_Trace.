# NULL_TRACE

NULL_TRACE is a terminal-based, retro-styled hacking and digital forensics simulation game. Built entirely with Python and the `tcod` library, it offers an immersive, full-screen cyberpunk experience reminiscent of classic DOS systems and early text-based RPGs.

## Overview

In NULL_TRACE, you play as a newly activated digital forensics agent navigating through corrupted systems and encrypted network nodes. Your primary objective is to infiltrate the system, locate hidden data files, and eliminate anomalous entities (Glitches) and rogue security protocols (System Admins) that stand in your way.

The game blends traditional roguelike exploration with typing-based combat and classic RPG mechanics, all presented through a highly stylized, retro-CRT visual interface.

## Key Features

* **True Terminal Aesthetics:** Experience a fully realized retro environment complete with dynamic Matrix rain, CRT scanline effects, and authentic phosphor-glow visual filtering.
* **Immersive Boot Sequence:** Every session begins with a simulated DOS-era system boot sequence, setting the tone before you even access the main menu.
* **Roguelike Exploration:** Navigate procedurally generated nodes (dungeons) with field-of-view (FOV) and exploration mechanics.
* **Dual Combat Systems:**
    * **Typing Puzzles:** Defeat standard 'Glitch' enemies by quickly and accurately typing the correct code patches to fix syntax errors or memory leaks.
    * **POV RPG Boss Battles:** Confront 'System Admin' mini-bosses in a classic, turn-based RPG perspective (inspired by Final Fantasy). Choose tactical commands to override their defenses while managing your system integrity.
* **Dynamic UI:** The interface shifts seamlessly between exploration mapping, real-time system logs, dialogue transmissions, and dedicated combat HUDs.
* **Standalone Executable:** Designed to be built and distributed as a standalone desktop application, requiring no web browser or external dependencies for the end-user.

## Installation and Execution (From Source)

To run the game directly from the Python source code, you will need Python installed on your system along with the necessary libraries.

### Prerequisites

1.  Python 3.x
2.  `tcod` library
3.  `numpy` library

### Setup

1.  Clone this repository to your local machine.
2.  Open your terminal or command prompt.
3.  Navigate to the cloned directory.
4.  Install the required dependencies using pip:
    ```bash
    pip install tcod numpy
    ```
5.  Ensure the font file `dejavu10x10_gs_tc.png` is located in the same directory as the main Python script.
6.  Run the game:
    ```bash
    python null_trace.py
    ```
    *(Note: Replace `null_trace.py` with the actual name of the main script file if different).*

## Controls

* **W, A, S, D / Arrow Keys:** Move your agent (@) around the map. Also used to navigate menus.
* **E:** Interact with objects (e.g., hack Data Files).
* **Enter:** Confirm selection in menus, execute typed code in battles, or advance dialogue.
* **Backspace:** Delete characters while typing during a puzzle battle.
* **Escape (ESC):** Disconnect (return to the Main Menu or exit the game).
* **Keyboard (A-Z, 0-9, Symbols):** Used for typing code solutions during puzzle battles.

## Building the Executable

You can compile the source code into a standalone executable using PyInstaller. This allows others to play the game without installing Python.

1.  Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```
2.  Build the executable (hiding the background console):
    ```bash
    pyinstaller --noconsole null_trace.py
    ```
3.  Once the build process is complete, navigate to the newly created `dist` directory, then into the `null_trace` folder.
4.  **Crucial Step:** Copy the font file `dejavu10x10_gs_tc.png` from the root directory and paste it into this `dist/null_trace` folder, alongside the generated `.exe` file.

The game is now ready to be distributed or played directly from the executable.

## License

This project is open-source. Feel free to modify, distribute, and learn from the code.
