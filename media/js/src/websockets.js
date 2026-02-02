const displayMessage = function(msg) {
    $(document).ready(function() {
        const el = $('#transcription-result');

        if (el && msg) {
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
        displayMessage(data.message);
    }
};

socket.onclose = function(e) {
    const errorMessage = 'Socket closed unexpectedly';

    displayMessage(errorMessage);
    console.error(errorMessage);
};
