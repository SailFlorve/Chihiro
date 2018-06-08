var searchvalue;

$("#research").click(function(){
    searchvalue = $("#filmnameSearch").val();
    $.cookie('svalue',searchvalue);
    alert($.cookie("svalue"));
    window.open("search.html");
})
