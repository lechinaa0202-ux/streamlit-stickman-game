import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Stickman vs Zombie 2D", page_icon="🥷", layout="centered")
st.title("🥷 Stickman vs Zombie 2D 🧟")
st.write("Di chuyển người que né tránh zombie và nhấn nút Kiếm để chém phun máu!")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { text-align: center; font-family: Arial, sans-serif; background-color: #111; color: white; margin: 0; padding: 0; overflow: hidden; }
        #game-arena { background: #222; border: 3px solid #555; width: 360px; height: 260px; margin: 10px auto; position: relative; overflow: hidden; }
        .controls { display: grid; grid-template-columns: repeat(3, 65px); grid-gap: 12px; justify-content: center; margin-top: 15px; }
        .btn { width: 65px; height: 65px; background: #444; color: white; border: none; border-radius: 12px; font-size: 22px; font-weight: bold; }
        .btn:active { background: #666; }
        .empty { visibility: hidden; }
        #score-board { font-size: 18px; margin: 5px; color: #ffeb3b; font-weight: bold; }
        
        /* Thực thể Game */
        .entity { position: absolute; font-size: 28px; width: 30px; height: 35px; transition: all 0.1s linear; }
        .hp-bar-bg { position: absolute; width: 30px; height: 4px; background: red; top: -8px; left: 0; }
        .hp-bar-fill { height: 100%; background: #00b0ff; width: 100%; }
        
        /* Hiệu ứng chém và máu */
        .sword-effect { position: absolute; font-size: 20px; display: none; transform: scaleX(-1); }
        .blood { position: absolute; width: 5px; height: 5px; background: #d32f2f; border-radius: 50%; animation: splash 0.3s ease-out forwards; }
        @keyframes splash {
            0% { transform: translate(0, 0) scale(1); opacity: 1; }
            100% { transform: translate(var(--bx), var(--by)) scale(0.5); opacity: 0; }
        }
        #game-over-screen { position: absolute; width: 100%; height: 100%; background: rgba(0,0,0,0.85); display: none; flex-direction: column; justify-content: center; align-items: center; z-index: 10; }
    </style>
</head>
<body>

    <div id="score-board">Điểm tiêu diệt: <span id="score">0</span></div>
    
    <div id="game-arena">
        <div id="game-over-screen">
            <h2 style="color: #ff1744; margin: 0;">BẠN ĐÃ BỊ HẠ GỤC!</h2>
            <p style="font-size: 14px; margin: 10px 0 0 0;">Nhấn nút Kiếm ⚔️ để hồi sinh</p>
        </div>
        
        <!-- Người que (Player) -->
        
            <div class="hp-bar-bg"><div id="player-hp" class="hp-bar-fill"></div></div>
            🥷<div id="sword" class="sword-effect" style="left: 20px; top: 0px;">🗡️</div>
        </div>

        <!-- Các con Zombie -->
        
            <div class="hp-bar-bg"><div id="zombie1-hp" class="hp-bar-fill" style="background:#00e676;"></div></div>🧟
        </div>
        
            <div class="hp-bar-bg"><div id="zombie2-hp" class="hp-bar-fill" style="background:#00e676;"></div></div>🧟
        </div>
    </div>

    <!-- Nút điều khiển -->
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
        const pElem = document.getElementById("player");
        const z1Elem = document.getElementById("zombie1");
        const z2Elem = document.getElementById("zombie2");
        const sword = document.getElementById("sword");
        const arena = document.getElementById("game-arena");
        const goScreen = document.getElementById("game-over-screen");

        let p = { x: 50, y: 110, hp: 100 };
        let z1 = { x: 300, y: 50, hp: 60, active: true, speed: 1.5 };
        let z2 = { x: 300, y: 160, hp: 60, active: true, speed: 1.2 };
        let score = 0;
        let gameOver = false;

        // Cơ chế Zombie tự động dí đuổi theo người que mỗi 0.15 giây công bằng ổn định
        function zombieAI() {
            if (gameOver) return;

            [ {e: z1Elem, d: z1}, {e: z2Elem, d: z2} ].forEach(z => {
                if (!z.d.active) return;
                
                if (z.d.x > p.x) z.d.x -= z.d.speed;
                else z.d.x += z.d.speed;
                
                if (z.d.y > p.y) z.d.y -= z.d.speed;
                else z.d.y += z.d.speed;

                z.e.style.left = z.d.x + "px";
                z.e.style.top = z.d.y + "px";

                // Kiểm tra va chạm làm người que mất máu
                let dist = Math.hypot(p.x - z.d.x, p.y - z.d.y);
                if (dist < 25) {
                    p.hp -= 2;
                    if (p.hp <= 0) { p.hp = 0; gameOver = true; goScreen.style.display = "flex"; }
                    document.getElementById("player-hp").style.width = p.hp + "%";
                }
            });
        }
        setInterval(zombieAI, 150);

        // Hiệu ứng phun máu đỏ tung tóe
        function spawnBlood(x, y) {
            for (let i = 0; i < 8; i++) {
                let b = document.createElement("div");
                b.className = "blood";
                b.style.left = (x + 10) + "px";
                b.style.top = (y + 15) + "px";
                b.style.setProperty("--bx", ((Math.random() - 0.2) * 40) + "px");
                b.style.setProperty("--by", ((Math.random() - 0.5) * 40) + "px");
                arena.appendChild(b);
                setTimeout(() => b.remove(), 300);
            }
        }

        // Điều khiển Người que di chuyển
        document.getElementById("btn-up").addEventListener("click", () => { if(p.y > 10 && !gameOver) { p.y -= 20; pElem.style.top = p.y + "px"; } });
        document.getElementById("btn-down").addEventListener("click", () => { if(p.y < 210 && !gameOver) { p.y += 20; pElem.style.top = p.y + "px"; } });
        document.getElementById("btn-left").addEventListener("click", () => { if(p.x > 10 && !gameOver) { p.x -= 20; pElem.style.left = p.x + "px"; } });
        document.getElementById("btn-right").addEventListener("click", () => { if(p.x < 320 && !gameOver) { p.x += 20; pElem.style.left = p.x + "px"; } });

        // Tấn công / Hồi sinh khi nhấn nút Kiếm
        document.getElementById("btn-atk").addEventListener("click", () => {
            if (gameOver) {
                p = { x: 50, y: 110, hp: 100 };
                z1 = { x: 300, y: 50, hp: 60, active: true, speed: 1.5 };
                z2 = { x: 300, y: 160, hp: 60, active: true, speed: 1.2 };
                score = 0; document.getElementById("score").innerText = score;
                document.getElementById("player-hp").style.width = "100%";
                document.getElementById("zombie1-hp").style.width = "100%";
                document.getElementById("zombie2-hp").style.width = "100%";
                z1Elem.style.display = "block"; z2Elem.style.display = "block";
                pElem.style.left = "50px"; pElem.style.top = "110px";
                goScreen.style.display = "none"; gameOver = false; return;
            }

            // Hiện cây kiếm chém ra
            sword.style.display = "block";
            setTimeout(() => sword.style.display = "none", 150);

            // Kiểm tra khoảng cách chém trúng Zombie
            [ {d: z1, e: z1Elem, h: "zombie1-hp"}, {d: z2, e: z2Elem, h: "zombie2-hp"} ].forEach(z => {
                if (!z.d.active) return;
                let dist = Math.hypot(p.x - z.d.x, p.y - z.d.y);
                if (dist < 45) { // Tầm chém kiếm
                    z.d.hp -= 20;
                    spawnBlood(z.d.x, z.d.y);
                    document.getElementById(z.h).style.width = (z.d.hp / 60 * 100) + "%";
                    
                    if (z.d.hp <= 0) {
                        z.d.active = false; z.e.style.display = "none";
                        score += 1; document.getElementById("score").innerText = score;
                        
                        // Tự hồi sinh zombie mới ở bên phải sau khi chết
                        setTimeout(() => {
                            z.d.hp = 60; z.d.x = 330; z.d.y = Math.random() * 200 + 20;
                            z.d.active = true; z.e.style.display = "block";
                            document.getElementById(z.h).style.width = "100%";
                        }, 1500);
                    }
                }
            });
        });
    </script>
</body>
</html>
"""

components.html(game_html, height=450)
