import json
import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="🐍 Snake World",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1rem;
        max-width: 1500px;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #111827 0%,
            #0f172a 100%
        );
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    .game-title {
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: -2px;
        margin-bottom: 0;
        background: linear-gradient(
            90deg,
            #4ade80,
            #22d3ee,
            #818cf8
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .game-subtitle {
        color: #94a3b8;
        margin-top: -8px;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## 🐍 SNAKE WORLD")
st.sidebar.caption("나만의 뱀을 만들어 보세요!")

st.sidebar.markdown("---")

snake_style = st.sidebar.selectbox(
    "🐍 뱀 스타일",
    [
        "클래식",
        "지렁이",
        "네온",
        "무지개",
    ],
)

snake_color = st.sidebar.selectbox(
    "🎨 뱀 색상",
    [
        "초록",
        "파랑",
        "보라",
        "빨강",
        "주황",
        "분홍",
        "민트",
    ],
)

food = st.sidebar.selectbox(
    "🍴 먹이",
    [
        "사과",
        "딸기",
        "포도",
        "체리",
        "햄버거",
        "치즈",
    ],
)

theme = st.sidebar.selectbox(
    "🗺️ 맵 테마",
    [
        "숲",
        "사막",
        "얼음",
        "우주",
    ],
)

difficulty = st.sidebar.selectbox(
    "⚡ 난이도",
    [
        "쉬움",
        "보통",
        "어려움",
        "지옥",
    ],
    index=1,
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    ### 🎮 조작법

    **↑** 위로 이동  
    **↓** 아래로 이동  
    **←** 왼쪽 이동  
    **→** 오른쪽 이동  

    **Space** 일시정지

    먹이를 먹으면  
    🐍 몸이 한 칸씩 길어집니다!
    """
)

st.sidebar.markdown("---")

st.sidebar.info(
    "💡 게임 중에는 게임 화면을 클릭한 뒤 방향키를 사용하세요."
)


# ============================================================
# CONFIG
# ============================================================

config = {
    "snake_style": snake_style,
    "snake_color": snake_color,
    "food": food,
    "theme": theme,
    "difficulty": difficulty,
}

config_json = json.dumps(config, ensure_ascii=False)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="game-title">🐍 SNAKE WORLD</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="game-subtitle">'
    '먹고, 성장하고, 살아남으세요!'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# GAME HTML / JAVASCRIPT
# ============================================================

html = r"""
<!DOCTYPE html>
<html lang="ko">

<head>

<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

body {
    background: #020617;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
}

.game-wrapper {
    width: 100%;
    max-width: 1100px;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 18px;
    padding: 12px 18px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.25);
}

.brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.brand-icon {
    font-size: 28px;
}

.brand-title {
    font-size: 18px;
    font-weight: 800;
}

.stats {
    display: flex;
    gap: 18px;
}

.stat {
    min-width: 75px;
    text-align: center;
}

.stat-label {
    color: #94a3b8;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stat-value {
    font-size: 21px;
    font-weight: 900;
}

#gameCanvas {
    display: block;
    width: 100%;
    flex: 1;
    min-height: 480px;
    border-radius: 24px;
    border: 2px solid rgba(148, 163, 184, 0.2);
    box-shadow:
        0 25px 70px rgba(0,0,0,0.45),
        inset 0 0 50px rgba(255,255,255,0.02);
    cursor: crosshair;
    outline: none;
}

.bottom-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 5px;
}

.message {
    color: #94a3b8;
    font-size: 13px;
}

.controls {
    display: flex;
    gap: 8px;
}

button {
    border: 1px solid rgba(148,163,184,0.25);
    background: #1e293b;
    color: white;
    border-radius: 10px;
    padding: 9px 14px;
    cursor: pointer;
    font-weight: 700;
}

button:hover {
    background: #334155;
}

.mobile-controls {
    display: none;
    grid-template-columns: repeat(3, 55px);
    grid-template-rows: repeat(2, 55px);
    justify-content: center;
    gap: 6px;
}

.mobile-btn {
    font-size: 20px;
    padding: 0;
}

.mobile-up {
    grid-column: 2;
}

.mobile-left {
    grid-column: 1;
    grid-row: 2;
}

.mobile-down {
    grid-column: 2;
    grid-row: 2;
}

.mobile-right {
    grid-column: 3;
    grid-row: 2;
}

.overlay {
    position: fixed;
    inset: 0;
    display: none;
    align-items: center;
    justify-content: center;
    background: rgba(2,6,23,0.78);
    backdrop-filter: blur(8px);
    z-index: 10;
}

.overlay-card {
    width: min(420px, 90%);
    text-align: center;
    padding: 35px;
    border-radius: 25px;
    background:
        linear-gradient(
            145deg,
            #111827,
            #1e293b
        );
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 30px 100px rgba(0,0,0,0.5);
}

.overlay-title {
    font-size: 38px;
    font-weight: 900;
    margin-bottom: 8px;
}

.overlay-score {
    font-size: 20px;
    color: #94a3b8;
    margin-bottom: 25px;
}

.restart-button {
    background: linear-gradient(
        135deg,
        #22c55e,
        #06b6d4
    );
    border: none;
    padding: 13px 30px;
    font-size: 16px;
}

@media (max-width: 700px) {

    .top-bar {
        border-radius: 12px;
        padding: 8px 10px;
    }

    .brand-title {
        font-size: 14px;
    }

    .stats {
        gap: 7px;
    }

    .stat {
        min-width: 55px;
    }

    .stat-value {
        font-size: 17px;
    }

    #gameCanvas {
        min-height: 390px;
        border-radius: 15px;
    }

    .mobile-controls {
        display: grid;
    }

    .bottom-bar {
        flex-direction: column;
        gap: 10px;
    }
}

</style>

</head>

<body>

<div class="game-wrapper">

    <div class="top-bar">

        <div class="brand">
            <div class="brand-icon">🐍</div>
            <div class="brand-title">SNAKE WORLD</div>
        </div>

        <div class="stats">

            <div class="stat">
                <div class="stat-label">SCORE</div>
                <div class="stat-value" id="score">0</div>
            </div>

            <div class="stat">
                <div class="stat-label">BEST</div>
                <div class="stat-value" id="best">0</div>
            </div>

            <div class="stat">
                <div class="stat-label">LENGTH</div>
                <div class="stat-value" id="length">3</div>
            </div>

        </div>

    </div>

    <canvas id="gameCanvas" tabindex="0"></canvas>

    <div class="mobile-controls">

        <button class="mobile-btn mobile-up" data-dir="up">▲</button>
        <button class="mobile-btn mobile-left" data-dir="left">◀</button>
        <button class="mobile-btn mobile-down" data-dir="down">▼</button>
        <button class="mobile-btn mobile-right" data-dir="right">▶</button>

    </div>

    <div class="bottom-bar">

        <div class="message" id="message">
            방향키로 움직이세요
        </div>

        <div class="controls">
            <button id="pauseBtn">⏸ 일시정지</button>
            <button id="restartBtn">🔄 다시 시작</button>
        </div>

    </div>

</div>


<div class="overlay" id="gameOverOverlay">

    <div class="overlay-card">

        <div class="overlay-title">
            💥 GAME OVER
        </div>

        <div class="overlay-score">
            점수: <strong id="finalScore">0</strong>
        </div>

        <button class="restart-button" id="overlayRestart">
            다시 도전하기
        </button>

    </div>

</div>


<script>

const CONFIG = __CONFIG__;

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const scoreElement = document.getElementById("score");
const bestElement = document.getElementById("best");
const lengthElement = document.getElementById("length");
const messageElement = document.getElementById("message");

const pauseBtn = document.getElementById("pauseBtn");
const restartBtn = document.getElementById("restartBtn");

const overlay = document.getElementById("gameOverOverlay");
const finalScore = document.getElementById("finalScore");
const overlayRestart = document.getElementById("overlayRestart");


// ============================================================
// GAME SETTINGS
// ============================================================

const GRID = 28;

const difficultySpeed = {
    "쉬움": 155,
    "보통": 110,
    "어려움": 78,
    "지옥": 52
};

const THEMES = {

    "숲": {
        background: "#071c12",
        board: "#0b2a1a",
        grid: "rgba(74,222,128,0.055)",
        border: "#22c55e",
        glow: "rgba(34,197,94,0.25)",
        decoration: "#14532d"
    },

    "사막": {
        background: "#291807",
        board: "#4a2d0d",
        grid: "rgba(251,191,36,0.07)",
        border: "#f59e0b",
        glow: "rgba(245,158,11,0.25)",
        decoration: "#78350f"
    },

    "얼음": {
        background: "#071b2b",
        board: "#0c3045",
        grid: "rgba(125,211,252,0.07)",
        border: "#38bdf8",
        glow: "rgba(56,189,248,0.28)",
        decoration: "#164e63"
    },

    "우주": {
        background: "#07051c",
        board: "#100d2e",
        grid: "rgba(167,139,250,0.07)",
        border: "#8b5cf6",
        glow: "rgba(139,92,246,0.3)",
        decoration: "#312e81"
    }
};


const COLORS = {

    "초록": "#22c55e",
    "파랑": "#3b82f6",
    "보라": "#a855f7",
    "빨강": "#ef4444",
    "주황": "#f97316",
    "분홍": "#ec4899",
    "민트": "#2dd4bf"

};


const FOOD_EMOJI = {

    "사과": "🍎",
    "딸기": "🍓",
    "포도": "🍇",
    "체리": "🍒",
    "햄버거": "🍔",
    "치즈": "🧀"

};


const theme = THEMES[CONFIG.theme];
const snakeColor = COLORS[CONFIG.snake_color];
const speed = difficultySpeed[CONFIG.difficulty];


// ============================================================
// CANVAS
// ============================================================

let width = 800;
let height = 600;
let cell = 20;

function resizeCanvas() {

    const rect = canvas.getBoundingClientRect();

    const dpr = window.devicePixelRatio || 1;

    width = rect.width;
    height = rect.height;

    canvas.width = width * dpr;
    canvas.height = height * dpr;

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    cell = Math.min(
        width / GRID,
        height / GRID
    );
}

window.addEventListener("resize", resizeCanvas);


// ============================================================
// GAME STATE
// ============================================================

let snake;
let direction;
let nextDirection;

let foodPosition;

let score = 0;

let best = Number(
    localStorage.getItem("snakeWorldBest") || 0
);

let running = true;
let paused = false;

let lastUpdate = 0;

bestElement.textContent = best;


// ============================================================
// AUDIO
// ============================================================

let audioContext = null;

function playEatSound() {

    try {

        if (!audioContext) {
            audioContext =
                new (window.AudioContext ||
                window.webkitAudioContext)();
        }

        const oscillator =
            audioContext.createOscillator();

        const gain =
            audioContext.createGain();

        oscillator.frequency.value = 520;
        oscillator.type = "sine";

        gain.gain.setValueAtTime(
            0.08,
            audioContext.currentTime
        );

        gain.gain.exponentialRampToValueAtTime(
            0.001,
            audioContext.currentTime + 0.15
        );

        oscillator.connect(gain);
        gain.connect(audioContext.destination);

        oscillator.start();

        oscillator.stop(
            audioContext.currentTime + 0.15
        );

    } catch (e) {}

}


// ============================================================
// RANDOM FOOD
// ============================================================

function randomFood() {

    let position;

    do {

        position = {
            x: Math.floor(Math.random() * GRID),
            y: Math.floor(Math.random() * GRID)
        };

    } while (
        snake.some(
            part =>
                part.x === position.x &&
                part.y === position.y
        )
    );

    return position;
}


// ============================================================
// START GAME
// ============================================================

function startGame() {

    const center = Math.floor(GRID / 2);

    snake = [

        {
            x: center,
            y: center
        },

        {
            x: center - 1,
            y: center
        },

        {
            x: center - 2,
            y: center
        }

    ];

    direction = {
        x: 1,
        y: 0
    };

    nextDirection = {
        x: 1,
        y: 0
    };

    score = 0;

    foodPosition = randomFood();

    running = true;
    paused = false;

    overlay.style.display = "none";

    pauseBtn.textContent = "⏸ 일시정지";

    messageElement.textContent =
        "방향키로 움직이세요";

    updateStats();

    canvas.focus();

    lastUpdate = performance.now();

    requestAnimationFrame(gameLoop);
}


// ============================================================
// STATS
// ============================================================

function updateStats() {

    scoreElement.textContent = score;
    bestElement.textContent = best;
    lengthElement.textContent = snake.length;

}


// ============================================================
// DIRECTION
// ============================================================

function changeDirection(dir) {

    if (!running) {
        return;
    }

    const directions = {

        up: {
            x: 0,
            y: -1
        },

        down: {
            x: 0,
            y: 1
        },

        left: {
            x: -1,
            y: 0
        },

        right: {
            x: 1,
            y: 0
        }

    };

    const newDirection = directions[dir];

    if (!newDirection) {
        return;
    }


    // 180도 반전 방지

    if (
        newDirection.x === -direction.x &&
        newDirection.y === -direction.y
    ) {
        return;
    }

    if (
        newDirection.x === -nextDirection.x &&
        newDirection.y === -nextDirection.y
    ) {
        return;
    }

    nextDirection = newDirection;
}


// ============================================================
// KEYBOARD
// ============================================================

document.addEventListener("keydown", function(event) {

    const key = event.key;

    if (
        [
            "ArrowUp",
            "ArrowDown",
            "ArrowLeft",
            "ArrowRight",
            " "
        ].includes(key)
    ) {
        event.preventDefault();
    }


    if (key === "ArrowUp") {
        changeDirection("up");
    }

    else if (key === "ArrowDown") {
        changeDirection("down");
    }

    else if (key === "ArrowLeft") {
        changeDirection("left");
    }

    else if (key === "ArrowRight") {
        changeDirection("right");
    }

    else if (key === " ") {
        togglePause();
    }

});


// ============================================================
// MOBILE CONTROLS
// ============================================================

document
    .querySelectorAll(".mobile-btn")
    .forEach(button => {

        button.addEventListener(
            "pointerdown",
            function(event) {

                event.preventDefault();

                changeDirection(
                    button.dataset.dir
                );

                canvas.focus();

            }
        );

    });


// ============================================================
// GAME UPDATE
// ============================================================

function updateGame() {

    direction = {
        ...nextDirection
    };

    const head = {
        x: snake[0].x + direction.x,
        y: snake[0].y + direction.y
    };


    // 벽 충돌

    if (
        head.x < 0 ||
        head.x >= GRID ||
        head.y < 0 ||
        head.y >= GRID
    ) {

        gameOver();
        return;
    }


    // 몸 충돌

    const ateFood =
        head.x === foodPosition.x &&
        head.y === foodPosition.y;

    const collisionBody =
        ateFood
            ? snake
            : snake.slice(0, -1);

    if (
        collisionBody.some(
            part =>
                part.x === head.x &&
                part.y === head.y
        )
    ) {

        gameOver();
        return;
    }


    snake.unshift(head);


    // 먹이

    if (ateFood) {

        score++;

        if (score > best) {

            best = score;

            localStorage.setItem(
                "snakeWorldBest",
                best
            );

        }

        foodPosition = randomFood();

        playEatSound();

    }

    else {

        snake.pop();

    }

    updateStats();

}


// ============================================================
// GAME OVER
// ============================================================

function gameOver() {

    running = false;

    finalScore.textContent = score;

    overlay.style.display = "flex";

    messageElement.textContent =
        "게임이 끝났습니다";

}


// ============================================================
// PAUSE
// ============================================================

function togglePause() {

    if (!running) {
        return;
    }

    paused = !paused;

    if (paused) {

        pauseBtn.textContent =
            "▶ 계속하기";

        messageElement.textContent =
            "일시정지됨";

    }

    else {

        pauseBtn.textContent =
            "⏸ 일시정지";

        messageElement.textContent =
            "게임 진행 중";

        lastUpdate = performance.now();

    }

}


// ============================================================
// BUTTONS
// ============================================================

pauseBtn.addEventListener(
    "click",
    togglePause
);

restartBtn.addEventListener(
    "click",
    startGame
);

overlayRestart.addEventListener(
    "click",
    startGame
);


// ============================================================
// BACKGROUND
// ============================================================

function drawBackground() {

    ctx.fillStyle = theme.background;

    ctx.fillRect(
        0,
        0,
        width,
        height
    );


    // board

    const boardWidth = GRID * cell;
    const boardHeight = GRID * cell;

    const offsetX =
        (width - boardWidth) / 2;

    const offsetY =
        (height - boardHeight) / 2;


    ctx.fillStyle = theme.board;

    ctx.beginPath();

    ctx.roundRect(
        offsetX,
        offsetY,
        boardWidth,
        boardHeight,
        18
    );

    ctx.fill();


    // grid

    ctx.strokeStyle = theme.grid;
    ctx.lineWidth = 1;

    for (let x = 0; x <= GRID; x++) {

        ctx.beginPath();

        ctx.moveTo(
            offsetX + x * cell,
            offsetY
        );

        ctx.lineTo(
            offsetX + x * cell,
            offsetY + boardHeight
        );

        ctx.stroke();

    }

    for (let y = 0; y <= GRID; y++) {

        ctx.beginPath();

        ctx.moveTo(
            offsetX,
            offsetY + y * cell
        );

        ctx.lineTo(
            offsetX + boardWidth,
            offsetY + y * cell
        );

        ctx.stroke();

    }


    // border

    ctx.strokeStyle = theme.border;
    ctx.lineWidth = 3;

    ctx.shadowColor = theme.glow;
    ctx.shadowBlur = 20;

    ctx.beginPath();

    ctx.roundRect(
        offsetX,
        offsetY,
        boardWidth,
        boardHeight,
        18
    );

    ctx.stroke();

    ctx.shadowBlur = 0;


    drawThemeDecoration(
        offsetX,
        offsetY,
        boardWidth,
        boardHeight
    );

}


function drawThemeDecoration(
    offsetX,
    offsetY,
    boardWidth,
    boardHeight
) {

    ctx.save();

    ctx.globalAlpha = 0.25;

    if (CONFIG.theme === "숲") {

        drawTree(
            offsetX + 25,
            offsetY + 25
        );

        drawTree(
            offsetX + boardWidth - 25,
            offsetY + 40
        );

    }

    else if (CONFIG.theme === "사막") {

        drawCactus(
            offsetX + 25,
            offsetY + 35
        );

        drawCactus(
            offsetX + boardWidth - 30,
            offsetY + 45
        );

    }

    else if (CONFIG.theme === "얼음") {

        drawSnowflake(
            offsetX + 30,
            offsetY + 30
        );

        drawSnowflake(
            offsetX + boardWidth - 30,
            offsetY + 40
        );

    }

    else if (CONFIG.theme === "우주") {

        for (let i = 0; i < 30; i++) {

            const sx =
                offsetX +
                Math.random() *
                boardWidth;

            const sy =
                offsetY +
                Math.random() *
                boardHeight;

            ctx.fillStyle = "#ffffff";

            ctx.beginPath();

            ctx.arc(
                sx,
                sy,
                Math.random() * 1.5,
                0,
                Math.PI * 2
            );

            ctx.fill();

        }

    }

    ctx.restore();

}


function drawTree(x, y) {

    ctx.fillStyle = "#166534";

    ctx.beginPath();

    ctx.arc(
        x,
        y,
        16,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.fillRect(
        x - 4,
        y + 10,
        8,
        14
    );

}


function drawCactus(x, y) {

    ctx.fillStyle = "#65a30d";

    ctx.fillRect(
        x - 5,
        y - 15,
        10,
        35
    );

    ctx.fillRect(
        x - 16,
        y - 4,
        10,
        8
    );

    ctx.fillRect(
        x + 6,
        y - 10,
        10,
        8
    );

}


function drawSnowflake(x, y) {

    ctx.strokeStyle = "#bae6fd";
    ctx.lineWidth = 2;

    for (let i = 0; i < 3; i++) {

        const angle =
            i * Math.PI / 3;

        ctx.beginPath();

        ctx.moveTo(
            x - Math.cos(angle) * 14,
            y - Math.sin(angle) * 14
        );

        ctx.lineTo(
            x + Math.cos(angle) * 14,
            y + Math.sin(angle) * 14
        );

        ctx.stroke();

    }

}


// ============================================================
// FOOD
// ============================================================

function drawFood() {

    const boardWidth = GRID * cell;
    const boardHeight = GRID * cell;

    const offsetX =
        (width - boardWidth) / 2;

    const offsetY =
        (height - boardHeight) / 2;

    const x =
        offsetX +
        foodPosition.x * cell +
        cell / 2;

    const y =
        offsetY +
        foodPosition.y * cell +
        cell / 2;


    // glow

    ctx.save();

    ctx.shadowColor = theme.border;
    ctx.shadowBlur = 18;

    ctx.font =
        `${Math.max(20, cell * 0.82)}px Arial`;

    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    ctx.fillText(
        FOOD_EMOJI[CONFIG.food],
        x,
        y
    );

    ctx.restore();

}


// ============================================================
// SNAKE
// ============================================================

function getSegmentColor(index) {

    if (CONFIG.snake_style === "무지개") {

        const hue =
            (index * 35 + score * 8) % 360;

        return `hsl(${hue}, 85%, 55%)`;

    }


    if (CONFIG.snake_style === "네온") {

        const base =
            snakeColor;

        return index % 2 === 0
            ? base
            : lightenColor(base, 25);

    }


    if (index === 0) {

        return lightenColor(
            snakeColor,
            15
        );

    }


    return darkenColor(
        snakeColor,
        Math.min(
            35,
            index * 2
        )
    );

}


function lightenColor(hex, amount) {

    const num =
        parseInt(hex.slice(1), 16);

    let r =
        Math.min(
            255,
            ((num >> 16) & 255) + amount
        );

    let g =
        Math.min(
            255,
            ((num >> 8) & 255) + amount
        );

    let b =
        Math.min(
            255,
            (num & 255) + amount
        );

    return `rgb(${r},${g},${b})`;

}


function darkenColor(hex, amount) {

    const num =
        parseInt(hex.slice(1), 16);

    let r =
        Math.max(
            0,
            ((num >> 16) & 255) - amount
        );

    let g =
        Math.max(
            0,
            ((num >> 8) & 255) - amount
        );

    let b =
        Math.max(
            0,
            (num & 255) - amount
        );

    return `rgb(${r},${g},${b})`;

}


function drawSnake() {

    const boardWidth = GRID * cell;
    const boardHeight = GRID * cell;

    const offsetX =
        (width - boardWidth) / 2;

    const offsetY =
        (height - boardHeight) / 2;


    // tail -> head

    for (
        let i = snake.length - 1;
        i >= 0;
        i--
    ) {

        const part = snake[i];

        const cx =
            offsetX +
            part.x * cell +
            cell / 2;

        const cy =
            offsetY +
            part.y * cell +
            cell / 2;

        const radius =
            cell * 0.39;


        ctx.save();

        if (CONFIG.snake_style === "네온") {

            ctx.shadowColor =
                getSegmentColor(i);

            ctx.shadowBlur = 16;

        }


        ctx.fillStyle =
            getSegmentColor(i);


        // body segment

        ctx.beginPath();

        ctx.arc(
            cx,
            cy,
            radius,
            0,
            Math.PI * 2
        );

        ctx.fill();


        // segment highlight

        if (
            CONFIG.snake_style !== "클래식"
        ) {

            ctx.fillStyle =
                "rgba(255,255,255,0.14)";

            ctx.beginPath();

            ctx.arc(
                cx - radius * 0.28,
                cy - radius * 0.28,
                radius * 0.25,
                0,
                Math.PI * 2
            );

            ctx.fill();

        }


        ctx.restore();

    }


    drawHead(
        offsetX,
        offsetY
    );

}


function drawHead(
    offsetX,
    offsetY
) {

    const head = snake[0];

    const cx =
        offsetX +
        head.x * cell +
        cell / 2;

    const cy =
        offsetY +
        head.y * cell +
        cell / 2;

    const radius =
        cell * 0.46;


    ctx.save();

    if (CONFIG.snake_style === "네온") {

        ctx.shadowColor =
            snakeColor;

        ctx.shadowBlur = 22;

    }


    // head

    const gradient =
        ctx.createRadialGradient(
            cx - radius * 0.35,
            cy - radius * 0.4,
            1,
            cx,
            cy,
            radius
        );

    gradient.addColorStop(
        0,
        lightenColor(snakeColor, 35)
    );

    gradient.addColorStop(
        1,
        snakeColor
    );

    ctx.fillStyle = gradient;

    ctx.beginPath();

    ctx.arc(
        cx,
        cy,
        radius,
        0,
        Math.PI * 2
    );

    ctx.fill();


    // eyes position

    let eyeOffsetX = 0;
    let eyeOffsetY = 0;

    if (direction.x !== 0) {

        eyeOffsetX =
            direction.x * radius * 0.45;

        eyeOffsetY =
            radius * 0.27;

    }

    else {

        eyeOffsetX =
            radius * 0.27;

        eyeOffsetY =
            direction.y * radius * 0.45;

    }


    // eyes

    drawEye(
        cx + eyeOffsetX,
        cy + eyeOffsetY
    );

    drawEye(
        cx + eyeOffsetX,
        cy - eyeOffsetY
    );


    // tongue

    if (CONFIG.snake_style !== "클래식") {

        ctx.strokeStyle = "#fda4af";
        ctx.lineWidth = 1.7;
        ctx.lineCap = "round";

        const tongueStartX =
            cx +
            direction.x *
            radius *
            0.75;

        const tongueStartY =
            cy +
            direction.y *
            radius *
            0.75;

        const tongueEndX =
            cx +
            direction.x *
            radius *
            1.25;

        const tongueEndY =
            cy +
            direction.y *
            radius *
            1.25;

        ctx.beginPath();

        ctx.moveTo(
            tongueStartX,
            tongueStartY
        );

        ctx.lineTo(
            tongueEndX,
            tongueEndY
        );

        ctx.stroke();

    }

    ctx.restore();

}


function drawEye(x, y) {

    ctx.fillStyle = "#ffffff";

    ctx.beginPath();

    ctx.arc(
        x,
        y,
        cell * 0.105,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.fillStyle = "#111827";

    ctx.beginPath();

    ctx.arc(
        x + direction.x * cell * 0.025,
        y + direction.y * cell * 0.025,
        cell * 0.055,
        0,
        Math.PI * 2
    );

    ctx.fill();

}


// ============================================================
// DRAW
// ============================================================

function draw() {

    resizeCanvas();

    drawBackground();

    drawFood();

    drawSnake();

}


// ============================================================
// GAME LOOP
// ============================================================

function gameLoop(timestamp) {

    if (!running) {

        draw();

        return;

    }


    if (!paused) {

        if (
            timestamp - lastUpdate >= speed
        ) {

            updateGame();

            lastUpdate = timestamp;

        }

    }


    draw();

    requestAnimationFrame(
        gameLoop
    );

}


// ============================================================
// START
// ============================================================

resizeCanvas();

startGame();

</script>

</body>
</html>
"""


html = html.replace(
    "__CONFIG__",
    config_json
)


components.html(
    html,
    height=760,
    scrolling=False
)
