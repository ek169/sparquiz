$(document).ready(function() {
    $("#add-class").click(function(e){
        var url = $(this).attr("href");
        var addDiv = $("#add-class-div");

        $.ajax({
            type: "GET",
            url: url,
            dataType: "text json",
            }).done(function(msg) {
                addDiv.replaceWith("<span><a>" + msg + "</a></span>")
            }).fail(function(){
                alert("Your response wasn't recorded");
            });
        e.preventDefault;
    });
});


$(document).on('click',':submit',function(e) {
    var answer = $(this).val();
    var form = $(this).parents('form:first');
    if(form.attr("name") == 'userAddForm') {
        $(form).submit(function(e){
            var url = $(this).attr("action");
            var formId = $(this).attr("id");
            var formDiv = $("#"+formId+"div");
            var uid = $("input[type=hidden][name=uid]").val();
            $.ajax({
            type: "POST",
            url: url,
            dataType: "text json",
            data: JSON.stringify({"uid": uid, "answer": answer}),
                }).done(function(msg) {
                    formDiv.replaceWith("<span><a>Got It!</a></span>")
                }).fail(function(){
                    alert("Your response wasn't recorded");
                });
            e.preventDefault();
        });
    }
});