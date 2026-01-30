const socket = new WebSocket(
    'wss://' + window.location.host + '/ws/'
);

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log('onmessage', data);

    const el = document.getElementById('transcription-result');

    if (el && data && data.message) {
        el.innerHTML = data.message;
    }
};

socket.onclose = function(e) {
    console.error('Socket closed unexpectedly');
};
