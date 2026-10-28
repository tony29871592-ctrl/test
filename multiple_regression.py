import streamlit as st
import streamlit.components.v1 as components

# =====================================================================
# 2단계: 다중 회귀 (3차원 그래프)
#  - 메인 파일의 st.navigation 에 등록된 페이지입니다. 메인 파일과 같은 폴더에 두세요.
#  - 와이드 레이아웃, 사이드바 펼침, 여백 제거 스타일은 메인 파일에서 공통으로 적용됩니다.
#  - 3D 그래프는 Plotly.js(3D 전용 번들)를 CDN으로 불러옵니다. 파이썬 패키지 설치는 필요 없습니다.
#  - 축 이름·범위를 바꾸려면 아래 JS의 AXES 설정만 고치면 됩니다.
# =====================================================================

# r"""...""" (raw 문자열): JS 정규식의 역슬래시(\d, \s 등)가 파이썬에서 바뀌지 않도록 함
html_code = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>머신러닝 플레이그라운드 - 다중 회귀</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts: Noto Sans KR -->
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Plotly.js 3D 전용 번들 (3차원 산점도·평면) -->
    <script src="https://cdn.jsdelivr.net/npm/plotly.js-gl3d-dist-min@3.7.0/plotly-gl3d.min.js"></script>
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
                <span class="px-3 py-1.5 rounded-lg text-indigo-100 cursor-help" title="왼쪽 사이드바에서 '1단계: 선형 회귀'를 눌러 이동하세요">
                    <i class="fa-solid fa-chart-line mr-1"></i> 1단계: 선형 회귀
                </span>
                <span class="px-3 py-1.5 rounded-lg font-semibold bg-white text-indigo-700 shadow-sm">
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

            <!-- Left Panel: 3D Graph (7 cols) -->
            <section class="lg:col-span-7 flex flex-col gap-4">
                <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 flex flex-wrap justify-between items-center gap-3">
                    <div class="flex items-center gap-2">
                        <span class="font-bold text-slate-700 text-sm sm:text-base"><i class="fa-solid fa-cube text-indigo-500 mr-1"></i> 3차원 데이터 공간</span>
                        <span id="point-count" class="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 font-mono border border-slate-200">점 0개</span>
                    </div>
                    <div class="flex flex-wrap items-center gap-2">
                        <button id="reset-view-btn" class="px-3 py-1.5 bg-slate-100 hover:bg-indigo-50 text-slate-600 hover:text-indigo-700 font-medium rounded-lg text-xs sm:text-sm transition flex items-center gap-1 border border-slate-200">
                            <i class="fa-solid fa-camera-rotate"></i> 시점 초기화
                        </button>
                        <button id="undo-btn" class="px-3 py-1.5 bg-slate-100 hover:bg-amber-50 text-slate-600 hover:text-amber-700 font-medium rounded-lg text-xs sm:text-sm transition flex items-center gap-1 border border-slate-200">
                            <i class="fa-solid fa-delete-left"></i> 마지막 점 삭제
                        </button>
                        <button id="clear-btn" class="px-3 py-1.5 bg-slate-100 hover:bg-red-50 text-slate-600 hover:text-red-600 font-medium rounded-lg text-xs sm:text-sm transition flex items-center gap-1 border border-slate-200">
                            <i class="fa-solid fa-trash-can"></i> 전체 삭제
                        </button>
                    </div>
                </div>

                <div class="bg-white rounded-2xl p-4 shadow-sm border border-slate-200 flex flex-col">
                    <div class="relative w-full rounded-xl border border-slate-200 bg-slate-900 overflow-hidden shadow-inner">
                        <div id="plot3d" class="w-full h-[380px] sm:h-[460px] lg:h-[520px]"></div>
                        <div id="plot-fallback" class="hidden absolute inset-0 flex items-center justify-center p-6 text-center text-sm text-slate-300 leading-relaxed">
                            3D 그래프를 불러오지 못했어요.<br>인터넷 연결을 확인하거나, 학교 방화벽에서 cdn.jsdelivr.net 접속이 막혀 있는지 확인해 주세요.
                        </div>
                    </div>

                    <div class="w-full flex flex-wrap items-center gap-x-4 gap-y-1 mt-3 px-1 text-xs text-slate-600">
                        <span class="flex items-center gap-1.5"><span class="inline-block w-3 h-3 rounded-full bg-blue-500 ring-2 ring-white shadow"></span> 학생 데이터</span>
                        <span class="flex items-center gap-1.5"><span class="inline-block w-4 h-3 rounded-sm bg-indigo-400/70"></span> AI 회귀 평면</span>
                        <span class="flex items-center gap-1.5"><span class="inline-block w-4 border-t-2 border-dashed border-rose-500"></span> 오차</span>
                    </div>

                    <div class="w-full flex flex-wrap justify-between items-center gap-2 mt-2 px-1 text-xs sm:text-sm text-slate-600">
                        <label class="flex items-center space-x-2 cursor-pointer select-none">
                            <input type="checkbox" id="toggle-residuals" checked class="w-4 h-4 text-indigo-600 rounded border-slate-300 focus:ring-indigo-500">
                            <span>오차 선(Residuals) 표시</span>
                        </label>
                        <span class="text-slate-400 text-xs"><i class="fa-solid fa-computer-mouse mr-1"></i>드래그: 회전 · 휠: 확대/축소 · 점에 올리면 값 표시</span>
                    </div>
                </div>

                <!-- 좌표 직접 입력 패널 -->
                <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
                    <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1">
                        <i class="fa-solid fa-keyboard text-indigo-500"></i> 데이터 직접 입력하기 (공부 시간, 수면 시간, 점수)
                    </h3>
                    <div class="flex flex-col sm:flex-row gap-2">
                        <textarea id="coord-input" rows="2" spellcheck="false" autocomplete="off"
                            class="flex-grow px-3 py-2 rounded-xl border border-slate-300 bg-slate-50 font-mono text-sm resize-y focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:bg-white"
                            placeholder="예) (5,7,80) (2,6,55)   또는   5,7,80   또는   5 7 80"></textarea>
                        <button id="coord-add-btn" class="sm:w-28 px-3 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow-sm transition flex items-center justify-center gap-1.5 text-xs sm:text-sm">
                            <i class="fa-solid fa-circle-plus"></i> 점 추가
                        </button>
                    </div>
                    <p id="coord-hint" class="text-[11px] text-slate-500 mt-2 leading-relaxed break-keep"></p>
                    <div id="coord-feedback" class="hidden mt-2 p-2.5 rounded-xl text-xs border space-y-1"></div>
                </div>

                <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
                    <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1">
                        <i class="fa-solid fa-folder-open text-indigo-500"></i> 예시 데이터 세트 불러오기
                    </h3>
                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
                        <button id="preset-basic" class="p-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 rounded-xl font-medium text-xs sm:text-sm transition text-center border border-indigo-100">
                            📈 기본 데이터
                        </button>
                        <button id="preset-nosleep" class="p-2 bg-rose-50 hover:bg-rose-100 text-rose-700 rounded-xl font-medium text-xs sm:text-sm transition text-center border border-rose-100">
                            😴 수면 영향 없음
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

            <!-- Right Panel: Training & Metrics (5 cols) -->
            <section class="lg:col-span-5 flex flex-col gap-4">
                <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
                    <div class="flex flex-wrap justify-between items-center mb-3 gap-2">
                        <h2 class="text-base font-bold text-slate-800 flex items-center">
                            <i class="fa-solid fa-sliders text-indigo-600 mr-2"></i>학습 제어 및 하이퍼파라미터
                        </h2>
                        <div class="flex items-center gap-1.5 flex-wrap">
                            <span class="text-xs px-2.5 py-1 rounded-full bg-indigo-50 text-indigo-700 font-bold font-mono border border-indigo-200">
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
                                <span id="epochs-val" class="font-mono font-bold text-indigo-600 text-sm bg-indigo-50 px-2 py-0.5 rounded">300회</span>
                            </div>
                            <input type="range" id="epochs-slider" min="10" max="2000" step="10" value="300" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600">
                        </div>

                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <label for="lr-slider" class="text-xs sm:text-sm font-semibold text-slate-700">학습률 (Learning Rate, α)</label>
                                <span id="lr-val" class="font-mono font-bold text-indigo-600 text-sm bg-indigo-50 px-2 py-0.5 rounded">0.30</span>
                            </div>
                            <input type="range" id="lr-slider" min="0.01" max="1" step="0.01" value="0.3" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600">
                            <p class="text-[11px] text-slate-400 mt-1">학습률이 너무 크면 오차가 줄지 않고 오히려 커질 수 있어요.</p>
                        </div>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
                    <h2 class="text-base font-bold text-slate-800 mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-square-poll-vertical text-emerald-600"></i> 실시간 AI 평가 지표
                    </h2>

                    <div class="grid grid-cols-3 gap-2 mb-2">
                        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl">
                            <span class="text-[11px] text-slate-500 font-semibold block mb-0.5 break-keep">w₁ (공부 시간)</span>
                            <span id="metric-w1" class="text-lg font-extrabold text-indigo-600 font-mono">0.00</span>
                        </div>
                        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl">
                            <span class="text-[11px] text-slate-500 font-semibold block mb-0.5 break-keep">w₂ (수면 시간)</span>
                            <span id="metric-w2" class="text-lg font-extrabold text-indigo-600 font-mono">0.00</span>
                        </div>
                        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl">
                            <span class="text-[11px] text-slate-500 font-semibold block mb-0.5 break-keep">b (절편)</span>
                            <span id="metric-b" class="text-lg font-extrabold text-indigo-600 font-mono">0.00</span>
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-2">
                        <div class="p-3 bg-amber-50/70 border border-amber-200 rounded-xl">
                            <span class="text-xs text-amber-700 font-semibold block mb-0.5">AI 평균 제곱 오차 (MSE)</span>
                            <span id="metric-mse" class="text-xl font-extrabold text-amber-800 font-mono">0.00</span>
                        </div>
                        <div class="p-3 bg-emerald-50/70 border border-emerald-200 rounded-xl">
                            <span class="text-xs text-emerald-700 font-semibold block mb-0.5">결정계수 (R²)</span>
                            <span id="metric-r2" class="text-xl font-extrabold text-emerald-800 font-mono">0.0000</span>
                        </div>
                    </div>

                    <div class="mt-4 p-3 bg-slate-900 text-white rounded-xl font-mono text-center shadow-inner">
                        <span class="text-slate-400 text-xs block mb-1">현재 AI 방정식 (y = w₁x₁ + w₂x₂ + b)</span>
                        <span id="equation-display" class="text-yellow-300 font-bold text-xs sm:text-sm break-words">점수 = 0.00 × 공부 + 0.00 × 수면 + 0.00</span>
                    </div>

                    <div id="coef-explain" class="mt-3 p-3 bg-indigo-50/60 border border-indigo-100 rounded-xl text-xs text-indigo-900 leading-relaxed break-keep space-y-1"></div>
                </div>

                <div class="bg-amber-50/80 border border-amber-200 p-5 rounded-2xl shadow-sm">
                    <h3 class="text-sm font-bold text-amber-900 flex items-center gap-1.5 mb-2">
                        <i class="fa-solid fa-lightbulb text-amber-600"></i> 선형 회귀와 무엇이 다를까?
                    </h3>
                    <div class="space-y-2 text-xs text-amber-900 break-keep">
                        <div class="bg-white p-2.5 rounded-xl border border-amber-200">
                            <span class="font-bold">입력 1개</span> · 점수 = w × 공부 + b
                            <span class="block text-amber-700 mt-0.5">→ 2차원 평면 위의 <strong>직선</strong></span>
                        </div>
                        <div class="bg-white p-2.5 rounded-xl border border-amber-200">
                            <span class="font-bold">입력 2개</span> · 점수 = w₁ × 공부 + w₂ × 수면 + b
                            <span class="block text-amber-700 mt-0.5">→ 3차원 공간 속의 <strong>평면</strong></span>
                        </div>
                        <p class="text-amber-800">학습 방법(경사하강법)과 평가 방법(MSE, R²)은 선형 회귀와 같아요. 바뀌는 것은 찾아야 할 값의 개수입니다.</p>
                    </div>
                </div>

            </section>
        </div>
    </main>

    <div id="toast-container" class="fixed bottom-5 right-5 z-50 flex flex-col gap-2"></div>

    <footer class="bg-slate-100 border-t border-slate-200 py-3 text-center text-xs text-slate-500">
        머신러닝 인터랙티브 교구 | HTML5 & Plotly.js 3D
    </footer>

    <script>
        // ================================================================
        // 축 설정: 이름·단위·범위를 바꾸려면 여기만 고치면 됩니다. (최솟값은 0 기준)
        // ================================================================
        const AXES = {
            x1: { name: '공부 시간', short: '공부', unit: '시간', max: 12, dtick: 2 },
            x2: { name: '수면 시간', short: '수면', unit: '시간', max: 12, dtick: 2 },
            y:  { name: '시험 점수', short: '점수', unit: '점',  max: 100, dtick: 20 }
        };
        const DEFAULT_CAMERA = {
            eye: { x: 1.6, y: -1.6, z: 0.75 },
            center: { x: 0, y: 0, z: -0.12 },
            up: { x: 0, y: 0, z: 1 }
        };
        const PLANE_GRID = 7;            // 평면을 그릴 격자 수 (0, 2, 4, ..., 12)
        const DIVERGE_MSE = 1e7;         // 이 값을 넘으면 '발산'으로 판단

        // 학습은 0~1로 정규화한 값으로 진행하고(a1, a2, c), 화면에는 실제 단위의 w₁, w₂, b로 보여줍니다.
        const state = {
            points: [],
            a1: 0,
            a2: 0,
            c: 0,
            showResiduals: true,
            epochs: 300,
            totalEpochs: 0,
            lr: 0.3,
            isTraining: false,
            diverged: false
        };

        const $ = (id) => document.getElementById(id);
        const elements = {
            plot: $('plot3d'),
            plotFallback: $('plot-fallback'),
            pointCount: $('point-count'),
            resetViewBtn: $('reset-view-btn'),
            undoBtn: $('undo-btn'),
            clearBtn: $('clear-btn'),
            toggleResiduals: $('toggle-residuals'),
            coordInput: $('coord-input'),
            coordAddBtn: $('coord-add-btn'),
            coordHint: $('coord-hint'),
            coordFeedback: $('coord-feedback'),
            trainBtn: $('train-btn'),
            stepBtn: $('step-btn'),
            resetModelBtn: $('reset-model-btn'),
            cumulativeVal: $('cumulative-val'),
            statusTag: $('status-tag'),
            epochsSlider: $('epochs-slider'),
            epochsVal: $('epochs-val'),
            lrSlider: $('lr-slider'),
            lrVal: $('lr-val'),
            metricW1: $('metric-w1'),
            metricW2: $('metric-w2'),
            metricB: $('metric-b'),
            metricMSE: $('metric-mse'),
            metricR2: $('metric-r2'),
            equationDisplay: $('equation-display'),
            coefExplain: $('coef-explain')
        };

        // ---------------- 모델 ----------------
        function getParams() {
            return {
                w1: state.a1 * AXES.y.max / AXES.x1.max,
                w2: state.a2 * AXES.y.max / AXES.x2.max,
                b: state.c * AXES.y.max
            };
        }

        function predict(x1, x2) {
            const { w1, w2, b } = getParams();
            return w1 * x1 + w2 * x2 + b;
        }

        function calculateMSE() {
            if (state.points.length === 0) return 0;
            let sum = 0;
            state.points.forEach(p => { sum += Math.pow(p.y - predict(p.x1, p.x2), 2); });
            return sum / state.points.length;
        }

        function calculateR2() {
            if (state.points.length <= 1) return 0;
            const yMean = state.points.reduce((s, p) => s + p.y, 0) / state.points.length;
            let sst = 0, sse = 0;
            state.points.forEach(p => {
                sst += Math.pow(p.y - yMean, 2);
                sse += Math.pow(p.y - predict(p.x1, p.x2), 2);
            });
            if (sst === 0) return 1;
            return Math.max(0, 1 - sse / sst);
        }

        function stepGradientDescent() {
            const N = state.points.length;
            if (N === 0) return;
            let g1 = 0, g2 = 0, gc = 0;
            state.points.forEach(p => {
                const u1 = p.x1 / AXES.x1.max;
                const u2 = p.x2 / AXES.x2.max;
                const v = p.y / AXES.y.max;
                const err = state.a1 * u1 + state.a2 * u2 + state.c - v;
                g1 += (2 / N) * err * u1;
                g2 += (2 / N) * err * u2;
                gc += (2 / N) * err;
            });
            state.a1 -= state.lr * g1;
            state.a2 -= state.lr * g2;
            state.c -= state.lr * gc;
            state.totalEpochs += 1;
        }

        function checkDiverged() {
            const mse = calculateMSE();
            if (!Number.isFinite(mse) || mse > DIVERGE_MSE) {
                state.diverged = true;
                state.isTraining = false;
                setStatus('diverged');
                showToast("학습률이 너무 커서 오차가 계속 커졌어요(발산). '모델 초기화' 후 학습률을 낮춰 보세요.", "warning");
                return true;
            }
            return false;
        }

        // ---------------- 3D 그래프 ----------------
        function axisStyle(axis) {
            return {
                title: { text: `${axis.name} (${axis.unit})`, font: { size: 12, color: '#e2e8f0' } },
                range: [0, axis.max],
                autorange: false,
                dtick: axis.dtick,
                color: '#94a3b8',
                tickfont: { size: 10, color: '#94a3b8' },
                gridcolor: '#334155',
                zerolinecolor: '#64748b',
                showbackground: true,
                backgroundcolor: '#111c33',
                showspikes: false
            };
        }

        const plotLayout = {
            paper_bgcolor: '#0f172a',
            margin: { l: 0, r: 0, t: 0, b: 0 },
            showlegend: false,
            uirevision: 'keep-camera',
            font: { family: "'Noto Sans KR', sans-serif", color: '#cbd5e1' },
            hoverlabel: { bgcolor: '#1e1b4b', bordercolor: '#818cf8', font: { color: '#ffffff', size: 12 } },
            scene: {
                xaxis: axisStyle(AXES.x1),
                yaxis: axisStyle(AXES.x2),
                zaxis: axisStyle(AXES.y),
                aspectmode: 'cube',
                dragmode: 'turntable',
                camera: DEFAULT_CAMERA
            }
        };

        const plotConfig = { responsive: true, displaylogo: false, displayModeBar: false, scrollZoom: true };

        function gridValues(axis) {
            return Array.from({ length: PLANE_GRID }, (_, i) => i * axis.max / (PLANE_GRID - 1));
        }

        function buildTraces() {
            const pts = state.points;
            const hasPoints = pts.length > 0;
            const traces = [];

            // 0) 학생 데이터 점
            traces.push({
                type: 'scatter3d',
                mode: 'markers',
                x: pts.map(p => p.x1),
                y: pts.map(p => p.x2),
                z: pts.map(p => p.y),
                marker: { size: 5.5, color: '#3b82f6', line: { color: '#ffffff', width: 1.5 } },
                hovertemplate: `${AXES.x1.short} %{x:.1f}${AXES.x1.unit}<br>${AXES.x2.short} %{y:.1f}${AXES.x2.unit}<br>${AXES.y.short} %{z:.1f}${AXES.y.unit}<extra></extra>`
            });

            // 1) 오차 선: 각 점에서 평면까지 수직으로 잇는 선
            const rx = [], ry = [], rz = [];
            const planeOk = hasPoints && !state.diverged;
            if (state.showResiduals && planeOk) {
                pts.forEach(p => {
                    rx.push(p.x1, p.x1, null);
                    ry.push(p.x2, p.x2, null);
                    rz.push(p.y, predict(p.x1, p.x2), null);
                });
            }
            traces.push({
                type: 'scatter3d',
                mode: 'lines',
                x: rx, y: ry, z: rz,
                line: { color: '#f43f5e', width: 4, dash: 'dash' },
                connectgaps: false,
                hoverinfo: 'skip'
            });

            // 2) AI 회귀 평면
            const gx = gridValues(AXES.x1);
            const gy = gridValues(AXES.x2);
            const gz = gy.map(v2 => gx.map(v1 => predict(v1, v2)));
            traces.push({
                type: 'surface',
                x: gx, y: gy, z: gz,
                visible: planeOk,
                colorscale: [[0, '#818cf8'], [1, '#818cf8']],
                showscale: false,
                opacity: 0.55,
                hoverinfo: 'skip',
                lighting: { ambient: 0.85, diffuse: 0.35, specular: 0.05, roughness: 0.9 },
                contours: {
                    x: { show: true, color: 'rgba(255,255,255,0.35)', width: 1, highlight: false },
                    y: { show: true, color: 'rgba(255,255,255,0.35)', width: 1, highlight: false },
                    z: { show: false, highlight: false }
                }
            });

            return traces;
        }

        function renderPlot() {
            if (!window.Plotly) return;
            Plotly.react(elements.plot, buildTraces(), plotLayout, plotConfig);
        }

        function resetView() {
            if (!window.Plotly) return;
            Plotly.relayout(elements.plot, { 'scene.camera': JSON.parse(JSON.stringify(DEFAULT_CAMERA)) });
        }

        // ---------------- 화면 갱신 ----------------
        const fmt2 = (v) => (Number.isFinite(v) ? v.toFixed(2) : '발산');

        function signed(v) {
            return `${v >= 0 ? '+' : '-'} ${Math.abs(v).toFixed(2)}`;
        }

        function setStatus(kind) {
            const map = {
                idle:     ['대기 중', 'bg-slate-100 text-slate-600 font-semibold'],
                training: ['학습 중...', 'bg-indigo-600 text-white font-semibold animate-pulse'],
                done:     ['학습 완료', 'bg-emerald-100 text-emerald-700 font-bold'],
                diverged: ['발산!', 'bg-rose-100 text-rose-700 font-bold']
            };
            const [text, cls] = map[kind];
            elements.statusTag.textContent = text;
            elements.statusTag.className = `text-xs px-2.5 py-1 rounded-full ${cls}`;
        }

        function describeEffect(w, name, otherName) {
            const amount = Math.abs(w).toFixed(1);
            if (Math.abs(w) < 0.5) {
                return `${otherName}이 같을 때, ${name}이 1시간 늘어도 점수는 <strong>거의 변하지 않아요</strong> (약 ${w >= 0 ? '+' : '-'}${amount}점).`;
            }
            return `${otherName}이 같을 때, ${name}이 1시간 늘면 점수가 약 <strong>${amount}점 ${w > 0 ? '올라가요' : '내려가요'}</strong>.`;
        }

        function updateMetricsUI() {
            const { w1, w2, b } = getParams();
            const mse = calculateMSE();
            const r2 = calculateR2();

            elements.pointCount.textContent = `점 ${state.points.length}개`;
            elements.metricW1.textContent = fmt2(w1);
            elements.metricW2.textContent = fmt2(w2);
            elements.metricB.textContent = fmt2(b);
            elements.metricMSE.textContent = state.diverged ? '발산' : mse.toFixed(2);
            elements.metricR2.textContent = state.diverged ? '-' : r2.toFixed(4);
            elements.cumulativeVal.textContent = state.totalEpochs;

            elements.equationDisplay.textContent = state.diverged
                ? '값이 너무 커져서 식을 표시할 수 없어요'
                : `${AXES.y.short} = ${w1.toFixed(2)} × ${AXES.x1.short} ${signed(w2)} × ${AXES.x2.short} ${signed(b)}`;

            let explain;
            if (state.diverged) {
                explain = `<div>⚠️ 학습이 발산했어요. <strong>모델 초기화</strong>를 누르고 학습률을 낮춰서 다시 학습해 보세요.</div>`;
            } else if (state.points.length === 0) {
                explain = `<div>💡 데이터를 넣고 학습을 시작해 보세요.</div>`;
            } else if (state.totalEpochs === 0) {
                explain = `<div>💡 학습을 시작하면 각 변수가 점수에 주는 영향을 풀어서 설명해 드려요.</div>`;
            } else {
                explain = `<div class="font-bold text-indigo-700 mb-0.5"><i class="fa-solid fa-comment-dots mr-1"></i>AI가 찾은 규칙 해석하기</div>`
                    + `<div>• ${describeEffect(w1, AXES.x1.name, AXES.x2.name)}</div>`
                    + `<div>• ${describeEffect(w2, AXES.x2.name, AXES.x1.name)}</div>`;
            }
            elements.coefExplain.innerHTML = explain;
        }

        function refresh() {
            updateMetricsUI();
            renderPlot();
        }

        // ---------------- 학습 제어 ----------------
        function startTraining() {
            if (state.points.length === 0) {
                showToast("데이터를 먼저 넣어 주세요!", "warning");
                return;
            }
            if (state.isTraining) return;
            if (state.diverged) {
                showToast("발산한 상태예요. '모델 초기화' 후 다시 학습해 보세요.", "warning");
                return;
            }

            state.isTraining = true;
            setStatus('training');

            // 3D 그래프는 다시 그리는 데 시간이 걸려서, 에포크 수와 관계없이
            // 약 0.6~2.5초 동안 진행 과정을 보여주도록 시간 기준으로 나눠 학습합니다.
            let done = 0;
            const duration = Math.min(2500, Math.max(600, state.epochs * 8));
            const startTime = performance.now();

            function runFrame(now) {
                if (!state.isTraining) return;
                const progress = Math.min(1, (now - startTime) / duration);
                const target = Math.max(done + 1, Math.round(state.epochs * progress));
                while (done < Math.min(target, state.epochs)) {
                    stepGradientDescent();
                    done++;
                    if (checkDiverged()) { refresh(); return; }
                }
                refresh();
                if (done >= state.epochs) {
                    state.isTraining = false;
                    setStatus('done');
                    return;
                }
                requestAnimationFrame(runFrame);
            }
            requestAnimationFrame(runFrame);
        }

        function stepOnce() {
            if (state.points.length === 0) return showToast("데이터를 먼저 넣어 주세요!", "warning");
            if (state.diverged) return showToast("발산한 상태예요. '모델 초기화' 후 다시 학습해 보세요.", "warning");
            stepGradientDescent();
            checkDiverged();
            refresh();
        }

        function resetModel(showMessage = true) {
            state.a1 = 0;
            state.a2 = 0;
            state.c = 0;
            state.totalEpochs = 0;
            state.isTraining = false;
            state.diverged = false;
            setStatus('idle');
            refresh();
            if (showMessage) showToast("가중치 및 누적 에포크가 초기화되었습니다.");
        }

        // ---------------- 예시 데이터 ----------------
        const rand = (min, max) => min + Math.random() * (max - min);
        const round1 = (v) => Math.round(v * 10) / 10;
        const clampScore = (v) => Math.max(5, Math.min(98, v));

        function makeData(n, w1, w2, b, noise) {
            const pts = [];
            for (let i = 0; i < n; i++) {
                const x1 = round1(rand(1, 10));
                const x2 = round1(rand(4, 9));
                const y = round1(clampScore(w1 * x1 + w2 * x2 + b + (Math.random() - 0.5) * 2 * noise));
                pts.push({ x1, x2, y });
            }
            return pts;
        }

        function loadPreset(type) {
            hideCoordFeedback();
            if (type === 'basic') {
                state.points = makeData(18, 4.5, 3.5, 15, 8);
            } else if (type === 'nosleep') {
                state.points = makeData(18, 6, 0, 25, 8);
            } else if (type === 'noisy') {
                state.points = makeData(22, 4.5, 3.5, 15, 25);
            } else if (type === 'outlier') {
                // 이상치 2개만으로 공부 시간의 기울기(w₁)가 약 4.5 → 약 1.8로 크게 줄어드는 것을 볼 수 있음
                state.points = makeData(16, 4.5, 3.5, 15, 5);
                state.points.push({ x1: 9, x2: 7, y: 35 });   // 많이 공부했는데 점수가 낮은 학생
                state.points.push({ x1: 2, x2: 6, y: 90 });   // 거의 공부하지 않았는데 점수가 높은 학생
            }
            resetModel(false);
            showToast("예시 데이터 세트가 로드되었습니다.");
        }

        // ---------------- 데이터 직접 입력 ----------------
        const NUMBER_PATTERN = /^[-+]?(?:\d+\.?\d*|\.\d+)$/;

        // 입력 문자열 → { points: [{x1, x2, y, raw}], invalid: [원문 조각] }
        function parseCoordinateText(text) {
            const normalized = text
                .replace(/（/g, '(')
                .replace(/）/g, ')')
                .replace(/，/g, ',');

            const points = [];
            const invalid = [];
            let pending = []; // 괄호 없이 입력된 숫자를 3개씩 모으는 중

            const flushPending = () => {
                if (pending.length) {
                    invalid.push(pending.map(t => t.raw).join(','));
                    pending = [];
                }
            };

            // ① (괄호 묶음)  ② 괄호·쉼표·공백이 아닌 덩어리  ③ 짝이 맞지 않는 괄호
            const tokenPattern = /\(([^()]*)\)|[^\s,;()]+|[()]/g;
            let match;
            while ((match = tokenPattern.exec(normalized)) !== null) {
                const token = match[0];
                if (match[1] !== undefined) {
                    flushPending();
                    const parts = match[1].split(/[\s,;]+/).filter(Boolean);
                    if (parts.length === 3 && parts.every(t => NUMBER_PATTERN.test(t))) {
                        const [x1, x2, y] = parts.map(parseFloat);
                        points.push({ x1, x2, y, raw: token });
                    } else {
                        invalid.push(token);
                    }
                } else if (token === '(' || token === ')') {
                    continue; // 짝이 맞지 않는 괄호는 무시
                } else if (NUMBER_PATTERN.test(token)) {
                    pending.push({ value: parseFloat(token), raw: token });
                    if (pending.length === 3) {
                        points.push({
                            x1: pending[0].value, x2: pending[1].value, y: pending[2].value,
                            raw: pending.map(t => t.raw).join(',')
                        });
                        pending = [];
                    }
                } else {
                    flushPending();
                    invalid.push(token);
                }
            }
            flushPending();
            return { points, invalid };
        }

        const inRange = (v, axis) => v >= 0 && v <= axis.max;
        const isPointInRange = (p) => inRange(p.x1, AXES.x1) && inRange(p.x2, AXES.x2) && inRange(p.y, AXES.y);

        function formatPoint(p) {
            const f = (v) => String(Math.round(v * 100) / 100);
            return `(${f(p.x1)}, ${f(p.x2)}, ${f(p.y)})`;
        }

        function summarizeList(items, max = 5) {
            const shown = items.slice(0, max).join(', ');
            return items.length > max ? `${shown} 외 ${items.length - max}개` : shown;
        }

        function escapeHtml(str) {
            return String(str).replace(/[&<>"']/g, (c) => ({
                '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
            }[c]));
        }

        function rangeText() {
            return `${AXES.x1.name} 0~${AXES.x1.max}${AXES.x1.unit}, ${AXES.x2.name} 0~${AXES.x2.max}${AXES.x2.unit}, ${AXES.y.name} 0~${AXES.y.max}${AXES.y.unit}`;
        }

        function hideCoordFeedback() {
            elements.coordFeedback.classList.add('hidden');
            elements.coordFeedback.innerHTML = '';
        }

        function renderCoordFeedback(accepted, outOfRange, invalid) {
            const lines = [];
            if (accepted.length) {
                lines.push(`✅ <strong>${accepted.length}개</strong>의 점을 추가했어요: <span class="font-mono">${escapeHtml(summarizeList(accepted.map(formatPoint)))}</span>`);
            }
            if (outOfRange.length) {
                lines.push(`⚠️ 범위를 벗어나서 추가하지 않았어요: <span class="font-mono">${escapeHtml(summarizeList(outOfRange.map(formatPoint)))}</span> <span class="opacity-75">(${escapeHtml(rangeText())})</span>`);
            }
            if (invalid.length) {
                lines.push(`❌ 데이터로 읽을 수 없는 입력이에요: <span class="font-mono">${escapeHtml(summarizeList(invalid))}</span> <span class="opacity-75">(공부 시간, 수면 시간, 점수 세 수를 짝지어 입력하세요. 예: (5,7,80))</span>`);
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
                showToast("데이터를 입력해 주세요. 예) (5,7,80)", "warning");
                elements.coordInput.focus();
                return;
            }

            const { points, invalid } = parseCoordinateText(text);
            if (points.length === 0 && invalid.length === 0) invalid.push(text.trim());

            const accepted = [];
            const outOfRange = [];
            points.forEach(p => (isPointInRange(p) ? accepted : outOfRange).push(p));

            if (accepted.length) {
                const wasEmpty = state.points.length === 0;
                accepted.forEach(p => state.points.push({ x1: p.x1, x2: p.x2, y: p.y }));
                // 선형 회귀 페이지와 같게: 첫 점을 넣으면 평면의 시작 높이(절편)를 그 점의 점수로 설정
                if (wasEmpty && state.totalEpochs === 0) state.c = accepted[0].y / AXES.y.max;
                refresh();
            }

            renderCoordFeedback(accepted, outOfRange, invalid);
            elements.coordInput.value = [...outOfRange.map(p => p.raw), ...invalid].join(' ');
            elements.coordInput.focus();

            if (!outOfRange.length && !invalid.length) {
                showToast(`${accepted.length}개의 점을 추가했어요.`);
            } else if (accepted.length) {
                showToast("일부 데이터만 추가했어요. 입력창 아래 안내를 확인하세요.", "warning");
            } else {
                showToast("데이터를 추가하지 못했어요. 입력창 아래 안내를 확인하세요.", "warning");
            }
        }

        // ---------------- 알림 ----------------
        function showToast(msg, type = "info") {
            const container = $('toast-container');
            const toast = document.createElement('div');
            const bgColor = type === 'warning' ? 'bg-amber-600' : 'bg-slate-800';
            toast.className = `${bgColor} text-white text-xs px-4 py-2.5 rounded-xl shadow-xl transition-all duration-300 transform translate-y-2 opacity-0 flex items-center gap-2`;
            toast.innerHTML = `<i class="fa-solid fa-circle-info text-yellow-400"></i> ${msg}`;
            container.appendChild(toast);
            setTimeout(() => toast.classList.remove('translate-y-2', 'opacity-0'), 10);
            setTimeout(() => {
                toast.classList.add('opacity-0');
                setTimeout(() => toast.remove(), 300);
            }, 2500);
        }

        // ---------------- 이벤트 연결 ----------------
        elements.coordHint.innerHTML =
            `<i class="fa-solid fa-circle-info mr-1 text-slate-400"></i>순서는 <strong class="text-indigo-600">(공부 시간, 수면 시간, 점수)</strong>이고, `
            + `공부·수면은 <strong class="text-indigo-600">0~${AXES.x1.max}시간</strong>, 점수는 <strong class="text-indigo-600">0~${AXES.y.max}점</strong>까지 입력할 수 있어요.<br>`
            + `<span class="whitespace-nowrap"><kbd>Enter</kbd> 추가</span> · <span class="whitespace-nowrap"><kbd>Shift</kbd>+<kbd>Enter</kbd> 줄바꿈</span> · 여러 학생은 띄어쓰기나 줄바꿈으로 구분`;

        elements.resetViewBtn.addEventListener('click', resetView);

        elements.undoBtn.addEventListener('click', () => {
            if (state.points.length === 0) return showToast("삭제할 점이 없어요.", "warning");
            const removed = state.points.pop();
            refresh();
            showToast(`마지막 점 ${formatPoint(removed)}을 삭제했어요.`);
        });

        elements.clearBtn.addEventListener('click', () => {
            state.points = [];
            hideCoordFeedback();
            resetModel(false);
            showToast("모든 데이터 점이 삭제되었습니다.");
        });

        elements.toggleResiduals.addEventListener('change', (e) => {
            state.showResiduals = e.target.checked;
            renderPlot();
        });

        elements.epochsSlider.addEventListener('input', (e) => {
            state.epochs = parseInt(e.target.value, 10);
            elements.epochsVal.textContent = `${state.epochs}회`;
        });

        elements.lrSlider.addEventListener('input', (e) => {
            state.lr = parseFloat(e.target.value);
            elements.lrVal.textContent = state.lr.toFixed(2);
        });

        elements.trainBtn.addEventListener('click', startTraining);
        elements.stepBtn.addEventListener('click', stepOnce);
        elements.resetModelBtn.addEventListener('click', () => resetModel(true));

        $('preset-basic').addEventListener('click', () => loadPreset('basic'));
        $('preset-nosleep').addEventListener('click', () => loadPreset('nosleep'));
        $('preset-noisy').addEventListener('click', () => loadPreset('noisy'));
        $('preset-outlier').addEventListener('click', () => loadPreset('outlier'));

        elements.coordAddBtn.addEventListener('click', addPointsFromInput);
        elements.coordInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey && !e.isComposing && e.keyCode !== 229) {
                e.preventDefault();
                addPointsFromInput();
            }
        });

        window.onload = function () {
            if (!window.Plotly) {
                elements.plotFallback.classList.remove('hidden');
            }
            loadPreset('basic');
        };
    </script>
</body>
</html>
"""

# HTML을 화면에 배치
#  - streamlit 1.56 이상: st.iframe 사용 (내용 높이에 맞춰 화면 높이가 자동으로 조절됨)
#  - 그보다 낮은 버전: 예전 방식인 components.html 사용 (고정 높이 1280px + 스크롤)
if hasattr(st, "iframe"):
    st.iframe(html_code, height="content")
else:
    components.html(html_code, height=1280, scrolling=True)
