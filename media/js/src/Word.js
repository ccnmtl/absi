/**
 * Word class to encapsulate Arabic text + IPA functionality.
 */
export default class Word {
    constructor(text, ipa) {
        this.text = text;
        this.ipa = ipa;
    }

    selectWord(text, ipa) {
        this.text = text;
        this.ipa = ipa;

        // Reset success display state when new word is selected.
        $('.dabke-success-text').addClass('d-none');
    }
};
