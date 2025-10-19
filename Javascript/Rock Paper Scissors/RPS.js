function game(){
  randNum = Math.floor(Math.random()*3)
  console.log(randNum)
  if(hand.RPS[0].checked == true){
    you = "rock"
  }
  else if(hand.RPS[1].checked == true){
    you = "paper"
  }
  else if(hand.RPS[2].checked == true){
    you = "scissors"
  }
  console.log(you)
  if(randNum == 0){
    randValue = "rock"
  }
  else if(randNum == 1){
    randValue = "paper"
  }
  else if(randNum == 2){
    randValue = "scissors"
  }
  console.log(randValue)
  if(you == randValue){
    returnResult= "You and the computer both chose " + you + ", therefore it is a tie";
    document.getElementById("result").innerHTML = returnResult
  }
  else if(you == "rock" && randValue == "paper"){
    returnResult = "You chose " + you + ", the computer chose " + randValue + ", so you lose";
    document.getElementById("result").innerHTML = returnResult
  }
  else if(you == "rock" && randValue == "scissors"){
    returnResult = "You chose " + you + ", the computer chose " + randValue + ", so you win";
    document.getElementById("result").innerHTML = returnResult
  }
  else if(you == "scissors" && randValue == "rock"){
    returnResult = "You chose " + you + ", the computer chose " + randValue + ", so you lose";
    document.getElementById("result").innerHTML = returnResult
  }
  else if(you == "scissors" && randValue == "paper"){
    returnResult = "You chose " + you + ", the computer chose " + randValue + ", so you win";
    document.getElementById("result").innerHTML = returnResult
  }
  else if(you == "paper" && randValue == "rock"){
    returnResult = "You chose " + you + ", the computer chose " + randValue + ", so you win";
    document.getElementById("result").innerHTML = returnResult
  }
  else if(you == "paper" && randValue == "scissors"){
    returnResult= "You chose " + you + ", the computer chose " + randValue + ", so you lose";
    document.getElementById("result").innerHTML = returnResult
  }
}