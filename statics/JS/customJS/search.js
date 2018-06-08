var searchvalue;

/*searchvalue = $.cookie('svalue');
alert(searchvalue);
getshowdata(searchvalue);*/


// $("#successshow").append("<div class='showpart'></div>");
// $(".showpart").append("<div class='headtype'></div>");
// $(".headtype").append("<div class='headleft'></div>");
// $(".headleft").append("<a id='filmurl' style='text-decoration:none'><h3 id='title'></h3></a>");
// $(".headleft").append("<p id='ename' class='ename'></p>");
// $(".headleft").append("<p id='types' class='types'></p>");
// $(".headtype").append("<div class='headright'></div>");
// $(".headright").append("<img id='filmpicture'/>");
// $(".showpart").append("<div class='bottombody'></div>");
// $(".bottombody").append("<div class='bodytop'></div>");
// $(".bodytop").append("<span class='spanlable'></span>");
// $(".bodytop").append("<p>剧情简介</p>");
// $(".bodytop").append("<p id='introduction' class='a'>");
// $(".bottombody").append("<div class='bodybottom'></div>");
// $(".bodybottom").append("<span class='spanlable'></span>");
// $(".bodybottom").append("<p>演职人员</p>");
// $(".bodybottom").append("<div class='b'></div>");
// $(".b").append("<p>导演：<span id='director'></span></p>");
// $(".b").append("<p>主演：<span id='actor'></span></p>");
// $("#title").text("超时空同居");
// $("#filmurl").attr("href","http://maoyan.com/films/1208942")
// $("#ename").text("How Long Will I Love You");
// $("#types").text("喜剧,爱情,奇幻");
// $("#filmpicture").attr("src","http://p0.meituan.net/movie/f193e43ca706aa6bc6a26d6f53f0115a5315542.jpg@160w_220h_1e_1c");
// $("#introduction").text("来自2018年谷小焦（佟丽娅 饰）与1999年陆鸣（雷佳音 饰），两人时空重叠意外住在同一个房间。从互相嫌弃到试图“共谋大业”，阴差阳错发生了一系列好笑的事情。乐在其中的两人并不知道操控这一切的神秘人竟是想要去2037年“投机取巧”的2018年的……")
// $("#director").text("苏伦");
// $("#actor").text("雷佳音/佟丽娅/徐峥");
// $("#successshow").show();

$("#research").click(function(){
    $("#successshow").empty();
    searchvalue = $("#filmnameSearch").val();
    getshowdata(searchvalue);
})

function getshowdata(searchvalue)
{
    alert("into getshowdata()");
    $.ajax({
        type:"get",
        url:"/Search.php",
        dataType:"json",
        data:{
            filmName:searchvalue
        },
        success:function(data){
            //data的类型是string，故转换成json
            json = JSON.parse(data);
            if(!json.state){
                alert(json.messgae);
            }
            else {
                jsonData = json.data;//jsonData的结构是[{information of a movie},{},{}......]
                for(var i = 0; i< jsonData.length ; i++)
                {
                    //{information of a movie}是object型，故先转化为string，再转为json
                    json1 = JSON.parse(JSON.stringify(jsonData[i]));

                    $("#successshow").append("<div class='showpart'></div>");
                    $(".showpart").append("<div class='headtype'></div>");
                    $(".headtype").append("<div class='headleft'></div>");
                    $(".headleft").append("<a id='filmurl' style='text-decoration:none'><h3 id='title'></h3></a>");
                    $(".headleft").append("<p id='ename' class='ename'></p>");
                    $(".headleft").append("<p id='types' class='types'></p>");
                    $(".headtype").append("<div class='headright'></div>");
                    $(".headright").append("<img id='filmpicture'/>");
                    $(".showpart").append("<div class='bottombody'></div>");
                    $(".bottombody").append("<div class='bodytop'></div>");
                    $(".bodytop").append("<span class='spanlable'></span>");
                    $(".bodytop").append("<p>剧情简介</p>");
                    $(".bodytop").append("<p id='introduction' class='a'>");
                    $(".bottombody").append("<div class='bodybottom'></div>");
                    $(".bodybottom").append("<span class='spanlable'></span>");
                    $(".bodybottom").append("<p>演职人员</p>");
                    $(".bodybottom").append("<div class='b'></div>");
                    $(".b").append("<p>导演：<span id='director'></span></p>");
                    $(".b").append("<p>主演：<span id='actor'></span></p>");
                    $("#title").text(json1.title);
                    $("#filmurl").attr("href",json1.url);
                    $("#ename").text(json1.ename);
                    $("#types").text(json1.types);
                    $("#filmpicture").attr("src",json1.img);
                    $("#introduction").text(json1.body);
                    $("#director").text(json1.directors);
                    $("#actor").text(json1.actors);
                    $("#successshow").show();
                }
            }
        },
        error: function(data){
            $("#faild").show();
            console.error("出错了，返回的data：" + data);
        }
    }) 

}

