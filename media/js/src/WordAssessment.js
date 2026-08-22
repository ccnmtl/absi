export default class WordAssessment {
    constructor(score, confidence) {
        this.score = score;
        this.confidence = confidence;
    }

    assess(score, confidence) {
        this.score = score;
        this.confidence = confidence;

        if ($) {
            $('.dabke-score-summary').removeClass('d-none');
            $('.dabke-score').text(score);
        }
    }
};
