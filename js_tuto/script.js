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
function match(str){
    let text = document.getElementById('box').innerHTML;
    console.log(text.match(str));
}
function parse_demo(){
    let text = document.getElementById('box').innerHTML;
    text = text + '<br>parseInt("-10") ' + parseInt("-10");
    text = text + '<br>parseInt("-10.33") ' + parseInt("-10.33");
    text = text + '<br>parseInt("10") ' + parseInt("10");
    text = text + '<br>parseInt("10.33") ' + parseInt("10.33");
    text = text + '<br>parseInt("10 20 30") ' + parseInt("10 20 30");
    text = text + '<br>parseInt("10 years") ' + parseInt("10 years");
    text = text + '<br>parseInt("years 10") ' + parseInt("years 10");
    text = text + '<br>parseFloat("10") ' + parseFloat("10");
    text = text + '<br>parseFloat("10.33") ' + parseFloat("10.33");
    text = text + '<br>parseFloat("10 20 30") ' + parseFloat("10 20 30");
    text = text + '<br>parseFloat("10 years") ' + parseFloat("10 years");
    text = text + '<br>parseFloat("years 10") ' + parseFloat("years 10");
    document.getElementById('box').innerHTML = text;
}
// foreach is not like others in js
function foreach_demo(){
    const cars = ['bmw','mercedes','audi','kia'];
    let text = '<ul>';
    cars.forEach((value) => {text += `<li>${value}</li>`});
    document.getElementById('box').innerHTML = text + '</ul>'
}
function concat_demo(){
    const arr1 = ["Emil", "Tobias", "Linus"];
    const myChildren = arr1.concat("Peter"); 
    document.getElementById('box').innerHTML = myChildren;
}
