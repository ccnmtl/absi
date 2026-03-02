const displayMessage = function(msg, azure) {
    $(document).ready(function() {
        let el = $('#transcription-result');
        if (azure) {
            el = $('#azure-transcription-result>pre');
        };

        if (el && msg) {
            if (typeof msg === 'object') {
                msg = JSON.stringify(msg, null, '  ');
            }

            $(el).text(msg);
        }
    });
};

const socket = new WebSocket(
    'wss://' + window.location.host + '/ws/'
);

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log('onmessage', data);

    if (data && data.message) {
        displayMessage(data.message, data.azure);
    }
};

socket.onclose = function(e) {
    const errorMessage = 'Socket closed unexpectedly';

    displayMessage(errorMessage);
    displayMessage(errorMessage, true);
    console.error(errorMessage);
};
