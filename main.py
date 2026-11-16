#!/usr/bin/env python3
"""
===========================================================================
  STRIKER ARENA 6v6 — eFootball Complete Edition (PC + Android Touch)
  Features:
    - Full 9-Team League Simulation (All Teams Play Every Round!)
    - 6 New Clubs from 3 Other Leagues (AC Milan, Juventus, Dortmund,
      Leverkusen, Al-Nassr, Al-Hilal) + Champions League Knockout Mode
      (Top 6 League + 6 Other-League Teams, Pure Knockout, Round Difficulty)
    - League & UCL Top Scorers + Ballon d'Or Rankings + Transfer Market
    - Club Trophies Screen & Club Crest with Dynamic Championship Stars
    - Trophy Ceremony Celebration (League & UCL)
    - Detailed Pitch (LED Ad Boards, Corner Flags, Penalty Arcs, Dugouts,
      Floodlights, Tiered Stands, Spotify Camp Nou Blaugrana, Crowd)
    - Realistic Rotating Ball, Elastic Net Mesh Physics, Impact Effects
    - Smart Goalkeeper & Dynamic Off-Ball Player Awareness
    - Hafid Derradji "KHATIRA!", Menu BGM, & Verified Download Links
===========================================================================
"""

import sys
import os
import math
import time
import json
import socket
import struct
import random
import threading
import datetime
import wave
import webbrowser

try:
    import pygame
except ImportError:
    print("Pygame is not installed! Run: pip install pygame")
    sys.exit(1)


# ---------------------------------------------------------------------------
# CONSTANTS & LARGE 6v6 WORLD CONFIGURATION
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 1200, 740
FPS = 60
TOP_HUD = 82

WORLD_W, WORLD_H = 2200, 1320
PITCH_MARGIN_X = 120
PITCH_MARGIN_Y = 90
PITCH_X = PITCH_MARGIN_X
PITCH_Y = PITCH_MARGIN_Y
PITCH_W = WORLD_W - 2 * PITCH_MARGIN_X
PITCH_H = WORLD_H - 2 * PITCH_MARGIN_Y
PITCH_CX = PITCH_X + PITCH_W // 2
PITCH_CY = PITCH_Y + PITCH_H // 2

GOAL_W = 54
GOAL_H = 250
GOAL_TOP = PITCH_CY - GOAL_H // 2
GOAL_BOTTOM = PITCH_CY + GOAL_H // 2

PLAYER_RADIUS = 19
BALL_RADIUS = 12
DEFAULT_PORT = 5555

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(BASE_DIR, "striker_save.json")
PACKS_DIR = os.path.join(BASE_DIR, "packs")

# Verified External Resource URLs (Opened in Chrome/Browser)
HAFID_DANGER_URL = "https://fish.audio/ar/m/4e4d4eb3dda64c9eb92a94820890a6ce/"
MENU_BGM_URL = "https://elevenlabs.io/music/football"
PLAYER_PHOTOS_URL = "https://www.efootballdb.com/"

# Colors
WHITE = (255, 255, 255)
BLACK = (12, 14, 20)
GOLD = (255, 210, 60)
CYAN = (0, 230, 255)
RED = (235, 65, 75)
BLUE = (55, 145, 255)
GREEN = (46, 204, 113)
PURPLE = (175, 95, 255)
ORANGE = (255, 145, 45)
PINK = (255, 75, 185)
DARK_PANEL = (18, 22, 32)
CARD_BG = (28, 34, 48)
CARD_HOVER = (40, 48, 68)
MUTED_TEXT = (165, 175, 195)


# ---------------------------------------------------------------------------
# 5 MANAGERS & SPREAD-OUT FORMATIONS
# ---------------------------------------------------------------------------
MANAGERS = [
    {"id": "pep", "name": "Pep Guardiola", "style": "Possession Game", "boost": "+5 PAS, +2 DRI", "pac": 0, "sho": 0, "pas": 5, "dri": 2, "key": "pas", "req": 84},
    {"id": "klopp", "name": "Jurgen Klopp", "style": "Quick Counter", "boost": "+5 PAC, +2 SHO", "pac": 5, "sho": 2, "pas": 0, "dri": 0, "key": "pac", "req": 88},
    {"id": "ancelotti", "name": "Carlo Ancelotti", "style": "Out Wide", "boost": "+4 DRI, +3 SHO", "pac": 1, "sho": 3, "pas": 0, "dri": 4, "key": "dri", "req": 88},
    {"id": "mourinho", "name": "Jose Mourinho", "style": "Long Ball Counter", "boost": "+4 SHO, +3 PAS", "pac": 2, "sho": 4, "pas": 3, "dri": 0, "key": "sho", "req": 86},
    {"id": "alonso", "name": "Xabi Alonso", "style": "Total Balanced", "boost": "+3 ALL STATS", "pac": 3, "sho": 3, "pas": 3, "dri": 3, "key": "all", "req": 80},
]

FORMATIONS = [
    {"name": "1-2-2 Attack", "offsets": [(-160, 0), (-360, -320), (-360, 320), (-640, -210), (-640, 210)]},
    {"name": "2-2-1 Balanced", "offsets": [(-180, 0), (-410, -260), (-410, 260), (-690, -260), (-690, 260)]},
    {"name": "2-1-2 Wingers", "offsets": [(-180, -240), (-180, 240), (-440, 0), (-700, -250), (-700, 250)]},
    {"name": "3-1-1 Fortress", "offsets": [(-180, 0), (-440, 0), (-700, -320), (-730, 0), (-700, 320)]},
]


# ---------------------------------------------------------------------------
# PLAYER CATALOG: 14 REAL CLUBS' STARS + EPIC RASHFORD + 15 FREE BASE
# ---------------------------------------------------------------------------
PLAYER_CATALOG = [
    # --- EPIC RASHFORD MAN UTD ---
    {"id": "rashford", "name": "Marcus Rashford", "short": "RASHFORD", "nation": "England", "club": "Man Utd", "pos": "LWF", "num": 10, "match": "Man Utd Classic • Old Trafford", "skills": ["Loop Scream", "Knuckle Shot"], "booster": "United +3", "ovr": 99, "pac": 96, "sho": 95, "pas": 86, "dri": 94, "price": 0, "is_base": False, "skin": (145, 96, 66), "hair": (22, 20, 20), "kit": (205, 32, 38)},

    # --- REAL MADRID ---
    {"id": "mbappe", "name": "Kylian Mbappe", "short": "MBAPPE", "nation": "France", "club": "Real Madrid", "pos": "ST", "num": 9, "match": "El Clasico", "skills": ["Phenomenal Finishing"], "booster": "Agility +2", "ovr": 92, "pac": 97, "sho": 91, "pas": 83, "dri": 93, "price": 4500, "is_base": False, "skin": (145, 98, 68), "hair": (25, 25, 28), "kit": (240, 242, 248)},
    {"id": "vinicius", "name": "Vinicius Jr", "short": "VINI JR", "nation": "Brazil", "club": "Real Madrid", "pos": "LW", "num": 7, "match": "UCL Semi-Final", "skills": ["Momentum Dribbling"], "booster": "Technique +2", "ovr": 91, "pac": 96, "sho": 85, "pas": 83, "dri": 94, "price": 3900, "is_base": False, "skin": (128, 84, 58), "hair": (22, 22, 25), "kit": (240, 242, 248)},
    {"id": "bellingham", "name": "Jude Bellingham", "short": "BELLINGHAM", "nation": "England", "club": "Real Madrid", "pos": "CAM", "num": 5, "match": "La Liga Derby", "skills": ["Rising Shot"], "booster": "Box2Box +2", "ovr": 90, "pac": 83, "sho": 88, "pas": 86, "dri": 90, "price": 3800, "is_base": False, "skin": (165, 118, 86), "hair": (24, 22, 22), "kit": (240, 242, 248)},
    {"id": "valverde", "name": "F. Valverde", "short": "VALVERDE", "nation": "Uruguay", "club": "Real Madrid", "pos": "CM", "num": 8, "match": "UCL Final", "skills": ["Rising Shot"], "booster": "Engine +2", "ovr": 89, "pac": 88, "sho": 85, "pas": 87, "dri": 85, "price": 3500, "is_base": False, "skin": (232, 194, 168), "hair": (48, 38, 30), "kit": (240, 242, 248)},
    {"id": "rudiger", "name": "Antonio Rudiger", "short": "RUDIGER", "nation": "Germany", "club": "Real Madrid", "pos": "CB", "num": 22, "match": "UCL Knockout", "skills": ["Fortress"], "booster": "Defending +2", "ovr": 88, "pac": 83, "sho": 60, "pas": 77, "dri": 74, "price": 3100, "is_base": False, "skin": (132, 88, 60), "hair": (22, 20, 20), "kit": (240, 242, 248)},
    {"id": "courtois", "name": "Thibaut Courtois", "short": "COURTOIS", "nation": "Belgium", "club": "Real Madrid", "pos": "GK", "num": 1, "match": "UCL Final", "skills": ["GK Directing"], "booster": "Reflexes +2", "ovr": 90, "pac": 68, "sho": 55, "pas": 82, "dri": 70, "price": 3400, "is_base": False, "skin": (238, 204, 180), "hair": (58, 44, 34), "kit": (65, 195, 120)},

    # --- MAN CITY ---
    {"id": "haaland", "name": "Erling Haaland", "short": "HAALAND", "nation": "Norway", "club": "Man City", "pos": "ST", "num": 9, "match": "UCL QF vs Bayern", "skills": ["Bullet Header", "Acrobatic Finishing"], "booster": "Striker +3", "ovr": 92, "pac": 87, "sho": 95, "pas": 72, "dri": 82, "price": 4500, "is_base": False, "skin": (245, 212, 188), "hair": (235, 210, 120), "kit": (108, 171, 221)},
    {"id": "rodri", "name": "Rodri", "short": "RODRI", "nation": "Spain", "club": "Man City", "pos": "CDM", "num": 16, "match": "PL Clash", "skills": ["Visionary Pass"], "booster": "Anchor +2", "ovr": 91, "pac": 75, "sho": 82, "pas": 90, "dri": 86, "price": 3900, "is_base": False, "skin": (235, 198, 172), "hair": (65, 48, 36), "kit": (108, 171, 221)},
    {"id": "foden", "name": "Phil Foden", "short": "FODEN", "nation": "England", "club": "Man City", "pos": "CAM", "num": 47, "match": "Manchester Derby", "skills": ["Blitz Curler"], "booster": "Technique +2", "ovr": 89, "pac": 86, "sho": 86, "pas": 87, "dri": 91, "price": 3600, "is_base": False, "skin": (240, 204, 182), "hair": (52, 42, 34), "kit": (108, 171, 221)},
    {"id": "debruyne", "name": "K. De Bruyne", "short": "DE BRUYNE", "nation": "Belgium", "club": "Man City", "pos": "CM", "num": 17, "match": "PL Title Decider", "skills": ["Visionary Pass"], "booster": "Maestro +2", "ovr": 90, "pac": 72, "sho": 88, "pas": 95, "dri": 86, "price": 3800, "is_base": False, "skin": (245, 212, 188), "hair": (195, 145, 78), "kit": (108, 171, 221)},
    {"id": "dias", "name": "Ruben Dias", "short": "R. DIAS", "nation": "Portugal", "club": "Man City", "pos": "CB", "num": 3, "match": "PL Clash", "skills": ["Fortress"], "booster": "Defending +2", "ovr": 88, "pac": 76, "sho": 54, "pas": 80, "dri": 76, "price": 3100, "is_base": False, "skin": (230, 192, 168), "hair": (42, 34, 28), "kit": (108, 171, 221)},
    {"id": "ederson", "name": "Ederson", "short": "EDERSON", "nation": "Brazil", "club": "Man City", "pos": "GK", "num": 31, "match": "PL Clash", "skills": ["GK Directing"], "booster": "Passing +2", "ovr": 88, "pac": 72, "sho": 60, "pas": 90, "dri": 75, "price": 2900, "is_base": False, "skin": (212, 168, 134), "hair": (28, 26, 26), "kit": (245, 195, 45)},

    # --- FC BARCELONA ---
    {"id": "yamal", "name": "Lamine Yamal", "short": "YAMAL", "nation": "Spain", "club": "FC Barcelona", "pos": "RW", "num": 19, "match": "El Clasico", "skills": ["Blitz Curler"], "booster": "Ball Carry +2", "ovr": 90, "pac": 91, "sho": 83, "pas": 87, "dri": 93, "price": 3800, "is_base": False, "skin": (182, 134, 98), "hair": (25, 25, 28), "kit": (165, 30, 65)},
    {"id": "lewandowski", "name": "R. Lewandowski", "short": "LEWA", "nation": "Poland", "club": "FC Barcelona", "pos": "ST", "num": 9, "match": "El Clasico", "skills": ["Phenomenal Finishing"], "booster": "Striker +2", "ovr": 89, "pac": 77, "sho": 92, "pas": 81, "dri": 86, "price": 3500, "is_base": False, "skin": (238, 202, 178), "hair": (46, 36, 30), "kit": (165, 30, 65)},
    {"id": "raphinha", "name": "Raphinha", "short": "RAPHINHA", "nation": "Brazil", "club": "FC Barcelona", "pos": "LW", "num": 11, "match": "UCL Night", "skills": ["Blitz Curler"], "booster": "Agility +2", "ovr": 89, "pac": 91, "sho": 85, "pas": 85, "dri": 89, "price": 3500, "is_base": False, "skin": (188, 140, 104), "hair": (26, 24, 24), "kit": (165, 30, 65)},
    {"id": "pedri", "name": "Pedri", "short": "PEDRI", "nation": "Spain", "club": "FC Barcelona", "pos": "CM", "num": 8, "match": "El Clasico", "skills": ["Visionary Pass"], "booster": "Technique +2", "ovr": 89, "pac": 81, "sho": 76, "pas": 90, "dri": 91, "price": 3400, "is_base": False, "skin": (236, 198, 174), "hair": (42, 34, 28), "kit": (165, 30, 65)},
    {"id": "cubarsi", "name": "Pau Cubarsi", "short": "CUBARSI", "nation": "Spain", "club": "FC Barcelona", "pos": "CB", "num": 2, "match": "La Liga", "skills": ["Fortress"], "booster": "Build Up +2", "ovr": 86, "pac": 80, "sho": 52, "pas": 83, "dri": 79, "price": 2600, "is_base": False, "skin": (238, 202, 178), "hair": (78, 56, 38), "kit": (165, 30, 65)},
    {"id": "terstegen", "name": "Ter Stegen", "short": "TER STEGEN", "nation": "Germany", "club": "FC Barcelona", "pos": "GK", "num": 1, "match": "El Clasico", "skills": ["GK Directing"], "booster": "Reflexes +2", "ovr": 88, "pac": 69, "sho": 55, "pas": 87, "dri": 72, "price": 2900, "is_base": False, "skin": (242, 208, 184), "hair": (145, 108, 65), "kit": (50, 210, 150)},

    # --- BAYERN MUNICH ---
    {"id": "kane", "name": "Harry Kane", "short": "KANE", "nation": "England", "club": "Bayern Munich", "pos": "ST", "num": 9, "match": "Der Klassiker", "skills": ["Phenomenal Finishing"], "booster": "Finishing +2", "ovr": 91, "pac": 74, "sho": 94, "pas": 87, "dri": 84, "price": 4000, "is_base": False, "skin": (242, 208, 184), "hair": (165, 125, 72), "kit": (210, 32, 48)},
    {"id": "musiala", "name": "Jamal Musiala", "short": "MUSIALA", "nation": "Germany", "club": "Bayern Munich", "pos": "CAM", "num": 42, "match": "Der Klassiker", "skills": ["Momentum Dribbling"], "booster": "Dribbling +2", "ovr": 89, "pac": 86, "sho": 82, "pas": 84, "dri": 94, "price": 3600, "is_base": False, "skin": (182, 134, 98), "hair": (26, 24, 24), "kit": (210, 32, 48)},
    {"id": "olise", "name": "Michael Olise", "short": "OLISE", "nation": "France", "club": "Bayern Munich", "pos": "RW", "num": 17, "match": "Der Klassiker", "skills": ["Blitz Curler"], "booster": "Curler +2", "ovr": 88, "pac": 87, "sho": 83, "pas": 86, "dri": 90, "price": 3200, "is_base": False, "skin": (172, 124, 92), "hair": (26, 24, 26), "kit": (210, 32, 48)},
    {"id": "kimmich", "name": "Joshua Kimmich", "short": "KIMMICH", "nation": "Germany", "club": "Bayern Munich", "pos": "CDM", "num": 6, "match": "Bundesliga", "skills": ["Visionary Pass"], "booster": "Maestro +2", "ovr": 88, "pac": 74, "sho": 79, "pas": 90, "dri": 85, "price": 3200, "is_base": False, "skin": (238, 204, 180), "hair": (92, 68, 45), "kit": (210, 32, 48)},
    {"id": "davies", "name": "Alphonso Davies", "short": "DAVIES", "nation": "Canada", "club": "Bayern Munich", "pos": "LB", "num": 19, "match": "UCL Night", "skills": ["Edged Crossing"], "booster": "Speedster +2", "ovr": 86, "pac": 96, "sho": 72, "pas": 80, "dri": 85, "price": 2800, "is_base": False, "skin": (132, 88, 60), "hair": (22, 20, 20), "kit": (210, 32, 48)},
    {"id": "neuer", "name": "Manuel Neuer", "short": "NEUER", "nation": "Germany", "club": "Bayern Munich", "pos": "GK", "num": 1, "match": "UCL Classic", "skills": ["GK Directing"], "booster": "Sweeper +2", "ovr": 88, "pac": 70, "sho": 55, "pas": 88, "dri": 74, "price": 2900, "is_base": False, "skin": (242, 208, 184), "hair": (145, 108, 65), "kit": (45, 165, 220)},

    # --- ARSENAL ---
    {"id": "saka", "name": "Bukayo Saka", "short": "SAKA", "nation": "England", "club": "Arsenal", "pos": "RW", "num": 7, "match": "North London Derby", "skills": ["Blitz Curler"], "booster": "Agility +2", "ovr": 89, "pac": 89, "sho": 85, "pas": 86, "dri": 90, "price": 3600, "is_base": False, "skin": (136, 90, 62), "hair": (22, 20, 20), "kit": (220, 42, 48)},
    {"id": "odegaard", "name": "Martin Odegaard", "short": "ODEGAARD", "nation": "Norway", "club": "Arsenal", "pos": "CAM", "num": 8, "match": "North London Derby", "skills": ["Visionary Pass"], "booster": "Maestro +2", "ovr": 89, "pac": 79, "sho": 83, "pas": 91, "dri": 90, "price": 3500, "is_base": False, "skin": (242, 210, 188), "hair": (195, 158, 92), "kit": (220, 42, 48)},
    {"id": "rice", "name": "Declan Rice", "short": "RICE", "nation": "England", "club": "Arsenal", "pos": "CDM", "num": 41, "match": "PL Clash", "skills": ["Fortress"], "booster": "Box2Box +2", "ovr": 88, "pac": 79, "sho": 77, "pas": 85, "dri": 83, "price": 3200, "is_base": False, "skin": (236, 198, 174), "hair": (68, 50, 36), "kit": (220, 42, 48)},
    {"id": "saliba", "name": "William Saliba", "short": "SALIBA", "nation": "France", "club": "Arsenal", "pos": "CB", "num": 2, "match": "North London Derby", "skills": ["Fortress"], "booster": "Defending +2", "ovr": 88, "pac": 84, "sho": 55, "pas": 78, "dri": 77, "price": 3100, "is_base": False, "skin": (138, 92, 64), "hair": (22, 20, 20), "kit": (220, 42, 48)},
    {"id": "gabriel", "name": "Gabriel M.", "short": "GABRIEL", "nation": "Brazil", "club": "Arsenal", "pos": "CB", "num": 6, "match": "PL Clash", "skills": ["Bullet Header"], "booster": "Defending +2", "ovr": 87, "pac": 78, "sho": 62, "pas": 75, "dri": 72, "price": 2800, "is_base": False, "skin": (182, 134, 98), "hair": (24, 22, 22), "kit": (220, 42, 48)},
    {"id": "raya", "name": "David Raya", "short": "RAYA", "nation": "Spain", "club": "Arsenal", "pos": "GK", "num": 22, "match": "UCL Quarter-Final", "skills": ["GK Directing"], "booster": "Reflexes +2", "ovr": 87, "pac": 70, "sho": 62, "pas": 84, "dri": 72, "price": 2700, "is_base": False, "skin": (232, 195, 170), "hair": (52, 42, 34), "kit": (230, 210, 50)},

    # --- LIVERPOOL ---
    {"id": "salah", "name": "Mohamed Salah", "short": "SALAH", "nation": "Egypt", "club": "Liverpool", "pos": "RW", "num": 11, "match": "Anfield Night", "skills": ["Blitz Curler"], "booster": "Shooting +2", "ovr": 91, "pac": 92, "sho": 90, "pas": 86, "dri": 90, "price": 3800, "is_base": False, "skin": (195, 145, 108), "hair": (22, 20, 20), "kit": (200, 22, 38)},
    {"id": "vandijk", "name": "Virgil van Dijk", "short": "VAN DIJK", "nation": "Netherlands", "club": "Liverpool", "pos": "CB", "num": 4, "match": "Anfield Night", "skills": ["Fortress"], "booster": "Defending +2", "ovr": 90, "pac": 81, "sho": 64, "pas": 81, "dri": 76, "price": 3500, "is_base": False, "skin": (178, 132, 98), "hair": (24, 22, 22), "kit": (200, 22, 38)},
    {"id": "macallister", "name": "A. Mac Allister", "short": "MAC ALLISTER", "nation": "Argentina", "club": "Liverpool", "pos": "CM", "num": 10, "match": "PL Clash", "skills": ["Visionary Pass"], "booster": "Maestro +2", "ovr": 87, "pac": 75, "sho": 82, "pas": 87, "dri": 86, "price": 2900, "is_base": False, "skin": (235, 198, 174), "hair": (132, 72, 42), "kit": (200, 22, 38)},
    {"id": "diaz", "name": "Luis Diaz", "short": "L. DIAZ", "nation": "Colombia", "club": "Liverpool", "pos": "LW", "num": 7, "match": "PL Clash", "skills": ["Momentum Dribbling"], "booster": "Agility +2", "ovr": 87, "pac": 92, "sho": 82, "pas": 79, "dri": 89, "price": 3000, "is_base": False, "skin": (192, 144, 108), "hair": (24, 22, 22), "kit": (200, 22, 38)},
    {"id": "taa", "name": "T. Alexander-Arnold", "short": "TRENT", "nation": "England", "club": "Liverpool", "pos": "RB", "num": 66, "match": "Anfield Night", "skills": ["Edged Crossing"], "booster": "Passing +2", "ovr": 87, "pac": 79, "sho": 76, "pas": 92, "dri": 82, "price": 2900, "is_base": False, "skin": (175, 128, 95), "hair": (26, 24, 24), "kit": (200, 22, 38)},
    {"id": "alisson", "name": "Alisson Becker", "short": "ALISSON", "nation": "Brazil", "club": "Liverpool", "pos": "GK", "num": 1, "match": "Anfield Night", "skills": ["GK Directing"], "booster": "Reflexes +2", "ovr": 89, "pac": 70, "sho": 55, "pas": 86, "dri": 72, "price": 3200, "is_base": False, "skin": (232, 192, 165), "hair": (58, 42, 32), "kit": (40, 180, 140)},

    # --- PSG ---
    {"id": "dembele", "name": "Ousmane Dembele", "short": "DEMBELE", "nation": "France", "club": "PSG", "pos": "RW", "num": 10, "match": "Le Classique", "skills": ["Momentum Dribbling"], "booster": "Speedster +2", "ovr": 89, "pac": 95, "sho": 84, "pas": 84, "dri": 92, "price": 3500, "is_base": False, "skin": (138, 92, 64), "hair": (22, 20, 20), "kit": (28, 48, 92)},
    {"id": "kvara", "name": "Kvaratskhelia", "short": "KVARA", "nation": "Georgia", "club": "PSG", "pos": "LW", "num": 7, "match": "Le Classique", "skills": ["Momentum Dribbling"], "booster": "Dribbling +2", "ovr": 88, "pac": 89, "sho": 83, "pas": 84, "dri": 92, "price": 3300, "is_base": False, "skin": (236, 202, 180), "hair": (38, 30, 26), "kit": (28, 48, 92)},
    {"id": "vitinha", "name": "Vitinha", "short": "VITINHA", "nation": "Portugal", "club": "PSG", "pos": "CM", "num": 17, "match": "UCL Knockout", "skills": ["Game-changing Pass"], "booster": "Maestro +2", "ovr": 89, "pac": 82, "sho": 80, "pas": 89, "dri": 90, "price": 3300, "is_base": False, "skin": (232, 194, 168), "hair": (48, 38, 30), "kit": (28, 48, 92)},
    {"id": "hakimi", "name": "Achraf Hakimi", "short": "HAKIMI", "nation": "Morocco", "club": "PSG", "pos": "RB", "num": 2, "match": "Le Classique", "skills": ["Edged Crossing"], "booster": "Speedster +2", "ovr": 88, "pac": 94, "sho": 76, "pas": 83, "dri": 84, "price": 2900, "is_base": False, "skin": (208, 162, 126), "hair": (22, 20, 20), "kit": (28, 48, 92)},
    {"id": "nuno", "name": "Nuno Mendes", "short": "N. MENDES", "nation": "Portugal", "club": "PSG", "pos": "LB", "num": 25, "match": "UCL Final Stage", "skills": ["Edged Crossing"], "booster": "Speedster +2", "ovr": 87, "pac": 95, "sho": 68, "pas": 80, "dri": 84, "price": 2900, "is_base": False, "skin": (142, 96, 66), "hair": (22, 20, 20), "kit": (28, 48, 92)},
    {"id": "donnarumma", "name": "G. Donnarumma", "short": "DONNARUMMA", "nation": "Italy", "club": "PSG", "pos": "GK", "num": 99, "match": "UCL Knockout", "skills": ["GK Directing"], "booster": "Reflexes +2", "ovr": 89, "pac": 68, "sho": 54, "pas": 79, "dri": 70, "price": 3100, "is_base": False, "skin": (232, 195, 170), "hair": (42, 34, 28), "kit": (235, 130, 45)},

    # --- INTER MILAN ---
    {"id": "lautaro", "name": "Lautaro Martinez", "short": "LAUTARO", "nation": "Argentina", "club": "Inter Milan", "pos": "ST", "num": 10, "match": "Derby della Madonnina", "skills": ["Phenomenal Finishing"], "booster": "Striker +2", "ovr": 89, "pac": 84, "sho": 89, "pas": 78, "dri": 87, "price": 3500, "is_base": False, "skin": (226, 184, 152), "hair": (32, 28, 26), "kit": (20, 65, 165)},
    {"id": "thuram", "name": "Marcus Thuram", "short": "THURAM", "nation": "France", "club": "Inter Milan", "pos": "ST", "num": 9, "match": "Serie A Clash", "skills": ["Acrobatic Finishing"], "booster": "Physical +2", "ovr": 86, "pac": 89, "sho": 84, "pas": 77, "dri": 84, "price": 2700, "is_base": False, "skin": (142, 96, 66), "hair": (22, 20, 20), "kit": (20, 65, 165)},
    {"id": "barella", "name": "Nicolo Barella", "short": "BARELLA", "nation": "Italy", "club": "Inter Milan", "pos": "CM", "num": 23, "match": "Serie A Clash", "skills": ["Game-changing Pass"], "booster": "Engine +2", "ovr": 88, "pac": 82, "sho": 80, "pas": 87, "dri": 87, "price": 3200, "is_base": False, "skin": (236, 198, 174), "hair": (48, 38, 30), "kit": (20, 65, 165)},
    {"id": "calhanoglu", "name": "H. Calhanoglu", "short": "CALHANOGLU", "nation": "Turkey", "club": "Inter Milan", "pos": "CDM", "num": 20, "match": "Serie A Clash", "skills": ["Visionary Pass"], "booster": "Set Piece +2", "ovr": 87, "pac": 74, "sho": 84, "pas": 90, "dri": 84, "price": 2900, "is_base": False, "skin": (232, 192, 166), "hair": (36, 28, 24), "kit": (20, 65, 165)},
    {"id": "bastoni", "name": "A. Bastoni", "short": "BASTONI", "nation": "Italy", "club": "Inter Milan", "pos": "CB", "num": 95, "match": "Derby della Madonnina", "skills": ["Fortress"], "booster": "Build Up +2", "ovr": 87, "pac": 77, "sho": 55, "pas": 82, "dri": 78, "price": 2900, "is_base": False, "skin": (238, 204, 180), "hair": (52, 40, 32), "kit": (20, 65, 165)},
    {"id": "sommer", "name": "Yann Sommer", "short": "SOMMER", "nation": "Switzerland", "club": "Inter Milan", "pos": "GK", "num": 1, "match": "Serie A Clash", "skills": ["GK Directing"], "booster": "Reflexes +2", "ovr": 87, "pac": 68, "sho": 52, "pas": 82, "dri": 70, "price": 2700, "is_base": False, "skin": (238, 204, 180), "hair": (58, 44, 34), "kit": (230, 190, 45)},

    # --- OTHER LEAGUES (SERIE A: AC MILAN & JUVENTUS) ---
    {"id": "leao", "name": "Rafael Leao", "short": "R. LEAO", "nation": "Portugal", "club": "AC Milan", "pos": "LW", "num": 10, "match": "San Siro Derby", "skills": ["Momentum Dribbling"], "booster": "Speedster +2", "ovr": 88, "pac": 94, "sho": 82, "pas": 81, "dri": 90, "price": 3300, "is_base": False, "skin": (145, 98, 68), "hair": (22, 20, 20), "kit": (200, 28, 36)},
    {"id": "pulisic", "name": "Christian Pulisic", "short": "PULISIC", "nation": "USA", "club": "AC Milan", "pos": "RW", "num": 11, "match": "Serie A Night", "skills": ["Blitz Curler"], "booster": "Agility +2", "ovr": 86, "pac": 89, "sho": 82, "pas": 82, "dri": 87, "price": 2700, "is_base": False, "skin": (236, 198, 174), "hair": (58, 44, 34), "kit": (200, 28, 36)},
    {"id": "theo", "name": "Theo Hernandez", "short": "THEO H.", "nation": "France", "club": "AC Milan", "pos": "LB", "num": 19, "match": "San Siro Derby", "skills": ["Edged Crossing"], "booster": "Speedster +2", "ovr": 87, "pac": 94, "sho": 78, "pas": 81, "dri": 84, "price": 2900, "is_base": False, "skin": (232, 194, 168), "hair": (180, 160, 110), "kit": (200, 28, 36)},
    {"id": "reijnders", "name": "T. Reijnders", "short": "REIJNDERS", "nation": "Netherlands", "club": "AC Milan", "pos": "CM", "num": 14, "match": "UCL Night", "skills": ["Box2Box"], "booster": "Engine +2", "ovr": 86, "pac": 83, "sho": 80, "pas": 85, "dri": 86, "price": 2600, "is_base": False, "skin": (210, 165, 130), "hair": (28, 24, 24), "kit": (200, 28, 36)},
    {"id": "tomori", "name": "Fikayo Tomori", "short": "TOMORI", "nation": "England", "club": "AC Milan", "pos": "CB", "num": 23, "match": "Serie A Night", "skills": ["Fortress"], "booster": "Defending +2", "ovr": 85, "pac": 86, "sho": 52, "pas": 74, "dri": 74, "price": 2400, "is_base": False, "skin": (136, 90, 62), "hair": (22, 20, 20), "kit": (200, 28, 36)},
    {"id": "maignan", "name": "Mike Maignan", "short": "MAIGNAN", "nation": "France", "club": "AC Milan", "pos": "GK", "num": 16, "match": "San Siro Derby", "skills": ["GK Directing"], "booster": "Reflexes +2", "ovr": 88, "pac": 71, "sho": 54, "pas": 84, "dri": 73, "price": 2900, "is_base": False, "skin": (138, 92, 64), "hair": (22, 20, 20), "kit": (55, 200, 145)},

    {"id": "vlahovic", "name": "Dusan Vlahovic", "short": "VLAHOVIC", "nation": "Serbia", "club": "Juventus", "pos": "ST", "num": 9, "match": "Derby d'Italia", "skills": ["Rising Shot"], "booster": "Striker +2", "ovr": 86, "pac": 83, "sho": 88, "pas": 74, "dri": 81, "price": 2700, "is_base": False, "skin": (238, 204, 180), "hair": (42, 34, 28), "kit": (230, 232, 238)},
    {"id": "yildiz", "name": "Kenan Yildiz", "short": "YILDIZ", "nation": "Turkey", "club": "Juventus", "pos": "LW", "num": 10, "match": "Serie A Clash", "skills": ["Momentum Dribbling"], "booster": "Technique +2", "ovr": 84, "pac": 86, "sho": 80, "pas": 80, "dri": 87, "price": 2300, "is_base": False, "skin": (235, 198, 174), "hair": (36, 28, 24), "kit": (230, 232, 238)},
    {"id": "koopmeiners", "name": "T. Koopmeiners", "short": "KOOPMEINERS", "nation": "Netherlands", "club": "Juventus", "pos": "CAM", "num": 8, "match": "Serie A Clash", "skills": ["Visionary Pass"], "booster": "Maestro +2", "ovr": 85, "pac": 76, "sho": 83, "pas": 86, "dri": 82, "price": 2400, "is_base": False, "skin": (242, 208, 184), "hair": (135, 98, 62), "kit": (230, 232, 238)},
    {"id": "bremer", "name": "Gleison Bremer", "short": "BREMER", "nation": "Brazil", "club": "Juventus", "pos": "CB", "num": 3, "match": "Derby d'Italia", "skills": ["Fortress"], "booster": "Defending +2", "ovr": 87, "pac": 82, "sho": 56, "pas": 75, "dri": 74, "price": 2800, "is_base": False, "skin": (175, 128, 95), "hair": (24, 22, 22), "kit": (230, 232, 238)},
    {"id": "cambiaso", "name": "A. Cambiaso", "short": "CAMBIASO", "nation": "Italy", "club": "Juventus", "pos": "RB", "num": 27, "match": "Serie A Clash", "skills": ["Edged Crossing"], "booster": "Engine +2", "ovr": 84, "pac": 84, "sho": 72, "pas": 82, "dri": 83, "price": 2200, "is_base": False, "skin": (236, 198, 174), "hair": (48, 38, 30), "kit": (230, 232, 238)},
    {"id": "digregorio", "name": "M. Di Gregorio", "short": "DI GREGORIO", "nation": "Italy", "club": "Juventus", "pos": "GK", "num": 29, "match": "UCL Night", "skills": ["GK Directing"], "booster": "Reflexes +2", "ovr": 84, "pac": 68, "sho": 52, "pas": 79, "dri": 70, "price": 2100, "is_base": False, "skin": (236, 198, 174), "hair": (42, 34, 28), "kit": (245, 185, 45)},

    # --- OTHER LEAGUES (BUNDESLIGA: DORTMUND & LEVERKUSEN) ---
    {"id": "guirassy", "name": "Serhou Guirassy", "short": "GUIRASSY", "nation": "Guinea", "club": "Dortmund", "pos": "ST", "num": 9, "match": "Der Klassiker", "skills": ["Phenomenal Finishing"], "booster": "Striker +2", "ovr": 86, "pac": 82, "sho": 88, "pas": 74, "dri": 81, "price": 2700, "is_base": False, "skin": (138, 92, 64), "hair": (22, 20, 20), "kit": (245, 205, 30)},
    {"id": "brandt", "name": "Julian Brandt", "short": "BRANDT", "nation": "Germany", "club": "Dortmund", "pos": "CAM", "num": 10, "match": "UCL Night", "skills": ["Visionary Pass"], "booster": "Playmaker +2", "ovr": 85, "pac": 80, "sho": 80, "pas": 86, "dri": 86, "price": 2500, "is_base": False, "skin": (242, 208, 184), "hair": (185, 148, 82), "kit": (245, 205, 30)},
    {"id": "sabitzer", "name": "Marcel Sabitzer", "short": "SABITZER", "nation": "Austria", "club": "Dortmund", "pos": "CM", "num": 20, "match": "UCL Knockout", "skills": ["Rising Shot"], "booster": "Engine +2", "ovr": 84, "pac": 78, "sho": 82, "pas": 83, "dri": 82, "price": 2300, "is_base": False, "skin": (238, 204, 180), "hair": (68, 50, 36), "kit": (245, 205, 30)},
    {"id": "schlotterbeck", "name": "N. Schlotterbeck", "short": "SCHLOTTER", "nation": "Germany", "club": "Dortmund", "pos": "CB", "num": 4, "match": "Bundesliga", "skills": ["Fortress"], "booster": "Build Up +2", "ovr": 85, "pac": 80, "sho": 58, "pas": 79, "dri": 76, "price": 2400, "is_base": False, "skin": (242, 208, 184), "hair": (110, 82, 52), "kit": (245, 205, 30)},
    {"id": "kobel", "name": "Gregor Kobel", "short": "KOBEL", "nation": "Switzerland", "club": "Dortmund", "pos": "GK", "num": 1, "match": "UCL Final", "skills": ["GK Directing"], "booster": "Reflexes +2", "ovr": 88, "pac": 69, "sho": 52, "pas": 78, "dri": 70, "price": 2900, "is_base": False, "skin": (238, 204, 180), "hair": (52, 42, 34), "kit": (45, 190, 110)},

    {"id": "wirtz", "name": "Florian Wirtz", "short": "WIRTZ", "nation": "Germany", "club": "Leverkusen", "pos": "CAM", "num": 10, "match": "Bundesliga", "skills": ["Visionary Pass"], "booster": "Maestro +2", "ovr": 89, "pac": 85, "sho": 83, "pas": 89, "dri": 92, "price": 3600, "is_base": False, "skin": (242, 208, 184), "hair": (145, 112, 68), "kit": (205, 28, 38)},
    {"id": "boniface", "name": "Victor Boniface", "short": "BONIFACE", "nation": "Nigeria", "club": "Leverkusen", "pos": "ST", "num": 22, "match": "Bundesliga", "skills": ["Bullet Header"], "booster": "Striker +2", "ovr": 85, "pac": 85, "sho": 86, "pas": 74, "dri": 83, "price": 2500, "is_base": False, "skin": (132, 88, 60), "hair": (22, 20, 20), "kit": (205, 28, 38)},
    {"id": "frimpong", "name": "J. Frimpong", "short": "FRIMPONG", "nation": "Netherlands", "club": "Leverkusen", "pos": "RB", "num": 30, "match": "Bundesliga", "skills": ["Edged Crossing"], "booster": "Speedster +2", "ovr": 86, "pac": 96, "sho": 74, "pas": 80, "dri": 87, "price": 2800, "is_base": False, "skin": (136, 90, 62), "hair": (22, 20, 20), "kit": (205, 28, 38)},
    {"id": "xhaka", "name": "Granit Xhaka", "short": "XHAKA", "nation": "Switzerland", "club": "Leverkusen", "pos": "CDM", "num": 34, "match": "Bundesliga", "skills": ["Visionary Pass"], "booster": "Anchor +2", "ovr": 86, "pac": 68, "sho": 80, "pas": 88, "dri": 80, "price": 2600, "is_base": False, "skin": (236, 198, 174), "hair": (42, 34, 28), "kit": (205, 28, 38)},
    {"id": "tah", "name": "Jonathan Tah", "short": "TAH", "nation": "Germany", "club": "Leverkusen", "pos": "CB", "num": 4, "match": "Bundesliga", "skills": ["Fortress"], "booster": "Defending +2", "ovr": 86, "pac": 79, "sho": 55, "pas": 78, "dri": 73, "price": 2600, "is_base": False, "skin": (165, 118, 86), "hair": (22, 20, 20), "kit": (205, 28, 38)},
    {"id": "hradecky", "name": "Lukas Hradecky", "short": "HRADECKY", "nation": "Finland", "club": "Leverkusen", "pos": "GK", "num": 1, "match": "Bundesliga", "skills": ["GK Directing"], "booster": "Reflexes +2", "ovr": 84, "pac": 66, "sho": 52, "pas": 76, "dri": 68, "price": 2100, "is_base": False, "skin": (242, 208, 184), "hair": (88, 66, 44), "kit": (45, 165, 220)},

    # --- OTHER LEAGUES (SAUDI PRO LEAGUE: AL-NASSR & AL-HILAL) ---
    {"id": "ronaldo", "name": "Cristiano Ronaldo", "short": "RONALDO", "nation": "Portugal", "club": "Al-Nassr", "pos": "ST", "num": 7, "match": "Riyadh Derby", "skills": ["Bullet Header"], "booster": "Aerial +2", "ovr": 87, "pac": 81, "sho": 91, "pas": 78, "dri": 83, "price": 2800, "is_base": False, "skin": (225, 178, 145), "hair": (32, 28, 26), "kit": (245, 205, 45)},
    {"id": "mane", "name": "Sadio Mane", "short": "MANE", "nation": "Senegal", "club": "Al-Nassr", "pos": "LW", "num": 10, "match": "Riyadh Derby", "skills": ["Momentum Dribbling"], "booster": "Agility +2", "ovr": 85, "pac": 88, "sho": 83, "pas": 79, "dri": 86, "price": 2400, "is_base": False, "skin": (128, 84, 58), "hair": (22, 20, 20), "kit": (245, 205, 45)},
    {"id": "talisca", "name": "Anderson Talisca", "short": "TALISCA", "nation": "Brazil", "club": "Al-Nassr", "pos": "CAM", "num": 94, "match": "Riyadh Derby", "skills": ["Rising Shot"], "booster": "Shooting +2", "ovr": 84, "pac": 80, "sho": 86, "pas": 81, "dri": 83, "price": 2200, "is_base": False, "skin": (175, 128, 95), "hair": (26, 24, 24), "kit": (245, 205, 45)},
    {"id": "brozovic", "name": "Marcelo Brozovic", "short": "BROZOVIC", "nation": "Croatia", "club": "Al-Nassr", "pos": "CDM", "num": 77, "match": "Riyadh Derby", "skills": ["Visionary Pass"], "booster": "Engine +2", "ovr": 84, "pac": 72, "sho": 76, "pas": 86, "dri": 81, "price": 2100, "is_base": False, "skin": (238, 204, 180), "hair": (48, 38, 30), "kit": (245, 205, 45)},
    {"id": "laporte", "name": "Aymeric Laporte", "short": "LAPORTE", "nation": "Spain", "club": "Al-Nassr", "pos": "CB", "num": 27, "match": "Riyadh Derby", "skills": ["Fortress"], "booster": "Build Up +2", "ovr": 85, "pac": 74, "sho": 55, "pas": 82, "dri": 75, "price": 2300, "is_base": False, "skin": (238, 204, 180), "hair": (68, 50, 36), "kit": (245, 205, 45)},
    {"id": "bento", "name": "Bento", "short": "BENTO", "nation": "Brazil", "club": "Al-Nassr", "pos": "GK", "num": 24, "match": "Riyadh Derby", "skills": ["GK Directing"], "booster": "Reflexes +2", "ovr": 83, "pac": 68, "sho": 52, "pas": 76, "dri": 68, "price": 1900, "is_base": False, "skin": (232, 194, 168), "hair": (42, 34, 28), "kit": (50, 175, 130)},

    {"id": "mitrovic", "name": "A. Mitrovic", "short": "MITROVIC", "nation": "Serbia", "club": "Al-Hilal", "pos": "ST", "num": 9, "match": "Riyadh Derby", "skills": ["Bullet Header"], "booster": "Striker +2", "ovr": 86, "pac": 77, "sho": 88, "pas": 75, "dri": 79, "price": 2600, "is_base": False, "skin": (238, 204, 180), "hair": (42, 34, 28), "kit": (25, 85, 210)},
    {"id": "malcom", "name": "Malcom", "short": "MALCOM", "nation": "Brazil", "club": "Al-Hilal", "pos": "RW", "num": 77, "match": "Riyadh Derby", "skills": ["Blitz Curler"], "booster": "Agility +2", "ovr": 85, "pac": 89, "sho": 82, "pas": 82, "dri": 86, "price": 2400, "is_base": False, "skin": (188, 140, 104), "hair": (26, 24, 24), "kit": (25, 85, 210)},
    {"id": "salem", "name": "Salem Al-Dawsari", "short": "SALEM", "nation": "Saudi Arabia", "club": "Al-Hilal", "pos": "LW", "num": 29, "match": "Riyadh Derby", "skills": ["Momentum Dribbling"], "booster": "Technique +2", "ovr": 84, "pac": 88, "sho": 81, "pas": 80, "dri": 86, "price": 2300, "is_base": False, "skin": (208, 162, 126), "hair": (22, 20, 20), "kit": (25, 85, 210)},
    {"id": "neves", "name": "Ruben Neves", "short": "R. NEVES", "nation": "Portugal", "club": "Al-Hilal", "pos": "CDM", "num": 8, "match": "Riyadh Derby", "skills": ["Visionary Pass"], "booster": "Maestro +2", "ovr": 85, "pac": 71, "sho": 81, "pas": 88, "dri": 81, "price": 2400, "is_base": False, "skin": (232, 194, 168), "hair": (48, 38, 30), "kit": (25, 85, 210)},
    {"id": "koulibaly", "name": "K. Koulibaly", "short": "KOULIBALY", "nation": "Senegal", "club": "Al-Hilal", "pos": "CB", "num": 3, "match": "Riyadh Derby", "skills": ["Fortress"], "booster": "Defending +2", "ovr": 85, "pac": 79, "sho": 54, "pas": 75, "dri": 72, "price": 2400, "is_base": False, "skin": (128, 84, 58), "hair": (22, 20, 20), "kit": (25, 85, 210)},
    {"id": "bono", "name": "Yassine Bounou", "short": "BONO", "nation": "Morocco", "club": "Al-Hilal", "pos": "GK", "num": 37, "match": "Riyadh Derby", "skills": ["GK Directing"], "booster": "Reflexes +2", "ovr": 86, "pac": 69, "sho": 52, "pas": 79, "dri": 70, "price": 2600, "is_base": False, "skin": (212, 168, 134), "hair": (32, 26, 24), "kit": (235, 135, 45)},

    # --- OTHER STARS ---
    {"id": "messi", "name": "Lionel Messi", "short": "MESSI", "nation": "Argentina", "club": "Inter Miami", "pos": "RW", "num": 10, "match": "WC Qualifier", "skills": ["Visionary Pass"], "booster": "Playmaker +2", "ovr": 89, "pac": 79, "sho": 90, "pas": 93, "dri": 95, "price": 3500, "is_base": False, "skin": (232, 192, 165), "hair": (58, 42, 32), "kit": (245, 145, 175)},
    {"id": "bruno", "name": "Bruno Fernandes", "short": "BRUNO F.", "nation": "Portugal", "club": "Man Utd", "pos": "CAM", "num": 8, "match": "Manchester Derby", "skills": ["Pinpoint Crossing"], "booster": "Playmaker +2", "ovr": 88, "pac": 77, "sho": 86, "pas": 90, "dri": 85, "price": 3200, "is_base": False, "skin": (230, 192, 168), "hair": (48, 38, 32), "kit": (205, 32, 38)},
]

# 15 FREE BASE PLAYERS
BASE_PLAYERS_DATA = [
    ("base_1", "Tariq Lamptey", "LAMPTEY", "Ghana", "Brighton", "RB", 2, 71),
    ("base_2", "K. Adeyemi", "ADEYEMI", "Germany", "Dortmund", "LW", 27, 74),
    ("base_3", "Omar Marmoush", "MARMOUSH", "Egypt", "Man City", "ST", 7, 75),
    ("base_4", "Y. En-Nesyri", "EN-NESYRI", "Morocco", "Fenerbahce", "ST", 19, 73),
    ("base_5", "M. Elneny", "ELNENY", "Egypt", "Al Jazira", "CDM", 17, 69),
    ("base_6", "A. Martial", "MARTIAL", "France", "AEK Athens", "ST", 9, 72),
    ("base_7", "J. Evans", "EVANS", "N. Ireland", "Man Utd", "CB", 35, 68),
    ("base_8", "T. Malacia", "MALACIA", "Netherlands", "Man Utd", "LB", 12, 70),
    ("base_9", "H. Maguire", "MAGUIRE", "England", "Man Utd", "CB", 5, 74),
    ("base_10", "A. Bayindir", "BAYINDIR", "Turkey", "Man Utd", "GK", 1, 71),
    ("base_11", "S. Amrabat", "AMRABAT", "Morocco", "Fenerbahce", "CDM", 4, 73),
    ("base_12", "D. Dalot", "DALOT", "Portugal", "Man Utd", "RB", 20, 74),
    ("base_13", "M. Mount", "MOUNT", "England", "Man Utd", "CAM", 7, 73),
    ("base_14", "K. Mainoo", "MAINOO", "England", "Man Utd", "CM", 37, 72),
    ("base_15", "A. Diallo", "AMAD", "Ivory Coast", "Man Utd", "RW", 16, 73),
]

for bid, bname, bshort, bnat, bclub, bpos, bnum, bovr in BASE_PLAYERS_DATA:
    PLAYER_CATALOG.append({
        "id": bid, "name": bname, "short": bshort, "nation": bnat, "club": bclub,
        "pos": bpos, "num": bnum, "match": "Base Squad Player",
        "skills": [], "booster": None, "ovr": bovr,
        "pac": bovr + 2, "sho": bovr - 2, "pas": bovr, "dri": bovr + 1,
        "price": 0, "is_base": True,
        "skin": (195, 150, 115), "hair": (26, 24, 24), "kit": (70, 85, 110),
    })

CATALOG_BY_ID = {c["id"]: c for c in PLAYER_CATALOG}

# 8 Domestic League Opponent Clubs + 6 Foreign League Clubs (3 Leagues x 2 Clubs)
CLUBS_DATA = {
    # Domestic League (Top 6 qualify for Champions League!)
    "Real Madrid":   {"league": "Premier", "kit": (235, 238, 245), "gk_kit": (65, 195, 120), "difficulty": 3, "rating": 90, "lineup": ["mbappe", "vinicius", "bellingham", "valverde", "rudiger"], "gk": "courtois"},
    "Man City":      {"league": "Premier", "kit": (108, 171, 221), "gk_kit": (245, 195, 45), "difficulty": 3, "rating": 90, "lineup": ["haaland", "foden", "debruyne", "rodri", "dias"], "gk": "ederson"},
    "FC Barcelona":  {"league": "Premier", "kit": (165, 30, 65),   "gk_kit": (50, 210, 150), "difficulty": 2, "rating": 88, "lineup": ["yamal", "lewandowski", "raphinha", "pedri", "cubarsi"], "gk": "terstegen"},
    "Bayern Munich": {"league": "Premier", "kit": (210, 32, 48),   "gk_kit": (45, 165, 220), "difficulty": 3, "rating": 89, "lineup": ["kane", "musiala", "olise", "kimmich", "davies"], "gk": "neuer"},
    "Arsenal":       {"league": "Premier", "kit": (220, 42, 48),   "gk_kit": (230, 210, 50), "difficulty": 2, "rating": 88, "lineup": ["saka", "odegaard", "rice", "saliba", "gabriel"], "gk": "raya"},
    "Liverpool":     {"league": "Premier", "kit": (200, 22, 38),   "gk_kit": (40, 180, 140), "difficulty": 3, "rating": 89, "lineup": ["salah", "diaz", "macallister", "taa", "vandijk"], "gk": "alisson"},
    "PSG":           {"league": "Premier", "kit": (28, 48, 92),    "gk_kit": (235, 130, 45), "difficulty": 2, "rating": 87, "lineup": ["dembele", "kvara", "vitinha", "hakimi", "nuno"], "gk": "donnarumma"},
    "Inter Milan":   {"league": "Premier", "kit": (20, 65, 165),   "gk_kit": (230, 190, 45), "difficulty": 1, "rating": 87, "lineup": ["lautaro", "thuram", "barella", "calhanoglu", "bastoni"], "gk": "sommer"},
    # Foreign League 1: Serie A (2 Clubs)
    "AC Milan":      {"league": "Serie A", "kit": (200, 28, 36),   "gk_kit": (55, 200, 145), "difficulty": 2, "rating": 86, "lineup": ["leao", "pulisic", "reijnders", "theo", "tomori"], "gk": "maignan"},
    "Juventus":      {"league": "Serie A", "kit": (220, 222, 228), "gk_kit": (245, 185, 45), "difficulty": 2, "rating": 85, "lineup": ["vlahovic", "yildiz", "koopmeiners", "cambiaso", "bremer"], "gk": "digregorio"},
    # Foreign League 2: Bundesliga (2 Clubs)
    "Dortmund":      {"league": "Bundesliga", "kit": (245, 205, 30), "gk_kit": (45, 190, 110), "difficulty": 2, "rating": 86, "lineup": ["guirassy", "base_2", "brandt", "sabitzer", "schlotterbeck"], "gk": "kobel"},
    "Leverkusen":    {"league": "Bundesliga", "kit": (205, 28, 38),  "gk_kit": (45, 165, 220), "difficulty": 2, "rating": 87, "lineup": ["boniface", "wirtz", "frimpong", "xhaka", "tah"], "gk": "hradecky"},
    # Foreign League 3: Saudi Pro League (2 Clubs)
    "Al-Nassr":      {"league": "Saudi Pro", "kit": (245, 205, 45),  "gk_kit": (50, 175, 130), "difficulty": 1, "rating": 85, "lineup": ["ronaldo", "mane", "talisca", "brozovic", "laporte"], "gk": "bento"},
    "Al-Hilal":      {"league": "Saudi Pro", "kit": (25, 85, 210),   "gk_kit": (235, 135, 45), "difficulty": 2, "rating": 86, "lineup": ["mitrovic", "malcom", "salem", "neves", "koulibaly"], "gk": "bono"},
}

FOREIGN_UCL_CLUBS = ["AC Milan", "Juventus", "Dortmund", "Leverkusen", "Al-Nassr", "Al-Hilal"]

PACK_POOL_10 = [{"pid": "rashford", "rarity": "EPIC"}] + [
    {"pid": f"base_{i}", "rarity": "BASE"} for i in range(1, 10)
]


# ---------------------------------------------------------------------------
# 8 STADIUMS (INCLUDING DETAILED SPOTIFY CAMP NOU)
# ---------------------------------------------------------------------------
STADIUMS = [
    {"id": "classic", "name": "Classic Wembley", "subtitle": "Balanced Turf • Daytime", "bg": (18, 26, 22), "stands": (34, 42, 48), "turf_a": (42, 138, 64), "turf_b": (36, 124, 56), "lines": (245, 250, 245), "goal_post": (240, 240, 240), "net": (210, 220, 215), "accent": (72, 220, 110), "sky": (45, 110, 185), "ball_friction": 0.985},
    {"id": "night", "name": "Champions Night", "subtitle": "Floodlit Emerald • Fast Pitch", "bg": (10, 14, 28), "stands": (22, 28, 46), "turf_a": (24, 108, 78), "turf_b": (20, 94, 68), "lines": (230, 255, 245), "goal_post": (255, 255, 255), "net": (180, 210, 230), "accent": (80, 190, 255), "sky": (12, 18, 42), "ball_friction": 0.988},
    {"id": "bernabeu", "name": "Santiago Bernabeu", "subtitle": "Royal White & Gold • Madrid", "bg": (20, 22, 34), "stands": (215, 218, 228), "turf_a": (32, 148, 74), "turf_b": (26, 132, 66), "lines": (255, 255, 255), "goal_post": (255, 215, 80), "net": (230, 235, 245), "accent": (255, 210, 60), "sky": (25, 35, 68), "ball_friction": 0.987},
    {"id": "trafford", "name": "Old Trafford", "subtitle": "Theatre of Dreams • Red & Turf", "bg": (34, 14, 16), "stands": (165, 28, 36), "turf_a": (38, 132, 58), "turf_b": (32, 118, 50), "lines": (250, 250, 250), "goal_post": (255, 255, 255), "net": (220, 220, 220), "accent": (235, 65, 75), "sky": (48, 28, 35), "ball_friction": 0.986},
    {"id": "campnou", "name": "Spotify Camp Nou", "subtitle": "Blaugrana Stands • Barcelona", "bg": (14, 18, 42), "stands": (18, 48, 128), "turf_a": (34, 146, 72), "turf_b": (26, 130, 62), "lines": (252, 252, 255), "goal_post": (255, 212, 65), "net": (225, 232, 248), "accent": (168, 28, 68), "sky": (22, 38, 88), "ball_friction": 0.987},
    {"id": "desert", "name": "Cairo Sunset Arena", "subtitle": "Warm Golden Turf • Heavy Grip", "bg": (38, 24, 18), "stands": (62, 38, 28), "turf_a": (122, 132, 52), "turf_b": (108, 118, 44), "lines": (255, 246, 220), "goal_post": (255, 215, 130), "net": (235, 215, 175), "accent": (255, 175, 65), "sky": (145, 72, 42), "ball_friction": 0.981},
    {"id": "arctic", "name": "Arctic Ice Dome", "subtitle": "Low Friction Ice • High Speed", "bg": (16, 28, 42), "stands": (30, 48, 70), "turf_a": (135, 195, 225), "turf_b": (120, 182, 214), "lines": (255, 255, 255), "goal_post": (200, 240, 255), "net": (225, 245, 255), "accent": (140, 235, 255), "sky": (28, 52, 82), "ball_friction": 0.992},
    {"id": "cyber", "name": "Cyber Neon Arena", "subtitle": "Futuristic Synth Pitch", "bg": (10, 8, 22), "stands": (24, 18, 44), "turf_a": (26, 28, 52), "turf_b": (20, 22, 42), "lines": (0, 245, 220), "goal_post": (255, 60, 180), "net": (130, 80, 255), "accent": (255, 60, 180), "sky": (16, 10, 38), "ball_friction": 0.989},
]


# ---------------------------------------------------------------------------
# DUAL AUDIO ENGINE (PYGAME + ANDROID MEDIAPLAYER + MENU BGM + HAFID KHATIRA)
# ---------------------------------------------------------------------------
class SoundBank:
    def __init__(self):
        self.enabled = True
        self.bg_enabled = True
        self.menu_bgm_enabled = True
        self.commentary_lang = "hafid"
        self.sounds = {}
        self.paths = {}
        self.bg_channel = None
        self.menu_channel = None
        self.android_bg = None
        self.android_menu = None
        self.backend = "None"
        self.has_jnius = False
        self._init_audio()

    def _init_audio(self):
        self._ensure_core_files()
        self._jnius_mp = None
        self.has_jnius = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
            pygame.mixer.set_num_channels(16)
            for name, fp in self.paths.items():
                snd = pygame.mixer.Sound(fp)
                snd.set_volume(1.0)
                self.sounds[name] = snd
            self.backend = f"Pygame {pygame.mixer.get_init()}"
        except Exception as e:
            self.backend = "Android MediaPlayer" if self.has_jnius else f"Err: {e}"
        if self.has_jnius:
            self.backend += " + Android"

    def _write_stereo_wav_file(self, mono_samples, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        stereo = []
        for s in mono_samples:
            stereo.append(s)
            stereo.append(s)
        raw = struct.pack("<" + "h" * len(stereo), *stereo)
        with wave.open(filepath, "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(44100)
            wf.writeframes(raw)

    def _find_custom_audio(self, folder, stem):
        d = os.path.join(PACKS_DIR, folder)
        for ext in (".mp3", ".ogg", ".wav"):
            fp = os.path.join(d, stem + ext)
            if os.path.exists(fp):
                return fp
        return None

    def _ensure_core_files(self):
        core_dir = os.path.join(PACKS_DIR, "core_audio_44k")
        sr = 44100

        def make_if_missing(name, samples):
            fp = os.path.join(core_dir, f"{name}.wav")
            if not os.path.exists(fp):
                self._write_stereo_wav_file(samples, fp)
            self.paths[name] = fp

        make_if_missing("kick", [max(-32767, min(32767, int(30000 * math.exp(-i / sr * 26) * math.sin(2 * math.pi * (165 * math.exp(-i / sr * 22) + 52) * (i / sr))))) for i in range(int(sr * 0.12))])
        make_if_missing("power", [max(-32767, min(32767, int(31500 * math.exp(-i / sr * 15) * math.sin(2 * math.pi * (230 * math.exp(-i / sr * 18) + 42) * (i / sr))))) for i in range(int(sr * 0.20))])
        make_if_missing("net", [max(-32767, min(32767, int(27000 * math.exp(-i / sr * 8) * (random.uniform(-0.7, 0.7) + 0.3 * math.sin(2 * math.pi * 360 * (i / sr)))))) for i in range(int(sr * 0.32))])
        make_if_missing("post", [max(-32767, min(32767, int(23000 * math.exp(-i / sr * 11) * (0.6 * math.sin(2 * math.pi * 620 * i / sr) + 0.4 * math.sin(2 * math.pi * 930 * i / sr))))) for i in range(int(sr * 0.26))])
        make_if_missing("click", [max(-32767, min(32767, int(18000 * math.exp(-i / sr * 60) * math.sin(2 * math.pi * 880 * i / sr)))) for i in range(int(sr * 0.05))])

        whistle = []
        for i in range(int(sr * 0.36)):
            t = i / sr
            env = 1.0 if t < 0.28 else max(0.0, (0.36 - t) / 0.08)
            mod = 1.0 + 0.04 * math.sin(2 * math.pi * 38 * t)
            whistle.append(max(-32767, min(32767, int(22000 * env * (0.7 * math.sin(2 * math.pi * 2650 * mod * t) + 0.3 * math.sin(2 * math.pi * 2780 * t))))))
        make_if_missing("whistle", whistle)

        crowd = []
        for i in range(int(sr * 1.1)):
            t = i / sr
            env = min(1.0, t / 0.14) * max(0.0, 1.0 - (t / 1.1) ** 2)
            noise = random.uniform(-1, 1) * 0.55
            chord = 0.22 * math.sin(2 * math.pi * 261.6 * t) + 0.22 * math.sin(2 * math.pi * 329.6 * t) + 0.16 * math.sin(2 * math.pi * 392.0 * t)
            crowd.append(max(-32767, min(32767, int(26000 * env * (noise + chord)))))
        make_if_missing("goal", crowd)

    def install_bg_pack(self):
        fp = os.path.join(PACKS_DIR, "bg_crowd", "crowd_loop.wav")
        sr = 44100
        bg = [max(-32767, min(32767, int(6500 * (0.7 + 0.3 * math.sin(2 * math.pi * 0.5 * i / sr)) * (random.uniform(-0.65, 0.65) + 0.35 * math.sin(2 * math.pi * 130 * i / sr))))) for i in range(int(sr * 2.0))]
        self._write_stereo_wav_file(bg, fp)
        self.paths["bg_loop"] = fp
        try:
            snd = pygame.mixer.Sound(fp)
            snd.set_volume(0.45)
            self.sounds["bg_loop"] = snd
        except Exception:
            pass

    def install_menu_bgm_pack(self):
        fp = os.path.join(PACKS_DIR, "menu_bgm", "menu_theme.wav")
        sr = 44100
        dur = 4.0
        n = int(sr * dur)
        chords = [(220.0, 261.6, 329.6), (174.6, 220.0, 261.6), (261.6, 329.6, 392.0), (196.0, 246.9, 293.7)]
        samples = []
        for i in range(n):
            t = i / sr
            beat = (t * 2.0) % 1.0
            pulse = 0.55 + 0.45 * math.exp(-beat * 5.0)
            c = chords[min(3, int(t))]
            pad = 0.35 * math.sin(2 * math.pi * c[0] * t) + 0.30 * math.sin(2 * math.pi * c[1] * t) + 0.25 * math.sin(2 * math.pi * c[2] * t)
            bass = 0.35 * math.sin(2 * math.pi * (c[0] * 0.5) * t) * math.exp(-beat * 3.5)
            samples.append(max(-32767, min(32767, int(9500 * pulse * (pad + bass)))))
        self._write_stereo_wav_file(samples, fp)
        self.paths["menu_bgm"] = fp
        try:
            snd = pygame.mixer.Sound(fp)
            snd.set_volume(0.40)
            self.sounds["menu_bgm"] = snd
        except Exception:
            pass

    def generate_commentary_pack_files(self, lang):
        fp_goal = os.path.join(PACKS_DIR, f"commentary_{lang}", "goal.wav")
        sr = 44100
        freqs = [330, 440, 554, 659] if lang == "hafid" else [293, 392, 493, 587]
        samples = [max(-32767, min(32767, int(22000 * math.sin(math.pi * (i / sr) / 1.1) * (0.5 * math.sin(2 * math.pi * freqs[min(3, int((i / sr) / 1.1 * 4))] * (i / sr)) + 0.3 * random.uniform(-1, 1))))) for i in range(int(sr * 1.1))]
        self._write_stereo_wav_file(samples, fp_goal)

        if lang == "hafid":
            fp_danger = os.path.join(PACKS_DIR, "commentary_hafid", "danger.wav")
            d_samples = []
            for i in range(int(sr * 0.75)):
                t = i / sr
                env = math.sin(math.pi * t / 0.75)
                pitch = 380 + 260 * (t / 0.75)
                d_samples.append(max(-32767, min(32767, int(24000 * env * (0.65 * math.sin(2 * math.pi * pitch * t) + 0.25 * math.sin(2 * math.pi * pitch * 1.5 * t) + 0.1 * random.uniform(-1, 1))))))
            self._write_stereo_wav_file(d_samples, fp_danger)

    def _play_android_file(self, fp, loop=False, slot="fx"):
        if not self._jnius_mp or not os.path.exists(fp):
            return False
        try:
            mp = self._jnius_mp()
            mp.setDataSource(fp)
            mp.setLooping(loop)
            mp.prepare()
            mp.start()
            if slot == "bg":
                self.android_bg = mp
            elif slot == "menu":
                self.android_menu = mp
            return True
        except Exception:
            return False

    def start_menu_bgm(self):
        if not self.enabled or not self.menu_bgm_enabled:
            return
        fp = self._find_custom_audio("menu_bgm", "menu_theme")
        if fp is None:
            self.install_menu_bgm_pack()
            fp = os.path.join(PACKS_DIR, "menu_bgm", "menu_theme.wav")
        if self._jnius_mp:
            if self.android_menu is None:
                self._play_android_file(fp, loop=True, slot="menu")
            return
        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(fp)
                pygame.mixer.music.set_volume(0.42)
                pygame.mixer.music.play(-1)
        except Exception:
            if "menu_bgm" in self.sounds and (self.menu_channel is None or not self.menu_channel.get_busy()):
                try:
                    self.menu_channel = self.sounds["menu_bgm"].play(loops=-1)
                except Exception:
                    pass

    def stop_menu_bgm(self):
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        if self.menu_channel:
            try:
                self.menu_channel.stop()
            except Exception:
                pass
        if self.android_menu:
            try:
                self.android_menu.stop()
                self.android_menu.release()
            except Exception:
                pass
            self.android_menu = None

    def start_bg(self):
        if not self.enabled or not self.bg_enabled:
            return
        fp = self._find_custom_audio("bg_crowd", "crowd_loop")
        if fp is None:
            self.install_bg_pack()
            fp = os.path.join(PACKS_DIR, "bg_crowd", "crowd_loop.wav")
        if self._jnius_mp:
            self._play_android_file(fp, loop=True, slot="bg")
            return
        if "bg_loop" in self.sounds:
            try:
                if self.bg_channel is None or not self.bg_channel.get_busy():
                    self.bg_channel = self.sounds["bg_loop"].play(loops=-1)
                return
            except Exception:
                pass

    def stop_bg(self):
        if self.bg_channel:
            try:
                self.bg_channel.stop()
            except Exception:
                pass
        if self.android_bg:
            try:
                self.android_bg.stop()
                self.android_bg.release()
            except Exception:
                pass
            self.android_bg = None

    def play(self, name):
        if not self.enabled:
            return
        if self._jnius_mp and name in self.paths:
            if self._play_android_file(self.paths[name], loop=False):
                return
        if name in self.sounds:
            try:
                self.sounds[name].play()
                return
            except Exception:
                pass

    def play_commentary_goal(self):
        self.play("net")
        self.play("goal")
        fp = self._find_custom_audio(f"commentary_{self.commentary_lang}", "goal")
        if self.enabled and fp:
            if self._jnius_mp:
                self._play_android_file(fp, loop=False)
                return
            try:
                pygame.mixer.Sound(fp).play()
            except Exception:
                pass

    def play_commentary_danger(self):
        if not self.enabled:
            return
        fp = self._find_custom_audio("commentary_hafid", "danger")
        if fp is None:
            self.generate_commentary_pack_files("hafid")
            fp = os.path.join(PACKS_DIR, "commentary_hafid", "danger.wav")
        if self._jnius_mp:
            self._play_android_file(fp, loop=False)
            return
        try:
            pygame.mixer.Sound(fp).play()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# NETWORKING (ROOM SYSTEM)
# ---------------------------------------------------------------------------
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def encode_room_code(ip, port=DEFAULT_PORT):
    try:
        parts = [int(p) for p in ip.split(".")]
        if len(parts) == 4 and all(0 <= p <= 255 for p in parts):
            code = "".join(f"{p:02X}" for p in parts)
            return f"{code}-{port}" if port != DEFAULT_PORT else code
    except Exception:
        pass
    return f"{ip}:{port}"


def decode_room_code(text):
    text = text.strip()
    if not text:
        return None, DEFAULT_PORT
    if ":" in text:
        host, port_s = text.split(":", 1)
        try:
            return host.strip(), int(port_s.strip())
        except ValueError:
            return host.strip(), DEFAULT_PORT
    port, code = DEFAULT_PORT, text
    if "-" in text:
        code, port_s = text.split("-", 1)
        try:
            port = int(port_s.strip())
        except ValueError:
            port = DEFAULT_PORT
    if len(code) == 8:
        try:
            return ".".join(str(int(code[i : i + 2], 16)) for i in range(0, 8, 2)), port
        except ValueError:
            pass
    return text, port


class RoomNetwork:
    def __init__(self):
        self.role = None
        self.server_sock = None
        self.conn = None
        self.connected = False
        self.error = ""
        self.room_code = ""
        self.local_ip = get_local_ip()
        self.port = DEFAULT_PORT
        self.lock = threading.Lock()
        self.latest_remote_input = {"ax": 0.0, "ay": 0.0, "shoot": False, "shoot_type": "normal", "pass": False, "pass_type": "ground", "sprint": False, "switch": False}
        self.latest_state = None
        self.running = False
        self._recv_buffer = b""

    def start_host(self, port=DEFAULT_PORT):
        self.close()
        self.role, self.port = "host", port
        self.local_ip = get_local_ip()
        self.room_code = encode_room_code(self.local_ip, port)
        self.error, self.running = "", True
        try:
            self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_sock.bind(("0.0.0.0", port))
            self.server_sock.listen(1)
            self.server_sock.settimeout(0.5)
            threading.Thread(target=self._accept_loop, daemon=True).start()
            return True
        except Exception as e:
            self.error, self.running = f"Host error: {e}", False
            return False

    def _accept_loop(self):
        while self.running and not self.connected:
            try:
                conn, _ = self.server_sock.accept()
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                conn.settimeout(0.05)
                self.conn, self.connected = conn, True
                threading.Thread(target=self._recv_loop, daemon=True).start()
                break
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    self.error = str(e)
                break

    def join_room(self, code_or_ip):
        self.close()
        self.role = "client"
        host, port = decode_room_code(code_or_ip)
        if not host:
            self.error = "Invalid Room Code or IP"
            return False
        self.error, self.running = "", True
        threading.Thread(target=self._connect_thread, args=(host, port), daemon=True).start()
        return True

    def _connect_thread(self, host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4.0)
            sock.connect((host, port))
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sock.settimeout(0.05)
            self.conn, self.connected = sock, True
            self._recv_loop()
        except Exception as e:
            self.error, self.connected, self.running = f"Could not connect: {e}", False, False

    def _recv_loop(self):
        while self.running and self.connected:
            try:
                data = self.conn.recv(8192)
                if not data:
                    self.connected, self.error = False, "Opponent disconnected"
                    break
                self._recv_buffer += data
                while b"\n" in self._recv_buffer:
                    line, self._recv_buffer = self._recv_buffer.split(b"\n", 1)
                    if not line:
                        continue
                    try:
                        msg = json.loads(line.decode("utf-8"))
                        with self.lock:
                            if self.role == "host":
                                self.latest_remote_input = msg
                            else:
                                self.latest_state = msg
                    except Exception:
                        pass
            except socket.timeout:
                continue
            except Exception:
                self.connected, self.error = False, "Connection lost"
                break

    def send_json(self, obj):
        if not self.connected or not self.conn:
            return
        try:
            self.conn.sendall((json.dumps(obj, separators=(",", ":")) + "\n").encode("utf-8"))
        except Exception:
            self.connected, self.error = False, "Connection lost"

    def get_remote_input(self):
        with self.lock:
            return dict(self.latest_remote_input)

    def get_latest_state(self):
        with self.lock:
            return self.latest_state

    def close(self):
        self.running = self.connected = False
        for s in (self.conn, self.server_sock):
            if s:
                try:
                    s.close()
                except Exception:
                    pass
        self.conn = self.server_sock = None
        self._recv_buffer = b""


# ---------------------------------------------------------------------------
# TRUE MULTI-TOUCH CONTROLS
# ---------------------------------------------------------------------------
class TouchControls:
    def __init__(self, font_xs):
        self.joy_center = (135, HEIGHT - 125)
        self.joy_radius = 68
        self.knob_pos = list(self.joy_center)
        self.joy_finger = None

        self.btn_shoot = (WIDTH - 105, HEIGHT - 115, 48)
        self.btn_pass = (WIDTH - 220, HEIGHT - 100, 44)
        self.btn_sprint = (WIDTH - 195, HEIGHT - 210, 34)
        self.btn_switch = (WIDTH - 95, HEIGHT - 230, 34)

        self.active_fingers = {}
        self.using_touch = False
        self.mouse_down = False
        self.mouse_pos = (0, 0)

        self.shoot_finger = None
        self.shoot_start = None
        self.shoot_gesture = "normal"
        self.pass_finger = None
        self.pass_start = None
        self.pass_gesture = "ground"

        r = self.joy_radius + 4
        self._joy_base_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(self._joy_base_surf, (255, 255, 255, 45), (r, r), self.joy_radius)
        pygame.draw.circle(self._joy_base_surf, (255, 255, 255, 110), (r, r), self.joy_radius, 3)

        self._knob_surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(self._knob_surf, (0, 230, 255, 180), (30, 30), 26)

        self._btn_surfs = {}
        for key, btn, label, sub, col in [
            ("shoot", self.btn_shoot, "SHOOT", "v R2  <> PWR", (255, 205, 50)),
            ("pass", self.btn_pass, "PASS", "^ LOFT", (0, 220, 255)),
            ("sprint", self.btn_sprint, "RUN", "", (46, 204, 113)),
            ("switch", self.btn_switch, "SWITCH", "", (185, 120, 255)),
        ]:
            br = btn[2]
            sz = (br + 4) * 2
            idle = pygame.Surface((sz, sz), pygame.SRCALPHA)
            active = pygame.Surface((sz, sz), pygame.SRCALPHA)
            txt = font_xs.render(label, True, WHITE)
            sub_t = font_xs.render(sub, True, WHITE) if sub else None
            for surf, alpha in ((idle, 95), (active, 195)):
                pygame.draw.circle(surf, (*col, alpha), (br + 4, br + 4), br)
                pygame.draw.circle(surf, (255, 255, 255, 185), (br + 4, br + 4), br, 2)
                if sub_t:
                    surf.blit(txt, txt.get_rect(center=(br + 4, br - 3)))
                    surf.blit(sub_t, sub_t.get_rect(center=(br + 4, br + 13)))
                else:
                    surf.blit(txt, txt.get_rect(center=(br + 4, br + 4)))
            self._btn_surfs[key] = (btn, idle, active)

    def _detect_shoot_gesture(self, sx, sy, cx, cy):
        dx, dy = cx - sx, cy - sy
        if dy > 20 and dy > abs(dx):
            return "curler"
        if abs(dx) > 20:
            return "power"
        return "normal"

    def _detect_pass_gesture(self, sx, sy, cx, cy):
        return "lofted" if (sy - cy > 20) else "ground"

    def handle_event(self, event):
        if event.type == pygame.FINGERDOWN:
            self.using_touch = True
            x, y = event.x * WIDTH, event.y * HEIGHT
            self.active_fingers[event.finger_id] = (x, y)
            if x < WIDTH * 0.48 and y > TOP_HUD + 30 and self.joy_finger is None:
                self.joy_finger = event.finger_id
                self._update_knob(x, y)
            elif math.hypot(x - self.btn_shoot[0], y - self.btn_shoot[1]) <= self.btn_shoot[2] + 22:
                self.shoot_finger = event.finger_id
                self.shoot_start = (x, y)
                self.shoot_gesture = "normal"
            elif math.hypot(x - self.btn_pass[0], y - self.btn_pass[1]) <= self.btn_pass[2] + 22:
                self.pass_finger = event.finger_id
                self.pass_start = (x, y)
                self.pass_gesture = "ground"
        elif event.type == pygame.FINGERMOTION:
            x, y = event.x * WIDTH, event.y * HEIGHT
            self.active_fingers[event.finger_id] = (x, y)
            if event.finger_id == self.joy_finger:
                self._update_knob(x, y)
            elif event.finger_id == self.shoot_finger and self.shoot_start:
                self.shoot_gesture = self._detect_shoot_gesture(*self.shoot_start, x, y)
            elif event.finger_id == self.pass_finger and self.pass_start:
                self.pass_gesture = self._detect_pass_gesture(*self.pass_start, x, y)
        elif event.type == pygame.FINGERUP:
            self.active_fingers.pop(event.finger_id, None)
            if event.finger_id == self.joy_finger:
                self.joy_finger = None
                self.knob_pos = list(self.joy_center)
            elif event.finger_id == self.shoot_finger:
                self.shoot_finger = None
            elif event.finger_id == self.pass_finger:
                self.pass_finger = None
        elif not self.using_touch:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_down = True
                self.mouse_pos = event.pos
                x, y = event.pos
                if math.hypot(x - self.joy_center[0], y - self.joy_center[1]) <= self.joy_radius * 2.1:
                    self._update_knob(x, y)
                elif math.hypot(x - self.btn_shoot[0], y - self.btn_shoot[1]) <= self.btn_shoot[2] + 18:
                    self.shoot_start = (x, y)
                    self.shoot_gesture = "normal"
                elif math.hypot(x - self.btn_pass[0], y - self.btn_pass[1]) <= self.btn_pass[2] + 18:
                    self.pass_start = (x, y)
                    self.pass_gesture = "ground"
            elif event.type == pygame.MOUSEMOTION and self.mouse_down:
                self.mouse_pos = event.pos
                x, y = event.pos
                if math.hypot(x - self.joy_center[0], y - self.joy_center[1]) <= self.joy_radius * 2.6:
                    self._update_knob(x, y)
                if self.shoot_start:
                    self.shoot_gesture = self._detect_shoot_gesture(*self.shoot_start, x, y)
                if self.pass_start:
                    self.pass_gesture = self._detect_pass_gesture(*self.pass_start, x, y)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.mouse_down = False
                self.knob_pos = list(self.joy_center)
                self.shoot_start = None
                self.pass_start = None

    def _update_knob(self, x, y):
        dx, dy = x - self.joy_center[0], y - self.joy_center[1]
        d = math.hypot(dx, dy)
        if d > self.joy_radius:
            dx, dy = dx / d * self.joy_radius, dy / d * self.joy_radius
        self.knob_pos = [self.joy_center[0] + dx, self.joy_center[1] + dy]

    def _is_btn_pressed(self, btn):
        bx, by, br = btn
        for fx, fy in self.active_fingers.values():
            if math.hypot(fx - bx, fy - by) <= br + 20:
                return True
        if not self.using_touch and self.mouse_down and math.hypot(self.mouse_pos[0] - bx, self.mouse_pos[1] - by) <= br + 18:
            return True
        return False

    def get_input(self):
        dx = (self.knob_pos[0] - self.joy_center[0]) / self.joy_radius
        dy = (self.knob_pos[1] - self.joy_center[1]) / self.joy_radius
        if math.hypot(dx, dy) < 0.12:
            dx, dy = 0.0, 0.0
        shoot_pressed = (self.shoot_finger is not None) or self._is_btn_pressed(self.btn_shoot)
        pass_pressed = (self.pass_finger is not None) or self._is_btn_pressed(self.btn_pass)
        return {"ax": dx, "ay": dy, "shoot": shoot_pressed, "shoot_type": self.shoot_gesture, "pass": pass_pressed, "pass_type": self.pass_gesture, "sprint": self._is_btn_pressed(self.btn_sprint), "switch": self._is_btn_pressed(self.btn_switch)}

    def draw(self, screen):
        r = self.joy_radius + 4
        screen.blit(self._joy_base_surf, (self.joy_center[0] - r, self.joy_center[1] - r))
        screen.blit(self._knob_surf, (int(self.knob_pos[0]) - 30, int(self.knob_pos[1]) - 30))
        for btn, idle, active in self._btn_surfs.values():
            bx, by, br = btn
            screen.blit(active if self._is_btn_pressed(btn) else idle, (bx - br - 4, by - br - 4))


# ---------------------------------------------------------------------------
# CAREER, FULL LEAGUE SIMULATION, UCL KNOCKOUT, TOP SCORERS & BALLON D'OR
# ---------------------------------------------------------------------------
class CareerManager:
    def __init__(self):
        self.coins = 5000
        self.trophies = 0
        self.league_titles = 0
        self.ucl_titles = 0
        self.ballon_dors = 0
        self.owned = ["salah", "hakimi", "ronaldo", "bellingham", "yamal", "kane", "raya", "saliba", "pedri", "vitinha"]
        self.card_types = {pid: "STANDARD" for pid in self.owned}
        self.lineup = ["ronaldo", "salah", "bellingham", "hakimi", "yamal"]
        self.gk_id = "raya"
        self.bench = ["kane", "pedri", "saliba", "vitinha"]
        self.goals_by_id = {c["id"]: 0 for c in PLAYER_CATALOG}
        self.league_scorers = {}
        self.ucl_scorers = {}
        self.custom_stats = {}
        self.custom_offsets = {}
        self.last_pack_date = ""
        self.manager_idx = 0
        self.formation_idx = 0
        self.smart_assist = True
        self.installed_packs = {
            "stadium_hd": False,
            "bg_crowd": False,
            "menu_bgm": False,
            "commentary_hafid": False,
            "commentary_spanish": False,
            "player_photos": False,
        }
        self.league_teams = [
            "Your Club", "Real Madrid", "Man City", "FC Barcelona",
            "Bayern Munich", "Arsenal", "Liverpool", "PSG", "Inter Milan",
        ]
        self.league_round = 0
        self.league_table = self._fresh_league_table()

        # Champions League Knockout State (No Group Stage — Knockout Only!)
        self.ucl_active = False
        self.ucl_round_name = "Knockout Playoff"
        self.ucl_matches = []  # list of [teamA, teamB]
        self.ucl_byes = []     # teams with bye in Playoff
        self.ucl_eliminated = False
        self.ucl_champion = None

        self.load()

    def _fresh_league_table(self):
        return {t: {"p": 0, "w": 0, "d": 0, "l": 0, "gf": 0, "ga": 0, "pts": 0} for t in self.league_teams}

    def get_current_league_opponent(self):
        opps = self.league_teams[1:]
        return opps[self.league_round % len(opps)]

    def get_your_league_rank(self):
        for idx, row in enumerate(self.get_standings()):
            if row[0] == "Your Club":
                return idx + 1
        return 9

    def _sim_ai_match(self, club_a, club_b, scorer_dict):
        ra = CLUBS_DATA[club_a]["rating"] if club_a in CLUBS_DATA else 85
        rb = CLUBS_DATA[club_b]["rating"] if club_b in CLUBS_DATA else 85
        diff = (ra - rb) * 0.08
        ga = max(0, min(5, int(random.gauss(1.4 + diff, 1.0))))
        gb = max(0, min(5, int(random.gauss(1.4 - diff, 1.0))))
        for club, goals in ((club_a, ga), (club_b, gb)):
            if club in CLUBS_DATA and goals > 0:
                attackers = CLUBS_DATA[club]["lineup"][:3]
                for _ in range(goals):
                    pid = random.choice(attackers)
                    scorer_dict[pid] = scorer_dict.get(pid, 0) + 1
        return ga, gb

    def record_league_match(self, gf, ga):
        opp = self.get_current_league_opponent()
        self._apply_table_result("Your Club", opp, gf, ga)

        # Simulate ALL OTHER TEAMS playing in this round!
        others = [t for t in self.league_teams if t not in ("Your Club", opp)]
        random.shuffle(others)
        for i in range(0, len(others) - 1, 2):
            ca, cb = others[i], others[i + 1]
            sa, sb = self._sim_ai_match(ca, cb, self.league_scorers)
            self._apply_table_result(ca, cb, sa, sb)

        self.league_round += 1
        champ_bonus = 0
        won_league = False
        total_rounds = len(self.league_teams) - 1
        if self.league_round >= total_rounds:
            standings = self.get_standings()
            if standings[0][0] == "Your Club":
                won_league = True
                self.trophies += 1
                self.league_titles += 1
                champ_bonus = 2500
                self.coins += champ_bonus
            # Check if Top 6 qualified for UCL!
            top6 = [r[0] for r in standings[:6]]
            if "Your Club" in top6 and not self.ucl_active:
                self.start_ucl_from_top6(top6)
            self.league_round = 0
            self.league_table = self._fresh_league_table()
        self.save()
        return champ_bonus, won_league

    def _apply_table_result(self, ca, cb, ga, gb):
        ta, tb = self.league_table[ca], self.league_table[cb]
        ta["p"] += 1
        tb["p"] += 1
        ta["gf"] += ga
        ta["ga"] += gb
        tb["gf"] += gb
        tb["ga"] += ga
        if ga > gb:
            ta["w"] += 1
            ta["pts"] += 3
            tb["l"] += 1
        elif ga == gb:
            ta["d"] += 1
            ta["pts"] += 1
            tb["d"] += 1
            tb["pts"] += 1
        else:
            ta["l"] += 1
            tb["w"] += 1
            tb["pts"] += 3

    def start_ucl_from_top6(self, top6=None):
        if top6 is None:
            top6 = [r[0] for r in self.get_standings()[:6]]
        if "Your Club" not in top6:
            return False, "Reach Top 6 in League to qualify for Champions League!"
        # 6 League Top Teams + 6 Foreign League Teams (2 each from Serie A, Bundesliga, Saudi Pro) = 12 Teams!
        # Pure Knockout Only: Top 4 League seeds get bye to QF; Seeds 5-6 + 6 Foreign Clubs play Knockout Playoff!
        self.ucl_active = True
        self.ucl_eliminated = False
        self.ucl_champion = None
        self.ucl_scorers = {}
        self.ucl_round_name = "Knockout Playoff"
        self.ucl_byes = list(top6[:4])
        playoff_pool = list(top6[4:6]) + list(FOREIGN_UCL_CLUBS)
        random.shuffle(playoff_pool)
        self.ucl_matches = [[playoff_pool[i], playoff_pool[i + 1]] for i in range(0, len(playoff_pool), 2)]
        self.save()
        return True, "Champions League Knockout Started!"

    def get_your_ucl_match(self):
        for pair in self.ucl_matches:
            if "Your Club" in pair:
                return pair[1] if pair[0] == "Your Club" else pair[0]
        return None

    def get_ucl_difficulty(self):
        return {"Knockout Playoff": 1, "Quarter-Finals": 2, "Semi-Finals": 3, "Final": 4}.get(self.ucl_round_name, 2)

    def advance_ucl_round(self, your_gf=0, your_ga=0):
        # Resolve all current UCL knockout matches (no draws allowed — penalties decide ties!)
        winners = list(self.ucl_byes)
        self.ucl_byes = []
        won_ucl = False
        champ_bonus = 0

        for ca, cb in self.ucl_matches:
            if "Your Club" in (ca, cb):
                win_team = "Your Club" if your_gf > your_ga else (cb if ca == "Your Club" else ca)
                if win_team != "Your Club":
                    self.ucl_eliminated = True
                winners.append(win_team)
            else:
                sa, sb = self._sim_ai_match(ca, cb, self.ucl_scorers)
                if sa == sb:
                    sa += random.choice([0, 1])
                    if sa == sb:
                        sb += 1
                winners.append(ca if sa > sb else cb)

        if len(winners) == 1:
            self.ucl_champion = winners[0]
            self.ucl_active = False
            if self.ucl_champion == "Your Club":
                won_ucl = True
                self.trophies += 1
                self.ucl_titles += 1
                champ_bonus = 4000
                self.coins += champ_bonus
        elif self.ucl_eliminated:
            self.ucl_active = False
        else:
            random.shuffle(winners)
            self.ucl_matches = [[winners[i], winners[i + 1]] for i in range(0, len(winners), 2)]
            if len(winners) == 8:
                self.ucl_round_name = "Quarter-Finals"
            elif len(winners) == 4:
                self.ucl_round_name = "Semi-Finals"
            elif len(winners) == 2:
                self.ucl_round_name = "Final"
        self.save()
        return champ_bonus, won_ucl

    def get_ballon_dor_top10(self):
        board = []
        your_set = set(self.lineup + [self.gk_id] + self.bench)
        for c in PLAYER_CATALOG:
            if c.get("is_base") or c["pos"] == "GK":
                continue
            pid = c["id"]
            st = self.get_card_stats(pid)
            lg = self.league_scorers.get(pid, 0)
            ug = self.ucl_scorers.get(pid, 0)
            trophy_pts = (self.league_titles * 4 + self.ucl_titles * 7) if pid in your_set else 0
            score = st["ovr"] + lg * 3 + ug * 5 + trophy_pts
            board.append((pid, st["short"], st["club"], st["ovr"], lg, ug, score))
        board.sort(key=lambda r: r[6], reverse=True)
        return board[:10]

    @property
    def manager(self):
        return MANAGERS[self.manager_idx]

    @property
    def formation(self):
        return FORMATIONS[self.formation_idx]

    def get_slot_offset(self, idx):
        if str(idx) in self.custom_offsets:
            return tuple(self.custom_offsets[str(idx)])
        return self.formation["offsets"][idx]

    def get_reserves(self):
        used = set(self.lineup + [self.gk_id] + self.bench)
        return [pid for pid in self.owned if pid not in used]

    def get_team_strength(self):
        return sum(self.get_card_stats(pid)["ovr"] for pid in (self.lineup + [self.gk_id] + self.bench)) * 3 + 500

    def get_card_stats(self, pid):
        base = CATALOG_BY_ID[pid]
        ctype = self.card_types.get(pid, "BASE" if base.get("is_base") else "STANDARD")
        goals = self.goals_by_id.get(pid, 0)
        lvl = goals // 2
        mgr = self.manager
        cust = self.custom_stats.get(pid, {})

        max_ovr = 105 if ctype == "EPIC" else 99
        booster_val = 3 if ctype == "EPIC" else (2 if ctype == "HIGHLIGHT" else 0)

        pac = min(max_ovr, max(40, cust.get("pac", base["pac"]) + lvl + mgr["pac"] + booster_val))
        sho = min(max_ovr, max(40, cust.get("sho", base["sho"]) + lvl * 2 + mgr["sho"] + booster_val))
        pas = min(max_ovr, max(40, cust.get("pas", base["pas"]) + lvl + mgr["pas"] + booster_val))
        dri = min(max_ovr, max(40, cust.get("dri", base["dri"]) + lvl + mgr["dri"] + booster_val))

        stat_map = {"pac": pac, "sho": sho, "pas": pas, "dri": dri}
        mgr_ovr = 2 if mgr["key"] == "all" else (3 if stat_map.get(mgr["key"], 0) >= mgr["req"] else 1)
        ovr = min(max_ovr, base["ovr"] + lvl + booster_val + mgr_ovr)

        skills = list(base["skills"]) if ctype == "EPIC" else ([base["skills"][0]] if (ctype == "HIGHLIGHT" and base["skills"]) else [])
        return {
            **base,
            "card_type": ctype,
            "is_epic": ctype == "EPIC",
            "booster": base["booster"] if ctype in ("EPIC", "HIGHLIGHT") else None,
            "skills": skills,
            "goals": goals, "level": 1 + lvl,
            "ovr": ovr, "pac": pac, "sho": sho, "pas": pas, "dri": dri,
        }

    def swap_squad_slots(self, slot_a, slot_b):
        def get_pid(slot):
            kind, val = slot
            if kind == "pitch":
                return self.lineup[val]
            if kind == "gk":
                return self.gk_id
            if kind == "bench":
                return self.bench[val]
            return val

        def set_pid(slot, pid):
            kind, val = slot
            if kind == "pitch":
                self.lineup[val] = pid
            elif kind == "gk":
                self.gk_id = pid
            elif kind == "bench":
                self.bench[val] = pid

        pa, pb = get_pid(slot_a), get_pid(slot_b)
        if pa == pb:
            return
        if slot_a[0] != "res" and slot_b[0] != "res":
            set_pid(slot_a, pb)
            set_pid(slot_b, pa)
        elif slot_a[0] == "res":
            set_pid(slot_b, pa)
        elif slot_b[0] == "res":
            set_pid(slot_a, pb)
        self.save()

    def adjust_custom_stat(self, pid, stat_key, delta):
        base_val = self.custom_stats.get(pid, {}).get(stat_key, CATALOG_BY_ID[pid][stat_key])
        new_val = max(40, min(99, base_val + delta))
        if pid not in self.custom_stats:
            self.custom_stats[pid] = {}
        self.custom_stats[pid][stat_key] = new_val
        self.save()

    def is_pack_day(self):
        return datetime.datetime.now().weekday() in (0, 3)

    def open_10_pack(self, use_coins=False):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        if not use_coins:
            if not self.is_pack_day():
                return None, "Free Pack is Mon & Thu! (Or open for 1,000 Coins)"
            if self.last_pack_date == today:
                return None, "Already claimed today's Free Pack! (Or open for 1,000 Coins)"
            self.last_pack_date = today
        else:
            if self.coins < 1000:
                return None, "Need 1,000 Coins to open Pack!"
            self.coins -= 1000

        pull = random.choice(PACK_POOL_10)
        pid, rarity = pull["pid"], pull["rarity"]
        self.card_types[pid] = rarity
        if pid not in self.owned:
            self.owned.append(pid)
            msg = f"PULLED {rarity}: {CATALOG_BY_ID[pid]['short']}! Added to Reserves."
        else:
            bonus = 1200 if rarity == "EPIC" else 350
            self.coins += bonus
            msg = f"Duplicate {CATALOG_BY_ID[pid]['short']} -> +{bonus} Coins!"
        self.save()
        return {"pid": pid, "rarity": rarity, "msg": msg}, msg

    def download_pack(self, pack_key, sound_bank):
        os.makedirs(PACKS_DIR, exist_ok=True)
        sub = os.path.join(PACKS_DIR, pack_key)
        os.makedirs(sub, exist_ok=True)
        if pack_key == "bg_crowd":
            sound_bank.install_bg_pack()
        elif pack_key == "menu_bgm":
            sound_bank.install_menu_bgm_pack()
            sound_bank.start_menu_bgm()
        elif pack_key == "commentary_hafid":
            sound_bank.generate_commentary_pack_files("hafid")
        elif pack_key == "commentary_spanish":
            sound_bank.generate_commentary_pack_files("spanish")
        with open(os.path.join(sub, "pack_manifest.json"), "w", encoding="utf-8") as f:
            json.dump({"pack": pack_key, "installed_at": time.time()}, f, indent=2)
        self.installed_packs[pack_key] = True
        self.save()
        return f"Installed & Activated: {pack_key}!"

    def buy_player(self, pid):
        if pid in self.owned:
            return False, "Already owned!"
        price = CATALOG_BY_ID[pid]["price"]
        if self.coins < price:
            return False, "Not enough coins!"
        self.coins -= price
        self.owned.append(pid)
        self.card_types[pid] = "BASE" if CATALOG_BY_ID[pid].get("is_base") else "STANDARD"
        self.save()
        return True, f"Signed {CATALOG_BY_ID[pid]['short']}! Check Game Plan Reserves."

    def sell_player(self, pid):
        if pid not in self.owned or len(self.owned) <= 10:
            return False, "Need at least 10 players (6 Pitch + 4 Bench)!"
        refund = int(CATALOG_BY_ID[pid]["price"] * 0.7)
        self.coins += refund
        self.owned.remove(pid)
        res = self.get_reserves()
        if pid in self.lineup and res:
            self.lineup[self.lineup.index(pid)] = res[0]
        elif pid in self.bench and res:
            self.bench[self.bench.index(pid)] = res[0]
        elif pid == self.gk_id and res:
            self.gk_id = res[0]
        self.save()
        return True, f"Sold for +{refund} Coins"

    def record_goal(self, pid, mode="ai"):
        if pid in self.goals_by_id:
            self.goals_by_id[pid] += 1
        if mode == "league":
            self.league_scorers[pid] = self.league_scorers.get(pid, 0) + 1
        elif mode == "ucl":
            self.ucl_scorers[pid] = self.ucl_scorers.get(pid, 0) + 1
        self.save()

    def get_standings(self):
        rows = [(name, st["p"], st["w"], st["d"], st["l"], st["gf"] - st["ga"], st["pts"]) for name, st in self.league_table.items()]
        rows.sort(key=lambda r: (r[6], r[5]), reverse=True)
        return rows

    def save(self):
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "coins": self.coins, "trophies": self.trophies,
                    "league_titles": self.league_titles, "ucl_titles": self.ucl_titles, "ballon_dors": self.ballon_dors,
                    "owned": self.owned, "card_types": self.card_types, "lineup": self.lineup, "gk_id": self.gk_id, "bench": self.bench,
                    "goals_by_id": self.goals_by_id, "league_scorers": self.league_scorers, "ucl_scorers": self.ucl_scorers,
                    "custom_stats": self.custom_stats, "custom_offsets": self.custom_offsets,
                    "last_pack_date": self.last_pack_date, "installed_packs": self.installed_packs,
                    "manager_idx": self.manager_idx, "formation_idx": self.formation_idx,
                    "smart_assist": self.smart_assist, "league_round": self.league_round, "league_table": self.league_table,
                    "ucl_active": self.ucl_active, "ucl_round_name": self.ucl_round_name, "ucl_matches": self.ucl_matches,
                    "ucl_byes": self.ucl_byes, "ucl_eliminated": self.ucl_eliminated, "ucl_champion": self.ucl_champion,
                }, f, indent=2)
        except Exception:
            pass

    def load(self):
        if not os.path.exists(SAVE_FILE):
            return
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.coins = int(data.get("coins", 5000))
            self.trophies = int(data.get("trophies", 0))
            self.league_titles = int(data.get("league_titles", 0))
            self.ucl_titles = int(data.get("ucl_titles", 0))
            self.ballon_dors = int(data.get("ballon_dors", 0))
            owned = [p for p in data.get("owned", []) if p in CATALOG_BY_ID]
            if len(owned) >= 10:
                self.owned = owned
            self.card_types.update(data.get("card_types", {}))
            lineup = [p for p in data.get("lineup", []) if p in self.owned]
            if len(lineup) == 5:
                self.lineup = lineup
            if data.get("gk_id") in self.owned:
                self.gk_id = data["gk_id"]
            bench = [p for p in data.get("bench", []) if p in self.owned]
            if len(bench) == 4:
                self.bench = bench
            for k, v in data.get("goals_by_id", {}).items():
                if k in self.goals_by_id:
                    self.goals_by_id[k] = int(v)
            self.league_scorers = data.get("league_scorers", {})
            self.ucl_scorers = data.get("ucl_scorers", {})
            self.custom_stats = data.get("custom_stats", {})
            self.custom_offsets = data.get("custom_offsets", {})
            self.last_pack_date = data.get("last_pack_date", "")
            self.installed_packs.update(data.get("installed_packs", {}))
            self.manager_idx = int(data.get("manager_idx", 0)) % len(MANAGERS)
            self.formation_idx = int(data.get("formation_idx", 0)) % len(FORMATIONS)
            self.smart_assist = bool(data.get("smart_assist", True))
            self.league_round = int(data.get("league_round", 0)) % max(1, len(self.league_teams) - 1)
            lt = data.get("league_table")
            if isinstance(lt, dict):
                for t in self.league_teams:
                    if t in lt:
                        self.league_table[t] = lt[t]
            self.ucl_active = bool(data.get("ucl_active", False))
            self.ucl_round_name = data.get("ucl_round_name", "Knockout Playoff")
            self.ucl_matches = data.get("ucl_matches", [])
            self.ucl_byes = data.get("ucl_byes", [])
            self.ucl_eliminated = bool(data.get("ucl_eliminated", False))
            self.ucl_champion = data.get("ucl_champion", None)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# GAME ENTITIES
# ---------------------------------------------------------------------------
class Player:
    def __init__(self, x, y, home_x, home_y, color, team, card_id, stats, is_gk=False):
        self.x, self.y = float(x), float(y)
        self.home_x, self.home_y = float(home_x), float(home_y)
        self.vx = self.vy = 0.0
        self.color, self.team, self.card_id, self.stats, self.is_gk = color, team, card_id, stats, is_gk
        self.facing_x = 1.0 if team == 1 else -1.0
        self.facing_y = 0.0
        self.stamina, self.charge, self.charging, self.shoot_type = 100.0, 0.0, False, "normal"
        self.gk_hold_timer = 0.0
        self.ai_shoot_timer = 0.0
        self.ai_shoot_type = "normal"

    def reset(self):
        self.x, self.y = self.home_x, self.home_y
        self.vx = self.vy = self.charge = self.gk_hold_timer = self.ai_shoot_timer = 0.0
        self.charging = False
        self.stamina = 100.0
        self.facing_x, self.facing_y = (1.0 if self.team == 1 else -1.0), 0.0


class Ball:
    def __init__(self):
        self.x, self.y, self.z = float(PITCH_CX), float(PITCH_CY), 0.0
        self.vx = self.vy = self.vz = self.curve = 0.0
        self.spin_angle = 0.0
        self.owner = None
        self.steal_cd = 0.0
        self.trail = []
        self.trail_color = (220, 220, 230)
        self.last_touch_team = 0
        self.last_touch_id = None

    def reset(self):
        self.x, self.y, self.z = float(PITCH_CX), float(PITCH_CY), 0.0
        self.vx = self.vy = self.vz = self.curve = 0.0
        self.spin_angle = 0.0
        self.owner = None
        self.steal_cd = 0.0
        self.trail.clear()


class Particle:
    def __init__(self, x, y, vx, vy, color, life, size=4):
        self.x, self.y, self.vx, self.vy, self.color, self.life, self.size = x, y, vx, vy, color, life, size


class ImpactRing:
    def __init__(self, x, y, color, max_r=36, life=0.28):
        self.x, self.y, self.color, self.max_r, self.life, self.max_life = x, y, color, max_r, life, life


# ---------------------------------------------------------------------------
# MAIN GAME APPLICATION
# ---------------------------------------------------------------------------
class FootballGame:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 4096)
        pygame.init()
        pygame.display.set_caption("STRIKER ARENA 6v6 — eFootball Pro")
        flags = pygame.SCALED if hasattr(pygame, "SCALED") else 0
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        self.clock = pygame.time.Clock()
        self.sound = SoundBank()
        self.net = RoomNetwork()
        self.career = CareerManager()

        self.font_xl = pygame.font.SysFont("segoeui,arial,dejavusans", 46, bold=True)
        self.font_lg = pygame.font.SysFont("segoeui,arial,dejavusans", 28, bold=True)
        self.font_md = pygame.font.SysFont("segoeui,arial,dejavusans", 19, bold=True)
        self.font_sm = pygame.font.SysFont("segoeui,arial,dejavusans", 14, bold=True)
        self.font_xs = pygame.font.SysFont("segoeui,arial,dejavusans", 11, bold=True)

        self.touch = TouchControls(self.font_xs)
        self._pitch_cache = {}
        self._portrait_cache = {}
        self._text_cache = {}
        self._dim_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self._dim_overlay.fill((10, 14, 24, 200))
        self._goal_banner = pygame.Surface((WIDTH, 130), pygame.SRCALPHA)
        self._goal_banner.fill((12, 16, 28, 210))

        self.stadium_idx = 0
        self.match_duration = 120
        self.ai_difficulty = 1
        self.match_ai_difficulty = 2
        self.opponent_club_name = "CPU All-Stars"
        self.mode = "ai"
        self.camera_mode = "classic"
        self.cam_x, self.cam_y = PITCH_CX - WIDTH // 2, PITCH_CY - HEIGHT // 2
        self.auto_ai = False

        self.state = "MENU"
        self.join_input = ""
        self.market_msg = ""
        self.market_page = 0
        self.edit_pid = None
        self.selected_slot = None
        self.move_pos_mode = False
        self.reserves_open = False
        self.reserves_page = 0
        self.pending_reserve_pid = None
        self.gp_msg = ""
        self.pack_result = None
        self.pack_msg = ""
        self.dl_msg = ""
        self.ucl_msg = ""
        self.ceremony_title = ""
        self.ceremony_sub = ""
        self.ceremony_color = GOLD
        self.commentary_banner = ""
        self.commentary_timer = 0.0
        self.danger_cd = 0.0

        self.net_ripple_left = 0.0
        self.net_ripple_right = 0.0
        self.net_hit_y = float(PITCH_CY)
        self.post_flash_timer = 0.0
        self.post_flash_pos = None

        self.extra_time = False
        self.subs_used = 0
        self.max_subs = 2
        self.sub_selected_pitch = None
        self.pen_round = 1
        self.pen_score1 = self.pen_score2 = 0
        self.pen_turn = 1
        self.pen_msg = ""

        self.replay_buffer = []
        self.replay_frames = []
        self.replay_idx = 0.0
        self.in_replay = False
        self.celebration_timer = 0.0

        self.team1 = []
        self.team2 = []
        self.active1_idx = 0
        self.active2_idx = 0
        self.ball = Ball()

        self.score1 = self.score2 = 0
        self.time_left = float(self.match_duration)
        self.last_scorer_team = 0
        self.last_scorer_name = ""
        self.last_scorer_player = None
        self.match_reward = self.champ_bonus = 0
        self.particles = []
        self.impact_rings = []
        self.stats = {"shots1": 0, "shots2": 0, "passes1": 0, "passes2": 0}

        self._prev_p1_shoot = self._prev_p2_shoot = False
        self._prev_p1_pass = self._prev_p2_pass = False
        self._prev_p1_switch = self._prev_p2_switch = False
        self.buttons = {}

        self.sound.start_menu_bgm()

    @property
    def stadium(self):
        return STADIUMS[self.stadium_idx]

    def _get_portrait(self, pid):
        if pid in self._portrait_cache:
            return self._portrait_cache[pid]
        photos_dir = os.path.join(PACKS_DIR, "player_photos")
        for ext in (".png", ".jpg", ".jpeg"):
            fp = os.path.join(photos_dir, pid + ext)
            if os.path.exists(fp):
                try:
                    img = pygame.transform.smoothscale(pygame.image.load(fp).convert_alpha(), (64, 64))
                    self._portrait_cache[pid] = img
                    return img
                except Exception:
                    pass
        st = CATALOG_BY_ID[pid]
        surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        pygame.draw.circle(surf, (40, 50, 72), (32, 32), 30)
        pygame.draw.ellipse(surf, st["kit"], (10, 42, 44, 28))
        pygame.draw.rect(surf, st["skin"], (27, 36, 10, 10))
        pygame.draw.circle(surf, st["skin"], (32, 27), 14)
        pygame.draw.arc(surf, st["hair"], (17, 11, 30, 22), 0.1, math.pi - 0.1, 7)
        pygame.draw.circle(surf, BLACK, (27, 26), 2)
        pygame.draw.circle(surf, BLACK, (37, 26), 2)
        pygame.draw.circle(surf, GOLD, (32, 32), 30, 2)
        self._portrait_cache[pid] = surf
        return surf

    def draw_club_crest(self, cx, cy, scale=1.0):
        # Club Shield + Stars for League (Gold) & Champions League (Cyan)
        pts = [
            (cx - int(24 * scale), cy - int(22 * scale)),
            (cx + int(24 * scale), cy - int(22 * scale)),
            (cx + int(22 * scale), cy + int(8 * scale)),
            (cx, cy + int(28 * scale)),
            (cx - int(22 * scale), cy + int(8 * scale)),
        ]
        pygame.draw.polygon(self.screen, (20, 45, 115), pts)
        pygame.draw.polygon(self.screen, GOLD, pts, max(2, int(3 * scale)))
        pygame.draw.line(self.screen, CYAN, (cx, cy - int(18 * scale)), (cx, cy + int(22 * scale)), max(2, int(3 * scale)))
        self.draw_text("FC", self.font_sm if scale >= 1.0 else self.font_xs, WHITE, cx, cy)

        # Draw Stars above the crest
        stars = ([GOLD] * min(5, self.career.league_titles)) + ([CYAN] * min(5, self.career.ucl_titles))
        if stars:
            spacing = int(14 * scale)
            start_x = cx - ((len(stars) - 1) * spacing) // 2
            sy = cy - int(32 * scale)
            for idx, scol in enumerate(stars):
                sx = start_x + idx * spacing
                pygame.draw.circle(self.screen, scol, (sx, sy), max(4, int(5 * scale)))
                pygame.draw.circle(self.screen, WHITE, (sx, sy), max(2, int(2 * scale)))

    def _get_pitch_surface(self):
        idx = self.stadium_idx
        hd = self.career.installed_packs.get("stadium_hd", False)
        key = (idx, hd)
        if key in self._pitch_cache:
            return self._pitch_cache[key]
        st = STADIUMS[idx]
        surf = pygame.Surface((WORLD_W, WORLD_H)).convert()
        surf.fill(st["bg"])

        # Outer stadium stands & tiered walkways
        stand_rect = pygame.Rect(PITCH_X - 98, PITCH_Y - 78, PITCH_W + 196, PITCH_H + 156)
        pygame.draw.rect(surf, st["stands"], stand_rect, border_radius=28)

        # Stand aisles / stairways
        for ax in range(PITCH_X, PITCH_X + PITCH_W + 1, 240):
            pygame.draw.rect(surf, (25, 30, 40), (ax - 6, PITCH_Y - 74, 12, 56))
            pygame.draw.rect(surf, (25, 30, 40), (ax - 6, PITCH_Y + PITCH_H + 18, 12, 56))

        # Spotify Camp Nou signature Blaugrana tiered stands & banners
        if st["id"] == "campnou":
            garnet = (148, 22, 58)
            blau = (18, 48, 128)
            pygame.draw.rect(surf, garnet, (PITCH_X - 88, PITCH_Y - 68, PITCH_W + 176, 30), border_radius=12)
            pygame.draw.rect(surf, garnet, (PITCH_X - 88, PITCH_Y + PITCH_H + 38, PITCH_W + 176, 30), border_radius=12)
            pygame.draw.rect(surf, blau, (PITCH_X - 88, PITCH_Y - 36, PITCH_W + 176, 22))
            pygame.draw.rect(surf, blau, (PITCH_X - 88, PITCH_Y + PITCH_H + 14, PITCH_W + 176, 22))
            pygame.draw.rect(surf, garnet, (PITCH_X - 88, PITCH_Y - 10, 32, PITCH_H + 20))
            pygame.draw.rect(surf, garnet, (PITCH_X + PITCH_W + 56, PITCH_Y - 10, 32, PITCH_H + 20))
            banner_font = pygame.font.SysFont("segoeui,arial,dejavusans", 18, bold=True)
            t1 = banner_font.render("SPOTIFY CAMP NOU  •  MES QUE UN CLUB", True, GOLD)
            surf.blit(t1, t1.get_rect(center=(PITCH_CX, PITCH_Y - 52)))
            t2 = banner_font.render("FC BARCELONA  •  BLAUGRANA", True, GOLD)
            surf.blit(t2, t2.get_rect(center=(PITCH_CX, PITCH_Y + PITCH_H + 52)))

        # LED Advertising Boards around touchlines
        ad_font = pygame.font.SysFont("segoeui,arial,dejavusans", 11, bold=True)
        ads = ["STRIKER ARENA", "CHAMPIONS", "EFOOTBALL PRO", "FAIR PLAY"]
        for i, ax in enumerate(range(PITCH_X, PITCH_X + PITCH_W - 140, 180)):
            col_ad = (20, 32, 60) if i % 2 == 0 else (35, 20, 48)
            pygame.draw.rect(surf, col_ad, (ax, PITCH_Y - 14, 172, 11), border_radius=3)
            pygame.draw.rect(surf, col_ad, (ax, PITCH_Y + PITCH_H + 4, 172, 11), border_radius=3)
            txt = ad_font.render(ads[i % len(ads)], True, st["accent"])
            surf.blit(txt, (ax + 24, PITCH_Y - 15))
            surf.blit(txt, (ax + 24, PITCH_Y + PITCH_H + 3))

        # Dugout / Technical Benches along top touchline
        for bx in (PITCH_CX - 220, PITCH_CX + 90):
            pygame.draw.rect(surf, (45, 52, 68), (bx, PITCH_Y - 26, 130, 12), border_radius=4)
            pygame.draw.rect(surf, GOLD, (bx, PITCH_Y - 26, 130, 12), 1, border_radius=4)

        # Primitive crowd spectators
        crowd_rng = random.Random(42 + idx)
        palette = [st["accent"], WHITE, GOLD, BLUE, RED, (210, 215, 225)]
        if st["id"] == "campnou":
            palette = [(18, 68, 185), (175, 28, 72), GOLD, WHITE, (45, 95, 215)]
        for row_off in (32, 46, 60):
            for x in range(PITCH_X - 40, PITCH_X + PITCH_W + 41, 20):
                c_top = crowd_rng.choice(palette)
                c_bot = crowd_rng.choice(palette)
                pygame.draw.circle(surf, c_top, (x + crowd_rng.randint(-2, 2), PITCH_Y - row_off), 5)
                pygame.draw.circle(surf, (230, 195, 165), (x, PITCH_Y - row_off - 3), 2)
                pygame.draw.circle(surf, c_bot, (x + crowd_rng.randint(-2, 2), PITCH_Y + PITCH_H + row_off), 5)
                pygame.draw.circle(surf, (230, 195, 165), (x, PITCH_Y + PITCH_H + row_off - 3), 2)
        for col_off in (24, 42, 60):
            for y in range(PITCH_Y, PITCH_Y + PITCH_H + 1, 22):
                if GOAL_TOP - 15 <= y <= GOAL_BOTTOM + 15:
                    continue
                pygame.draw.circle(surf, crowd_rng.choice(palette), (PITCH_X - col_off, y), 5)
                pygame.draw.circle(surf, crowd_rng.choice(palette), (PITCH_X + PITCH_W + col_off, y), 5)

        # Turf stripes
        stripes = 16
        sw = PITCH_W / stripes
        for i in range(stripes):
            pygame.draw.rect(surf, st["turf_a"] if i % 2 == 0 else st["turf_b"], (int(PITCH_X + i * sw), PITCH_Y, int(sw) + 2, PITCH_H))

        # Pitch markings + Corner Arcs + Corner Flags + Penalty D-Arcs
        lc = st["lines"]
        pygame.draw.rect(surf, lc, (PITCH_X, PITCH_Y, PITCH_W, PITCH_H), 4)
        pygame.draw.line(surf, lc, (PITCH_CX, PITCH_Y), (PITCH_CX, PITCH_Y + PITCH_H), 4)
        pygame.draw.circle(surf, lc, (PITCH_CX, PITCH_CY), 130, 4)
        pygame.draw.circle(surf, lc, (PITCH_CX, PITCH_CY), 7)
        box_w, box_h = 240, 500
        pygame.draw.rect(surf, lc, (PITCH_X, PITCH_CY - box_h // 2, box_w, box_h), 4)
        pygame.draw.rect(surf, lc, (PITCH_X + PITCH_W - box_w, PITCH_CY - box_h // 2, box_w, box_h), 4)
        pygame.draw.arc(surf, lc, (PITCH_X + box_w - 70, PITCH_CY - 95, 140, 190), -math.pi / 2.2, math.pi / 2.2, 4)
        pygame.draw.arc(surf, lc, (PITCH_X + PITCH_W - box_w - 70, PITCH_CY - 95, 140, 190), math.pi - math.pi / 2.2, math.pi + math.pi / 2.2, 4)
        pygame.draw.rect(surf, lc, (PITCH_X, PITCH_CY - 165, 95, 330), 3)
        pygame.draw.rect(surf, lc, (PITCH_X + PITCH_W - 95, PITCH_CY - 165, 95, 330), 3)
        pygame.draw.circle(surf, lc, (PITCH_X + 168, PITCH_CY), 5)
        pygame.draw.circle(surf, lc, (PITCH_X + PITCH_W - 168, PITCH_CY), 5)

        # Corner arcs & flags
        for cx, cy, a0, a1 in [
            (PITCH_X, PITCH_Y, -math.pi / 2, 0),
            (PITCH_X + PITCH_W, PITCH_Y, math.pi, 1.5 * math.pi),
            (PITCH_X, PITCH_Y + PITCH_H, 0, math.pi / 2),
            (PITCH_X + PITCH_W, PITCH_Y + PITCH_H, math.pi / 2, math.pi),
        ]:
            pygame.draw.arc(surf, lc, (cx - 24, cy - 24, 48, 48), a0, a1, 3)
            pygame.draw.circle(surf, st["accent"], (cx, cy), 6)

        # Stadium Corner Floodlight Towers
        for fx, fy in [(PITCH_X - 75, PITCH_Y - 58), (PITCH_X + PITCH_W + 75, PITCH_Y - 58), (PITCH_X - 75, PITCH_Y + PITCH_H + 58), (PITCH_X + PITCH_W + 75, PITCH_Y + PITCH_H + 58)]:
            pygame.draw.circle(surf, (255, 250, 210), (fx, fy), 14)
            pygame.draw.circle(surf, GOLD, (fx, fy), 18, 2)

        for gr in (pygame.Rect(PITCH_X - GOAL_W, GOAL_TOP, GOAL_W, GOAL_H), pygame.Rect(PITCH_X + PITCH_W, GOAL_TOP, GOAL_W, GOAL_H)):
            pygame.draw.rect(surf, (16, 22, 28), gr)

        self._pitch_cache[key] = surf
        return surf

    def draw_text(self, text, font, color, x, y, center=True):
        key = (id(font), text, color)
        surf = self._text_cache.get(key)
        if surf is None:
            if len(self._text_cache) > 500:
                self._text_cache.clear()
            surf = font.render(text, True, color)
            self._text_cache[key] = surf
        rect = surf.get_rect(center=(x, y)) if center else surf.get_rect(topleft=(x, y))
        self.screen.blit(surf, rect)
        return rect

    def _build_teams(self):
        t1_ids = (self.career.lineup + ["ronaldo", "salah", "bellingham", "hakimi", "yamal"])[:5]
        self.team1 = []
        for i, pid in enumerate(t1_ids):
            ox, oy = self.career.get_slot_offset(i)
            self.team1.append(Player(PITCH_CX + ox, PITCH_CY + oy, PITCH_CX + ox, PITCH_CY + oy, BLUE, 1, pid, self.career.get_card_stats(pid)))
        gk1_st = self.career.get_card_stats(self.career.gk_id)
        self.team1.append(Player(PITCH_X + 38, PITCH_CY, PITCH_X + 38, PITCH_CY, (30, 180, 140), 1, self.career.gk_id, gk1_st, is_gk=True))

        t2_pos = [(PITCH_CX + 180, PITCH_CY), (PITCH_CX + 400, PITCH_CY - 300), (PITCH_CX + 400, PITCH_CY + 300), (PITCH_CX + 680, PITCH_CY - 200), (PITCH_CX + 680, PITCH_CY + 200)]

        if self.mode == "league":
            club_name = self.career.get_current_league_opponent()
            club = CLUBS_DATA[club_name]
            self.opponent_club_name = club_name
            self.match_ai_difficulty = club["difficulty"]
            opp_ids, opp_gk, opp_kit, opp_gk_kit = club["lineup"], club["gk"], club["kit"], club["gk_kit"]
        elif self.mode == "ucl":
            club_name = self.career.get_your_ucl_match() or "Real Madrid"
            club = CLUBS_DATA[club_name]
            self.opponent_club_name = club_name
            self.match_ai_difficulty = self.career.get_ucl_difficulty()
            opp_ids, opp_gk, opp_kit, opp_gk_kit = club["lineup"], club["gk"], club["kit"], club["gk_kit"]
        else:
            self.opponent_club_name = "CPU All-Stars"
            self.match_ai_difficulty = self.ai_difficulty + 1
            pool = [c["id"] for c in PLAYER_CATALOG if not c.get("is_base") and c["id"] not in t1_ids and c["pos"] != "GK"]
            random.shuffle(pool)
            opp_ids = pool[:5]
            opp_gk = "courtois" if self.match_ai_difficulty >= 3 else "raya"
            opp_kit, opp_gk_kit = RED, (220, 130, 40)

        self.team2 = [Player(x, y, x, y, opp_kit, 2, pid, CATALOG_BY_ID[pid]) for pid, (x, y) in zip(opp_ids[:5], t2_pos)]
        self.team2.append(Player(PITCH_X + PITCH_W - 38, PITCH_CY, PITCH_X + PITCH_W - 38, PITCH_CY, opp_gk_kit, 2, opp_gk, CATALOG_BY_ID[opp_gk], is_gk=True))
        self.active1_idx = 0
        self.active2_idx = 0

    def start_match(self, mode):
        self.mode = mode
        self.auto_ai = False
        self.extra_time = False
        self.subs_used = 0
        self.max_subs = 2
        self.sub_selected_pitch = None
        self.danger_cd = 2.0
        self.net_ripple_left = 0.0
        self.net_ripple_right = 0.0
        self.post_flash_timer = 0.0
        self._build_teams()
        self.score1 = self.score2 = 0
        self.time_left = float(self.match_duration)
        self.celebration_timer = 0.0
        self.in_replay = False
        self.replay_buffer.clear()
        self.replay_frames.clear()
        self.last_scorer_team = 0
        self.last_scorer_name = ""
        self.last_scorer_player = None
        self.match_reward = self.champ_bonus = 0
        self.particles.clear()
        self.impact_rings.clear()
        self.stats = {"shots1": 0, "shots2": 0, "passes1": 0, "passes2": 0}
        self._reset_positions()
        self.state = "PLAYING"
        self.sound.stop_menu_bgm()
        self.sound.play("whistle")
        self.sound.start_bg()

    def _reset_positions(self):
        for p in self.team1 + self.team2:
            p.reset()
        self.ball.reset()

    def spawn_goal_confetti(self, color):
        for _ in range(45):
            ang, spd = random.uniform(0, math.tau), random.uniform(2.5, 9.0)
            self.particles.append(Particle(self.ball.x, self.ball.y, math.cos(ang) * spd, math.sin(ang) * spd, random.choice([color, GOLD, WHITE, CYAN]), random.uniform(0.7, 1.4), random.randint(3, 6)))

    def spawn_kick_sparks(self, x, y, color, count=7, ring_r=26):
        for _ in range(count):
            ang, spd = random.uniform(0, math.tau), random.uniform(1.5, 5.2)
            self.particles.append(Particle(x, y, math.cos(ang) * spd, math.sin(ang) * spd, color, random.uniform(0.18, 0.38), random.randint(2, 4)))
        self.impact_rings.append(ImpactRing(x, y, color, max_r=ring_r, life=0.22))

    # -----------------------------------------------------------------------
    # INPUTS & DYNAMIC OFF-BALL AWARENESS + SMART GK + ATTACKING AI
    # -----------------------------------------------------------------------
    def get_p1_input(self):
        keys = pygame.key.get_pressed()
        kx = (1.0 if keys[pygame.K_d] else 0.0) - (1.0 if keys[pygame.K_a] else 0.0)
        ky = (1.0 if keys[pygame.K_s] else 0.0) - (1.0 if keys[pygame.K_w] else 0.0)
        if kx != 0 and ky != 0:
            kx *= 0.7071
            ky *= 0.7071
        t_inp = self.touch.get_input()
        ax = t_inp["ax"] if abs(t_inp["ax"]) > 0.05 else kx
        ay = t_inp["ay"] if abs(t_inp["ay"]) > 0.05 else ky
        shoot_type = "curler" if keys[pygame.K_c] else ("power" if keys[pygame.K_x] else t_inp["shoot_type"])
        pass_type = "lofted" if keys[pygame.K_f] else t_inp["pass_type"]
        return {
            "ax": ax, "ay": ay,
            "shoot": keys[pygame.K_SPACE] or keys[pygame.K_c] or keys[pygame.K_x] or t_inp["shoot"],
            "shoot_type": shoot_type,
            "pass": keys[pygame.K_q] or keys[pygame.K_f] or t_inp["pass"],
            "pass_type": pass_type,
            "sprint": keys[pygame.K_LSHIFT] or t_inp["sprint"],
            "switch": keys[pygame.K_TAB] or keys[pygame.K_e] or t_inp["switch"],
        }

    def get_p2_local_input(self):
        keys = pygame.key.get_pressed()
        ax = (1.0 if keys[pygame.K_RIGHT] else 0.0) - (1.0 if keys[pygame.K_LEFT] else 0.0)
        ay = (1.0 if keys[pygame.K_DOWN] else 0.0) - (1.0 if keys[pygame.K_UP] else 0.0)
        if ax != 0 and ay != 0:
            ax *= 0.7071
            ay *= 0.7071
        return {"ax": ax, "ay": ay, "shoot": keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER], "shoot_type": "normal", "pass": keys[pygame.K_RCTRL] or keys[pygame.K_SLASH], "pass_type": "ground", "sprint": keys[pygame.K_RSHIFT], "switch": keys[pygame.K_BACKSLASH]}

    def get_ai_input(self, p, is_chaser, team_num, dt):
        b = self.ball
        diff = self.match_ai_difficulty if team_num == 2 else 2
        teammates = self.team2 if team_num == 2 else self.team1
        opponents = self.team1 if team_num == 2 else self.team2
        opp_gk = opponents[-1]

        # 1. Enhanced Goalkeeper AI
        if p.is_gk:
            if b.owner is p:
                if p.gk_hold_timer <= 0:
                    mates = [m for m in teammates if not m.is_gk]
                    best_m = max(mates, key=lambda m: (-m.x if team_num == 2 else m.x)) if mates else None
                    if best_m:
                        dx, dy = best_m.x - p.x, best_m.y - p.y
                        d = max(1.0, math.hypot(dx, dy))
                        return {"ax": dx / d, "ay": dy / d, "shoot": False, "shoot_type": "normal", "pass": True, "pass_type": "lofted", "sprint": False, "switch": False}
                    return {"ax": 1.0 if team_num == 1 else -1.0, "ay": 0.0, "shoot": False, "shoot_type": "normal", "pass": True, "pass_type": "lofted", "sprint": False, "switch": False}
                return {"ax": 0.0, "ay": 0.0, "shoot": False, "shoot_type": "normal", "pass": False, "pass_type": "ground", "sprint": False, "switch": False}

            near_own_box = (b.x < PITCH_X + 225) if team_num == 1 else (b.x > PITCH_X + PITCH_W - 225)
            if b.owner is None and near_own_box and b.z < 22 and math.hypot(b.x - p.x, b.y - p.y) < 190:
                dx, dy = b.x - p.x, b.y - p.y
                d = max(1.0, math.hypot(dx, dy))
                return {"ax": dx / d, "ay": dy / d, "shoot": False, "shoot_type": "normal", "pass": False, "pass_type": "ground", "sprint": True, "switch": False}

            shot_coming = (team_num == 1 and b.vx < -3.0) or (team_num == 2 and b.vx > 3.0)
            if shot_coming:
                t_hit = max(0.0, min(35.0, (p.home_x - b.x) / b.vx))
                pred_y = b.y + b.vy * t_hit
                tx = p.home_x
                ty = max(GOAL_TOP + 16, min(GOAL_BOTTOM - 16, pred_y))
            else:
                dist_ball = abs(b.x - p.home_x)
                step_out = 48 if dist_ball < 340 else 18
                tx = p.home_x + (step_out if team_num == 1 else -step_out)
                ty = PITCH_CY + max(-GOAL_H * 0.42, min(GOAL_H * 0.42, (b.y - PITCH_CY) * 0.58))

            dx, dy = tx - p.x, ty - p.y
            dist = max(1.0, math.hypot(dx, dy))
            return {"ax": dx / dist if dist > 4 else 0.0, "ay": dy / dist if dist > 4 else 0.0, "shoot": False, "shoot_type": "normal", "pass": False, "pass_type": "ground", "sprint": True, "switch": False}

        if b.owner is not None and b.owner.is_gk and b.owner.team != team_num:
            dx, dy = p.home_x - p.x, p.home_y - p.y
            dist = max(1.0, math.hypot(dx, dy))
            return {"ax": dx / dist if dist > 14 else 0.0, "ay": dy / dist if dist > 14 else 0.0, "shoot": False, "shoot_type": "normal", "pass": False, "pass_type": "ground", "sprint": False, "switch": False}

        target_goal_x = PITCH_X + PITCH_W if team_num == 1 else PITCH_X
        own_goal_x = PITCH_X if team_num == 1 else PITCH_X + PITCH_W

        # 2. On-Ball Attacking AI
        if b.owner is p:
            dist_to_goal = math.hypot(target_goal_x - p.x, PITCH_CY - p.y)
            shoot_range = 420 if diff == 1 else (510 if diff == 2 else (600 if diff == 3 else 660))
            aim_y = (GOAL_TOP + 34) if opp_gk.y >= PITCH_CY else (GOAL_BOTTOM - 34)

            if p.ai_shoot_timer > 0:
                p.ai_shoot_timer -= dt
                dx, dy = target_goal_x - p.x, aim_y - p.y
                d = max(1.0, math.hypot(dx, dy))
                if p.ai_shoot_timer <= 0:
                    return {"ax": dx / d, "ay": dy / d, "shoot": False, "shoot_type": p.ai_shoot_type, "pass": False, "pass_type": "ground", "sprint": True, "switch": False}
                return {"ax": dx / d, "ay": dy / d, "shoot": True, "shoot_type": p.ai_shoot_type, "pass": False, "pass_type": "ground", "sprint": False, "switch": False}

            if dist_to_goal < shoot_range and abs(p.y - PITCH_CY) < 340:
                p.ai_shoot_timer = 0.16 if diff == 1 else (0.24 if diff == 2 else 0.32)
                if diff >= 2 and abs(p.y - PITCH_CY) > 120:
                    p.ai_shoot_type = "curler"
                elif diff >= 3 and random.random() < 0.5:
                    p.ai_shoot_type = "power"
                else:
                    p.ai_shoot_type = "normal"
                dx, dy = target_goal_x - p.x, aim_y - p.y
                d = max(1.0, math.hypot(dx, dy))
                return {"ax": dx / d, "ay": dy / d, "shoot": True, "shoot_type": p.ai_shoot_type, "pass": False, "pass_type": "ground", "sprint": False, "switch": False}

            dx, dy = target_goal_x - p.x, aim_y - p.y
            d = max(1.0, math.hypot(dx, dy))
            ax, ay = dx / d, dy / d
            nearest_opp = min(opponents, key=lambda o: math.hypot(o.x - p.x, o.y - p.y))
            if math.hypot(nearest_opp.x - p.x, nearest_opp.y - p.y) < 135:
                forward_mates = [m for m in teammates if m is not p and not m.is_gk and ((m.x < p.x - 40) if team_num == 2 else (m.x > p.x + 40))]
                if forward_mates and random.random() < (0.04 if diff == 1 else 0.13):
                    best_m = max(forward_mates, key=lambda m: (-m.x if team_num == 2 else m.x))
                    pdx, pdy = best_m.x - p.x, best_m.y - p.y
                    pd = max(1.0, math.hypot(pdx, pdy))
                    return {"ax": pdx / pd, "ay": pdy / pd, "shoot": False, "shoot_type": "normal", "pass": True, "pass_type": "ground", "sprint": True, "switch": False}
                ev_x, ev_y = p.x - nearest_opp.x, p.y - nearest_opp.y
                ev_d = max(1.0, math.hypot(ev_x, ev_y))
                ax = ax * 0.65 + (ev_x / ev_d) * 0.55
                ay = ay * 0.65 + (ev_y / ev_d) * 0.75
                mag = max(1.0, math.hypot(ax, ay))
                ax, ay = ax / mag, ay / mag
            return {"ax": ax, "ay": ay, "shoot": False, "shoot_type": "normal", "pass": False, "pass_type": "ground", "sprint": diff >= 2 and p.stamina > 20, "switch": False}

        # 3. Dynamic Off-Ball Awareness (Attacking Runs & Defensive Tracking — Never Standing Still!)
        team_has_ball = (b.owner is not None and b.owner.team == team_num)
        if is_chaser:
            tx, ty = b.x, b.y
            want_sprint = True
        elif team_has_ball:
            # Make dynamic forward attacking runs into open lanes!
            attack_dir = 1.0 if team_num == 1 else -1.0
            lane_shift = math.sin(time.time() * 1.4 + p.home_y * 0.01) * 75.0
            tx = max(PITCH_X + 160, min(PITCH_X + PITCH_W - 140, p.home_x * 0.35 + (b.x + attack_dir * 310) * 0.65))
            ty = max(PITCH_Y + 75, min(PITCH_Y + PITCH_H - 75, p.home_y * 0.65 + b.y * 0.35 + lane_shift))
            want_sprint = math.hypot(tx - p.x, ty - p.y) > 95 and p.stamina > 28
        else:
            # Defending phase: shift compactly between ball and own goal, tracking attackers
            tx = p.home_x * 0.52 + b.x * 0.48
            tx = max(own_goal_x + 110, min(PITCH_CX + 320, tx)) if team_num == 1 else min(own_goal_x - 110, max(PITCH_CX - 320, tx))
            ty = p.home_y * 0.60 + b.y * 0.40
            want_sprint = math.hypot(tx - p.x, ty - p.y) > 120 and p.stamina > 30

        dx, dy = tx - p.x, ty - p.y
        dist = max(1.0, math.hypot(dx, dy))
        return {"ax": dx / dist if dist > 8 else 0.0, "ay": dy / dist if dist > 8 else 0.0, "shoot": False, "shoot_type": "normal", "pass": False, "pass_type": "ground", "sprint": want_sprint, "switch": False}

    # -----------------------------------------------------------------------
    # MOVEMENT, DRIBBLING, PASSING & SHOOTING
    # -----------------------------------------------------------------------
    def _update_player(self, p, inp, prev_shoot, prev_pass, dt, teammates):
        if p.is_gk and p.gk_hold_timer > 0:
            p.gk_hold_timer = max(0.0, p.gk_hold_timer - dt)

        ax, ay = float(inp.get("ax", 0.0)), float(inp.get("ay", 0.0))
        mag = math.hypot(ax, ay)
        if mag > 1.0:
            ax /= mag
            ay /= mag
        if mag > 0.08:
            p.facing_x, p.facing_y = ax / max(1.0, mag), ay / max(1.0, mag)

        pac_mult = 0.66 + ((p.stats["pac"] - 65) / 35.0) * 0.56
        sprinting = inp.get("sprint", False) and mag > 0.1 and p.stamina > 4
        p.stamina = max(0.0, p.stamina - 26.0 * dt) if sprinting else min(100.0, p.stamina + 24.0 * dt)

        top_speed = (6.4 if sprinting else 4.7) * pac_mult
        if p.charging:
            top_speed *= 0.80
        blend = 0.34 if mag > 0.08 else 0.28
        p.vx += (ax * top_speed - p.vx) * blend
        p.vy += (ay * top_speed - p.vy) * blend

        p.x = max(PITCH_X + PLAYER_RADIUS, min(PITCH_X + PITCH_W - PLAYER_RADIUS, p.x + p.vx))
        p.y = max(PITCH_Y + PLAYER_RADIUS, min(PITCH_Y + PITCH_H - PLAYER_RADIUS, p.y + p.vy))

        pass_now = bool(inp.get("pass", False))
        if pass_now and not prev_pass:
            self._attempt_pass(p, teammates, inp.get("pass_type", "ground"))

        shoot_now = bool(inp.get("shoot", False))
        if shoot_now:
            p.charging = True
            p.charge = min(1.0, p.charge + dt * 1.75)
            p.shoot_type = inp.get("shoot_type", "normal")
        elif prev_shoot and p.charging:
            self._attempt_kick(p, p.charge, p.shoot_type)
            p.charging = False
            p.charge = 0.0
        else:
            p.charging = False
            p.charge = 0.0

        return shoot_now, pass_now

    def _attempt_pass(self, p, teammates, pass_type="ground"):
        if self.ball.owner is not p and (math.hypot(self.ball.x - p.x, self.ball.y - p.y) > PLAYER_RADIUS + BALL_RADIUS + 30 or self.ball.z > 24):
            return
        others = [m for m in teammates if m is not p and not m.is_gk]
        if not others:
            return

        def dir_score(m):
            dx, dy = m.x - p.x, m.y - p.y
            d = max(1.0, math.hypot(dx, dy))
            cos_sim = (dx / d) * p.facing_x + (dy / d) * p.facing_y
            return cos_sim * 3.0 - (d / 1200.0)

        best = max(others, key=dir_score)
        tx, ty = best.x + best.vx * 5 - self.ball.x, best.y + best.vy * 5 - self.ball.y

        self.ball.owner = None
        self.ball.steal_cd = 0.20
        dist = max(1.0, math.hypot(tx, ty))
        pas_spd = (11.5 if pass_type == "lofted" else 10.5) + (p.stats["pas"] / 100.0) * 5.0
        self.ball.vx, self.ball.vy = (tx / dist) * pas_spd, (ty / dist) * pas_spd
        self.ball.curve = 0.0
        self.ball.vz = 8.4 if pass_type == "lofted" else 0.0
        self.ball.trail_color = CYAN if pass_type == "lofted" else (220, 220, 230)
        self.ball.last_touch_team, self.ball.last_touch_id = p.team, p.card_id
        if p.team == 1:
            self.stats["passes1"] += 1
            self.active1_idx = teammates.index(best)
        else:
            self.stats["passes2"] += 1
        self.sound.play("kick")
        self.spawn_kick_sparks(self.ball.x, self.ball.y, CYAN if pass_type == "lofted" else WHITE, 8, ring_r=24)

    def _attempt_kick(self, p, power, shoot_type="normal"):
        dx, dy = self.ball.x - p.x, self.ball.y - p.y
        dist = math.hypot(dx, dy)
        if (self.ball.owner is p or (dist <= PLAYER_RADIUS + BALL_RADIUS + 28 and dist > 0.001)) and self.ball.z < 28:
            gx_pos = (PITCH_X + PITCH_W) if p.team == 1 else PITCH_X
            gx, gy = gx_pos - self.ball.x, PITCH_CY - self.ball.y
            gd = max(1.0, math.hypot(gx, gy))
            if p.team == 2:
                nx, ny = p.facing_x, p.facing_y
            elif self.career.smart_assist:
                nx = p.facing_x * 0.42 + (gx / gd) * 0.58
                ny = p.facing_y * 0.42 + (gy / gd) * 0.58
                nd = max(1.0, math.hypot(nx, ny))
                nx, ny = nx / nd, ny / nd
            else:
                nx, ny = p.facing_x, p.facing_y

            self.ball.owner = None
            self.ball.steal_cd = 0.22
            sho_mult = 0.85 + (p.stats["sho"] / 100.0) * 0.35
            skills = p.stats.get("skills", [])
            if shoot_type == "curler":
                force = (12.5 + power * 11.5) * sho_mult
                blitz = 1.45 if "Blitz Curler" in skills else 1.0
                inward_dot = (-ny) * gx + nx * gy
                sign = 1.0 if inward_dot >= 0 else -1.0
                self.ball.curve = sign * 0.40 * blitz
                self.ball.vz = 3.2
                self.ball.trail_color = PURPLE
                self.sound.play("power")
            elif shoot_type == "power":
                bonus = 1.22 if any(s in skills for s in ("Bullet Header", "Rising Shot", "Phenomenal Finishing", "Loop Scream")) else 1.0
                force = (18.0 + power * 16.0) * sho_mult * bonus
                self.ball.curve = 0.0
                self.ball.vz = 2.6
                self.ball.trail_color = ORANGE
                self.sound.play("power")
            else:
                force = (12.0 + power * 11.0) * sho_mult
                self.ball.curve = 0.0
                self.ball.vz = 1.6
                self.ball.trail_color = GOLD if power > 0.45 else (220, 220, 230)
                self.sound.play("power" if power > 0.45 else "kick")

            self.ball.vx = nx * force + p.vx * 0.35
            self.ball.vy = ny * force + p.vy * 0.35
            self.ball.last_touch_team, self.ball.last_touch_id = p.team, p.card_id
            if p.team == 1:
                self.stats["shots1"] += 1
            else:
                self.stats["shots2"] += 1
            self.spawn_kick_sparks(self.ball.x, self.ball.y, self.ball.trail_color, 12, ring_r=34)

    def _resolve_all_player_collisions(self):
        all_p = self.team1 + self.team2
        min_d = PLAYER_RADIUS * 2
        for i in range(len(all_p)):
            for j in range(i + 1, len(all_p)):
                a, b = all_p[i], all_p[j]
                dx, dy = b.x - a.x, b.y - a.y
                dist = math.hypot(dx, dy)
                if 0.001 < dist < min_d:
                    nx, ny = dx / dist, dy / dist
                    ov = (min_d - dist) * 0.5
                    a.x -= nx * ov
                    a.y -= ny * ov
                    b.x += nx * ov
                    b.y += ny * ov
                    if a.team != b.team and self.ball.steal_cd <= 0:
                        if self.ball.owner is a and not a.is_gk:
                            front_dot = nx * a.facing_x + ny * a.facing_y
                            if front_dot > -0.15 or math.hypot(b.x - self.ball.x, b.y - self.ball.y) < 22:
                                self.ball.owner = b
                                self.ball.steal_cd = 0.40
                                self.sound.play("kick")
                                self.spawn_kick_sparks(self.ball.x, self.ball.y, WHITE, 6, ring_r=22)
                        elif self.ball.owner is b and not b.is_gk:
                            front_dot = (-nx) * b.facing_x + (-ny) * b.facing_y
                            if front_dot > -0.15 or math.hypot(a.x - self.ball.x, a.y - self.ball.y) < 22:
                                self.ball.owner = a
                                self.ball.steal_cd = 0.40
                                self.sound.play("kick")
                                self.spawn_kick_sparks(self.ball.x, self.ball.y, WHITE, 6, ring_r=22)

    def _resolve_ball_players(self):
        if self.ball.steal_cd > 0 or self.ball.owner is not None:
            return
        for p in self.team1 + self.team2:
            reach = PLAYER_RADIUS + BALL_RADIUS + (10 if p.is_gk else 5)
            max_z = 36 if p.is_gk else 24
            if self.ball.z <= max_z and math.hypot(self.ball.x - p.x, self.ball.y - p.y) < reach:
                self.ball.owner = p
                self.ball.curve = 0.0
                self.ball.last_touch_team = p.team
                self.ball.last_touch_id = p.card_id
                if p.is_gk:
                    p.gk_hold_timer = 0.90
                elif p.team == 1:
                    self.active1_idx = self.team1.index(p)
                self.sound.play("kick")
                self.spawn_kick_sparks(self.ball.x, self.ball.y, (200, 235, 195), 6, ring_r=22)
                break

    def _update_ball(self, dt, in_goal_celebration=False):
        b = self.ball
        if b.steal_cd > 0:
            b.steal_cd = max(0.0, b.steal_cd - dt)

        if b.owner is not None and not in_goal_celebration:
            p = b.owner
            target_x = p.x + p.facing_x * (PLAYER_RADIUS + BALL_RADIUS - 2)
            target_y = p.y + p.facing_y * (PLAYER_RADIUS + BALL_RADIUS - 2)
            b.x += (target_x - b.x) * 0.58
            b.y += (target_y - b.y) * 0.58
            b.vx, b.vy, b.z = p.vx, p.vy, 0.0
            b.spin_angle += math.hypot(p.vx, p.vy) * 0.11
            b.trail.clear()
            return

        st = self.stadium
        b.trail.append((b.x, b.y - b.z))
        if len(b.trail) > 8:
            b.trail.pop(0)

        if abs(b.curve) > 0.01:
            spd = math.hypot(b.vx, b.vy)
            if spd > 1.5:
                b.vx += -b.vy / spd * b.curve
                b.vy += b.vx / spd * b.curve
            b.curve *= 0.985

        b.x += b.vx
        b.y += b.vy
        b.spin_angle += math.hypot(b.vx, b.vy) * 0.12
        b.vx *= st["ball_friction"]
        b.vy *= st["ball_friction"]

        if b.z > 0 or b.vz != 0:
            b.z += b.vz
            b.vz -= 0.38
            if b.z <= 0:
                b.z = 0.0
                b.vz = -b.vz * 0.45 if abs(b.vz) > 1.2 else 0.0

        if math.hypot(b.vx, b.vy) < 0.05:
            b.vx = b.vy = 0.0

        if in_goal_celebration:
            if b.y - BALL_RADIUS < GOAL_TOP + 6:
                b.y = GOAL_TOP + 6 + BALL_RADIUS
                b.vy = abs(b.vy) * 0.35
                self.net_hit_y = b.y
            elif b.y + BALL_RADIUS > GOAL_BOTTOM - 6:
                b.y = GOAL_BOTTOM - 6 - BALL_RADIUS
                b.vy = -abs(b.vy) * 0.35
                self.net_hit_y = b.y
            if b.x < PITCH_X - GOAL_W + BALL_RADIUS + 4:
                b.x = PITCH_X - GOAL_W + BALL_RADIUS + 4
                b.vx = abs(b.vx) * 0.18
                b.vy *= 0.65
                self.net_ripple_left = 1.0
                self.net_hit_y = b.y
                self.spawn_kick_sparks(b.x, b.y, WHITE, 6, ring_r=28)
            elif b.x > PITCH_X + PITCH_W + GOAL_W - BALL_RADIUS - 4:
                b.x = PITCH_X + PITCH_W + GOAL_W - BALL_RADIUS - 4
                b.vx = -abs(b.vx) * 0.18
                b.vy *= 0.65
                self.net_ripple_right = 1.0
                self.net_hit_y = b.y
                self.spawn_kick_sparks(b.x, b.y, WHITE, 6, ring_r=28)
            b.vx *= 0.88
            b.vy *= 0.88
            return

        if b.y - BALL_RADIUS < PITCH_Y:
            b.y = PITCH_Y + BALL_RADIUS
            b.vy = abs(b.vy) * 0.82
        elif b.y + BALL_RADIUS > PITCH_Y + PITCH_H:
            b.y = PITCH_Y + PITCH_H - BALL_RADIUS
            b.vy = -abs(b.vy) * 0.82

        in_goal_y = GOAL_TOP + BALL_RADIUS * 0.3 <= b.y <= GOAL_BOTTOM - BALL_RADIUS * 0.3

        for px, py in [(PITCH_X, GOAL_TOP), (PITCH_X, GOAL_BOTTOM), (PITCH_X + PITCH_W, GOAL_TOP), (PITCH_X + PITCH_W, GOAL_BOTTOM)]:
            dx, dy = b.x - px, b.y - py
            d = math.hypot(dx, dy)
            if 0.001 < d < BALL_RADIUS + 6:
                nx, ny = dx / d, dy / d
                b.x, b.y = px + nx * (BALL_RADIUS + 6), py + ny * (BALL_RADIUS + 6)
                dot = b.vx * nx + b.vy * ny
                if dot < 0:
                    b.vx -= 1.8 * dot * nx
                    b.vy -= 1.8 * dot * ny
                    self.sound.play("post")
                    self.post_flash_timer = 0.25
                    self.post_flash_pos = (px, py)
                    self.spawn_kick_sparks(px, py, GOLD, 14, ring_r=38)

        if b.x - BALL_RADIUS < PITCH_X:
            if in_goal_y:
                if b.x < PITCH_X - 8:
                    self.net_ripple_left = 1.0
                    self.net_hit_y = b.y
                    self._score_goal(2)
                    return
            else:
                b.x = PITCH_X + BALL_RADIUS
                b.vx = abs(b.vx) * 0.82

        if b.x + BALL_RADIUS > PITCH_X + PITCH_W:
            if in_goal_y:
                if b.x > PITCH_X + PITCH_W + 8:
                    self.net_ripple_right = 1.0
                    self.net_hit_y = b.y
                    self._score_goal(1)
                    return
            else:
                b.x = PITCH_X + PITCH_W - BALL_RADIUS
                b.vx = -abs(b.vx) * 0.82

    def _record_replay_frame(self):
        self.replay_buffer.append({"b": (self.ball.x, self.ball.y, self.ball.z), "t1": [(p.x, p.y) for p in self.team1], "t2": [(p.x, p.y) for p in self.team2]})
        if len(self.replay_buffer) > 150:
            self.replay_buffer.pop(0)

    def _score_goal(self, scorer_team):
        if self.celebration_timer > 0 or self.in_replay:
            return
        self.ball.owner = None
        if scorer_team == 1:
            self.score1 += 1
            self.spawn_goal_confetti(BLUE)
            scorer_pid = self.ball.last_touch_id if self.ball.last_touch_team == 1 else self.team1[self.active1_idx].card_id
            self.last_scorer_player = next((p for p in self.team1 if p.card_id == scorer_pid), self.team1[self.active1_idx])
            if scorer_pid in CATALOG_BY_ID:
                self.career.record_goal(scorer_pid, mode=self.mode)
                self.last_scorer_name = CATALOG_BY_ID[scorer_pid]["short"]
            else:
                self.last_scorer_name = "TEAM 1"
        else:
            self.score2 += 1
            self.spawn_goal_confetti(RED)
            opp_pid = self.ball.last_touch_id if self.ball.last_touch_team == 2 else self.team2[self.active2_idx].card_id
            self.last_scorer_player = next((p for p in self.team2 if p.card_id == opp_pid), self.team2[self.active2_idx])
            if opp_pid in CATALOG_BY_ID:
                self.career.record_goal(opp_pid, mode=self.mode)
            self.last_scorer_name = self.last_scorer_player.stats["short"]

        self.last_scorer_team = scorer_team
        self.celebration_timer = 1.9
        self.replay_frames = list(self.replay_buffer)
        self.replay_idx = 0.0
        self.in_replay = False
        self.commentary_banner = f"Hafid Derradji: GOLAZO! {self.last_scorer_name}!!" if self.sound.commentary_lang == "hafid" else f"Spanish: GOOOOL! {self.last_scorer_name}!!"
        self.commentary_timer = 3.5
        self.sound.play_commentary_goal()
        self.sound.play("whistle")

    def _skip_replay(self):
        self.celebration_timer = 0.0
        self.in_replay = False
        if self.time_left <= 0 and self.score1 != self.score2:
            self._finish_match()
        else:
            self._reset_positions()
            self.sound.play("whistle")

    def _start_penalties(self):
        self.pen_round = 1
        self.pen_score1 = self.pen_score2 = 0
        self.pen_turn = 1
        self.pen_msg = "YOUR TURN! Tap Left / Center / Right to SHOOT!"
        self.state = "PENALTIES"
        self.sound.play("whistle")

    def _take_penalty_choice(self, choice_idx):
        ai_choice = random.randint(0, 2)
        dirs = ["LEFT", "CENTER", "RIGHT"]
        if self.pen_turn == 1:
            if choice_idx != ai_choice:
                self.pen_score1 += 1
                self.pen_msg = f"GOAL!! ({dirs[choice_idx]})"
                self.sound.play_commentary_goal()
            else:
                self.pen_msg = f"SAVED by GK! ({dirs[choice_idx]})"
                self.sound.play("post")
            self.pen_turn = 2
        else:
            if ai_choice != choice_idx:
                self.pen_score2 += 1
                self.pen_msg = f"CPU SCORED! ({dirs[ai_choice]})"
                self.sound.play("goal")
            else:
                self.pen_msg = f"YOU SAVED IT! ({dirs[choice_idx]})"
                self.sound.play("kick")
            self.pen_turn = 1
            self.pen_round += 1

        if self.pen_round > 3 and self.pen_turn == 1 and self.pen_score1 != self.pen_score2:
            if self.pen_score1 > self.pen_score2:
                self.score1 += 1
            else:
                self.score2 += 1
            self._finish_match()

    def _finish_match(self):
        self.state = "FULLTIME"
        self.sound.play("whistle")
        self.sound.stop_bg()
        if self.mode in ("ai", "league", "ucl", "host", "local"):
            reward = self.score1 * 100 + (600 if self.score1 > self.score2 else (250 if self.score1 == self.score2 else 100))
            self.match_reward = reward
            self.career.coins += reward
            won_title = False
            if self.mode == "league":
                self.champ_bonus, won_title = self.career.record_league_match(self.score1, self.score2)
                if won_title:
                    self.ceremony_title = "LEAGUE CHAMPIONS!"
                    self.ceremony_sub = f"You won the Striker Premier League! (+{self.champ_bonus:,} Coins & Gold Star)"
                    self.ceremony_color = GOLD
                    self.state = "TROPHY_CEREMONY"
                    self.sound.play_commentary_goal()
            elif self.mode == "ucl":
                self.champ_bonus, won_title = self.career.advance_ucl_round(self.score1, self.score2)
                if won_title:
                    self.ceremony_title = "CHAMPIONS LEAGUE WINNERS!"
                    self.ceremony_sub = f"Kings of Europe! (+{self.champ_bonus:,} Coins & Cyan Star)"
                    self.ceremony_color = CYAN
                    self.state = "TROPHY_CEREMONY"
                    self.sound.play_commentary_goal()
            self.career.save()

    def update_playing(self, dt):
        if self.commentary_timer > 0:
            self.commentary_timer -= dt
        if self.danger_cd > 0:
            self.danger_cd -= dt
        if self.net_ripple_left > 0:
            self.net_ripple_left = max(0.0, self.net_ripple_left - dt * 1.4)
        if self.net_ripple_right > 0:
            self.net_ripple_right = max(0.0, self.net_ripple_right - dt * 1.4)
        if self.post_flash_timer > 0:
            self.post_flash_timer = max(0.0, self.post_flash_timer - dt)

        for pt in self.particles[:]:
            pt.x += pt.vx
            pt.y += pt.vy
            pt.vx *= 0.96
            pt.vy *= 0.96
            pt.life -= dt
            if pt.life <= 0:
                self.particles.remove(pt)

        for rg in self.impact_rings[:]:
            rg.life -= dt
            if rg.life <= 0:
                self.impact_rings.remove(rg)

        if self.celebration_timer > 0:
            self.celebration_timer -= dt
            self._update_ball(dt, in_goal_celebration=True)
            if self.last_scorer_player:
                self.last_scorer_player.x += math.cos(time.time() * 6) * 2.5
                self.last_scorer_player.y += math.sin(time.time() * 6) * 2.5
            if self.celebration_timer <= 0:
                if self.replay_frames and self.mode != "client":
                    self.in_replay = True
                    self.replay_idx = 0.0
                else:
                    self._skip_replay()
            return

        if self.in_replay:
            self.replay_idx += 0.55
            if int(self.replay_idx) >= len(self.replay_frames):
                self._skip_replay()
            return

        target_cx = max(0, min(WORLD_W - WIDTH, self.ball.x - WIDTH // 2))
        target_cy = max(0, min(WORLD_H - (HEIGHT - TOP_HUD), self.ball.y - (HEIGHT - TOP_HUD) // 2))
        self.cam_x += (target_cx - self.cam_x) * 0.14
        self.cam_y += (target_cy - self.cam_y) * 0.14

        if self.mode == "client":
            self.net.send_json(self.get_p1_input())
            st = self.net.get_latest_state()
            if st:
                self._apply_network_state(st)
            return

        b = self.ball
        near_goal = (b.x < PITCH_X + 350 or b.x > PITCH_X + PITCH_W - 350) and (GOAL_TOP - 110 < b.y < GOAL_BOTTOM + 110)
        if near_goal and self.danger_cd <= 0 and (math.hypot(b.vx, b.vy) > 3.2 or (b.owner is not None and not b.owner.is_gk)):
            self.danger_cd = 7.5
            self.commentary_banner = "Hafid Derradji: KHATIRA!! (DANGER!)"
            self.commentary_timer = 2.2
            self.sound.play_commentary_danger()

        self.time_left = max(0.0, self.time_left - dt)
        if self.time_left <= 0:
            if self.score1 != self.score2:
                self._finish_match()
                self._broadcast_host_state()
                return
            elif not self.extra_time:
                self.extra_time = True
                self.max_subs = 3
                self.time_left = 30.0
                self._reset_positions()
                self.sound.play("whistle")
                self.commentary_banner = "EXTRA TIME! (+1 SUB UNLOCKED)"
                self.commentary_timer = 3.0
            else:
                self._start_penalties()
                return

        outfield1 = range(len(self.team1) - 1)
        if self.auto_ai:
            closest1 = min(outfield1, key=lambda i: math.hypot(self.team1[i].x - self.ball.x, self.team1[i].y - self.ball.y))
            self.active1_idx = closest1
            for i, p in enumerate(self.team1):
                self._update_player(p, self.get_ai_input(p, i == closest1, 1, dt), False, False, dt, self.team1)
        else:
            inp1 = self.get_p1_input()
            if inp1["switch"] and not self._prev_p1_switch:
                others = [i for i in outfield1 if i != self.active1_idx]
                if others:
                    self.active1_idx = min(others, key=lambda i: math.hypot(self.team1[i].x - self.ball.x, self.team1[i].y - self.ball.y))
            self._prev_p1_switch = inp1["switch"]
            closest1_ai = min([i for i in outfield1 if i != self.active1_idx], key=lambda i: math.hypot(self.team1[i].x - self.ball.x, self.team1[i].y - self.ball.y), default=0)
            for i, p in enumerate(self.team1):
                if i == self.active1_idx:
                    self._prev_p1_shoot, self._prev_p1_pass = self._update_player(p, inp1, self._prev_p1_shoot, self._prev_p1_pass, dt, self.team1)
                else:
                    self._update_player(p, self.get_ai_input(p, i == closest1_ai and self.ball.owner is None, 1, dt), False, False, dt, self.team1)

        outfield2 = range(len(self.team2) - 1)
        closest2 = min(outfield2, key=lambda i: math.hypot(self.team2[i].x - self.ball.x, self.team2[i].y - self.ball.y))
        if self.mode == "local":
            inp2 = self.get_p2_local_input()
            if inp2["switch"] and not self._prev_p2_switch:
                others = [i for i in outfield2 if i != self.active2_idx]
                if others:
                    self.active2_idx = min(others, key=lambda i: math.hypot(self.team2[i].x - self.ball.x, self.team2[i].y - self.ball.y))
            self._prev_p2_switch = inp2["switch"]
        elif self.mode == "host":
            inp2 = self.net.get_remote_input()
            if inp2.get("switch") and not self._prev_p2_switch:
                self.active2_idx = closest2
            self._prev_p2_switch = bool(inp2.get("switch", False))
        else:
            inp2 = None
            self.active2_idx = closest2

        for i, p in enumerate(self.team2):
            if inp2 is not None and i == self.active2_idx:
                self._prev_p2_shoot, self._prev_p2_pass = self._update_player(p, inp2, self._prev_p2_shoot, self._prev_p2_pass, dt, self.team2)
            else:
                ai_i = self.get_ai_input(p, i == closest2 and inp2 is None, 2, dt)
                self._update_player(p, ai_i, p.charging, False, dt, self.team2)

        self._resolve_all_player_collisions()
        self._resolve_ball_players()
        self._update_ball(dt)
        self._record_replay_frame()
        self._broadcast_host_state()

    def _broadcast_host_state(self):
        if self.mode != "host":
            return
        self.net.send_json({
            "t1": [[round(p.x, 1), round(p.y, 1), round(p.stamina, 1), round(p.charge, 2)] for p in self.team1],
            "t2": [[round(p.x, 1), round(p.y, 1), round(p.stamina, 1), round(p.charge, 2)] for p in self.team2],
            "a1": self.active1_idx, "a2": self.active2_idx,
            "b": [round(self.ball.x, 1), round(self.ball.y, 1), round(self.ball.z, 1)],
            "s": [self.score1, self.score2], "t": round(self.time_left, 1),
            "cel": round(self.celebration_timer, 2), "lt": self.last_scorer_team,
            "ln": self.last_scorer_name, "et": self.extra_time,
            "st": self.stadium_idx, "done": self.state == "FULLTIME",
        })

    def _apply_network_state(self, st):
        if len(self.team1) != 6 or len(self.team2) != 6:
            self._build_teams()
        for p, vals in zip(self.team1, st["t1"]):
            p.x, p.y, p.stamina, p.charge = vals
        for p, vals in zip(self.team2, st["t2"]):
            p.x, p.y, p.stamina, p.charge = vals
        self.active1_idx, self.active2_idx = st["a1"], st["a2"]
        self.ball.x, self.ball.y, self.ball.z = st["b"]
        self.score1, self.score2 = st["s"]
        self.time_left = st["t"]
        prev_c = self.celebration_timer
        self.celebration_timer = st["cel"]
        self.last_scorer_team, self.last_scorer_name = st["lt"], st["ln"]
        self.extra_time, self.stadium_idx = st["et"], st["st"]
        if self.celebration_timer > 0 and prev_c <= 0:
            self.sound.play_commentary_goal()
            self.spawn_goal_confetti(BLUE if self.last_scorer_team == 1 else RED)
        if st.get("done"):
            self.state = "FULLTIME"

    # -----------------------------------------------------------------------
    # RENDERING
    # -----------------------------------------------------------------------
    def draw_button(self, key, rect, label, accent=CYAN, sublabel=None):
        mx, my = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mx, my)
        pygame.draw.rect(self.screen, CARD_HOVER if hovered else CARD_BG, rect, border_radius=12)
        pygame.draw.rect(self.screen, accent if hovered else (65, 78, 105), rect, width=2, border_radius=12)
        if sublabel:
            self.draw_text(label, self.font_md, WHITE, rect.centerx, rect.centery - 9)
            self.draw_text(sublabel, self.font_xs, MUTED_TEXT, rect.centerx, rect.centery + 13)
        else:
            self.draw_text(label, self.font_md, WHITE, rect.centerx, rect.centery)
        self.buttons[key] = rect

    def draw_player_2d(self, p, is_active, ox, oy, celebrating=False):
        sx, sy = int(p.x - ox), int(p.y - oy + TOP_HUD)
        if not (-40 <= sx <= WIDTH + 40 and TOP_HUD - 40 <= sy <= HEIGHT + 40):
            return
        jump_y = int(abs(math.sin(time.time() * 10)) * 14) if celebrating else 0
        pygame.draw.ellipse(self.screen, (0, 0, 0), (sx - 15, sy + 12, 30, 9))
        if is_active:
            pygame.draw.circle(self.screen, GOLD, (sx, sy - jump_y), PLAYER_RADIUS + 6, 3)
        if p.charge > 0.05:
            r = PLAYER_RADIUS + 9
            col = PURPLE if p.shoot_type == "curler" else (ORANGE if p.shoot_type == "power" else CYAN)
            pygame.draw.arc(self.screen, col, (sx - r, sy - r, r * 2, r * 2), -math.pi / 2, -math.pi / 2 + p.charge * math.tau, 4)
        pygame.draw.circle(self.screen, WHITE, (sx, sy - jump_y), PLAYER_RADIUS + 1)
        pygame.draw.circle(self.screen, p.color, (sx, sy - jump_y), PLAYER_RADIUS - 2)
        self.draw_text(str(p.stats["num"]), self.font_sm, WHITE, sx, sy - jump_y)
        self.draw_text(p.stats["short"], self.font_xs, WHITE, sx, sy - jump_y - PLAYER_RADIUS - 11)

    def draw_goal_nets_2d(self, ox, oy):
        st = self.stadium
        nc, pc = st["net"], st["goal_post"]
        for side in (-1, 1):
            gx0, gx1 = (PITCH_X - GOAL_W, PITCH_X) if side == -1 else (PITCH_X + PITCH_W, PITCH_X + PITCH_W + GOAL_W)
            rip = self.net_ripple_left if side == -1 else self.net_ripple_right
            sx0, sx1 = int(gx0 - ox), int(gx1 - ox)
            sy0, sy1 = int(GOAL_TOP - oy + TOP_HUD), int(GOAL_BOTTOM - oy + TOP_HUD)
            if sx1 < -20 or sx0 > WIDTH + 20 or sy1 < TOP_HUD - 20 or sy0 > HEIGHT + 20:
                continue

            bulge = int(rip * 16 * math.sin(time.time() * 24)) * side
            for gy in range(GOAL_TOP, GOAL_BOTTOM + 1, 16):
                sy = int(gy - oy + TOP_HUD)
                dist_factor = max(0.0, 1.0 - abs(gy - self.net_hit_y) / (GOAL_H * 0.65))
                off = int(bulge * dist_factor)
                if side == -1:
                    pygame.draw.line(self.screen, nc, (sx0 + off, sy), (sx1, sy), 1)
                else:
                    pygame.draw.line(self.screen, nc, (sx0, sy), (sx1 + off, sy), 1)
            for gx in range(gx0, gx1 + 1, 13):
                sx = int(gx - ox)
                pygame.draw.line(self.screen, nc, (sx, sy0), (sx, sy1), 1)
            back_x = sx0 + bulge if side == -1 else sx1 + bulge
            front_x = sx1 if side == -1 else sx0
            pygame.draw.line(self.screen, pc, (front_x, sy0), (back_x, sy0), 4)
            pygame.draw.line(self.screen, pc, (front_x, sy1), (back_x, sy1), 4)
            pygame.draw.line(self.screen, pc, (back_x, sy0), (back_x, sy1), 3)
            pygame.draw.circle(self.screen, pc, (front_x, sy0), 6)
            pygame.draw.circle(self.screen, pc, (front_x, sy1), 6)

        if self.post_flash_timer > 0 and self.post_flash_pos:
            fx, fy = int(self.post_flash_pos[0] - ox), int(self.post_flash_pos[1] - oy + TOP_HUD)
            pygame.draw.circle(self.screen, GOLD, (fx, fy), 12, 3)

    def draw_ball_2d(self, ox, oy):
        b = self.ball
        sx, sy = int(b.x - ox), int(b.y - oy + TOP_HUD)
        for i, (tx, ty) in enumerate(b.trail):
            pygame.draw.circle(self.screen, b.trail_color, (int(tx - ox), int(ty - oy + TOP_HUD)), max(2, int(BALL_RADIUS * (i + 1) / (len(b.trail) + 2))))

        sh_r = max(5, BALL_RADIUS - int(b.z * 0.14))
        pygame.draw.ellipse(self.screen, (18, 22, 20), (sx - sh_r + int(b.z * 0.25), sy - sh_r // 2 + 6, sh_r * 2, sh_r + 3))

        by = int(sy - b.z)
        r = BALL_RADIUS + int(b.z * 0.12)
        pygame.draw.circle(self.screen, (238, 240, 244), (sx, by), r)
        pygame.draw.circle(self.screen, (255, 255, 255), (sx - r // 4, by - r // 4), max(3, r // 2))

        ang = b.spin_angle
        pts = [(sx + math.cos(ang + k * math.tau / 5) * (r * 0.42), by + math.sin(ang + k * math.tau / 5) * (r * 0.42)) for k in range(5)]
        pygame.draw.polygon(self.screen, (32, 36, 44), pts)
        for k in range(5):
            px, py = pts[k]
            ex = sx + math.cos(ang + k * math.tau / 5) * (r - 1)
            ey = by + math.sin(ang + k * math.tau / 5) * (r - 1)
            pygame.draw.line(self.screen, (55, 60, 72), (px, py), (ex, ey), 2)
        pygame.draw.circle(self.screen, BLACK, (sx, by), r, 2)

    def render_first_person_3d(self):
        st = self.stadium
        cam_p = self.team1[self.active1_idx]
        horizon_y = TOP_HUD + 170
        pygame.draw.rect(self.screen, st["sky"], (0, TOP_HUD, WIDTH, horizon_y - TOP_HUD))
        pygame.draw.rect(self.screen, st["stands"], (0, horizon_y - 34, WIDTH, 34))
        pygame.draw.rect(self.screen, st["turf_a"], (0, horizon_y, WIDTH, HEIGHT - horizon_y))

        for row in range(8):
            y0 = int(horizon_y + ((row / 8.0) ** 1.7) * (HEIGHT - horizon_y))
            y1 = int(horizon_y + (((row + 1) / 8.0) ** 1.7) * (HEIGHT - horizon_y))
            pygame.draw.rect(self.screen, st["turf_a"] if row % 2 == 0 else st["turf_b"], (0, y0, WIDTH, max(1, y1 - y0)))

        cam_x, cam_y, fov = cam_p.x - 130.0, cam_p.y, 540.0

        def project(wx, wy, wz=0.0):
            depth = wx - cam_x
            if depth < 25.0:
                return None
            scale = fov / depth
            return WIDTH // 2 + (wy - cam_y) * scale * 1.35, horizon_y + (55.0 - wz) * scale, scale

        gx = PITCH_X + PITCH_W
        g_bl, g_br, g_tl, g_tr = project(gx, GOAL_TOP, 0), project(gx, GOAL_BOTTOM, 0), project(gx, GOAL_TOP, 74), project(gx, GOAL_BOTTOM, 74)
        if g_bl and g_br and g_tl and g_tr:
            pygame.draw.polygon(self.screen, (20, 28, 38), [(g_bl[0], g_bl[1]), (g_br[0], g_br[1]), (g_tr[0], g_tr[1]), (g_tl[0], g_tl[1])])
            pygame.draw.line(self.screen, st["goal_post"], (g_bl[0], g_bl[1]), (g_tl[0], g_tl[1]), 5)
            pygame.draw.line(self.screen, st["goal_post"], (g_br[0], g_br[1]), (g_tr[0], g_tr[1]), 5)
            pygame.draw.line(self.screen, st["goal_post"], (g_tl[0], g_tl[1]), (g_tr[0], g_tr[1]), 5)

        entities = [(p.x, "player", p, idx == self.active1_idx) for idx, p in enumerate(self.team1)] + [(p.x, "player", p, False) for p in self.team2] + [(self.ball.x, "ball", self.ball, False)]
        entities.sort(key=lambda e: e[0], reverse=True)
        for _, kind, obj, is_act in entities:
            proj = project(obj.x, obj.y, obj.z if kind == "ball" else 0.0)
            if not proj:
                continue
            sx, sy, sc = proj
            if kind == "ball":
                br = max(5, int(BALL_RADIUS * sc * 1.4))
                pygame.draw.circle(self.screen, WHITE, (int(sx), int(sy - br * 0.4)), br)
                pygame.draw.circle(self.screen, (32, 36, 44), (int(sx), int(sy - br * 0.4)), max(2, br // 3))
                pygame.draw.circle(self.screen, BLACK, (int(sx), int(sy - br * 0.4)), br, 2)
            else:
                ph, pw = max(18, int(52 * sc)), max(12, int(28 * sc))
                body_rect = pygame.Rect(int(sx - pw // 2), int(sy - ph), pw, ph)
                pygame.draw.rect(self.screen, obj.color, body_rect, border_radius=6)
                pygame.draw.rect(self.screen, GOLD if is_act else WHITE, body_rect, 2, border_radius=6)
                pygame.draw.circle(self.screen, (240, 210, 185), (int(sx), int(sy - ph - pw * 0.25)), max(5, int(pw * 0.35)))
                if sc > 0.32:
                    self.draw_text(obj.stats["short"], self.font_xs, WHITE, int(sx), int(sy - ph - pw * 0.8))

        rw, rh, rx, ry = 190, 110, 18, TOP_HUD + 14
        pygame.draw.rect(self.screen, (15, 24, 34), (rx, ry, rw, rh), border_radius=8)
        pygame.draw.rect(self.screen, CYAN, (rx, ry, rw, rh), 2, border_radius=8)
        for p in self.team1:
            pygame.draw.circle(self.screen, GOLD if p is cam_p else BLUE, (rx + int((p.x - PITCH_X) / PITCH_W * rw), ry + int((p.y - PITCH_Y) / PITCH_H * rh)), 4)
        for p in self.team2:
            pygame.draw.circle(self.screen, RED, (rx + int((p.x - PITCH_X) / PITCH_W * rw), ry + int((p.y - PITCH_Y) / PITCH_H * rh)), 4)
        pygame.draw.circle(self.screen, WHITE, (rx + int((self.ball.x - PITCH_X) / PITCH_W * rw), ry + int((self.ball.y - PITCH_Y) / PITCH_H * rh)), 3)

    def draw_hud(self):
        pygame.draw.rect(self.screen, DARK_PANEL, (0, 0, WIDTH, TOP_HUD))
        pygame.draw.line(self.screen, self.stadium["accent"], (0, TOP_HUD), (WIDTH, TOP_HUD), 2)
        active_p = self.team1[self.active1_idx]
        pygame.draw.rect(self.screen, BLUE, (20, 14, 10, 54), border_radius=4)
        self.draw_text(f"YOU ({active_p.stats['short']} OVR {active_p.stats['ovr']})", self.font_sm, WHITE, 40, 18, center=False)
        self.draw_text(str(self.score1), self.font_lg, WHITE, 290, 41)

        mins, secs = int(self.time_left) // 60, int(self.time_left) % 60
        t_str = f"ET {mins:02d}:{secs:02d}" if self.extra_time else f"{mins:02d}:{secs:02d}"
        pygame.draw.rect(self.screen, CARD_BG, (WIDTH // 2 - 110, 10, 220, 62), border_radius=12)
        self.draw_text(t_str, self.font_lg, GOLD if self.extra_time or self.time_left <= 15 else WHITE, WIDTH // 2, 33)
        self.draw_text(self.stadium["name"], self.font_xs, self.stadium["accent"], WIDTH // 2, 59)

        pygame.draw.rect(self.screen, RED, (WIDTH - 30, 14, 10, 54), border_radius=4)
        self.draw_text(str(self.score2), self.font_lg, WHITE, WIDTH - 290, 41)
        diff_lbl = ["EASY", "MED", "HARD", "LEGEND"][max(0, min(3, self.match_ai_difficulty - 1))]
        self.draw_text(f"{self.opponent_club_name} ({diff_lbl})", self.font_xs, MUTED_TEXT, WIDTH - 140, 18)

        cam_rect = pygame.Rect(40, 46, 118, 28)
        pygame.draw.rect(self.screen, CARD_BG, cam_rect, border_radius=8)
        self.draw_text("CAM: " + ("1ST-P" if self.camera_mode == "fp" else "2D"), self.font_xs, CYAN, cam_rect.centerx, cam_rect.centery)
        self.buttons["cam_btn"] = cam_rect

        auto_rect = pygame.Rect(166, 46, 98, 28)
        pygame.draw.rect(self.screen, GREEN if self.auto_ai else CARD_BG, auto_rect, border_radius=8)
        self.draw_text("AUTO: ON" if self.auto_ai else "AUTO: OFF", self.font_xs, BLACK if self.auto_ai else GOLD, auto_rect.centerx, auto_rect.centery)
        self.buttons["auto_ai_btn"] = auto_rect

        pause_rect = pygame.Rect(WIDTH - 165, 46, 120, 28)
        pygame.draw.rect(self.screen, CARD_BG, pause_rect, border_radius=8)
        self.draw_text("PAUSE / SUBS", self.font_xs, WHITE, pause_rect.centerx, pause_rect.centery)
        self.buttons["pause_btn"] = pause_rect

        if self.commentary_timer > 0 and self.commentary_banner:
            self.draw_text(self.commentary_banner, self.font_sm, GOLD, WIDTH // 2, TOP_HUD + 18)

    # -----------------------------------------------------------------------
    # SCREENS (MENU, LEAGUE, UCL, BALLON D'OR, TROPHIES, CEREMONY, DOWNLOADS)
    # -----------------------------------------------------------------------
    def render_menu(self):
        self.buttons.clear()
        self.screen.blit(self._get_pitch_surface(), (0, 0), area=pygame.Rect(0, 0, WIDTH, HEIGHT))
        self.screen.blit(self._dim_overlay, (0, 0))

        self.draw_club_crest(95, 68, scale=0.95)
        self.draw_text("STRIKER ARENA 6v6", self.font_xl, WHITE, WIDTH // 2, 48)
        self.draw_text(f"Coins: {self.career.coins:,}  |  Team Strength: {self.career.get_team_strength()}  |  Titles: {self.career.trophies}  |  Audio: {self.sound.backend}", self.font_sm, GOLD, WIDTH // 2, 92)

        bw, bh = 360, 56
        lx, rx = WIDTH // 2 - bw - 18, WIDTH // 2 + 18

        self.draw_button("play_ai", pygame.Rect(lx, 126, bw, bh), f"6v6 VS CPU ({['EASY','MED','HARD'][self.ai_difficulty]})", GREEN, "5 Outfield + GK • Right-Click to change Diff")
        self.draw_button("league", pygame.Rect(rx, 126, bw, bh), f"LEAGUE MODE (RD {self.career.league_round + 1}/{len(self.career.league_teams)-1})", GOLD, "All 9 Clubs Play • Top 6 -> Champions League")
        self.draw_button("ucl", pygame.Rect(lx, 194, bw, bh), "CHAMPIONS LEAGUE (KNOCKOUT)", CYAN, "Top 6 + 6 Foreign Clubs • Pure Knockout Only")
        self.draw_button("ballondor", pygame.Rect(rx, 194, bw, bh), "BALLON D'OR & TOP SCORERS", PINK, "Live Ballon d'Or Rankings & Golden Boot")
        self.draw_button("game_plan", pygame.Rect(lx, 262, bw, bh), "GAME PLAN / SQUAD (eFootball)", CYAN, "6 Pitch + 4 Bench + Reserves + Move Pos")
        self.draw_button("market", pygame.Rect(rx, 262, bw, bh), "TRANSFER MARKET & STARS", PURPLE, f"{len(PLAYER_CATALOG)} Players • 14 Clubs + Free Base")
        self.draw_button("packs", pygame.Rect(lx, 330, bw, bh), "RASHFORD 10-PLAYER EPIC PACK", GOLD, "1 EPIC Rashford (102 OVR) + 9 Base Players")
        self.draw_button("trophies", pygame.Rect(rx, 330, bw, bh), f"CLUB TROPHIES & STARS ({self.career.trophies})", GOLD, "View Crest Stars, League & UCL Titles")
        self.draw_button("downloads", pygame.Rect(lx, 398, bw, bh), "DOWNLOAD PACKS & LINKS", ORANGE, "Hafid Danger, Menu BGM, Card Photo Links")
        self.draw_button("stadiums", pygame.Rect(rx, 398, bw, bh), f"STADIUM: {self.stadium['name']} (8 Total)", self.stadium["accent"], "Includes Spotify Camp Nou & Animated Crowd")
        self.draw_button("create_room", pygame.Rect(lx, 466, bw, 52), "CREATE ROOM (HOST)", GOLD, "Get Room Code & play vs Friend")
        self.draw_button("join_room", pygame.Rect(rx, 466, bw, 52), "JOIN FRIEND'S ROOM", CYAN, "Enter Friend's Room Code / IP")
        self.draw_button("settings", pygame.Rect(WIDTH // 2 - 200, 534, 400, 50), "SETTINGS (SMART ASSIST / AUDIO / CAM)", WHITE)

    def render_league(self):
        self.buttons.clear()
        self.screen.fill(DARK_PANEL)
        total_r = len(self.career.league_teams) - 1
        self.draw_text("STRIKER PREMIER LEAGUE (ALL 9 CLUBS PLAY EVERY ROUND)", self.font_lg, GOLD, WIDTH // 2, 36)
        self.draw_text(f"Round {self.career.league_round + 1} of {total_r}  •  Green Top 6 Qualify for Champions League!", self.font_sm, MUTED_TEXT, WIDTH // 2, 68)

        table_rect = pygame.Rect(40, 95, 740, 405)
        pygame.draw.rect(self.screen, CARD_BG, table_rect, border_radius=14)
        pygame.draw.rect(self.screen, GOLD, table_rect, 2, border_radius=14)
        xs = [75, 195, 385, 440, 495, 550, 610, 685]
        for h, hx in zip(["POS", "CLUB", "P", "W", "D", "L", "GD", "PTS"], xs):
            self.draw_text(h, self.font_sm, GOLD, hx, 120)
        for idx, (name, p, w, d, l, gd, pts) in enumerate(self.career.get_standings()):
            ry = 158 + idx * 36
            col = CYAN if name == "Your Club" else (GREEN if idx < 6 else WHITE)
            for v, hx in zip([str(idx + 1), name, str(p), str(w), str(d), str(l), f"{gd:+d}", str(pts)], xs):
                self.draw_text(v, self.font_sm, col, hx, ry)

        # League Top Scorers Panel
        sc_rect = pygame.Rect(800, 95, 360, 405)
        pygame.draw.rect(self.screen, CARD_BG, sc_rect, border_radius=14)
        pygame.draw.rect(self.screen, CYAN, sc_rect, 2, border_radius=14)
        self.draw_text("LEAGUE TOP SCORERS", self.font_md, CYAN, sc_rect.centerx, 124)
        top_sc = sorted(self.career.league_scorers.items(), key=lambda kv: kv[1], reverse=True)[:8]
        if not top_sc:
            self.draw_text("No goals scored yet", self.font_sm, MUTED_TEXT, sc_rect.centerx, 260)
        for idx, (pid, g) in enumerate(top_sc):
            st = CATALOG_BY_ID.get(pid)
            nm = st["short"] if st else pid
            self.draw_text(f"{idx+1}. {nm} ({st['club'] if st else ''})", self.font_sm, WHITE, sc_rect.left + 22, 165 + idx * 38, center=False)
            self.draw_text(f"{g} G", self.font_sm, GOLD, sc_rect.right - 35, 165 + idx * 38)

        opp = self.career.get_current_league_opponent()
        club = CLUBS_DATA[opp]
        diff_lbl = ["EASY", "MEDIUM", "HARD"][club["difficulty"] - 1]
        self.draw_button("play_league", pygame.Rect(WIDTH // 2 - 220, 520, 440, 62), f"PLAY VS {opp.upper()} ({diff_lbl})", GREEN, f"Club OVR {club['rating']} • All Other Teams Simulate!")
        self.draw_button("back_menu", pygame.Rect(WIDTH // 2 - 120, 598, 240, 50), "BACK", WHITE)

    def render_ucl(self):
        self.buttons.clear()
        self.screen.fill((12, 18, 42))
        self.draw_text("UEFA-STYLE CHAMPIONS LEAGUE (KNOCKOUT ONLY)", self.font_lg, CYAN, WIDTH // 2, 40)
        self.draw_text("Top 6 League Teams + 6 Foreign League Clubs (AC Milan, Juventus, Dortmund, Leverkusen, Al-Nassr, Al-Hilal)", self.font_xs, MUTED_TEXT, WIDTH // 2, 74)
        if self.ucl_msg:
            self.draw_text(self.ucl_msg, self.font_sm, GOLD, WIDTH // 2, 100)

        br_rect = pygame.Rect(40, 122, 740, 390)
        pygame.draw.rect(self.screen, CARD_BG, br_rect, border_radius=14)
        pygame.draw.rect(self.screen, CYAN, br_rect, 2, border_radius=14)

        if self.career.ucl_active:
            diff_lbl = ["EASY-MED", "MEDIUM", "HARD", "LEGEND BOSS"][self.career.get_ucl_difficulty() - 1]
            self.draw_text(f"CURRENT STAGE: {self.career.ucl_round_name.upper()}  (DIFFICULTY: {diff_lbl})", self.font_md, GOLD, br_rect.centerx, 152)
            for idx, (ca, cb) in enumerate(self.career.ucl_matches):
                y = 205 + idx * 54
                col = CYAN if "Your Club" in (ca, cb) else WHITE
                self.draw_text(f"{ca}   VS   {cb}", self.font_md, col, br_rect.centerx, y)
            if self.career.ucl_byes:
                self.draw_text("Direct QF Seeds (Top 4): " + ", ".join(self.career.ucl_byes), self.font_xs, GREEN, br_rect.centerx, 475)
        else:
            rank = self.career.get_your_league_rank()
            if self.career.ucl_champion:
                self.draw_text(f"LAST UCL CHAMPION: {self.career.ucl_champion.upper()}", self.font_lg, GOLD, br_rect.centerx, 250)
            self.draw_text(f"Your Current League Rank: #{rank} (Need Top 6 to Enter)", self.font_md, GREEN if rank <= 6 else RED, br_rect.centerx, 320)

        # UCL Top Scorers
        sc_rect = pygame.Rect(800, 122, 360, 390)
        pygame.draw.rect(self.screen, CARD_BG, sc_rect, border_radius=14)
        pygame.draw.rect(self.screen, GOLD, sc_rect, 2, border_radius=14)
        self.draw_text("UCL TOP SCORERS", self.font_md, GOLD, sc_rect.centerx, 152)
        top_sc = sorted(self.career.ucl_scorers.items(), key=lambda kv: kv[1], reverse=True)[:8]
        if not top_sc:
            self.draw_text("No UCL goals yet", self.font_sm, MUTED_TEXT, sc_rect.centerx, 280)
        for idx, (pid, g) in enumerate(top_sc):
            st = CATALOG_BY_ID.get(pid)
            nm = st["short"] if st else pid
            self.draw_text(f"{idx+1}. {nm} ({st['club'] if st else ''})", self.font_sm, WHITE, sc_rect.left + 22, 195 + idx * 36, center=False)
            self.draw_text(f"{g} G", self.font_sm, GOLD, sc_rect.right - 35, 195 + idx * 36)

        if self.career.ucl_active and self.career.get_your_ucl_match():
            opp = self.career.get_your_ucl_match()
            self.draw_button("play_ucl", pygame.Rect(WIDTH // 2 - 220, 535, 440, 62), f"PLAY {self.career.ucl_round_name.upper()} VS {opp.upper()}", GREEN, "Win to Advance • Lose = Eliminated!")
        elif self.career.ucl_active:
            self.draw_button("sim_ucl_round", pygame.Rect(WIDTH // 2 - 220, 535, 440, 62), "SIMULATE PLAYOFF ROUND (YOU HAVE BYE)", GOLD, "Top 4 League Seed — Direct to Quarter-Finals!")
        else:
            self.draw_button("start_ucl", pygame.Rect(WIDTH // 2 - 220, 535, 440, 62), "START CHAMPIONS LEAGUE KNOCKOUT", CYAN, "Requires Top 6 in League Standings")
        self.draw_button("back_menu", pygame.Rect(WIDTH // 2 - 120, 612, 240, 50), "BACK", WHITE)

    def render_ballon_dor(self):
        self.buttons.clear()
        self.screen.fill((22, 18, 32))
        self.draw_text("BALLON D'OR RANKINGS (TOP 10)", self.font_xl, GOLD, WIDTH // 2, 46)
        self.draw_text("Points = Player OVR + (League Goals x 3) + (UCL Goals x 5) + Trophy Bonus", self.font_sm, MUTED_TEXT, WIDTH // 2, 82)
        box = pygame.Rect(110, 110, 980, 460)
        pygame.draw.rect(self.screen, CARD_BG, box, border_radius=14)
        pygame.draw.rect(self.screen, GOLD, box, 2, border_radius=14)
        xs = [165, 310, 510, 650, 760, 870, 995]
        for h, hx in zip(["RANK", "PLAYER", "CLUB", "OVR", "LEAGUE G", "UCL G", "SCORE"], xs):
            self.draw_text(h, self.font_sm, GOLD, hx, 140)
        for idx, (pid, short, club, ovr, lg, ug, sc) in enumerate(self.career.get_ballon_dor_top10()):
            ry = 180 + idx * 38
            col = GOLD if idx == 0 else (CYAN if pid in (self.career.lineup + self.career.bench) else WHITE)
            for v, hx in zip([f"#{idx+1}", short, club, str(ovr), str(lg), str(ug), str(sc)], xs):
                self.draw_text(v, self.font_sm, col, hx, ry)
        self.draw_button("back_menu", pygame.Rect(WIDTH // 2 - 120, 595, 240, 52), "BACK", WHITE)

    def render_trophies(self):
        self.buttons.clear()
        self.screen.fill((16, 20, 38))
        self.draw_text("CLUB TROPHIES & CHAMPIONSHIP STARS", self.font_xl, GOLD, WIDTH // 2, 52)
        self.draw_club_crest(WIDTH // 2, 185, scale=2.2)
        self.draw_text(f"Gold Stars (League): {self.career.league_titles}   |   Cyan Stars (UCL): {self.career.ucl_titles}", self.font_md, WHITE, WIDTH // 2, 285)

        cards = [
            ("PREMIER LEAGUE TITLES", self.career.league_titles, GOLD, 220),
            ("CHAMPIONS LEAGUE TITLES", self.career.ucl_titles, CYAN, WIDTH // 2),
            ("TOTAL TROPHIES", self.career.trophies, GREEN, WIDTH - 220),
        ]
        for title, val, col, cx in cards:
            r = pygame.Rect(cx - 155, 340, 310, 170)
            pygame.draw.rect(self.screen, CARD_BG, r, border_radius=16)
            pygame.draw.rect(self.screen, col, r, 3, border_radius=16)
            self.draw_text(title, self.font_sm, col, cx, 380)
            self.draw_text(str(val), self.font_xl, WHITE, cx, 445)
        self.draw_button("back_menu", pygame.Rect(WIDTH // 2 - 120, 575, 240, 54), "BACK", WHITE)

    def render_trophy_ceremony(self):
        self.buttons.clear()
        self.screen.fill((12, 14, 34))
        t = time.time()
        # Animated confetti & spotlights
        for k in range(36):
            cx = int((k * 97 + t * 80) % WIDTH)
            cy = int((k * 61 + t * 140) % HEIGHT)
            pygame.draw.circle(self.screen, random.Random(k).choice([GOLD, CYAN, WHITE, PINK]), (cx, cy), 5)

        self.draw_text("CHAMPIONS CELEBRATION!", self.font_xl, self.ceremony_color, WIDTH // 2, 72)
        self.draw_text(self.ceremony_title, self.font_lg, WHITE, WIDTH // 2, 122)
        self.draw_text(self.ceremony_sub, self.font_md, GOLD, WIDTH // 2, 165)

        # Draw Trophy Cup
        tx, ty = WIDTH // 2, 320
        pygame.draw.polygon(self.screen, self.ceremony_color, [(tx - 65, ty - 70), (tx + 65, ty - 70), (tx + 35, ty + 20), (tx - 35, ty + 20)])
        pygame.draw.rect(self.screen, self.ceremony_color, (tx - 14, ty + 20, 28, 45))
        pygame.draw.rect(self.screen, GOLD, (tx - 48, ty + 62, 96, 22), border_radius=6)
        pygame.draw.circle(self.screen, self.ceremony_color, (tx - 68, ty - 35), 24, 5)
        pygame.draw.circle(self.screen, self.ceremony_color, (tx + 68, ty - 35), 24, 5)

        self.draw_club_crest(WIDTH // 2, 475, scale=1.4)
        self.draw_button("quit_menu", pygame.Rect(WIDTH // 2 - 160, 575, 320, 58), "CONTINUE TO MENU", GREEN)

    def _draw_mini_card(self, key, rect, pid, is_sel=False):
        st = self.career.get_card_stats(pid)
        col = PINK if st["is_epic"] else (CYAN if st["card_type"] == "HIGHLIGHT" else (GREEN if st["card_type"] == "STANDARD" else MUTED_TEXT))
        pygame.draw.rect(self.screen, CARD_HOVER if is_sel else CARD_BG, rect, border_radius=8)
        pygame.draw.rect(self.screen, GOLD if is_sel else col, rect, 3 if is_sel else 2, border_radius=8)
        self.screen.blit(pygame.transform.smoothscale(self._get_portrait(pid), (38, 38)), (rect.left + 6, rect.top + 6))
        self.draw_text(f"{st['ovr']}", self.font_md, GOLD, rect.right - 22, rect.top + 18)
        self.draw_text(f"{st['pos']}", self.font_xs, WHITE, rect.right - 22, rect.top + 36)
        self.draw_text(st["short"][:10], self.font_xs, WHITE, rect.centerx, rect.bottom - 12)
        self.buttons[key] = rect

    def render_game_plan(self):
        self.buttons.clear()
        self.screen.fill((14, 24, 52))
        self.draw_text("GAME PLAN — SQUAD & FORMATION", self.font_lg, WHITE, WIDTH // 2, 28)
        if self.gp_msg:
            self.draw_text(self.gp_msg, self.font_sm, GOLD, WIDTH // 2, 52)

        left = pygame.Rect(20, 68, 235, 646)
        pygame.draw.rect(self.screen, DARK_PANEL, left, border_radius=12)
        self.draw_text("TEAM STRENGTH", self.font_sm, MUTED_TEXT, left.centerx, 94)
        self.draw_text(str(self.career.get_team_strength()), self.font_xl, GOLD, left.centerx, 130)

        mgr = self.career.manager
        self.draw_button("gp_mgr", pygame.Rect(34, 174, 206, 70), mgr["name"], GOLD, f"{mgr['style']} ({mgr['boost']})")
        self.draw_button("gp_form", pygame.Rect(34, 256, 206, 56), self.career.formation["name"], CYAN, "Tap to change Formation")
        self.draw_button("gp_move", pygame.Rect(34, 324, 206, 56), "MOVE POS: " + ("ON" if self.move_pos_mode else "OFF"), ORANGE if self.move_pos_mode else WHITE, "Move player anywhere on pitch")
        self.draw_button("gp_reserves", pygame.Rect(34, 392, 206, 56), f"RESERVES ({len(self.career.get_reserves())})", GREEN, "Put Reserve players into Pitch/Bench")
        self.draw_button("gp_reset_pos", pygame.Rect(34, 460, 206, 44), "RESET POSITIONS", MUTED_TEXT)
        self.draw_button("back_menu", pygame.Rect(34, 636, 206, 54), "BACK", WHITE)

        pitch_r = pygame.Rect(275, 68, 610, 646)
        pygame.draw.rect(self.screen, (26, 98, 52), pitch_r, border_radius=12)
        pygame.draw.rect(self.screen, WHITE, pitch_r, 3, border_radius=12)
        pygame.draw.line(self.screen, WHITE, (pitch_r.left, pitch_r.centery), (pitch_r.right, pitch_r.centery), 2)
        pygame.draw.circle(self.screen, WHITE, pitch_r.center, 58, 2)
        pygame.draw.rect(self.screen, WHITE, (pitch_r.centerx - 120, pitch_r.bottom - 95, 240, 95), 2)
        self.buttons["gp_pitch_area"] = pitch_r

        for i in range(5):
            ox, oy = self.career.get_slot_offset(i)
            px = pitch_r.centerx + int(oy / 420.0 * 240)
            py = pitch_r.top + 60 + int((-ox - 120) / 620.0 * 420)
            px = max(pitch_r.left + 58, min(pitch_r.right - 58, px))
            py = max(pitch_r.top + 42, min(pitch_r.bottom - 125, py))
            self._draw_mini_card(f"slot_pitch_{i}", pygame.Rect(px - 52, py - 34, 104, 68), self.career.lineup[i], self.selected_slot == ("pitch", i))

        self._draw_mini_card("slot_gk_0", pygame.Rect(pitch_r.centerx - 52, pitch_r.bottom - 82, 104, 68), self.career.gk_id, self.selected_slot == ("gk", 0))

        right = pygame.Rect(905, 68, 275, 646)
        pygame.draw.rect(self.screen, DARK_PANEL, right, border_radius=12)
        self.draw_text("BENCH (4 SUBS)", self.font_md, GOLD, right.centerx, 92)
        for i in range(4):
            self._draw_mini_card(f"slot_bench_{i}", pygame.Rect(925, 122 + i * 115, 235, 92), self.career.bench[i], self.selected_slot == ("bench", i))

        if self.reserves_open:
            self.buttons.clear()
            self.screen.blit(self._dim_overlay, (0, 0))
            pop = pygame.Rect(110, 60, 980, 620)
            pygame.draw.rect(self.screen, DARK_PANEL, pop, border_radius=16)
            pygame.draw.rect(self.screen, CYAN, pop, 3, border_radius=16)
            self.draw_text("RESERVES — Tap any player to select, then tap Pitch/Bench!", self.font_lg, WHITE, WIDTH // 2, 98)
            res = self.career.get_reserves()
            start = self.reserves_page * 12
            for idx, pid in enumerate(res[start : start + 12]):
                col_i, row_i = idx % 4, idx // 4
                self._draw_mini_card(f"pick_res_{pid}", pygame.Rect(150 + col_i * 225, 140 + row_i * 125, 200, 100), pid, False)
            self.draw_button("res_prev", pygame.Rect(180, 595, 160, 50), "< PREV", CYAN)
            self.draw_button("res_next", pygame.Rect(360, 595, 160, 50), "NEXT >", CYAN)
            self.draw_button("close_reserves", pygame.Rect(WIDTH - 340, 595, 180, 50), "CLOSE", RED)

    def render_market(self):
        self.buttons.clear()
        self.screen.fill(DARK_PANEL)
        total_pages = (len(PLAYER_CATALOG) + 4) // 5
        self.draw_text("TRANSFER MARKET (14 CLUBS + 15 FREE BASE)", self.font_lg, WHITE, WIDTH // 2, 34)
        self.draw_text(f"Coins: {self.career.coins:,}  |  Page {self.market_page + 1}/{total_pages}  |  Owned: {len(self.career.owned)}/{len(PLAYER_CATALOG)}", self.font_sm, GOLD, WIDTH // 2, 66)
        if self.market_msg:
            self.draw_text(self.market_msg, self.font_sm, GREEN, WIDTH // 2, 92)

        cards = PLAYER_CATALOG[self.market_page * 5 : self.market_page * 5 + 5]
        cw, ch, gap = 216, 424, 18
        sx = (WIDTH - (len(cards) * cw + (len(cards) - 1) * gap)) // 2

        for idx, base in enumerate(cards):
            pid = base["id"]
            st = self.career.get_card_stats(pid)
            owned = pid in self.career.owned
            x, y = sx + idx * (cw + gap), 116
            col = PINK if st["is_epic"] else (CYAN if st["card_type"] == "HIGHLIGHT" else (GREEN if owned else MUTED_TEXT))
            card = pygame.Rect(x, y, cw, ch)
            pygame.draw.rect(self.screen, CARD_BG, card, border_radius=14)
            pygame.draw.rect(self.screen, col, card, 3, border_radius=14)

            self.screen.blit(self._get_portrait(pid), (x + 14, y + 14))
            self.draw_text(st["card_type"], self.font_xs, col, x + cw - 46, y + 18)
            self.draw_text(str(st["ovr"]), self.font_lg, GOLD, x + cw - 46, y + 42)
            self.draw_text(f"{st['pos']} #{st['num']}", self.font_xs, WHITE, x + cw - 46, y + 66)
            self.draw_text(st["short"], self.font_md, WHITE, x + cw // 2, y + 98)
            self.draw_text(f"{st['club']} • {st['nation']}", self.font_xs, GOLD, x + cw // 2, y + 120)
            self.draw_text(st["match"][:26], self.font_xs, CYAN, x + cw // 2, y + 142)
            self.draw_text(f"PAC {st['pac']}   SHO {st['sho']}", self.font_sm, WHITE, x + cw // 2, y + 174)
            self.draw_text(f"PAS {st['pas']}   DRI {st['dri']}", self.font_sm, WHITE, x + cw // 2, y + 198)
            self.draw_text("Skill: " + (", ".join(st["skills"])[:22] if st["skills"] else "None"), self.font_xs, GREEN if st["skills"] else MUTED_TEXT, x + cw // 2, y + 228)
            if st["booster"]:
                self.draw_text("Booster: " + st["booster"], self.font_xs, GOLD, x + cw // 2, y + 250)

            if owned:
                self.draw_button(f"gear_{pid}", pygame.Rect(x + 14, y + 292, cw - 28, 46), "EDIT STATS [GEAR]", CYAN)
                self.draw_button(f"sell_{pid}", pygame.Rect(x + 14, y + 350, cw - 28, 44), f"SELL +{int(base['price'] * 0.7)}", RED)
            else:
                lbl = "SIGN FREE" if base["price"] == 0 else f"BUY {base['price']}"
                self.draw_button(f"buy_{pid}", pygame.Rect(x + 14, y + 325, cw - 28, 56), lbl, GREEN)

        self.draw_button("mkt_prev", pygame.Rect(WIDTH // 2 - 280, 572, 160, 48), "< PREV 5", CYAN)
        self.draw_button("mkt_next", pygame.Rect(WIDTH // 2 + 120, 572, 160, 48), "NEXT 5 >", CYAN)
        self.draw_button("back_menu", pygame.Rect(WIDTH // 2 - 95, 636, 190, 50), "BACK", WHITE)

    def render_stat_editor(self):
        self.buttons.clear()
        self.screen.fill(DARK_PANEL)
        pid = self.edit_pid
        st = self.career.get_card_stats(pid)
        self.draw_text(f"PLAYER PROGRESSION — {st['name'].upper()}", self.font_lg, CYAN, WIDTH // 2, 54)
        self.screen.blit(self._get_portrait(pid), (WIDTH // 2 - 32, 90))
        self.draw_text(f"Effective OVR: {st['ovr']} (Cap: {105 if st['is_epic'] else 99})", self.font_md, GOLD, WIDTH // 2, 180)
        for idx, (sk, label) in enumerate([("pac", "PACE"), ("sho", "SHOOTING"), ("pas", "PASSING"), ("dri", "DRIBBLING")]):
            y = 240 + idx * 80
            self.draw_text(f"{label}:  {st[sk]}", self.font_md, WHITE, WIDTH // 2 - 80, y)
            self.draw_button(f"stat_sub_{sk}", pygame.Rect(WIDTH // 2 + 100, y - 24, 56, 48), "-1", RED)
            self.draw_button(f"stat_add_{sk}", pygame.Rect(WIDTH // 2 + 170, y - 24, 56, 48), "+1", GREEN)
        self.draw_button("back_market", pygame.Rect(WIDTH // 2 - 120, 585, 240, 52), "SAVE & BACK", WHITE)

    def render_packs(self):
        self.buttons.clear()
        self.screen.fill((16, 22, 48))
        pygame.draw.circle(self.screen, (32, 54, 115), (WIDTH // 2, HEIGHT // 2), 340)
        pygame.draw.circle(self.screen, (45, 75, 145), (WIDTH // 2, HEIGHT // 2), 210)

        if self.pack_result and self.pack_result["rarity"] == "EPIC":
            t = time.time() * 4
            for k in range(8):
                col = (int(127 + 127 * math.sin(t + k)), int(127 + 127 * math.sin(t + k + 2)), int(127 + 127 * math.sin(t + k + 4)))
                pygame.draw.line(self.screen, col, (WIDTH // 2, HEIGHT // 2 - 30), (k * 180, 0), 16)
                pygame.draw.line(self.screen, col, (WIDTH // 2, HEIGHT // 2 - 30), (k * 180, HEIGHT), 16)

        self.draw_text("MAN UTD RASHFORD 10-PLAYER PACK", self.font_xl, GOLD, WIDTH // 2, 56)
        self.draw_text("1 EPIC Rashford (102 OVR + Loop Scream) & 9 Base Players", self.font_sm, CYAN, WIDTH // 2, 98)
        day_status = "TODAY IS PACK DAY (MON/THU) — FREE PACK READY!" if self.career.is_pack_day() else "Next Free Pack: Monday or Thursday (Or open for 1,000 Coins)"
        self.draw_text(day_status, self.font_md, GREEN if self.career.is_pack_day() else WHITE, WIDTH // 2, 138)

        if self.pack_result:
            pid = self.pack_result["pid"]
            st = self.career.get_card_stats(pid)
            is_epic = self.pack_result["rarity"] == "EPIC"
            card_surf = pygame.Surface((280, 270), pygame.SRCALPHA)
            pygame.draw.rect(card_surf, CARD_BG, (0, 0, 280, 270), border_radius=16)
            pygame.draw.rect(card_surf, PINK if is_epic else GREEN, (0, 0, 280, 270), 4, border_radius=16)
            card_surf.blit(self._get_portrait(pid), (108, 18))
            card_surf.blit(self.font_md.render(self.pack_result["rarity"], True, PINK if is_epic else GREEN), (105, 92))
            t_n = self.font_lg.render(f"{st['short']} (OVR {st['ovr']})", True, WHITE)
            card_surf.blit(t_n, t_n.get_rect(center=(140, 142)))
            if st["booster"]:
                t_b = self.font_xs.render(f"Booster: {st['booster']}", True, GOLD)
                card_surf.blit(t_b, t_b.get_rect(center=(140, 174)))
            if st["skills"]:
                t_s = self.font_xs.render("Skills: " + ", ".join(st["skills"]), True, GREEN)
                card_surf.blit(t_s, t_s.get_rect(center=(140, 202)))
            t_m = self.font_xs.render(st["match"][:30], True, CYAN)
            card_surf.blit(t_m, t_m.get_rect(center=(140, 232)))
            if is_epic:
                rot = pygame.transform.rotozoom(card_surf, (time.time() * 90) % 360, 1.0)
                self.screen.blit(rot, rot.get_rect(center=(WIDTH // 2, 325)))
            else:
                self.screen.blit(card_surf, card_surf.get_rect(center=(WIDTH // 2, 325)))
            self.draw_text(self.pack_msg, self.font_md, GREEN, WIDTH // 2, 475)
        else:
            box = pygame.Rect(WIDTH // 2 - 110, 195, 220, 270)
            pygame.draw.rect(self.screen, (165, 28, 36), box, border_radius=18)
            pygame.draw.rect(self.screen, GOLD, box, 4, border_radius=18)
            self.draw_text("MAN UTD", self.font_lg, GOLD, box.centerx, box.top + 60)
            self.draw_text("EPIC PACK", self.font_xl, WHITE, box.centerx, box.centery)
            self.draw_text("10 PLAYERS", self.font_md, CYAN, box.centerx, box.bottom - 55)
            if self.pack_msg:
                self.draw_text(self.pack_msg, self.font_md, RED, WIDTH // 2, 480)

        self.draw_button("open_free_pack", pygame.Rect(WIDTH // 2 - 360, 515, 340, 62), "OPEN FREE MON/THU PACK", GREEN)
        self.draw_button("open_coin_pack", pygame.Rect(WIDTH // 2 + 20, 515, 340, 62), "OPEN PACK (1,000 COINS)", GOLD, f"Your Coins: {self.career.coins:,}")
        self.draw_button("back_menu", pygame.Rect(WIDTH // 2 - 120, 602, 240, 50), "BACK", WHITE)

    def render_downloads(self):
        self.buttons.clear()
        self.screen.fill(DARK_PANEL)
        self.draw_text("DOWNLOADABLE AUDIO, CARD PHOTOS & LINKS", self.font_xl, WHITE, WIDTH // 2, 38)
        self.draw_text(f"Audio: {self.sound.backend}  |  Place downloaded files in packs/ subfolders!", self.font_xs, CYAN, WIDTH // 2, 72)
        if self.dl_msg:
            self.draw_text(self.dl_msg, self.font_sm, GREEN, WIDTH // 2, 98)

        packs_ui = [
            ("voice_hafid", "commentary_hafid", "HAFID DERRADJI (GOAL + KHATIRA!)", "Generates goal.wav & danger.wav in packs/commentary_hafid/", "url_hafid", 122),
            ("dl_menu_bgm", "menu_bgm", "MENU BACKGROUND MUSIC PACK", "Plays in menus, stops in match (packs/menu_bgm/menu_theme.wav)", "url_bgm", 196),
            ("dl_photos", "player_photos", "REAL MATCH CARD PHOTOS PACK", "Place <player_id>.png in packs/player_photos/ (e.g. rashford.png)", "url_photos", 270),
            ("dl_bg", "bg_crowd", "MATCH CROWD AUDIO PACK", "Generates packs/bg_crowd/crowd_loop.wav", None, 344),
            ("voice_spanish", "commentary_spanish", "SPANISH COMMENTARY PACK", "Generates & activates packs/commentary_spanish/goal.wav", None, 418),
            ("dl_stadium", "stadium_hd", "STADIUM HD TEXTURE PACK", "Enhances pitch lines & atmosphere", None, 492),
        ]
        for btn_k, p_k, title, sub, url_btn, y in packs_ui:
            inst = self.career.installed_packs.get(p_k, False)
            active_voice = (p_k == f"commentary_{self.sound.commentary_lang}")
            tag = "ACTIVE" if (active_voice and inst) else ("INSTALLED" if inst else "DOWNLOAD")
            w = 500 if url_btn else 720
            x = WIDTH // 2 - 360
            self.draw_button(btn_k, pygame.Rect(x, y, w, 62), f"{title} [{tag}]", GREEN if inst else CYAN, sub)
            if url_btn:
                self.draw_button(url_btn, pygame.Rect(x + w + 14, y, 206, 62), "OPEN IN CHROME", GOLD, "Direct Download Page")

        self.draw_button("test_sound", pygame.Rect(WIDTH // 2 - 260, 578, 240, 50), "TEST HAFID KHATIRA", GOLD)
        self.draw_button("back_menu", pygame.Rect(WIDTH // 2 + 20, 578, 240, 50), "BACK", WHITE)

    def render_settings(self):
        self.buttons.clear()
        self.screen.fill(DARK_PANEL)
        self.draw_text("GAME SETTINGS", self.font_xl, WHITE, WIDTH // 2, 54)
        bw, cx = 480, WIDTH // 2 - 240
        sa = self.career.smart_assist
        self.draw_button("toggle_sa", pygame.Rect(cx, 110, bw, 60), "SMART ASSIST: " + ("ON" if sa else "OFF"), GREEN if sa else RED, "Auto-aims passes & shots toward teammates/goal")
        self.draw_button("toggle_sfx", pygame.Rect(cx, 184, bw, 60), "SOUND EFFECTS: " + ("ON" if self.sound.enabled else "OFF"), GREEN if self.sound.enabled else RED)
        self.draw_button("toggle_menu_bgm", pygame.Rect(cx, 258, bw, 60), "MENU BACKGROUND MUSIC: " + ("ON" if self.sound.menu_bgm_enabled else "OFF"), GREEN if self.sound.menu_bgm_enabled else RED)
        self.draw_button("toggle_bg", pygame.Rect(cx, 332, bw, 60), "STADIUM CROWD AUDIO: " + ("ON" if self.sound.bg_enabled else "OFF"), GREEN if self.sound.bg_enabled else RED)
        self.draw_button("cam_toggle", pygame.Rect(cx, 406, bw, 60), "CAMERA: " + ("FIRST PERSON 3D" if self.camera_mode == "fp" else "CLASSIC 2D"), PURPLE)
        self.draw_button("duration", pygame.Rect(cx, 480, bw, 56), f"MATCH TIME: {self.match_duration // 60}m {self.match_duration % 60:02d}s", GOLD)
        self.draw_button("back_menu", pygame.Rect(WIDTH // 2 - 120, 575, 240, 52), "BACK", WHITE)

    def render_stadium_select(self):
        self.buttons.clear()
        self.screen.blit(self._get_pitch_surface(), (0, 0), area=pygame.Rect(0, 0, WIDTH, HEIGHT))
        self.screen.blit(self._dim_overlay, (0, 0))
        self.draw_text("SELECT STADIUM (8 ARENAS)", self.font_xl, WHITE, WIDTH // 2, 54)
        for i, st in enumerate(STADIUMS):
            col_i, row_i = i % 2, i // 2
            r = pygame.Rect(110 + col_i * 510, 110 + row_i * 115, 470, 92)
            self.draw_button(f"st_{i}", r, ("* " if i == self.stadium_idx else "") + st["name"], st["accent"], st["subtitle"])
            pygame.draw.rect(self.screen, st["turf_a"], (r.left + 16, r.top + 22, 46, 46), border_radius=8)
        self.draw_button("back_menu", pygame.Rect(WIDTH // 2 - 120, 600, 240, 52), "BACK", WHITE)

    def render_room_host(self):
        self.buttons.clear()
        self.screen.blit(self._get_pitch_surface(), (0, 0), area=pygame.Rect(0, 0, WIDTH, HEIGHT))
        self.screen.blit(self._dim_overlay, (0, 0))
        self.draw_text("ROOM CREATED — WAITING FOR FRIEND", self.font_lg, GOLD, WIDTH // 2, 110)
        card = pygame.Rect(WIDTH // 2 - 290, 165, 580, 260)
        pygame.draw.rect(self.screen, CARD_BG, card, border_radius=16)
        pygame.draw.rect(self.screen, GOLD, card, 2, border_radius=16)
        self.draw_text("SHARE THIS ROOM CODE WITH YOUR FRIEND:", self.font_sm, MUTED_TEXT, WIDTH // 2, 205)
        self.draw_text(self.net.room_code, self.font_xl, CYAN, WIDTH // 2, 260)
        self.draw_text(f"Direct IP: {self.net.local_ip}:{self.net.port}", self.font_md, WHITE, WIDTH // 2, 315)
        if self.net.connected:
            self.draw_text("FRIEND CONNECTED!", self.font_md, GREEN, WIDTH // 2, 375)
            self.draw_button("host_start", pygame.Rect(WIDTH // 2 - 170, 465, 340, 64), "START MATCH NOW", GREEN)
        elif self.net.error:
            self.draw_text(self.net.error, self.font_sm, RED, WIDTH // 2, 375)
        else:
            self.draw_text("Waiting for friend to join" + "." * (int(time.time() * 2) % 4), self.font_md, GOLD, WIDTH // 2, 375)
        self.draw_button("stadiums", pygame.Rect(WIDTH // 2 - 170, 545, 340, 52), f"Stadium: {self.stadium['name']}", self.stadium["accent"])
        self.draw_button("cancel_room", pygame.Rect(WIDTH // 2 - 120, 615, 240, 50), "CANCEL", RED)

    def render_room_join(self):
        self.buttons.clear()
        self.screen.blit(self._get_pitch_surface(), (0, 0), area=pygame.Rect(0, 0, WIDTH, HEIGHT))
        self.screen.blit(self._dim_overlay, (0, 0))
        self.draw_text("JOIN FRIEND'S ROOM", self.font_lg, CYAN, WIDTH // 2, 120)
        self.draw_text("Type Room Code or Host IP", self.font_sm, MUTED_TEXT, WIDTH // 2, 168)
        input_box = pygame.Rect(WIDTH // 2 - 240, 225, 480, 68)
        pygame.draw.rect(self.screen, DARK_PANEL, input_box, border_radius=12)
        pygame.draw.rect(self.screen, CYAN, input_box, 2, border_radius=12)
        disp = self.join_input + ("|" if int(time.time() * 2) % 2 == 0 else "")
        self.draw_text(disp if self.join_input else "Enter Room Code or IP...", self.font_lg, WHITE if self.join_input else MUTED_TEXT, WIDTH // 2, 259)
        if self.net.connected:
            self.draw_text("CONNECTED! Waiting for Host...", self.font_md, GREEN, WIDTH // 2, 330)
            if self.net.get_latest_state() is not None:
                self.start_match("client")
                return
        elif self.net.error:
            self.draw_text(self.net.error, self.font_sm, RED, WIDTH // 2, 330)
        self.draw_button("do_join", pygame.Rect(WIDTH // 2 - 160, 385, 320, 62), "CONNECT TO ROOM", CYAN)
        self.draw_button("cancel_room", pygame.Rect(WIDTH // 2 - 120, 470, 240, 50), "BACK", WHITE)

    def render_playing(self):
        self.buttons.clear()
        if self.in_replay and self.replay_frames:
            frame = self.replay_frames[min(len(self.replay_frames) - 1, int(self.replay_idx))]
            bx, by, bz = frame["b"]
            ox = int(max(0, min(WORLD_W - WIDTH, bx - WIDTH // 2)))
            oy = int(max(0, min(WORLD_H - (HEIGHT - TOP_HUD), by - (HEIGHT - TOP_HUD) // 2)))
            self.screen.blit(self._get_pitch_surface(), (0, TOP_HUD), area=pygame.Rect(ox, oy, WIDTH, HEIGHT - TOP_HUD))
            self.draw_goal_nets_2d(ox, oy)
            for p, (px, py) in zip(self.team1, frame["t1"]):
                sx, sy = int(px - ox), int(py - oy + TOP_HUD)
                pygame.draw.circle(self.screen, WHITE, (sx, sy), PLAYER_RADIUS + 1)
                pygame.draw.circle(self.screen, p.color, (sx, sy), PLAYER_RADIUS - 2)
            for p, (px, py) in zip(self.team2, frame["t2"]):
                sx, sy = int(px - ox), int(py - oy + TOP_HUD)
                pygame.draw.circle(self.screen, WHITE, (sx, sy), PLAYER_RADIUS + 1)
                pygame.draw.circle(self.screen, p.color, (sx, sy), PLAYER_RADIUS - 2)
            pygame.draw.circle(self.screen, WHITE, (int(bx - ox), int(by - bz - oy + TOP_HUD)), BALL_RADIUS)
            self.draw_hud()
            self.draw_text("INSTANT REPLAY (SLOW-MO)", self.font_md, GOLD, WIDTH // 2, TOP_HUD + 26)
            self.draw_button("skip_replay", pygame.Rect(WIDTH - 210, HEIGHT - 82, 180, 52), "SKIP REPLAY >>", CYAN)
            return

        if self.camera_mode == "fp":
            self.render_first_person_3d()
        else:
            ox, oy = int(self.cam_x), int(self.cam_y)
            self.screen.blit(self._get_pitch_surface(), (0, TOP_HUD), area=pygame.Rect(ox, oy, WIDTH, HEIGHT - TOP_HUD))

            t_wave = time.time() * (11.0 if self.celebration_timer > 0 else 3.2)
            for idx_w, wx in enumerate(range(PITCH_X, PITCH_X + PITCH_W, 48)):
                sx = wx - ox
                if 0 <= sx <= WIDTH:
                    bounce = int(abs(math.sin(t_wave + idx_w * 0.7)) * (6 if self.celebration_timer > 0 else 2))
                    for wy in (PITCH_Y - 34, PITCH_Y + PITCH_H + 34):
                        sy = wy - oy + TOP_HUD
                        if TOP_HUD <= sy <= HEIGHT:
                            pygame.draw.circle(self.screen, self.stadium["accent"] if idx_w % 2 == 0 else GOLD, (sx, sy - bounce), 4)

            self.draw_goal_nets_2d(ox, oy)
            self.draw_ball_2d(ox, oy)
            for idx, p in enumerate(self.team1):
                self.draw_player_2d(p, idx == self.active1_idx, ox, oy, celebrating=(self.celebration_timer > 0 and p is self.last_scorer_player))
            for p in self.team2:
                self.draw_player_2d(p, False, ox, oy, celebrating=(self.celebration_timer > 0 and p is self.last_scorer_player))

        ox, oy = int(self.cam_x), int(self.cam_y)
        for rg in self.impact_rings:
            prog = 1.0 - (rg.life / rg.max_life)
            rad = max(4, int(rg.max_r * prog))
            pygame.draw.circle(self.screen, rg.color, (int(rg.x - ox), int(rg.y - oy + TOP_HUD)), rad, 2)
        for pt in self.particles:
            pygame.draw.circle(self.screen, pt.color, (int(pt.x - ox), int(pt.y - oy + TOP_HUD)), pt.size)

        self.draw_hud()
        self.touch.draw(self.screen)

        if self.celebration_timer > 0:
            self.screen.blit(self._goal_banner, (0, PITCH_CY - 65))
            col = BLUE if self.last_scorer_team == 1 else RED
            self.draw_text("GOAL!! CELEBRATION!", self.font_xl, GOLD, WIDTH // 2, HEIGHT // 2 - 15)
            self.draw_text(f"Scored by {self.last_scorer_name}", self.font_md, col, WIDTH // 2, HEIGHT // 2 + 30)

    def render_paused(self):
        self.buttons.clear()
        self.render_playing()
        self.screen.blit(self._dim_overlay, (0, 0))
        self.draw_text("MATCH PAUSED", self.font_xl, WHITE, WIDTH // 2, 100)
        bw, cx = 360, WIDTH // 2 - 180
        self.draw_button("resume", pygame.Rect(cx, 155, bw, 54), "RESUME MATCH", GREEN)
        self.draw_button("open_subs", pygame.Rect(cx, 223, bw, 54), f"SUBSTITUTIONS ({self.subs_used}/{self.max_subs})", GOLD)
        self.draw_button("toggle_sa", pygame.Rect(cx, 291, bw, 54), "SMART ASSIST: " + ("ON" if self.career.smart_assist else "OFF"), CYAN)
        self.draw_button("cam_toggle", pygame.Rect(cx, 359, bw, 54), "CAMERA: " + ("1ST PERSON 3D" if self.camera_mode == "fp" else "CLASSIC 2D"), PURPLE)
        self.draw_button("cycle_stadium", pygame.Rect(cx, 427, bw, 54), f"STADIUM: {self.stadium['name']}", self.stadium["accent"])
        self.draw_button("restart", pygame.Rect(cx, 495, bw, 54), "RESTART MATCH", ORANGE)
        self.draw_button("quit_menu", pygame.Rect(cx, 563, bw, 54), "MAIN MENU", RED)

    def render_subs(self):
        self.buttons.clear()
        self.screen.fill(DARK_PANEL)
        self.draw_text(f"IN-MATCH SUBSTITUTIONS ({self.subs_used}/{self.max_subs} USED)", self.font_lg, GOLD, WIDTH // 2, 54)
        self.draw_text("1) Tap Pitch Player to Take Off   2) Tap Bench Player to Bring On", self.font_sm, MUTED_TEXT, WIDTH // 2, 94)
        self.draw_text("ON PITCH (5 OUTFIELD)", self.font_md, CYAN, 300, 140)
        for i in range(5):
            self._draw_mini_card(f"sub_out_{i}", pygame.Rect(160, 170 + i * 92, 280, 76), self.team1[i].card_id, self.sub_selected_pitch == i)
        self.draw_text("BENCH (4 SUBS)", self.font_md, GOLD, 860, 140)
        for i, pid in enumerate(self.career.bench):
            self._draw_mini_card(f"sub_in_{i}", pygame.Rect(720, 170 + i * 92, 280, 76), pid, False)
        self.draw_button("back_pause", pygame.Rect(WIDTH // 2 - 120, 640, 240, 52), "BACK TO PAUSE", WHITE)

    def render_penalties(self):
        self.buttons.clear()
        self.screen.fill((16, 40, 28))
        self.draw_text("PENALTY SHOOTOUT!", self.font_xl, GOLD, WIDTH // 2, 70)
        self.draw_text(f"ROUND {self.pen_round}   |   YOU {self.pen_score1}  -  {self.pen_score2} CPU", self.font_lg, WHITE, WIDTH // 2, 130)
        self.draw_text(self.pen_msg, self.font_md, CYAN, WIDTH // 2, 190)
        gr = pygame.Rect(WIDTH // 2 - 260, 240, 520, 240)
        pygame.draw.rect(self.screen, (22, 30, 42), gr)
        pygame.draw.rect(self.screen, WHITE, gr, 6)
        action_lbl = "SHOOT" if self.pen_turn == 1 else "DIVE GK"
        self.draw_button("pen_0", pygame.Rect(gr.left + 25, 290, 140, 140), f"{action_lbl} LEFT", CYAN)
        self.draw_button("pen_1", pygame.Rect(gr.centerx - 70, 290, 140, 140), f"{action_lbl} MID", GOLD)
        self.draw_button("pen_2", pygame.Rect(gr.right - 165, 290, 140, 140), f"{action_lbl} RIGHT", GREEN)

    def render_fulltime(self):
        self.buttons.clear()
        self.screen.blit(self._get_pitch_surface(), (0, 0), area=pygame.Rect(0, 0, WIDTH, HEIGHT))
        self.screen.blit(self._dim_overlay, (0, 0))
        winner = "YOU WIN!" if self.score1 > self.score2 else ("OPPONENT WINS!" if self.score2 > self.score1 else "DRAW!")
        self.draw_text("FULL TIME", self.font_lg, GOLD, WIDTH // 2, 88)
        self.draw_text(winner, self.font_xl, WHITE, WIDTH // 2, 144)
        self.draw_text(f"{self.score1}  -  {self.score2}", self.font_xl, CYAN, WIDTH // 2, 212)
        card = pygame.Rect(WIDTH // 2 - 230, 265, 460, 155)
        pygame.draw.rect(self.screen, CARD_BG, card, border_radius=14)
        self.draw_text(f"Shots: {self.stats['shots1']} vs {self.stats['shots2']}  |  Passes: {self.stats['passes1']} vs {self.stats['passes2']}", self.font_sm, WHITE, WIDTH // 2, 310)
        self.draw_text(f"Match Reward: +{self.match_reward} Coins", self.font_md, GOLD, WIDTH // 2, 355)
        if self.champ_bonus > 0:
            self.draw_text(f"CHAMPION BONUS! +{self.champ_bonus} COINS!", self.font_md, GREEN, WIDTH // 2, 392)
        if self.mode not in ("client", "ucl"):
            self.draw_button("rematch", pygame.Rect(WIDTH // 2 - 160, 460, 320, 58), "REMATCH", GREEN)
        self.draw_button("quit_menu", pygame.Rect(WIDTH // 2 - 160, 535, 320, 54), "MAIN MENU", WHITE)

    # -----------------------------------------------------------------------
    # EVENT HANDLING & MAIN LOOP
    # -----------------------------------------------------------------------
    def handle_click(self, pos, button):
        for key, rect in list(self.buttons.items()):
            if not rect.collidepoint(pos):
                continue
            self.sound.play("click")
            if key == "play_ai":
                if button == 3:
                    self.ai_difficulty = (self.ai_difficulty + 1) % 3
                else:
                    self.start_match("ai")
            elif key == "league":
                self.state = "LEAGUE"
            elif key == "play_league":
                self.start_match("league")
            elif key == "ucl":
                self.ucl_msg = ""
                self.state = "UCL"
            elif key == "start_ucl":
                ok, self.ucl_msg = self.career.start_ucl_from_top6()
            elif key == "play_ucl":
                self.start_match("ucl")
            elif key == "sim_ucl_round":
                self.career.advance_ucl_round()
                self.ucl_msg = f"Advanced to {self.career.ucl_round_name}!"
            elif key == "ballondor":
                self.state = "BALLON_DOR"
            elif key == "trophies":
                self.state = "TROPHIES"
            elif key == "game_plan":
                self.selected_slot = None
                self.pending_reserve_pid = None
                self.move_pos_mode = False
                self.reserves_open = False
                self.gp_msg = ""
                self.state = "GAME_PLAN"
            elif key == "gp_mgr":
                self.career.manager_idx = (self.career.manager_idx + 1) % len(MANAGERS)
                self.career.save()
            elif key == "gp_form":
                self.career.formation_idx = (self.career.formation_idx + 1) % len(FORMATIONS)
                self.career.custom_offsets.clear()
                self.career.save()
            elif key == "gp_move":
                self.move_pos_mode = not self.move_pos_mode
                self.gp_msg = "MOVE POS ON: Tap Pitch Player, then tap anywhere on Pitch!" if self.move_pos_mode else ""
            elif key == "gp_reset_pos":
                self.career.custom_offsets.clear()
                self.career.save()
                self.gp_msg = "Positions reset to Formation!"
            elif key == "gp_reserves":
                self.reserves_open = True
                self.reserves_page = 0
            elif key == "res_prev":
                self.reserves_page = max(0, self.reserves_page - 1)
            elif key == "res_next":
                if (self.reserves_page + 1) * 12 < len(self.career.get_reserves()):
                    self.reserves_page += 1
            elif key == "close_reserves":
                self.reserves_open = False
            elif key.startswith("pick_res_"):
                self.pending_reserve_pid = key[9:]
                self.selected_slot = ("res", self.pending_reserve_pid)
                self.reserves_open = False
                self.gp_msg = f"Selected {CATALOG_BY_ID[self.pending_reserve_pid]['short']}! Now tap a Pitch or Bench slot!"
            elif key == "gp_pitch_area":
                if self.move_pos_mode and self.selected_slot and self.selected_slot[0] == "pitch":
                    idx = self.selected_slot[1]
                    pr = rect
                    new_oy = int((pos[0] - pr.centerx) / 240.0 * 420.0)
                    new_ox = int(-((pos[1] - (pr.top + 60)) / 420.0 * 620.0 + 120.0))
                    new_ox = max(-740, min(-120, new_ox))
                    new_oy = max(-360, min(360, new_oy))
                    self.career.custom_offsets[str(idx)] = [new_ox, new_oy]
                    self.career.save()
                    self.selected_slot = None
                    self.gp_msg = "Player moved!"
            elif key.startswith("slot_"):
                parts = key.split("_", 2)
                kind = parts[1]
                val = int(parts[2])
                slot = (kind, val)
                if self.selected_slot is None:
                    self.selected_slot = slot
                    self.gp_msg = "Tap another slot to SWAP (or tap pitch if Move Pos is ON)"
                else:
                    self.career.swap_squad_slots(self.selected_slot, slot)
                    self.selected_slot = None
                    self.pending_reserve_pid = None
                    self.gp_msg = "Swapped!"
            elif key == "open_subs":
                self.sub_selected_pitch = None
                self.state = "SUBS"
            elif key.startswith("sub_out_"):
                self.sub_selected_pitch = int(key.split("_")[2])
            elif key.startswith("sub_in_"):
                if self.sub_selected_pitch is not None and self.subs_used < self.max_subs:
                    b_idx = int(key.split("_")[2])
                    new_pid = self.career.bench[b_idx]
                    old_p = self.team1[self.sub_selected_pitch]
                    self.career.bench[b_idx] = old_p.card_id
                    self.career.lineup[self.sub_selected_pitch] = new_pid
                    self.team1[self.sub_selected_pitch] = Player(old_p.x, old_p.y, old_p.home_x, old_p.home_y, BLUE, 1, new_pid, self.career.get_card_stats(new_pid))
                    self.subs_used += 1
                    self.sub_selected_pitch = None
                    self.state = "PAUSED"
            elif key == "back_pause":
                self.state = "PAUSED"
            elif key.startswith("pen_"):
                self._take_penalty_choice(int(key.split("_")[1]))
            elif key == "settings":
                self.state = "SETTINGS"
            elif key == "toggle_sa":
                self.career.smart_assist = not self.career.smart_assist
                self.career.save()
            elif key == "toggle_sfx":
                self.sound.enabled = not self.sound.enabled
                if not self.sound.enabled:
                    self.sound.stop_bg()
                    self.sound.stop_menu_bgm()
                elif self.state != "PLAYING":
                    self.sound.start_menu_bgm()
            elif key == "toggle_menu_bgm":
                self.sound.menu_bgm_enabled = not self.sound.menu_bgm_enabled
                if not self.sound.menu_bgm_enabled:
                    self.sound.stop_menu_bgm()
                elif self.state != "PLAYING":
                    self.sound.start_menu_bgm()
            elif key == "toggle_bg":
                self.sound.bg_enabled = not self.sound.bg_enabled
                if not self.sound.bg_enabled:
                    self.sound.stop_bg()
            elif key == "market":
                self.market_msg = ""
                self.state = "MARKET"
            elif key.startswith("gear_"):
                self.edit_pid = key[5:]
                self.state = "STAT_EDITOR"
            elif key.startswith("stat_add_"):
                self.career.adjust_custom_stat(self.edit_pid, key[9:], 1)
            elif key.startswith("stat_sub_"):
                self.career.adjust_custom_stat(self.edit_pid, key[9:], -1)
            elif key == "back_market":
                self.state = "MARKET"
            elif key == "packs":
                self.pack_result, self.pack_msg = None, ""
                self.state = "PACKS"
            elif key == "open_free_pack":
                self.pack_result, self.pack_msg = self.career.open_10_pack(use_coins=False)
            elif key == "open_coin_pack":
                self.pack_result, self.pack_msg = self.career.open_10_pack(use_coins=True)
            elif key == "downloads":
                self.dl_msg = ""
                self.state = "DOWNLOADS"
            elif key == "dl_bg":
                self.dl_msg = self.career.download_pack("bg_crowd", self.sound)
            elif key == "dl_menu_bgm":
                self.dl_msg = self.career.download_pack("menu_bgm", self.sound)
            elif key == "url_hafid":
                try:
                    webbrowser.open(HAFID_DANGER_URL)
                    self.dl_msg = f"Opened Chrome/Browser: {HAFID_DANGER_URL}"
                except Exception:
                    self.dl_msg = f"URL: {HAFID_DANGER_URL}"
            elif key == "url_bgm":
                try:
                    webbrowser.open(MENU_BGM_URL)
                    self.dl_msg = f"Opened Chrome/Browser: {MENU_BGM_URL}"
                except Exception:
                    self.dl_msg = f"URL: {MENU_BGM_URL}"
            elif key == "url_photos":
                try:
                    webbrowser.open(PLAYER_PHOTOS_URL)
                    self.dl_msg = f"Opened Chrome/Browser: {PLAYER_PHOTOS_URL}"
                except Exception:
                    self.dl_msg = f"URL: {PLAYER_PHOTOS_URL}"
            elif key == "dl_stadium":
                self.dl_msg = self.career.download_pack("stadium_hd", self.sound)
            elif key == "dl_photos":
                self._portrait_cache.clear()
                self.dl_msg = self.career.download_pack("player_photos", self.sound)
            elif key == "voice_hafid":
                self.sound.commentary_lang = "hafid"
                self.dl_msg = self.career.download_pack("commentary_hafid", self.sound)
                self.sound.play_commentary_danger()
            elif key == "voice_spanish":
                self.sound.commentary_lang = "spanish"
                self.dl_msg = self.career.download_pack("commentary_spanish", self.sound)
                self.sound.play_commentary_goal()
            elif key == "test_sound":
                self.sound.play_commentary_danger()
                self.dl_msg = f"Played Hafid Khatira! ({self.sound.backend})"
            elif key == "mkt_prev":
                tp = (len(PLAYER_CATALOG) + 4) // 5
                self.market_page = (self.market_page - 1) % tp
            elif key == "mkt_next":
                tp = (len(PLAYER_CATALOG) + 4) // 5
                self.market_page = (self.market_page + 1) % tp
            elif key.startswith("buy_"):
                _, self.market_msg = self.career.buy_player(key[4:])
            elif key.startswith("sell_"):
                _, self.market_msg = self.career.sell_player(key[5:])
            elif key == "create_room":
                self.net.start_host(DEFAULT_PORT)
                self.state = "ROOM_HOST"
            elif key == "join_room":
                self.net.close()
                self.state = "ROOM_JOIN"
            elif key == "stadiums":
                self._prev_state = self.state
                self.state = "STADIUM_SELECT"
            elif key in ("cam_toggle", "cam_btn"):
                self.camera_mode = "fp" if self.camera_mode == "classic" else "classic"
            elif key == "auto_ai_btn":
                self.auto_ai = not self.auto_ai
            elif key == "skip_replay":
                self._skip_replay()
            elif key == "duration":
                options = [60, 90, 120, 180, 300]
                idx = (options.index(self.match_duration) + 1) % len(options) if self.match_duration in options else 0
                self.match_duration = options[idx]
            elif key.startswith("st_"):
                self.stadium_idx = int(key.split("_")[1])
            elif key == "back_menu":
                self.state = getattr(self, "_prev_state", "MENU")
                if self.state not in ("MENU", "ROOM_HOST"):
                    self.state = "MENU"
            elif key == "host_start" and self.net.connected:
                self.start_match("host")
            elif key == "do_join":
                self.net.join_room(self.join_input)
            elif key == "cancel_room":
                self.net.close()
                self.state = "MENU"
            elif key == "pause_btn":
                self.state = "PAUSED"
            elif key == "resume":
                self.state = "PLAYING"
            elif key == "cycle_stadium":
                self.stadium_idx = (self.stadium_idx + 1) % len(STADIUMS)
            elif key == "restart":
                self.start_match(self.mode)
            elif key == "rematch":
                self.start_match(self.mode)
            elif key == "quit_menu":
                self.net.close()
                self.sound.stop_bg()
                self.sound.start_menu_bgm()
                self.state = "MENU"
            break

    def run(self):
        running = True
        while running:
            dt = min(0.05, self.clock.tick(FPS) / 1000.0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif self.state == "PLAYING" and event.type in (
                    pygame.FINGERDOWN, pygame.FINGERMOTION, pygame.FINGERUP,
                    pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP,
                ):
                    self.touch.handle_event(event)
                    if event.type == pygame.FINGERDOWN:
                        self.handle_click((int(event.x * WIDTH), int(event.y * HEIGHT)), 1)
                    elif event.type == pygame.MOUSEBUTTONDOWN and not self.touch.using_touch:
                        self.handle_click(event.pos, event.button)
                elif event.type == pygame.FINGERDOWN:
                    self.touch.using_touch = True
                    self.handle_click((int(event.x * WIDTH), int(event.y * HEIGHT)), 1)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos, event.button)
                elif event.type == pygame.KEYDOWN:
                    if self.in_replay and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self._skip_replay()
                    elif event.key == pygame.K_v and self.state in ("PLAYING", "PAUSED", "MENU"):
                        self.camera_mode = "fp" if self.camera_mode == "classic" else "classic"
                    elif event.key == pygame.K_ESCAPE:
                        if self.state == "PLAYING":
                            self.state = "PAUSED"
                        elif self.state == "PAUSED":
                            self.state = "PLAYING"
                        elif self.state == "SUBS":
                            self.state = "PAUSED"
                        elif self.state == "STAT_EDITOR":
                            self.state = "MARKET"
                        elif self.state in ("STADIUM_SELECT", "ROOM_HOST", "ROOM_JOIN", "MARKET", "LEAGUE", "UCL", "BALLON_DOR", "TROPHIES", "PACKS", "DOWNLOADS", "GAME_PLAN", "SETTINGS"):
                            if self.state in ("ROOM_HOST", "ROOM_JOIN"):
                                self.net.close()
                            self.state = "MENU"
                    elif self.state == "ROOM_JOIN":
                        if event.key == pygame.K_BACKSPACE:
                            self.join_input = self.join_input[:-1]
                        elif event.key == pygame.K_RETURN:
                            self.net.join_room(self.join_input)
                        elif event.unicode and (event.unicode.isalnum() or event.unicode in ".:-"):
                            if len(self.join_input) < 28:
                                self.join_input += event.unicode.upper()

            if self.state == "MENU":
                self.render_menu()
            elif self.state == "GAME_PLAN":
                self.render_game_plan()
            elif self.state == "SETTINGS":
                self.render_settings()
            elif self.state == "MARKET":
                self.render_market()
            elif self.state == "STAT_EDITOR":
                self.render_stat_editor()
            elif self.state == "PACKS":
                self.render_packs()
            elif self.state == "DOWNLOADS":
                self.render_downloads()
            elif self.state == "LEAGUE":
                self.render_league()
            elif self.state == "UCL":
                self.render_ucl()
            elif self.state == "BALLON_DOR":
                self.render_ballon_dor()
            elif self.state == "TROPHIES":
                self.render_trophies()
            elif self.state == "TROPHY_CEREMONY":
                self.render_trophy_ceremony()
            elif self.state == "STADIUM_SELECT":
                self.render_stadium_select()
            elif self.state == "ROOM_HOST":
                self.render_room_host()
            elif self.state == "ROOM_JOIN":
                self.render_room_join()
            elif self.state == "PLAYING":
                self.update_playing(dt)
                self.render_playing()
            elif self.state == "PAUSED":
                self.render_paused()
            elif self.state == "SUBS":
                self.render_subs()
            elif self.state == "PENALTIES":
                self.render_penalties()
            elif self.state == "FULLTIME":
                self.render_fulltime()

            pygame.display.flip()

        self.net.close()
        self.sound.stop_bg()
        self.sound.stop_menu_bgm()
        pygame.quit()


if __name__ == "__main__":
    try:
        FootballGame().run()
    except Exception as exc:
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")