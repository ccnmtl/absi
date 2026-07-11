import {
    computePosition, flip, offset, shift
} from 'https://cdn.jsdelivr.net/npm/@floating-ui/dom@latest/+esm';

document.querySelectorAll('.wrapped-word').forEach((anchor) => {
    const box = document.querySelector('.float-box');

    if (!box) {
        return;
    }

    function update() {
        computePosition(anchor, box, {
            placement: 'top',
            middleware: [
                offset(6), flip(), shift()
            ],
        }).then(({ x, y }) => {
            Object.assign(box.style, {
                left: `${x}px`,
                top: `${y}px`,
            });
        });
    }

    function show() {
        box.style.display = 'block';
        update();
    }

    function hide() {
        box.style.display = 'none';
    }

    function toggle(event) {
        event.stopPropagation();

        document.querySelectorAll('.float-box').forEach((otherBox) => {
            otherBox.style.display = 'none';
        });

        show();

        const word = $(event.target).text().trim();
        $('#transcribe_text').text(word);

        const audioEl = document.getElementById('absi-audio');
        audioEl.querySelectorAll('source').forEach((source) => {
            const url = new URL(source.src);
            url.searchParams.set('text', word);
            source.src = url.toString();
        });
        audioEl.load();

        return audioEl.play();
    }

    anchor.addEventListener('click', toggle);
    anchor.addEventListener('focus', show);
    anchor.addEventListener('blur', hide);
});

document.addEventListener('DOMContentLoaded', () => {
    const floating = document.getElementById('floating');

    document.addEventListener('mousemove', ({ clientX, clientY }) => {
        if (!floating) return;

        Object.assign(floating.style, {
            position: 'fixed',
            left: `${clientX}px`,
            top: `${clientY}px`,
            transform: 'translate(-50%, -50%)',
            pointerEvents: 'none',
        });
    });

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

    $('.dabke-word-play,.dabke-syllable-play').on('click', () => {
        $audio[0].currentTime = 0;
        $audio[0].play();
    });
});
