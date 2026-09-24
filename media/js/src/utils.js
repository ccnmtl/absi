const audioMimeTypes = {
    m4a: 'audio/mp4',
    mp4: 'audio/mp4',
    webm: 'audio/webm',
    ogg: 'audio/ogg',
    mp3: 'audio/mpeg',
    wav: 'audio/wav',
    flac: 'audio/flac',
};

function getAudioMimeType(url) {
    const extension = new URL(url)
        .pathname
        .split('.')
        .pop()
        .toLowerCase();

    return audioMimeTypes[extension] || '';
}

export const toggleSpinnerState = (button, showSpinner = true) => {
    const $button = $(button);
    const $buttonSpinner = $button.find('.button-spinner');
    const $buttonText = $button.find('.button-text');

    if (showSpinner) {
        $buttonSpinner.removeClass('d-none');
        $buttonText.addClass('d-none');
    } else {
        $buttonSpinner.addClass('d-none');
        $buttonText.removeClass('d-none');
    }
};

export const updateRecordingSource = (url) => {
    const audioTag = document.getElementById('dabke-audio-recording');

    audioTag.querySelectorAll('source').forEach(source => source.remove());

    const source = document.createElement('source');
    source.src = url;
    source.type = getAudioMimeType(url);

    audioTag.appendChild(source);
};

/**
 * Given a list of tabs and an active tab, return the next tab as a
 * dom element. Cycles to the first tab at the end.
 */
export const getNextTab = ($tabList, $activeTab) => {
    const activeIdx = $tabList.index($activeTab);
    const nextIdx = (activeIdx + 1) % $tabList.length;
    return $tabList[nextIdx];
};

export const getPrevTab = ($tabList, $activeTab) => {
    const activeIdx = $tabList.index($activeTab);
    let prevIdx = (activeIdx - 1 + $tabList.length) % $tabList.length;
    return $tabList[prevIdx];
};
