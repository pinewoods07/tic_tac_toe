import streamlit as st
import json
import os
import random
import string
import time
from pathlib import Path

# ─────────────────────────────────────────
#  페이지 설정
# ─────────────────────────────────────────
st.set_page_config(
    page_title="틱택토 대결 ⭕❌",
    page_icon="⭕",
    layout="centered",
)

# ─────────────────────────────────────────
#  방 저장 경로 (Streamlit Cloud /tmp)
# ─────────────────────────────────────────
ROOMS_DIR = Path("/tmp/tictactoe_rooms")
ROOMS_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: #0f0f1a;
    color: #e8e8f0;
}
.stApp {
    background: radial-gradient(ellipse at 30% 20%, rgba(90,60,180,0.12) 0%, transparent 60%),
                radial-gradient(ellipse at 70% 80%, rgba(30,100,200,0.10) 0%, transparent 60%),
                #0f0f1a;
}

/* 타이틀 */
.main-title {
    font-family: 'Black Han Sans', sans-serif;
    font-size: 2.8rem;
    text-align: center;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 2px;
    margin-bottom: 4px;
}
.sub-title {
    text-align: center;
    color: #555570;
    font-size: 0.88rem;
    margin-bottom: 28px;
    letter-spacing: 1px;
}

/* 카드 */
.card {
    background: linear-gradient(135deg, #16162a 0%, #1e1e35 100%);
    border: 1px solid #2a2a45;
    border-radius: 16px;
    padding: 28px 32px;
    margin: 12px 0;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}

/* 방 코드 표시 */
.room-code-display {
    font-family: 'Black Han Sans', sans-serif;
    font-size: 3.5rem;
    text-align: center;
    letter-spacing: 12px;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 10px 0;
}
.room-code-label {
    text-align: center;
    color: #555570;
    font-size: 0.8rem;
    letter-spacing: 2px;
    margin-bottom: 6px;
}

/* 상태 뱃지 */
.badge {
    display: inline-block;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.8rem;
    font-weight: 700;
}
.badge-waiting { background: rgba(251,191,36,0.15); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.badge-playing { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.badge-x { background: rgba(167,139,250,0.15); color: #a78bfa; border: 1px solid rgba(167,139,250,0.3); }
.badge-o { background: rgba(96,165,250,0.15); color: #60a5fa; border: 1px solid rgba(96,165,250,0.3); }

/* 턴 표시 */
.turn-info {
    text-align: center;
    font-size: 1.1rem;
    font-weight: 700;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 16px;
}
.your-turn { background: rgba(52,211,153,0.12); color: #34d399; border: 1px solid rgba(52,211,153,0.25); }
.their-turn { background: rgba(100,100,120,0.12); color: #666680; border: 1px solid rgba(100,100,120,0.2); }

/* 틱택토 보드 */
.board-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    max-width: 320px;
    margin: 0 auto;
}
.cell {
    aspect-ratio: 1;
    background: #1a1a30;
    border: 2px solid #2a2a45;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.8rem;
    cursor: pointer;
    transition: all 0.15s ease;
}
.cell:hover { border-color: #4a4a70; background: #20203a; }
.cell.x-cell { color: #a78bfa; border-color: rgba(167,139,250,0.4); }
.cell.o-cell { color: #60a5fa; border-color: rgba(96,165,250,0.4); }
.cell.win-cell { background: rgba(52,211,153,0.1); border-color: #34d399 !important; }

/* 결과 */
.result-banner {
    text-align: center;
    font-family: 'Black Han Sans', sans-serif;
    font-size: 1.8rem;
    padding: 20px;
    border-radius: 14px;
    margin: 16px 0;
    letter-spacing: 2px;
}
.win-banner { background: rgba(52,211,153,0.12); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.lose-banner { background: rgba(239,68,68,0.1); color: #f87171; border: 1px solid rgba(239,68,68,0.25); }
.draw-banner { background: rgba(251,191,36,0.1); color: #fbbf24; border: 1px solid rgba(251,191,36,0.25); }

/* 버튼 */
div.stButton > button {
    background: linear-gradient(135deg, #4c1d95, #1e40af) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 12px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(76,29,149,0.3) !important;
}
div.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(76,29,149,0.4) !important;
}

/* 인풋 */
div.stTextInput > div > div > input {
    background: #1a1a2e !important;
    border: 1px solid #2a2a45 !important;
    color: #e8e8f0 !important;
    border-radius: 10px !important;
    font-family: 'Black Han Sans', sans-serif !important;
    font-size: 1.4rem !important;
    letter-spacing: 6px !important;
    text-align: center !important;
}
div.stTextInput > div > div > input:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 2px rgba(167,139,250,0.2) !important;
}

hr { border-color: #1e1e35 !important; }
.small-info { color: #44445a; font-size: 0.78rem; text-align: center; margin-top: 8px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  헬퍼 함수
# ─────────────────────────────────────────
def get_room_path(code: str) -> Path:
    return ROOMS_DIR / f"{code}.json"

def create_room(code: str) -> dict:
    state = {
        "board": [""] * 9,
        "current_turn": "X",
        "players": {"X": True, "O": False},
        "winner": None,
        "draw": False,
        "win_line": [],
        "created_at": time.time(),
        "rematch_request": {"X": False, "O": False},
    }
    save_room(code, state)
    return state

def load_room(code: str) -> dict | None:
    path = get_room_path(code)
    if path.exists():
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def save_room(code: str, state: dict):
    path = get_room_path(code)
    with open(path, "w") as f:
        json.dump(state, f)

def generate_code() -> str:
    while True:
        code = ''.join(random.choices(string.digits, k=4))
        if not get_room_path(code).exists():
            return code

def check_winner(board: list) -> tuple[str | None, list]:
    lines = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6],
    ]
    for line in lines:
        a, b, c = line
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], line
    return None, []

def is_draw(board: list) -> bool:
    return all(cell != "" for cell in board)

def cleanup_old_rooms():
    """1시간 이상 된 방 정리"""
    now = time.time()
    for p in ROOMS_DIR.glob("*.json"):
        try:
            with open(p) as f:
                s = json.load(f)
            if now - s.get("created_at", now) > 3600:
                p.unlink()
        except Exception:
            pass

# ─────────────────────────────────────────
#  세션 상태 초기화
# ─────────────────────────────────────────
if "room_code" not in st.session_state:
    st.session_state.room_code = None
if "my_mark" not in st.session_state:
    st.session_state.my_mark = None  # "X" or "O"
if "last_board" not in st.session_state:
    st.session_state.last_board = None

# ─────────────────────────────────────────
#  헤더
# ─────────────────────────────────────────
st.markdown('<div class="main-title">⭕ 틱택토 ❌</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">— 친구와 1대1 실시간 대결 —</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────
#  로비 화면
# ─────────────────────────────────────────
if st.session_state.room_code is None:
    cleanup_old_rooms()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🎮 새 방 만들기")
    st.markdown("<div style='color:#666680; font-size:0.88rem; margin-bottom:12px;'>방을 만들고 친구에게 코드를 알려주세요!</div>", unsafe_allow_html=True)
    if st.button("✨  방 만들기 (내가 ⭕)", use_container_width=True):
        code = generate_code()
        create_room(code)
        st.session_state.room_code = code
        st.session_state.my_mark = "X"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='text-align:center; color:#333350; margin:8px 0; font-size:0.9rem;'>— 또는 —</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🔑 방 참가하기")
    st.markdown("<div style='color:#666680; font-size:0.88rem; margin-bottom:12px;'>친구에게 받은 4자리 코드를 입력하세요!</div>", unsafe_allow_html=True)
    code_input = st.text_input("", placeholder="0000", max_chars=4, label_visibility="collapsed")
    if st.button("🚪  입장하기 (내가 ❌)", use_container_width=True):
        if len(code_input) == 4:
            room = load_room(code_input)
            if room is None:
                st.error("❌ 존재하지 않는 방 코드예요!")
            elif room["players"]["O"]:
                st.error("❌ 이미 두 명이 있는 방이에요!")
            else:
                room["players"]["O"] = True
                save_room(code_input, room)
                st.session_state.room_code = code_input
                st.session_state.my_mark = "O"
                st.rerun()
        else:
            st.warning("4자리 숫자를 입력해 주세요!")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='small-info'>⏰ 방은 1시간 후 자동으로 삭제됩니다</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  게임 화면
# ─────────────────────────────────────────
else:
    code = st.session_state.room_code
    my_mark = st.session_state.my_mark
    opponent_mark = "O" if my_mark == "X" else "X"
    my_emoji = "⭕" if my_mark == "X" else "❌"
    opp_emoji = "❌" if my_mark == "X" else "⭕"

    room = load_room(code)

    if room is None:
        st.error("방 정보를 불러올 수 없어요. 다시 시작해 주세요.")
        if st.button("🏠 처음으로"):
            st.session_state.room_code = None
            st.session_state.my_mark = None
            st.rerun()
        st.stop()

    both_joined = room["players"]["X"] and room["players"]["O"]

    # ── 방 코드 표시 ──
    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.markdown(f"""
        <div style="text-align:center; padding:12px; background:#16162a; border:1px solid #2a2a45; border-radius:12px;">
            <div class="room-code-label">ROOM CODE</div>
            <div class="room-code-display">{code}</div>
            <div class="small-info">친구에게 이 코드를 알려주세요</div>
        </div>
        """, unsafe_allow_html=True)
    with col_r:
        st.markdown(f"""
        <div style="text-align:center; padding:12px; background:#16162a; border:1px solid #2a2a45; border-radius:12px;">
            <div class="room-code-label">내 마크</div>
            <div style="font-size:2.8rem; margin:6px 0;">{my_emoji}</div>
            <span class="badge {'badge-x' if my_mark == 'X' else 'badge-o'}">{my_mark} {'(선공)' if my_mark == 'X' else '(후공)'}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 대기 중 ──
    if not both_joined:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <div style="font-size:2.5rem; margin-bottom:12px;">⏳</div>
            <div style="font-weight:700; font-size:1.1rem; color:#fbbf24;">친구를 기다리는 중...</div>
            <div style="color:#555570; font-size:0.88rem; margin-top:8px;">
                친구에게 코드 <strong style="color:#a78bfa;">{code}</strong>를 알려주세요!<br>
                친구가 접속하면 자동으로 시작돼요.
            </div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(2)
        st.rerun()

    # ── 게임 진행 중 ──
    board = room["board"]
    winner = room["winner"]
    draw = room["draw"]
    win_line = room.get("win_line", [])
    is_my_turn = room["current_turn"] == my_mark
    game_over = winner is not None or draw

    # 턴 / 결과 표시
    if game_over:
        if winner == my_mark:
            st.markdown('<div class="result-banner win-banner">🎉 승리했어요!</div>', unsafe_allow_html=True)
        elif winner == opponent_mark:
            st.markdown('<div class="result-banner lose-banner">😢 패배했어요...</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-banner draw-banner">🤝 무승부예요!</div>', unsafe_allow_html=True)
    else:
        if is_my_turn:
            st.markdown(f'<div class="turn-info your-turn">✅ 내 차례예요! ({my_emoji} {my_mark})</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="turn-info their-turn">⏳ 상대 차례를 기다리는 중... ({opp_emoji} {opponent_mark})</div>', unsafe_allow_html=True)

    # ── 보드 ──
    cell_labels = []
    for i, cell in enumerate(board):
        if cell == "X":
            cell_labels.append("⭕")
        elif cell == "O":
            cell_labels.append("❌")
        else:
            cell_labels.append(" ")

    # 3x3 버튼 그리드
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            idx = row * 3 + col
            with cols[col]:
                cell_val = board[idx]
                btn_label = cell_labels[idx]
                disabled = bool(cell_val) or not is_my_turn or game_over

                if st.button(
                    btn_label if btn_label.strip() else "　",
                    key=f"cell_{idx}",
                    disabled=disabled,
                    use_container_width=True,
                ):
                    # 클릭 처리
                    fresh = load_room(code)
                    if fresh and fresh["board"][idx] == "" and fresh["current_turn"] == my_mark:
                        fresh["board"][idx] = my_mark
                        w, wl = check_winner(fresh["board"])
                        if w:
                            fresh["winner"] = w
                            fresh["win_line"] = wl
                        elif is_draw(fresh["board"]):
                            fresh["draw"] = True
                        else:
                            fresh["current_turn"] = opponent_mark
                        save_room(code, fresh)
                        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 버튼 ──
    col1, col2 = st.columns(2)
    with col1:
        if game_over:
            # 리매치 요청
            rematch = room.get("rematch_request", {"X": False, "O": False})
            already_requested = rematch.get(my_mark, False)
            opp_requested = rematch.get(opponent_mark, False)

            if already_requested and opp_requested:
                # 둘 다 리매치 원함 → 초기화
                room["board"] = [""] * 9
                room["current_turn"] = "X"
                room["winner"] = None
                room["draw"] = False
                room["win_line"] = []
                room["rematch_request"] = {"X": False, "O": False}
                save_room(code, room)
                st.rerun()
            elif already_requested:
                st.markdown('<div style="text-align:center; color:#fbbf24; font-size:0.88rem; padding:12px;">⏳ 상대 리매치 수락 대기 중...</div>', unsafe_allow_html=True)
            else:
                if st.button("🔄  리매치 신청", use_container_width=True):
                    room["rematch_request"][my_mark] = True
                    save_room(code, room)
                    st.rerun()

                if opp_requested:
                    st.markdown('<div style="color:#34d399; font-size:0.82rem; text-align:center; margin-top:4px;">상대가 리매치를 신청했어요!</div>', unsafe_allow_html=True)

    with col2:
        if st.button("🚪  방 나가기", use_container_width=True):
            # 방 삭제 후 로비로
            try:
                get_room_path(code).unlink()
            except Exception:
                pass
            st.session_state.room_code = None
            st.session_state.my_mark = None
            st.rerun()

    # ── 자동 새로고침 (게임 중이고 내 차례 아닐 때) ──
    if not game_over and not is_my_turn:
        time.sleep(1.5)
        st.rerun()
    elif game_over:
        # 리매치 수락 여부 폴링
        time.sleep(1.5)
        st.rerun()

# ── 푸터 ──
st.markdown("<br>")
st.markdown(
    "<div style='text-align:center; color:#222235; font-size:0.75rem;'>⭕❌ 틱택토 멀티플레이어 | Made with Streamlit</div>",
    unsafe_allow_html=True,
)
