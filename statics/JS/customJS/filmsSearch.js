var searchvalue;
$("#showPart").hide();
$("#searchInformationPart").hide();


$("#showpicture").attr("src","http://img7.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2498971355.webp");
$("#filmname").text("看不见的客人");
$("#elsename").text("死无对证");
$("#director").text("奥里奥尔保罗");
$("#actor").text("马里奥·卡萨斯阿娜·瓦格纳/何塞·科罗纳多/巴巴拉·莱涅/弗兰塞斯克·奥雷利亚");
$("#filmtype").text("剧情/悬疑/惊悚/犯罪");
$("#country").text("西班牙");
$("#language").text("西班牙语");
$("#releasedate").text("2017-09-15");
$("#time").text("106分钟");


$("#research").click(function(){
    searchvalue = $("#filmnameSearch").value;
    //getshowdata(searchvalue);
    //getinformation(searchvalue);
    $("#showPart").show();
    $("#searchInformationPart").show();
})

function getshowdata(searchvalue)
{
    $.ajax({
        type:"post",
        url:"/filmNameSearch",
        dataType:"json",
        data:{
            filmName:searchvalue
        },
        success:function(data){
            alert("data");
        },
        error: function(data){
            console.error("出错了，返回的data：" + data);
        }
    }) 

}

function getinformation(searchurl)
{
    $.ajax({
        type: "get",
        url: "",
        dataType: "json",
        success: function (data) {
            for (var i = 0; i < data.length; i++) {
                var $a = '<a>' + '</a>';
                $("#searchInformationPart").append($a).attr(data[i]);
            }
        },
        error: function (data) {
            console.error("出错了，返回的data：" + data);
        }
    });

}

