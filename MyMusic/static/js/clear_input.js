var box1 = document.getElementById("box1");
var box2 = document.getElementById("box2");
var box4 = document.getElementById("box4");

box1.onfocus = function () {
    if(box1.value == 'username'){
        this.value = "";
    }
};

box1.onblur = function () {
    if(box1.value == ""){
        box1.value = 'username';
    }
};



box2.onfocus = function () {
    if(box2.value == 'password'){
        this.value = "";
    }
};

box2.onblur = function () {
    if(box2.value == ""){
        box2.value = 'password';
    }
};


box4.onfocus = function () {
    if(box4.value == 'password'){
        this.value = "";
    }
};

box4.onblur = function () {
    if(box4.value == ""){
        box4.value = 'username';
    }
};

