var a = 2;
const date = [];
const code = a;
const save = [];
const dateInput = document.getElementById("email").value;
const codeInput = document.getElementById('email').value;
const codeSubmit = document.querySelectorAll('.submit input');

function verify(ev) {
    if (code === codeInput) {
        alert('code match');
        console.log(code)
    } else {
        console.log('code mismatch');
    }
    if (codeInput === null) {
        console.log('Null');
    }
}