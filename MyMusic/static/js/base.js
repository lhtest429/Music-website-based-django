// 导航栏
var tit = document.getElementById("navigation");
// var tit = document.getElementsByClassName("navigation");
//alert(tit);
//占位符的位置
var rect = tit.getBoundingClientRect();//获得页面中导航条相对于浏览器视窗的位置
var inser = document.createElement("div");
tit.parentNode.replaceChild(inser, tit);
inser.appendChild(tit);
inser.style.height = rect.height + "px";
inser.style.width = rect.width + "px";

//获取距离页面顶端的距离
var titleTop = tit.offsetTop;
//滚动事件
document.onscroll = function () {
    //获取当前滚动的距离
    var btop = document.body.scrollTop || document.documentElement.scrollTop;
    //如果滚动距离大于导航条据顶部的距离
    if (btop > titleTop) {
        //为导航条设置fix
        tit.className = "clearfix fix";
    } else {
        //移除fixed
        tit.className = "clearfix";
    }
};


//================================================================================================

// 弹出窗口
// $(function() {
//     $('#input_button').click(function () {
//         pupopTip('300px','150px','请稍后...',"确认");
//     })
// });

// 搜索框
var input_text = document.getElementById('input_text');
input_text.onfocus = function () {
    if(input_text.value == '伟大的渺小  林俊杰'){
        this.value = "";
    }
};

input_text.onblur = function () {
    if(input_text.value == ""){
        input_text.value = '伟大的渺小  林俊杰';
    }
};


// 回到顶部

var timer  = null;
fixed.onclick = function(){
    cancelAnimationFrame(timer);
    //获取当前毫秒数
    var startTime = +new Date();
    //获取当前页面的滚动高度
    var b = document.body.scrollTop || document.documentElement.scrollTop;
    var d = 500;
    var c = b;
    timer = requestAnimationFrame(function func(){
        var t = d - Math.max(0,startTime - (+new Date()) + d);
        document.documentElement.scrollTop = document.body.scrollTop = t * (-c) / d + b;
        timer = requestAnimationFrame(func);
        if(t == d){
          cancelAnimationFrame(timer);
        }
    });
};


// 滚动出现





