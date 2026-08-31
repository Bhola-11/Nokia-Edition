/**
 * Snake Classic — Nokia Edition (HTML5 Canvas Engine)
 */

class SnakeGame {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        
        // Grid setup: 28 columns x 16 rows (Nokia 3310 aspect ratio 84x48 scaled)
        this.gridW = 28;
        this.gridH = 16;
        this.tileSize = 10;
        
        this.canvas.width = this.gridW * this.tileSize;
        this.canvas.height = this.gridH * this.tileSize;

        // State & Config
        this.state = 'MENU'; // MENU, PLAYING, PAUSED, GAMEOVER, SUBMITTING
        this.mode = 'classic';
        this.difficulty = 'normal';
        this.mapName = 'standard_box';
        
        // Difficulty intervals in ms
        this.speedIntervals = {
            'slug': 140,
            'normal': 100,
            'python': 70,
            'cobra': 45
        };

        // Multipliers
        this.scoreValues = {
            'slug': 10,
            'normal': 15,
            'python': 25,
            'cobra': 40
        };

        // Telemetry & Gameplay variables
        this.snake = [];
        this.direction = 'R';
        this.nextDirection = 'R';
        this.inputQueue = [];
        this.food = null;
        this.bonusFood = null;
        this.bonusTimer = 0;
        this.score = 0;
        this.applesEaten = 0;
        this.maxLength = 3;
        this.tick = 0;
        this.gameTimer = 60.0; // For time attack
        this.walls = [];
        this.portals = [];
        
        // Session & Anti-Cheat
        this.sessionId = null;
        this.seed = 12345678;
        this.rng = null;
        this.recorder = null;

        // Loop handles
        this.lastFrameTime = 0;
        this.tickAccumulator = 0;
        this.animationId = null;

        // Init Input Controller
        this.input = new InputController(this);

        this.initUIBindings();
        this.renderMenuScreen();
    }

    initUIBindings() {
        // Mode & Difficulty Selectors
        const modeSelect = document.getElementById('gameModeSelect');
        const diffSelect = document.getElementById('gameDifficultySelect');
        const mapSelect = document.getElementById('gameMapSelect');
        const startBtn = document.getElementById('btnStartGame');

        if (modeSelect) modeSelect.addEventListener('change', (e) => {
            this.mode = e.target.value;
            const mapGroup = document.getElementById('mapSelectGroup');
            if (mapGroup) {
                mapGroup.style.display = (this.mode === 'challenge') ? 'block' : 'none';
            }
        });

        if (diffSelect) diffSelect.addEventListener('change', (e) => {
            this.difficulty = e.target.value;
        });

        if (mapSelect) mapSelect.addEventListener('change', (e) => {
            this.mapName = e.target.value;
        });

        if (startBtn) startBtn.addEventListener('click', () => {
            this.startNewGame();
        });
    }

    async startNewGame() {
        // Request server session and deterministic seed
        try {
            const resp = await fetch('/api/session/start/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({
                    mode: this.mode,
                    difficulty: this.difficulty,
                    map_name: this.mapName
                })
            });

            const data = await resp.json();
            if (data.status === 'success') {
                this.sessionId = data.session_id;
                this.seed = data.seed;
                this.walls = data.walls || [];
                this.portals = data.portals || [];
            }
        } catch (e) {
            console.warn("Offline or fallback mode", e);
            this.sessionId = 'local-' + Date.now();
            this.seed = Math.floor(Math.random() * 89999999) + 10000000;
        }

        // Initialize components
        this.rng = new DeterministicRNG(this.seed);
        this.recorder = new MoveRecorder(this.sessionId, this.seed);
        
        this.snake = [[14, 8], [13, 8], [12, 8]];
        this.direction = 'R';
        this.nextDirection = 'R';
        this.inputQueue = [];
        this.score = 0;
        this.applesEaten = 0;
        this.maxLength = 3;
        this.tick = 0;
        this.gameTimer = 60.0;
        this.bonusFood = null;
        this.bonusTimer = 0;
        
        this.spawnFood();

        this.state = 'PLAYING';
        this.hideOverlays();
        this.updateHUD();

        if (window.soundEngine) {
            window.soundEngine.init();
        }

        this.lastFrameTime = performance.now();
        this.tickAccumulator = 0;
        
        if (this.animationId) cancelAnimationFrame(this.animationId);
        this.gameLoop(performance.now());
    }

    queueDirection(dir) {
        const opposites = { 'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L' };
        const lastQueued = this.inputQueue.length > 0 ? this.inputQueue[this.inputQueue.length - 1] : this.direction;

        if (dir !== lastQueued && dir !== opposites[lastQueued]) {
            if (this.inputQueue.length < 3) {
                this.inputQueue.push(dir);
            }
        }
    }

    handleActionBtn() {
        if (this.state === 'MENU' || this.state === 'GAMEOVER') {
            this.startNewGame();
        } else if (this.state === 'PLAYING') {
            this.state = 'PAUSED';
            this.showOverlay("PAUSED", "Press Center Key or Space to resume");
        } else if (this.state === 'PAUSED') {
            this.state = 'PLAYING';
            this.hideOverlays();
        }
    }

    handleBackBtn() {
        if (this.state === 'PLAYING' || this.state === 'PAUSED') {
            this.gameOver('quit');
        } else if (this.state === 'GAMEOVER') {
            this.state = 'MENU';
            this.renderMenuScreen();
        }
    }

    gameLoop(now) {
        if (this.state !== 'PLAYING') {
            this.render();
            return;
        }

        const delta = now - this.lastFrameTime;
        this.lastFrameTime = now;
        this.tickAccumulator += delta;

        // Dynamic speed calculation: faster as score increases
        let baseSpeed = this.speedIntervals[this.difficulty] || 100;
        let speed = Math.max(35, baseSpeed - Math.floor(this.applesEaten / 4) * 3);

        while (this.tickAccumulator >= speed) {
            this.updateTick();
            this.tickAccumulator -= speed;
        }

        // Time Attack countdown
        if (this.mode === 'time_attack') {
            this.gameTimer -= delta / 1000;
            if (this.gameTimer <= 0) {
                this.gameTimer = 0;
                this.gameOver('timeout');
                return;
            }
            this.updateHUD();
        }

        this.render();
        this.animationId = requestAnimationFrame((t) => this.gameLoop(t));
    }

    updateTick() {
        this.tick++;

        // Process next queued turn
        if (this.inputQueue.length > 0) {
            this.direction = this.inputQueue.shift();
            this.recorder.recordMove(this.tick, this.direction);
        }

        const dirOffsets = { 'U': [0, -1], 'D': [0, 1], 'L': [-1, 0], 'R': [1, 0] };
        const offset = dirOffsets[this.direction];
        const head = this.snake[0];
        let nx = head[0] + offset[0];
        let ny = head[1] + offset[1];

        // Wall collisions
        if (this.mode === 'endless') {
            nx = (nx + this.gridW) % this.gridW;
            ny = (ny + this.gridH) % this.gridH;
        } else {
            if (nx < 0 || nx >= this.gridW || ny < 0 || ny >= this.gridH) {
                this.gameOver('wall');
                return;
            }
        }

        // Check Obstacle Wall collisions
        for (let w of this.walls) {
            if (nx === w[0] && ny === w[1]) {
                this.gameOver('obstacle');
                return;
            }
        }

        // Check Quantum Portals
        for (let p of this.portals) {
            if (nx === p.entry[0] && ny === p.entry[1]) {
                nx = p.exit[0];
                ny = p.exit[1];
                if (window.soundEngine) window.soundEngine.playBonus();
                break;
            }
        }

        // Self collision check
        for (let i = 0; i < this.snake.length - 1; i++) {
            if (nx === this.snake[i][0] && ny === this.snake[i][1]) {
                this.gameOver('self');
                return;
            }
        }

        // Move Snake
        const newHead = [nx, ny];
        this.snake.unshift(newHead);

        // Food Eating
        if (this.food && nx === this.food[0] && ny === this.food[1]) {
            this.applesEaten++;
            const pts = this.scoreValues[this.difficulty] || 15;
            this.score += pts;
            
            if (this.snake.length > this.maxLength) {
                this.maxLength = this.snake.length;
            }

            if (window.soundEngine) window.soundEngine.playEat();
            this.updateHUD();
            this.spawnFood();
        } else {
            this.snake.pop();
        }
    }

    spawnFood() {
        const wallSet = new Set(this.walls.map(w => `${w[0]},${w[1]}`));
        const snakeSet = new Set(this.snake.map(s => `${s[0]},${s[1]}`));

        for (let attempt = 0; attempt < 500; attempt++) {
            const fx = this.rng.nextInt(0, this.gridW - 1);
            const fy = this.rng.nextInt(0, this.gridH - 1);
            const key = `${fx},${fy}`;

            if (!wallSet.has(key) && !snakeSet.has(key)) {
                this.food = [fx, fy];
                return;
            }
        }

        // Screen is full! Victory!
        this.gameOver('victory');
    }

    async gameOver(reason) {
        this.state = 'GAMEOVER';
        if (this.animationId) cancelAnimationFrame(this.animationId);

        if (window.soundEngine) {
            if (reason === 'victory') {
                window.soundEngine.playLevelUp();
            } else {
                window.soundEngine.playDie();
            }
        }

        this.showOverlay("GAME OVER", `Score: ${this.score} pts<br>Submitting score...`);

        // Submit Score and Telemetry to Server
        const telemetry = this.recorder.getTelemetry();
        try {
            const resp = await fetch('/api/session/submit/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    score: this.score,
                    apples_eaten: this.applesEaten,
                    max_length: this.maxLength,
                    duration_seconds: telemetry.durationSeconds,
                    death_reason: reason,
                    moves_data: telemetry.movesData,
                    checksum: telemetry.checksum
                })
            });

            const data = await resp.json();
            if (data.status === 'verified') {
                let msg = `Final Score: <b>${this.score}</b><br>Apples: ${this.applesEaten}`;
                if (data.new_high_score) {
                    msg += `<br><span style="color:#d35400; font-weight:bold;">🏆 NEW HIGH SCORE!</span>`;
                }
                if (data.earned_xp > 0) {
                    msg += `<br>+${data.earned_xp} XP (Rank: ${data.rank_title})`;
                }
                if (data.unlocked_achievements && data.unlocked_achievements.length > 0) {
                    msg += `<br>🎖️ Unlocked: ${data.unlocked_achievements.map(a => a.icon + ' ' + a.title).join(', ')}`;
                }
                msg += `<br><br><small>Press Menu or Space to play again</small>`;
                this.showOverlay("GAME OVER", msg);
            } else if (data.status === 'flagged') {
                this.showOverlay("SESSION FLAGGED", `Score not verified: ${data.reason}`);
            }
        } catch (e) {
            this.showOverlay("GAME OVER", `Score: ${this.score} pts<br><small>Press Menu to restart</small>`);
        }
    }

    render() {
        const ctx = this.ctx;
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Get LCD colors from CSS variables
        const computedStyle = getComputedStyle(document.body);
        const pixelColor = computedStyle.getPropertyValue('--nokia-lcd-pixel').trim() || '#0f380f';

        // Draw Map Walls
        ctx.fillStyle = pixelColor;
        for (let w of this.walls) {
            ctx.fillRect(w[0] * this.tileSize, w[1] * this.tileSize, this.tileSize, this.tileSize);
            // Inner brick pattern
            ctx.fillStyle = computedStyle.getPropertyValue('--nokia-lcd-bg').trim() || '#9bbc0f';
            ctx.fillRect(w[0] * this.tileSize + 1, w[1] * this.tileSize + 1, this.tileSize - 2, this.tileSize - 2);
            ctx.fillStyle = pixelColor;
            ctx.fillRect(w[0] * this.tileSize + 3, w[1] * this.tileSize + 3, this.tileSize - 6, this.tileSize - 6);
        }

        // Draw Portals
        for (let p of this.portals) {
            ctx.strokeStyle = pixelColor;
            ctx.lineWidth = 1.5;
            ctx.strokeRect(p.entry[0] * this.tileSize + 1, p.entry[1] * this.tileSize + 1, this.tileSize - 2, this.tileSize - 2);
            ctx.strokeRect(p.exit[0] * this.tileSize + 1, p.exit[1] * this.tileSize + 1, this.tileSize - 2, this.tileSize - 2);
        }

        // Draw Food (Apple dot with stem)
        if (this.food) {
            const fx = this.food[0] * this.tileSize;
            const fy = this.food[1] * this.tileSize;
            ctx.fillStyle = pixelColor;
            ctx.fillRect(fx + 2, fy + 2, this.tileSize - 4, this.tileSize - 4);
            ctx.fillRect(fx + 4, fy, 2, 2); // stem
        }

        // Draw Snake
        ctx.fillStyle = pixelColor;
        for (let i = 0; i < this.snake.length; i++) {
            const seg = this.snake[i];
            const sx = seg[0] * this.tileSize;
            const sy = seg[1] * this.tileSize;

            if (i === 0) {
                // Snake Head
                ctx.fillRect(sx + 1, sy + 1, this.tileSize - 2, this.tileSize - 2);
                // Eyes
                ctx.fillStyle = computedStyle.getPropertyValue('--nokia-lcd-bg').trim() || '#9bbc0f';
                if (this.direction === 'R') {
                    ctx.fillRect(sx + 6, sy + 2, 2, 2);
                    ctx.fillRect(sx + 6, sy + 6, 2, 2);
                } else if (this.direction === 'L') {
                    ctx.fillRect(sx + 2, sy + 2, 2, 2);
                    ctx.fillRect(sx + 2, sy + 6, 2, 2);
                } else if (this.direction === 'U') {
                    ctx.fillRect(sx + 2, sy + 2, 2, 2);
                    ctx.fillRect(sx + 6, sy + 2, 2, 2);
                } else if (this.direction === 'D') {
                    ctx.fillRect(sx + 2, sy + 6, 2, 2);
                    ctx.fillRect(sx + 6, sy + 6, 2, 2);
                }
                ctx.fillStyle = pixelColor;
            } else {
                // Snake Body Segments (Bordered dot matrix block)
                ctx.fillRect(sx + 1, sy + 1, this.tileSize - 2, this.tileSize - 2);
            }
        }
    }

    renderMenuScreen() {
        this.render();
        this.showOverlay("NOKIA 3310", "SNAKE CLASSIC<br><br>Press [START] or Space<br>to Begin Game");
    }

    showOverlay(title, html) {
        let overlay = document.getElementById('lcdOverlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'lcdOverlay';
            overlay.className = 'lcd-overlay';
            const screen = document.querySelector('.nokia-screen');
            if (screen) screen.appendChild(overlay);
        }
        overlay.innerHTML = `<h2>${title}</h2><p>${html}</p>`;
        overlay.style.display = 'flex';
    }

    hideOverlays() {
        const overlay = document.getElementById('lcdOverlay');
        if (overlay) overlay.style.display = 'none';
    }

    updateHUD() {
        const scoreEl = document.getElementById('hudScore');
        const timerEl = document.getElementById('hudTimer');
        const applesEl = document.getElementById('hudApples');

        if (scoreEl) scoreEl.innerText = this.score;
        if (applesEl) applesEl.innerText = this.applesEaten;
        if (timerEl) {
            if (this.mode === 'time_attack') {
                timerEl.style.display = 'inline';
                timerEl.innerText = `${Math.ceil(this.gameTimer)}s`;
            } else {
                timerEl.style.display = 'none';
            }
        }
    }

    getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }
}
