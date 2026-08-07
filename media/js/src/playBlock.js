const reloadWord = () => {
    const word = $(
        '#listenTabContent .tab-pane.active .carousel-item.active .dabke-text'
    ).text().trim();
    const ipa = $(
        '#listenTabContent .tab-pane.active .carousel-item.active .dabke-ipa'
    ).text().trim();
    $('#transcribe_text').text(word);

    const audioEl = document.getElementById('absi-audio');
    audioEl.querySelectorAll('source').forEach((source) => {
        const url = new URL(source.src);
        url.searchParams.set('text', word);
        url.searchParams.set('ipa', ipa);
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

    const tabEl = document.querySelector(
        'button[data-bs-toggle="tab"]#listen-tab');
    if (tabEl) {
        tabEl.addEventListener('shown.bs.tab', event => {
            document.querySelectorAll('.float-box').forEach((box) => {
                box.style.display = 'none';
            });
        });
    }

    $('.dabke-syllable-play').on('click', () => {
        $audio[0].currentTime = 0;
        $audio[0].play();
    });

    $('.dabke-word-play').on('click', () => {
        reloadWord();
        $audio[0].currentTime = 0;
        $audio[0].play();
    });
});
