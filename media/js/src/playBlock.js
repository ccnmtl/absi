import { state } from './state.js';
import Word from './Word.js';

const word = new Word();
state.word = word;

/**
 * reloadWord()
 *
 * Load selected word to <audio> tag source for playback.
 */
const reloadWord = () => {
    const arbText = $(
        '#listenTabContent .tab-pane.active .carousel-item.active .dabke-text'
    ).text().trim();
    const ipa = $(
        '#listenTabContent .tab-pane.active .carousel-item.active .dabke-ipa'
    ).text().trim();

    word.selectWord(arbText, ipa);

    $('#transcribe_text').text(word.text);

    const audioEl = document.getElementById('absi-audio');
    audioEl.querySelectorAll('source').forEach((source) => {
        const url = new URL(source.src);
        url.searchParams.set('text', word.text);
        url.searchParams.set('ipa', word.ipa);
        source.src = url.toString();
    });
    audioEl.load();
};

document.addEventListener('DOMContentLoaded', () => {
    // https://getbootstrap.com/docs/5.3/getting-started/javascript/#sanitizer
    const myDefaultAllowList = bootstrap.Tooltip.Default.allowList;
    myDefaultAllowList.audio = ['controls'];

    const $audio = $('#absi-audio');

    if ($audio.length > 0) {
        $('input[name="radioVoice"]').on('change', (e) => {
            if (e.target && e.target.value) {
                const voice = e.target.value;
                $audio.find('source').each((i, source) => {
                    const src = source.src;
                    const url = new URL(src);

                    url.searchParams.set('voice', voice);

                    source.src = url;
                });

                // Reload audio
                $audio[0].load();
                $audio[0].play();

                // Save this voice to user's profile.
                (async() => {
                    await fetch('/api/userprofile/update/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken,
                        },
                        credentials: 'same-origin',
                        body: JSON.stringify({
                            voice: voice
                        }),
                    });
                })();
            }
        });
    }

    $('.dabke-practice-next-button').on('click', function() {
        const trigger = document.querySelector(
            '[data-bs-target="#practice-tab-pane"]');
        bootstrap.Tab.getOrCreateInstance(trigger).show();
    });

    document.getElementById('dabke-review-next-button')
        .addEventListener('click', function() {
            const trigger = document.querySelector(
                '[data-bs-target="#review-tab-pane"]');
            bootstrap.Tab.getOrCreateInstance(trigger).show();
        });

    document.getElementById('dabke-assess-next-button')
        .addEventListener('click', function() {
            const trigger = document.querySelector(
                '[data-bs-target="#assess-tab-pane"]');
            bootstrap.Tab.getOrCreateInstance(trigger).show();
        });

    document.getElementById('dabke-listen-button')
        .addEventListener('click', function() {
            const trigger = document.querySelector(
                '[data-bs-target="#listen-tab-pane"]');
            bootstrap.Tab.getOrCreateInstance(trigger).show();
        });

    const practiceTab = document.querySelector(
        'button[data-bs-toggle="tab"]#practice-tab');
    if (practiceTab) {
        practiceTab.addEventListener('shown.bs.tab', event => {
            const practiceTab = $('#practice-tab-pane');
            practiceTab.find('.dabke-text').text(word.text);
            practiceTab.find('.dabke-ipa').text(word.ipa);
        });
    }

    $('.dabke-word-play').on('click', () => {
        reloadWord();
        $audio[0].currentTime = 0;
        $audio[0].play();
    });

    $('.carousel').each((_, carousel) => {
        carousel.addEventListener('slid.bs.carousel', event => {
            const selectedIndex = event.to;
            const selected = $(carousel).find(
                '.carousel-inner .carousel-item')[selectedIndex];

            const text = $(selected).find('.dabke-text').text();
            const ipa = $(selected).find('.dabke-ipa').text();
            word.selectWord(text, ipa);
        });
    });

    const wordTabs = document.querySelectorAll(
        '#word-example-tabs button[data-bs-toggle="tab"]');
    wordTabs.forEach(tabEl => {
        tabEl.addEventListener('shown.bs.tab', event => {
            const targetTab = event.target.getAttribute('data-bs-target');
            const targetTabEl = $(targetTab);
            const text = targetTabEl.find(
                '.carousel-inner .carousel-item.active .dabke-text').text();
            const ipa = targetTabEl.find(
                '.carousel-inner .carousel-item.active .dabke-ipa').text();

            word.selectWord(text, ipa);
        });
    });
});
