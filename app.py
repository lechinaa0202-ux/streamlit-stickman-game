
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Stickman vs Zombie 2D", page_icon="🥷", layout="centered")
st.title("🥷 Stickman vs Zombie 2D 🧟")
st.write("Sử dụng các nút điều khiển bên dưới để di chuyển người que né tránh và tự động tấn công Zombie!")

# Toàn bộ mã nguồn xử lý đồ họa, di chuyển và thanh máu bằng HTML5 Canvas + JS
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { text-align: center; font-family: Arial, sans-serif; background-color: #111; color: white; margin: 0; padding: 0; }
        canvas { background: #222; border: 3px solid #555; display: block; margin: 10px auto; max-width: 100%; touch-action: none; }
        .controls { display: grid; grid-template-columns: repeat(3, 60px); grid-gap: 10px; justify-content: center; margin-top: 15px; }
        .btn { width: 60px; height: 60px; background: #444; color: white; border: none; border-radius: 10px; font-size: 20px; font-weight: bold; active-background: #666; }
        .btn:active { background: #666; }
        .empty { visibility: hidden; }
        #score-board { font-size: 18px; margin: 5px; color: #ffeb3b; }
    </style>
</head>
<body>

    <div id="score-board">Điểm tiêu diệt: <span id="score">0</span></div>
    <canvas id="gameCanvas" width="400" height="300"></canvas>

    <!-- Bảng điều khiển nút bấm dưới màn hình -->
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

        // Khởi tạo Player (Người que)
        const player = { x: 50, y: 150, size: 20, hp: 100, maxHp: 100, speed: 8, isAttacking: false };
        
        // Khởi tạo danh sách Zombie
        let zombies = [];
        let score = 0;
        let gameOver = False;

        function spawnZombie() {
            if(zombies.length  {
                // Zombie đuổi theo người que
                if (zombie.x > player.x) zombie.x -= zombie.speed;
                else zombie.x += zombie.speed;
                
                if (zombie.y > player.y) zombie.y -= zombie.speed;
                else zombie.y += zombie.speed;

                // Kiểm tra va chạm gây sát thương cho người que
                let dist = Math.hypot(player.x - zombie.x, player.y - zombie.y);
                if (dist < player.size + zombie.size) {
                    player.hp -= 0.5; // Mất máu dần khi chạm vào zombie
                    if (player.hp <= 0) {
                        player.hp = 0;
                        gameOver = true;
                    }
                }
            });

            // Tắt trạng thái tấn công sau 1 khoảng thời gian ngắn
            if(player.isAttacking) {
                setTimeout(() => { player.isAttacking = false; }, 150);
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ Người que và Zombie
            drawEntity(player, "#29b6f6", false);
            zombies.forEach(zombie => drawEntity(zombie, "#4caf50", true));

            if (gameOver) {
                ctx.fillStyle = "rgba(0,0,0,0.8)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "red";
                ctx.font = "24px Arial";
                ctx.fillText("BẠN ĐÃ BỊ HẠ GỤC!", canvas.width/2 - 100, canvas.height/2);
                ctx.font = "16px Arial";
                ctx.fillStyle = "white";
                ctx.fillText("Nhấn nút Kiếm ⚔️ để hồi sinh", canvas.width/2 - 95, canvas.height/2 + 30);
            }
        }

        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        // Xử lý sự kiện từ Bảng điều khiển điều hướng dưới màn hình
        document.getElementById("btn-up").addEventListener("click", () => { if(player.y > 20) player.y -= player.speed; });
        document.getElementById("btn-down").addEventListener("click", () => { if(player.y < canvas.height - 20) player.y += player.speed; });
        document.getElementById("btn-left").addEventListener("click", () => { if(player.x > 20) player.x -= player.speed; });
        document.getElementById("btn-right").addEventListener("click", () => { if(player.x < canvas.width - 20) player.x += player.speed; });
        
        // Nút bấm Tấn công / Hồi sinh khi Game Over
        document.getElementById("btn-atk").addEventListener("click", () => {
            if (gameOver) { // Reset game nếu chết
                player.hp = 100;
                zombies = [];
                score = 0;
                document.getElementById("score").innerText = score;
                gameOver = false;
                return;
            }
            
            player.isAttacking = true;
            // Kiểm tra xem có chém trúng zombie nào xung quanh vòng quét không
            zombies.forEach((zombie, index) => {
                let dist = Math.hypot(player.x - zombie.x, player.y - zombie.y);
                if (dist < player.size + zombie.size + 20) {
                    zombie.hp -= 20;
                    if(zombie.hp <= 0) {
                        zombies.splice(index, 1);
                        score += 1;
                        document.getElementById("score").innerText = score;
                    }
                }
            });
        });

        // Khởi chạy vòng lặp game
        gameLoop();
    </script>
</body>
</html>
"""

# Nhúng giao diện HTML5 game vào Streamlit 
components.html(game_html, height=450)
