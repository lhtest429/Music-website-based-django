// // 设置input点击时的样式
var username = document.getElementById("username");
var password = document.getElementById("passwd");

username.onfocus = function() {
    if(this.value == "username or email") {
        this.value = "";
        this.style.backgroundColor = "rgb(211, 211, 211, 0.3)";
    }
};
username.onblur = function() {
    if(this.value == "") {
        this.value = "username or email";
        this.style.backgroundColor = "transparent";
    }
};

password.onfocus = function() {
    if(this.value == "password") {
        this.value = "";
        this.style.backgroundColor = "rgb(211, 211, 211, 0.3)";
    }
};
password.onblur = function() {
    if (this.value == "") {
        this.value = "password";
        this.style.backgroundColor = "transparent";
    }
};


var login = document.getElementById('login');
login.onclick = function () {
    var name = username.value.trim();
    var passwd = password.value.trim();

    // alert(name, passwd);

    if (name == "" || name=="username or email" || passwd == "" || passwd=="password"){
        alert("请输入合法的用户名或密码！");
        username.value = "username";
        password.value = "password";
        username.style.background = "transparent";
        password.style.background = "transparent";
    }
    else{
        login.setAttribute('href', "/index")
    }
};

// // 页面跳转
// var buttom = document.getElementById("login_button");
// buttom.onclick = function() {
//     if(username.value.trim() && password.value.trim() != "" &&
//         username.value.trim() != "username" &&
//         password.value.trim() != "password"
//     ) {
// //				window.location.href = 'study.html';
//         window.open("study.html");
//     } else {
//         alert("请输入合法的用户名或密码！");
//         username.value = "username";
//         password.value = "password";
//         username.style.background = "transparent";
//         password.style.background = "transparent";
//     }
//
//     // 设置cookies
//     document.cookie = "username=" + escape(username.value.trim()) + ";expires=" + (new Date().getTime());
//     document.cookie = "password=" + escape(password.value.trim()) + ";expires=" + (new Date().getTime());
// };
//
// function load() {
//     var username = document.getElementById("username");
//     var password = document.getElementById("password");
//     username.value = "username";
//     password.value = "password";
// }

