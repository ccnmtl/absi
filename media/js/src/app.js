const MAX_SECONDS = 5;

// Set up basic variables for app
const record = document.querySelector('.record');
const stop = document.querySelector('.stop');
const soundClips = document.querySelector('.sound-clips');
const canvas = document.querySelector('.visualizer');
const mainSection = document.querySelector('.main-controls');

// Disable stop button while not recording
stop.disabled = true;

// Visualiser setup - create web audio api context and canvas
let audioCtx;
const canvasCtx = canvas.getContext('2d');

const queueTranscribeJob = function(uri) {
    console.log('queueTranscribeJob', uri);
    return fetch('/api/transcribe/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`
        },
        mode: 'same-origin',
        body: JSON.stringify({
            s3_uri: uri
        })
    });
};

const queueAzureTranscribeJob = function(uri) {
    const transcribeText = jQuery('[name="transcribe_text"]').val();
    console.log('queueAzureTranscribeJob', uri, transcribeText);
    return fetch('/api/azure_transcribe/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`
        },
        mode: 'same-origin',
        body: JSON.stringify({
            s3_uri: uri,
            transcribe_text: transcribeText
        })
    });
};

// Main block for doing the audio recording
if (navigator.mediaDevices.getUserMedia) {
    console.log('The mediaDevices.getUserMedia() method is supported.');

    const constraints = { audio: true };
    let chunks = [];

    const stopRecording = function(media) {
        media.stop();
        console.log(media.state);
        console.log('Recorder stopped.');
        record.style.background = '';
        record.style.color = '';

        stop.disabled = true;
        record.disabled = false;
    };

    let onSuccess = function(stream) {
        const mediaRecorder = new MediaRecorder(stream);

        visualize(stream);

        record.onclick = function() {
            mediaRecorder.start();
            console.log(mediaRecorder.state);
            console.log('Recorder started.');
            record.style.background = 'red';

            stop.disabled = false;
            record.disabled = true;

            setTimeout(() => {
                if (mediaRecorder.state === 'recording') {
                    stopRecording(mediaRecorder);
                }
            }, MAX_SECONDS * 1000);
        };

        stop.onclick = function() {
            stopRecording(mediaRecorder);
        };

        mediaRecorder.onstop = function(e) {
            console.log(
                'Last data to read (after MediaRecorder.stop() called).');

            const d = new Date();
            const clipName = d.toISOString();

            const clipContainer = document.createElement('article');
            const clipLabel = document.createElement('p');
            const audio = document.createElement('audio');
            const deleteButton = document.createElement('button');

            clipContainer.classList.add('clip');
            audio.setAttribute('controls', '');
            deleteButton.textContent = 'Delete';
            deleteButton.className = 'delete';

            if (clipName === null) {
                clipLabel.textContent = 'My unnamed clip';
            } else {
                clipLabel.textContent = clipName;
            }

            clipContainer.appendChild(audio);
            clipContainer.appendChild(clipLabel);
            clipContainer.appendChild(deleteButton);
            soundClips.appendChild(clipContainer);

            audio.controls = true;
            const blob = new Blob(chunks, { type: mediaRecorder.mimeType });
            chunks = [];
            const audioURL = window.URL.createObjectURL(blob);
            audio.src = audioURL;
            console.log('recorder stopped');

            deleteButton.onclick = function(e) {
                e.target.closest('.clip').remove();
            };

            const s3upload = new S3Upload({
                file_dom_selector: null,
                s3_sign_put_url: '/s3sign/',
                onFinishS3Put: function(publicUrl) {
                    // Submit to django view queueing transcribe job
                    queueTranscribeJob(publicUrl);

                    // Transcribe in Azure as well.
                    queueAzureTranscribeJob(publicUrl);
                }
            });

            s3upload.uploadFile(blob);
        };

        mediaRecorder.ondataavailable = function(e) {
            chunks.push(e.data);
        };
    };

    let onError = function(err) {
        console.log('The following error occured: ' + err);
    };

    navigator.mediaDevices.getUserMedia(constraints).then(onSuccess, onError);
} else {
    console.log('MediaDevices.getUserMedia() not supported on your browser!');
}

function visualize(stream) {
    if (!audioCtx) {
        audioCtx = new AudioContext();
    }

    const source = audioCtx.createMediaStreamSource(stream);

    const bufferLength = 2048;
    const analyser = audioCtx.createAnalyser();
    analyser.fftSize = bufferLength;
    const dataArray = new Uint8Array(bufferLength);

    source.connect(analyser);

    draw();

    function draw() {
        const WIDTH = canvas.width;
        const HEIGHT = canvas.height;

        requestAnimationFrame(draw);

        analyser.getByteTimeDomainData(dataArray);

        canvasCtx.fillStyle = 'rgb(200, 200, 200)';
        canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

        canvasCtx.lineWidth = 2;
        canvasCtx.strokeStyle = 'rgb(0, 0, 0)';

        canvasCtx.beginPath();

        let sliceWidth = (WIDTH * 1.0) / bufferLength;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
            let v = dataArray[i] / 128.0;
            let y = (v * HEIGHT) / 2;

            if (i === 0) {
                canvasCtx.moveTo(x, y);
            } else {
                canvasCtx.lineTo(x, y);
            }

            x += sliceWidth;
        }

        canvasCtx.lineTo(canvas.width, canvas.height / 2);
        canvasCtx.stroke();
    }
}

window.onresize = function() {
    canvas.width = mainSection.offsetWidth;
};

window.onresize();

$(document).ready(function() {
    const $textarea = $('textarea[name="transcribe_text"]');
    $('.absi-text-buttons button').click(function(e) {
        let text = $(this).text();
        if (text) {
            text = text.trim();
        }

        $textarea.text(text);
    });
});
