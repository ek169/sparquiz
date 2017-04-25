$(document).ready(function() {
    var difficulty = $("#question-difficulty");
    var questionBorder = $("#question-border");
    if(difficulty <= 33){
        questionBorder.css("color", "red");
    }
    else if(difficulty <= 67 && difficulty >= 34){
        questionBorder.css("border-color", "yellow");
        }
    else {
        questionBorder.css("border-color", "green");
    }
});