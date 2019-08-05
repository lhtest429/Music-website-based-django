var a = document.getElementById("songlist").getElementsByTagName("div");
var zz =new Array(a.length);
for(var i=0;i <a.length;i++){
    zz[i]=a[i].innerHTML;
} //div的字符串数组付给zz
var pageno=1 ;              //当前页
var pagesize=5;            //每页多少条信息
if(zz.length%pagesize==0){
    var  pageall =zz.length/pagesize ;
}else{
    var  pageall =parseInt(zz.length/pagesize)+1;
}   //一共多少页

function change(e){
    pageno=e;
    if(e<1){ //如果输入页<1页
        e=1;pageno=1;//就等于第1页 ， 当前页为1
    }
    if(e>pageall){  //如果输入页大于最大页
        e=pageall;pageno=pageall; //输入页和当前页都=最大页
    }
    document.getElementById("all").innerHTML="";//全部清空
    for(var i=0;i<pagesize;i++){
        var div =document.createElement("li");//建立div对象
        div.innerHTML=zz[(e-1)*pagesize+i];//建立显示元素
        document.getElementById("all").appendChild(div);//加入all中
        if(zz[(e-1)*pagesize+i+1]==null) break;//超出范围跳出
    }
    var ye="";
    for(var j=1;j<=pageall;j++){
        if(e==j){
            ye=ye+"<span><a href='#' onClick='change("+j+")' style='color:#FF0000'>"+j+"</a></span> "
        }else{
            ye=ye+"<a href='#' onClick='change("+j+")'>"+j+"</a> "
        }
    }
    document.getElementById("a1").innerHTML=pageall;
    document.getElementById("a2").innerHTML=pageno;
    document.getElementById("a3").innerHTML=ye;
}
change(1);
