function bright() {
    console.log("brighten");
    //why is document.getElementById('box') null
    document.getElementById("box").style.backgroundColor = 'azure';
    document.getElementById('text').innerHTML = "Azure";
}
function dark() {
    console.log("darken");
    document.getElementById('box').style.backgroundColor = 'dodgerblue';
    document.getElementById('text').innerHTML = 'dodgerblue';
}
function raiseAlert(){
    alert("YOU ARE UNDER ARREST");
    console.log(50/6);
}