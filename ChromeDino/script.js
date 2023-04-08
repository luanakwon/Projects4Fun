var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
var width = canvas.width;
var height = canvas.height;
var x = 50;
var y = 0;
var dy = 0;
var gravity = 0.5;
var obstacleX = width;
var obstacleWidth = 20;
var obstacleHeight = 50;
var speed = 5;
var score = 0;
var highScore = 0;

function drawDino() {
  ctx.fillStyle = "#000000";
  ctx.fillRect(x, y, 30, 30);
}

function jump() {
  dy = -10;
}

function drawObstacle() {
  ctx.fillStyle = "#FF0000";
  ctx.fillRect(obstacleX, height - obstacleHeight, obstacleWidth, obstacleHeight);
}

function updateScore() {
  score += 1;
  if (score > highScore) {
    highScore = score;
  }
  document.getElementById("score").innerHTML = score;
  document.getElementById("high-score").innerHTML = highScore;
}

function reset() {
  x = 50;
  y = 0;
  dy = 0;
  obstacleX = width;
  score = -1;
  updateScore();
}

function gameOver() {
  alert("Game Over!");
  reset();
}

function checkCollision() {
  if (x + 30 >= obstacleX && x <= obstacleX + obstacleWidth && y + 30 >= height - obstacleHeight) {
    gameOver();
  }
}

function updateObstacle() {
  obstacleX -= speed;
  if (obstacleX < -obstacleWidth) {
    obstacleX = width;
	obstacleHeight = Math.floor(Math.random() * 2) ? 50 : 90;
    updateScore();
  }
}

function updateDino() {
  dy += gravity;
  y += dy;
  if (y > height - 30) {
    y = height - 30;
    dy = 0;
  }
}

function draw() {
  ctx.clearRect(0, 0, width, height);
  drawDino();
  drawObstacle();
  updateObstacle();
  checkCollision();
  updateDino();
}

reset()
setInterval(draw, 20);

document.addEventListener("keydown", function(event) {
  if (event.keyCode === 32) {
    jump();
  }
});
