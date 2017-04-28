$(document).ready(function() {
    $('.questionInfo').each(function(){
    var number = $(this).find("#question-difficulty");
    var difficulty = number.text();
    if(difficulty <= 33){
        number.css("color", "red");
    }
    else if(difficulty <= 67 && difficulty >= 34){
        number.css("color", "orange");
        }
    else {
        number.css("color", "green");
    }
    });

    var statsDiv = $("#stats-side-div");
    $(".difficulty-icon").click(function(e) {
        var correctAns = $(this).find("#question-correct-answer").text();
        var correctAtt = $(this).find("#question-correct-attempts").text();
        var totalAtt = $(this).find("#question-total-attempts").text();
        statsDiv.html('<div class="center"><div><div class="side-bar-title">Correct Answer</div>' + correctAns + '</div><br>'
                         + '<div><div class="side-bar-title">Total Attempts</div>' + totalAtt + '</div></div>');



    });
});