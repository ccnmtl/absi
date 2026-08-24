export const toggleSpinnerState = (button, showSpinner = true) => {
    const $button = $(button);
    const $buttonSpinner = $button.find('.button-spinner');
    const $buttonText = $button.find('.button-text');

    if (showSpinner) {
        $buttonSpinner.removeClass('d-none');
        $buttonText.addClass('d-none');
    } else {
        $buttonSpinner.addClass('d-none');
        $buttonText.removeClass('d-none');
    }
};
