/**
 * displayMessage for transcribe view.
 */
const displayMessage = function(msg, azure) {
    let el = $('#transcription-result');
    if (azure) {
        el = $('#azure-transcription-result>pre');
    };

    if (typeof msg === 'object') {
        msg = JSON.stringify(msg, null, '  ');
    }

    if (el.length) {
        $(el).text(msg);
    }
};

const socket = new WebSocket(
    'wss://' + window.location.host + '/ws/'
);

const parseAzureResponse = function(obj) {
    return JSON.stringify(obj);
};

/**
 * showToast for playblock/pagetree view.
 */
const showToast = function(title, body, time) {
    const $toast = $(`
    <div class="toast" role="alert" aria-live="assertive"
         data-bs-config='{"autohide":false}' aria-atomic="true">
      <div class="toast-header">
        <strong class="me-auto"></strong>
        <small></small>
        <button type="button" class="btn-close"
                data-bs-dismiss="toast" aria-label="Close">
        </button>
      </div>
      <div class="toast-body"></div>
    </div>`);

    $toast.find('.me-auto').text(title);
    $toast.find('small').text(time);

    if (body && typeof body === 'object') {
        body = parseAzureResponse(body);
    }

    $toast.find('.toast-body').text(body);
    $('#toast-container-0').append($toast);

    const toastBootstrap = bootstrap.Toast.getOrCreateInstance($toast[0]);
    toastBootstrap.show();
};

document.addEventListener('DOMContentLoaded', () => {
    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        let score = null;
        console.log('onmessage', data);

        if (data && data.message &&
            typeof data?.message?.['NBest']?.[0]?.[
                'PronunciationAssessment']?.['PronScore'] !== 'undefined'
        ) {
            score = data.message[
                'NBest'][0]['PronunciationAssessment']['PronScore'];
        }

        if (data && data.message) {
            displayMessage(data.message, data.azure);

            if (typeof score !== 'null') {
                showToast(
                    data.azure ? 'Azure Speech' : 'AWS Transcribe',
                    'Your score: ' + score, 'now');
            } else {
                showToast(
                    data.azure ? 'Azure Speech' : 'AWS Transcribe',
                    data.message || '', 'now');
            }
        }
    };

    socket.onclose = function(e) {
        const errorMessage =
              `Socket closed: code=${e.code}, reason=${e.reason || '(none)'}`;

        displayMessage(errorMessage);
        displayMessage(errorMessage, true);
        console.error(errorMessage, e);
    };
});
