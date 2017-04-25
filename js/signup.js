$(document).ready(function() {
    $("#sign-up").validate({
        errorElement: 'span',
        errorClass: 'errMsg',
        rules: {
        verify: "required",
        username: {
            required: true,
            minlength: 5,
        },
        password: {
            required: true,
            minlength: 4,
            alphanumeric: true,
            nowhitespace: true,
        },
        email: {
            email: true,
            required: true,
        }
        },
        messages: {
            username: "You must provide a username",
        password: {
            required: "Your password is invalid",
            alphanumeric: "Your password must contain at least one number",
        },
        email: "You must provide a valid email address",
        },

    });
});