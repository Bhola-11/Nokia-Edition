/**
 * Nokia 3310 Live Shell & Theme Switcher
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Live Clock on LCD Status Bar
    function updateClock() {
        const now = new Date();
        const hrs = String(now.getHours()).padStart(2, '0');
        const mins = String(now.getMinutes()).padStart(2, '0');
        const clockEl = document.getElementById('lcdClock');
        if (clockEl) clockEl.innerText = `${hrs}:${mins}`;
    }
    updateClock();
    setInterval(updateClock, 10000);

    // 2. Theme & Shell Quick Selector
    const themeSelect = document.getElementById('quickThemeSelect');
    const shellSelect = document.getElementById('quickShellSelect');
    const soundToggle = document.getElementById('quickSoundToggle');
    const ringtoneBtn = document.getElementById('btnPlayRingtone');

    if (themeSelect) {
        themeSelect.addEventListener('change', (e) => {
            document.documentElement.setAttribute('data-theme', e.target.value);
            saveQuickSetting({ theme: e.target.value });
        });
    }

    if (shellSelect) {
        shellSelect.addEventListener('change', (e) => {
            document.documentElement.setAttribute('data-shell', e.target.value);
            saveQuickSetting({ phone_shell: e.target.value });
        });
    }

    if (soundToggle) {
        soundToggle.addEventListener('change', (e) => {
            if (window.soundEngine) {
                window.soundEngine.setEnabled(e.target.checked);
            }
            saveQuickSetting({ sound_enabled: e.target.checked });
        });
    }

    if (ringtoneBtn) {
        ringtoneBtn.addEventListener('click', () => {
            if (window.soundEngine) {
                window.soundEngine.playNokiaTune();
            }
        });
    }

    function saveQuickSetting(payload) {
        fetch('/accounts/api/quick-settings/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(payload)
        }).catch(err => console.log('Saved locally'));
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
