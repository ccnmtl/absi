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
    }
};
