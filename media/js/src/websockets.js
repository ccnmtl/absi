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
    } else {
        console.log('el is empty:', el, msg, azure);
    }
};

const socket = new WebSocket(
    'wss://' + window.location.host + '/ws/'
);

const parseAzureResponse = function(obj) {
    return JSON.stringify(obj);
};

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
        console.log('onmessage', data);

        if (data && data.message) {
            displayMessage(data.message, data.azure);

            showToast(
                data.azure ? 'Azure Speech' : 'AWS Transcribe',
                data.message || '', 'now');
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
