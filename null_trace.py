import random
import numpy as np
import tcod
import time
import textwrap
import sys

FONT_FILE = "dejavu10x10_gs_tc.png"

COLOR_BG = (20, 25, 35)
COLOR_UI_BG = (30, 40, 50)
COLOR_BORDER = (0, 220, 100)
COLOR_BORDER_ACTIVE = (50, 255, 150)
COLOR_TEXT = (255, 255, 255)
COLOR_TEXT_DIM = (160, 190, 160)
COLOR_WALL = (50, 75, 85)
COLOR_WALL_DARK = (30, 45, 55)
COLOR_FLOOR = (35, 50, 60)
COLOR_FLOOR_DARK = (20, 30, 40)
COLOR_PLAYER = (0, 255, 255)
COLOR_ENEMY = (255, 80, 80)
COLOR_BOSS = (255, 80, 255)
COLOR_ACCENT = (50, 255, 150)
COLOR_WARNING = (255, 200, 50)
COLOR_HP_BAR = (0, 255, 255)
COLOR_HP_BG = (0, 80, 80)

SCREEN_W = 95
SCREEN_H = 55
SIDEBAR_W = 30
BOTTOM_PANEL_H = 13
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

AVATAR_ART = [
    r"    _____    ",
    r"   /     \   ",
    r"  | >   < |  ",
    r"  |  ---  |  ",
    r"   \ ___ /   ",
    r"   / /_\ \   ",
    r"  | |   | |  "
]

MISSION_DATA = {
    0: {
        "title": "EPISODE 0: AWAKENING",
        "loc_name": "SYS/BOOT_SECTOR",
        "start_dialog": [
            ("[ COMMANDER INTEGER ]", "Tracer, apakah kamu bisa mendengar suara saya? Koneksi neural terlihat sedikit tidak stabil dari monitor markas."),
            ("[ TRACER ]", "Suara Anda terdengar jelas, Commander. Sistem visual saya baru saja online. Di mana saya sekarang?"),
            ("[ COMMANDER INTEGER ]", "Bagus. Anda berada di sektor perimeter luar. Dengarkan baik-baik, misi ini sangat krusial.\n\nTAHUN 2084. Beberapa infrastruktur dikendalikan oleh superkomputer bernama The Core."),
            ("[ COMMANDER INTEGER ]", "Cerita dimulai ketika mentor dari Unit Rahasia, Elias Thorne, menghilang misterius saat menyelidiki anomali di server pemerintah. Elias meninggalkan jejak digital yang terenkripsi dan rusak."),
            ("[ COMMANDER INTEGER ]", "Anda adalah Tracer, anggota baru unit tersebut. Tugas Anda menelusuri jejak tersebut, menembus lapisan keamanan bervirus, dan mengungkap konspirasi besar di balik hilangnya Elias."),
            ("[ SYSTEM ]", "[ PROTOKOL DASAR ]\n> Navigasi : W, A, S, D atau Panah.\n> Interaksi: Tekan 'E' untuk meretas Data ( f ).\n> Objektif : Bersihkan area dan capai terminal keluar ( > ).\n\nSemoga berhasil, Tracer.")
        ],
        "end_dialog": [
            ("[ TRACER ]", "Commander, saya telah menemukan fragmen datanya. Enkripsi berhasil ditembus."),
            ("[ COMMANDER INTEGER ]", "Kerja bagus. CALIBRATION COMPLETE.\n\n[LOG_TXT]: 'Sistem stabil. Memulai proses intrusi ke gateway utama untuk mencari jejak Elias.'\n\nSegera menuju sektor berikutnya.")
        ],
    },
    1: {
        "title": "EPISODE 1: INTRUSION",
        "loc_name": "SYS/GATEWAY_01",
        "start_dialog": [
            ("[ COMMANDER INTEGER ]", "MEMASUKI GATEWAY_01...\n\nSistem keamanan aktif. Jejak pertama Elias Thorne terdeteksi di sektor ini."),
            ("[ COMMANDER INTEGER ]", "[ OBJEKTIF UTAMA ]\n> Ekstrak File Data ( f ).\n> Hancurkan entitas penjaga.\n> Lakukan ekstraksi melalui pintu keluar ( > ).")
        ],
        "end_dialog": [
            ("[ TRACER ]", "DATA ACQUIRED.\n\nMemecahkan enkripsi file... Tunggu, ada anomali lain yang mendekat!"),
            ("[ COMMANDER INTEGER ]", "[LOG_TXT]: 'Protokol Admin telah diaktifkan. Akses keluar dikunci.'\n\nWARNING: Tracer, kalahkan SYSTEM_ADMIN untuk membatalkan pemblokiran.")
        ],
    },
    2: {
        "title": "EPISODE 2: EXPLOIT & INJECTION",
        "loc_name": "SYS/DATA_VAULT",
        "start_dialog": [
            ("[ COMMANDER INTEGER ]", "Tracer, perhatikan! Setelah kamu menembus Gateway, sensor markas mendeteksi lalu lintas data yang sangat masif dari dalam server."),
            ("[ TRACER ]", "Maksud Anda, ada pihak lain di dalam jaringan ini?"),
            ("[ COMMANDER INTEGER ]", "Benar. Ada peretas yang sedang menyedot blueprint senjata rahasia pemerintah melalui 'Backdoor'. Ini adalah DATA BREACH (Kebocoran Data) tingkat tinggi."),
            ("[ COMMANDER INTEGER ]", "Cari file blueprint ( f ) yang tersisa sebelum peretas menghapusnya, dan berhati-hatilah dengan 'Worm' yang mereka tanam untuk merusak log sistem kita.")
        ],
        "end_dialog": [
            ("[ TRACER ]", "File Blueprint berhasil diamankan, Commander. Namun struktur kode di dalamnya memuat tanda tangan digital milik Elias..."),
            ("[ COMMANDER INTEGER ]", "Apa?! Elias... mencuri senjata pemerintah? Tidak, kita tidak bisa langsung mengambil kesimpulan. Selesaikan pertarunganmu dan cepat menuju titik ekstraksi!")
        ],
    }
}

ENEMY_PUZZLES = {
    "TUTORIAL_BUG": {
        "puzzle_title": "[ SYNTAX ERROR ]",
        "puzzle_desc": "Kesalahan format string terdeteksi.\nCODE: x = Hello\nTASK: Tambahkan karakter yang tepat agar Hello menjadi string.",
        "puzzle_solution": "'Hello'",
        "dmg": 5,
    },
    "GLITCH": {
        "puzzle_title": "[ MEMORY LEAK ]",
        "puzzle_desc": "Hentikan eksekusi kode berulang.\nCODE: print('Error')\nTASK: Ketik keyword Python untuk melewati blok ini secara aman.",
        "puzzle_solution": "pass",
        "dmg": 10,
    },
    "SQL_WORM": {
        "puzzle_title": "[ INJECTION VULNERABILITY ]",
        "puzzle_desc": "Spasi berlebih pada input dapat dieksploitasi untuk membongkar database.\nCODE: user_input = '  admin  '\nTASK: Ketik nama fungsi bawaan Python (beserta kurungnya) untuk memotong spasi kosong di awal dan akhir input string.",
        "puzzle_solution": "strip()",
        "dmg": 15,
    }
}

BOSS_PUZZLES_STANDARD = [
    {
        "puzzle_title": "[ FIREWALL BREACH: TYPE ERROR ]",
        "puzzle_desc": "Tipe data tidak valid terdeteksi.\nCODE: y = '5' + 5\nTASK: Tulis sintaks untuk konversi string '5' ke integer.",
        "puzzle_solution": "int('5')"
    },
    {
        "puzzle_title": "[ FIREWALL BREACH: LOGIC GATE ]",
        "puzzle_desc": "Selesaikan kondisi gerbang logika ini.\nCODE: True and False\nTASK: Ketik hasil boolean dari ekspresi di atas.",
        "puzzle_solution": "False"
    },
    {
        "puzzle_title": "[ FIREWALL BREACH: ENCRYPTION KEY ]",
        "puzzle_desc": "Sistem meminta jumlah elemen dari array.\nCODE: arr = [1, 2, 3]\nTASK: Gunakan fungsi bawaan Python untuk mendapatkan panjang array.",
        "puzzle_solution": "len(arr)"
    },
    {
        "puzzle_title": "[ FIREWALL BREACH: OVERRIDE PROTOCOL ]",
        "puzzle_desc": "Perbaiki fungsi otorisasi agar berhasil.\nCODE: def cek_akses():\nTASK: Ketik sintaks untuk mengembalikan nilai kebenaran absolut (True).",
        "puzzle_solution": "return True"
    },
    {
        "puzzle_title": "[ FIREWALL BREACH: VALUE FINDER ]",
        "puzzle_desc": "Sistem meminta nilai puncak dalam sektor data.\nCODE: arr = [1, 5, 2]\nTASK: Gunakan fungsi bawaan Python untuk mencari angka tertinggi dari array arr.",
        "puzzle_solution": "max(arr)"
    }
]

BOSS_PUZZLES_SIGMA = [
    {
        "puzzle_title": "[ SIGMA PROTOCOL: STRING MUTATION ]",
        "puzzle_desc": "Sistem mendeteksi format huruf yang mencurigakan.\nCODE: x = 'ADMIN'\nTASK: Tulis sintaks untuk mengubah semua karakter pada variabel x menjadi huruf kecil (lowercase).",
        "puzzle_solution": "x.lower()"
    },
    {
        "puzzle_title": "[ SIGMA PROTOCOL: ARRAY TRUNCATION ]",
        "puzzle_desc": "Terdapat anomali di akhir antrean memori.\nCODE: arr = [1, 2, 'malware']\nTASK: Tulis fungsi bawaan array/list untuk menghapus elemen terakhir tanpa menyebutkan indeksnya.",
        "puzzle_solution": "arr.pop()"
    },
    {
        "puzzle_title": "[ SIGMA PROTOCOL: KERNEL PATCHING ]",
        "puzzle_desc": "Sistem menemukan cacat program di dalam string.\nCODE: s = 'ada bug'\nTASK: Tulis sintaks (fungsi replace) untuk mengganti kata 'bug' menjadi 'fix' pada variabel s.",
        "puzzle_solution": "s.replace('bug', 'fix')"
    },
    {
        "puzzle_title": "[ SIGMA PROTOCOL: CONCATENATION ]",
        "puzzle_desc": "Protokol keamanan terpecah menjadi beberapa bagian list.\nCODE: parts = ['A', 'B']\nTASK: Tulis sintaks untuk menggabungkan elemen list tersebut menjadi satu string utuh tanpa spasi pemisah.",
        "puzzle_solution": "''.join(['A', 'B'])"
    },
    {
        "puzzle_title": "[ SIGMA PROTOCOL: DATA INJECTION ]",
        "puzzle_desc": "Sistem meminta penambahan node darurat di ujung array.\nCODE: arr = [1, 2]\nTASK: Tulis sintaks untuk menambahkan elemen string 'X' ke bagian paling akhir dari list arr.",
        "puzzle_solution": "arr.append('X')"
    }
]

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
                console.print(x, y, char, fg=(0, 150, 50))
                if y > 0:
                    console.print(x, y - 1, char, fg=(0, 255, 100))

def apply_crt_effect(console):
    console.rgb["bg"][:, 1::2] = (console.rgb["bg"][:, 1::2] * 0.85).astype(np.uint8)
    console.rgb["fg"][:, 1::2] = (console.rgb["fg"][:, 1::2] * 0.90).astype(np.uint8)

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
    elif ep_idx == 1:
        carve(Rect(5, 10, 10, 8))
        carve(Rect(14, 13, 20, 2))
        carve(Rect(25, 5, 10, 9))
        carve(Rect(34, 10, 15, 12))
        enemies = [
            {"x": 20, "y": 13, "name": "GLITCH", "hp": 10},
            {"x": 42, "y": 15, "name": "SYSTEM_ADMIN", "hp": 200},
        ]
        return dungeon, 8, 14, 29, 8, 47, 15, enemies
    elif ep_idx == 2:
        carve(Rect(5, 5, 12, 12))
        carve(Rect(17, 9, 15, 3))
        carve(Rect(32, 5, 15, 12))
        carve(Rect(47, 9, 10, 3))
        carve(Rect(57, 5, 10, 10))
        enemies = [
            {"x": 25, "y": 10, "name": "SQL_WORM", "hp": 15},
            {"x": 40, "y": 8, "name": "GLITCH", "hp": 10},
            {"x": 62, "y": 10, "name": "SYSTEM_ADMIN", "hp": 200},
        ]
        return dungeon, 10, 10, 38, 14, 63, 10, enemies

def render_gameplay_map(console, game_map, fov, explored, px, py, file_x, file_y, exit_x, exit_y, enemies, solved):
    for x in range(MAP_VIEW_W):
        for y in range(MAP_VIEW_H):
            if fov[x,y]:
                char, col = (".", COLOR_FLOOR) if game_map[x][y] == 0 else ("#", COLOR_WALL)
                console.print(x, y, char, fg=col)
            elif explored[x,y]:
                char, col = (".", COLOR_FLOOR_DARK) if game_map[x][y] == 0 else ("#", COLOR_WALL_DARK)
                console.print(x, y, char, fg=col)

    if explored[file_x, file_y] and not solved:
        console.print(file_x, file_y, "f", fg=COLOR_WARNING)
    
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
    
    bar_x, bar_w = 15, 25
    console.draw_rect(bar_x, y_base + 3, bar_w, 1, 177, fg=COLOR_HP_BG)
    fill = int(float(hp) / max_hp * bar_w)
    if fill > 0:
        col = COLOR_HP_BAR if hp > 30 else COLOR_ENEMY
        console.draw_rect(bar_x, y_base + 3, fill, 1, 219, fg=col)

    slot_x = 45
    console.print(slot_x, y_base, "ACTIVE_MODULES:", fg=COLOR_TEXT_DIM)
    for i, symbol in enumerate(["φ", "Σ", "-", "-"]):
        sx = slot_x + (i * 6)
        sy = y_base + 2
        col = COLOR_ACCENT if i == 0 else (COLOR_WARNING if i == 1 else COLOR_TEXT_DIM)
        console.draw_frame(sx, sy, 5, 3, fg=col)
        console.print(sx + 2, sy + 1, symbol, fg=col)

def render_dialog(console, text, title):
    w, h = 88, 26
    x, y = (SCREEN_W - w)//2, (SCREEN_H - h)//2
    console.draw_frame(x, y, w, h, title=title, fg=COLOR_PLAYER, bg=(10, 20, 30))
    console.draw_rect(x+1, y+1, w-2, h-2, 0, bg=(10, 20, 30))
    
    for i, line in enumerate(AVATAR_ART):
        console.print(x + 3, y + 4 + i, line, fg=COLOR_PLAYER)
        
    console.draw_rect(x + 20, y + 2, 1, h - 4, ord('│'), fg=COLOR_BORDER)
    
    draw_y = y + 3
    lines = text.split('\n')
    for l in lines:
        if l == "":
            draw_y += 1
            continue
        wrapped = textwrap.wrap(l, w - 24)
        for wl in wrapped:
            console.print(x + 23, draw_y, wl, fg=COLOR_TEXT)
            draw_y += 1
        
    console.print(x + w - 22, y + h - 3, "[ENTER] CONTINUE", fg=COLOR_TEXT_DIM, bg=(0, 40, 0))

def render_popup(console, text, title, is_success=False):
    w, h = 60, 14
    x, y = (SCREEN_W - w)//2, (SCREEN_H - h)//2
    
    frame_color = COLOR_ACCENT if is_success else COLOR_ENEMY
    bg_color = (5, 15, 5) if is_success else (20, 5, 5)
    inner_bg = (0, 10, 0) if is_success else (10, 0, 0)
    
    console.draw_frame(x, y, w, h, title=title, fg=frame_color, bg=bg_color)
    console.draw_rect(x+1, y+1, w-2, h-2, 0, bg=inner_bg)
    
    draw_y = y + 3
    lines = text.split('\n')
    for l in lines:
        if l == "":
            draw_y += 1
            continue
        wrapped = textwrap.wrap(l, w - 6)
        for wl in wrapped:
            console.print(x + 3, draw_y, wl, fg=COLOR_TEXT)
            draw_y += 1
        
    console.print(x + w - 22, y + h - 2, "[ENTER] CONTINUE", fg=COLOR_TEXT_DIM)

def render_battle_puzzle(console, enemy_name, puzzle, user_input, is_boss_attack=False):
    w, h = 84, 25
    x = (SCREEN_W - w)//2
    y = (SCREEN_H - h)//2
    
    if is_boss_attack:
        y -= 4

    title = "[ EXECUTING TACTICAL OVERRIDE ]" if is_boss_attack else "[ TARGET DETECTED ]"
    bg_col = (40, 10, 10) if is_boss_attack else (40, 5, 5)
    
    console.draw_frame(x, y, w, h, title=title, fg=COLOR_ENEMY, bg=bg_col)
    console.draw_rect(x+1, y+1, w-2, h-2, 0, bg=(30, 0, 0))
    
    if not is_boss_attack:
        for i, line in enumerate(GLITCH_ART):
            console.print(x + (w//2) - 8, y + 2 + i, line, fg=COLOR_ENEMY)
        py = y + 13
    else:
        console.print(x + 3, y + 3, "Sistem Pertahanan mendeteksi serangan Anda.", fg=COLOR_WARNING)
        console.print(x + 3, y + 5, "Selesaikan tantangan Firewall berikut agar serangan (-DMG) berhasil.", fg=COLOR_TEXT)
        py = y + 8

    console.print(x + 3, py, puzzle['puzzle_title'], fg=COLOR_ENEMY)
    
    draw_y = py + 2
    lines = puzzle['puzzle_desc'].split('\n')
    for l in lines:
        wrapped = textwrap.wrap(l, w - 6)
        for wl in wrapped:
            console.print(x + 3, draw_y, wl, fg=COLOR_TEXT)
            draw_y += 1
        
    console.print(x + 3, draw_y + 2, f"INPUT > {user_input}_", fg=COLOR_PLAYER)

def render_boss_rpg(console, boss_hp, max_boss_hp, player_hp, menu_idx):
    boss_hp = max(0, boss_hp)
    player_hp = max(0, player_hp)
    
    console.draw_rect(0, 0, SCREEN_W, SCREEN_H, 0, bg=(20, 10, 10))
    
    for i, line in enumerate(SYSTEM_ADMIN_ASCII_BATTLE):
        console.print((SCREEN_W - len(line)) // 2, 3 + i, line, fg=COLOR_ENEMY)
        
    hud_y = SCREEN_H - 16
    console.draw_rect(0, hud_y, SCREEN_W, 16, 0, bg=(30, 20, 30))
    console.draw_rect(0, hud_y, SCREEN_W, 1, ord('─'), fg=COLOR_ENEMY)
    console.draw_rect(SCREEN_W // 2, hud_y, 1, 16, ord('│'), fg=COLOR_ENEMY)
    
    console.print(5, hud_y + 3, "PLAYER_INTEGRITY", fg=COLOR_PLAYER)
    console.print(5, hud_y + 5, f"{player_hp} / 100", fg=COLOR_TEXT)
    
    console.print(5, hud_y + 9, "HOST_HP", fg=COLOR_ENEMY)
    console.print(5, hud_y + 11, f"{boss_hp} / {max_boss_hp}", fg=COLOR_ENEMY)
    
    console.print(SCREEN_W // 2 + 5, hud_y + 3, "TACTICAL_OVERRIDE (Select Attack)", fg=COLOR_ENEMY)
    
    commands = ["1. φ Standard Override (15 DMG)", "2. Σ Sigma Protocol (40 DMG)", "3. Disconnect (Retreat)"]
    for i, cmd in enumerate(commands):
        color = COLOR_PLAYER if i == menu_idx else COLOR_TEXT_DIM
        prefix = "> " if i == menu_idx else "  "
        console.print(SCREEN_W // 2 + 5, hud_y + 6 + (i*3), f"{prefix}{cmd}", fg=color)

def main():
    tileset = tcod.tileset.load_tilesheet(FONT_FILE, 32, 8, tcod.tileset.CHARMAP_TCOD)
    
    state = "POWER_ON"
    menu_idx = 0
    settings_menu_idx = 0
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
    dialog_title = ""
    dialog_text = ""
    dialog_queue = []
    next_state = ""
    
    pending_damage = 0
    current_boss_puzzle = None
    popup_success = False
    last_battle_type = "NORMAL"

    fov = None
    explored = None
    recompute = True
    last_enemy_move = time.time()
    
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
    is_fullscreen = False

    while True:
        flags = tcod.context.SDL_WINDOW_FULLSCREEN if is_fullscreen else tcod.context.SDL_WINDOW_RESIZABLE
        
        with tcod.context.new_terminal(SCREEN_W, SCREEN_H, tileset=tileset, title="NULL_TRACE v6.0", vsync=True, sdl_window_flags=flags) as context:
            console = context.new_console(order="F")
            recompute_context = False
            
            while True:
                console.clear(bg=COLOR_BG)
                current_time = time.time()
                
                if state in ["MAIN_MENU", "EPISODE_SELECT", "SETTINGS", "BOOT"]:
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

                elif state == "SETTINGS":
                    cx, cy = SCREEN_W // 2, SCREEN_H // 2
                    console.draw_rect(0, 0, SCREEN_W, SCREEN_H, 0, bg=(0,0,0), fg=(0,0,0), bg_blend=tcod.BKGND_MULTIPLY)
                    console.print(cx, cy - 8, "[ SYSTEM SETTINGS ]", fg=COLOR_ACCENT, alignment=tcod.CENTER)
                    
                    fs_text = "ON" if is_fullscreen else "OFF"
                    opts = [f"FULLSCREEN: {fs_text}", "BACK"]
                    for i, opt in enumerate(opts):
                        col = COLOR_PLAYER if i == settings_menu_idx else COLOR_TEXT_DIM
                        pref = "> " if i == settings_menu_idx else "  "
                        console.print(cx - 12, cy + (i*2), f"{pref}{opt}", fg=col)

                elif state == "EPISODE_SELECT":
                    console.draw_frame(SCREEN_W//2 - 25, SCREEN_H//2 - 10, 50, 20, title="[ SYSTEM SELECT ]", fg=COLOR_ACCENT, bg=(10, 20, 10))
                    console.draw_rect(SCREEN_W//2 - 24, SCREEN_H//2 - 9, 48, 18, 0, bg=(10, 20, 10))
                    
                    for i, ep_id in enumerate(MISSION_DATA.keys()):
                        is_locked = ep_id not in unlocked
                        col = COLOR_PLAYER if i == menu_idx else (COLOR_ENEMY if is_locked else COLOR_TEXT_DIM)
                        pref = "> " if i == menu_idx else "  "
                        title = MISSION_DATA[ep_id]['title']
                        status = "[LOCKED]" if is_locked else "[UNLOCKED]"
                        console.print(SCREEN_W//2 - 20, SCREEN_H//2 - 5 + (i*2), f"{pref}{title} {status}", fg=col)

                elif state == "DIALOG":
                    if fov is not None and explored is not None:
                        render_gameplay_map(console, game_map, fov, explored, px, py, file_x, file_y, exit_x, exit_y, enemies, solved)
                        render_game_ui(console, hp, max_hp, mission['loc_name'], log, solved)
                    render_dialog(console, dialog_text, dialog_title)
                    
                elif state == "POPUP":
                    if last_battle_type == "BOSS":
                        boss_hp = active_enemy['hp'] if active_enemy else 0
                        render_boss_rpg(console, boss_hp, 200, hp, boss_menu_idx)
                    else:
                        if fov is not None and explored is not None:
                            render_gameplay_map(console, game_map, fov, explored, px, py, file_x, file_y, exit_x, exit_y, enemies, solved)
                            render_game_ui(console, hp, max_hp, mission['loc_name'], log, solved)
                        
                    render_popup(console, dialog_text, dialog_title, is_success=popup_success)

                elif state == "GAMEPLAY":
                    
                    if current_time - last_enemy_move > 0.1:
                        last_enemy_move = current_time
                        enemy_moved = False
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
                                        enemy_moved = True
                        if enemy_moved:
                            recompute = True
                    
                    if recompute:
                        trans = np.array(game_map) == 0
                        fov = tcod.map.compute_fov(trans, (px, py), radius=12, algorithm=tcod.FOV_BASIC)
                        explored |= fov
                        recompute = False
                    
                    render_gameplay_map(console, game_map, fov, explored, px, py, file_x, file_y, exit_x, exit_y, enemies, solved)
                    render_game_ui(console, hp, max_hp, mission['loc_name'], log, solved)

                elif state == "BATTLE":
                    render_gameplay_map(console, game_map, fov, explored, px, py, file_x, file_y, exit_x, exit_y, enemies, solved)
                    render_game_ui(console, hp, max_hp, mission['loc_name'], log, solved)
                    puz = ENEMY_PUZZLES.get(active_enemy['name'], ENEMY_PUZZLES['GLITCH'])
                    render_battle_puzzle(console, active_enemy['name'], puz, battle_input, is_boss_attack=False)

                elif state == "BATTLE_BOSS":
                    render_boss_rpg(console, active_enemy['hp'], 200, hp, boss_menu_idx)

                elif state == "BATTLE_BOSS_PUZZLE":
                    render_boss_rpg(console, active_enemy['hp'], 200, hp, boss_menu_idx)
                    render_battle_puzzle(console, "SYSTEM_ADMIN", current_boss_puzzle, battle_input, is_boss_attack=True)

                if current_time < encounter_flash_end:
                    apply_encounter_flash(console)
                
                apply_crt_effect(console)
                context.present(console, keep_aspect=True, integer_scaling=False)
                
                for event in tcod.event.get():
                    context.convert_event(event)
                    
                    if event.type == "QUIT":
                        sys.exit()
                    
                    elif event.type == "TEXTINPUT" and state in ["BATTLE", "BATTLE_BOSS_PUZZLE"]:
                        battle_input += event.text
                    
                    elif event.type == "KEYDOWN":
                        sym = event.sym
                        
                        if sym == tcod.event.K_ESCAPE:
                            if state in ["GAMEPLAY", "BATTLE", "BATTLE_BOSS", "BATTLE_BOSS_PUZZLE", "EPISODE_SELECT", "DIALOG", "POPUP"]:
                                state = "MAIN_MENU"
                                menu_idx = 0
                                active_enemy = None
                            elif state == "SETTINGS":
                                state = "MAIN_MENU"
                                menu_idx = 2
                            else:
                                sys.exit()
                                
                        elif state == "MAIN_MENU":
                            if sym == tcod.event.K_UP: menu_idx = (menu_idx - 1) % 3
                            elif sym == tcod.event.K_DOWN: menu_idx = (menu_idx + 1) % 3
                            elif sym == tcod.event.K_RETURN:
                                if menu_idx == 0:
                                    state = "EPISODE_SELECT"
                                    menu_idx = 0
                                elif menu_idx == 1:
                                    dialog_title = "[ SYSTEM ]"
                                    dialog_text = "Peringatan: Modul belum dapat diakses pada versi DEMO."
                                    next_state = "MAIN_MENU"
                                    state = "DIALOG"
                                elif menu_idx == 2:
                                    state = "SETTINGS"
                                    settings_menu_idx = 0

                        elif state == "SETTINGS":
                            if sym == tcod.event.K_UP: settings_menu_idx = (settings_menu_idx - 1) % 2
                            elif sym == tcod.event.K_DOWN: settings_menu_idx = (settings_menu_idx + 1) % 2
                            elif sym == tcod.event.K_RETURN:
                                if settings_menu_idx == 0:
                                    is_fullscreen = not is_fullscreen
                                    recompute_context = True
                                elif settings_menu_idx == 1:
                                    state = "MAIN_MENU"
                                    menu_idx = 2

                        elif state == "EPISODE_SELECT":
                            if sym == tcod.event.K_UP: menu_idx = (menu_idx - 1) % len(MISSION_DATA)
                            elif sym == tcod.event.K_DOWN: menu_idx = (menu_idx + 1) % len(MISSION_DATA)
                            elif sym == tcod.event.K_RETURN:
                                if menu_idx in unlocked:
                                    ep_idx = menu_idx
                                    mission = MISSION_DATA[ep_idx]
                                    game_map, px, py, file_x, file_y, exit_x, exit_y, enemies = generate_dungeon(ep_idx)
                                    explored = np.zeros((MAP_VIEW_W, MAP_VIEW_H), dtype=bool, order="F")
                                    
                                    trans = np.array(game_map) == 0
                                    fov = tcod.map.compute_fov(trans, (px, py), radius=12, algorithm=tcod.FOV_BASIC)
                                    explored |= fov
                                    recompute = False
                                    
                                    hp = 100
                                    solved = False
                                    log.messages.clear()
                                    last_enemy_move = time.time()
                                    
                                    if isinstance(mission['start_dialog'], list):
                                        dialog_queue = mission['start_dialog'].copy()
                                        dialog_title, dialog_text = dialog_queue.pop(0)
                                    else:
                                        dialog_title = "[ INCOMING TRANSMISSION ]"
                                        dialog_text = mission['start_dialog']
                                        
                                    next_state = "GAMEPLAY"
                                    state = "DIALOG"
                                
                        elif state == "DIALOG":
                            if sym == tcod.event.K_RETURN:
                                if dialog_queue:
                                    dialog_title, dialog_text = dialog_queue.pop(0)
                                else:
                                    state = next_state
                                    if state == "GAMEPLAY" and len(log.messages) == 0:
                                        log.add("SYSTEM READY.", COLOR_ACCENT)
                                    elif state == "MAIN_MENU":
                                        hp = max_hp

                        elif state == "POPUP":
                            if sym == tcod.event.K_RETURN:
                                if next_state in ["GAMEPLAY", "MAIN_MENU"]:
                                    active_enemy = None
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
                                    if isinstance(mission['end_dialog'], list):
                                        dialog_queue = mission['end_dialog'].copy()
                                        dialog_title, dialog_text = dialog_queue.pop(0)
                                    else:
                                        dialog_title = "[ INCOMING TRANSMISSION ]"
                                        dialog_text = mission['end_dialog']
                                    next_state = "GAMEPLAY"
                                    state = "DIALOG"
                                elif abs(px - exit_x) <= 1 and abs(py - exit_y) <= 1:
                                    if solved:
                                        dialog_title = "[ SYSTEM ]"
                                        dialog_text = "NODE CLEARED.\n\nMemutuskan koneksi aman..."
                                        next_state = "MAIN_MENU"
                                        state = "DIALOG"
                                        if ep_idx + 1 not in unlocked and ep_idx + 1 in MISSION_DATA:
                                            unlocked.append(ep_idx + 1)
                                    else:
                                        log.add("DENIED: Retas file data (f) dahulu.", COLOR_ENEMY)

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
                                            state = "BATTLE_BOSS" if hit['name'] == "SYSTEM_ADMIN" else "BATTLE"
                                            encounter_flash_end = time.time() + 0.3 
                                        else:
                                            px, py = nx, ny
                                            recompute = True
                                            if abs(px - file_x) <= 1 and abs(py - file_y) <= 1 and not solved:
                                                log.add("Target File Found. Press 'E'.", COLOR_ACCENT)

                        elif state in ["BATTLE", "BATTLE_BOSS_PUZZLE"]:
                            puz = ENEMY_PUZZLES.get(active_enemy['name'], ENEMY_PUZZLES['GLITCH']) if state == "BATTLE" else current_boss_puzzle
                            
                            if sym == tcod.event.K_RETURN:
                                if battle_input == puz['puzzle_solution']:
                                    popup_success = True
                                    last_battle_type = "BOSS" if state == "BATTLE_BOSS_PUZZLE" else "NORMAL"
                                    
                                    if state == "BATTLE":
                                        log.add(f"{active_enemy['name']} DEFEATED.", COLOR_ACCENT)
                                        enemies.remove(active_enemy)
                                        
                                        dialog_title = "[ SYSTEM ]"
                                        dialog_text = f"✅ JAWABAN BENAR!\n\nSintaks valid. Anomali {active_enemy['name']} berhasil dihapus dari sistem."
                                        next_state = "GAMEPLAY"
                                        state = "POPUP"
                                        recompute = True
                                    else:
                                        active_enemy['hp'] -= pending_damage
                                        log.add(f"ATTACK SUCCESS: -{pending_damage} HOST", COLOR_PLAYER)
                                        if active_enemy['hp'] <= 0:
                                            log.add("SYSTEM_ADMIN DELETED.", COLOR_ACCENT)
                                            enemies.remove(active_enemy)
                                            
                                            dialog_title = "[ TACTICAL OVERRIDE ]"
                                            dialog_text = f"✅ JAWABAN BENAR!\n\nSerangan berhasil (-{pending_damage} HP).\n\nSYSTEM_ADMIN DELETED. Akses terbuka."
                                            next_state = "GAMEPLAY"
                                            state = "POPUP"
                                            recompute = True
                                        else:
                                            dialog_title = "[ TACTICAL OVERRIDE ]"
                                            dialog_text = f"✅ JAWABAN BENAR!\n\nSerangan berhasil mengenai sistem musuh (-{pending_damage} HP).\nIntegritas HOST tersisa: {active_enemy['hp']} HP."
                                            next_state = "BATTLE_BOSS"
                                            state = "POPUP"
                                else:
                                    popup_success = False
                                    last_battle_type = "BOSS" if state == "BATTLE_BOSS_PUZZLE" else "NORMAL"
                                    dmg = puz.get('dmg', 10) if state == "BATTLE" else 25
                                    hp -= dmg
                                    encounter_flash_end = time.time() + 0.1
                                    
                                    if state == "BATTLE":
                                        log.add(f"ERROR: INTEGRITY LOST (-{dmg})", COLOR_ENEMY)
                                    else:
                                        log.add(f"ATTACK FAILED: -{dmg} INTEGRITY", COLOR_ENEMY)
                                        
                                    if hp <= 0:
                                        dialog_title = "[ FATAL ERROR ]"
                                        dialog_text = f"❌ JAWABAN SALAH!\n\nSistem menerima serangan balik (-{dmg} HP).\n\nCRITICAL ERROR. SYSTEM INTEGRITY AT 0%.\n\n[ CONNECTION TERMINATED ]"
                                        next_state = "MAIN_MENU"
                                        state = "POPUP"
                                    else:
                                        dialog_title = "[ SYSTEM WARNING ]"
                                        dialog_text = f"❌ JAWABAN SALAH!\n\nSintaks tidak valid. Sistem menerima serangan balik sebesar -{dmg} HP."
                                        next_state = "BATTLE" if state == "BATTLE" else "BATTLE_BOSS"
                                        state = "POPUP"
                                        
                                battle_input = ""
                                
                            elif sym == tcod.event.K_BACKSPACE:
                                battle_input = battle_input[:-1]
                            elif 32 <= sym <= 126:
                                char = chr(sym)
                                shift = event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT)
                                shift_map = {'9':'(', '0':')', '[':'{', ']':'}', ';':':', ',':'<', '.':'>', '/':'?', '1':'!', '2':'@', '3':'#', '4':'$', '5':'%', '6':'^', '7':'&', '8':'*'}
                                if shift:
                                    if 'a' <= char <= 'z': char = char.upper()
                                    elif char in shift_map: char = shift_map[char]
                                    elif char == '=': char = '+'
                                    elif char == '-': char = '_'
                                    elif char == "'": char = '"'
                                battle_input += char

                        elif state == "BATTLE_BOSS":
                            if sym == tcod.event.K_UP: boss_menu_idx = (boss_menu_idx - 1) % 3
                            elif sym == tcod.event.K_DOWN: boss_menu_idx = (boss_menu_idx + 1) % 3
                            elif sym == tcod.event.K_RETURN:
                                if boss_menu_idx == 0:
                                    pending_damage = 15
                                    current_boss_puzzle = random.choice(BOSS_PUZZLES_STANDARD)
                                    battle_input = ""
                                    state = "BATTLE_BOSS_PUZZLE"
                                elif boss_menu_idx == 1:
                                    pending_damage = 40
                                    current_boss_puzzle = random.choice(BOSS_PUZZLES_SIGMA)
                                    battle_input = ""
                                    state = "BATTLE_BOSS_PUZZLE"
                                elif boss_menu_idx == 2:
                                    state = "GAMEPLAY"
                                    log.add("Retreating...", COLOR_TEXT_DIM)
                                    recompute = True
                                    active_enemy = None

                if recompute_context:
                    break

if __name__ == "__main__":
    main()