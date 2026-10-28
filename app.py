import streamlit as st
import streamlit.components.v1 as components

# =====================================================================
# 머신러닝 플레이그라운드 - 메인 파일 (멀티페이지 진입점)
#  - 이 파일이 배포에 쓰는 "메인 파일"입니다. 파일 이름은 지금 쓰는 이름 그대로 두세요.
#  - 맨 아래 st.navigation 에 등록된 순서대로 사이드바 메뉴가 만들어집니다.
#      1단계: 선형 회귀  → 이 파일 안의 linear_regression_page()
#      2단계: 다중 회귀  → 같은 폴더의 multiple_regression.py
#      3단계: 분류       → 같은 폴더의 classification.py (KNN·로지스틱 회귀·결정트리 탭)
#  - streamlit 1.36 이상에서 동작합니다. (1.56 이상이면 화면 높이가 내용에 맞춰 자동 조절됨)
# =====================================================================

# 1. 모든 페이지에 공통으로 적용되는 기본 설정 (와이드 모드, 사이드바 펼침)
#    탭 제목과 아이콘은 아래 st.Page 의 title, icon 으로 페이지마다 따로 정해집니다.
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

# 스트림릿 기본 여백(Padding) 제거 스타일 적용 (모든 페이지 공통)
#  - 위쪽만 3.75rem(60px)을 남깁니다. 0으로 두면 스트림릿 상단 메뉴 막대(흰색, 높이 60px)가
#    교구의 보라색 제목 영역을 가립니다. (상단 막대는 사이드바 열기 버튼이 있어서 숨기지 않음)
st.markdown("""
    <style>
        .block-container {
            padding-top: 3.75rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
        iframe {
            border: none;
        }
    </style>
""", unsafe_allow_html=True)

# 2. 1단계: 선형 회귀 페이지의 HTML/JS 코드
# ※ r"""...""" (raw 문자열): 좌표 입력 처리에 쓰는 JS 정규식의 역슬래시(\d, \s 등)가
#    파이썬 문자열 처리 과정에서 바뀌지 않도록 r 접두사를 붙였습니다.
LINEAR_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>머신러닝 플레이그라운드 - 선형 회귀</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts: Noto Sans KR -->
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            font-family: 'Noto Sans KR', sans-serif;
            background-color: #f8fafc;
        }
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
        canvas {
            touch-action: none;
        }
        kbd {
            font-family: ui-monospace, monospace;
            font-size: 10px;
            padding: 1px 5px;
            border: 1px solid #cbd5e1;
            border-bottom-width: 2px;
            border-radius: 4px;
            background: #f8fafc;
            color: #475569;
        }
    </style>
</head>
<body class="text-slate-800 antialiased flex flex-col justify-between">

    <header class="bg-indigo-600 text-white shadow-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex flex-wrap justify-between items-center gap-2">
            <div class="flex items-center space-x-3">
                <div class="bg-white/20 p-2 rounded-lg backdrop-blur-sm">
                    <i class="fa-solid fa-brain text-2xl text-yellow-300"></i>
                </div>
                <div>
                    <h1 class="text-xl font-bold tracking-tight">머신러닝 플레이그라운드</h1>
                    <p class="text-xs text-indigo-200">고등학생을 위한 인공지능 기초 인터랙티브 실습</p>
                </div>
            </div>
            
            <nav class="flex space-x-1 bg-indigo-700/50 p-1 rounded-xl text-xs sm:text-sm">
                <span class="px-3 py-1.5 rounded-lg font-semibold bg-white text-indigo-700 shadow-sm">
                    <i class="fa-solid fa-chart-line mr-1"></i> 1단계: 선형 회귀
                </span>
                <span class="px-3 py-1.5 rounded-lg text-indigo-100 cursor-help" title="왼쪽 사이드바에서 '2단계: 다중 회귀'를 눌러 이동하세요">
                    <i class="fa-solid fa-cube mr-1"></i> 2단계: 다중 회귀
                </span>
                <span class="px-3 py-1.5 rounded-lg text-indigo-100 cursor-help" title="왼쪽 사이드바에서 '3단계: 분류'를 눌러 이동하세요">
                    <i class="fa-solid fa-shapes mr-1"></i> 3단계: 분류
                </span>
            </nav>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-grow w-full">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

            <!-- Left Panel: Interactive Canvas (7 cols) -->
            <section class="lg:col-span-7 flex flex-col gap-4">
                <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 flex flex-wrap justify-between items-center gap-3">
                    <div class="flex items-center space-x-2">
                        <span class="font-bold text-slate-700 text-sm sm:text-base"><i class="fa-solid fa-hand-pointer text-indigo-500 mr-1"></i> 모드:</span>
                        <div class="inline-flex rounded-lg p-1 bg-slate-100 border border-slate-200 text-xs sm:text-sm">
                            <button id="mode-add-btn" class="px-3 py-1.5 rounded-md font-semibold bg-indigo-600 text-white transition shadow-sm flex items-center gap-1">
                                <i class="fa-solid fa-circle-plus"></i> 점 찍기
                            </button>
                            <button id="mode-user-line-btn" class="px-3 py-1.5 rounded-md font-semibold text-slate-600 hover:text-amber-600 transition flex items-center gap-1">
                                <i class="fa-solid fa-pen-ruler"></i> 내 직선 그리기
                            </button>
                            <button id="mode-predict-btn" class="px-3 py-1.5 rounded-md font-semibold text-slate-600 hover:text-indigo-600 transition flex items-center gap-1">
                                <i class="fa-solid fa-magnifying-glass-chart"></i> 예측하기
                            </button>
                            <button id="mode-erase-btn" class="px-3 py-1.5 rounded-md font-semibold text-slate-600 hover:text-red-600 transition flex items-center gap-1">
                                <i class="fa-solid fa-eraser"></i> 삭제하기
                            </button>
                        </div>
                    </div>

                    <button id="clear-btn" class="px-3 py-1.5 bg-slate-100 hover:bg-red-50 text-slate-600 hover:text-red-600 font-medium rounded-lg text-xs sm:text-sm transition flex items-center gap-1 border border-slate-200">
                        <i class="fa-solid fa-trash-can"></i> 전체 삭제
                    </button>
                </div>

                <div class="bg-white rounded-2xl p-4 shadow-sm border border-slate-200 flex flex-col items-center relative overflow-hidden">
                    <div id="predict-badge" class="hidden absolute top-6 left-6 bg-indigo-900/90 text-white px-3 py-1.5 rounded-lg text-xs font-mono shadow-lg backdrop-blur-md z-10 pointer-events-none">
                        입력 X: <span id="pred-x-val" class="font-bold text-yellow-300">0</span> ➔ 예측 Y: <span id="pred-y-val" class="font-bold text-green-300">0</span>
                    </div>

                    <div class="w-full aspect-square max-h-[500px] relative rounded-xl border border-slate-200 bg-slate-900 overflow-hidden cursor-crosshair shadow-inner">
                        <canvas id="regression-canvas" class="w-full h-full block"></canvas>
                    </div>

                    <div class="w-full flex justify-between items-center mt-3 px-1 text-xs sm:text-sm text-slate-600">
                        <label class="flex items-center space-x-2 cursor-pointer select-none">
                            <input type="checkbox" id="toggle-residuals" checked class="w-4 h-4 text-indigo-600 rounded border-slate-300 focus:ring-indigo-500">
                            <span>오차 선(Residuals) 표시</span>
                        </label>
                        <span class="text-slate-400"><i class="fa-solid fa-circle-info mr-1"></i>캔버스를 클릭하여 파란색 점을 생성하세요</span>
                    </div>
                </div>

                <!-- [추가] 좌표 직접 입력 패널 -->
                <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
                    <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1">
                        <i class="fa-solid fa-keyboard text-indigo-500"></i> 좌표 직접 입력하기
                    </h3>
                    <div class="flex flex-col sm:flex-row gap-2">
                        <textarea id="coord-input" rows="2" spellcheck="false" autocomplete="off"
                            class="flex-grow px-3 py-2 rounded-xl border border-slate-300 bg-slate-50 font-mono text-sm resize-y focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:bg-white"
                            placeholder="예) (20,30) (40,50) (60,70)   또는   20,30   또는   20 30"></textarea>
                        <button id="coord-add-btn" class="sm:w-28 px-3 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow-sm transition flex items-center justify-center gap-1.5 text-xs sm:text-sm">
                            <i class="fa-solid fa-circle-plus"></i> 점 추가
                        </button>
                    </div>
                    <p class="text-[11px] text-slate-500 mt-2 leading-relaxed break-keep">
                        <i class="fa-solid fa-circle-info mr-1 text-slate-400"></i>x, y는 각각 <strong class="text-indigo-600">0~100</strong> 사이의 수만 입력할 수 있어요.
                        여러 점은 띄어쓰기나 줄바꿈으로 구분합니다.<br>
                        <span class="whitespace-nowrap"><kbd>Enter</kbd> 추가</span> ·
                        <span class="whitespace-nowrap"><kbd>Shift</kbd>+<kbd>Enter</kbd> 줄바꿈</span>
                    </p>
                    <div id="coord-feedback" class="hidden mt-2 p-2.5 rounded-xl text-xs border space-y-1"></div>
                </div>

                <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
                    <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1">
                        <i class="fa-solid fa-folder-open text-indigo-500"></i> 예시 데이터 세트 불러오기
                    </h3>
                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
                        <button id="preset-positive" class="p-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 rounded-xl font-medium text-xs sm:text-sm transition text-center border border-indigo-100">
                            📈 양의 상관관계
                        </button>
                        <button id="preset-negative" class="p-2 bg-rose-50 hover:bg-rose-100 text-rose-700 rounded-xl font-medium text-xs sm:text-sm transition text-center border border-rose-100">
                            📉 음의 상관관계
                        </button>
                        <button id="preset-noisy" class="p-2 bg-amber-50 hover:bg-amber-100 text-amber-700 rounded-xl font-medium text-xs sm:text-sm transition text-center border border-amber-100">
                            💥 큰 노이즈
                        </button>
                        <button id="preset-outlier" class="p-2 bg-purple-50 hover:bg-purple-100 text-purple-700 rounded-xl font-medium text-xs sm:text-sm transition text-center border border-purple-100">
                            ⚠️ 이상치 포함
                        </button>
                    </div>
                </div>
            </section>

            <!-- Right Panel: Hyperparameters & Metrics (5 cols) -->
            <section class="lg:col-span-5 flex flex-col gap-4">
                <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
                    <div class="flex flex-wrap justify-between items-center mb-3 gap-2">
                        <h2 class="text-base font-bold text-slate-800 flex items-center">
                            <i class="fa-solid fa-sliders text-indigo-600 mr-2"></i>학습 제어 및 하이퍼파라미터
                        </h2>
                        <div class="flex items-center gap-1.5 flex-wrap">
                            <span id="cumulative-tag" class="text-xs px-2.5 py-1 rounded-full bg-indigo-50 text-indigo-700 font-bold font-mono border border-indigo-200">
                                누적: <strong id="cumulative-val" class="text-indigo-900">0</strong> 에포크
                            </span>
                            <span id="status-tag" class="text-xs px-2.5 py-1 rounded-full bg-slate-100 text-slate-600 font-semibold">대기 중</span>
                        </div>
                    </div>

                    <div class="grid grid-cols-3 gap-2 mb-5">
                        <button id="train-btn" class="col-span-1 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2.5 px-2 rounded-xl shadow-md hover:shadow-lg transition flex items-center justify-center gap-1.5 text-xs sm:text-sm">
                            <i class="fa-solid fa-play"></i> 학습 시작
                        </button>
                        <button id="step-btn" class="col-span-1 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold py-2.5 px-2 rounded-xl border border-indigo-200 transition flex items-center justify-center gap-1.5 text-xs sm:text-sm">
                            <i class="fa-solid fa-forward-step"></i> +1 에포크
                        </button>
                        <button id="reset-model-btn" class="col-span-1 bg-slate-100 hover:bg-amber-50 text-slate-700 hover:text-amber-700 font-bold py-2.5 px-2 rounded-xl border border-slate-200 transition flex items-center justify-center gap-1.5 text-xs sm:text-sm">
                            <i class="fa-solid fa-rotate-left"></i> 모델 초기화
                        </button>
                    </div>

                    <div class="space-y-4">
                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <label for="epochs-slider" class="text-xs sm:text-sm font-semibold text-slate-700">학습 횟수 (Epochs)</label>
                                <span id="epochs-val" class="font-mono font-bold text-indigo-600 text-sm bg-indigo-50 px-2 py-0.5 rounded">100회</span>
                            </div>
                            <input type="range" id="epochs-slider" min="10" max="1000" step="10" value="100" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600">
                        </div>

                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <label for="lr-slider" class="text-xs sm:text-sm font-semibold text-slate-700">학습률 (Learning Rate, α)</label>
                                <span id="lr-val" class="font-mono font-bold text-indigo-600 text-sm bg-indigo-50 px-2 py-0.5 rounded">0.05</span>
                            </div>
                            <input type="range" id="lr-slider" min="0.005" max="0.2" step="0.005" value="0.05" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600">
                        </div>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
                    <h2 class="text-base font-bold text-slate-800 mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-square-poll-vertical text-emerald-600"></i> 실시간 AI 평가 지표
                    </h2>

                    <div class="grid grid-cols-2 gap-3">
                        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl">
                            <span class="text-xs text-slate-500 font-semibold block mb-0.5">기울기 (Weight, w)</span>
                            <span id="metric-w" class="text-xl font-extrabold text-indigo-600 font-mono">0.0000</span>
                        </div>

                        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl">
                            <span class="text-xs text-slate-500 font-semibold block mb-0.5">절편 (Bias, b)</span>
                            <span id="metric-b" class="text-xl font-extrabold text-indigo-600 font-mono">0.0000</span>
                        </div>

                        <div class="p-3 bg-amber-50/70 border border-amber-200 rounded-xl">
                            <span class="text-xs text-amber-700 font-semibold block mb-0.5">AI 평균 제곱 오차 (MSE)</span>
                            <span id="metric-mse" class="text-xl font-extrabold text-amber-800 font-mono">0.0000</span>
                        </div>

                        <div class="p-3 bg-emerald-50/70 border border-emerald-200 rounded-xl">
                            <span class="text-xs text-emerald-700 font-semibold block mb-0.5">결정계수 (R²)</span>
                            <span id="metric-r2" class="text-xl font-extrabold text-emerald-800 font-mono">0.0000</span>
                        </div>
                    </div>

                    <div class="mt-4 p-3 bg-slate-900 text-white rounded-xl font-mono text-center text-sm shadow-inner">
                        <span class="text-slate-400 text-xs block mb-1">현재 AI 방정식 (y = wx + b)</span>
                        <span id="equation-display" class="text-yellow-300 font-bold">y = 0.00x + 0.00</span>
                    </div>
                </div>

                <div id="user-line-card" class="bg-amber-50/80 border border-amber-200 p-5 rounded-2xl shadow-sm">
                    <div class="flex justify-between items-center mb-2">
                        <h3 class="text-sm font-bold text-amber-900 flex items-center gap-1.5">
                            <i class="fa-solid fa-pen-ruler text-amber-600"></i> 내가 직접 그린 직선 (Human vs AI)
                        </h3>
                        <span class="text-xs bg-amber-200/80 text-amber-900 font-bold px-2 py-0.5 rounded-full">비교 모드</span>
                    </div>
                    <p class="text-xs text-amber-800 mb-3">'내 직선 그리기' 모드에서 <span class="font-bold text-amber-700">주황색 조종점(A, B)</span>을 드래그해보세요!</p>

                    <div class="grid grid-cols-2 gap-2 text-xs mb-3">
                        <div class="bg-white p-2.5 rounded-xl border border-amber-200">
                            <span class="text-slate-500 font-medium block">내 직선 방정식:</span>
                            <span id="user-equation" class="font-bold text-amber-700 font-mono text-sm block mt-0.5">y = 0.00x + 0.00</span>
                        </div>
                        <div class="bg-white p-2.5 rounded-xl border border-amber-200">
                            <span class="text-slate-500 font-medium block">내 오차 (User MSE):</span>
                            <span id="user-mse" class="font-bold text-amber-600 font-mono text-sm block mt-0.5">0.00</span>
                        </div>
                    </div>

                    <div id="mse-comparison-badge" class="p-2.5 bg-white rounded-xl border border-amber-200 text-xs text-center font-medium text-slate-700">
                        점이 있을 때 조종점을 움직여 AI 모델보다 MSE를 낮춰보세요!
                    </div>
                </div>

            </section>
        </div>
    </main>

    <div id="toast-container" class="fixed bottom-5 right-5 z-50 flex flex-col gap-2"></div>

    <footer class="bg-slate-100 border-t border-slate-200 py-3 text-center text-xs text-slate-500">
        머신러닝 인터랙티브 교구 | HTML5 Canvas & Pure Vanilla JavaScript
    </footer>

    <script>
        const canvas = document.getElementById('regression-canvas');
        const ctx = canvas.getContext('2d');

        const state = {
            points: [],
            w: 0,
            b: 0,
            mode: 'add',
            showResiduals: true,
            epochs: 100,
            totalEpochs: 0,
            lr: 0.05,
            isTraining: false,
            hoverPredictX: null,
            hoverPredictY: null,
            userLine: { p1: { x: 10, y: 20 }, p2: { x: 90, y: 80 } },
            draggingHandle: null
        };

        const elements = {
            modeAddBtn: document.getElementById('mode-add-btn'),
            modeUserLineBtn: document.getElementById('mode-user-line-btn'),
            modePredictBtn: document.getElementById('mode-predict-btn'),
            modeEraseBtn: document.getElementById('mode-erase-btn'),
            clearBtn: document.getElementById('clear-btn'),
            trainBtn: document.getElementById('train-btn'),
            stepBtn: document.getElementById('step-btn'),
            resetModelBtn: document.getElementById('reset-model-btn'),
            cumulativeVal: document.getElementById('cumulative-val'),
            epochsSlider: document.getElementById('epochs-slider'),
            epochsVal: document.getElementById('epochs-val'),
            lrSlider: document.getElementById('lr-slider'),
            lrVal: document.getElementById('lr-val'),
            toggleResiduals: document.getElementById('toggle-residuals'),
            metricW: document.getElementById('metric-w'),
            metricB: document.getElementById('metric-b'),
            metricMSE: document.getElementById('metric-mse'),
            metricR2: document.getElementById('metric-r2'),
            equationDisplay: document.getElementById('equation-display'),
            userEquation: document.getElementById('user-equation'),
            userMse: document.getElementById('user-mse'),
            mseComparisonBadge: document.getElementById('mse-comparison-badge'),
            statusTag: document.getElementById('status-tag'),
            predictBadge: document.getElementById('predict-badge'),
            predXVal: document.getElementById('pred-x-val'),
            predYVal: document.getElementById('pred-y-val'),
            presetPositive: document.getElementById('preset-positive'),
            presetNegative: document.getElementById('preset-negative'),
            presetNoisy: document.getElementById('preset-noisy'),
            presetOutlier: document.getElementById('preset-outlier'),
            // [추가] 좌표 직접 입력 요소
            coordInput: document.getElementById('coord-input'),
            coordAddBtn: document.getElementById('coord-add-btn'),
            coordFeedback: document.getElementById('coord-feedback')
        };

        function resizeCanvas() {
            const rect = canvas.parentElement.getBoundingClientRect();
            const dpr = window.devicePixelRatio || 1;
            canvas.width = rect.width * dpr;
            canvas.height = rect.height * dpr;
            render();
        }

        const PADDING = 45;

        function pixelToData(px, py) {
            const scale = canvas.width / 400;
            const pad = PADDING * scale;
            const plotW = canvas.width - pad * 2;
            const plotH = canvas.height - pad * 2;

            let x = ((px - pad) / plotW) * 100;
            let y = (1 - (py - pad) / plotH) * 100;

            return {
                x: Math.max(0, Math.min(100, x)),
                y: Math.max(0, Math.min(100, y))
            };
        }

        function dataToPixel(x, y) {
            const scale = canvas.width / 400;
            const pad = PADDING * scale;
            const plotW = canvas.width - pad * 2;
            const plotH = canvas.height - pad * 2;

            return {
                x: pad + (x / 100) * plotW,
                y: pad + (1 - y / 100) * plotH
            };
        }

        function drawGrid() {
            const scale = canvas.width / 400;
            const pad = PADDING * scale;
            const w = canvas.width;
            const h = canvas.height;

            ctx.strokeStyle = '#1e293b';
            ctx.lineWidth = 1 * scale;
            ctx.fillStyle = '#64748b';
            ctx.font = `${Math.max(10, 11 * scale)}px sans-serif`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';

            for (let i = 0; i <= 100; i += 20) {
                const pt = dataToPixel(i, i);
                
                ctx.beginPath();
                ctx.moveTo(pt.x, pad);
                ctx.lineTo(pt.x, h - pad);
                ctx.stroke();

                ctx.beginPath();
                ctx.moveTo(pad, pt.y);
                ctx.lineTo(w - pad, pt.y);
                ctx.stroke();

                ctx.fillText(i.toString(), pt.x, h - pad + 15 * scale);
                ctx.fillText(i.toString(), pad - 15 * scale, pt.y);
            }

            ctx.strokeStyle = '#475569';
            ctx.lineWidth = 2 * scale;
            ctx.strokeRect(pad, pad, w - pad * 2, h - pad * 2);
        }

        function drawPoints() {
            const scale = Math.max(1, canvas.width / 400);
            const radius = 7.5 * scale;

            state.points.forEach((p) => {
                const pixel = dataToPixel(p.x, p.y);

                ctx.beginPath();
                ctx.arc(pixel.x, pixel.y, radius * 1.8, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(59, 130, 246, 0.25)';
                ctx.fill();

                ctx.beginPath();
                ctx.arc(pixel.x, pixel.y, radius, 0, Math.PI * 2);
                ctx.fillStyle = '#2563eb';
                ctx.fill();

                ctx.lineWidth = 2.5 * scale;
                ctx.strokeStyle = '#ffffff';
                ctx.stroke();
            });
        }

        function drawRegressionLine() {
            if (state.points.length === 0) return;
            const scale = Math.max(1, canvas.width / 400);
            
            const p1 = dataToPixel(0, state.b);
            const p2 = dataToPixel(100, state.w * 100 + state.b);

            ctx.strokeStyle = '#818cf8';
            ctx.lineWidth = 3.5 * scale;
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
        }

        function drawResiduals() {
            if (state.points.length === 0) return;
            const scale = Math.max(1, canvas.width / 400);

            ctx.strokeStyle = '#f43f5e';
            ctx.lineWidth = 1.5 * scale;
            ctx.setLineDash([4 * scale, 3 * scale]);

            state.points.forEach(p => {
                const yHat = predict(p.x);
                const ptData = dataToPixel(p.x, p.y);
                const ptPred = dataToPixel(p.x, yHat);

                ctx.beginPath();
                ctx.moveTo(ptData.x, ptData.y);
                ctx.lineTo(ptPred.x, ptPred.y);
                ctx.stroke();
            });

            ctx.setLineDash([]);
        }

        function getUserLineParams() {
            const dx = state.userLine.p2.x - state.userLine.p1.x;
            const dy = state.userLine.p2.y - state.userLine.p1.y;
            const w = dx === 0 ? 0 : dy / dx;
            const b = state.userLine.p1.y - w * state.userLine.p1.x;
            return { w, b };
        }

        function drawUserLine() {
            const scale = Math.max(1, canvas.width / 400);
            const { w, b } = getUserLineParams();
            const p1Pixel = dataToPixel(0, b);
            const p2Pixel = dataToPixel(100, w * 100 + b);

            ctx.strokeStyle = '#f59e0b';
            ctx.lineWidth = 3 * scale;
            ctx.setLineDash([6 * scale, 4 * scale]);
            ctx.beginPath();
            ctx.moveTo(p1Pixel.x, p1Pixel.y);
            ctx.lineTo(p2Pixel.x, p2Pixel.y);
            ctx.stroke();
            ctx.setLineDash([]);

            const h1 = dataToPixel(state.userLine.p1.x, state.userLine.p1.y);
            const h2 = dataToPixel(state.userLine.p2.x, state.userLine.p2.y);
            drawHandle(h1, "A", scale);
            drawHandle(h2, "B", scale);
        }

        function drawHandle(pixel, label, scale) {
            ctx.fillStyle = '#f97316';
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 3 * scale;

            ctx.beginPath();
            ctx.arc(pixel.x, pixel.y, 11 * scale, 0, Math.PI * 2);
            ctx.fill();
            ctx.stroke();

            ctx.fillStyle = '#ffffff';
            ctx.font = `bold ${Math.max(10, 11 * scale)}px sans-serif`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(label, pixel.x, pixel.y);
        }

        function drawPredictionVisuals() {
            const scale = Math.max(1, canvas.width / 400);
            const x = state.hoverPredictX;
            const y = state.hoverPredictY;
            const pt = dataToPixel(x, y);

            ctx.strokeStyle = '#facc15';
            ctx.lineWidth = 2 * scale;
            ctx.setLineDash([4 * scale, 4 * scale]);

            ctx.beginPath();
            ctx.moveTo(pt.x, dataToPixel(x, 0).y);
            ctx.lineTo(pt.x, pt.y);
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(dataToPixel(0, y).x, pt.y);
            ctx.lineTo(pt.x, pt.y);
            ctx.stroke();
            ctx.setLineDash([]);

            ctx.fillStyle = '#facc15';
            ctx.beginPath();
            ctx.arc(pt.x, pt.y, 6 * scale, 0, Math.PI * 2);
            ctx.fill();
        }

        function render() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            drawGrid();

            if (state.mode === 'userLine') {
                drawUserLine();
            }

            if (state.showResiduals && state.points.length > 0) {
                drawResiduals();
            }

            if (state.points.length > 0) {
                drawRegressionLine();
            }

            drawPoints();

            if (state.mode === 'predict' && state.hoverPredictX !== null) {
                drawPredictionVisuals();
            }
        }

        function predict(x) {
            return state.w * x + state.b;
        }

        function calculateMSE() {
            if (state.points.length === 0) return 0;
            let sumError = 0;
            state.points.forEach(p => {
                const yHat = predict(p.x);
                sumError += Math.pow(p.y - yHat, 2);
            });
            return sumError / state.points.length;
        }

        function calculateUserMSE() {
            if (state.points.length === 0) return 0;
            const { w, b } = getUserLineParams();
            let sumError = 0;
            state.points.forEach(p => {
                const yHat = w * p.x + b;
                sumError += Math.pow(p.y - yHat, 2);
            });
            return sumError / state.points.length;
        }

        function calculateR2() {
            if (state.points.length <= 1) return 0;
            const yMean = state.points.reduce((sum, p) => sum + p.y, 0) / state.points.length;
            
            let sst = 0;
            let sse = 0;

            state.points.forEach(p => {
                const yHat = predict(p.x);
                sst += Math.pow(p.y - yMean, 2);
                sse += Math.pow(p.y - yHat, 2);
            });

            if (sst === 0) return 1;
            const r2 = 1 - (sse / sst);
            return Math.max(0, r2);
        }

        function updateMetricsUI() {
            const mse = calculateMSE();
            const r2 = calculateR2();

            elements.metricW.textContent = state.w.toFixed(4);
            elements.metricB.textContent = state.b.toFixed(4);
            elements.metricMSE.textContent = mse.toFixed(2);
            elements.metricR2.textContent = r2.toFixed(4);

            const sign = state.b >= 0 ? '+' : '-';
            elements.equationDisplay.textContent = `y = ${state.w.toFixed(2)}x ${sign} ${Math.abs(state.b).toFixed(2)}`;

            elements.cumulativeVal.textContent = state.totalEpochs;

            const userParams = getUserLineParams();
            const userMse = calculateUserMSE();
            const uSign = userParams.b >= 0 ? '+' : '-';
            elements.userEquation.textContent = `y = ${userParams.w.toFixed(2)}x ${uSign} ${Math.abs(userParams.b).toFixed(2)}`;
            elements.userMse.textContent = userMse.toFixed(2);

            if (state.points.length === 0) {
                elements.mseComparisonBadge.className = "p-2.5 bg-white rounded-xl border border-amber-200 text-xs text-center font-medium text-slate-700";
                elements.mseComparisonBadge.innerHTML = "점이 있을 때 조종점을 움직여 AI 모델보다 MSE를 낮춰보세요!";
            } else {
                const diff = userMse - mse;
                if (Math.abs(diff) < 1.0) {
                    elements.mseComparisonBadge.className = "p-2.5 bg-emerald-50 text-emerald-800 rounded-xl border border-emerald-200 text-xs text-center font-bold";
                    elements.mseComparisonBadge.innerHTML = `🎉 대단합니다! AI 모델과 오차(MSE)가 거의 동일합니다!`;
                } else if (diff > 0) {
                    elements.mseComparisonBadge.className = "p-2.5 bg-amber-50 text-amber-800 rounded-xl border border-amber-200 text-xs text-center font-medium";
                    elements.mseComparisonBadge.innerHTML = `💡 AI 모델의 MSE가 내 직선보다 <strong class="text-indigo-700">${diff.toFixed(2)}</strong> 더 작습니다.`;
                } else {
                    elements.mseComparisonBadge.className = "p-2.5 bg-indigo-50 text-indigo-800 rounded-xl border border-indigo-200 text-xs text-center font-bold";
                    elements.mseComparisonBadge.innerHTML = `🏆 놀라워요! AI 학습 전보다 오차가 더 낮습니다! AI를 학습시켜 보세요.`;
                }
            }
        }

        function stepGradientDescent() {
            if (state.points.length === 0) return;

            const N = state.points.length;
            let dW = 0;
            let dB = 0;

            state.points.forEach(p => {
                const xNorm = p.x / 100;
                const yNorm = p.y / 100;
                const wNorm = state.w;
                const bNorm = state.b / 100;

                const predNorm = wNorm * xNorm + bNorm;
                const err = predNorm - yNorm;

                dW += (2 / N) * err * xNorm;
                dB += (2 / N) * err;
            });

            state.w -= state.lr * dW;
            const bNormNew = (state.b / 100) - state.lr * dB;
            state.b = bNormNew * 100;

            state.totalEpochs += 1;
            updateMetricsUI();
        }

        function startTraining() {
            if (state.points.length === 0) {
                showToast("데이터 점을 먼저 캔버스에 찍어주세요!", "warning");
                return;
            }
            if (state.isTraining) return;

            state.isTraining = true;
            elements.statusTag.textContent = "학습 중...";
            elements.statusTag.className = "text-xs px-2.5 py-1 rounded-full bg-indigo-600 text-white font-semibold animate-pulse";

            let trainedInThisRun = 0;

            function runStep() {
                if (!state.isTraining || trainedInThisRun >= state.epochs) {
                    state.isTraining = false;
                    elements.statusTag.textContent = "학습 완료";
                    elements.statusTag.className = "text-xs px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-700 font-bold";
                    return;
                }

                stepGradientDescent();
                render();
                trainedInThisRun++;

                requestAnimationFrame(runStep);
            }

            requestAnimationFrame(runStep);
        }

        function resetModel(resetWeightsOnly = true) {
            state.w = 0;
            state.b = 0;
            state.totalEpochs = 0;
            state.isTraining = false;
            elements.statusTag.textContent = "대기 중";
            elements.statusTag.className = "text-xs px-2.5 py-1 rounded-full bg-slate-100 text-slate-600 font-semibold";
            updateMetricsUI();
            render();
            if (resetWeightsOnly) {
                showToast("가중치 및 누적 에포크가 초기화되었습니다.");
            }
        }

        function loadPreset(type) {
            state.points = [];
            resetModel(true);
            hideCoordFeedback();

            if (type === 'positive') {
                for (let i = 10; i <= 90; i += 8) {
                    const noise = (Math.random() - 0.5) * 15;
                    state.points.push({ x: i, y: Math.max(5, Math.min(95, 0.8 * i + 10 + noise)) });
                }
            } else if (type === 'negative') {
                for (let i = 10; i <= 90; i += 8) {
                    const noise = (Math.random() - 0.5) * 15;
                    state.points.push({ x: i, y: Math.max(5, Math.min(95, -0.7 * i + 85 + noise)) });
                }
            } else if (type === 'noisy') {
                for (let i = 10; i <= 90; i += 6) {
                    const noise = (Math.random() - 0.5) * 45;
                    state.points.push({ x: i, y: Math.max(5, Math.min(95, 0.5 * i + 25 + noise)) });
                }
            } else if (type === 'outlier') {
                for (let i = 10; i <= 80; i += 10) {
                    const noise = (Math.random() - 0.5) * 10;
                    state.points.push({ x: i, y: Math.max(5, Math.min(95, 0.6 * i + 15 + noise)) });
                }
                state.points.push({ x: 25, y: 90 });
                state.points.push({ x: 85, y: 15 });
            }

            updateMetricsUI();
            render();
            showToast("예시 데이터 세트가로드되었습니다.");
        }

        function showToast(msg, type = "info") {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            
            const bgColor = type === 'warning' ? 'bg-amber-600' : 'bg-slate-800';
            toast.className = `${bgColor} text-white text-xs px-4 py-2.5 rounded-xl shadow-xl transition-all duration-300 transform translate-y-2 opacity-0 flex items-center gap-2`;
            toast.innerHTML = `<i class="fa-solid fa-circle-info text-yellow-400"></i> ${msg}`;
            
            container.appendChild(toast);
            
            setTimeout(() => {
                toast.classList.remove('translate-y-2', 'opacity-0');
            }, 10);

            setTimeout(() => {
                toast.classList.add('opacity-0');
                setTimeout(() => toast.remove(), 300);
            }, 2500);
        }

        // ================================================================
        // [추가] 키보드로 좌표 직접 입력하기
        //  - 허용 형식: (20,30) / 20,30 / 20 30, 여러 점은 띄어쓰기·줄바꿈으로 구분
        //  - x, y 모두 0~100 범위만 허용 (범위 밖은 추가하지 않고 안내)
        // ================================================================
        const COORD_MIN = 0;
        const COORD_MAX = 100;
        const NUMBER_PATTERN = /^[-+]?(?:\d+\.?\d*|\.\d+)$/;

        // 입력 문자열 → { points: [{x, y, raw}], invalid: [원문 조각] }
        function parseCoordinateText(text) {
            const normalized = text
                .replace(/（/g, '(')
                .replace(/）/g, ')')
                .replace(/，/g, ',');

            const points = [];
            const invalid = [];
            let pending = null; // 괄호 없이 입력된 x값이 y값을 기다리는 중

            const flushPending = () => {
                if (pending) {
                    invalid.push(pending.raw);
                    pending = null;
                }
            };

            // ① (괄호 묶음)  ② 괄호·쉼표·공백이 아닌 덩어리  ③ 짝이 맞지 않는 괄호
            const tokenPattern = /\(([^()]*)\)|[^\s,;()]+|[()]/g;
            let match;
            while ((match = tokenPattern.exec(normalized)) !== null) {
                const token = match[0];

                if (match[1] !== undefined) {
                    // 괄호 묶음: 안에 숫자가 정확히 2개여야 함
                    flushPending();
                    const parts = match[1].split(/[\s,;]+/).filter(Boolean);
                    if (parts.length === 2 && NUMBER_PATTERN.test(parts[0]) && NUMBER_PATTERN.test(parts[1])) {
                        points.push({ x: parseFloat(parts[0]), y: parseFloat(parts[1]), raw: token });
                    } else {
                        invalid.push(token);
                    }
                } else if (token === '(' || token === ')') {
                    // 짝이 맞지 않는 괄호는 무시 (예: "(20,30" → 20,30으로 처리)
                    continue;
                } else if (NUMBER_PATTERN.test(token)) {
                    // 괄호 없는 숫자: 두 개씩 짝지어 (x, y)로 처리
                    if (pending) {
                        points.push({ x: pending.value, y: parseFloat(token), raw: `${pending.raw},${token}` });
                        pending = null;
                    } else {
                        pending = { value: parseFloat(token), raw: token };
                    }
                } else {
                    flushPending();
                    invalid.push(token);
                }
            }
            flushPending();

            return { points, invalid };
        }

        function isInCoordRange(v) {
            return v >= COORD_MIN && v <= COORD_MAX;
        }

        function formatCoord(p) {
            const f = (v) => String(Math.round(v * 100) / 100);
            return `(${f(p.x)}, ${f(p.y)})`;
        }

        function summarizeList(items, max = 6) {
            const shown = items.slice(0, max).join(', ');
            return items.length > max ? `${shown} 외 ${items.length - max}개` : shown;
        }

        function escapeHtml(str) {
            return String(str).replace(/[&<>"']/g, (c) => ({
                '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
            }[c]));
        }

        function hideCoordFeedback() {
            if (!elements.coordFeedback) return;
            elements.coordFeedback.classList.add('hidden');
            elements.coordFeedback.innerHTML = '';
        }

        function renderCoordFeedback(accepted, outOfRange, invalid) {
            const lines = [];

            if (accepted.length > 0) {
                lines.push(`✅ <strong>${accepted.length}개</strong>의 점을 추가했어요: <span class="font-mono">${escapeHtml(summarizeList(accepted.map(formatCoord)))}</span>`);
            }
            if (outOfRange.length > 0) {
                lines.push(`⚠️ x, y는 <strong>${COORD_MIN}~${COORD_MAX}</strong> 사이여야 해서 추가하지 않았어요: <span class="font-mono">${escapeHtml(summarizeList(outOfRange.map(formatCoord)))}</span>`);
            }
            if (invalid.length > 0) {
                lines.push(`❌ 좌표로 읽을 수 없는 입력이에요: <span class="font-mono">${escapeHtml(summarizeList(invalid))}</span> <span class="opacity-75">(x와 y 두 수를 짝지어 입력하세요. 예: (20,30))</span>`);
            }

            const hasProblem = outOfRange.length > 0 || invalid.length > 0;
            if (hasProblem) {
                lines.push(`<span class="opacity-75">추가하지 못한 입력은 입력창에 남겨 두었어요. 고친 뒤 다시 추가해 보세요.</span>`);
            }

            let tone;
            if (!hasProblem) tone = 'bg-emerald-50 text-emerald-800 border-emerald-200';
            else if (accepted.length === 0) tone = 'bg-rose-50 text-rose-800 border-rose-200';
            else tone = 'bg-amber-50 text-amber-800 border-amber-200';

            elements.coordFeedback.className = `mt-2 p-2.5 rounded-xl text-xs border space-y-1 ${tone}`;
            elements.coordFeedback.innerHTML = lines.map(l => `<div>${l}</div>`).join('');
        }

        function addPointsFromInput() {
            const text = elements.coordInput.value;
            if (!text.trim()) {
                showToast("좌표를 입력해 주세요. 예) (20,30)", "warning");
                elements.coordInput.focus();
                return;
            }

            const { points, invalid } = parseCoordinateText(text);
            if (points.length === 0 && invalid.length === 0) {
                invalid.push(text.trim());
            }

            const accepted = [];
            const outOfRange = [];
            points.forEach(p => {
                if (isInCoordRange(p.x) && isInCoordRange(p.y)) accepted.push(p);
                else outOfRange.push(p);
            });

            if (accepted.length > 0) {
                const wasEmpty = state.points.length === 0;
                accepted.forEach(p => state.points.push({ x: p.x, y: p.y }));
                // 마우스로 첫 점을 찍을 때와 동일하게 절편 시작값을 첫 점의 y로 설정
                if (wasEmpty) state.b = accepted[0].y;
                updateMetricsUI();
                render();
            }

            renderCoordFeedback(accepted, outOfRange, invalid);

            // 추가하지 못한 입력만 입력창에 남겨 수정할 수 있게 함
            const leftovers = [...outOfRange.map(p => p.raw), ...invalid];
            elements.coordInput.value = leftovers.join(' ');
            elements.coordInput.focus();

            if (outOfRange.length === 0 && invalid.length === 0) {
                showToast(`${accepted.length}개의 점을 추가했어요.`);
            } else if (accepted.length > 0) {
                showToast("일부 좌표만 추가했어요. 입력창 아래 안내를 확인하세요.", "warning");
            } else {
                showToast("좌표를 추가하지 못했어요. 입력창 아래 안내를 확인하세요.", "warning");
            }
        }

        function setMode(newMode) {
            state.mode = newMode;
            
            [elements.modeAddBtn, elements.modeUserLineBtn, elements.modePredictBtn, elements.modeEraseBtn].forEach(btn => {
                btn.className = "px-3 py-1.5 rounded-md font-semibold text-slate-600 hover:text-indigo-600 transition flex items-center gap-1";
            });

            if (newMode === 'add') {
                elements.modeAddBtn.className = "px-3 py-1.5 rounded-md font-semibold bg-indigo-600 text-white transition shadow-sm flex items-center gap-1";
                elements.predictBadge.classList.add('hidden');
            } else if (newMode === 'userLine') {
                elements.modeUserLineBtn.className = "px-3 py-1.5 rounded-md font-semibold bg-amber-500 text-white transition shadow-sm flex items-center gap-1";
                elements.predictBadge.classList.add('hidden');
                showToast("조종점(A, B)을 드래그하여 직관적인 최적의 선을 맞추어보세요!");
            } else if (newMode === 'predict') {
                elements.modePredictBtn.className = "px-3 py-1.5 rounded-md font-semibold bg-indigo-600 text-white transition shadow-sm flex items-center gap-1";
                showToast("캔버스를 마우스로 가리켜 예측 X, Y 값을 확인하세요!");
            } else if (newMode === 'erase') {
                elements.modeEraseBtn.className = "px-3 py-1.5 rounded-md font-semibold bg-red-600 text-white transition shadow-sm flex items-center gap-1";
                elements.predictBadge.classList.add('hidden');
            }
            render();
        }

        function handleCanvasPointer(e, type) {
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;

            const px = (e.clientX - rect.left) * scaleX;
            const py = (e.clientY - rect.top) * scaleY;

            const dataPt = pixelToData(px, py);

            if (state.mode === 'userLine') {
                const scale = Math.max(1, canvas.width / 400);
                const p1Pixel = dataToPixel(state.userLine.p1.x, state.userLine.p1.y);
                const p2Pixel = dataToPixel(state.userLine.p2.x, state.userLine.p2.y);

                const dist1 = Math.hypot(px - p1Pixel.x, py - p1Pixel.y);
                const dist2 = Math.hypot(px - p2Pixel.x, py - p2Pixel.y);
                const threshold = 30 * scale;

                if (type === 'down') {
                    if (dist1 < threshold) state.draggingHandle = 'p1';
                    else if (dist2 < threshold) state.draggingHandle = 'p2';
                } else if (type === 'move' && state.draggingHandle) {
                    if (state.draggingHandle === 'p1') state.userLine.p1 = dataPt;
                    else if (state.draggingHandle === 'p2') state.userLine.p2 = dataPt;
                    updateMetricsUI();
                    render();
                } else if (type === 'up') {
                    state.draggingHandle = null;
                }
                return;
            }

            if (type !== 'down' && type !== 'move') return;

            if (state.mode === 'add' && type === 'down') {
                state.points.push(dataPt);
                if (state.points.length === 1) state.b = dataPt.y;
                updateMetricsUI();
                render();
            } else if (state.mode === 'erase' && type === 'down') {
                state.points = state.points.filter(p => Math.hypot(p.x - dataPt.x, p.y - dataPt.y) > 6);
                updateMetricsUI();
                render();
            } else if (state.mode === 'predict') {
                state.hoverPredictX = dataPt.x;
                state.hoverPredictY = predict(dataPt.x);
                
                elements.predXVal.textContent = dataPt.x.toFixed(1);
                elements.predYVal.textContent = state.hoverPredictY.toFixed(1);
                elements.predictBadge.classList.remove('hidden');

                render();
            }
        }

        window.addEventListener('resize', resizeCanvas);

        canvas.addEventListener('pointerdown', (e) => {
            handleCanvasPointer(e, 'down');
            const moveHandler = (me) => handleCanvasPointer(me, 'move');
            const upHandler = (ue) => {
                handleCanvasPointer(ue, 'up');
                canvas.removeEventListener('pointermove', moveHandler);
                canvas.removeEventListener('pointerup', upHandler);
            };
            canvas.addEventListener('pointermove', moveHandler);
            canvas.addEventListener('pointerup', upHandler);
        });

        elements.modeAddBtn.addEventListener('click', () => setMode('add'));
        elements.modeUserLineBtn.addEventListener('click', () => setMode('userLine'));
        elements.modePredictBtn.addEventListener('click', () => setMode('predict'));
        elements.modeEraseBtn.addEventListener('click', () => setMode('erase'));

        elements.clearBtn.addEventListener('click', () => {
            state.points = [];
            resetModel(false);
            state.hoverPredictX = null;
            elements.predictBadge.classList.add('hidden');
            hideCoordFeedback();
            updateMetricsUI();
            render();
            showToast("모든 데이터 점이 삭제되었습니다.");
        });

        elements.toggleResiduals.addEventListener('change', (e) => {
            state.showResiduals = e.target.checked;
            render();
        });

        elements.epochsSlider.addEventListener('input', (e) => {
            state.epochs = parseInt(e.target.value);
            elements.epochsVal.textContent = `${state.epochs}회`;
        });

        elements.lrSlider.addEventListener('input', (e) => {
            state.lr = parseFloat(e.target.value);
            elements.lrVal.textContent = state.lr.toFixed(3);
        });

        elements.trainBtn.addEventListener('click', startTraining);
        elements.stepBtn.addEventListener('click', () => {
            if (state.points.length === 0) return showToast("데이터 점을 먼저 캔버스에 찍어주세요!", "warning");
            stepGradientDescent();
            render();
        });
        elements.resetModelBtn.addEventListener('click', () => resetModel(true));

        elements.presetPositive.addEventListener('click', () => loadPreset('positive'));
        elements.presetNegative.addEventListener('click', () => loadPreset('negative'));
        elements.presetNoisy.addEventListener('click', () => loadPreset('noisy'));
        elements.presetOutlier.addEventListener('click', () => loadPreset('outlier'));

        // [추가] 좌표 입력: 버튼 클릭 또는 Enter(한글 입력 조합 중 제외)로 추가, Shift+Enter는 줄바꿈
        elements.coordAddBtn.addEventListener('click', addPointsFromInput);
        elements.coordInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey && !e.isComposing && e.keyCode !== 229) {
                e.preventDefault();
                addPointsFromInput();
            }
        });

        window.onload = function() {
            resizeCanvas();
            loadPreset('positive');
        };
    </script>
</body>
</html>
"""

# 3. HTML을 화면에 배치하는 공통 함수
#  - streamlit 1.56 이상: st.iframe 사용 (내용 높이에 맞춰 화면 높이가 자동으로 조절됨)
#  - 그보다 낮은 버전: 예전 방식인 components.html 사용 (고정 높이 + 스크롤)
#    ※ components.html 은 최신 버전에서 "곧 제거될 예정"이라는 경고가 나와서 st.iframe 으로 옮겼습니다.
def show_html(html, fallback_height):
    if hasattr(st, "iframe"):
        st.iframe(html, height="content")
    else:
        components.html(html, height=fallback_height, scrolling=True)


# 4. 1단계: 선형 회귀 페이지
def linear_regression_page():
    show_html(LINEAR_HTML, fallback_height=1250)


# 5. 사이드바 페이지 목록 (위에서부터 순서대로 표시됨)
pg = st.navigation([
    st.Page(linear_regression_page, title="1단계: 선형 회귀", icon="📈", default=True),
    st.Page("multiple_regression.py", title="2단계: 다중 회귀", icon="🧊", url_path="multiple_regression"),
    st.Page("classification.py", title="3단계: 분류", icon="🐧", url_path="classification"),
])
pg.run()
