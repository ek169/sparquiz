$(document).ready(function() {
    $("#add-class").click(function(e){
        e.preventDefault();
        var aElement = $(this).find("a");
        var url = aElement.attr("href");
        $.ajax({
            dataType: "text json",
            data: JSON.stringify({'answer': 'add'}),
            type: "POST",
            url: url,
            }).done(function() {
                $(aElement).replaceWith("<a>Request Sent!</a>")
            }).fail(function(){
                alert("Your response wasn't recorded");
            });
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
                    formDiv.replaceWith("<div><span><a>Got It!</a></span></div>")
                }).fail(function(){
                    alert("Your response wasn't recorded");
                });
            e.preventDefault();
        });
    }
});