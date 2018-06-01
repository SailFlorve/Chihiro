var searchvalue;
$("#showPart").hide();
$("#searchInformationPart").hide();


$("#showpicture").attr("src","http://img7.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2498971355.webp");
$("#name").text("奥里奥尔·保罗");
$("#chinesename").text("奥里奥尔·保罗");
$("#englishname").text("Oriol Paulo");
$("#elsename").text("奥里奥尔·保罗");
$("#country").text("西班牙");
$("#bornplace").text("西班牙巴塞罗那");
$("#borndata").text("1975年");
$("#representative").text("看不见的客人、女尸谜案、茱莉娅的眼睛");
$("#prize").text("第27届西班牙戈雅奖-最佳新人导演奖提名");

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
        type:"get",
        url:searchurl,
        dataType:"json",
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

