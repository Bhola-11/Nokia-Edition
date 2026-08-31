# 🐍 Snake Classic — Nokia Edition

> An authentic **Nokia 3310** retro gaming platform powered by **Django MVT** backend and an **HTML5 Canvas + Web Audio API** 8-bit game engine on the frontend.

![Nokia 3310 Snake Platform](https://img.shields.io/badge/Architecture-Django%20MVT-green.svg)
![Game Engine](https://img.shields.io/badge/Engine-HTML5%20Canvas%20%2B%20WebAudio-orange.svg)
![Anti-Cheat](https://img.shields.io/badge/Anti--Cheat-Deterministic%20LCG%20Replay-blue.svg)

---

## 🎮 Key Features

### 1. Authentic Nokia 3310 Visuals & Web Audio Synthesizer
* **Nokia 3310 Phone Chassis**: Bezel frame, speaker grill, battery meter, signal bars, LCD clock, and physical tactile keypad (2, 4, 6, 8, Soft keys, C button, Menu).
* **Dot-Matrix LCD Display**: Authentic monochrome 28x16 grid with CRT scanlines and 5 swappable color themes:
  * *Classic Green LCD* (`#9bbc0f`)
  * *Vintage Amber* (`#f39c12`)
  * *Cyber Cyan Matrix* (`#00f2fe`)
  * *Retro GameBoy Olive* (`#8bac0f`)
  * *Monochrome Dark OLED* (`#121212`)
* **Pure Web Audio API Synthesizer**: Zero external audio assets! Built-in square-wave oscillators for apple eating chirps, bonus bug chords, fatal crash crunch, menu clicks, and the iconic full **Nokia Ringtone Tune** (*Gran Vals*).

### 2. Gameplay Modes & Difficulties
* **Classic 3310**: Original boundary walls and accelerating speed.
* **Time Attack**: 60-second high-intensity countdown rush.
* **Endless**: Screen wrap-around endurance survival.
* **Labyrinth Challenge**: Multi-chamber mazes, static obstacles, and Quantum Warp Teleport Portals.
* **4 Speeds**: Slug (140ms), Normal (100ms), Python (70ms), Cobra (45ms).

### 3. Controls & Mobile Responsiveness
* **Desktop**: Arrow keys, `WASD`, Numpad `2, 4, 6, 8`, Space to Pause.
* **Mobile / Touch**: Direct screen swipe gestures + on-screen Nokia tactile buttons.

### 4. Anti-Cheat Score Verification & Deterministic Replay Engine
* Deterministic Linear Congruential PRNG seed generation per session.
* Telemetry move recording with millisecond precision and tick indexes.
* Backend physics simulation recreating full trajectories, food pickups, and collision checks.
* Interactive canvas **Match Replay Viewer** with play/pause, scrub bar, and 1x/2x/4x playback speed.

### 5. Tournaments, Achievements & Player Profiles
* **Tournaments**: Time-limited competitive events with dedicated standings and XP prizes.
* **14+ Achievements**: *First Bite*, *Centurion*, *Speed Demon*, *Anaconda*, *Survivor*, *Ouroboros God*, and more.
* **Progression System**: Earn XP, rank up from *Worm Cadet* to *Nokia Ouroboros Legend*.
* **Leaderboards**: Filterable by Mode, Difficulty, and Timeframe (Today, Weekly, All-Time).
* **Analytics Dashboard**: Global telemetry, fatal cause distributions, and anti-cheat audit logs.

---

## 🏗️ Architecture (Django MVT)

```
Nokia_Edition/
├── manage.py
├── requirements.txt
├── nokia_snake/             # Settings, ASGI, WSGI, Root URLs
├── apps/
│   ├── accounts/           # User authentication, PlayerProfile, custom skins
│   ├── game/               # Core game backend, GameSession, Score, GameMap
│   ├── leaderboard/        # Global rankings, Seasons
│   ├── achievements/       # Badges, XP rewards, evaluator
│   ├── tournaments/        # Competitive events, participant brackets
│   ├── anticheat/          # Deterministic LCG replay validation engine
│   └── analytics/          # Server telemetry & audit dashboard
├── templates/              # Django HTML templates
└── static/                 # Canvas engine, WebAudio synth, CSS themes
```

---

## 🚀 Quick Start Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Seed Initial Maps, Tournaments, Achievements & Sample High Scores
```bash
python manage.py seed_data
```

### 4. Run the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to: **`http://127.0.0.1:8000/`**

---

## 🧪 Running Automated Tests
```bash
python manage.py test
```
