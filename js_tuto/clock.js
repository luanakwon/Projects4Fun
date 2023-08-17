function spreadDigits(){
    const digits = document.getElementsByClassName('digit');
    console.log(digits);
    
    for (let i=0;i<digits.length;i++){
        // theta = angle from 12 O'clock
        let theta = (i+1)*Math.PI/6;
        // x, y converted to 0~100
        let x = (Math.sin(theta)+1)*50;
        let y = (Math.cos(theta)+1)*50;
        digits[i].style.left = `${x.toFixed(2)}%`;
        digits[i].style.bottom = `${y.toFixed(2)}%`;
    }
}
function setTime(){
    let hour_hand = document.getElementById('hour');
    let min_hand = document.getElementById('min');
    let sec_hand = document.getElementById('sec');
    let d = new Date();
    
    hour_hand.animate([
        {transform: `rotate(${d.getHours()%12*30-180}deg)`},
        {transform: `rotate(${d.getHours()%12*30}deg)`},
        {transform: `rotate(${d.getHours()%12*30+180}deg)`}
    ],{
        duration: 43200000,
        iterations: Infinity
    });
    
    min_hand.animate([
        {transform: `rotate(${d.getMinutes()*6-180}deg)`},
        {transform: `rotate(${d.getMinutes()*6}deg)`},
        {transform: `rotate(${d.getMinutes()*6+180}deg)`}
    ],{
        duration: 3600000,
        iterations: Infinity
    });
    
    sec_hand.animate([
        {transform: `rotate(${d.getSeconds()*6-180}deg)`},
        {transform: `rotate(${d.getSeconds()*6}deg)`},
        {transform: `rotate(${d.getSeconds()*6+180}deg)`}
    ],{
        duration: 60000,
        iterations: Infinity
    });
}
// set color theme by current time
// written from what I've learnt so far
function setTheme(){
    let palette;
    const d = new Date();
    // if night time
    if (d.getHours() < 7 || 17 < d.getHours()){
        palette = {
            base: '#38444d',
            sub: '#1d2a35',
            accent: '#ffffff'
        };
    } else {
        palette = {
            base: '#ffffff',
            sub: '#a9a9a9',
            accent: '#000000'
        };
    }
    
    document.querySelector('body').style.backgroundColor = palette.base;
    document.getElementById('face').style.backgroundColor = palette.sub;
    document.getElementById('face').style.color = palette.accent;
    document.getElementById('hour').style.backgroundColor = palette.accent;
    document.getElementById('min').style.backgroundColor = palette.accent;
    document.getElementById('sec').style.backgroundColor = palette.accent;
    
}