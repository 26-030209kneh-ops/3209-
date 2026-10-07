import json
import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Snake World",
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
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1rem;
        max-width: 1500px;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0f172a 0%,
                #020617 100%
            );
    }

    .snake-title {
        font-size: 3.2rem;
        font-weight: 950;
        letter-spacing: -3px;
        background:
            linear-gradient(
                90deg,
                #4ade80,
                #22d3ee,
                #818cf8,
                #e879f9
            );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }

    .snake-subtitle {
        color: #94a3b8;
        margin-top: -8px;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## 🐍 SNAKE WORLD")
st.sidebar.caption("나만의 생명체를 만들어 보세요.")

st.sidebar.markdown("---")


game_mode = st.sidebar.selectbox(
    "🎮 게임 모드",
    [
        "클래식",
        "어드벤처",
        "AI 대결",
    ],
)


snake_style = st.sidebar.selectbox(
    "🐍 뱀 스타일",
    [
        "클래식",
        "지렁이",
        "코브라",
        "드래곤",
        "사이버",
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
        "황금사과",
        "고추",
    ],
)


theme = st.sidebar.selectbox(
    "🗺️ 맵",
    [
        "숲",
        "사막",
        "얼음",
        "우주",
    ],
)


difficulty = st.sidebar.selectbox(
    "⚡ 게임 난이도",
    [
        "쉬움",
        "보통",
        "어려움",
        "지옥",
    ],
    index=1,
)


special_food = st.sidebar.toggle(
    "✨ 음식 특수효과",
    value=game_mode != "클래식",
)


missions = st.sidebar.toggle(
    "🎯 미션 시스템",
    value=game_mode != "클래식",
)


evolution = st.sidebar.toggle(
    "🧬 진화 시스템",
    value=game_mode != "클래식",
)


obstacles = st.sidebar.toggle(
    "🧱 맵 장애물",
    value=game_mode != "클래식",
)


# ============================================================
# MUSIC SETTINGS
# ============================================================

st.sidebar.markdown("---")

music_enabled = st.sidebar.toggle(
    "🎵 배경음악",
    value=True,
)

music_volume = st.sidebar.slider(
    "🔊 음악 볼륨",
    min_value=0,
    max_value=100,
    value=35,
    step=5,
)

sound_effects = st.sidebar.toggle(
    "🔔 효과음",
    value=True,
)


# ============================================================
# AI
# ============================================================

ai_level = "중"

if game_mode == "AI 대결":

    st.sidebar.markdown("---")

    ai_level = st.sidebar.select_slider(
        "🤖 AI 실력",
        options=[
            "하",
            "중",
            "상",
        ],
        value="중",
    )


st.sidebar.markdown("---")

st.sidebar.markdown(
    """
### 🎮 조작법

**↑ ↓ ← →** 이동  
**W A S D** 이동  
**Space** 일시정지

### 🎵 음악

게임 화면에서  
**음악 시작** 버튼을 누르면  
배경음악이 재생됩니다.

### 🍴 특수 음식

특수효과를 끄면  
일반 Snake처럼 플레이합니다.

### 🧬 진화

길이가 늘어나면  
뱀의 모습이 단계적으로 변합니다.
"""
)


# ============================================================
# CONFIG
# ============================================================

config = {
    "gameMode": game_mode,
    "snakeStyle": snake_style,
    "snakeColor": snake_color,
    "food": food,
    "theme": theme,
    "difficulty": difficulty,
    "specialFood": special_food,
    "missions": missions,
    "evolution": evolution,
    "obstacles": obstacles,
    "aiLevel": ai_level,
    "musicEnabled": music_enabled,
    "musicVolume": music_volume,
    "soundEffects": sound_effects,
}

config_json = json.dumps(
    config,
    ensure_ascii=False,
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="snake-title">🐍 SNAKE WORLD</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="snake-subtitle">'
    '먹고 · 성장하고 · 진화하고 · 살아남으세요'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# GAME HTML
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

html,
body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
}

body {
    background: #020617;
    color: white;

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    display: flex;
    justify-content: center;
    align-items: center;
}

.game {
    width: 100%;
    max-width: 1150px;
    height: 100%;

    display: flex;
    flex-direction: column;

    gap: 10px;
}

.top {
    height: 68px;
    flex-shrink: 0;

    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 10px 18px;

    background:
        linear-gradient(
            135deg,
            rgba(15,23,42,.98),
            rgba(30,41,59,.95)
        );

    border:
        1px solid
        rgba(148,163,184,.18);

    border-radius: 18px;

    box-shadow:
        0 15px 50px rgba(0,0,0,.25);
}

.logo {
    display: flex;
    align-items: center;
    gap: 10px;
}

.logo-icon {
    font-size: 29px;
}

.logo-text {
    font-size: 17px;
    font-weight: 900;
}

.mode {
    font-size: 10px;
    color: #94a3b8;
    margin-top: 2px;
}

.stats {
    display: flex;
    gap: 10px;
}

.stat {
    min-width: 75px;
    text-align: center;
}

.label {
    color: #64748b;
    font-size: 9px;
    letter-spacing: 1px;
}

.value {
    font-size: 20px;
    font-weight: 900;
}

#canvas {
    width: 100%;
    flex: 1;
    min-height: 480px;

    display: block;

    border-radius: 24px;

    border:
        2px solid
        rgba(148,163,184,.18);

    outline: none;

    box-shadow:
        0 25px 80px rgba(0,0,0,.5);

    cursor: crosshair;
}

.bottom {
    flex-shrink: 0;

    display: flex;
    align-items: center;
    justify-content: space-between;

    min-height: 45px;
}

.status {
    color: #94a3b8;
    font-size: 13px;
}

.buttons {
    display: flex;
    gap: 7px;
    flex-wrap: wrap;
    justify-content: flex-end;
}

.game-btn {
    color: white;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 9px;
    padding: 8px 13px;
    font-weight: 700;
    cursor: pointer;
}

.game-btn:hover {
    background: #334155;
}

.music-btn {
    background:
        linear-gradient(
            135deg,
            #7c3aed,
            #2563eb
        );

    border-color:
        rgba(167,139,250,.5);
}

.mobile {
    display: none;

    grid-template-columns:
        repeat(3, 54px);

    grid-template-rows:
        repeat(2, 54px);

    justify-content: center;

    gap: 5px;
}

.mobile button {
    background: #1e293b;
    color: white;
    border:
        1px solid
        #334155;

    border-radius: 12px;
    font-size: 19px;
}

.up {
    grid-column: 2;
}

.left {
    grid-column: 1;
    grid-row: 2;
}

.down {
    grid-column: 2;
    grid-row: 2;
}

.right {
    grid-column: 3;
    grid-row: 2;
}

.overlay {
    position: fixed;
    inset: 0;

    display: none;

    align-items: center;
    justify-content: center;

    background:
        rgba(2,6,23,.82);

    backdrop-filter: blur(8px);

    z-index: 50;
}

.card {
    width: min(450px, 90%);

    padding: 34px;

    text-align: center;

    background:
        linear-gradient(
            145deg,
            #111827,
            #1e293b
        );

    border:
        1px solid
        rgba(255,255,255,.12);

    border-radius: 25px;

    box-shadow:
        0 35px 100px rgba(0,0,0,.55);
}

.card-title {
    font-size: 39px;
    font-weight: 950;
}

.card-text {
    color: #94a3b8;
    margin: 10px 0 25px;
}

.restart {
    color: white;
    border: 0;
    border-radius: 12px;
    padding: 13px 30px;
    font-weight: 900;
    font-size: 15px;

    background:
        linear-gradient(
            135deg,
            #22c55e,
            #06b6d4
        );

    cursor: pointer;
}

.mission {
    position: absolute;

    left: 20px;
    top: 95px;

    padding: 10px 13px;

    border-radius: 12px;

    background:
        rgba(15,23,42,.88);

    border:
        1px solid
        rgba(255,255,255,.1);

    font-size: 11px;

    min-width: 190px;

    pointer-events: none;
}

.mission-title {
    color: #fbbf24;
    font-weight: 900;
    margin-bottom: 4px;
}

.mission-progress {
    color: #cbd5e1;
}

.power {
    position: absolute;

    right: 20px;
    top: 95px;

    padding: 9px 12px;

    border-radius: 12px;

    background:
        rgba(15,23,42,.88);

    border:
        1px solid
        rgba(255,255,255,.1);

    font-size: 11px;

    pointer-events: none;
}

.music-indicator {
    position: absolute;

    right: 20px;
    bottom: 75px;

    padding: 8px 12px;

    border-radius: 10px;

    background:
        rgba(15,23,42,.85);

    border:
        1px solid
        rgba(255,255,255,.1);

    color: #cbd5e1;

    font-size: 11px;

    pointer-events: none;
}

@media(max-width:700px) {

    .top {
        height: 55px;
        border-radius: 12px;
    }

    .logo-text {
        font-size: 13px;
    }

    .stats {
        gap: 3px;
    }

    .stat {
        min-width: 48px;
    }

    .value {
        font-size: 16px;
    }

    #canvas {
        min-height: 380px;
        border-radius: 15px;
    }

    .mobile {
        display: grid;
    }

    .bottom {
        flex-direction: column;
        gap: 7px;
    }

    .mission,
    .power,
    .music-indicator {
        display: none;
    }

}

</style>

</head>


<body>


<div class="game">


    <div class="top">

        <div class="logo">

            <div class="logo-icon">
                🐍
            </div>

            <div>

                <div class="logo-text">
                    SNAKE WORLD
                </div>

                <div class="mode"
                     id="modeText">
                    CLASSIC
                </div>

            </div>

        </div>


        <div class="stats">

            <div class="stat">

                <div class="label">
                    SCORE
                </div>

                <div class="value"
                     id="score">
                    0
                </div>

            </div>


            <div class="stat">

                <div class="label">
                    BEST
                </div>

                <div class="value"
                     id="best">
                    0
                </div>

            </div>


            <div class="stat">

                <div class="label">
                    LENGTH
                </div>

                <div class="value"
                     id="length">
                    3
                </div>

            </div>


            <div class="stat">

                <div class="label">
                    LEVEL
                </div>

                <div class="value"
                     id="level">
                    1
                </div>

            </div>

        </div>

    </div>


    <canvas id="canvas"
            tabindex="0">
    </canvas>


    <div class="mission"
         id="missionBox">

        <div class="mission-title">
            🎯 MISSION
        </div>

        <div class="mission-progress"
             id="missionText">
            준비 중...
        </div>

    </div>


    <div class="power"
         id="powerBox">

        ⚡
        <span id="powerText">
            특별 효과 없음
        </span>

    </div>


    <div class="music-indicator"
         id="musicIndicator">
        🎵 음악 대기 중
    </div>


    <div class="mobile">

        <button class="up"
                data-dir="up">
            ▲
        </button>

        <button class="left"
                data-dir="left">
            ◀
        </button>

        <button class="down"
                data-dir="down">
            ▼
        </button>

        <button class="right"
                data-dir="right">
            ▶
        </button>

    </div>


    <div class="bottom">

        <div class="status"
             id="status">
            방향키로 시작하세요
        </div>

        <div class="buttons">

            <button class="game-btn music-btn"
                    id="musicButton">
                🎵 음악 시작
            </button>

            <button class="game-btn"
                    id="pause">
                ⏸ 일시정지
            </button>

            <button class="game-btn"
                    id="restart">
                🔄 다시 시작
            </button>

        </div>

    </div>

</div>


<div class="overlay"
     id="overlay">

    <div class="card">

        <div class="card-title"
             id="overTitle">
            GAME OVER
        </div>

        <div class="card-text"
             id="overText">
            점수: 0
        </div>

        <button class="restart"
                id="overRestart">
            다시 도전하기
        </button>

    </div>

</div>


<script>


// ============================================================
// CONFIG
// ============================================================

const CONFIG = __CONFIG__;


// ============================================================
// DOM
// ============================================================

const canvas =
    document.getElementById("canvas");

const ctx =
    canvas.getContext("2d");

const scoreEl =
    document.getElementById("score");

const bestEl =
    document.getElementById("best");

const lengthEl =
    document.getElementById("length");

const levelEl =
    document.getElementById("level");

const statusEl =
    document.getElementById("status");

const modeEl =
    document.getElementById("modeText");

const overlay =
    document.getElementById("overlay");

const overTitle =
    document.getElementById("overTitle");

const overText =
    document.getElementById("overText");

const missionBox =
    document.getElementById("missionBox");

const missionText =
    document.getElementById("missionText");

const powerText =
    document.getElementById("powerText");

const musicButton =
    document.getElementById("musicButton");

const musicIndicator =
    document.getElementById("musicIndicator");


// ============================================================
// AUDIO SYSTEM
// ============================================================

let audioContext = null;

let masterGain = null;

let musicGain = null;

let musicTimer = null;

let musicPlaying = false;

let musicStep = 0;


/*
    외부 음악 파일을 사용하지 않고
    Web Audio API로 게임용 배경음악을 생성합니다.

    따라서 별도의 mp3 파일을 GitHub에 넣지 않아도
    바로 작동합니다.
*/


const melody = [
    261.63,
    329.63,
    392.00,
    329.63,
    293.66,
    349.23,
    440.00,
    349.23
];


const bass = [
    130.81,
    130.81,
    146.83,
    146.83,
    164.81,
    164.81,
    146.83,
    146.83
];


function setupAudio() {

    if (audioContext) {
        return;
    }

    audioContext =
        new (
            window.AudioContext ||
            window.webkitAudioContext
        )();

    masterGain =
        audioContext.createGain();

    musicGain =
        audioContext.createGain();

    masterGain.gain.value = 0.9;

    musicGain.gain.value =
        CONFIG.musicVolume / 100 * 0.20;

    musicGain.connect(masterGain);

    masterGain.connect(
        audioContext.destination
    );

}


function playTone(
    frequency,
    duration,
    type,
    volume,
    destination
) {

    if (!audioContext) {
        return;
    }

    const oscillator =
        audioContext.createOscillator();

    const gain =
        audioContext.createGain();

    oscillator.type =
        type;

    oscillator.frequency.value =
        frequency;

    gain.gain.setValueAtTime(
        0,
        audioContext.currentTime
    );

    gain.gain.linearRampToValueAtTime(
        volume,
        audioContext.currentTime + 0.015
    );

    gain.gain.exponentialRampToValueAtTime(
        0.001,
        audioContext.currentTime +
        duration
    );

    oscillator.connect(gain);

    gain.connect(
        destination
    );

    oscillator.start();

    oscillator.stop(
        audioContext.currentTime +
        duration +
        0.02
    );

}


function musicTick() {

    if (
        !musicPlaying ||
        !audioContext
    ) {
        return;
    }

    const now =
        audioContext.currentTime;

    const note =
        melody[
            musicStep %
            melody.length
        ];

    const bassNote =
        bass[
            musicStep %
            bass.length
        ];


    const osc =
        audioContext.createOscillator();

    const gain =
        audioContext.createGain();


    osc.type = "sine";

    osc.frequency.setValueAtTime(
        note,
        now
    );

    gain.gain.setValueAtTime(
        0,
        now
    );

    gain.gain.linearRampToValueAtTime(
        0.055,
        now + 0.025
    );

    gain.gain.exponentialRampToValueAtTime(
        0.001,
        now + 0.42
    );


    osc.connect(gain);

    gain.connect(
        musicGain
    );

    osc.start(now);

    osc.stop(
        now + 0.45
    );


    // BASS

    const bassOsc =
        audioContext.createOscillator();

    const bassGain =
        audioContext.createGain();


    bassOsc.type =
        "triangle";

    bassOsc.frequency.setValueAtTime(
        bassNote,
        now
    );

    bassGain.gain.setValueAtTime(
        0,
        now
    );

    bassGain.gain.linearRampToValueAtTime(
        0.035,
        now + 0.02
    );

    bassGain.gain.exponentialRampToValueAtTime(
        0.001,
        now + 0.48
    );


    bassOsc.connect(
        bassGain
    );

    bassGain.connect(
        musicGain
    );

    bassOsc.start(now);

    bassOsc.stop(
        now + 0.5
    );


    musicStep++;

}


function startMusic() {

    if (!CONFIG.musicEnabled) {

        statusEl.textContent =
            "🎵 사이드바에서 음악을 켜주세요";

        return;

    }


    setupAudio();


    if (
        audioContext.state ===
        "suspended"
    ) {

        audioContext.resume();

    }


    if (musicPlaying) {
        return;
    }


    musicPlaying = true;

    musicStep = 0;


    musicTimer =
        setInterval(
            musicTick,
            500
        );


    musicTick();


    musicButton.textContent =
        "🔇 음악 끄기";

    musicIndicator.textContent =
        "🎵 BGM ON";

}


function stopMusic() {

    musicPlaying = false;


    if (musicTimer) {

        clearInterval(
            musicTimer
        );

        musicTimer = null;

    }


    musicButton.textContent =
        "🎵 음악 시작";

    musicIndicator.textContent =
        "🎵 음악 OFF";

}


function toggleMusic() {

    if (musicPlaying) {

        stopMusic();

    }

    else {

        startMusic();

    }

}


function soundEffect(
    type
) {

    if (
        !CONFIG.soundEffects
    ) {
        return;
    }


    setupAudio();


    if (
        audioContext.state ===
        "suspended"
    ) {

        audioContext.resume();

    }


    if (type === "eat") {

        playTone(
            520,
            0.10,
            "sine",
            0.12,
            masterGain
        );

        setTimeout(
            () => {

                playTone(
                    780,
                    0.12,
                    "sine",
                    0.10,
                    masterGain
                );

            },
            55
        );

    }


    if (type === "mission") {

        playTone(
            523.25,
            0.12,
            "triangle",
            0.14,
            masterGain
        );

        setTimeout(
            () => {

                playTone(
                    659.25,
                    0.12,
                    "triangle",
                    0.14,
                    masterGain
                );

            },
            100
        );

        setTimeout(
            () => {

                playTone(
                    783.99,
                    0.20,
                    "triangle",
                    0.14,
                    masterGain
                );

            },
            200
        );

    }


    if (type === "gameover") {

        playTone(
            392,
            0.18,
            "sawtooth",
            0.10,
            masterGain
        );

        setTimeout(
            () => {

                playTone(
                    293.66,
                    0.25,
                    "sawtooth",
                    0.10,
                    masterGain
                );

            },
            160
        );

        setTimeout(
            () => {

                playTone(
                    196,
                    0.35,
                    "sawtooth",
                    0.08,
                    masterGain
                );

            },
            350
        );

    }


    if (type === "evolution") {

        playTone(
            440,
            0.10,
            "square",
            0.08,
            masterGain
        );

        setTimeout(
            () => {

                playTone(
                    554.37,
                    0.10,
                    "square",
                    0.08,
                    masterGain
                );

            },
            100
        );

        setTimeout(
            () => {

                playTone(
                    659.25,
                    0.16,
                    "square",
                    0.08,
                    masterGain
                );

            },
            200
        );

    }

}


musicButton.onclick =
    toggleMusic;


// ============================================================
// CONSTANTS
// ============================================================

const GRID = 30;


const SPEEDS = {

    "쉬움": 155,
    "보통": 110,
    "어려움": 78,
    "지옥": 52

};


const AI_SPEEDS = {

    "하": 145,
    "중": 105,
    "상": 72

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


const FOOD = {

    "사과": {
        emoji: "🍎",
        points: 1,
        grow: 1,
        effect: "몸 +1"
    },

    "딸기": {
        emoji: "🍓",
        points: 2,
        grow: 2,
        effect: "몸 +2"
    },

    "포도": {
        emoji: "🍇",
        points: 5,
        grow: 1,
        effect: "점수 +5"
    },

    "체리": {
        emoji: "🍒",
        points: 3,
        grow: 1,
        effect: "잠시 속도 증가"
    },

    "햄버거": {
        emoji: "🍔",
        points: 4,
        grow: 4,
        effect: "몸 +4 / 느려짐"
    },

    "치즈": {
        emoji: "🧀",
        points: 3,
        grow: 1,
        effect: "3초 무적"
    },

    "황금사과": {
        emoji: "🍏",
        points: 10,
        grow: 3,
        effect: "보너스"
    },

    "고추": {
        emoji: "🌶️",
        points: 6,
        grow: 1,
        effect: "엄청 빨라짐"
    }

};


// ============================================================
// THEMES
// ============================================================

const THEMES = {

    "숲": {
        bg: "#06140d",
        board: "#0b2416",
        grid: "rgba(74,222,128,.06)",
        border: "#22c55e",
        accent: "#86efac"
    },

    "사막": {
        bg: "#241205",
        board: "#4a2b0a",
        grid: "rgba(251,191,36,.06)",
        border: "#f59e0b",
        accent: "#fde68a"
    },

    "얼음": {
        bg: "#041522",
        board: "#0a2c40",
        grid: "rgba(125,211,252,.07)",
        border: "#38bdf8",
        accent: "#bae6fd"
    },

    "우주": {
        bg: "#060313",
        board: "#100a27",
        grid: "rgba(167,139,250,.07)",
        border: "#8b5cf6",
        accent: "#ddd6fe"
    }

};


const THEME =
    THEMES[CONFIG.theme];

const SNAKE_COLOR =
    COLORS[CONFIG.snakeColor];


// ============================================================
// CANVAS
// ============================================================

let W = 800;

let H = 600;

let cell = 20;


function resize() {

    const r =
        canvas.getBoundingClientRect();

    const dpr =
        window.devicePixelRatio || 1;

    W = r.width;

    H = r.height;

    canvas.width =
        W * dpr;

    canvas.height =
        H * dpr;

    ctx.setTransform(
        dpr,
        0,
        0,
        dpr,
        0,
        0
    );

    cell =
        Math.min(
            W / GRID,
            H / GRID
        );

}


window.addEventListener(
    "resize",
    resize
);


// ============================================================
// GAME STATE
// ============================================================

let snake = [];

let aiSnake = [];

let direction = {
    x: 1,
    y: 0
};

let nextDirection = {
    x: 1,
    y: 0
};

let aiDirection = {
    x: -1,
    y: 0
};

let foodPos = null;

let score = 0;

let best =
    Number(
        localStorage.getItem(
            "snakeWorldBest"
        ) || 0
    );

let level = 1;

let running = true;

let paused = false;

let lastTime = 0;

let invincibleUntil = 0;

let speedUntil = 0;

let obstacleList = [];

let particles = [];

let stars = [];

let mission = null;

let missionDone = false;

let evolutionStage = 1;


// ============================================================
// MISSIONS
// ============================================================

const MISSIONS = [

    {
        text: "음식 5개 먹기",
        type: "eat",
        target: 5
    },

    {
        text: "점수 15점 만들기",
        type: "score",
        target: 15
    },

    {
        text: "길이 12 달성",
        type: "length",
        target: 12
    },

    {
        text: "음식 8개 연속 먹기",
        type: "eat",
        target: 8
    }

];


let missionProgress = 0;


function newMission() {

    if (!CONFIG.missions) {

        missionBox.style.display =
            "none";

        return;

    }

    missionBox.style.display =
        "block";


    mission =
        MISSIONS[
            Math.floor(
                Math.random() *
                MISSIONS.length
            )
        ];


    missionProgress = 0;

    missionDone = false;

    updateMission();

}


function updateMission() {

    if (
        !CONFIG.missions ||
        !mission
    ) {
        return;
    }


    if (
        mission.type === "eat"
    ) {

        missionProgress =
            Math.min(
                mission.target,
                score
            );

    }


    if (
        mission.type === "score"
    ) {

        missionProgress =
            Math.min(
                mission.target,
                score
            );

    }


    if (
        mission.type === "length"
    ) {

        missionProgress =
            Math.min(
                mission.target,
                snake.length
            );

    }


    missionText.textContent =
        `${mission.text}  ${missionProgress}/${mission.target}`;


    if (
        missionProgress >=
        mission.target &&
        !missionDone
    ) {

        missionDone = true;

        score += 10;

        statusEl.textContent =
            "🎉 미션 완료! +10 보너스";

        soundEffect(
            "mission"
        );

        createParticles(
            snake[0].x,
            snake[0].y,
            "#fbbf24",
            30
        );

        setTimeout(
            newMission,
            1200
        );

    }

}


// ============================================================
// ACHIEVEMENTS
// ============================================================

function unlockAchievement(
    id,
    title
) {

    const key =
        "snakeAchievement_" + id;


    if (
        localStorage.getItem(key)
    ) {

        return;

    }


    localStorage.setItem(
        key,
        "true"
    );


    statusEl.textContent =
        `🏆 업적 달성: ${title}`;

}


// ============================================================
// INIT
// ============================================================

function init() {

    resize();


    const c =
        Math.floor(
            GRID / 2
        );


    snake = [

        {
            x: c,
            y: c
        },

        {
            x: c - 1,
            y: c
        },

        {
            x: c - 2,
            y: c
        }

    ];


    if (
        CONFIG.gameMode ===
        "AI 대결"
    ) {

        aiSnake = [

            {
                x: GRID - 5,
                y: GRID - 5
            },

            {
                x: GRID - 4,
                y: GRID - 5
            },

            {
                x: GRID - 3,
                y: GRID - 5
            }

        ];


        aiDirection = {
            x: -1,
            y: 0
        };

    }


    direction = {
        x: 1,
        y: 0
    };


    nextDirection = {
        x: 1,
        y: 0
    };


    score = 0;

    level = 1;

    running = true;

    paused = false;

    invincibleUntil = 0;

    speedUntil = 0;

    evolutionStage = 1;


    createObstacles();

    createStars();

    spawnFood();

    newMission();


    modeEl.textContent =
        CONFIG.gameMode.toUpperCase();


    bestEl.textContent =
        best;


    updateStats();


    overlay.style.display =
        "none";


    statusEl.textContent =
        "방향키로 이동하세요";


    lastTime =
        performance.now();


    canvas.focus();


    requestAnimationFrame(
        loop
    );

}


// ============================================================
// STATS
// ============================================================

function updateStats() {

    scoreEl.textContent =
        score;

    bestEl.textContent =
        best;

    lengthEl.textContent =
        snake.length;

    levelEl.textContent =
        level;

}


// ============================================================
// OBSTACLES
// ============================================================

function createObstacles() {

    obstacleList = [];


    if (!CONFIG.obstacles) {
        return;
    }


    if (
        CONFIG.gameMode ===
        "클래식"
    ) {

        return;

    }


    let amount = 10;


    if (
        CONFIG.theme ===
        "사막"
    ) {

        amount = 12;

    }


    if (
        CONFIG.theme ===
        "얼음"
    ) {

        amount = 8;

    }


    if (
        CONFIG.theme ===
        "우주"
    ) {

        amount = 6;

    }


    for (
        let i = 0;
        i < amount;
        i++
    ) {

        let p;

        let safe = false;


        for (
            let tries = 0;
            tries < 100 &&
            !safe;
            tries++
        ) {

            p = {

                x:
                    Math.floor(
                        Math.random() *
                        GRID
                    ),

                y:
                    Math.floor(
                        Math.random() *
                        GRID
                    )

            };


            safe =
                Math.abs(
                    p.x -
                    Math.floor(
                        GRID / 2
                    )
                ) > 5 &&

                Math.abs(
                    p.y -
                    Math.floor(
                        GRID / 2
                    )
                ) > 5;


            if (
                obstacleList.some(
                    o =>
                        o.x === p.x &&
                        o.y === p.y
                )
            ) {

                safe = false;

            }

        }


        if (safe) {

            obstacleList.push(p);

        }

    }

}


// ============================================================
// STARS
// ============================================================

function createStars() {

    stars = [];


    for (
        let i = 0;
        i < 70;
        i++
    ) {

        stars.push({

            x: Math.random(),

            y: Math.random(),

            r:
                Math.random() *
                1.5 +
                0.4

        });

    }

}


// ============================================================
// FOOD
// ============================================================

function spawnFood() {

    let p;


    do {

        p = {

            x:
                Math.floor(
                    Math.random() *
                    GRID
                ),

            y:
                Math.floor(
                    Math.random() *
                    GRID
                )

        };

    }

    while (

        snake.some(
            s =>
                s.x === p.x &&
                s.y === p.y
        )

        ||

        aiSnake.some(
            s =>
                s.x === p.x &&
                s.y === p.y
        )

        ||

        obstacleList.some(
            o =>
                o.x === p.x &&
                o.y === p.y
        )

    );


    foodPos = p;

}


// ============================================================
// INPUT
// ============================================================

function setDirection(dir) {

    if (!running) {
        return;
    }


    const dirs = {

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


    const nd =
        dirs[dir];


    if (!nd) {
        return;
    }


    if (
        nd.x === -direction.x &&
        nd.y === -direction.y
    ) {

        return;

    }


    nextDirection = nd;

}


document.addEventListener(
    "keydown",
    e => {

        const key =
            e.key.toLowerCase();


        if (
            [
                "arrowup",
                "arrowdown",
                "arrowleft",
                "arrowright",
                " ",
                "w",
                "a",
                "s",
                "d"
            ].includes(key)
        ) {

            e.preventDefault();

        }


        if (
            key === "arrowup" ||
            key === "w"
        ) {

            setDirection("up");

        }


        if (
            key === "arrowdown" ||
            key === "s"
        ) {

            setDirection("down");

        }


        if (
            key === "arrowleft" ||
            key === "a"
        ) {

            setDirection("left");

        }


        if (
            key === "arrowright" ||
            key === "d"
        ) {

            setDirection("right");

        }


        if (key === " ") {

            togglePause();

        }

    }
);


document
    .querySelectorAll(
        ".mobile button"
    )
    .forEach(
        button => {

            button.addEventListener(
                "pointerdown",
                e => {

                    e.preventDefault();

                    setDirection(
                        button.dataset.dir
                    );

                    canvas.focus();

                }
            );

        }
    );


// ============================================================
// COLLISION
// ============================================================

function obstacleCollision(p) {

    return obstacleList.some(
        o =>
            o.x === p.x &&
            o.y === p.y
    );

}


function selfCollision(p) {

    return snake.some(
        s =>
            s.x === p.x &&
            s.y === p.y
    );

}


function aiCollision(p) {

    return aiSnake.some(
        s =>
            s.x === p.x &&
            s.y === p.y
    );

}


// ============================================================
// PLAYER UPDATE
// ============================================================

function updatePlayer() {

    direction = {
        ...nextDirection
    };


    let head = {

        x:
            snake[0].x +
            direction.x,

        y:
            snake[0].y +
            direction.y

    };


    if (
        CONFIG.theme ===
        "우주"
    ) {

        if (head.x < 0)
            head.x = GRID - 1;

        if (head.x >= GRID)
            head.x = 0;

        if (head.y < 0)
            head.y = GRID - 1;

        if (head.y >= GRID)
            head.y = 0;

    }

    else {

        if (
            head.x < 0 ||
            head.x >= GRID ||
            head.y < 0 ||
            head.y >= GRID
        ) {

            gameOver(
                "벽에 부딪혔습니다!"
            );

            return;

        }

    }


    if (
        obstacleCollision(head)
    ) {

        if (
            Date.now() >
            invincibleUntil
        ) {

            gameOver(
                "장애물에 부딪혔습니다!"
            );

            return;

        }

    }


    if (
        selfCollision(head)
    ) {

        if (
            Date.now() >
            invincibleUntil
        ) {

            gameOver(
                "내 몸에 부딪혔습니다!"
            );

            return;

        }

    }


    if (
        CONFIG.gameMode ===
        "AI 대결" &&
        aiCollision(head)
    ) {

        if (
            Date.now() >
            invincibleUntil
        ) {

            gameOver(
                "AI 뱀과 충돌했습니다!"
            );

            return;

        }

    }


    snake.unshift(head);


    const ate =
        head.x === foodPos.x &&
        head.y === foodPos.y;


    if (ate) {

        eatFood();

    }

    else {

        snake.pop();

    }


    level =
        Math.floor(
            score / 10
        ) + 1;


    if (
        CONFIG.evolution
    ) {

        const newStage =
            snake.length >= 25
                ? 4
                : snake.length >= 16
                    ? 3
                    : snake.length >= 9
                        ? 2
                        : 1;


        if (
            newStage >
            evolutionStage
        ) {

            evolutionStage =
                newStage;


            statusEl.textContent =
                evolutionStage === 2
                    ? "🌱 성장했습니다!"
                    : evolutionStage === 3
                        ? "🔥 진화했습니다!"
                        : "🐉 최종 진화!";


            soundEffect(
                "evolution"
            );


            createParticles(
                snake[0].x,
                snake[0].y,
                "#fbbf24",
                45
            );

        }

    }


    updateMission();

}


// ============================================================
// FOOD EFFECT
// ============================================================

function eatFood() {

    const data =
        FOOD[CONFIG.food];


    let grow =
        CONFIG.specialFood
            ? data.grow
            : 1;


    let points =
        CONFIG.specialFood
            ? data.points
            : 1;


    score += points;


    for (
        let i = 1;
        i < grow;
        i++
    ) {

        const tail =
            snake[
                snake.length - 1
            ];


        snake.push({

            x: tail.x,

            y: tail.y

        });

    }


    if (
        CONFIG.specialFood
    ) {

        if (
            CONFIG.food ===
            "체리"
        ) {

            speedUntil =
                Date.now() + 4000;


            powerText.textContent =
                "⚡ SPEED UP";

        }


        if (
            CONFIG.food ===
            "햄버거"
        ) {

            speedUntil =
                Date.now() + 3000;


            powerText.textContent =
                "🍔 HEAVY MODE";

        }


        if (
            CONFIG.food ===
            "치즈"
        ) {

            invincibleUntil =
                Date.now() + 3000;


            powerText.textContent =
                "🛡️ 무적";

        }


        if (
            CONFIG.food ===
            "고추"
        ) {

            speedUntil =
                Date.now() + 5000;


            powerText.textContent =
                "🔥 TURBO";

        }


        if (
            CONFIG.food ===
            "황금사과"
        ) {

            createParticles(
                foodPos.x,
                foodPos.y,
                "#facc15",
                45
            );


            unlockAchievement(
                "gold",
                "황금 사냥꾼"
            );

        }

    }


    if (
        score > best
    ) {

        best = score;


        localStorage.setItem(
            "snakeWorldBest",
            best
        );

    }


    soundEffect(
        "eat"
    );


    createParticles(
        foodPos.x,
        foodPos.y,
        "#ffffff",
        18
    );


    if (
        snake.length >= 10
    ) {

        unlockAchievement(
            "ten",
            "작은 거인"
        );

    }


    if (
        snake.length >= 25
    ) {

        unlockAchievement(
            "giant",
            "거대 생명체"
        );

    }


    if (
        score >= 50
    ) {

        unlockAchievement(
            "fifty",
            "폭식가"
        );

    }


    statusEl.textContent =
        CONFIG.specialFood
            ? `${data.emoji} ${data.effect}`
            : "🍴 먹이를 먹었습니다!";


    spawnFood();

    updateStats();

}


// ============================================================
// AI
// ============================================================

function updateAI() {

    if (
        CONFIG.gameMode !==
        "AI 대결"
    ) {

        return;

    }


    if (
        aiSnake.length === 0
    ) {

        return;

    }


    const head =
        aiSnake[0];


    const dx =
        foodPos.x -
        head.x;


    const dy =
        foodPos.y -
        head.y;


    const candidates = [];


    if (
        Math.abs(dx) >=
        Math.abs(dy)
    ) {

        if (dx !== 0) {

            candidates.push({

                x: Math.sign(dx),

                y: 0

            });

        }


        if (dy !== 0) {

            candidates.push({

                x: 0,

                y: Math.sign(dy)

            });

        }

    }

    else {

        if (dy !== 0) {

            candidates.push({

                x: 0,

                y: Math.sign(dy)

            });

        }


        if (dx !== 0) {

            candidates.push({

                x: Math.sign(dx),

                y: 0

            });

        }

    }


    candidates.push(

        {
            x: 1,
            y: 0
        },

        {
            x: -1,
            y: 0
        },

        {
            x: 0,
            y: 1
        },

        {
            x: 0,
            y: -1
        }

    );


    let chosen =
        aiDirection;


    if (
        CONFIG.aiLevel ===
        "상"
    ) {

        for (
            const c of candidates
        ) {

            if (
                validAIMove(c)
            ) {

                chosen = c;

                break;

            }

        }

    }


    else if (
        CONFIG.aiLevel ===
        "중"
    ) {

        const good =
            candidates.filter(
                validAIMove
            );


        if (
            good.length
        ) {

            chosen =
                good[
                    Math.floor(
                        Math.random() *
                        good.length
                    )
                ];

        }

    }


    else {

        if (
            Math.random() <
            0.65
        ) {

            const good =
                candidates.filter(
                    validAIMove
                );


            if (
                good.length
            ) {

                chosen =
                    good[
                        Math.floor(
                            Math.random() *
                            good.length
                        )
                    ];

            }

        }

    }


    if (
        chosen.x ===
        -aiDirection.x &&

        chosen.y ===
        -aiDirection.y
    ) {

        chosen =
            aiDirection;

    }


    aiDirection =
        chosen;


    let next = {

        x:
            head.x +
            aiDirection.x,

        y:
            head.y +
            aiDirection.y

    };


    if (
        CONFIG.theme ===
        "우주"
    ) {

        if (next.x < 0)
            next.x = GRID - 1;

        if (next.x >= GRID)
            next.x = 0;

        if (next.y < 0)
            next.y = GRID - 1;

        if (next.y >= GRID)
            next.y = 0;

    }


    if (
        next.x < 0 ||
        next.x >= GRID ||
        next.y < 0 ||
        next.y >= GRID
    ) {

        return;

    }


    if (
        obstacleCollision(next)
    ) {

        return;

    }


    aiSnake.unshift(next);


    const ate =
        next.x === foodPos.x &&
        next.y === foodPos.y;


    if (!ate) {

        aiSnake.pop();

    }

    else {

        spawnFood();

    }


    if (
        snake.some(
            s =>
                s.x === next.x &&
                s.y === next.y
        )
    ) {

        gameOver(
            "AI 뱀과 충돌했습니다!"
        );

    }

}


function validAIMove(dir) {

    const h =
        aiSnake[0];


    const p = {

        x:
            h.x + dir.x,

        y:
            h.y + dir.y

    };


    if (
        CONFIG.theme ===
        "우주"
    ) {

        if (p.x < 0)
            p.x = GRID - 1;

        if (p.x >= GRID)
            p.x = 0;

        if (p.y < 0)
            p.y = GRID - 1;

        if (p.y >= GRID)
            p.y = 0;

    }


    if (
        p.x < 0 ||
        p.x >= GRID ||
        p.y < 0 ||
        p.y >= GRID
    ) {

        return false;

    }


    if (
        obstacleCollision(p)
    ) {

        return false;

    }


    if (
        aiSnake.some(
            s =>
                s.x === p.x &&
                s.y === p.y
        )
    ) {

        return false;

    }


    return true;

}


// ============================================================
// AI FINISH
// ============================================================

function checkAIFinish() {

    if (
        CONFIG.gameMode !==
        "AI 대결"
    ) {

        return;

    }


    if (
        aiSnake.length >= 30
    ) {

        gameOver(
            "🤖 AI가 먼저 거대해졌습니다!"
        );

    }

}


// ============================================================
// GAME OVER
// ============================================================

function gameOver(reason) {

    if (!running) {
        return;
    }


    running = false;


    soundEffect(
        "gameover"
    );


    overTitle.textContent =
        "💥 GAME OVER";


    overText.textContent =
        `${reason}  ·  점수 ${score}`;


    overlay.style.display =
        "flex";


    statusEl.textContent =
        reason;


    unlockAchievement(
        "first",
        "첫 번째 생존"
    );

}


// ============================================================
// PAUSE
// ============================================================

function togglePause() {

    if (!running) {
        return;
    }


    paused =
        !paused;


    if (paused) {

        statusEl.textContent =
            "⏸ 일시정지";


        document.getElementById(
            "pause"
        ).textContent =
            "▶ 계속하기";

    }

    else {

        statusEl.textContent =
            "게임 진행 중";


        document.getElementById(
            "pause"
        ).textContent =
            "⏸ 일시정지";


        lastTime =
            performance.now();

    }

}


document.getElementById(
    "pause"
).onclick =
    togglePause;


document.getElementById(
    "restart"
).onclick =
    init;


document.getElementById(
    "overRestart"
).onclick =
    init;


// ============================================================
// PARTICLES
// ============================================================

function createParticles(
    gx,
    gy,
    color,
    amount
) {

    for (
        let i = 0;
        i < amount;
        i++
    ) {

        particles.push({

            x:
                gx + 0.5,

            y:
                gy + 0.5,

            vx:
                (Math.random() - .5)
                * .16,

            vy:
                (Math.random() - .5)
                * .16,

            life: 1,

            color: color

        });

    }

}


function updateParticles() {

    particles =
        particles.filter(
            p => {

                p.x += p.vx;

                p.y += p.vy;

                p.life -= .035;

                return p.life > 0;

            }
        );

}


// ============================================================
// DRAW BACKGROUND
// ============================================================

function drawBackground() {

    ctx.fillStyle =
        THEME.bg;


    ctx.fillRect(
        0,
        0,
        W,
        H
    );


    const bw =
        GRID * cell;


    const bh =
        GRID * cell;


    const ox =
        (W - bw) / 2;


    const oy =
        (H - bh) / 2;


    ctx.fillStyle =
        THEME.board;


    ctx.beginPath();


    ctx.roundRect(
        ox,
        oy,
        bw,
        bh,
        20
    );


    ctx.fill();


    ctx.strokeStyle =
        THEME.grid;


    ctx.lineWidth = 1;


    for (
        let x = 0;
        x <= GRID;
        x++
    ) {

        ctx.beginPath();


        ctx.moveTo(
            ox + x * cell,
            oy
        );


        ctx.lineTo(
            ox + x * cell,
            oy + bh
        );


        ctx.stroke();

    }


    for (
        let y = 0;
        y <= GRID;
        y++
    ) {

        ctx.beginPath();


        ctx.moveTo(
            ox,
            oy + y * cell
        );


        ctx.lineTo(
            ox + bw,
            oy + y * cell
        );


        ctx.stroke();

    }


    ctx.strokeStyle =
        THEME.border;


    ctx.lineWidth = 3;


    ctx.shadowColor =
        THEME.border;


    ctx.shadowBlur = 20;


    ctx.beginPath();


    ctx.roundRect(
        ox,
        oy,
        bw,
        bh,
        20
    );


    ctx.stroke();


    ctx.shadowBlur = 0;


    drawThemeDetails(
        ox,
        oy,
        bw,
        bh
    );

}


function drawThemeDetails(
    ox,
    oy,
    bw,
    bh
) {

    ctx.save();


    if (
        CONFIG.theme ===
        "우주"
    ) {

        for (
            const s of stars
        ) {

            ctx.fillStyle =
                "rgba(255,255,255,.7)";


            ctx.beginPath();


            ctx.arc(
                ox + s.x * bw,
                oy + s.y * bh,
                s.r,
                0,
                Math.PI * 2
            );


            ctx.fill();

        }

    }


    if (
        CONFIG.theme ===
        "숲"
    ) {

        drawTree(
            ox + 28,
            oy + 28
        );


        drawTree(
            ox + bw - 28,
            oy + 35
        );

    }


    if (
        CONFIG.theme ===
        "사막"
    ) {

        drawCactus(
            ox + 30,
            oy + 35
        );


        drawCactus(
            ox + bw - 30,
            oy + 40
        );

    }


    if (
        CONFIG.theme ===
        "얼음"
    ) {

        drawIceCrystal(
            ox + 30,
            oy + 30
        );


        drawIceCrystal(
            ox + bw - 30,
            oy + 40
        );

    }


    ctx.restore();

}


function drawTree(x,y) {

    ctx.fillStyle =
        "#166534";


    ctx.beginPath();


    ctx.arc(
        x,
        y,
        15,
        0,
        Math.PI * 2
    );


    ctx.fill();


    ctx.fillRect(
        x - 3,
        y + 9,
        6,
        14
    );

}


function drawCactus(x,y) {

    ctx.fillStyle =
        "#65a30d";


    ctx.fillRect(
        x - 4,
        y - 15,
        8,
        35
    );


    ctx.fillRect(
        x - 14,
        y - 2,
        10,
        7
    );


    ctx.fillRect(
        x + 4,
        y - 9,
        10,
        7
    );

}


function drawIceCrystal(x,y) {

    ctx.strokeStyle =
        "#bae6fd";


    ctx.lineWidth = 2;


    for (
        let i = 0;
        i < 3;
        i++
    ) {

        const a =
            i * Math.PI / 3;


        ctx.beginPath();


        ctx.moveTo(
            x -
            Math.cos(a) * 14,
            y -
            Math.sin(a) * 14
        );


        ctx.lineTo(
            x +
            Math.cos(a) * 14,
            y +
            Math.sin(a) * 14
        );


        ctx.stroke();

    }

}


// ============================================================
// DRAW OBSTACLES
// ============================================================

function drawObstacles() {

    for (
        const o of obstacleList
    ) {

        const p =
            gridToPixel(
                o.x,
                o.y
            );


        ctx.save();


        if (
            CONFIG.theme ===
            "숲"
        ) {

            ctx.fillStyle =
                "#475569";


            ctx.beginPath();


            ctx.arc(
                p.x,
                p.y,
                cell * .34,
                0,
                Math.PI * 2
            );


            ctx.fill();


            ctx.fillStyle =
                "#64748b";


            ctx.beginPath();


            ctx.arc(
                p.x - cell*.1,
                p.y - cell*.1,
                cell*.13,
                0,
                Math.PI * 2
            );


            ctx.fill();

        }


        else if (
            CONFIG.theme ===
            "사막"
        ) {

            ctx.fillStyle =
                "#a16207";


            ctx.fillRect(
                p.x - cell*.18,
                p.y - cell*.35,
                cell*.36,
                cell*.7
            );

        }


        else if (
            CONFIG.theme ===
            "얼음"
        ) {

            ctx.fillStyle =
                "#67e8f9";


            ctx.globalAlpha =
                .7;


            ctx.beginPath();


            ctx.moveTo(
                p.x,
                p.y - cell*.4
            );


            ctx.lineTo(
                p.x + cell*.35,
                p.y
            );


            ctx.lineTo(
                p.x,
                p.y + cell*.4
            );


            ctx.lineTo(
                p.x - cell*.35,
                p.y
            );


            ctx.closePath();


            ctx.fill();

        }


        else {

            ctx.fillStyle =
                "#64748b";


            ctx.beginPath();


            ctx.arc(
                p.x,
                p.y,
                cell*.33,
                0,
                Math.PI * 2
            );


            ctx.fill();

        }


        ctx.restore();

    }

}


// ============================================================
// GRID POSITION
// ============================================================

function gridToPixel(x,y) {

    const bw =
        GRID * cell;


    const bh =
        GRID * cell;


    const ox =
        (W - bw) / 2;


    const oy =
        (H - bh) / 2;


    return {

        x:
            ox +
            x * cell +
            cell / 2,

        y:
            oy +
            y * cell +
            cell / 2

    };

}


// ============================================================
// FOOD
// ============================================================

function drawFood() {

    const p =
        gridToPixel(
            foodPos.x,
            foodPos.y
        );


    const data =
        FOOD[CONFIG.food];


    ctx.save();


    const pulse =
        1 +
        Math.sin(
            performance.now() / 180
        ) * .08;


    ctx.shadowColor =
        THEME.accent;


    ctx.shadowBlur = 22;


    ctx.font =
        `${cell * .85 * pulse}px Arial`;


    ctx.textAlign =
        "center";


    ctx.textBaseline =
        "middle";


    ctx.fillText(
        data.emoji,
        p.x,
        p.y
    );


    ctx.restore();

}


// ============================================================
// COLOR
// ============================================================

function hexToRgb(hex) {

    const n =
        parseInt(
            hex.slice(1),
            16
        );


    return {

        r:
            (n >> 16) & 255,

        g:
            (n >> 8) & 255,

        b:
            n & 255

    };

}


function shade(
    hex,
    amount
) {

    const c =
        hexToRgb(hex);


    return `rgb(
        ${Math.max(
            0,
            Math.min(
                255,
                c.r + amount
            )
        )},
        ${Math.max(
            0,
            Math.min(
                255,
                c.g + amount
            )
        )},
        ${Math.max(
            0,
            Math.min(
                255,
                c.b + amount
            )
        )}
    )`;

}


// ============================================================
// SNAKE COLOR
// ============================================================

function segmentColor(i) {

    if (
        CONFIG.snakeStyle ===
        "무지개"
    ) {

        return `
            hsl(
                ${(i * 35 + score * 8) % 360},
                85%,
                58%
            )
        `;

    }


    if (
        CONFIG.snakeStyle ===
        "사이버"
    ) {

        return i % 2 === 0
            ? "#22d3ee"
            : "#8b5cf6";

    }


    if (
        CONFIG.snakeStyle ===
        "드래곤"
    ) {

        return i % 3 === 0
            ? shade(
                SNAKE_COLOR,
                30
            )
            : shade(
                SNAKE_COLOR,
                -10
            );

    }


    if (
        CONFIG.snakeStyle ===
        "코브라"
    ) {

        return i === 0
            ? shade(
                SNAKE_COLOR,
                30
            )
            : shade(
                SNAKE_COLOR,
                i % 2
                    ? -15
                    : 10
            );

    }


    if (
        CONFIG.snakeStyle ===
        "지렁이"
    ) {

        return i % 2 === 0
            ? shade(
                SNAKE_COLOR,
                15
            )
            : shade(
                SNAKE_COLOR,
                -8
            );

    }


    return i === 0
        ? shade(
            SNAKE_COLOR,
            25
        )
        : shade(
            SNAKE_COLOR,
            -Math.min(
                35,
                i * 2
            )
        );

}


// ============================================================
// DRAW SNAKE
// ============================================================

function drawSnake() {

    for (
        let i =
            snake.length - 1;
        i >= 0;
        i--
    ) {

        drawSegment(
            snake[i],
            i,
            false
        );

    }


    drawHead();

}


function drawSegment(
    part,
    index,
    ai
) {

    const p =
        gridToPixel(
            part.x,
            part.y
        );


    let radius =
        cell * .38;


    if (
        CONFIG.snakeStyle ===
        "지렁이"
    ) {

        radius =
            cell * .42;

    }


    if (
        CONFIG.snakeStyle ===
        "드래곤"
    ) {

        radius =
            cell * .39;

    }


    if (
        CONFIG.snakeStyle ===
        "사이버"
    ) {

        radius =
            cell * .35;

    }


    const color =
        ai
            ? (
                index % 2
                    ? "#ef4444"
                    : "#fb7185"
            )
            : segmentColor(index);


    ctx.save();


    if (
        CONFIG.snakeStyle ===
        "사이버"
        &&
        !ai
    ) {

        ctx.shadowColor =
            color;


        ctx.shadowBlur =
            16;

    }


    const gradient =
        ctx.createRadialGradient(
            p.x - radius*.35,
            p.y - radius*.4,
            1,
            p.x,
            p.y,
            radius
        );


    gradient.addColorStop(
        0,
        shade(color,35)
    );


    gradient.addColorStop(
        1,
        color
    );


    ctx.fillStyle =
        gradient;


    ctx.beginPath();


    ctx.arc(
        p.x,
        p.y,
        radius,
        0,
        Math.PI * 2
    );


    ctx.fill();


    if (
        CONFIG.snakeStyle ===
        "코브라"
        &&
        !ai
    ) {

        ctx.strokeStyle =
            "rgba(0,0,0,.28)";


        ctx.lineWidth = 2;


        ctx.beginPath();


        ctx.arc(
            p.x,
            p.y,
            radius * .7,
            0,
            Math.PI * 2
        );


        ctx.stroke();

    }


    if (
        CONFIG.snakeStyle ===
        "사이버"
        &&
        !ai
    ) {

        ctx.strokeStyle =
            "#67e8f9";


        ctx.lineWidth = 1;


        ctx.beginPath();


        ctx.moveTo(
            p.x - radius*.5,
            p.y
        );


        ctx.lineTo(
            p.x + radius*.5,
            p.y
        );


        ctx.moveTo(
            p.x,
            p.y - radius*.5
        );


        ctx.lineTo(
            p.x,
            p.y + radius*.5
        );


        ctx.stroke();

    }


    if (
        CONFIG.snakeStyle ===
        "드래곤"
        &&
        !ai
    ) {

        ctx.fillStyle =
            "#fbbf24";


        ctx.beginPath();


        ctx.arc(
            p.x,
            p.y,
            radius*.13,
            0,
            Math.PI * 2
        );


        ctx.fill();

    }


    ctx.fillStyle =
        "rgba(255,255,255,.14)";


    ctx.beginPath();


    ctx.arc(
        p.x - radius*.3,
        p.y - radius*.3,
        radius*.23,
        0,
        Math.PI * 2
    );


    ctx.fill();


    ctx.restore();

}


// ============================================================
// HEAD
// ============================================================

function drawHead() {

    const h =
        snake[0];


    const p =
        gridToPixel(
            h.x,
            h.y
        );


    let r =
        cell * .46;


    if (
        CONFIG.snakeStyle ===
        "지렁이"
    ) {

        r =
            cell * .44;

    }


    if (
        CONFIG.snakeStyle ===
        "코브라"
    ) {

        r =
            cell * .52;

    }


    if (
        CONFIG.snakeStyle ===
        "드래곤"
    ) {

        r =
            cell * .49;

    }


    ctx.save();


    if (
        CONFIG.snakeStyle ===
        "사이버"
    ) {

        ctx.shadowColor =
            "#22d3ee";


        ctx.shadowBlur =
            25;

    }


    const g =
        ctx.createRadialGradient(
            p.x-r*.3,
            p.y-r*.4,
            1,
            p.x,
            p.y,
            r
        );


    g.addColorStop(
        0,
        shade(
            SNAKE_COLOR,
            45
        )
    );


    g.addColorStop(
        1,
        SNAKE_COLOR
    );


    ctx.fillStyle = g;


    ctx.beginPath();


    ctx.arc(
        p.x,
        p.y,
        r,
        0,
        Math.PI * 2
    );


    ctx.fill();


    if (
        CONFIG.snakeStyle ===
        "드래곤"
        ||
        (
            CONFIG.evolution &&
            evolutionStage >= 4
        )
    ) {

        ctx.fillStyle =
            "#f8fafc";


        drawHorn(
            p.x - r*.55,
            p.y - r*.65,
            -1
        );


        drawHorn(
            p.x + r*.55,
            p.y - r*.65,
            1
        );

    }


    if (
        CONFIG.snakeStyle ===
        "코브라"
    ) {

        ctx.strokeStyle =
            shade(
                SNAKE_COLOR,
                35
            );


        ctx.lineWidth = 5;


        ctx.beginPath();


        ctx.arc(
            p.x,
            p.y,
            r * 1.2,
            Math.PI * .2,
            Math.PI * .8
        );


        ctx.stroke();

    }


    let ex = 0;

    let ey = 0;


    if (
        direction.x !== 0
    ) {

        ex =
            direction.x *
            r*.45;


        ey =
            r*.27;

    }

    else {

        ex =
            r*.27;


        ey =
            direction.y *
            r*.45;

    }


    drawEye(
        p.x + ex,
        p.y + ey
    );


    drawEye(
        p.x + ex,
        p.y - ey
    );


    if (
        CONFIG.snakeStyle !==
        "지렁이"
    ) {

        ctx.strokeStyle =
            "#fb7185";


        ctx.lineWidth = 1.8;


        ctx.lineCap =
            "round";


        const sx =
            p.x +
            direction.x *
            r*.75;


        const sy =
            p.y +
            direction.y *
            r*.75;


        const tx =
            p.x +
            direction.x *
            r*1.2;


        const ty =
            p.y +
            direction.y *
            r*1.2;


        ctx.beginPath();


        ctx.moveTo(
            sx,
            sy
        );


        ctx.lineTo(
            tx,
            ty
        );


        ctx.stroke();


        if (
            CONFIG.snakeStyle ===
            "코브라"
            ||
            CONFIG.snakeStyle ===
            "드래곤"
        ) {

            ctx.beginPath();


            ctx.moveTo(
                tx,
                ty
            );


            ctx.lineTo(
                tx -
                direction.y *
                cell*.15,

                ty +
                direction.x *
                cell*.15
            );


            ctx.stroke();

        }

    }


    if (
        CONFIG.evolution &&
        evolutionStage >= 3
    ) {

        ctx.fillStyle =
            evolutionStage >= 4
                ? "#fbbf24"
                : "#f97316";


        ctx.beginPath();


        ctx.arc(
            p.x -
            direction.y *
            r*.7,

            p.y +
            direction.x *
            r*.7,

            cell*.07,

            0,
            Math.PI * 2
        );


        ctx.fill();

    }


    ctx.restore();

}


function drawHorn(
    x,
    y,
    side
) {

    ctx.beginPath();


    ctx.moveTo(
        x,
        y
    );


    ctx.lineTo(
        x +
        side * cell*.18,
        y -
        cell*.25
    );


    ctx.lineTo(
        x +
        side * cell*.12,
        y +
        cell*.02
    );


    ctx.closePath();


    ctx.fill();

}


function drawEye(
    x,
    y
) {

    ctx.fillStyle =
        "#ffffff";


    ctx.beginPath();


    ctx.arc(
        x,
        y,
        cell*.105,
        0,
        Math.PI * 2
    );


    ctx.fill();


    ctx.fillStyle =
        "#111827";


    ctx.beginPath();


    ctx.arc(
        x +
        direction.x *
        cell*.025,

        y +
        direction.y *
        cell*.025,

        cell*.055,

        0,
        Math.PI * 2
    );


    ctx.fill();

}


// ============================================================
// AI DRAW
// ============================================================

function drawAI() {

    if (
        CONFIG.gameMode !==
        "AI 대결"
    ) {

        return;

    }


    for (
        let i =
            aiSnake.length - 1;
        i >= 0;
        i--
    ) {

        drawSegment(
            aiSnake[i],
            i,
            true
        );

    }


    if (
        aiSnake.length === 0
    ) {

        return;

    }


    const h =
        aiSnake[0];


    const p =
        gridToPixel(
            h.x,
            h.y
        );


    ctx.save();


    ctx.fillStyle =
        "#f87171";


    ctx.font =
        `${cell*.32}px Arial`;


    ctx.textAlign =
        "center";


    ctx.fillText(
        "AI",
        p.x,
        p.y - cell*.62
    );


    ctx.restore();

}


// ============================================================
// PARTICLES
// ============================================================

function drawParticles() {

    for (
        const p of particles
    ) {

        const pos =
            gridToPixel(
                p.x,
                p.y
            );


        ctx.save();


        ctx.globalAlpha =
            Math.max(
                0,
                p.life
            );


        ctx.fillStyle =
            p.color;


        ctx.beginPath();


        ctx.arc(
            pos.x,
            pos.y,
            cell*.07,
            0,
            Math.PI * 2
        );


        ctx.fill();


        ctx.restore();

    }

}


// ============================================================
// DRAW
// ============================================================

function draw() {

    resize();

    drawBackground();

    drawObstacles();

    drawFood();

    drawAI();

    drawSnake();

    drawParticles();

}


// ============================================================
// LOOP
// ============================================================

function loop(timestamp) {

    if (!running) {

        draw();

        return;

    }


    const baseSpeed =
        SPEEDS[
            CONFIG.difficulty
        ];


    let currentSpeed =
        baseSpeed;


    if (
        Date.now() <
        speedUntil
    ) {

        if (
            CONFIG.food ===
            "햄버거"
        ) {

            currentSpeed *=
                1.45;

        }

        else {

            currentSpeed *=
                .62;

        }

    }

    else {

        powerText.textContent =
            "특별 효과 없음";

    }


    if (
        !paused &&
        timestamp -
        lastTime >=
        currentSpeed
    ) {

        updatePlayer();


        if (
            CONFIG.gameMode ===
            "AI 대결"
        ) {

            const aiSpeed =
                AI_SPEEDS[
                    CONFIG.aiLevel
                ];


            if (
                timestamp -
                lastTime >=
                aiSpeed
            ) {

                updateAI();

            }


            checkAIFinish();

        }


        updateParticles();


        lastTime =
            timestamp;

    }


    draw();


    requestAnimationFrame(
        loop
    );

}


// ============================================================
// START
// ============================================================

init();


// 음악이 켜져 있는 경우
// 첫 번째 사용자 입력에서 음악 시작

if (
    CONFIG.musicEnabled
) {

    const startAudioOnInteraction =
        () => {

            if (!musicPlaying) {

                startMusic();

            }

            document.removeEventListener(
                "keydown",
                startAudioOnInteraction
            );

            canvas.removeEventListener(
                "pointerdown",
                startAudioOnInteraction
            );

        };


    document.addEventListener(
        "keydown",
        startAudioOnInteraction,
        {
            once: true
        }
    );


    canvas.addEventListener(
        "pointerdown",
        startAudioOnInteraction,
        {
            once: true
        }
    );

}

</script>

</body>
</html>
"""


# ============================================================
# INSERT CONFIG
# ============================================================

html = html.replace(
    "__CONFIG__",
    config_json
)


# ============================================================
# STREAMLIT COMPONENT
# ============================================================

components.html(
    html,
    height=790,
    scrolling=False
)
