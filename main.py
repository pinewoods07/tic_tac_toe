import streamlit as st
import json
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
.card {
    background: linear-gradient(135deg, #16162a 0%, #1e1e35 100%);
    border: 1px solid #2a2a45;
    border-radius: 16px;
    padding: 28px 32px;
    margin: 12px 0;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}
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
.badge {
    display: inline-block;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.8rem;
    font-weight: 700;
}
.badge-x { background: rgba(167,139,250,0.15); color: #a78bfa; border: 1px solid rgba(167,139,250,0.3); }
.badge-o { background: rgba(96,165,250,0.15); color: #60a5fa; border: 1px solid rgba(96,165,250,0.3); }
.badge-ai { background: rgba(251,113,133,0.15); color: #fb7185; border: 1px solid rgba(251,113,133,0.3); }

/* AI 난이도 뱃지 */
.diff-easy   { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.3); border-radius:20px; padding:3px 12px; font-size:0.8rem; font-weight:700; }
.diff-normal { background: rgba(251,191,36,0.15); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); border-radius:20px; padding:3px 12px; font-size:0.8rem; font-weight:700; }
.diff-hard   { background: rgba(239,68,68,0.15);  color: #f87171; border: 1px solid rgba(239,68,68,0.3);  border-radius:20px; padding:3px 12px; font-size:0.8rem; font-weight:700; }

.turn-info {
    text-align: center;
    font-size: 1.1rem;
    font-weight: 700;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 16px;
}
.your-turn  { background: rgba(52,211,153,0.12); color: #34d399; border: 1px solid rgba(52,211,153,0.25); }
.their-turn { background: rgba(100,100,120,0.12); color: #666680; border: 1px solid rgba(100,100,120,0.2); }
.ai-turn    { background: rgba(251,113,133,0.10); color: #fb7185; border: 1px solid rgba(251,113,133,0.2); }

.result-banner {
    text-align: center;
    font-family: 'Black Han Sans', sans-serif;
    font-size: 1.8rem;
    padding: 20px;
    border-radius: 14px;
    margin: 16px 0;
    letter-spacing: 2px;
}
.win-banner  { background: rgba(52,211,153,0.12); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.lose-banner { background: rgba(239,68,68,0.10);  color: #f87171; border: 1px solid rgba(239,68,68,0.25); }
.draw-banner { background: rgba(251,191,36,0.10); color: #fbbf24; border: 1px solid rgba(251,191,36,0.25); }

/* AI 타이핑 효과 */
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }
.ai-thinking { animation: blink 1s ease-in-out infinite; color: #fb7185; font-size: 0.9rem; text-align:center; margin:8px 0; }

/* 모드 선택 카드 */
.mode-card {
    background: #16162a;
    border: 2px solid #2a2a45;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
}
.mode-card:hover { border-color: #a78bfa; }

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

/* 점수판 */
.scoreboard {
    display: flex;
    gap: 10px;
    margin-bottom: 16px;
}
.score-item {
    flex: 1;
    background: #16162a;
    border: 1px solid #2a2a45;
    border-radius: 12px;
    padding: 10px;
    text-align: center;
}
.score-num { font-family: 'Black Han Sans', sans-serif; font-size: 2rem; }
.score-label { font-size: 0.72rem; color: #555570; margin-top: 2px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  게임 로직
# ─────────────────────────────────────────
def check_winner(board):
    lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for line in lines:
        a, b, c = line
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], line
    return None, []

def is_draw(board):
    return all(c != "" for c in board)

# ── 미니맥스 AI ──
def minimax(board, is_maximizing, ai_mark, human_mark):
    winner, _ = check_winner(board)
    if winner == ai_mark:
        return 10
    if winner == human_mark:
        return -10
    if is_draw(board):
        return 0

    if is_maximizing:
        best = -100
        for i in range(9):
            if board[i] == "":
                board[i] = ai_mark
                best = max(best, minimax(board, False, ai_mark, human_mark))
                board[i] = ""
        return best
    else:
        best = 100
        for i in range(9):
            if board[i] == "":
                board[i] = human_mark
                best = min(best, minimax(board, True, ai_mark, human_mark))
                board[i] = ""
        return best

def ai_move(board, ai_mark, human_mark, difficulty):
    empty = [i for i, c in enumerate(board) if c == ""]
    if not empty:
        return None

    if difficulty == "쉬움":
        # 완전 랜덤
        return random.choice(empty)

    elif difficulty == "보통":
        # 60% 확률로 최선, 40% 랜덤
        if random.random() < 0.6:
            # 이길 수 있으면 이기고, 막을 수 있으면 막고
            for i in empty:
                board[i] = ai_mark
                w, _ = check_winner(board)
                board[i] = ""
                if w == ai_mark:
                    return i
            for i in empty:
                board[i] = human_mark
                w, _ = check_winner(board)
                board[i] = ""
                if w == human_mark:
                    return i
            return random.choice(empty)
        else:
            return random.choice(empty)

    else:  # 어려움 - 미니맥스 (완전 최강)
        best_score = -100
        best_move = random.choice(empty)
        for i in empty:
            board[i] = ai_mark
            score = minimax(board, False, ai_mark, human_mark)
            board[i] = ""
            if score > best_score:
                best_score = score
                best_move = i
        return best_move

# ─────────────────────────────────────────
#  멀티플레이어 방 관리
# ─────────────────────────────────────────
def get_room_path(code):
    return ROOMS_DIR / f"{code}.json"

def create_room(code):
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
    with open(get_room_path(code), "w") as f:
        json.dump(state, f)
    return state

def load_room(code):
    path = get_room_path(code)
    if path.exists():
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            return None
    return None

def save_room(code, state):
    with open(get_room_path(code), "w") as f:
        json.dump(state, f)

def generate_code():
    while True:
        code = ''.join(random.choices(string.digits, k=4))
        if not get_room_path(code).exists():
            return code

def cleanup_old_rooms():
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
#  세션 초기화
# ─────────────────────────────────────────
defaults = {
    "mode": None,           # "ai" | "multi"
    "ai_board": [""] * 9,
    "ai_turn": "X",         # X = 플레이어, O = AI
    "ai_winner": None,
    "ai_draw": False,
    "ai_win_line": [],
    "ai_difficulty": "보통",
    "ai_thinking": False,
    "ai_score": {"player": 0, "ai": 0, "draw": 0},
    "room_code": None,
    "my_mark": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────
#  헤더
# ─────────────────────────────────────────
st.markdown('<div class="main-title">⭕ 틱택토 ❌</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">— AI 대결 · 친구와 1대1 —</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────
#  모드 선택 화면
# ─────────────────────────────────────────
if st.session_state.mode is None:
    cleanup_old_rooms()
    st.markdown("### 🎮 모드를 선택하세요")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="mode-card">
            <div style="font-size:2.8rem;">🤖</div>
            <div style="font-weight:700; font-size:1.05rem; margin:8px 0;">AI 대결</div>
            <div style="color:#666680; font-size:0.82rem;">혼자서 AI와 대결!<br>난이도 3단계 선택 가능</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🤖  AI와 대결하기", use_container_width=True):
            st.session_state.mode = "ai"
            st.rerun()
    with col2:
        st.markdown("""
        <div class="mode-card">
            <div style="font-size:2.8rem;">👥</div>
            <div style="font-weight:700; font-size:1.05rem; margin:8px 0;">친구와 대결</div>
            <div style="color:#666680; font-size:0.82rem;">방 코드로 친구 초대!<br>실시간 1대1 대결</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("👥  친구와 대결하기", use_container_width=True):
            st.session_state.mode = "multi"
            st.rerun()

# ─────────────────────────────────────────
#  AI 모드
# ─────────────────────────────────────────
elif st.session_state.mode == "ai":

    # 상단 정보
    col_l, col_r = st.columns([1, 1])
    with col_l:
        diff = st.session_state.ai_difficulty
        diff_class = {"쉬움": "diff-easy", "보통": "diff-normal", "어려움": "diff-hard"}[diff]
        diff_emoji = {"쉬움": "😊", "보통": "😤", "어려움": "💀"}[diff]
        st.markdown(f"""
        <div style="text-align:center; padding:14px; background:#16162a; border:1px solid #2a2a45; border-radius:12px;">
            <div class="room-code-label">난이도</div>
            <div style="font-size:2rem; margin:6px 0;">{diff_emoji}</div>
            <span class="{diff_class}">{diff}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_r:
        sc = st.session_state.ai_score
        st.markdown(f"""
        <div style="padding:14px; background:#16162a; border:1px solid #2a2a45; border-radius:12px;">
            <div class="room-code-label" style="text-align:center;">전적</div>
            <div class="scoreboard" style="margin-top:10px; margin-bottom:0;">
                <div class="score-item">
                    <div class="score-num" style="color:#34d399;">{sc['player']}</div>
                    <div class="score-label">내 승리</div>
                </div>
                <div class="score-item">
                    <div class="score-num" style="color:#fb7185;">{sc['ai']}</div>
                    <div class="score-label">AI 승리</div>
                </div>
                <div class="score-item">
                    <div class="score-num" style="color:#fbbf24;">{sc['draw']}</div>
                    <div class="score-label">무승부</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    board = st.session_state.ai_board
    ai_winner = st.session_state.ai_winner
    ai_draw = st.session_state.ai_draw
    current_turn = st.session_state.ai_turn
    game_over = ai_winner is not None or ai_draw
    is_player_turn = current_turn == "X"

    # AI가 먼저 생각 중인지 확인 후 AI 수 두기
    if not game_over and not is_player_turn:
        st.markdown('<div class="ai-thinking">🤖 AI가 생각 중...</div>', unsafe_allow_html=True)
        time.sleep(0.6)
        move = ai_move(board, "O", "X", st.session_state.ai_difficulty)
        if move is not None:
            board[move] = "O"
            w, wl = check_winner(board)
            if w:
                st.session_state.ai_winner = w
                st.session_state.ai_win_line = wl
                st.session_state.ai_score["ai"] += 1
            elif is_draw(board):
                st.session_state.ai_draw = True
                st.session_state.ai_score["draw"] += 1
            else:
                st.session_state.ai_turn = "X"
        st.rerun()

    # 턴 / 결과 표시
    if game_over:
        if ai_winner == "X":
            st.markdown('<div class="result-banner win-banner">🎉 이겼어요!</div>', unsafe_allow_html=True)
        elif ai_winner == "O":
            st.markdown('<div class="result-banner lose-banner">🤖 AI가 이겼어요...</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-banner draw-banner">🤝 무승부예요!</div>', unsafe_allow_html=True)
    else:
        if is_player_turn:
            st.markdown('<div class="turn-info your-turn">✅ 내 차례예요! (⭕ X)</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="turn-info ai-turn">🤖 AI 차례...</div>', unsafe_allow_html=True)

    # 보드
    win_line = st.session_state.ai_win_line
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            idx = row * 3 + col
            cell = board[idx]
            with cols[col]:
                if cell == "X":
                    label = "⭕"
                elif cell == "O":
                    label = "❌"
                else:
                    label = "　"
                disabled = bool(cell) or not is_player_turn or game_over
                if st.button(label, key=f"ai_cell_{idx}", disabled=disabled, use_container_width=True):
                    if board[idx] == "" and is_player_turn and not game_over:
                        board[idx] = "X"
                        w, wl = check_winner(board)
                        if w:
                            st.session_state.ai_winner = w
                            st.session_state.ai_win_line = wl
                            st.session_state.ai_score["player"] += 1
                        elif is_draw(board):
                            st.session_state.ai_draw = True
                            st.session_state.ai_score["draw"] += 1
                        else:
                            st.session_state.ai_turn = "O"
                        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # 버튼 행
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄  다시하기", use_container_width=True):
            st.session_state.ai_board = [""] * 9
            st.session_state.ai_turn = "X"
            st.session_state.ai_winner = None
            st.session_state.ai_draw = False
            st.session_state.ai_win_line = []
            st.rerun()
    with col2:
        # 난이도 변경
        diff_options = ["쉬움", "보통", "어려움"]
        current_idx = diff_options.index(st.session_state.ai_difficulty)
        next_diff = diff_options[(current_idx + 1) % 3]
        next_emoji = {"쉬움": "😊", "보통": "😤", "어려움": "💀"}[next_diff]
        if st.button(f"⚙️  난이도: {next_emoji}{next_diff}", use_container_width=True):
            st.session_state.ai_difficulty = next_diff
            st.session_state.ai_board = [""] * 9
            st.session_state.ai_turn = "X"
            st.session_state.ai_winner = None
            st.session_state.ai_draw = False
            st.session_state.ai_win_line = []
            st.rerun()
    with col3:
        if st.button("🏠  처음으로", use_container_width=True):
            st.session_state.mode = None
            st.session_state.ai_board = [""] * 9
            st.session_state.ai_turn = "X"
            st.session_state.ai_winner = None
            st.session_state.ai_draw = False
            st.session_state.ai_win_line = []
            st.session_state.ai_score = {"player": 0, "ai": 0, "draw": 0}
            st.rerun()

# ─────────────────────────────────────────
#  멀티플레이어 모드
# ─────────────────────────────────────────
elif st.session_state.mode == "multi":

    # 로비
    if st.session_state.room_code is None:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ✨ 새 방 만들기")
        st.markdown("<div style='color:#666680; font-size:0.88rem; margin-bottom:12px;'>방을 만들고 친구에게 코드를 알려주세요!</div>", unsafe_allow_html=True)
        if st.button("✨  방 만들기 (내가 ⭕ 선공)", use_container_width=True):
            code = generate_code()
            create_room(code)
            st.session_state.room_code = code
            st.session_state.my_mark = "X"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='text-align:center; color:#333350; margin:8px 0;'>— 또는 —</div>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🔑 방 참가하기")
        st.markdown("<div style='color:#666680; font-size:0.88rem; margin-bottom:12px;'>친구에게 받은 4자리 코드를 입력하세요!</div>", unsafe_allow_html=True)
        code_input = st.text_input("", placeholder="0000", max_chars=4, label_visibility="collapsed")
        if st.button("🚪  입장하기 (내가 ❌ 후공)", use_container_width=True):
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

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠  처음으로", use_container_width=True):
                st.session_state.mode = None
                st.rerun()
        st.markdown("<div class='small-info'>⏰ 방은 1시간 후 자동으로 삭제됩니다</div>", unsafe_allow_html=True)

    # 게임 중
    else:
        code = st.session_state.room_code
        my_mark = st.session_state.my_mark
        opponent_mark = "O" if my_mark == "X" else "X"
        my_emoji = "⭕" if my_mark == "X" else "❌"
        opp_emoji = "❌" if my_mark == "X" else "⭕"

        room = load_room(code)
        if room is None:
            st.error("방 정보를 불러올 수 없어요.")
            if st.button("🏠 처음으로"):
                st.session_state.room_code = None
                st.session_state.my_mark = None
                st.session_state.mode = None
                st.rerun()
            st.stop()

        both_joined = room["players"]["X"] and room["players"]["O"]

        col_l, col_r = st.columns(2)
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

        if not both_joined:
            st.markdown(f"""
            <div class="card" style="text-align:center;">
                <div style="font-size:2.5rem; margin-bottom:12px;">⏳</div>
                <div style="font-weight:700; font-size:1.1rem; color:#fbbf24;">친구를 기다리는 중...</div>
                <div style="color:#555570; font-size:0.88rem; margin-top:8px;">
                    코드 <strong style="color:#a78bfa;">{code}</strong>를 친구에게 알려주세요!<br>
                    친구가 접속하면 자동으로 시작돼요.
                </div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(2)
            st.rerun()

        board = room["board"]
        winner = room["winner"]
        draw = room["draw"]
        win_line = room.get("win_line", [])
        is_my_turn = room["current_turn"] == my_mark
        game_over = winner is not None or draw

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
                st.markdown(f'<div class="turn-info their-turn">⏳ 상대 차례 기다리는 중... ({opp_emoji} {opponent_mark})</div>', unsafe_allow_html=True)

        for row in range(3):
            cols = st.columns(3)
            for col in range(3):
                idx = row * 3 + col
                cell = board[idx]
                with cols[col]:
                    label = "⭕" if cell == "X" else ("❌" if cell == "O" else "　")
                    disabled = bool(cell) or not is_my_turn or game_over
                    if st.button(label, key=f"mp_cell_{idx}", disabled=disabled, use_container_width=True):
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

        col1, col2, col3 = st.columns(3)
        with col1:
            if game_over:
                rematch = room.get("rematch_request", {"X": False, "O": False})
                already = rematch.get(my_mark, False)
                opp_req = rematch.get(opponent_mark, False)
                if already and opp_req:
                    room["board"] = [""] * 9
                    room["current_turn"] = "X"
                    room["winner"] = None
                    room["draw"] = False
                    room["win_line"] = []
                    room["rematch_request"] = {"X": False, "O": False}
                    save_room(code, room)
                    st.rerun()
                elif already:
                    st.markdown('<div style="text-align:center;color:#fbbf24;font-size:0.85rem;padding:10px;">⏳ 상대 수락 대기중...</div>', unsafe_allow_html=True)
                else:
                    if st.button("🔄  리매치", use_container_width=True):
                        room["rematch_request"][my_mark] = True
                        save_room(code, room)
                        st.rerun()
                    if opp_req:
                        st.markdown('<div style="color:#34d399;font-size:0.8rem;text-align:center;">상대가 리매치 신청!</div>', unsafe_allow_html=True)
        with col2:
            if st.button("🏠  처음으로", use_container_width=True):
                try:
                    get_room_path(code).unlink()
                except Exception:
                    pass
                st.session_state.room_code = None
                st.session_state.my_mark = None
                st.session_state.mode = None
                st.rerun()
        with col3:
            if st.button("🚪  방 나가기", use_container_width=True):
                try:
                    get_room_path(code).unlink()
                except Exception:
                    pass
                st.session_state.room_code = None
                st.session_state.my_mark = None
                st.rerun()

        if not game_over and not is_my_turn:
            time.sleep(1.5)
            st.rerun()
        elif game_over:
            time.sleep(1.5)
            st.rerun()

# ── 푸터 ──
st.markdown("<br>")
st.markdown(
    "<div style='text-align:center; color:#222235; font-size:0.75rem;'>⭕❌ 틱택토 | AI 대결 · 친구와 1대1 | Made with Streamlit</div>",
    unsafe_allow_html=True,
)
