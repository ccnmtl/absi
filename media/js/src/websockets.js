import { state } from './state.js';
import { toggleSpinnerState } from './utils.js';
import WordAssessment from './WordAssessment.js';

const assessment = new WordAssessment();
state.assessment = assessment;

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

/**
 * showToast for playblock/pagetree view.
 */
const showToast = function(title, body, time) {
    console.log('showToast:', title, body, time);
};

document.addEventListener('DOMContentLoaded', () => {
    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        let score = null;
        let confidence = null;
        console.log('onmessage', data);

        if (data && data.message) {
            if (
                typeof data?.message?.['NBest']?.[0]?.[
                    'PronunciationAssessment']?.['PronScore'] !== 'undefined'
            ) {
                score = data.message[
                    'NBest'][0]['PronunciationAssessment']['PronScore'];
            }

            if (
                typeof data?.message?.['NBest']?.[0]?.['Confidence'] !==
                    'undefined'
            ) {
                confidence = data.message['NBest'][0]['Confidence'];

                if (typeof confidence === 'number') {
                    confidence = confidence.toFixed(2);
                }
            }
        }

        if (data && data.message) {
            displayMessage(data.message, data.azure);

            if (typeof score === 'number') {
                const recordButton = document.querySelector('.dabke-record');
                toggleSpinnerState(recordButton, false);
                $('.dabke-success-text').removeClass('d-none');
                $('.dabke-error-text').addClass('d-none');

                state.assessment.assess(score, confidence);
                showToast(
                    data.azure ? 'Azure Speech' : 'AWS Transcribe',
                    'Your score: ' + score +
                        ' (confidence: ' + confidence + ')',
                    'now');
            } else if (data.message.status === 'no_match') {
                toggleSpinnerState(recordButton, false);
                $('.dabke-error-text').removeClass('d-none');
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
