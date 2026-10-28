import streamlit as st
import streamlit.components.v1 as components

# =====================================================================
# 2단계: 다중 회귀 (3차원 그래프) - 청바지 치수 데이터로 허리둘레 예측
#  - 메인 파일의 st.navigation 에 등록된 페이지입니다. 메인 파일과 같은 폴더에 두세요.
#  - 와이드 레이아웃, 사이드바 펼침, 여백 제거 스타일은 메인 파일에서 공통으로 적용됩니다.
#  - 3D 그래프는 Plotly.js(3D 전용 번들)를 CDN으로 불러옵니다. 파이썬 패키지 설치는 필요 없습니다.
#  - 데이터: jeans.csv 963명(목둘레, 몸무게, 엉덩이둘레 → 허리둘레)을 아래 JS의 JEANS 배열에 넣어 두었습니다.
#    CSV 파일을 따로 올리지 않아도 동작합니다. (몸무게가 65인 242명도 원본 그대로 포함)
#  - 독립변수가 3개라 한 화면에 그릴 수 없어서, 두 변수씩 짝지어 3D 평면으로 보여줍니다.
#  - 변수 이름·단위·축 범위를 바꾸려면 아래 JS의 VARS, TARGET 설정만 고치면 됩니다.
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

            <!-- 상단 단계 메뉴: 클릭하면 해당 페이지로 이동 (target="_top": 교구 화면이 아니라 스트림릿 전체 페이지를 이동) -->
            <nav class="flex space-x-1 bg-indigo-700/50 p-1 rounded-xl text-xs sm:text-sm">
                <a href="./" target="_top" data-page="" class="px-3 py-1.5 rounded-lg text-indigo-100 hover:bg-white/20 hover:text-white transition" title="'1단계: 선형 회귀' 페이지로 이동">
                    <i class="fa-solid fa-chart-line mr-1"></i> 1단계: 선형 회귀
                </a>
                <span class="px-3 py-1.5 rounded-lg font-semibold bg-white text-indigo-700 shadow-sm">
                    <i class="fa-solid fa-cube mr-1"></i> 2단계: 다중 회귀
                </span>
                <a href="classification" target="_top" data-page="classification" class="px-3 py-1.5 rounded-lg text-indigo-100 hover:bg-white/20 hover:text-white transition" title="'3단계: 분류' 페이지로 이동">
                    <i class="fa-solid fa-shapes mr-1"></i> 3단계: 분류
                </a>
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
                        <span id="point-count" class="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 font-mono border border-slate-200">0명</span>
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

                <!-- 그래프에 그릴 두 변수 고르기 -->
                <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
                    <div class="flex flex-wrap items-center justify-between gap-2">
                        <span class="font-bold text-slate-700 text-sm"><i class="fa-solid fa-object-group text-indigo-500 mr-1"></i> 그래프에 그릴 두 변수</span>
                        <div id="pair-btns" class="inline-flex flex-wrap rounded-lg p-1 bg-slate-100 border border-slate-200 text-xs sm:text-sm"></div>
                    </div>
                    <p class="text-[11px] text-slate-500 mt-2 break-keep">예측하려는 값은 항상 <strong class="text-indigo-600">허리둘레(세로축)</strong>예요. 독립변수가 3개(목둘레·몸무게·엉덩이둘레)라 한 화면에 모두 그릴 수 없어서, 두 개씩 짝지어 보여줘요.</p>
                </div>

                <div class="bg-white rounded-2xl p-4 shadow-sm border border-slate-200 flex flex-col">
                    <div class="relative w-full rounded-xl border border-slate-200 bg-slate-900 overflow-hidden shadow-inner">
                        <div id="plot3d" class="w-full h-[380px] sm:h-[460px] lg:h-[520px]"></div>
                        <div id="plot-fallback" class="hidden absolute inset-0 flex items-center justify-center p-6 text-center text-sm text-slate-300 leading-relaxed">
                            3D 그래프를 불러오지 못했어요.<br>인터넷 연결을 확인하거나, 학교 방화벽에서 cdn.jsdelivr.net 접속이 막혀 있는지 확인해 주세요.
                        </div>
                    </div>

                    <div class="w-full flex flex-wrap items-center gap-x-4 gap-y-1 mt-3 px-1 text-xs text-slate-600">
                        <span class="flex items-center gap-1.5"><span class="inline-block w-3 h-3 rounded-full bg-blue-500 ring-2 ring-white shadow"></span> 측정 데이터</span>
                        <span class="flex items-center gap-1.5"><span class="inline-block w-4 h-3 rounded-sm bg-indigo-400/70"></span> AI 회귀 평면</span>
                        <span class="flex items-center gap-1.5"><span class="inline-block w-4 border-t-2 border-dashed border-rose-500"></span> 오차</span>
                        <span class="flex items-center gap-1.5"><span class="text-yellow-500">◆</span> 예측해 본 사람</span>
                    </div>

                    <div class="w-full flex flex-wrap justify-between items-center gap-2 mt-2 px-1 text-xs sm:text-sm text-slate-600">
                        <label class="flex items-center space-x-2 cursor-pointer select-none">
                            <input type="checkbox" id="toggle-residuals" checked class="w-4 h-4 text-indigo-600 rounded border-slate-300 focus:ring-indigo-500">
                            <span>오차 선(Residuals) 표시</span>
                        </label>
                        <span class="text-slate-400 text-xs"><i class="fa-solid fa-computer-mouse mr-1"></i>드래그: 회전 · 휠: 확대/축소 · 점에 올리면 값 표시</span>
                    </div>
                    <p id="slice-note" class="hidden mt-2 p-2.5 rounded-xl text-xs bg-amber-50 text-amber-800 border border-amber-200 break-keep"></p>
                </div>

                <!-- 새 사람 예측 -->
                <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
                    <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1">
                        <i class="fa-solid fa-ruler-combined text-indigo-500"></i> 내 허리둘레 예측해 보기
                    </h3>
                    <div class="grid grid-cols-3 gap-2" id="query-inputs"></div>
                    <div class="flex flex-col sm:flex-row gap-2 mt-2">
                        <button id="query-btn" class="flex-grow px-3 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow-sm transition flex items-center justify-center gap-1.5 text-xs sm:text-sm">
                            <i class="fa-solid fa-magnifying-glass-chart"></i> 허리둘레 예측
                        </button>
                        <button id="query-clear-btn" class="sm:w-24 px-3 py-2 bg-slate-100 hover:bg-red-50 text-slate-600 hover:text-red-600 font-medium rounded-xl border border-slate-200 transition flex items-center justify-center gap-1.5 text-xs sm:text-sm">
                            <i class="fa-solid fa-eraser"></i> 지우기
                        </button>
                    </div>
                    <div id="query-result" class="hidden mt-2 p-3 rounded-xl text-xs border bg-yellow-50 border-yellow-300 text-slate-700 break-keep"></div>
                </div>

                <!-- 좌표 직접 입력 패널 -->
                <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
                    <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1">
                        <i class="fa-solid fa-keyboard text-indigo-500"></i> 데이터 직접 추가하기 (목둘레, 몸무게, 엉덩이둘레, 허리둘레)
                    </h3>
                    <div class="flex flex-col sm:flex-row gap-2">
                        <textarea id="coord-input" rows="2" spellcheck="false" autocomplete="off"
                            class="flex-grow px-3 py-2 rounded-xl border border-slate-300 bg-slate-50 font-mono text-sm resize-y focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:bg-white"
                            placeholder="예) (36, 62, 96, 78)   또는   36 62 96 78"></textarea>
                        <button id="coord-add-btn" class="sm:w-28 px-3 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow-sm transition flex items-center justify-center gap-1.5 text-xs sm:text-sm">
                            <i class="fa-solid fa-circle-plus"></i> 점 추가
                        </button>
                    </div>
                    <p id="coord-hint" class="text-[11px] text-slate-500 mt-2 leading-relaxed break-keep"></p>
                    <div id="coord-feedback" class="hidden mt-2 p-2.5 rounded-xl text-xs border space-y-1"></div>
                </div>

                <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
                    <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1">
                        <i class="fa-solid fa-folder-open text-indigo-500"></i> 데이터 세트 불러오기 (청바지 치수 데이터)
                    </h3>
                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
                        <button id="preset-10" class="p-2 bg-rose-50 hover:bg-rose-100 text-rose-700 rounded-xl font-medium text-xs sm:text-sm transition text-center border border-rose-100">
                            🎲 무작위 10명
                        </button>
                        <button id="preset-50" class="p-2 bg-amber-50 hover:bg-amber-100 text-amber-700 rounded-xl font-medium text-xs sm:text-sm transition text-center border border-amber-100">
                            🎲 무작위 50명
                        </button>
                        <button id="preset-200" class="p-2 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 rounded-xl font-medium text-xs sm:text-sm transition text-center border border-emerald-100">
                            🎲 무작위 200명
                        </button>
                        <button id="preset-all" class="p-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 rounded-xl font-medium text-xs sm:text-sm transition text-center border border-indigo-100">
                            👖 전체 963명
                        </button>
                    </div>
                    <p class="text-[11px] text-slate-500 mt-2 break-keep">첫 화면은 963명 중 고정으로 뽑은 50명이에요. 버튼으로 다른 표본이나 전체 데이터를 불러와 보세요. 사람 수가 적을수록 학습할 때마다 가중치가 크게 달라져요. 이 데이터에는 몸무게가 정확히 65kg인 사람이 많아요(963명 중 242명). 몸무게 축에서 65 위치에 점들이 한 줄로 늘어선 이유예요.</p>
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

                    <div class="mb-4">
                        <span class="text-xs sm:text-sm font-semibold text-slate-700 block mb-1">학습에 쓸 독립변수</span>
                        <div class="grid grid-cols-2 gap-2 text-xs sm:text-sm">
                            <button data-mode="pair" class="mode-btn p-2 rounded-xl border font-semibold transition"></button>
                            <button data-mode="all" class="mode-btn p-2 rounded-xl border font-semibold transition">⭐ 3개 모두 사용</button>
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
                                <span id="lr-val" class="font-mono font-bold text-indigo-600 text-sm bg-indigo-50 px-2 py-0.5 rounded">0.01</span>
                            </div>
                            <input type="range" id="lr-slider" min="0.01" max="1" step="0.01" value="0.01" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600">
                            <p class="text-[11px] text-slate-400 mt-1">학습률이 너무 크면 오차가 줄지 않고 오히려 커질 수 있어요. (이 데이터는 3개 모두 쓰면 약 0.43, 2개만 쓰면 짝에 따라 약 0.5~0.65부터 발산해요)</p>
                        </div>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
                    <h2 class="text-base font-bold text-slate-800 mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-square-poll-vertical text-emerald-600"></i> 실시간 AI 평가 지표
                    </h2>

                    <div class="grid grid-cols-4 gap-2 mb-2" id="weight-cards"></div>

                    <div class="grid grid-cols-2 gap-2">
                        <div class="p-3 bg-amber-50/70 border border-amber-200 rounded-xl">
                            <span class="text-xs text-amber-700 font-semibold block mb-0.5">AI 평균 제곱 오차 (MSE)</span>
                            <span id="metric-mse" class="text-xl font-extrabold text-amber-800 font-mono">0.00</span>
                            <span id="metric-rmse" class="text-[11px] text-amber-700 block mt-0.5"></span>
                        </div>
                        <div class="p-3 bg-emerald-50/70 border border-emerald-200 rounded-xl">
                            <span class="text-xs text-emerald-700 font-semibold block mb-0.5">결정계수 (R²)</span>
                            <span id="metric-r2" class="text-xl font-extrabold text-emerald-800 font-mono">0.0000</span>
                        </div>
                    </div>

                    <div class="mt-4 p-3 bg-slate-900 text-white rounded-xl font-mono text-center shadow-inner">
                        <span id="equation-label" class="text-slate-400 text-xs block mb-1">현재 AI 방정식</span>
                        <span id="equation-display" class="text-yellow-300 font-bold text-xs sm:text-sm break-words"></span>
                    </div>

                    <div id="coef-explain" class="mt-3 p-3 bg-indigo-50/60 border border-indigo-100 rounded-xl text-xs text-indigo-900 leading-relaxed break-keep space-y-1"></div>
                </div>

                <!-- 변수 조합별 R² 비교 -->
                <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
                    <h2 class="text-base font-bold text-slate-800 mb-1 flex items-center gap-2">
                        <i class="fa-solid fa-ranking-star text-indigo-600"></i> 어떤 조합이 허리둘레를 가장 잘 예측할까?
                    </h2>
                    <p class="text-[11px] text-slate-500 mb-3 break-keep">조합마다 끝까지 학습했을 때 도달할 수 있는 최고 R²(최소제곱법으로 계산)예요. 노란 선은 지금 AI의 R²예요.</p>
                    <div id="combo-chart" class="space-y-2"></div>
                </div>

                <div class="bg-amber-50/80 border border-amber-200 p-5 rounded-2xl shadow-sm">
                    <h3 class="text-sm font-bold text-amber-900 flex items-center gap-1.5 mb-2">
                        <i class="fa-solid fa-lightbulb text-amber-600"></i> 입력이 늘어나면 무엇이 달라질까?
                    </h3>
                    <div class="space-y-2 text-xs text-amber-900 break-keep">
                        <div class="bg-white p-2.5 rounded-xl border border-amber-200">
                            <span class="font-bold">입력 1개</span> · 허리 = w × 엉덩이 + b
                            <span class="block text-amber-700 mt-0.5">→ 2차원 평면 위의 <strong>직선</strong></span>
                        </div>
                        <div class="bg-white p-2.5 rounded-xl border border-amber-200">
                            <span class="font-bold">입력 2개</span> · 허리 = w₁ × 목 + w₂ × 엉덩이 + b
                            <span class="block text-amber-700 mt-0.5">→ 3차원 공간 속의 <strong>평면</strong></span>
                        </div>
                        <div class="bg-white p-2.5 rounded-xl border border-amber-200">
                            <span class="font-bold">입력 3개</span> · 허리 = w₁ × 목 + w₂ × 몸무게 + w₃ × 엉덩이 + b
                            <span class="block text-amber-700 mt-0.5">→ 4차원 공간 속의 <strong>초평면</strong> (눈으로 그릴 수 없어서 두 변수씩 잘라서 봐요)</span>
                        </div>
                        <p class="text-amber-800">학습 방법(경사하강법)과 평가 방법(MSE, R²)은 그대로예요. 찾아야 할 가중치만 늘어나요. 변수를 추가하면 다른 변수의 가중치도 달라져요. 예를 들어 '목둘레'의 가중치를 2개 모드와 3개 모드에서 비교해 보세요!</p>
                    </div>
                </div>

            </section>
        </div>
    </main>

    <div id="toast-container" class="fixed bottom-5 right-5 z-50 flex flex-col gap-2"></div>

    <footer class="bg-slate-100 border-t border-slate-200 py-3 text-center text-xs text-slate-500">
        머신러닝 인터랙티브 교구 | HTML5 & Plotly.js 3D · 데이터: 청바지 치수 데이터(jeans.csv, 963명)
    </footer>

    <script>
        // ================================================================
        // 데이터: [목둘레(cm), 몸무게(kg), 엉덩이둘레(cm), 허리둘레(cm)] 963명 (jeans.csv)
        // ================================================================
        const JEANS = [
            [33.8,51.1,86,62.9],[33,45.4,87.9,63],[35.3,58.9,95.2,64.2],[33.1,47.3,88.6,64.4],[33.1,47.7,88.5,65],[33,44.4,87.5,65.3],[35.2,58,88.9,65.6],[34.7,56.4,91.7,65.8],[33.2,47.3,89.7,66],[33.2,47.5,87.6,66.1],
            [33.9,51.1,85.8,66.1],[34,51,89.3,66.3],[33.7,49.5,90.6,66.6],[34.2,53.8,88.3,66.6],[34.3,52.9,91.4,66.7],[34.3,52.9,91.4,66.7],[34.3,52.9,91.4,66.7],[34.3,52.9,91.4,66.7],[33.4,48,85.9,66.9],[33.6,48.6,87.4,66.9],
            [34.5,53.5,89.9,67],[34.1,52.1,85.7,67.1],[32.5,45.4,90.2,67.2],[32.5,45.4,90.2,67.2],[32.5,45.4,90.2,67.2],[33.1,47,89.8,67.2],[35.8,61.1,91.8,67.3],[34.2,51.4,94.7,67.5],[34.7,55.6,89.1,67.5],[34.3,52.7,89.6,67.6],
            [34.9,56.1,93.5,67.6],[33.8,50.6,91.4,67.7],[34.7,55.1,91.9,67.9],[34.6,54.3,88.9,68],[33.6,49.9,90,68.1],[33.6,49.9,90,68.1],[33.6,49.9,90,68.1],[33.6,49.9,90,68.1],[34.5,54,92.3,68.2],[34.5,54,92.3,68.2],
            [34.5,54,92.3,68.2],[34.5,54,92.3,68.2],[34.7,54.9,92.3,68.2],[34.4,53.3,90.9,68.3],[32.9,45.5,88.2,68.4],[33.8,50.7,92.9,68.6],[34.9,57,89.9,68.6],[32.5,46.5,90.2,68.7],[33.9,51.9,88.5,68.8],[33.7,50.8,91.2,69],
            [35.6,60.8,99.2,69],[35,65,92.1,69],[33.9,51.1,89.8,69.1],[34.5,52.7,95.1,69.2],[34.3,51.6,95,69.3],[36,63.3,94.7,69.3],[34,50.9,93.6,69.4],[34.2,51.6,89.9,69.4],[35.3,59.3,90.4,69.4],[34.5,53.4,90.8,69.5],
            [34.1,51.1,89.3,69.6],[34.9,56.1,91.2,69.7],[35.5,59.8,91.6,69.7],[33.5,48.5,91.1,69.9],[33.5,48.5,91.1,69.9],[33.5,48.5,91.1,69.9],[33.5,48.5,91.1,69.9],[33.5,48.5,91.1,69.9],[33.5,48.5,91.1,69.9],[35.5,58.3,93.7,69.9],
            [35.4,65,89.2,70],[34.3,51.4,90.5,70.1],[38,65,93,70.1],[34.8,55.9,91.7,70.2],[35.8,61.8,91.8,70.2],[33.2,48.3,90.3,70.3],[34.3,52.3,90.1,70.3],[34.9,57,92.8,70.3],[36,59.1,92.6,70.3],[34.3,51.5,90.6,70.4],
            [35.2,58.4,88.6,70.4],[33.2,46.9,88.9,70.5],[34.5,53.3,97.2,70.5],[34.6,65,91.4,70.6],[37.3,65,92,70.6],[33.8,50.5,91.7,70.7],[33.8,50.5,91.7,70.7],[33.8,50.5,91.7,70.7],[33.8,50.5,91.7,70.7],[33.8,50.5,91.7,70.7],
            [34.2,51.4,91,70.7],[37.3,65,96.5,70.7],[36.9,70.3,95.8,70.7],[34.1,51,93.9,70.8],[34.3,52.8,90.2,70.8],[34.8,55.3,93.1,70.8],[34.9,56.6,95.1,70.8],[34.9,56.6,95.1,70.8],[34.9,56.6,95.1,70.8],[34.9,56.6,95.1,70.8],
            [36,63.3,96.2,70.8],[34.3,52.3,95.9,70.9],[34.3,52.6,94.2,70.9],[34.5,54.3,91.2,70.9],[35.6,61.7,88.5,71],[36.6,65,92.4,71],[33.3,48.5,92.1,71.1],[34.6,52.9,94.7,71.3],[35.2,58.8,91.1,71.3],[36.6,65,89.6,71.4],
            [33.8,50.5,92.2,71.5],[34.1,51,87.9,71.5],[34.1,51,87.9,71.5],[34.1,51,87.9,71.5],[34.1,51,87.9,71.5],[34.1,51,87.9,71.5],[34.1,51,87.9,71.5],[34.7,55.4,91.3,71.5],[35.4,59.2,97.8,71.5],[36.1,65,93.1,71.5],
            [40,65,94.8,71.5],[33.4,52.1,95.1,71.6],[34.6,52.8,91.9,71.6],[34.4,52.9,92.7,71.6],[34.4,52.9,92.7,71.6],[34.4,52.9,92.7,71.6],[34.4,52.9,92.7,71.6],[34.4,52.9,92.7,71.6],[34.4,52.9,92.7,71.6],[35.1,57.4,95.9,71.7],
            [35.6,60.3,93.1,71.7],[35.4,65,87.8,71.7],[34.6,54.5,97.6,71.8],[35.8,61.4,94.1,71.8],[37.8,65,98.5,71.8],[34.3,52.4,88,71.9],[34.9,56.1,89.9,71.9],[35.2,55.9,97.5,72],[35.5,58.8,91.8,72],[33.5,49.2,92.1,72.1],
            [36,63.4,92,72.1],[33.9,50.3,92.6,72.2],[34.7,54.3,89.4,72.3],[35.2,56.9,90.5,72.3],[34.4,52.7,94.3,72.4],[33.9,50.5,91.9,72.5],[35.9,62.8,94.1,72.5],[34.9,56.2,90.1,72.6],[35.3,58.9,94.3,72.6],[35.6,60.8,96.4,72.6],
            [35.9,62.3,98.4,72.7],[39.7,65,93.7,72.7],[36.6,66.9,93.2,72.7],[38.1,65,94.4,72.8],[33.4,47.1,90.1,72.9],[33.9,50.2,90.5,72.9],[34.4,52.6,93,72.9],[34.4,53.1,91.6,72.9],[35.6,54.7,94.3,72.9],[34.5,54.7,91.8,72.9],
            [33.4,49.3,92.3,73],[35.1,57.2,92,73.1],[35.1,57.3,95.1,73.1],[38.7,65,96.6,73.1],[35.4,59.5,94.1,73.3],[36.1,63.6,95.2,73.3],[35.9,59.7,96.7,73.4],[36.1,64,93.3,73.4],[38.3,65,98.6,73.4],[36.6,67.2,98.1,73.4],
            [36.6,67.9,96.8,73.4],[35.5,58.1,96.9,73.5],[35.6,60.9,93.4,73.5],[37.4,65,96.7,73.5],[35.8,61.8,90.5,73.6],[33.6,48.9,91,73.7],[35.3,57.7,97.9,73.7],[35.3,57.7,97.9,73.7],[35.3,57.7,97.9,73.7],[35.3,57.7,97.9,73.7],
            [38.8,65,96.5,73.7],[33.5,48.8,91.5,73.8],[35.3,57.9,94.7,73.8],[37.3,65,95.8,73.8],[37.1,65,93.8,73.8],[36.7,67.4,94.5,73.8],[35.7,61.5,90.9,73.9],[35.9,65,94.9,73.9],[36,63.3,95.1,74],[34.3,52.3,92.6,74.1],
            [35.5,60,96.3,74.1],[36,63.2,92.7,74.1],[34.7,55.2,95.4,74.2],[36.1,63.9,93.1,74.2],[36.1,64.5,96,74.2],[36.2,65,94.9,74.2],[34.8,55.3,95.8,74.3],[35.4,58.2,97.5,74.3],[35.5,59.9,90.9,74.4],[35.9,64.5,95.3,74.4],
            [36.3,65.9,93.6,74.4],[36.1,63.8,93.3,74.5],[40.3,65,95.8,74.5],[34.1,51.2,93.5,74.6],[34.5,53.6,93.1,74.6],[35.7,61.4,91.8,74.6],[35.8,61.7,93.3,74.6],[36.2,64.2,95.1,74.6],[36.6,70.8,96.2,74.6],[34.4,52.8,92.9,74.7],
            [36.6,65,95.4,74.7],[36,65,92.9,74.7],[36.3,65.5,93.5,74.7],[35.2,58.1,91.7,74.8],[34.2,51.4,91.4,74.9],[34.9,56.5,94.8,74.9],[35.8,61.7,93.4,74.9],[38.2,65,94.5,74.9],[37.3,65,94.6,74.9],[35.4,55.9,93.3,75],
            [35.2,57.5,94.8,75],[36.8,64.8,100.3,75],[36.6,64.9,93.6,75],[36.7,68.1,98.8,75],[36.2,58.9,96.1,75.1],[35.9,62.4,95.1,75.1],[35.2,57.2,92.6,75.2],[35.7,58.7,97.4,75.2],[36.7,61.4,99.7,75.2],[39.6,65,94.6,75.2],
            [35.9,65,98.4,75.2],[34.9,56.5,93.6,75.3],[40.1,65,93.9,75.3],[33.2,48.3,92.3,75.4],[36,63,100.2,75.4],[34.7,53.6,96.1,75.6],[35.2,58.5,97.5,75.6],[35.7,60.7,94.5,75.6],[36.1,62.9,102,75.6],[36.3,66.6,93.9,75.7],
            [37.4,72.9,95,75.7],[35.2,55.1,97,75.8],[35.5,58.7,97.3,75.8],[35.3,58.8,90.5,75.8],[36.1,65.4,92.3,75.8],[34.5,53.2,92.6,75.9],[34.6,54.4,91.5,75.9],[35.9,61.7,100.6,75.9],[36,62.3,96.3,75.9],[37.3,65,96.3,75.9],
            [34.7,52.9,96.3,76],[34.9,57,93.8,76],[35.9,60.8,97.7,76],[36.1,56.1,92.7,76.1],[35.1,57.1,93.6,76.1],[36.2,64.9,91.5,76.1],[36.8,69.3,93.2,76.1],[36.9,69.9,94.9,76.1],[40,65,95.8,76.2],[36.3,65.6,93,76.2],
            [36.2,63.9,95.7,76.3],[36.2,64.9,94.2,76.3],[36.6,67,99,76.3],[36.7,67.6,96.8,76.3],[36.7,68.9,95.6,76.3],[35.5,60.4,99.4,76.4],[38.6,82.3,100.3,76.4],[34.2,52.1,92.7,76.5],[34.8,54.1,92.9,76.5],[35.2,57.3,91.4,76.5],
            [36.2,58.8,98.2,76.6],[39.8,65,96.7,76.6],[36.5,65.6,96.2,76.6],[36.5,70.8,98,76.6],[37.1,71.3,94.4,76.6],[34.8,56.2,95.5,76.7],[35.2,58.2,93.6,76.7],[35.4,59.8,93.7,76.7],[35.8,61.6,103.3,76.7],[36.2,64.5,99.7,76.7],
            [36.4,65.8,93.2,76.7],[36.8,70.3,95.3,76.7],[34.3,52.1,92.1,76.8],[36,63.4,91.5,76.8],[36.1,62,92.5,76.9],[36.6,65,97.2,76.9],[36.6,65,92.7,76.9],[36.4,65.3,94.4,76.9],[36.5,68.2,97.3,76.9],[36.8,68.6,95.6,76.9],
            [35.5,54.9,95.8,77],[35.9,62.6,93.1,77],[35.9,62.7,92.1,77],[35.8,61.3,96.2,77.1],[36.2,66,94.8,77.1],[37.3,73.3,100.2,77.1],[36.7,65,93.4,77.2],[36.9,70.8,98.5,77.2],[36.2,59,97,77.3],[35.9,62.9,93.9,77.3],
            [37.1,65,98.7,77.3],[38.9,65,100,77.3],[35.8,65,94.7,77.3],[37.1,67.8,99.8,77.3],[37.1,72,96,77.3],[36.1,57.2,96.5,77.4],[37.1,71.5,95.2,77.4],[37.3,72.8,96.5,77.4],[37.5,73.7,101.6,77.4],[34.4,54.1,97.1,77.5],
            [36.4,60.2,97,77.5],[36.9,69.3,94.7,77.5],[36.1,58.5,99.7,77.6],[36.4,66.6,98.4,77.6],[37.8,76,96.7,77.6],[36.3,59.2,97.2,77.7],[36.5,64.6,96.4,77.7],[36.5,65,95.9,77.7],[36.5,67,95.5,77.7],[36.2,59.2,99.8,77.8],
            [35.8,62,93.6,77.8],[40.2,65,98.7,77.8],[36.9,69.3,96.6,77.8],[36.3,68.1,96.1,77.9],[38.5,65,98,78.1],[35.7,65,100,78.1],[38.6,65,99.2,78.1],[36.2,65.1,94.3,78.1],[36.6,67.1,97,78.1],[36,63.4,94.7,78.2],
            [39.2,65,97.7,78.2],[36.9,65,100.1,78.2],[36.5,68.6,97.9,78.2],[37.1,60.4,100.3,78.3],[39.6,65,96.6,78.3],[36.8,66,93.3,78.3],[36.7,69.1,98.4,78.3],[38.2,65,95.9,78.4],[35,56.5,93.9,78.5],[35.5,60.1,99.8,78.5],
            [39.1,65,97.6,78.5],[37,69.4,96.6,78.5],[36.2,57.6,93,78.6],[39.7,65,95.2,78.6],[37.5,65,101.4,78.6],[36.4,65.4,93.5,78.6],[36,57.9,93.1,78.7],[35.8,60.1,96.5,78.7],[35.8,61.8,98.5,78.7],[36.6,62,98.5,78.7],
            [36.8,67.6,94.2,78.7],[37,68.9,98.4,78.7],[36.8,70.6,96.2,78.7],[37.5,74,99.5,78.7],[34.9,56.4,95.6,78.8],[36.2,60,95.6,78.8],[36.8,62.9,96.8,78.8],[36.8,62.9,96.8,78.8],[36.8,62.9,96.8,78.8],[36.8,62.9,96.8,78.8],
            [36.5,64.8,98,78.8],[37.8,77,95.6,78.8],[38.8,65,97.6,78.9],[36.4,65.9,96.6,78.9],[36.7,67.3,103.1,78.9],[35.2,58.8,96.1,79],[36.2,64.5,95.7,79.1],[40.4,65,101.5,79.1],[36.5,67.6,95.8,79.1],[37.6,74.5,102.5,79.1],
            [35.1,58.3,95.1,79.2],[35.8,61.2,94.9,79.3],[35.8,61.2,94.9,79.3],[35.8,61.2,94.9,79.3],[35.8,61.2,94.9,79.3],[36.8,68.1,97,79.3],[37,68.8,93.9,79.3],[37.1,69.9,98.7,79.4],[37.1,70.4,99.8,79.4],[37.2,71.1,97.4,79.4],
            [37.5,75.1,97.1,79.4],[35.8,61.8,95.9,79.5],[35.8,62.2,97.3,79.5],[36.3,64.8,101.4,79.5],[36.6,67.4,94,79.5],[36.9,68.4,99.8,79.5],[37.2,70.5,99.9,79.5],[37.4,70.9,96.4,79.5],[36.5,60.2,98.4,79.6],[36.5,60.2,98.4,79.6],
            [36.5,60.2,98.4,79.6],[36.5,60.2,98.4,79.6],[36,63.2,97.3,79.6],[36.2,64.2,96.3,79.6],[41.7,65,100.8,79.6],[34.4,52.4,94.3,79.7],[35.8,61.7,98.7,79.7],[41.1,65,98.5,79.7],[38.9,65,97,79.7],[36.9,68.3,94.2,79.7],
            [37.6,75.4,97.4,79.7],[34.4,53.2,91.7,79.8],[35.2,56.6,94.6,79.8],[36,59.1,95.7,79.8],[37.6,65,102.4,79.9],[36.3,66,96,79.9],[36.9,69.2,94.5,79.9],[37,70.6,96.6,79.9],[36,59.4,97.1,80],[36.3,65.8,95.7,80],
            [37.3,72.3,98.5,80],[35.8,62.1,94.8,80.1],[37.4,71.7,97.9,80.1],[37.1,71.7,99.1,80.1],[37.3,72.5,94.7,80.1],[39,65,100.4,80.2],[39.9,65,106.1,80.2],[40.1,65,100.6,80.2],[39.9,65,102.5,80.2],[37.1,70.4,99.1,80.2],
            [37.2,71.2,97.3,80.2],[36.5,67.5,96.5,80.3],[36.9,68.7,93.5,80.3],[37,70.5,98.9,80.3],[37,75.3,99.6,80.3],[35.4,54.8,94.1,80.4],[33.9,65,101.5,80.4],[36.6,67.6,97,80.4],[36.8,68.3,98.9,80.4],[37.8,76.4,99.2,80.4],
            [36.1,59.9,98.5,80.5],[36,62.9,96.8,80.5],[37,66.6,99.6,80.5],[37.9,65,98.1,80.6],[36.5,61.4,100.4,80.7],[36.2,64.5,94.4,80.7],[39.1,65,93.5,80.7],[36.7,68,97.8,80.7],[37.6,74.4,99.9,80.7],[37.2,74.9,96.3,80.7],
            [35,57.3,91.8,80.8],[37.5,65,100.2,80.8],[37.3,65,97.5,80.8],[37.7,77,101,80.8],[35.3,58.6,97,80.9],[39.6,65,99.2,80.9],[36.4,65.3,94.2,80.9],[36.9,68.9,100.7,80.9],[37.2,69.6,96.8,80.9],[37.2,71.4,99.7,80.9],
            [38.7,83.6,103.2,80.9],[36.3,63.6,100.6,81],[39.4,65,101.6,81],[38.5,65,103.9,81],[37.8,75.1,99.1,81],[36,62.3,97.7,81.1],[37.1,70.6,97.1,81.1],[37.9,75.6,98.5,81.1],[36.1,63.7,97.9,81.2],[40.8,65,101.3,81.2],
            [37,69.4,96.1,81.2],[37,70,104,81.2],[35.3,58.1,96.8,81.3],[39.3,65,95.9,81.3],[39.2,65,101.2,81.4],[36.3,66,97,81.4],[36.6,66.8,100.6,81.4],[37.4,71,99.7,81.5],[37.1,71.6,99.7,81.5],[37.3,73.7,100,81.5],
            [37.8,75.8,101.8,81.5],[38.4,76.1,98.7,81.5],[40.6,65,101.2,81.6],[38.5,65,99.9,81.6],[36.5,65,96.7,81.6],[37,69.7,94.8,81.6],[36.9,71.4,97.7,81.6],[37.6,73.3,98.8,81.6],[36.5,65.4,101.1,81.7],[38.2,79.3,100.7,81.7],
            [40,65,101.9,81.8],[39,65,98.5,81.8],[36.9,67.8,100.2,81.8],[37.1,70.3,101.5,81.8],[37.1,70.4,97,81.8],[37.2,71.4,99.1,81.8],[36.8,66.5,93.5,81.9],[37.7,74.3,97.7,81.9],[38.1,74.8,103.6,81.9],[38.3,80.9,102.4,81.9],
            [40.1,65,99.8,82],[38,65,99.7,82],[36.7,65.3,100.5,82],[37.1,68.3,98.9,82],[36.5,65.2,100.1,82.1],[37,69.9,103.2,82.1],[36.1,63.4,96.1,82.2],[38.8,65,102.7,82.2],[37.3,71.3,97.3,82.2],[38,76,101.9,82.2],
            [38.6,80.7,101.5,82.2],[36.7,69.1,99.1,82.3],[37.2,71.2,96.6,82.3],[37.1,71.4,97.8,82.3],[37,71.7,97,82.3],[40.1,65,104.5,82.4],[38.3,65,100.6,82.4],[38.4,74.7,98.6,82.4],[36.1,62.2,95.3,82.5],[36.1,62.2,95.3,82.5],
            [38.1,65,97.3,82.5],[39.2,65,103.7,82.5],[37.6,71.1,102.1,82.5],[37.2,71.9,97.9,82.5],[37.6,72.6,96.3,82.5],[37.6,73.7,97.6,82.5],[39.7,65,101.7,82.6],[36.4,66.6,98.3,82.6],[37.6,72.7,98.9,82.6],[38.2,80.6,99.3,82.6],
            [36.1,57,94.3,82.7],[41.3,65,101.2,82.7],[38.2,77.5,98.7,82.7],[41,65,100.7,82.8],[37,70,100.6,82.8],[37.6,72.9,99.5,82.8],[37.9,77.7,103.4,82.8],[38.3,79,98.9,82.8],[36.2,63.5,98.2,82.9],[37,68,97.8,82.9],
            [37.5,68.7,97.3,82.9],[37.6,69.4,98.8,82.9],[37.3,69.5,99.6,82.9],[37.3,71,97.3,82.9],[37.4,72.7,97.8,82.9],[37.3,72.7,97.9,82.9],[37.9,65,97.8,83],[37.4,73.2,101.2,83],[37.7,75,97.6,83],[37.9,78.6,102.2,83],
            [36.3,63.7,100.8,83.1],[36.3,63.7,100.8,83.1],[36.3,63.7,100.8,83.1],[36.3,63.7,100.8,83.1],[36.3,63.7,100.8,83.1],[36.3,64.1,100.2,83.1],[40.9,65,102.4,83.1],[41.4,65,102.9,83.1],[37,70.8,100.4,83.1],[37.8,75.7,99.3,83.1],
            [36.4,62.2,98.7,83.2],[37.1,65,99.9,83.2],[36.5,65.5,101.5,83.2],[37.5,66.4,97.9,83.2],[37.4,67.9,100.3,83.2],[37.6,74.5,100.1,83.2],[37.6,74.8,99.3,83.2],[38.2,75.8,100,83.2],[35.8,61.9,98.7,83.3],[38.8,65,100,83.3],
            [36.9,65,96.7,83.3],[36.5,66.1,100.3,83.3],[37.5,71.6,100.1,83.3],[37.2,71.7,98.8,83.3],[37.4,72.3,99.2,83.3],[36.3,62.6,99.9,83.4],[41.4,65,99.4,83.4],[38.2,65,104.8,83.4],[37.9,74.4,94.7,83.4],[38.5,80.6,100.9,83.4],
            [37.3,64.5,100.4,83.5],[37,70.5,98.8,83.5],[37.3,71,105,83.5],[37,71.6,100.6,83.5],[37.4,73.4,100.6,83.5],[36.4,61.2,97.4,83.6],[39,65,100.8,83.6],[38.6,65,102.8,83.6],[36.7,67.5,97.6,83.6],[37.2,72.5,98.9,83.6],
            [38,77.6,99.1,83.6],[37.3,71.9,96.1,83.7],[37.7,75.5,101.5,83.7],[37.7,75.6,97.5,83.7],[37.7,75.9,102.4,83.7],[37.8,76.1,99.6,83.7],[37.9,79.5,99.9,83.7],[36.2,61.1,101.1,83.8],[41.8,65,101,83.8],[38.2,65,100.6,83.8],
            [37.3,66.4,102.5,83.8],[36.5,68.1,93.9,83.8],[38,78.2,104.2,83.8],[40.4,65,103.4,83.9],[39.4,65,104.5,83.9],[37.3,65.9,100.2,83.9],[38.7,80.3,100.3,83.9],[37.1,69.8,99.6,84],[37.3,71.5,98.1,84],[37.8,71.7,102.6,84],
            [37.4,71.8,98.1,84],[38.3,82.5,102.3,84],[38,65,104.2,84.1],[36.8,68.7,97.3,84.1],[38.5,78.5,99.6,84.1],[41.5,65,102.9,84.2],[37.3,71.1,101,84.2],[37.3,72,100.6,84.2],[37.4,73.1,97.4,84.2],[37.4,76.8,94.5,84.2],
            [42.8,65,105.3,84.3],[38.1,77.6,102.9,84.3],[37.4,72.1,98.1,84.4],[38.3,65,100.8,84.5],[36.7,67.6,99.4,84.5],[37.7,72.1,98.4,84.5],[38,75.9,101.9,84.5],[37,68.8,100.6,84.6],[37.4,73.4,97.2,84.6],[37.6,73.9,99.3,84.6],
            [38,77.5,101.7,84.6],[37.8,78.5,101.5,84.6],[37.5,66.5,99.7,84.7],[36.8,67.9,94.1,84.7],[37.3,69.2,98.6,84.7],[38.2,76.9,99.7,84.7],[39.4,65,100.3,84.8],[37.5,70.7,101.4,84.8],[39.3,78.1,100.5,84.8],[38.8,81.2,98.8,84.8],
            [38.3,82.5,103.9,84.8],[40.7,65,101,84.9],[40.1,65,100,84.9],[38.4,79.9,99.6,84.9],[40.6,65,100.2,85],[37.4,73.3,99.3,85],[38.6,84.8,101,85],[41.5,65,103.8,85.1],[37.5,70.4,100.9,85.1],[37.6,73.9,99.5,85.1],
            [38.2,78,100.8,85.1],[38.3,78.8,102.1,85.1],[37,68.2,99.7,85.2],[37,71.5,98.2,85.2],[39.1,79.1,108.6,85.2],[38.3,79.7,104.3,85.2],[37.6,65,97.7,85.3],[41.9,65,100.9,85.3],[37.9,70.2,104.7,85.3],[37.4,73.2,98.3,85.3],
            [38.2,79.1,99,85.3],[38.2,80.5,101.1,85.3],[39.1,82.9,101.2,85.3],[35.9,61.7,99.6,85.5],[39.6,65,103.7,85.5],[36.7,67.5,95.1,85.5],[37.5,72.4,99.8,85.5],[37.5,72.6,105,85.5],[37.8,74.7,100.8,85.5],[37.9,74.5,101.3,85.6],
            [37.7,74.7,98.8,85.6],[39.1,82.3,102.8,85.6],[37.7,75.8,104.6,85.7],[38.9,77.2,109.8,85.7],[38.9,77.2,109.8,85.7],[38.9,77.2,109.8,85.7],[38.9,77.2,109.8,85.7],[38.9,77.2,109.8,85.7],[38.9,77.2,109.8,85.7],[38.9,77.2,109.8,85.7],
            [38.8,81.6,104.5,85.7],[39.9,65,104.5,85.8],[38.2,79.8,101,85.8],[39.6,65,98.4,85.9],[41.2,65,103.6,85.9],[39,65,100.9,85.9],[39.4,65,102.1,85.9],[37.8,67.7,100.2,85.9],[37.8,67.7,100.2,85.9],[37.8,67.7,100.2,85.9],
            [37.8,67.7,100.2,85.9],[37.5,73.3,105,85.9],[38.3,65,98.8,86],[36.7,68.6,99.6,86],[37.7,72.4,104.3,86],[37.7,75.7,100.6,86],[38.3,78.2,105.5,86],[39.1,65,106.2,86.1],[37.7,65,103.3,86.1],[37.8,76.6,101.3,86.1],
            [37.2,64.2,100.6,86.2],[38.3,78.2,100.9,86.2],[38.8,78.6,104.3,86.2],[38.1,79.4,100.9,86.2],[39.8,65,104.4,86.3],[37.2,70.7,100.9,86.3],[38.5,81.1,102.1,86.3],[39.5,86.5,104.6,86.3],[42.1,65,102,86.4],[39.6,65,104.4,86.4],
            [38.5,76.4,101,86.4],[38.3,76.5,98,86.4],[36.7,62.2,100.7,86.5],[38.9,65,101.9,86.5],[38.8,65,106.8,86.5],[40.7,65,101.5,86.7],[40.4,65,106.2,86.7],[38.4,73.1,103,86.7],[40.7,65,101.4,86.8],[38.7,82.6,104,86.8],
            [37.9,80.1,102.6,86.9],[38.7,83.1,103.4,86.9],[36.5,64.6,101.8,87],[40,65,104.1,87],[38.4,72.5,102,87],[37.9,74.8,101,87],[39.2,80.5,103,87],[38.2,80.7,103.3,87],[42.6,65,109.4,87.1],[41.7,65,101.9,87.1],
            [38.9,77.7,103,87.1],[37.4,67,100.7,87.2],[38.7,76.1,102.1,87.2],[38.7,80.3,102.5,87.3],[38.9,81.3,106.2,87.3],[39.2,86.8,102.8,87.3],[42.9,65,102.6,87.4],[38,71,106.7,87.4],[38.4,73.5,98.6,87.4],[38.7,77.4,106.2,87.4],
            [38.6,85.7,102.6,87.4],[39.4,87,104.5,87.4],[39.3,89.2,103.4,87.4],[40.2,65,101,87.5],[39.4,86.8,104.2,87.5],[39,80.3,103.7,87.6],[38.7,81,101.8,87.6],[37.8,65,101.8,87.7],[37.5,67.3,106.6,87.7],[38.1,75.1,101.1,87.7],
            [38,75.1,104.7,87.7],[39,80.4,103,87.7],[37.7,75.1,99.8,87.8],[37.5,75,95.9,87.9],[38.4,76.4,103.1,87.9],[38.7,79.5,101.8,87.9],[38.2,75.4,104.7,88],[39,83,106.8,88],[40.9,65,106,88.1],[41.1,65,105.9,88.1],
            [37.8,65,103.7,88.1],[40.9,65,107.3,88.2],[38.8,80.8,103.2,88.2],[36.9,68.6,99.5,88.3],[38.1,78.5,103.7,88.3],[40.7,65,105.7,88.4],[40.1,65,107.7,88.4],[37.6,65,99.3,88.4],[39.3,65,103.8,88.4],[37.1,69.3,99.7,88.4],
            [38.2,77.6,101.6,88.4],[40.5,65,105.9,88.5],[43,65,108.5,88.5],[38.5,81.6,103.1,88.5],[39.8,85.1,104.1,88.5],[39.2,65,102.4,88.6],[39.2,79,100.5,88.6],[39.1,84.6,102.5,88.6],[39.2,65,107.3,88.7],[39.3,82.1,101.3,88.7],
            [37.8,76.6,103.8,88.8],[38.5,82.9,106.6,88.8],[38.4,73.2,106.5,88.9],[39.2,89.1,104.6,88.9],[39.6,65,106.8,89],[42.1,65,101.3,89],[38,77.7,101.9,89.1],[38.4,81.6,103.2,89.1],[42.2,65,107.1,89.2],[41.4,65,99.8,89.2],
            [37.4,65,106.8,89.2],[38.4,80.3,102.8,89.2],[40,87.3,102.7,89.2],[38.5,73.3,101.3,89.3],[38.9,78.8,109,89.3],[38.9,78.8,109,89.3],[38.9,78.8,109,89.3],[40.1,65,111,89.4],[39.1,80.4,104.6,89.4],[38.4,81.8,105.9,89.4],
            [39.1,82.2,105.2,89.4],[39.8,65,104.5,89.5],[38.7,83.9,105.8,89.5],[38.9,85,107.2,89.5],[41.5,65,106.3,89.6],[42.6,65,102.9,89.6],[39.1,80.4,100.5,89.6],[38.9,85.8,101.5,89.6],[38.6,65,103.4,89.7],[42.9,65,108.3,89.7],
            [38.8,85.2,105.8,89.7],[36.7,66.2,100.6,89.8],[38.7,79.7,104.5,89.8],[39.7,82.1,108.3,89.8],[38.8,84.5,103.7,89.8],[38.3,79.3,101.4,89.9],[39.6,87.8,108.7,89.9],[41.7,65,106.4,90],[39.2,65,100.3,90],[41.7,65,105,90],
            [41.9,65,110.1,90.1],[41.9,65,103.3,90.1],[39.7,89.4,107.8,90.1],[42.7,65,105.3,90.2],[37.8,76.1,101.1,90.2],[39.3,86.8,105.3,90.2],[39.9,92,108.9,90.2],[41.3,65,107.5,90.3],[37.5,72.7,103.4,90.3],[38.6,81.3,101.1,90.3],
            [44.8,65,107.5,90.4],[39,77.6,105.7,90.5],[39,85.7,104.9,90.6],[37.9,70.2,100.5,90.7],[41.7,65,101.3,90.8],[38.8,65,100.1,90.8],[38.1,78.4,101.8,90.8],[38.7,78.6,104,90.8],[39.3,82.2,101.9,90.8],[44.8,65,103.2,90.9],
            [38.8,82,101.2,90.9],[43.1,65,105.9,91],[38.8,80,99.7,91],[39.3,86.1,103.5,91.1],[39,84.2,106.5,91.2],[39.5,84.7,106.3,91.2],[40.2,65,104,91.3],[39.5,65,104.8,91.4],[41.5,65,111.4,91.6],[38.4,90.1,108.3,91.6],
            [41.4,65,106,91.7],[40.5,65,102.7,91.7],[37.9,72.9,103.2,91.7],[41.3,65,106,91.8],[44.3,65,111.8,91.8],[39.5,86.4,100.4,91.9],[39.4,82.6,106.1,92],[40.1,86.6,108.2,92],[40.4,65,98.6,92.1],[38.4,65,108.1,92.1],
            [39,85.9,102.6,92.1],[40.1,90.8,109.3,92.1],[41.2,100.6,109.8,92.1],[40.1,94,107.3,92.3],[41.9,65,107.7,92.4],[39.3,81.5,110,92.4],[43.3,65,107.3,92.5],[41.9,65,108.4,92.6],[41.1,65,107.8,92.6],[38.7,79.6,106.8,92.6],
            [42.4,65,104.2,92.7],[44,65,108.9,92.8],[40,65,105,92.8],[39.8,86.2,105.6,92.8],[41.5,65,106.6,93],[40.6,87.5,113.8,93.1],[39.6,90.8,107.4,93.1],[39.6,83.6,104.3,93.2],[39.7,83.8,110,93.2],[42.8,65,107.2,93.3],
            [40.2,65,108,93.4],[43.1,65,108.9,93.5],[40.9,65,108.3,93.5],[39.2,83.4,101.6,93.5],[38.6,65,106.1,93.6],[42.6,65,103.9,93.8],[43.1,65,104.4,93.8],[39.1,84.4,104.9,93.9],[41.2,65,103,94.1],[38.4,71,108.1,94.1],
            [45.8,65,106.1,94.2],[40.3,87.4,106.9,94.3],[40.1,65,104.1,94.4],[40,65,112.6,94.5],[41.5,65,107.4,94.5],[40.6,65,107,94.5],[40.2,88.5,108.4,94.6],[43.4,65,111,94.9],[39.3,85.5,104,94.9],[40,92.5,106.5,94.9],
            [42.2,65,113.5,95],[39.5,87.8,104.4,95.1],[38.6,65,109.1,95.2],[45.9,65,117,95.3],[39.3,85.6,106.4,95.3],[45.8,65,103.7,95.4],[42.5,65,110.9,95.4],[41.7,65,105.5,95.4],[39.3,87,104.8,95.5],[40,88,106.5,95.5],
            [39.8,65,104.1,95.6],[40.1,87,106.9,95.6],[39.9,88.3,104.6,95.6],[41.9,65,104.7,95.7],[40.2,93.2,110.4,95.9],[42,65,107.6,96],[40.7,65,110.5,96],[39.3,65,109.4,96.1],[43.4,65,112.1,96.2],[40.8,65,108.4,96.4],
            [40,92.2,108.5,96.4],[39.4,77.6,107.1,96.5],[40.2,93.2,103.2,96.6],[41.7,99.4,111.6,96.6],[43.9,65,109.5,96.8],[43.3,65,112.5,96.8],[38.4,81.8,105.6,96.8],[40.5,65,108,96.9],[39.2,81.1,107.6,96.9],[39.9,84.2,103.5,96.9],
            [39.8,86.4,103.3,96.9],[40.8,100.2,111,96.9],[40.4,95.8,107.9,97.1],[40.1,90.3,109.5,97.2],[42.2,65,109.5,97.3],[40.1,93.7,105.7,97.3],[42.9,65,107,97.4],[39.2,81.6,104.5,97.4],[40.8,65,107.5,97.7],[39.4,76.8,109.7,97.7],
            [40.6,65,111.6,97.8],[42.3,65,109.4,97.8],[43,65,99.7,98.6],[43.1,65,106.5,99.1],[40.5,94.2,107.1,99.2],[40.5,65,113.2,99.3],[43.4,65,114.8,99.6],[46.1,65,115.5,100.4],[42.3,65,108.5,100.4],[41.1,97.6,110.2,100.4],
            [40.6,65,113,100.7],[40.6,98.9,112.7,100.9],[40,92.2,102.7,101.2],[41.2,103.6,111.6,101.6],[40.8,65,112.2,101.7],[41.7,101.6,109.8,101.8],[40.2,103.7,111,102],[40.2,65,107.5,102.3],[41.4,102.7,112.4,102.7],[46.2,65,117.2,102.9],
            [45.9,65,114.1,103.2],[45.1,65,118.3,104.1],[44.7,65,117.5,105],[45.7,65,112.4,105.4],[47.7,65,112.5,105.7],[40.8,90,109.8,107.1],[44.6,113.1,112.4,107.3],[41.8,104.8,116.6,108.2],[44.2,65,114.5,108.7],[46.6,65,118.1,110],
            [46.7,65,119.4,110.1],[42.9,65,114.6,110.5],[42.8,65,110.5,110.5]
        ];

        // 변수 설정: 이름·단위·축 범위를 바꾸려면 여기만 고치면 됩니다.
        const VARS = [
            { name: '목둘레',     short: '목',     unit: 'cm', min: 30, max: 50,  dtick: 5 },
            { name: '몸무게',     short: '몸무게', unit: 'kg', min: 40, max: 120, dtick: 20 },
            { name: '엉덩이둘레', short: '엉덩이', unit: 'cm', min: 80, max: 125, dtick: 10 }
        ];
        const TARGET = { name: '허리둘레', short: '허리', unit: 'cm', min: 60, max: 115, dtick: 10 };
        const PAIRS = [[0, 1], [0, 2], [1, 2]];      // 그래프에 그릴 수 있는 두 변수 짝
        const SUB = ['₁', '₂', '₃'];
        const DEFAULT_CAMERA = {
            eye: { x: 1.6, y: -1.6, z: 0.75 },
            center: { x: 0, y: 0, z: -0.12 },
            up: { x: 0, y: 0, z: 1 }
        };
        const PLANE_GRID = 7;
        const DIVERGE_MSE = 1e7;

        // 학습은 전체 데이터의 평균·표준편차로 표준화한 값으로 진행하고(a, c), 화면에는 실제 단위의 w, b로 보여줍니다.
        const NORM = (() => {
            const n = JEANS.length;
            const mean = [0, 1, 2, 3].map(j => JEANS.reduce((s, r) => s + r[j], 0) / n);
            const sd = [0, 1, 2, 3].map(j => Math.sqrt(JEANS.reduce((s, r) => s + (r[j] - mean[j]) ** 2, 0) / n));
            return { mean, sd };
        })();

        const state = {
            points: [],          // { x: [목, 몸무게, 엉덩이], y: 허리 }
            pair: 1,             // 그래프에 그릴 짝 (기본: 목둘레 × 엉덩이둘레)
            mode: 'pair',        // 'pair' = 그래프의 2개만 학습, 'all' = 3개 모두 학습
            a: [0, 0, 0],
            c: 0,
            showResiduals: true,
            epochs: 300,
            totalEpochs: 0,
            lr: 0.01,           // 처음에는 작게: 학습이 천천히 진행되는 모습을 볼 수 있음
            isTraining: false,
            diverged: false,
            query: null          // { x: [3], y: 예측값 }
        };

        const $ = (id) => document.getElementById(id);
        const elements = {
            plot: $('plot3d'),
            plotFallback: $('plot-fallback'),
            pointCount: $('point-count'),
            toggleResiduals: $('toggle-residuals'),
            coordInput: $('coord-input'),
            coordHint: $('coord-hint'),
            coordFeedback: $('coord-feedback'),
            statusTag: $('status-tag'),
            metricMSE: $('metric-mse'),
            metricRMSE: $('metric-rmse'),
            metricR2: $('metric-r2'),
            equationDisplay: $('equation-display'),
            coefExplain: $('coef-explain')
        };

        // ---------------- 모델 ----------------
        const activeVars = () => (state.mode === 'all' ? [0, 1, 2] : PAIRS[state.pair]);
        const shownVars = () => PAIRS[state.pair];

        function getParams() {
            const w = state.a.map((a, j) => a * NORM.sd[3] / NORM.sd[j]);
            const b = NORM.mean[3] + NORM.sd[3] * state.c - w.reduce((s, wj, j) => s + wj * NORM.mean[j], 0);
            return { w, b };
        }

        function predict(x) {
            const { w, b } = getParams();
            return activeVars().reduce((s, j) => s + w[j] * x[j], b);
        }

        // 그래프에 보이지 않는 세 번째 변수의 고정값 (지금 데이터의 평균)
        function hiddenVar() {
            const j = [0, 1, 2].find(v => !shownVars().includes(v));
            const pts = state.points.length ? state.points : JEANS.map(r => ({ x: r }));
            const mean = pts.reduce((s, p) => s + p.x[j], 0) / pts.length;
            return { j, mean };
        }

        function calculateMSE() {
            if (state.points.length === 0) return 0;
            return state.points.reduce((s, p) => s + (p.y - predict(p.x)) ** 2, 0) / state.points.length;
        }

        function calculateR2() {
            if (state.points.length <= 1) return 0;
            const yMean = state.points.reduce((s, p) => s + p.y, 0) / state.points.length;
            let sst = 0, sse = 0;
            state.points.forEach(p => {
                sst += (p.y - yMean) ** 2;
                sse += (p.y - predict(p.x)) ** 2;
            });
            if (sst === 0) return 1;
            return Math.max(0, 1 - sse / sst);
        }

        function stepGradientDescent() {
            const N = state.points.length;
            if (N === 0) return;
            const act = activeVars();
            const g = [0, 0, 0];
            let gc = 0;
            state.points.forEach(p => {
                const u = p.x.map((v, j) => (v - NORM.mean[j]) / NORM.sd[j]);
                const v = (p.y - NORM.mean[3]) / NORM.sd[3];
                const err = act.reduce((s, j) => s + state.a[j] * u[j], state.c) - v;
                act.forEach(j => { g[j] += (2 / N) * err * u[j]; });
                gc += (2 / N) * err;
            });
            act.forEach(j => { state.a[j] -= state.lr * g[j]; });
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

        // 최소제곱법으로 '도달 가능한 최고 R²' 계산 (정규방정식을 가우스 소거법으로 풀기)
        function bestR2(vars) {
            const pts = state.points;
            if (pts.length <= vars.length + 1) return null;
            const k = vars.length + 1;
            const A = Array.from({ length: k }, () => new Array(k + 1).fill(0));
            pts.forEach(p => {
                const row = [...vars.map(j => (p.x[j] - NORM.mean[j]) / NORM.sd[j]), 1];
                for (let r = 0; r < k; r++) {
                    for (let c = 0; c < k; c++) A[r][c] += row[r] * row[c];
                    A[r][k] += row[r] * p.y;
                }
            });
            for (let col = 0; col < k; col++) {
                let piv = col;
                for (let r = col + 1; r < k; r++) if (Math.abs(A[r][col]) > Math.abs(A[piv][col])) piv = r;
                [A[col], A[piv]] = [A[piv], A[col]];
                if (Math.abs(A[col][col]) < 1e-12) return null;
                for (let r = 0; r < k; r++) {
                    if (r === col) continue;
                    const f = A[r][col] / A[col][col];
                    for (let c = col; c <= k; c++) A[r][c] -= f * A[col][c];
                }
            }
            const beta = A.map((row, i) => row[k] / row[i]);
            const yMean = pts.reduce((s, p) => s + p.y, 0) / pts.length;
            let sst = 0, sse = 0;
            pts.forEach(p => {
                const row = [...vars.map(j => (p.x[j] - NORM.mean[j]) / NORM.sd[j]), 1];
                const yhat = row.reduce((s, v, i) => s + v * beta[i], 0);
                sst += (p.y - yMean) ** 2;
                sse += (p.y - yhat) ** 2;
            });
            return sst === 0 ? null : Math.max(0, 1 - sse / sst);
        }

        // ---------------- 3D 그래프 ----------------
        function axisStyle(axis) {
            return {
                title: { text: `${axis.name} (${axis.unit})`, font: { size: 12, color: '#e2e8f0' } },
                range: [axis.min, axis.max],
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

        function plotLayout() {
            const [i, j] = shownVars();
            return {
                paper_bgcolor: '#0f172a',
                margin: { l: 0, r: 0, t: 0, b: 0 },
                showlegend: false,
                font: { family: "'Noto Sans KR', sans-serif", color: '#cbd5e1' },
                hoverlabel: { bgcolor: '#1e1b4b', bordercolor: '#818cf8', font: { color: '#ffffff', size: 12 } },
                scene: {
                    xaxis: axisStyle(VARS[i]),
                    yaxis: axisStyle(VARS[j]),
                    zaxis: axisStyle(TARGET),
                    aspectmode: 'cube',
                    dragmode: 'turntable',
                    camera: DEFAULT_CAMERA
                }
            };
        }

        const plotConfig = { responsive: true, displaylogo: false, displayModeBar: false, scrollZoom: true };

        function gridValues(axis) {
            return Array.from({ length: PLANE_GRID }, (_, i) => axis.min + i * (axis.max - axis.min) / (PLANE_GRID - 1));
        }

        // 평면 위의 높이: 그래프에 안 보이는 변수는 평균값으로 고정
        function planeHeight(vi, vj, i, j) {
            const x = [0, 0, 0];
            const hv = hiddenVar();
            x[hv.j] = hv.mean;
            x[i] = vi; x[j] = vj;
            return predict(x);
        }

        function buildTraces() {
            const pts = state.points;
            const [i, j] = shownVars();
            const hasPoints = pts.length > 0;
            const planeOk = hasPoints && !state.diverged;
            const traces = [];

            traces.push({
                type: 'scatter3d',
                mode: 'markers',
                x: pts.map(p => p.x[i]),
                y: pts.map(p => p.x[j]),
                z: pts.map(p => p.y),
                customdata: pts.map(p => [p.x[0], p.x[1], p.x[2]]),
                marker: { size: pts.length > 300 ? 3.2 : 5, color: '#3b82f6', opacity: pts.length > 300 ? 0.75 : 1, line: { color: '#ffffff', width: pts.length > 300 ? 0.5 : 1.5 } },
                hovertemplate: `목 %{customdata[0]}cm · 몸무게 %{customdata[1]}kg · 엉덩이 %{customdata[2]}cm<br>허리 %{z}cm<extra></extra>`
            });

            // 오차 선: 2개 모드에서만 (3개 모드의 예측값은 그려진 평면 위에 있지 않음)
            const rx = [], ry = [], rz = [];
            if (state.showResiduals && planeOk && state.mode === 'pair') {
                pts.forEach(p => {
                    rx.push(p.x[i], p.x[i], null);
                    ry.push(p.x[j], p.x[j], null);
                    rz.push(p.y, predict(p.x), null);
                });
            }
            traces.push({
                type: 'scatter3d',
                mode: 'lines',
                x: rx, y: ry, z: rz,
                line: { color: '#f43f5e', width: pts.length > 300 ? 2 : 4, dash: 'dash' },
                opacity: pts.length > 300 ? 0.6 : 1,
                connectgaps: false,
                hoverinfo: 'skip'
            });

            const gx = gridValues(VARS[i]);
            const gy = gridValues(VARS[j]);
            const gz = gy.map(vj => gx.map(vi => planeHeight(vi, vj, i, j)));
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

            // 예측해 본 사람
            const q = state.query;
            traces.push({
                type: 'scatter3d',
                mode: 'markers',
                x: q ? [q.x[i]] : [], y: q ? [q.x[j]] : [], z: q ? [predict(q.x)] : [],
                marker: { size: 9, color: '#facc15', symbol: 'diamond', line: { color: '#0f172a', width: 2 } },
                hovertemplate: `예측한 허리 %{z:.1f}cm<extra></extra>`
            });

            return traces;
        }

        function renderPlot(newAxes = false) {
            if (!window.Plotly) return;
            const layout = plotLayout();
            layout.uirevision = `axes-${state.pair}`;   // 회전한 시점은 유지하고, 짝이 바뀌면 시점도 새로
            Plotly.react(elements.plot, buildTraces(), layout, plotConfig);
        }

        function resetView() {
            if (!window.Plotly) return;
            Plotly.relayout(elements.plot, { 'scene.camera': JSON.parse(JSON.stringify(DEFAULT_CAMERA)) });
        }

        // ---------------- 화면 갱신 ----------------
        const fmt = (v, d = 2) => (Number.isFinite(v) ? v.toFixed(d) : '발산');

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

        function describeEffect(w, j) {
            const v = VARS[j];
            const others = activeVars().filter(k => k !== j).map(k => VARS[k].name).join('·');
            const cond = others ? `${others}가 같을 때, ` : '';
            if (Math.abs(w) < 0.05) {
                return `${cond}${v.name}가 1${v.unit} 늘어도 허리둘레는 <strong>거의 변하지 않아요</strong> (약 ${w >= 0 ? '+' : '-'}${Math.abs(w).toFixed(2)}cm).`;
            }
            return `${cond}${v.name}가 1${v.unit} 늘면 허리둘레가 약 <strong>${Math.abs(w).toFixed(2)}cm ${w > 0 ? '늘어나요' : '줄어들어요'}</strong>.`;
        }

        function updateControlsUI() {
            const [i, j] = shownVars();
            $('pair-btns').innerHTML = PAIRS.map(([a, b], k) => `<button data-pair="${k}" class="px-3 py-1.5 rounded-md font-semibold transition ${k === state.pair ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-600 hover:text-indigo-600'}">${VARS[a].short} × ${VARS[b].short}</button>`).join('');
            document.querySelectorAll('.mode-btn').forEach(btn => {
                const on = btn.dataset.mode === state.mode;
                btn.className = `mode-btn p-2 rounded-xl border font-semibold transition ${on ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm' : 'bg-white text-slate-600 border-slate-200 hover:border-indigo-300'}`;
                if (btn.dataset.mode === 'pair') btn.textContent = `그래프의 2개만 (${VARS[i].short}, ${VARS[j].short})`;
            });

            const hv = hiddenVar();
            const note = $('slice-note');
            if (state.mode === 'all') {
                note.classList.remove('hidden');
                note.innerHTML = `⭐ <strong>3개 모두 사용 중</strong>: AI는 ${VARS[hv.j].name}까지 함께 써서 예측해요. 화면의 평면은 ${VARS[hv.j].name}를 평균 <strong>${hv.mean.toFixed(1)}${VARS[hv.j].unit}</strong>로 고정해서 자른 단면이에요. 실제 예측값은 이 평면 위에 있지 않아서 오차 선은 숨겼어요.`;
            } else {
                note.classList.add('hidden');
            }
            elements.toggleResiduals.disabled = state.mode === 'all';
            elements.toggleResiduals.parentElement.classList.toggle('opacity-40', state.mode === 'all');

            // 예측 입력칸: 학습에 안 쓰는 변수는 흐리게
            document.querySelectorAll('#query-inputs input').forEach(inp => {
                const used = activeVars().includes(parseInt(inp.dataset.var, 10));
                inp.disabled = !used;
                inp.parentElement.classList.toggle('opacity-40', !used);
            });
        }

        function updateMetricsUI() {
            const { w, b } = getParams();
            const act = activeVars();
            const mse = calculateMSE();
            const r2 = calculateR2();

            elements.pointCount.textContent = `${state.points.length}명`;
            $('weight-cards').innerHTML = [0, 1, 2].map(j => {
                const used = act.includes(j);
                return `<div class="p-2.5 border rounded-xl ${used ? 'bg-slate-50 border-slate-200' : 'bg-slate-50/40 border-dashed border-slate-200 opacity-50'}">
                    <span class="text-[11px] text-slate-500 font-semibold block mb-0.5 break-keep">w${SUB[j]} (${VARS[j].short})</span>
                    <span class="text-base font-extrabold ${used ? 'text-indigo-600' : 'text-slate-400'} font-mono">${used ? fmt(w[j]) : '사용 안 함'}</span>
                </div>`;
            }).join('') + `<div class="p-2.5 bg-slate-50 border border-slate-200 rounded-xl">
                    <span class="text-[11px] text-slate-500 font-semibold block mb-0.5">b (절편)</span>
                    <span class="text-base font-extrabold text-indigo-600 font-mono">${fmt(b)}</span>
                </div>`;
            elements.metricMSE.textContent = state.diverged ? '발산' : mse.toFixed(2);
            elements.metricRMSE.textContent = state.diverged || !state.points.length ? '' : `→ 평균적으로 약 ${Math.sqrt(mse).toFixed(1)}cm 정도 틀려요`;
            elements.metricR2.textContent = state.diverged ? '-' : r2.toFixed(4);
            $('cumulative-val').textContent = state.totalEpochs;

            $('equation-label').textContent = act.length === 3 ? '현재 AI 방정식 (y = w₁x₁ + w₂x₂ + w₃x₃ + b)' : '현재 AI 방정식 (y = w·x + w·x + b)';
            elements.equationDisplay.textContent = state.diverged
                ? '값이 너무 커져서 식을 표시할 수 없어요'
                : `허리 = ${act.map((j, k) => `${k === 0 ? w[j].toFixed(2) : signed(w[j])} × ${VARS[j].short}`).join(' ')} ${signed(b)}`;

            let explain;
            if (state.diverged) {
                explain = `<div>⚠️ 학습이 발산했어요. <strong>모델 초기화</strong>를 누르고 학습률을 낮춰서 다시 학습해 보세요.</div>`;
            } else if (state.points.length === 0) {
                explain = `<div>💡 데이터를 넣고 학습을 시작해 보세요.</div>`;
            } else if (state.totalEpochs === 0) {
                explain = `<div>💡 학습을 시작하면 각 변수가 허리둘레에 주는 영향을 풀어서 설명해 드려요.</div>`;
            } else {
                explain = `<div class="font-bold text-indigo-700 mb-0.5"><i class="fa-solid fa-comment-dots mr-1"></i>AI가 찾은 규칙 해석하기</div>`
                    + act.map(j => `<div>• ${describeEffect(w[j], j)}</div>`).join('');
            }
            elements.coefExplain.innerHTML = explain;

            updateComboChart(r2);
            updateQueryResult();
        }

        // 조합별 최고 R² 막대그래프 (데이터가 바뀔 때만 다시 계산)
        let comboCache = { key: '', values: [] };
        function updateComboChart(currentR2) {
            const key = `${state.points.length}:${state.points.length ? state.points[state.points.length - 1].y : ''}:${state.points.reduce((s, p) => s + p.y, 0).toFixed(3)}`;
            const combos = [...PAIRS.map(p => p.slice()), [0, 1, 2]];
            if (comboCache.key !== key) comboCache = { key, values: combos.map(c => bestR2(c)) };
            const act = activeVars().join(',');
            const cur = state.diverged ? null : currentR2;
            $('combo-chart').innerHTML = combos.map((c, k) => {
                const v = comboCache.values[k];
                const on = c.join(',') === act;
                const label = c.length === 3 ? '⭐ 3개 모두' : c.map(j => VARS[j].short).join(' + ');
                return `<div class="flex items-center gap-2 text-xs">
                    <span class="w-24 shrink-0 font-semibold ${on ? 'text-indigo-700' : 'text-slate-600'}">${label}</span>
                    <div class="relative flex-grow h-5 bg-slate-100 rounded-md overflow-hidden ${on ? 'ring-2 ring-indigo-400' : ''}">
                        <div class="h-full ${on ? 'bg-indigo-500' : 'bg-slate-300'}" style="width:${v === null ? 0 : (v * 100).toFixed(1)}%"></div>
                        ${on && cur !== null ? `<div class="absolute top-0 bottom-0 w-1 bg-yellow-400" style="left:calc(${(cur * 100).toFixed(1)}% - 2px)" title="지금 AI의 R²"></div>` : ''}
                    </div>
                    <span class="w-14 text-right font-mono ${on ? 'text-indigo-700 font-bold' : 'text-slate-500'}">${v === null ? '-' : v.toFixed(3)}</span>
                </div>`;
            }).join('') + `<p class="text-[11px] text-slate-500 mt-1 break-keep">${state.totalEpochs === 0 ? '학습을 시작하면 노란 선(지금 AI)이 막대 끝(최고 R²)을 향해 다가가요.' : '노란 선이 막대 끝에 가까울수록 학습이 거의 끝난 거예요.'}</p>`;
        }

        function refresh(newAxes = false) {
            updateControlsUI();
            updateMetricsUI();
            renderPlot(newAxes);
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
            state.a = [0, 0, 0];
            state.c = 0;
            state.totalEpochs = 0;
            state.isTraining = false;
            state.diverged = false;
            setStatus('idle');
            refresh();
            if (showMessage) showToast("가중치 및 누적 에포크가 초기화되었습니다.");
        }

        function setPair(k) {
            if (k === state.pair) return;
            const wasPair = state.mode === 'pair';
            state.pair = k;
            if (wasPair) {
                // 2개 모드에서는 짝이 바뀌면 다른 모델이 되므로 새로 학습
                state.a = [0, 0, 0]; state.c = 0; state.totalEpochs = 0; state.diverged = false; state.isTraining = false;
                setStatus('idle');
                showToast(`${VARS[PAIRS[k][0]].name}·${VARS[PAIRS[k][1]].name}로 새 모델을 만들었어요. 학습을 시작해 보세요.`);
            }
            refresh(true);
        }

        function setMode(mode) {
            if (mode === state.mode) return;
            state.mode = mode;
            resetModel(false);
            showToast(mode === 'all' ? '3개 변수를 모두 써서 새로 학습해요. 다른 가중치들이 어떻게 바뀌는지 보세요!' : '그래프의 두 변수만 써서 새로 학습해요.');
        }

        // ---------------- 예시 데이터 ----------------
        // seed를 주면 항상 같은 사람들을 뽑음 (첫 화면용), 없으면 누를 때마다 새로 뽑음
        function loadPreset(n, seed = null) {
            hideCoordFeedback();
            const rows = JEANS.slice();
            let s = seed;
            const rand = seed === null ? Math.random : () => {   // 간단한 시드 난수 (mulberry32)
                s = (s + 0x6D2B79F5) | 0;
                let t = Math.imul(s ^ (s >>> 15), 1 | s);
                t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
                return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
            };
            if (n < rows.length) {
                for (let i = rows.length - 1; i > 0; i--) {
                    const k = Math.floor(rand() * (i + 1));
                    [rows[i], rows[k]] = [rows[k], rows[i]];
                }
            }
            state.points = rows.slice(0, n).map(r => ({ x: [r[0], r[1], r[2]], y: r[3] }));
            resetModel(false);
            if (seed === null) showToast(n >= JEANS.length ? "전체 데이터(963명)를 불러왔어요." : `무작위로 ${n}명을 뽑았어요.`);
        }

        // ---------------- 새 사람 예측 ----------------
        function buildQueryInputs() {
            $('query-inputs').innerHTML = VARS.map((v, j) => `
                <label class="block">
                    <span class="text-[11px] font-semibold text-slate-600 block mb-0.5">${v.name} (${v.unit})</span>
                    <input type="number" step="0.1" data-var="${j}" value="${NORM.mean[j].toFixed(1)}"
                        class="w-full px-2 py-1.5 rounded-lg border border-slate-300 bg-slate-50 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:cursor-not-allowed">
                </label>`).join('');
        }

        function runQuery() {
            const x = [...document.querySelectorAll('#query-inputs input')].map(inp => parseFloat(inp.value));
            const bad = activeVars().filter(j => !Number.isFinite(x[j]) || x[j] < VARS[j].min || x[j] > VARS[j].max);
            if (bad.length) {
                return showToast(`${bad.map(j => `${VARS[j].name}는 ${VARS[j].min}~${VARS[j].max}${VARS[j].unit}`).join(', ')} 사이로 입력해 주세요.`, 'warning');
            }
            [0, 1, 2].forEach(j => { if (!Number.isFinite(x[j])) x[j] = NORM.mean[j]; });
            state.query = { x };
            refresh();
        }

        function updateQueryResult() {
            const box = $('query-result');
            if (!state.query) { box.classList.add('hidden'); return; }
            const { w, b } = getParams();
            const act = activeVars();
            const yhat = predict(state.query.x);
            box.classList.remove('hidden');
            if (state.diverged) { box.innerHTML = '⚠️ 학습이 발산해서 예측할 수 없어요.'; return; }
            box.innerHTML = `<div class="text-sm font-extrabold text-slate-800">예측 허리둘레: <span class="text-indigo-700">${yhat.toFixed(1)}cm</span> <span class="text-xs font-semibold text-slate-500">(청바지 약 ${(yhat / 2.54).toFixed(1)}인치)</span></div>`
                + `<div class="font-mono text-[11px] text-slate-600 mt-1">= ${act.map(j => `${w[j].toFixed(2)}×${state.query.x[j]}`).join(' + ')} ${signed(b)}</div>`
                + (state.totalEpochs === 0 ? `<div class="text-[11px] text-amber-700 mt-1">아직 학습 전이라 모두에게 비슷한 값을 예측해요. 학습 후 다시 확인해 보세요.</div>` : '')
                + (state.mode === 'all' ? `<div class="text-[11px] text-slate-500 mt-1">3개 모드에서는 노란 ◆가 평면(평균 단면) 위에 있지 않을 수 있어요.</div>` : '');
        }

        // ---------------- 데이터 직접 입력 ----------------
        const NUMBER_PATTERN = /^[-+]?(?:\d+\.?\d*|\.\d+)$/;
        const N_VALUES = 4;

        // 입력 문자열 → { points: [{x, y, raw}], invalid: [원문 조각] }
        function parseCoordinateText(text) {
            const normalized = text
                .replace(/（/g, '(')
                .replace(/）/g, ')')
                .replace(/，/g, ',');

            const points = [];
            const invalid = [];
            let pending = []; // 괄호 없이 입력된 숫자를 4개씩 모으는 중

            const flushPending = () => {
                if (pending.length) {
                    invalid.push(pending.map(t => t.raw).join(','));
                    pending = [];
                }
            };
            const toPoint = (vals, raw) => ({ x: vals.slice(0, 3), y: vals[3], raw });

            // ① (괄호 묶음)  ② 괄호·쉼표·공백이 아닌 덩어리  ③ 짝이 맞지 않는 괄호
            const tokenPattern = /\(([^()]*)\)|[^\s,;()]+|[()]/g;
            let match;
            while ((match = tokenPattern.exec(normalized)) !== null) {
                const token = match[0];
                if (match[1] !== undefined) {
                    flushPending();
                    const parts = match[1].split(/[\s,;]+/).filter(Boolean);
                    if (parts.length === N_VALUES && parts.every(t => NUMBER_PATTERN.test(t))) {
                        points.push(toPoint(parts.map(parseFloat), token));
                    } else {
                        invalid.push(token);
                    }
                } else if (token === '(' || token === ')') {
                    continue;
                } else if (NUMBER_PATTERN.test(token)) {
                    pending.push({ value: parseFloat(token), raw: token });
                    if (pending.length === N_VALUES) {
                        points.push(toPoint(pending.map(t => t.value), pending.map(t => t.raw).join(',')));
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

        const inRange = (v, axis) => v >= axis.min && v <= axis.max;
        const isPointInRange = (p) => p.x.every((v, j) => inRange(v, VARS[j])) && inRange(p.y, TARGET);

        function formatPoint(p) {
            const f = (v) => String(Math.round(v * 100) / 100);
            return `(${p.x.map(f).join(', ')}, ${f(p.y)})`;
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
            return [...VARS, TARGET].map(v => `${v.name} ${v.min}~${v.max}${v.unit}`).join(', ');
        }

        function hideCoordFeedback() {
            elements.coordFeedback.classList.add('hidden');
            elements.coordFeedback.innerHTML = '';
        }

        function renderCoordFeedback(accepted, outOfRange, invalid) {
            const lines = [];
            if (accepted.length) {
                lines.push(`✅ <strong>${accepted.length}명</strong>을 추가했어요: <span class="font-mono">${escapeHtml(summarizeList(accepted.map(formatPoint)))}</span>`);
            }
            if (outOfRange.length) {
                lines.push(`⚠️ 범위를 벗어나서 추가하지 않았어요: <span class="font-mono">${escapeHtml(summarizeList(outOfRange.map(formatPoint)))}</span> <span class="opacity-75">(${escapeHtml(rangeText())})</span>`);
            }
            if (invalid.length) {
                lines.push(`❌ 데이터로 읽을 수 없는 입력이에요: <span class="font-mono">${escapeHtml(summarizeList(invalid))}</span> <span class="opacity-75">(목둘레, 몸무게, 엉덩이둘레, 허리둘레 네 수를 짝지어 입력하세요. 예: (36,62,96,78))</span>`);
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
                showToast("데이터를 입력해 주세요. 예) (36,62,96,78)", "warning");
                elements.coordInput.focus();
                return;
            }

            const { points, invalid } = parseCoordinateText(text);
            if (points.length === 0 && invalid.length === 0) invalid.push(text.trim());

            const accepted = [];
            const outOfRange = [];
            points.forEach(p => (isPointInRange(p) ? accepted : outOfRange).push(p));

            if (accepted.length) {
                accepted.forEach(p => state.points.push({ x: p.x, y: p.y }));
                refresh();
            }

            renderCoordFeedback(accepted, outOfRange, invalid);
            elements.coordInput.value = [...outOfRange.map(p => p.raw), ...invalid].join(' ');
            elements.coordInput.focus();

            if (!outOfRange.length && !invalid.length) {
                showToast(`${accepted.length}명을 추가했어요.`);
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
            `<i class="fa-solid fa-circle-info mr-1 text-slate-400"></i>순서는 <strong class="text-indigo-600">(목둘레 cm, 몸무게 kg, 엉덩이둘레 cm, 허리둘레 cm)</strong>이에요. `
            + `<span class="whitespace-nowrap"><kbd>Enter</kbd> 추가</span> · <span class="whitespace-nowrap"><kbd>Shift</kbd>+<kbd>Enter</kbd> 줄바꿈</span> · 여러 명은 띄어쓰기나 줄바꿈으로 구분`;

        $('reset-view-btn').addEventListener('click', resetView);

        $('undo-btn').addEventListener('click', () => {
            if (state.points.length === 0) return showToast("삭제할 점이 없어요.", "warning");
            const removed = state.points.pop();
            refresh();
            showToast(`마지막 점 ${formatPoint(removed)}을 삭제했어요.`);
        });

        $('clear-btn').addEventListener('click', () => {
            state.points = [];
            hideCoordFeedback();
            resetModel(false);
            showToast("모든 데이터 점이 삭제되었습니다.");
        });

        elements.toggleResiduals.addEventListener('change', (e) => {
            state.showResiduals = e.target.checked;
            renderPlot();
        });

        $('pair-btns').addEventListener('click', (e) => {
            const btn = e.target.closest('button[data-pair]');
            if (btn) setPair(parseInt(btn.dataset.pair, 10));
        });
        document.querySelectorAll('.mode-btn').forEach(btn => btn.addEventListener('click', () => setMode(btn.dataset.mode)));

        $('epochs-slider').addEventListener('input', (e) => {
            state.epochs = parseInt(e.target.value, 10);
            $('epochs-val').textContent = `${state.epochs}회`;
        });

        $('lr-slider').addEventListener('input', (e) => {
            state.lr = parseFloat(e.target.value);
            $('lr-val').textContent = state.lr.toFixed(2);
        });

        $('train-btn').addEventListener('click', startTraining);
        $('step-btn').addEventListener('click', stepOnce);
        $('reset-model-btn').addEventListener('click', () => resetModel(true));

        $('preset-all').addEventListener('click', () => loadPreset(JEANS.length));
        $('preset-200').addEventListener('click', () => loadPreset(200));
        $('preset-50').addEventListener('click', () => loadPreset(50));
        $('preset-10').addEventListener('click', () => loadPreset(10));

        $('query-btn').addEventListener('click', runQuery);
        $('query-clear-btn').addEventListener('click', () => { state.query = null; refresh(); });

        $('coord-add-btn').addEventListener('click', addPointsFromInput);
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
            buildQueryInputs();
            // 첫 화면: 보기 편하도록 963명 중 50명만 (수업에서 모두 같은 화면을 보도록 항상 같은 50명)
            loadPreset(50, 2024);
        };
    </script>

    <script>
        // 상단 단계 메뉴 클릭 → 스트림릿 왼쪽 사이드바의 같은 메뉴를 대신 눌러서 페이지 이동
        //  - st.iframe 은 보안상 교구 화면이 바깥 페이지 주소를 직접 바꾸지 못해서 이 방법을 씁니다.
        //  - 사이드바 메뉴를 찾지 못하면 a 태그의 기본 링크(href)로 이동합니다.
        document.querySelectorAll('nav a[data-page]').forEach(a => a.addEventListener('click', (e) => {
            try {
                const links = window.parent.document.querySelectorAll('a[data-testid="stSidebarNavLink"]');
                const target = [...links].find(l => new URL(l.href).pathname.replace(/\/$/, '').split('/').pop() === a.dataset.page);
                if (target) {
                    e.preventDefault();
                    target.click();
                }
            } catch (err) { /* 바깥 페이지에 접근할 수 없으면 기본 링크 동작 사용 */ }
        }));
    </script>
</body>
</html>
"""

# HTML을 화면에 배치
#  - streamlit 1.56 이상: st.iframe 사용 (내용 높이에 맞춰 화면 높이가 자동으로 조절됨)
#  - 그보다 낮은 버전: 예전 방식인 components.html 사용 (고정 높이 1700px + 스크롤)
if hasattr(st, "iframe"):
    st.iframe(html_code, height="content")
else:
    components.html(html_code, height=1700, scrolling=True)