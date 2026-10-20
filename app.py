import streamlit as st
import random

st.set_page_config(page_title="Stickman vs Zombie", page_icon="🥷")
st.title("🥷 Stickman vs Zombie 🧟")

# Khởi tạo trạng thái game
if "player_hp" not in st.session_state:
    st.session_state.player_hp = 100
    st.session_state.zombie_hp = 100
    st.session_state.log = ["Trận chiến bắt đầu! Một Zombie xuất hiện!"]
    st.session_state.game_over = False

# Hiển thị thanh máu
col1, col2 = st.columns(2)
with col1:
    st.subheader("Người que (Bạn)")
    st.progress(st.session_state.player_hp / 100)
    st.write(f"❤️ HP: {st.session_state.player_hp}/100")
with col2:
    st.subheader("Zombie")
    st.progress(st.session_state.zombie_hp / 100)
    st.write(f"💚 HP: {st.session_state.zombie_hp}/100")

# Xử lý logic chiến đấu
if not st.session_state.game_over:
    col_atk, col_heal = st.columns(2)
    
    with col_atk:
        if st.button("⚔️ Tấn công Zombie", use_container_width=True):
            dmg_to_zombie = random.randint(15, 30)
            st.session_state.zombie_hp = max(0, st.session_state.zombie_hp - dmg_to_zombie)
            st.session_state.log.append(f"💥 Bạn chém Zombie mất {dmg_to_zombie} HP!")
            
            if st.session_state.zombie_hp > 0:
                dmg_to_player = random.randint(10, 25)
                st.session_state.player_hp = max(0, st.session_state.player_hp - dmg_to_player)
                st.session_state.log.append(f"🧟 Zombie cắn lại bạn mất {dmg_to_player} HP!")
            st.rerun()

    with col_heal:
        if st.button("🧪 Uống thuốc hồi máu", use_container_width=True):
            heal = random.randint(20, 40)
            st.session_state.player_hp = min(100, st.session_state.player_hp + heal)
            st.session_state.log.append(f"🧪 Bạn uống thuốc tăng {heal} HP!")
            
            dmg_to_player = random.randint(10, 25)
            st.session_state.player_hp = max(0, st.session_state.player_hp - dmg_to_player)
            st.session_state.log.append(f"🧟 Zombie tận dụng cơ hội cắn bạn mất {dmg_to_player} HP!")
            st.rerun()

# Kiểm tra kết quả
if st.session_state.zombie_hp <= 0:
    st.success("🎉 Bạn đã tiêu diệt được Zombie! Chiến thắng!")
    st.session_state.game_over = True
elif st.session_state.player_hp <= 0:
    st.error("💀 Bạn đã bị Zombie hạ gục! Game Over!")
    st.session_state.game_over = True

if st.session_state.game_over:
    if st.button("🔄 Chơi lại từ đầu"):
        del st.session_state.player_hp
        del st.session_state.zombie_hp
        del st.session_state.log
        del st.session_state.game_over
        st.rerun()

# Lịch sử trận đấu
st.write("---")
st.write("📝 **Nhật ký trận đấu:**")
for line in reversed(st.session_state.log):
    st.write(line)
