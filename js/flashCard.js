$(document).ready(function(){
    var questions;
    var url = $("#questions-link").val();
    alert(url);
    $.ajax({
        type: "POST",
        url: url,
        data: {"name":""},
        dataType: "html",
        async: false,
    }).done(function(json_output){
        questions = JSON.parse(json_output);
    });
    alert(questions);
    $(".card").flip({
        axis: 'x',
        trigger: 'hover'
    });
    var counter = 0;
    var frontDiv = $("#front");
    var backDiv = $("#back");
    var leftArrow = $("#left-arrow");
    var rightArrow = $("#right-arrow");

    checkCounter(counter);

    rightArrow.click(function(e){
        if(counter < questions.length - 1){
            counter = counter + 1;
            checkCounter(counter);
        }
        showQuestion(counter);
    });

    leftArrow.click(function(e){
        if(counter > 0){
            counter = counter - 1;
            checkCounter(counter);
        }
        showQuestion(counter);
    });

    function showQuestion(counter) {
        frontDiv.html(questions[counter].q);
        backDiv.html(questions[counter].a);
    }

    function checkCounter(counter){
        if(counter == 0) {
            leftArrow.hide();
            rightArrow.show();
            showQuestion(counter);
        } else if(counter == questions.length - 1) {
            rightArrow.hide();
            leftArrow.show();
        } else {
            leftArrow.show();
            rightArrow.show();
        }
    }

});