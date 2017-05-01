$(document).ready(function() {
    $(".difficulty-icon").tooltip();
    var statsDiv = $("#stats-side-div");
    $('.questionInfo').each(function(){
    var number = $(this).find("#question-difficulty");
    if(number){
        statsDiv.html('<span class="hover">Click <span class="glyphicon glyphicon-stats"></span> for more info</span>');
    }
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

    $(".difficulty-icon").click(function(e) {
        $(".question-view-format").each(function(){
            if($(this).parent().is("a")){
                $(this).unwrap();
            }
        });
        var question = $(this).closest(".questionInfo");
        question.find(".question-view-format").wrap('<a href="#"><a/>')
        var correctAns = $(this).find("#question-correct-answer").text();
        var correctAtt = $(this).find("#question-correct-attempts").text();
        var totalAtt = $(this).find("#question-total-attempts").text();
        statsDiv.html('<div class="center"><div><div class="side-bar-title">Correct Answer</div>' + correctAns + '</div><br>'
                         + '<div><div class="side-bar-title">Total Attempts</div>' + totalAtt + '</div></div>');

        e.preventDefault();

    });
});