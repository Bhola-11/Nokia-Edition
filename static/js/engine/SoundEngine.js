/**
 * Web Audio API 8-Bit Retro Sound Synthesizer for Nokia 3310 Snake
 */
class SoundEngine {
    constructor() {
        this.ctx = null;
        this.enabled = true;
        this.volume = 0.8;
    }

    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) {
                this.ctx = new AudioContext();
            }
        }
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    setVolume(vol) {
        this.volume = Math.max(0, Math.min(1, vol / 100));
    }

    setEnabled(isEnabled) {
        this.enabled = !!isEnabled;
    }

    playTone(freq, type = 'square', duration = 0.08, startTime = 0) {
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;

        try {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();

            osc.type = type;
            osc.frequency.setValueAtTime(freq, this.ctx.currentTime + startTime);

            gain.gain.setValueAtTime(this.volume * 0.3, this.ctx.currentTime + startTime);
            gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + startTime + duration);

            osc.connect(gain);
            gain.connect(this.ctx.destination);

            osc.start(this.ctx.currentTime + startTime);
            osc.stop(this.ctx.currentTime + startTime + duration);
        } catch (e) {
            console.warn("Audio play error", e);
        }
    }

    playEat() {
        // Classic Nokia Snake Apple Chime (Short high square blip)
        this.playTone(880, 'square', 0.06, 0);
        this.playTone(1174, 'square', 0.08, 0.04);
    }

    playBonus() {
        // Special 3-note golden apple chime
        this.playTone(659.25, 'square', 0.07, 0);
        this.playTone(830.61, 'square', 0.07, 0.07);
        this.playTone(1046.50, 'square', 0.12, 0.14);
    }

    playDie() {
        // Crash buzz (descending frequency harsh square wave)
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;

        try {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();

            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(320, this.ctx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(40, this.ctx.currentTime + 0.4);

            gain.gain.setValueAtTime(this.volume * 0.5, this.ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.4);

            osc.connect(gain);
            gain.connect(this.ctx.destination);

            osc.start(this.ctx.currentTime);
            osc.stop(this.ctx.currentTime + 0.45);
        } catch (e) {}
    }

    playKeyClick() {
        // Physical key click
        this.playTone(1800, 'triangle', 0.015, 0);
    }

    playLevelUp() {
        // Victory fanfare
        const notes = [523.25, 659.25, 783.99, 1046.50];
        notes.forEach((freq, idx) => {
            this.playTone(freq, 'square', 0.1, idx * 0.08);
        });
    }

    playNokiaTune() {
        // The legendary Nokia Tune (Gran Vals by Francisco Tárrega)
        const notes = [
            { f: 659.25, d: 0.15 }, // E5
            { f: 587.33, d: 0.15 }, // D5
            { f: 369.99, d: 0.30 }, // F#4
            { f: 415.30, d: 0.30 }, // G#4
            { f: 554.37, d: 0.15 }, // C#5
            { f: 493.88, d: 0.15 }, // B4
            { f: 293.66, d: 0.30 }, // D4
            { f: 329.63, d: 0.30 }, // E4
            { f: 493.88, d: 0.15 }, // B4
            { f: 440.00, d: 0.15 }, // A4
            { f: 277.18, d: 0.30 }, // C#4
            { f: 329.63, d: 0.30 }, // E4
            { f: 440.00, d: 0.60 }, // A4
        ];

        let offset = 0;
        notes.forEach(n => {
            this.playTone(n.f, 'square', n.d * 0.9, offset);
            offset += n.d;
        });
    }
}

window.soundEngine = new SoundEngine();
