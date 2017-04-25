$(document).ready(function() {

    $('#question-type').on('change',function(){
    $("#correct-answer").find("a").remove();
    $("#other-answers-div").show();
    $("#other-answers-div :input").attr("disabled", false);
    $("#correct-answer :input").attr("disabled", false);
    $("#answer-label").find("select").remove();
    $("#correct-answer").show();
    if( $(this).val()==="multiple"){
    $("input#first-correct.form-control").append("<span class='glyphicon glyphicon-plus'></span>")
    }
    else if( $(this).val()==="check"){
        $("#first-correct").after('<a href="#"><span id="add-correct-answer" class="add-input glyphicon glyphicon-plus"></span></a>');
        var correctAnswers = $('#correct-answer');
        var correctTotal = $('#correct-answer p').size() + 1;
        $("#add-correct-answer").click(function() {
            var newCorrect = $('<p><label><input class="form-control" type="text" name="correctAnswer' + correctTotal + '"/></label><a href="#"><span class="delete-input glyphicon glyphicon-minus"></span></a></p>');
            newCorrect.appendTo(correctAnswers);
            correctTotal++;

            $('[name*="correctAnswer"]').each(function () {
                $(this).rules('add', "required");
            });
            return false;
        });

        $("body").on("click", ".delete-input", function() {
            $(this).parents("p").remove();
            correctTotal--;
            return false;
	    });
    }
    else if( $(this).val()==="true/false") {
    $("#other-answers-div").find("p").slice(1).remove();
    $("#other-answers-div").hide();
    $("#other-answers-div :input").attr("disabled", true);
    $("#correct-answer").find("p").slice(1).remove();
    $("#correct-answer").hide();
    $("#correct-answer :input").attr("disabled", true);
    $("#answer-label").append("<div><select name='correctAnswer' class='form-control'><option value='true'>True</option><option value='false'>False</option></select></div>");
    }
});


var otherAnswers = $('#other-answers');
var otherTotal = $('#other-answers p').size() + 1;
$("#add-other-answers").click(function() {
    var newOther = $('<p><label><input class="form-control" type="text" name="otherAnswers' + otherTotal + '"/></label><a href="#"><span class="delete-input glyphicon glyphicon-minus"></span></a></p>');
    newOther.appendTo(otherAnswers);
    otherTotal++;
    $('[name*="otherAnswers"]').each(function () {
        $(this).rules('add', "required");
    });

    return false;

});

$("body").on("click", ".delete-input", function() {
    $(this).parents("p").remove();
    otherTotal--;
    return false;

});

    jQuery.validator.setDefaults({
        errorPlacement: function(error, element) {
            if (element.attr("name") == "correctAnswer1"){
                error.appendTo("#correct-answer-error");
                }
            if (element.attr("name") == "otherAnswers1") {
                error.appendTo("#other-answer-error");
            }
        }
    });



    $("#create-question").validate({
    errorElement: 'p',
    errorClass: 'errMsg',
    rules: {
      questionType: {
        required: true,
        minlength: 1,
      },
      question: {
        required: true,
       },
      otherAnswers1: {
        required: true,
      },
      correctAnswer1: {
        required: true,
      },
      },
});


});




