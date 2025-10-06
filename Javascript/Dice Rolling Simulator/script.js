// input element displaying button is referenced in the 'button' variable.
const button = document.querySelector('#button');
// video element displaying animation is referenced in the 'animation' variable.
const animation = document.getElementById('rolling-dice');
// span element displaying the output is referenced in the 'output' variable.
const output = document.getElementById('output-text');

// function 'getRandomIntegerInclusive' generates a number between 1 to 6.
function getRandomIntegerInclusive(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// When 'Roll' button is clicked then below action is carried out.
button.addEventListener('click', function() {
// video containing rolling-dice animation is hidden.
    animation.style.visibility = 'hidden';
    // adding a slight delay for effective visual effect.
    setTimeout(() => {
        // we will generate a random number by calling 'getRandomIntegerInclusive' function.    
        let randomInteger = getRandomIntegerInclusive(1, 6);
        console.log(randomInteger);
        // Now, displaying the output number in the span element 
        output.textContent = randomInteger;
    
        // Now, displaying the dice rolling animation again.
        if(output.textContent != "") {
            animation.style.visibility = 'visible';
        }
    }, 500);

});