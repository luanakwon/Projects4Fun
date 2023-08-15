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
    
    hour_hand.style.transform = `rotate(${d.getHours()%12*30-180}deg)`;
    min_hand.style.transform = `rotate(${d.getMinutes()*6-180}deg)`;
    sec_hand.style.transform = `rotate(${d.getSeconds()*6-180}deg)`;
}