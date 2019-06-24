$(document).ready(function () {
    $(".blogs-update").click(function () {
        $("#blogs-control").toggle()
    });

    $("#reply").click(function () {
        $(".reply-form").toggle();
    });
    $("#reply-total").click(function () {
        console.log("hello");
        $("#reply-list").slideToggle(1000);
    });
    $("#comment").focus(function () {
        $("#comment").animate({height:"120px"});
    });
    $("#comment").blur(function () {
        $("#comment").animate({height:"40px"});
    });
    $("#reply").focus(function () {
        $("#reply").animate({height:"120px"});
    });
    $("#reply").blur(function () {
        $("#reply").animate({height:"40px"});
    });
});


