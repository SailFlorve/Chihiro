var searchvalue;
$("#showPart").hide();
$("#searchInformationPart").hide();


$("#showpicture").attr("src","http://img7.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2498971355.webp");
$("#name").text("马里奥·卡萨斯");
$("#chinesename").text("马里奥·卡萨斯");
$("#englishname").text("Mario Casas (Sierra)");
$("#elsename").text("马里奥·卡萨斯");
$("#country").text("西班牙");
$("#bornplace").text("西班牙，加利西亚自治区，拉科鲁尼亚省");
$("#borndata").text("1986年6月12日");
$("#representative").text("《SMS,sin miedo a soñar》，《天空之上三公尺》，《苏镇巫婆》，《Los Hombres de Paco》");
$("#prize").text("无");

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

