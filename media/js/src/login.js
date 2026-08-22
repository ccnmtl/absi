$(document).ready(() => {
    $('.btn-guest-login').on('click', (e) => {
        $(e.target).closest('button').hide();
        $('.login-local-form').removeClass('d-none');
        $('.login-local-form #id_username').focus();
    });
});
