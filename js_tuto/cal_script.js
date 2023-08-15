function press(arg) {
    let display = document.getElementById('display');
    let text_in = display.innerHTML.split(' ');
    if (text_in.length == 1) {
        console.log('only num')
        console.log(text_in[0])
        if (typeof arg == 'number'){
            display.innerHTML = arg;
        }
        else {
            display.innerHTML = display.innerHTML + ' ' + arg;
        }
    }
    else {
        if (typeof arg == 'number'){
            switch (text_in[1]) {
                case '+':
                    console.log(' add');
                    display.innerHTML = Number(text_in[0]) + arg;
                    break;
                case '-':
                    console.log(' sub');
                    display.innerHTML = Number(text_in[0]) - arg;
                    break;
                case '*':
                    console.log(' mult');
                    display.innerHTML = Number(text_in[0]) * arg;
                    break;
                case '/':
                    console.log(' div');
                    display.innerHTML = Number(text_in[0]) / arg;
                    break;
            }
        }
        else {
            display.innerHTML = text_in[0] + ' ' + arg;
        }
    }
}