$(document).ready(function () {

    $(".blogsbox").each(function (index,item) {
        $(item).attr('id','showlist-'+index)
    });
    $("div[id*=showlist-] img[class=blogs-update]").click(function () {
        $(this).next().toggle()
    });

    $("#comment-list>li").each(function (index,item) {
        $(item).attr('id','id-'+index)
    });

    $("li[id*=id-] span[id=reply]").click(function () {
        //根据li的id值区分
        $(this).parent().next().toggle();
    });

    $("li[id*=id-] span[id=reply-total]").click(function () {
        $(this).parent().next().next().slideToggle(1000);
    });

    $("#comment").focus(function () {
        $("#comment").animate({height:"120px"});
    });
    $("#comment").parent().blur(function () {
        $("#comment").animate({height:"40px"});
    });
    $("li[id*=id-] textarea").focus(function () {
        $(this).animate({height:"120px"});
    });
    $("li[id*=id-] form").blur(function () {
        $(this).animate({height:"40px"});
    });

});


