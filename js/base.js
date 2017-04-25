$(document).ready(function() {
    $('li.hover').hover(
        function() {
             $(this).find('ul').slideDown();
        },
        function() {
              $(this).find('ul').slideUp();
    });
});