// // 设置input点击时的样式
var username = document.getElementById("username");
var password = document.getElementById("passwd");

username.onfocus = function() {
    if(this.value == "username or email") {
        this.value = "";
        // this.style.backgroundColor = "rgb(211, 211, 211, 0.3)";
        // this.style.backgroundColor = "#fff";
    }
};
username.onblur = function() {
    if(this.value == "") {
        this.value = "username or email";
        // this.style.backgroundColor = "transparent";
        // this.style.backgroundColor = "#fff";
    }
};

password.onfocus = function() {
    if(this.value == "password") {
        this.value = "";
        // this.style.backgroundColor = "rgb(211, 211, 211, 0.3)";
        // this.style.backgroundColor = "#fff";
    }
};
password.onblur = function() {
    if (this.value == "") {
        this.value = "password";
        // this.style.backgroundColor = "transparent";
        // this.style.backgroundColor = "#fff";
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
        // username.style.background = "transparent";
        // password.style.background = "transparent";

        username.style.background = "#fff";
        password.style.background = "#fff";
    }
    else{
        login.setAttribute('href', "/index")
    }
};