const socket = new WebSocket(
    'wss://' + window.location.host + '/ws/'
);

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log('onmessage', data);
};

socket.onclose = function(e) {
    console.error('Socket closed unexpectedly');
};
