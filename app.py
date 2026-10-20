import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Stickman vs Zombie", layout="centered")

st.title("🥷 Người Que Đại Chiến Zombie 2D")
st.write("Dùng phím **A / D** (hoặc phím mũi tên) để di chuyển. Nhấn phím **Space** (Dấu cách) hoặc phím **J** để vung kiếm chém!")

game_source = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            background-color: #1e1e1e;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        canvas {
            border: 4px solid #fff;
            background: linear-gradient(to bottom, #2c3e50, #0f2027);
            box-shadow: 0 10px 30px rgba(0,0,0,0.7);
        }
    </style>
</head>
<body>

<canvas id="gameCanvas" width="850" height="480"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const keys = { a: false, d: false, ArrowLeft: false, ArrowRight: false };

window.addEventListener("keydown", (e) => {
    if (e.code === "KeyA" || e.code === "ArrowLeft") keys.a = true;
    if (e.code === "KeyD" || e.code === "ArrowRight") keys.d = true;
    if (e.code === "Space" || e.code === "KeyJ") player.attack();
});

window.addEventListener("keyup", (e) => {
    if (e.code === "KeyA" || e.code === "ArrowLeft") keys.a = false;
    if (e.code === "KeyD" || e.code === "ArrowRight") keys.d = false;
});

class BloodParticle {
    constructor(x, y, facing) {
        this.x = x;
        this.y = y;
        this.vx = facing * (Math.random() * 4 + 3) + (Math.random() * 2 - 1);
        this.vy = Math.random() * -5 - 2; 
        this.radius = Math.random() * 3 + 2;
        this.life = 35;
    }
    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.vy += 0.25;
        this.life--;
    }
    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(220, 20, 60, 0.9)";
        ctx.fill();
    }
}

const player = {
    x: 400,
    y: 330,
    width: 40,
    height: 90,
    speed: 5,
    health: 100,
    maxHealth: 100,
    facing: 1,
    isAttacking: false,
    attackProgress: 0,
    walkCycle: 0,

    attack() {
        if (!this.isAttacking) {
            this.isAttacking = true;
            this.attackProgress = 0;
        }
    },

    update() {
        let isMoving = false;
        if (keys.a) { this.x -= this.speed; this.facing = -1; isMoving = true; }
        if (keys.d) { this.x += this.speed; this.facing = 1; isMoving = true; }

        if (this.x < 10) this.x = 10;
        if (this.x > canvas.width - this.width - 10) this.x = canvas.width - this.width - 10;

        if (isMoving) {
            this.walkCycle += 0.25;
        } else {
            this.walkCycle = 0;
        }

        if (this.isAttacking) {
            this.attackProgress += 0.15;
            if (this.attackProgress > 1) {
                this.isAttacking = false;
            }
        }
    },

    draw() {
        let headX = this.x + this.width / 2;
        let headY = this.y + 15;
        let headRadius = 12;

        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 4;
        ctx.lineCap = "round";

        ctx.beginPath();
        ctx.arc(headX, headY, headRadius, 0, Math.PI * 2);
        ctx.stroke();

        let neckY = headY + headRadius;
        let pelvisY = neckY + 35;
        ctx.beginPath();
        ctx.moveTo(headX, neckY);
        ctx.lineTo(headX, pelvisY);
        ctx.stroke();

        let legSwing = Math.sin(this.walkCycle) * 15;
        ctx.beginPath();
        ctx.moveTo(headX, pelvisY);
        ctx.lineTo(headX - 12 + legSwing, pelvisY + 28);
        ctx.moveTo(headX, pelvisY);
        ctx.lineTo(headX + 12 - legSwing, pelvisY + 28);
        ctx.stroke();

        let shoulderY = neckY + 10;
        if (this.isAttacking) {
            let startAngle = -Math.PI / 3 * this.facing;
            let endAngle = Math.PI / 1.2 * this.facing;
            let currentAngle = startAngle + (endAngle - startAngle) * this.attackProgress;

            let handX = headX + Math.cos(currentAngle) * 20;
            let handY = shoulderY + Math.sin(currentAngle) * 15;

            ctx.beginPath();
            ctx.moveTo(headX, shoulderY);
            ctx.lineTo(handX, handY);
            ctx.stroke();

            let swordLength = 45;
            let swordTipX = handX + Math.cos(currentAngle) * swordLength;
            let swordTipY = handY + Math.sin(currentAngle) * swordLength;

            ctx.strokeStyle = "#00f0ff";
            ctx.lineWidth = 5;
            ctx.beginPath();
            ctx.moveTo(handX, handY);
            ctx.lineTo(swordTipX, swordTipY);
            ctx.stroke();
            
            ctx.strokeStyle = "#ffffff";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(handX, handY);
            ctx.lineTo(swordTipX, swordTipY);
            ctx.stroke();
        } else {
            let handX = headX + this.facing * 15;
            let handY = shoulderY + 15;

            ctx.beginPath();
            ctx.moveTo(headX, shoulderY);
            ctx.lineTo(handX, handY);
            ctx.stroke();

            ctx.strokeStyle = "#00f0ff";
            ctx.lineWidth = 5;
            ctx.beginPath();
            ctx.moveTo(handX, handY);
            ctx.lineTo(handX + this.facing * 12, handY - 30);
            ctx.stroke();
        }

        ctx.fillStyle = "#444";
        ctx.fillRect(20, 20, 180, 18);
        ctx.fillStyle = "#2ecc71";
        ctx.fillRect(20, 20, Math.max(0, 180 * (this.health / this.maxHealth)), 18);
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 2;
        ctx.strokeRect(20, 20, 180, 18);
    }
};

class Zombie {
    constructor(x) {
        this.x = x;
        this.y = 330;
        this.width = 40;
        this.height = 90;
        this.speed = Math.random() * 1.2 + 1.0;
        this.health = 50;
        this.maxHealth = 50;
        this.walkCycle = Math.random() * 100;
        this.facing = 1;
    }

    update() {
        if (this.x < player.x) {
            this.x += this.speed;
            this.facing = 1;
        } else {
            this.x -= this.speed;
            this.facing = -1;
        }
        this.walkCycle += 0.08;
    }

    draw() {
        let headX = this.x + this.width / 2;
        let headY = this.y + 15;
        let headRadius = 12;

        ctx.fillStyle = "#729d39";
        ctx.beginPath();
        ctx.arc(headX, headY, headRadius, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = "#ff0000";
        ctx.beginPath();
        ctx.arc(headX + this.facing * 4, headY - 2, 2.5, 0, Math.PI * 2);
        ctx.fill();

        let neckY = headY + headRadius;
        let pelvisY = neckY + 35;
        ctx.strokeStyle = "#3e4a36";
        ctx.lineWidth = 7;
        ctx.beginPath();
        ctx.moveTo(headX, neckY);
        ctx.lineTo(headX, pelvisY);
        ctx.stroke();

        let legSwing = Math.sin(this.walkCycle) * 10;
        ctx.strokeStyle = "#729d39";
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(headX, pelvisY);
        ctx.lineTo(headX - 10 + legSwing, pelvisY + 28);
        ctx.moveTo(headX, pelvisY);
        ctx.lineTo(headX + 10 - legSwing, pelvisY + 28);
        ctx.stroke();

        let shoulderY = neckY + 10;
        ctx.beginPath();
        ctx.moveTo(headX, shoulderY);
        ctx.lineTo(headX + this.facing * 24, shoulderY + 4);
        ctx.stroke();

        let barW = 40;
        let barH = 6;
        let barX = headX - barW / 2;
        let barY = headY - 25;

        ctx.fillStyle = "#000000";
        ctx.fillRect(barX, barY, barW, barH);
        
        let currentBarW = barW * (this.health / this.maxHealth);
        ctx.fillStyle = "#e74c3c";
        ctx.fillRect(barX, barY, Math.max(0, currentBarW), barH);
        
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 1;
        ctx.strokeRect(barX, barY, barW, barH);
    }
}

const zombies = [];
const particles = [];
let score = 0;
let spawnTimer = 0;
let isGameOver = false;

function checkSwordHit(p, z) {
    if (p.isAttacking && p.attackProgress > 0.2 && p.attackProgress < 0.7) {
        let hitBoxX = p.facing === 1 ? p.x + p.width : p.x - 75;
        let hitBoxWidth = 75;
        
        return (hitBoxX < z.x + z.width && hitBoxX + hitBoxWidth > z.x &&
                p.y < z.y + z.height && p.y + p.height > z.y);
    }
    return false;
}

function gameLoop() {
    if (isGameOver) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = "#e74c3c";
        ctx.font = "bold 38px Arial";
        ctx.fillText("BẠN ĐÃ BỊ ZOMBIE HẠ GỤC", canvas.width / 2 - 210, canvas.height / 2 - 20);
        
        ctx.fillStyle = "#ffffff";
        ctx.font = "20px Arial";
        ctx.fillText("Bấm phím F5 trên bàn phím để hồi sinh chơi lại!", canvas.width / 2 - 190, canvas.height / 2 + 30);
        return;
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#111a24";
    ctx.fillRect(0, 445, canvas.width, 35);
    ctx.strokeStyle = "#4b6584";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(0, 445);
    ctx.lineTo(canvas.width, 445);
    ctx.stroke();

    player.update();
    player.draw();

    spawnTimer++;
    if (spawnTimer > Math.max(35, 90 - score * 3)) {
        spawnTimer = 0;
        let spawnX = Math.random() < 0.5 ? -30 : canvas.width + 30;
        zombies.push(new Zombie(spawnX));
    }

    for (let i = particles.length - 1; i >= 0; i--) {
        particles[i].update();
        particles[i].draw();
        if (particles[i].life <= 0) {
            particles.splice(i, 1);
        }
    }

    for (let i = zombies.length - 1; i >= 0; i--) {
        let z = zombies[i];
        z.update();
        z.draw();

        if (checkSwordHit(player, z)) {
z.health -= 1.5;
if (Math.random() < 0.6) {
particles.push(new BloodParticle(z.x + z.width / 2, z.y + 30, player.facing));
}
if (z.health <= 0) {
for (let k = 0; k < 15; k++) {
particles.push(new BloodParticle(z.x + z.width / 2, z.y + 30, player.facing));
}
zombies.splice(i, 1);
score++;
continue;
}
}
if (player.x < z.x + z.width && player.x + player.width > z.x &&
player.y < z.y + z.height && player.y + player.height > z.y) {
player.health -= 0.3;
if (player.health <= 0) {
isGameOver = true;
}
}
}
ctx.fillStyle = "#f1c40f";
ctx.font = "bold 20px Arial";
ctx.fillText("Điểm Tiêu Diệt: " + score, 20, 65);
requestAnimationFrame(gameLoop);
}
gameLoop();
"""
components.html(game_source, height=510, scrolling=False)
