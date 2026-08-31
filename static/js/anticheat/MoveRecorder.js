/**
 * Anti-Cheat Move Recorder & Deterministic Random Generator (Client)
 */

class DeterministicRNG {
    constructor(seed) {
        this.seed = parseInt(seed) % 2147483647;
        if (this.seed <= 0) this.seed += 2147483646;
    }

    nextFloat() {
        this.seed = (this.seed * 16807) % 2147483647;
        return (this.seed - 1) / 2147483646.0;
    }

    nextInt(min, max) {
        return Math.floor(min + this.nextFloat() * (max - min + 1));
    }
}

class MoveRecorder {
    constructor(sessionId, seed) {
        this.sessionId = sessionId;
        this.seed = seed;
        this.startTime = Date.now();
        this.moves = [];
        this.lastDirection = 'R';
    }

    recordMove(tick, direction) {
        const timestamp = Date.now() - this.startTime;
        this.moves.push({
            t: tick,
            d: direction,
            ms: timestamp
        });
        this.lastDirection = direction;
    }

    getTelemetry() {
        return {
            sessionId: this.sessionId,
            durationSeconds: (Date.now() - this.startTime) / 1000,
            moveCount: this.moves.length,
            movesData: this.moves,
            checksum: this.generateChecksum()
        };
    }

    generateChecksum() {
        let hash = 0;
        const str = `${this.sessionId}-${this.seed}-${this.moves.length}`;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash |= 0;
        }
        return Math.abs(hash).toString(16);
    }
}
