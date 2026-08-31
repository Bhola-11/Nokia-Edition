/**
 * Deterministic Canvas Replay Player for Nokia Snake
 */

class ReplayViewer {
    constructor(canvasId, sessionData) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.data = sessionData;
        
        this.gridW = 28;
        this.gridH = 16;
        this.tileSize = 10;

        this.canvas.width = this.gridW * this.tileSize;
        this.canvas.height = this.gridH * this.tileSize;

        // Playback state
        this.isPlaying = false;
        this.speedMultiplier = 1;
        this.currentTick = 0;
        this.maxTick = 0;
        
        // Simulation history buffer for instant scrubbing
        this.frames = [];
        this.buildSimulationHistory();

        this.initControls();
        this.renderFrame(0);
    }

    buildSimulationHistory() {
        const rng = new DeterministicRNG(this.data.seed);
        let snake = [[14, 8], [13, 8], [12, 8]];
        let direction = 'R';
        let score = 0;
        let apples = 0;
        const walls = this.data.walls || [];
        const portals = this.data.portals || [];
        const wallSet = new Set(walls.map(w => `${w[0]},${w[1]}`));

        const ptsPerApple = { 'slug': 10, 'normal': 15, 'python': 25, 'cobra': 40 }[this.data.difficulty] || 15;

        function spawnFood(currentSnake) {
            const sSet = new Set(currentSnake.map(s => `${s[0]},${s[1]}`));
            for (let i = 0; i < 500; i++) {
                const fx = rng.nextInt(0, 27);
                const fy = rng.nextInt(0, 15);
                if (!wallSet.has(`${fx},${fy}`) && !sSet.has(`${fx},${fy}`)) {
                    return [fx, fy];
                }
            }
            return null;
        }

        let food = spawnFood(snake);
        const moveDict = {};
        (this.data.moves || []).forEach(m => {
            moveDict[m.t] = m.d;
        });

        const totalMoves = this.data.moves || [];
        const maxInputTick = totalMoves.length > 0 ? Math.max(...totalMoves.map(m => m.t)) : 0;
        this.maxTick = Math.max(maxInputTick + 2, 1);

        const dirOffsets = { 'U': [0, -1], 'D': [0, 1], 'L': [-1, 0], 'R': [1, 0] };
        const opposites = { 'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L' };

        for (let tick = 0; tick <= this.maxTick; tick++) {
            if (moveDict[tick] && moveDict[tick] !== opposites[direction]) {
                direction = moveDict[tick];
            }

            // Save state snapshot
            this.frames.push({
                tick: tick,
                snake: JSON.parse(JSON.stringify(snake)),
                direction: direction,
                food: food ? [...food] : null,
                score: score,
                apples: apples
            });

            // Advance
            const offset = dirOffsets[direction];
            const head = snake[0];
            let nx = head[0] + offset[0];
            let ny = head[1] + offset[1];

            if (this.data.mode === 'endless') {
                nx = (nx + this.gridW) % this.gridW;
                ny = (ny + this.gridH) % this.gridH;
            } else {
                if (nx < 0 || nx >= this.gridW || ny < 0 || ny >= this.gridH) break;
            }

            if (wallSet.has(`${nx},${ny}`)) break;
            if (snake.slice(0, -1).some(s => s[0] === nx && s[1] === ny)) break;

            snake.unshift([nx, ny]);
            if (food && nx === food[0] && ny === food[1]) {
                apples++;
                score += ptsPerApple;
                food = spawnFood(snake);
                if (!food) break;
            } else {
                snake.pop();
            }
        }

        this.maxTick = this.frames.length - 1;
    }

    initControls() {
        const playBtn = document.getElementById('btnReplayPlay');
        const scrubSlider = document.getElementById('replayScrubSlider');
        const speed1x = document.getElementById('btnSpeed1x');
        const speed2x = document.getElementById('btnSpeed2x');
        const speed4x = document.getElementById('btnSpeed4x');

        if (scrubSlider) {
            scrubSlider.max = this.maxTick;
            scrubSlider.addEventListener('input', (e) => {
                this.currentTick = parseInt(e.target.value);
                this.renderFrame(this.currentTick);
            });
        }

        if (playBtn) {
            playBtn.addEventListener('click', () => {
                this.isPlaying = !this.isPlaying;
                playBtn.innerHTML = this.isPlaying ? '⏸️ Pause' : '▶️ Play';
                if (this.isPlaying) this.playbackLoop();
            });
        }

        const setSpeed = (spd, activeBtn) => {
            this.speedMultiplier = spd;
            [speed1x, speed2x, speed4x].forEach(b => b?.classList.remove('btn-retro-gold'));
            activeBtn?.classList.add('btn-retro-gold');
        };

        if (speed1x) speed1x.addEventListener('click', () => setSpeed(1, speed1x));
        if (speed2x) speed2x.addEventListener('click', () => setSpeed(2, speed2x));
        if (speed4x) speed4x.addEventListener('click', () => setSpeed(4, speed4x));
    }

    playbackLoop() {
        if (!this.isPlaying) return;

        this.currentTick++;
        if (this.currentTick > this.maxTick) {
            this.currentTick = this.maxTick;
            this.isPlaying = false;
            const playBtn = document.getElementById('btnReplayPlay');
            if (playBtn) playBtn.innerHTML = '▶️ Replay';
            return;
        }

        this.renderFrame(this.currentTick);
        const slider = document.getElementById('replayScrubSlider');
        if (slider) slider.value = this.currentTick;

        const baseMs = { 'slug': 140, 'normal': 100, 'python': 70, 'cobra': 45 }[this.data.difficulty] || 100;
        const delay = Math.max(15, baseMs / this.speedMultiplier);

        setTimeout(() => this.playbackLoop(), delay);
    }

    renderFrame(tickIdx) {
        const frame = this.frames[tickIdx];
        if (!frame) return;

        const ctx = this.ctx;
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        const computedStyle = getComputedStyle(document.body);
        const pixelColor = computedStyle.getPropertyValue('--nokia-lcd-pixel').trim() || '#0f380f';

        // Draw Walls
        ctx.fillStyle = pixelColor;
        (this.data.walls || []).forEach(w => {
            ctx.fillRect(w[0] * this.tileSize, w[1] * this.tileSize, this.tileSize, this.tileSize);
        });

        // Draw Food
        if (frame.food) {
            ctx.fillRect(frame.food[0] * this.tileSize + 2, frame.food[1] * this.tileSize + 2, this.tileSize - 4, this.tileSize - 4);
        }

        // Draw Snake
        frame.snake.forEach((seg, i) => {
            ctx.fillRect(seg[0] * this.tileSize + 1, seg[1] * this.tileSize + 1, this.tileSize - 2, this.tileSize - 2);
        });

        // Update indicators
        const tickEl = document.getElementById('replayTickIndicator');
        const scoreEl = document.getElementById('replayScoreIndicator');
        if (tickEl) tickEl.innerText = `Tick: ${frame.tick} / ${this.maxTick}`;
        if (scoreEl) scoreEl.innerText = `Score: ${frame.score} (Apples: ${frame.apples})`;
    }
}
