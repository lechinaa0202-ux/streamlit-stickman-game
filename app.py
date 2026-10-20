import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Stickman vs Zombie 2D", page_icon="🥷", layout="centered")
st.title("🥷 Stickman vs Zombie 2D 🧟")
st.write("Dùng các nút điều khiển ▲ ▼ ◀ ▶ để di chuyển người que và nút ⚔️ để vung kiếm chém zombie phun máu!")

game_src = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { text-align: center; font-family: Arial, sans-serif; background-color: #111; color: white; margin: 0; padding: 0; }
        canvas { background: #222; border: 3px solid #555; display: block; margin: 10px auto; max-width: 100%; touch-action: none; box-shadow: 0 0 10px rgba(0,0,0,0.5); }
        .controls { display: grid; grid-template-columns: repeat(3, 65px); grid-gap: 12px; justify-content: center; margin-top: 15px; }
        .btn { width: 65px; height: 65px; background: #444; color: white; border: none; border-radius: 12px; font-size: 22px; font-weight: bold; }
        .btn:active { background: #666; }
        .empty { visibility: hidden; }
        #score-board { font-size: 18px; margin: 5px; color: #ffeb3b; font-weight: bold; }
    </style>
</head>
<body>

    <div id="score-board">Điểm tiêu diệt: <span id="score">0</span></div>
    <canvas id="gameCanvas" width="400" height="300"></canvas>

    <div class="controls">
        <button class="btn empty"></button>
        <button class="btn" id="btn-up">▲</button>
        <button class="btn empty"></button>
        <button class="btn" id="btn-left">◀</button>
        <button class="btn" style="background:#d32f2f;" id="btn-atk">⚔️</button>
        <button class="btn" id="btn-right">▶</button>
        <button class="btn empty"></button>
        <button class="btn" id="btn-down">▼</button>
        <button class="btn empty"></button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        const player = { x: 80, y: 150, radius: 15, hp: 100, maxHp: 100, speed: 15, isAttacking: false };
        let zombies = [];
        let bloodParticles = [];
        let score = 0;
        let gameOver = false;

        function createZombie() {
            if (zombies.length  {
                    if (zombie.x > player.x) zombie.x -= zombie.speed;
                    else zombie.x += zombie.speed;
                    
                    if (zombie.y > player.y) zombie.y -= zombie.speed * 0.3;
                    else zombie.y += zombie.speed * 0.3;

                    let dist = Math.hypot(player.x - zombie.x, player.y - zombie.y);
                    if (dist < player.radius + zombie.radius) {
                        player.hp -= 0.4;
                        if (player.hp <= 0) { player.hp = 0; gameOver = true; }
                    }
                });

                bloodParticles.forEach((particle, idx) => {
                    particle.x += particle.vx;
                    particle.y += particle.vy;
                    particle.vy += 0.15;
                    particle.life--;
                    if (particle.life <= 0) bloodParticles.splice(idx, 1);
                });
            }

            bloodParticles.forEach(p => {
                ctx.fillStyle = `rgba(211, 47, 47, ${p.life / 20})`;
                ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2); ctx.fill();
            });

            drawPlayer(player.x, player.y, player.isAttacking);
            drawHealthBar(player, false);

            zombies.forEach(zombie => {
                drawZombie(zombie.x, zombie.y);
                drawHealthBar(zombie, true);
            });

            if (gameOver) {
                ctx.fillStyle = "rgba(0,0,0,0.85)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "#ff1744";
                ctx.font = "bold 24px Arial";
                ctx.fillText("BẠN ĐÃ BỊ HẠ GỤC!", canvas.width/2 - 105, canvas.height/2);
                ctx.font = "16px Arial";
                ctx.fillStyle = "#ffffff";
                ctx.fillText("Nhấn nút Kiếm ⚔️ dưới đây để hồi sinh chơi lại!", canvas.width/2 - 145, canvas.height/2 + 35);
            }
        }
        setInterval(runGameEngine, 1000 / 30);

        document.getElementById("btn-up").addEventListener("click", () => { if(player.y > 40 && !gameOver) player.y -= player.speed; });
        document.getElementById("btn-down").addEventListener("click", () => { if(player.y < canvas.height - 40 && !gameOver) player.y += player.speed; });
        document.getElementById("btn-left").addEventListener("click", () => { if(player.x > 30 && !gameOver) player.x -= player.speed; });
        document.getElementById("btn-right").addEventListener("click", () => { if(player.x < canvas.width - 30 && !gameOver) player.x += player.speed; });
        
        document.getElementById("btn-atk").addEventListener("click", () => {
            if (gameOver) {
                player.hp = 100; zombies = []; bloodParticles = []; score = 0;
                document.getElementById("score").innerText = score;
                gameOver = false; return;
            }
            
            player.isAttacking = true;
            setTimeout(() => { player.isAttacking = false; }, 120);

            zombies.forEach((zombie, index) => {
                let dist = Math.hypot(player.x - zombie.x, player.y - zombie.y);
                if (dist < player.radius + zombie.radius + 30) {
                    zombie.hp -= 25;
                    triggerBlood(zombie.x, zombie.y);

                    if (zombie.hp <= 0) {
                        zombies.splice(index, 1);
                        score += 1;
                        document.getElementById("score").innerText = score;
                    }
                }
            });
        });
    </script>
</body>
</html>
"""

components.html(game_src, height=460)
