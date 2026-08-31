/**
 * Input Controller for Nokia 3310 Snake
 * Handles Keyboard, Touch Swipes, Virtual Keypad & Bezel Buttons
 */

class InputController {
    constructor(game) {
        this.game = game;
        this.touchStartX = 0;
        this.touchStartY = 0;
        this.init();
    }

    init() {
        // Keyboard Listener
        window.addEventListener('keydown', (e) => this.handleKeyDown(e));

        // Touch / Swipe Listener on Canvas
        const canvas = document.getElementById('snakeCanvas');
        if (canvas) {
            canvas.addEventListener('touchstart', (e) => {
                const touch = e.touches[0];
                this.touchStartX = touch.clientX;
                this.touchStartY = touch.clientY;
            }, { passive: true });

            canvas.addEventListener('touchend', (e) => {
                const touch = e.changedTouches[0];
                const dx = touch.clientX - this.touchStartX;
                const dy = touch.clientY - this.touchStartY;
                const absX = Math.abs(dx);
                const absY = Math.abs(dy);

                if (Math.max(absX, absY) > 20) {
                    if (absX > absY) {
                        this.game.queueDirection(dx > 0 ? 'R' : 'L');
                    } else {
                        this.game.queueDirection(dy > 0 ? 'D' : 'U');
                    }
                }
            }, { passive: true });
        }

        // Nokia Physical Keypad Buttons
        document.querySelectorAll('.phone-btn[data-key]').forEach(btn => {
            const handlePress = (e) => {
                e.preventDefault();
                const key = btn.getAttribute('data-key');
                this.handleKeyAction(key);
                
                // Visual feedback
                btn.classList.add('pressed');
                setTimeout(() => btn.classList.remove('pressed'), 120);

                if (window.soundEngine) {
                    window.soundEngine.playKeyClick();
                }
            };

            btn.addEventListener('mousedown', handlePress);
            btn.addEventListener('touchstart', handlePress, { passive: false });
        });
    }

    handleKeyDown(e) {
        // Avoid scrolling page with arrows/space
        if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(e.key)) {
            e.preventDefault();
        }

        switch (e.key) {
            // Directional Controls
            case 'ArrowUp':
            case 'w':
            case 'W':
            case '8':
                this.game.queueDirection('U');
                break;
            case 'ArrowDown':
            case 's':
            case 'S':
            case '2':
                this.game.queueDirection('D');
                break;
            case 'ArrowLeft':
            case 'a':
            case 'A':
            case '4':
                this.game.queueDirection('L');
                break;
            case 'ArrowRight':
            case 'd':
            case 'D':
            case '6':
                this.game.queueDirection('R');
                break;
            
            // Actions
            case ' ':
            case 'Enter':
                this.game.handleActionBtn();
                break;
            case 'Escape':
            case 'c':
            case 'C':
                this.game.handleBackBtn();
                break;
        }
    }

    handleKeyAction(key) {
        switch (key) {
            case '2':
            case 'UP':
                this.game.queueDirection('U');
                break;
            case '8':
            case 'DOWN':
                this.game.queueDirection('D');
                break;
            case '4':
            case 'LEFT':
                this.game.queueDirection('L');
                break;
            case '6':
            case 'RIGHT':
                this.game.queueDirection('R');
                break;
            case 'MENU':
            case 'START':
                this.game.handleActionBtn();
                break;
            case 'C':
            case 'BACK':
                this.game.handleBackBtn();
                break;
        }
    }
}
