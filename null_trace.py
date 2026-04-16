import random
import numpy as np
import tcod
import time
import textwrap
import sys

FONT_FILE = "dejavu10x10_gs_tc.png"

COLOR_BG = (2, 2, 5)
COLOR_UI_BG = (5, 10, 15)
COLOR_BORDER = (0, 150, 50)
COLOR_BORDER_ACTIVE = (0, 255, 100)
COLOR_TEXT = (200, 255, 200)
COLOR_TEXT_DIM = (70, 100, 70)
COLOR_WALL = (20, 30, 30)
COLOR_WALL_DARK = (10, 15, 15)
COLOR_FLOOR = (10, 15, 20)
COLOR_FLOOR_DARK = (5, 5, 10)
COLOR_PLAYER = (0, 255, 255)
COLOR_ENEMY = (255, 50, 50)
COLOR_BOSS = (255, 0, 255)
COLOR_ACCENT = (0, 255, 120)
COLOR_WARNING = (255, 180, 0)
COLOR_HP_BAR = (0, 255, 255)
COLOR_HP_BG = (0, 50, 50)

SCREEN_W = 120
SCREEN_H = 70
SIDEBAR_W = 35
BOTTOM_PANEL_H = 15
MAP_VIEW_W = SCREEN_W - SIDEBAR_W
MAP_VIEW_H = SCREEN_H - BOTTOM_PANEL_H

SYSTEM_ADMIN_ASCII_BATTLE = [
    r"        _,.-------.,_        ",
    r"     ,;~'             '~;,   ",
    r"   ,;                     ;, ",
    r"  ;    ,                   ; ",
    r" ,'   / \                 /' ",
    r",;   |   |               ;   ",
    r"|    |   |               |   ",
    r"|    |   |               |   ",
    r"|    |   |               |   ",
    r"|    \   /               |   ",
    r"|     `-'               ,'   ",
    r"|                      ;     ",
    r" ;                    ;      ",
    r"  ;                  ;       ",
    r"   ;,              ,;        ",
    r"     ';,        ,;'          ",
    r"        '------'             ",
    r"     [ ACCESS DENIED ]       "
]

GLITCH_ART = [
    "      .---.      ",
    "     /     \\     ",
    "    | () () |    ",
    "     \\  ^  /     ",
    "    __|||||__    ",
    "   / _     _ \\   ",
    "  | | |   | | |  ",
    "  |_| |___| |_|  ",
    "     ERROR       "
]

MISSION_DATA = {
    0: {
        "title": "EPISODE 0: AWAKENING",
        "loc_name": "SYS/BOOT_SECTOR",
        "start_dialog": "SYSTEM INITIALIZATION...\n\nAgen NULL_TRACE, Anda baru saja diaktifkan. Modul memori Anda terfragmentasi.\n\n[ OBJEKTIF TUTORIAL ]:\n1. Gunakan 'WASD' atau Panah untuk bergerak.\n2. Hampiri dan retas File Data ( 💾 ) menggunakan tombol 'E'.\n3. Atasi anomali ringan yang menghalangi.\n4. Akses terminal keluar ( > ).",
        "end_dialog": "CALIBRATION COMPLETE.\n\n[LOG_TXT]: 'Sistem stabil. Memulai proses intrusi ke gateway utama.'\n\nMenuju sektor berikutnya.",
    },
    1: {
        "title": "EPISODE 1: INTRUSION",
        "loc_name": "SYS/GATEWAY_01",
        "start_dialog": "MEMASUKI GATEWAY_01...\n\nAgen NULL_TRACE, ini adalah target pertama Anda.\n\n1. Temukan dan retas File Data ( 💾 ).\n2. Kalahkan Mini-Boss yang menjaga pintu keluar.\n3. Capai pintu keluar ( > ).",
        "end_dialog": "DATA ACQUIRED.\n\nMemecahkan enkripsi file...\n[LOG_TXT]: 'Protokol Admin telah diaktifkan. Akses keluar dikunci secara manual.'\n\nWARNING: Kalahkan SYSTEM_ADMIN untuk membuka gerbang.",
    }
}

ENEMY_PUZZLES = {
    "TUTORIAL_BUG": {
        "puzzle_title": "[ SYNTAX ERROR ]",
        "puzzle_desc": "Inisialisasi variabel string dasar.\nCODE: x = Hello\nTASK: Tambahkan tanda kutip 'Hello'",
        "puzzle_solution": "'Hello'",
        "dmg": 5,
    },
    "GLITCH": {
        "puzzle_title": "[ MEMORY LEAK ]",
        "puzzle_desc": "Hentikan eksekusi kode berulang.\nCODE: print('Error')\nTASK: Ubah jadi 'pass'",
        "puzzle_solution": "pass",
        "dmg": 10,
    },
    "SYSTEM_ADMIN": {
        "puzzle_title": "[ MINI BOSS: SYS_ADMIN ]",
        "dmg": 25,
        "max_hp": 200
    }
}

class MessageLog:
    def __init__(self, width, height):
        self.messages = []
        self.width = width
        self.height = height

    def add(self, text, color=COLOR_TEXT):
        timestamp = time.strftime("%H:%M:%S")
        full_text = f"[{timestamp}] {text}"
        wrapped_lines = textwrap.wrap(full_text, self.width)
        for line in wrapped_lines:
            self.messages.append((line, color))
            if len(self.messages) > self.height:
                self.messages.pop(0)

    def render(self, console, x, y):
        for i, (text, color) in enumerate(self.messages):
            console.print(x, y + i, text, fg=color)

class Rect:
    def __init__(self, x, y, w, h):
        self.x1, self.y1, self.x2, self.y2 = x, y, x + w, y + h
    def center(self):
        return int((self.x1 + self.x2) / 2), int((self.y1 + self.y2) / 2)

class MatrixRain:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.drops = [0] * width
        self.last_update = time.time()

    def update(self):
        now = time.time()
        if now - self.last_update > 0.05:
            self.last_update = now
            for i in range(self.width):
                if self.drops[i] > self.height and random.random() > 0.95:
                    self.drops[i] = 0
                self.drops[i] += 1

    def render(self, console):
        for x in range(self.width):
            y = self.drops[x]
            if 0 <= y < self.height:
                char = chr(random.randint(33, 126))
                console.print(x, y, char, fg=(0, 80, 0))
                if y > 0:
                    console.print(x, y - 1, char, fg=(0, 200, 50))

def apply_crt_effect(console):
    console.rgb["bg"][:, 1::2] = (console.rgb["bg"][:, 1::2] * 0.6).astype(np.uint8)
    console.rgb["fg"][:, 1::2] = (console.rgb["fg"][:, 1::2] * 0.8).astype(np.uint8)

def apply_encounter_flash(console):
    temp_fg = np.copy(console.rgb["fg"])
    console.rgb["fg"] = console.rgb["bg"]
    console.rgb["bg"] = temp_fg

def generate_dungeon(ep_idx):
    dungeon = [[1 for _ in range(MAP_VIEW_H)] for _ in range(MAP_VIEW_W)]
    
    def carve(r):
        for x in range(r.x1, r.x2):
            for y in range(r.y1, r.y2):
                if 0 < x < MAP_VIEW_W - 1 and 0 < y < MAP_VIEW_H - 1:
                    dungeon[x][y] = 0

    if ep_idx == 0:
        carve(Rect(5, 10, 8, 5))
        carve(Rect(13, 11, 15, 3))
        carve(Rect(28, 9, 10, 7))
        enemies = [{"x": 20, "y": 12, "name": "TUTORIAL_BUG", "hp": 5}]
        return dungeon, 8, 12, 32, 12, 36, 12, enemies
    else:
        carve(Rect(5, 10, 10, 8))
        carve(Rect(14, 13, 20, 2))
        carve(Rect(25, 5, 10, 9))
        carve(Rect(34, 10, 15, 12))
        enemies = [
            {"x": 20, "y": 13, "name": "GLITCH", "hp": 10},
            {"x": 42, "y": 15, "name": "SYSTEM_ADMIN", "hp": 200},
        ]
        return dungeon, 8, 14, 29, 8, 47, 15, enemies

def render_game_ui(console, hp, max_hp, loc, log, solved):
    console.draw_rect(MAP_VIEW_W, 0, SIDEBAR_W, SCREEN_H, 0, bg=COLOR_UI_BG)
    console.draw_rect(0, MAP_VIEW_H, SCREEN_W, BOTTOM_PANEL_H, 0, bg=COLOR_UI_BG)
    
    console.draw_rect(MAP_VIEW_W, 0, 1, SCREEN_H, ord('│'), fg=COLOR_BORDER)
    console.draw_rect(0, MAP_VIEW_H, MAP_VIEW_W, 1, ord('─'), fg=COLOR_BORDER)
    console.print(MAP_VIEW_W, MAP_VIEW_H, "┤", fg=COLOR_BORDER)

    console.print(MAP_VIEW_W + 2, 2, ">> SYS_LOGS", fg=COLOR_ACCENT)
    console.print(MAP_VIEW_W + 2, 3, "────────────────", fg=COLOR_BORDER)
    log.render(console, MAP_VIEW_W + 2, 5)
    
    info_y = MAP_VIEW_H - 6
    console.print(MAP_VIEW_W + 2, info_y, "CURRENT_NODE:", fg=COLOR_TEXT_DIM)
    console.print(MAP_VIEW_W + 2, info_y + 1, loc, fg=COLOR_ACCENT)
    console.print(MAP_VIEW_W + 2, info_y + 3, "NET_STATUS:", fg=COLOR_TEXT_DIM)
    console.print(MAP_VIEW_W + 2, info_y + 4, "ONLINE [SECURE]", fg=COLOR_ACCENT, bg=(0,40,0))

    y_base = MAP_VIEW_H + 2
    console.print(3, y_base, "SYS_INTEGRITY:", fg=COLOR_TEXT_DIM)
    console.print(3, y_base + 3, f"{hp}/{max_hp}", fg=COLOR_PLAYER)
    
    bar_x, bar_w = 15, 30
    console.draw_rect(bar_x, y_base + 3, bar_w, 1, 177, fg=COLOR_HP_BG)
    fill = int(float(hp) / max_hp * bar_w)
    if fill > 0:
        col = COLOR_HP_BAR if hp > 30 else COLOR_ENEMY
        console.draw_rect(bar_x, y_base + 3, fill, 1, 219, fg=col)

    slot_x = 55
    console.print(slot_x, y_base, "ACTIVE_MODULES:", fg=COLOR_TEXT_DIM)
    for i, symbol in enumerate(["φ", "Σ", "-", "-"]):
        sx = slot_x + (i * 6)
        sy = y_base + 2
        col = COLOR_ACCENT if i == 0 else (COLOR_WARNING if i == 1 else COLOR_TEXT_DIM)
        console.draw_frame(sx, sy, 5, 3, fg=col)
        console.print(sx + 2, sy + 1, symbol, fg=col)

def render_dialog(console, text):
    w, h = 60, 15
    x, y = (SCREEN_W - w)//2, (SCREEN_H - h)//2
    console.draw_frame(x, y, w, h, title="[ INCOMING TRANSMISSION ]", fg=COLOR_PLAYER, bg=(0, 10, 10))
    console.draw_rect(x+1, y+1, w-2, h-2, 0, bg=(0, 10, 10))
    
    lines = textwrap.wrap(text, w - 4)
    for i, line in enumerate(lines):
        console.print(x + 2, y + 3 + i, line, fg=COLOR_TEXT)
        
    console.print(x + w - 20, y + h - 2, "[ENTER] CONTINUE", fg=COLOR_TEXT_DIM, bg=(0, 40, 0))

def render_battle_puzzle(console, enemy_name, puzzle, user_input):
    w, h = 60, 20
    x, y = (SCREEN_W - w)//2, (SCREEN_H - h)//2
    console.draw_frame(x, y, w, h, title="[ TARGET DETECTED ]", fg=COLOR_ENEMY, bg=(20, 0, 0))
    console.draw_rect(x+1, y+1, w-2, h-2, 0, bg=(15, 0, 0))
    
    for i, line in enumerate(GLITCH_ART):
        console.print(x + (w//2) - 8, y + 2 + i, line, fg=COLOR_ENEMY)

    py = y + 12
    console.print(x + 2, py, puzzle['puzzle_title'], fg=COLOR_ENEMY)
    
    lines = puzzle['puzzle_desc'].split('\n')
    for i, l in enumerate(lines):
        console.print(x + 2, py + 2 + i, l, fg=COLOR_TEXT)
        
    console.print(x + 2, py + 6, f"INPUT > {user_input}_", fg=COLOR_PLAYER)

def render_boss_rpg(console, boss_hp, max_boss_hp, player_hp, menu_idx):
    console.draw_rect(0, 0, SCREEN_W, SCREEN_H, 0, bg=(10, 0, 0))
    
    for i, line in enumerate(SYSTEM_ADMIN_ASCII_BATTLE):
        console.print((SCREEN_W - len(line)) // 2, 5 + i, line, fg=COLOR_ENEMY)
        
    hud_y = SCREEN_H - 18
    console.draw_rect(0, hud_y, SCREEN_W, 18, 0, bg=(5, 0, 0))
    console.draw_rect(0, hud_y, SCREEN_W, 1, ord('─'), fg=COLOR_ENEMY)
    console.draw_rect(SCREEN_W // 2, hud_y, 1, 18, ord('│'), fg=COLOR_ENEMY)
    
    console.print(5, hud_y + 3, "PLAYER_INTEGRITY", fg=COLOR_PLAYER)
    console.print(5, hud_y + 5, f"{player_hp} / 100", fg=COLOR_TEXT)
    
    console.print(5, hud_y + 9, "HOST_HP", fg=COLOR_ENEMY)
    console.print(5, hud_y + 11, f"{boss_hp} / {max_boss_hp}", fg=COLOR_ENEMY)
    
    console.print(SCREEN_W // 2 + 5, hud_y + 3, "TACTICAL_OVERRIDE", fg=COLOR_ENEMY)
    
    commands = ["1. φ Attack (15 DMG)", "2. Σ Sigma (40 DMG)", "3. Retreat"]
    for i, cmd in enumerate(commands):
        color = COLOR_PLAYER if i == menu_idx else COLOR_TEXT_DIM
        prefix = "> " if i == menu_idx else "  "
        console.print(SCREEN_W // 2 + 5, hud_y + 6 + (i*2), f"{prefix}{cmd}", fg=color)

def main():
    tileset = tcod.tileset.load_tilesheet(FONT_FILE, 32, 8, tcod.tileset.CHARMAP_TCOD)
    
    state = "POWER_ON"
    menu_idx = 0
    boss_menu_idx = 0
    ep_idx = 0
    unlocked = [0]
    
    log = MessageLog(SIDEBAR_W - 4, SCREEN_H - 22)
    game_map = []
    enemies = []
    px, py, file_x, file_y, exit_x, exit_y = 0, 0, 0, 0, 0, 0
    
    mission = MISSION_DATA[0]
    solved = False
    hp = 100
    max_hp = 100
    active_enemy = None
    battle_input = ""
    dialog_text = ""
    next_state = ""
    
    fov = None
    explored = None
    recompute = True
    
    matrix_rain = MatrixRain(SCREEN_W, SCREEN_H)
    
    power_on_timer = time.time() + 1.5
    boot_timer = 0
    boot_lines_shown = 0
    boot_lines = [
        "BIOS DATE 09/22/84 15:23:01 VER 1.02", "CPU: NEC V20, SPEED: 8 MHz", "640K RAM SYSTEM... OK", "",
        "LOADING BOOTSTRAP LOADER...", "DETECTING DRIVE A: [ NULL_TRACE DISK ]", "READING SECTOR 0...",
        "INITIALIZING KERNEL...", "SYSTEM READY.", "", "CONNECTING TO NEURAL LINK..."
    ]
    
    encounter_flash_end = 0

    flags = tcod.context.SDL_WINDOW_FULLSCREEN
    with tcod.context.new_terminal(SCREEN_W, SCREEN_H, tileset=tileset, title="NULL_TRACE v4.0", vsync=True, sdl_window_flags=flags) as context:
        console = context.new_console(order="F")
        
        while True:
            console.clear(bg=COLOR_BG)
            current_time = time.time()
            
            if state in ["MAIN_MENU", "EPISODE_SELECT", "BOOT"]:
                matrix_rain.update()
                matrix_rain.render(console)
            
            if state == "POWER_ON":
                if current_time < power_on_timer:
                    console.draw_rect(0, SCREEN_H//2, SCREEN_W, 1, 219, fg=(255, 255, 255))
                else:
                    state = "BOOT"
                    boot_timer = current_time

            elif state == "BOOT":
                console.draw_rect(0, 0, SCREEN_W, SCREEN_H, 0, bg=(0,0,0))
                if current_time - boot_timer > 0.2 and boot_lines_shown < len(boot_lines):
                    boot_lines_shown += 1
                    boot_timer = current_time
                
                for i in range(boot_lines_shown):
                    console.print(5, 5 + i, boot_lines[i], fg=COLOR_TEXT)
                
                if boot_lines_shown >= len(boot_lines) and current_time - boot_timer > 1.0:
                    state = "MAIN_MENU"

            elif state == "MAIN_MENU":
                cx, cy = SCREEN_W // 2, SCREEN_H // 2
                console.draw_rect(0, 0, SCREEN_W, SCREEN_H, 0, bg=(0,0,0), fg=(0,0,0), bg_blend=tcod.BKGND_MULTIPLY)
                console.print(cx, cy - 8, "N U L L _ T R A C E", fg=COLOR_PLAYER, alignment=tcod.CENTER)
                
                opts = ["PLAY", "LOAD GAME", "SETTINGS"]
                for i, opt in enumerate(opts):
                    col = COLOR_PLAYER if i == menu_idx else COLOR_TEXT_DIM
                    pref = "> " if i == menu_idx else "  "
                    console.print(cx - 10, cy + (i*2), f"{pref}{opt}", fg=col)

            elif state == "EPISODE_SELECT":
                console.draw_frame(SCREEN_W//2 - 20, SCREEN_H//2 - 10, 40, 20, title="[ SYSTEM SELECT ]", fg=COLOR_ACCENT, bg=(0,5,0))
                console.draw_rect(SCREEN_W//2 - 19, SCREEN_H//2 - 9, 38, 18, 0, bg=(0,5,0))
                
                for i, ep_id in enumerate(MISSION_DATA.keys()):
                    is_locked = ep_id not in unlocked
                    col = COLOR_PLAYER if i == menu_idx else (COLOR_ENEMY if is_locked else COLOR_TEXT_DIM)
                    pref = "> " if i == menu_idx else "  "
                    title = MISSION_DATA[ep_id]['title']
                    status = "[LOCKED]" if is_locked else "[UNLOCKED]"
                    console.print(SCREEN_W//2 - 15, SCREEN_H//2 - 5 + (i*2), f"{pref}{title} {status}", fg=col)

            elif state == "DIALOG":
                render_game_ui(console, hp, max_hp, mission['loc_name'], log, solved)
                render_dialog(console, dialog_text)

            elif state == "GAMEPLAY":
                if recompute:
                    trans = np.array(game_map) == 0
                    fov = tcod.map.compute_fov(trans, (px, py), radius=12, algorithm=tcod.FOV_BASIC)
                    explored |= fov
                    recompute = False
                
                for x in range(MAP_VIEW_W):
                    for y in range(MAP_VIEW_H):
                        if fov[x,y]:
                            char, col = (".", COLOR_FLOOR) if game_map[x][y] == 0 else ("#", COLOR_WALL)
                            console.print(x, y, char, fg=col)
                        elif explored[x,y]:
                            char, col = (".", COLOR_FLOOR_DARK) if game_map[x][y] == 0 else ("#", COLOR_WALL_DARK)
                            console.print(x, y, char, fg=col)

                if explored[file_x, file_y] and not solved:
                    console.print(file_x, file_y, "💾", fg=COLOR_WARNING)
                
                if explored[exit_x, exit_y]:
                    col = COLOR_ACCENT if solved else COLOR_ENEMY
                    char = ">" if solved else "X"
                    console.print(exit_x, exit_y, char, fg=col)

                for e in enemies:
                    if fov[e['x'], e['y']]:
                        char = "M" if e['name'] == "SYSTEM_ADMIN" else "E"
                        col = COLOR_BOSS if e['name'] == "SYSTEM_ADMIN" else COLOR_ENEMY
                        console.print(e['x'], e['y'], char, fg=col)

                console.print(px, py, "@", fg=COLOR_PLAYER)
                render_game_ui(console, hp, max_hp, mission['loc_name'], log, solved)

            elif state == "BATTLE":
                if active_enemy['name'] == "SYSTEM_ADMIN":
                    state = "BATTLE_BOSS"
                else:
                    render_game_ui(console, hp, max_hp, mission['loc_name'], log, solved)
                    puz = ENEMY_PUZZLES.get(active_enemy['name'], ENEMY_PUZZLES['GLITCH'])
                    render_battle_puzzle(console, active_enemy['name'], puz, battle_input)

            elif state == "BATTLE_BOSS":
                render_boss_rpg(console, active_enemy['hp'], ENEMY_PUZZLES['SYSTEM_ADMIN']['max_hp'], hp, boss_menu_idx)

            if current_time < encounter_flash_end:
                apply_encounter_flash(console)
            
            apply_crt_effect(console)
            context.present(console, keep_aspect=True, integer_scaling=False)
            
            for event in tcod.event.get():
                context.convert_event(event)
                
                if event.type == "QUIT":
                    raise SystemExit()
                
                elif event.type == "KEYDOWN":
                    sym = event.sym
                    
                    if sym == tcod.event.K_ESCAPE:
                        if state in ["GAMEPLAY", "BATTLE", "BATTLE_BOSS", "EPISODE_SELECT", "DIALOG"]:
                            state = "MAIN_MENU"
                            menu_idx = 0
                        else:
                            raise SystemExit()
                            
                    elif state == "MAIN_MENU":
                        if sym == tcod.event.K_UP: menu_idx = (menu_idx - 1) % 3
                        elif sym == tcod.event.K_DOWN: menu_idx = (menu_idx + 1) % 3
                        elif sym == tcod.event.K_RETURN:
                            if menu_idx == 0:
                                state = "EPISODE_SELECT"
                                menu_idx = 0
                            else:
                                dialog_text = "Peringatan: Modul belum dapat diakses pada versi DEMO."
                                next_state = "MAIN_MENU"
                                state = "DIALOG"
                                
                    elif state == "EPISODE_SELECT":
                        if sym == tcod.event.K_UP: menu_idx = (menu_idx - 1) % len(MISSION_DATA)
                        elif sym == tcod.event.K_DOWN: menu_idx = (menu_idx + 1) % len(MISSION_DATA)
                        elif sym == tcod.event.K_RETURN:
                            if menu_idx in unlocked:
                                ep_idx = menu_idx
                                mission = MISSION_DATA[ep_idx]
                                game_map, px, py, file_x, file_y, exit_x, exit_y, enemies = generate_dungeon(ep_idx)
                                explored = np.zeros((MAP_VIEW_W, MAP_VIEW_H), dtype=bool, order="F")
                                hp = 100
                                solved = False
                                log.messages.clear()
                                dialog_text = mission['start_dialog']
                                next_state = "GAMEPLAY"
                                state = "DIALOG"
                            
                    elif state == "DIALOG":
                        if sym == tcod.event.K_RETURN:
                            state = next_state
                            if state == "GAMEPLAY" and len(log.messages) == 0:
                                log.add("SYSTEM READY.", COLOR_ACCENT)
                            elif state == "MAIN_MENU":
                                hp = max_hp

                    elif state == "GAMEPLAY":
                        dx, dy = 0, 0
                        if sym in (tcod.event.K_UP, tcod.event.K_w): dy = -1
                        elif sym in (tcod.event.K_DOWN, tcod.event.K_s): dy = 1
                        elif sym in (tcod.event.K_LEFT, tcod.event.K_a): dx = -1
                        elif sym in (tcod.event.K_RIGHT, tcod.event.K_d): dx = 1
                        
                        elif sym == tcod.event.K_e:
                            if abs(px - file_x) <= 1 and abs(py - file_y) <= 1 and not solved:
                                solved = True
                                dialog_text = mission['end_dialog']
                                next_state = "GAMEPLAY"
                                state = "DIALOG"
                            elif abs(px - exit_x) <= 1 and abs(py - exit_y) <= 1:
                                if solved:
                                    dialog_text = "NODE CLEARED.\n\nMemutuskan koneksi aman..."
                                    next_state = "MAIN_MENU"
                                    state = "DIALOG"
                                    if ep_idx + 1 not in unlocked and ep_idx + 1 in MISSION_DATA:
                                        unlocked.append(ep_idx + 1)
                                else:
                                    log.add("DENIED: Retas file data (💾) dahulu.", COLOR_ENEMY)

                        if dx != 0 or dy != 0:
                            nx, ny = px + dx, py + dy
                            if 0 <= nx < MAP_VIEW_W and 0 <= ny < MAP_VIEW_H:
                                if game_map[nx][ny] == 0:
                                    hit = next((e for e in enemies if e['x'] == nx and e['y'] == ny), None)
                                    if hit:
                                        active_enemy = hit
                                        battle_input = ""
                                        boss_menu_idx = 0
                                        log.add(f"THREAT DETECTED: {hit['name']}", COLOR_WARNING)
                                        state = "BATTLE"
                                        encounter_flash_end = time.time() + 0.3 
                                    else:
                                        px, py = nx, ny
                                        recompute = True
                                        if abs(px - file_x) <= 1 and abs(py - file_y) <= 1 and not solved:
                                            log.add("Target File Found. Press 'E'.", COLOR_ACCENT)

                                        for e in enemies:
                                            if e['name'] == "SYSTEM_ADMIN":
                                                continue
                                            edx, edy = random.choice([(0,1), (0,-1), (1,0), (-1,0), (0,0)])
                                            if edx != 0 or edy != 0:
                                                enx, eny = e['x'] + edx, e['y'] + edy
                                                if 0 <= enx < MAP_VIEW_W and 0 <= eny < MAP_VIEW_H and game_map[enx][eny] == 0:
                                                    if enx == px and eny == py:
                                                        active_enemy = e
                                                        battle_input = ""
                                                        boss_menu_idx = 0
                                                        log.add(f"THREAT DETECTED: {e['name']}", COLOR_WARNING)
                                                        state = "BATTLE"
                                                        encounter_flash_end = time.time() + 0.3
                                                        break
                                                    elif not any(o['x'] == enx and o['y'] == eny for o in enemies):
                                                        e['x'], e['y'] = enx, eny

                    elif state == "BATTLE":
                        puz = ENEMY_PUZZLES.get(active_enemy['name'], ENEMY_PUZZLES['GLITCH'])
                        if sym == tcod.event.K_RETURN:
                            if battle_input == puz['puzzle_solution']:
                                log.add(f"{active_enemy['name']} DEFEATED.", COLOR_ACCENT)
                                enemies.remove(active_enemy)
                                state = "GAMEPLAY"
                                recompute = True
                            else:
                                dmg = puz['dmg']
                                hp -= dmg
                                log.add(f"ERROR: INTEGRITY LOST (-{dmg})", COLOR_ENEMY)
                                if hp <= 0:
                                    dialog_text = "CRITICAL ERROR.\nSYSTEM INTEGRITY AT 0%.\n\n[ CONNECTION TERMINATED ]"
                                    next_state = "MAIN_MENU"
                                    state = "DIALOG"
                            battle_input = ""
                        elif sym == tcod.event.K_BACKSPACE:
                            battle_input = battle_input[:-1]
                        elif 32 <= sym <= 126:
                            char = chr(sym)
                            shift = event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT)
                            if 'a' <= char <= 'z' and shift: char = char.upper()
                            elif char == '=' and shift: char = '+'
                            elif char == '-' and shift: char = '_'
                            elif char == "'" and shift: char = '"'
                            battle_input += char
                            
                    elif state == "BATTLE_BOSS":
                        if sym == tcod.event.K_UP: boss_menu_idx = (boss_menu_idx - 1) % 3
                        elif sym == tcod.event.K_DOWN: boss_menu_idx = (boss_menu_idx + 1) % 3
                        elif sym == tcod.event.K_RETURN:
                            boss_puz = ENEMY_PUZZLES['SYSTEM_ADMIN']
                            if boss_menu_idx == 0:
                                active_enemy['hp'] -= 15
                                log.add("SYS_DMG: -15 HOST", COLOR_PLAYER)
                            elif boss_menu_idx == 1:
                                active_enemy['hp'] -= 40
                                log.add("SIGMA_DMG: -40 HOST", COLOR_WARNING)
                            elif boss_menu_idx == 2:
                                state = "GAMEPLAY"
                                log.add("Retreating...", COLOR_TEXT_DIM)
                                recompute = True
                                continue
                            
                            if active_enemy['hp'] <= 0:
                                log.add("SYSTEM_ADMIN DELETED.", COLOR_ACCENT)
                                enemies.remove(active_enemy)
                                state = "GAMEPLAY"
                                recompute = True
                            else:
                                dmg = boss_puz['dmg']
                                hp -= dmg
                                log.add(f"ERROR: INTEGRITY LOST (-{dmg})", COLOR_ENEMY)
                                encounter_flash_end = time.time() + 0.1
                                if hp <= 0:
                                    dialog_text = "CRITICAL ERROR.\nSYSTEM INTEGRITY AT 0%.\n\n[ CONNECTION TERMINATED ]"
                                    next_state = "MAIN_MENU"
                                    state = "DIALOG"

if __name__ == "__main__":
    main()