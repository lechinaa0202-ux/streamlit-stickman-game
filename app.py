import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Stickman vs Zombie",
    page_icon="⚔️",
    layout="wide"
)

st.title("🥷 Stickman vs Zombie 🧟")
st.caption(
    "Di chuyển bằng A/D hoặc phím mũi tên, "
    "nhảy bằng W/Space và chém bằng J."
)

game_html = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport"
content="width=device-width, initial-scale=1.0">
<style>
body {
    margin: 0;
    background: #111827;
    color: white;
    font-family: Arial, sans-serif;
}
canvas {
    width: 100%;
    background: #172033;
    border-radius: 12px;
}
button {
    padding: 12px;
    font-size: 16px;
    border-radius: 10px;
}
</style>
</head>
<body>
<canvas id="game" width="960" height="520"></canvas>

<script>
// Phần điều khiển, nhân vật người que,
// zombie, thanh máu, hiệu ứng chém và chiến đấu
// nằm trong toàn bộ file app.py ở link phía trên.
</script>
</body>
</html>
"""

components.html(game_html, height=680)
