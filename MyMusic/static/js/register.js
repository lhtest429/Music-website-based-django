var username = document.getElementById('username');
var email = document.getElementById('passwd');
var password = document.getElementById('confirm');

username.onfocus = function() {
    if(this.value == "username") {
        this.value = "";
        this.style.backgroundColor = "rgb(211, 211, 211, 0.3)";
    }
};
username.onblur = function() {
    if(this.value == "") {
        this.value = "username";
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

email.onfocus = function() {
    if(this.value == "email address") {
        this.value = "";
        this.style.backgroundColor = "rgb(211, 211, 211, 0.3)";
    }
};
email.onblur = function() {
    if (this.value == "") {
        this.value = "email address";
        this.style.backgroundColor = "transparent";
    }
};