$(document).ready(function() {
    $("#addUser").submit(function(e) {
      e.preventDefault();
      var $form = $( this ),
          url = $form.attr( 'action' );

      /* Send the data using post with element id name and name2*/
      var postToMain = $.post( url, { uid: $("uid").val(), answer: $("answer").val() } );

      /* Alerts the results */
      posting.done(function( data ) {
        alert("Submitted!");
      });
    });
});