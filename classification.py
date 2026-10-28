import streamlit as st
import streamlit.components.v1 as components

# =====================================================================
# 3단계: 분류 (KNN · 로지스틱 회귀 · 결정트리)
#  - 메인 파일의 st.navigation 에 등록된 페이지입니다. 메인 파일과 같은 폴더에 두세요.
#  - 와이드 레이아웃, 사이드바 펼침, 여백 제거 스타일은 메인 파일에서 공통으로 적용됩니다.
#  - 데이터: Palmer Penguins (penguins_size.csv) 342마리를 아래 JS의 PENGUINS 배열에 넣어 두었습니다.
#    CSV 파일을 따로 올리지 않아도 동작합니다. (원본 344마리 중 측정값이 빈 2마리 제외)
#  - 모든 계산(KNN, 경사하강법, 결정트리)은 학생 브라우저에서 JS로 처리합니다.
#    scikit-learn 등 파이썬 패키지 설치는 필요 없습니다.
#  - 종 이름·색은 SPECIES, 특성 이름·단위는 FEATURES 설정만 고치면 됩니다.
# =====================================================================

# r"""...""" (raw 문자열): JS 정규식의 역슬래시(\d 등)가 파이썬에서 바뀌지 않도록 함
html_code = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>머신러닝 플레이그라운드 - 분류</title>
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
        .tab-btn-active {
            background-color: #4f46e5;
            color: #ffffff;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
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
                <span class="px-3 py-1.5 rounded-lg text-indigo-100 cursor-help" title="왼쪽 사이드바에서 '2단계: 다중 회귀'를 눌러 이동하세요">
                    <i class="fa-solid fa-cube mr-1"></i> 2단계: 다중 회귀
                </span>
                <span class="px-3 py-1.5 rounded-lg font-semibold bg-white text-indigo-700 shadow-sm">
                    <i class="fa-solid fa-shapes mr-1"></i> 3단계: 분류
                </span>
            </nav>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-grow w-full">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

            <!-- Left Panel: Data Canvas (7 cols) -->
            <section class="lg:col-span-7 flex flex-col gap-4">
                <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 flex flex-wrap justify-between items-center gap-3">
                    <div class="flex items-center space-x-2">
                        <span class="font-bold text-slate-700 text-sm sm:text-base"><i class="fa-solid fa-robot text-indigo-500 mr-1"></i> 알고리즘:</span>
                        <div class="inline-flex rounded-lg p-1 bg-slate-100 border border-slate-200 text-xs sm:text-sm">
                            <button data-tab-btn="knn" class="tab-btn px-3 py-1.5 rounded-md font-semibold text-slate-600 hover:text-indigo-600 transition flex items-center gap-1">
                                <i class="fa-solid fa-users"></i> KNN
                            </button>
                            <button data-tab-btn="logi" class="tab-btn px-3 py-1.5 rounded-md font-semibold text-slate-600 hover:text-indigo-600 transition flex items-center gap-1">
                                <i class="fa-solid fa-wave-square"></i> 로지스틱 회귀
                            </button>
                            <button data-tab-btn="tree" class="tab-btn px-3 py-1.5 rounded-md font-semibold text-slate-600 hover:text-indigo-600 transition flex items-center gap-1">
                                <i class="fa-solid fa-sitemap"></i> 결정트리
                            </button>
                        </div>
                    </div>
                    <span id="split-count" class="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 font-mono border border-slate-200">훈련 0 · 테스트 0</span>
                </div>

                <div class="bg-white rounded-2xl p-4 shadow-sm border border-slate-200 flex flex-col items-center relative overflow-hidden">
                    <div id="hover-badge" class="hidden absolute top-6 left-6 bg-indigo-900/90 text-white px-3 py-1.5 rounded-lg text-xs font-mono shadow-lg backdrop-blur-md z-10 pointer-events-none"></div>

                    <div class="w-full aspect-square max-h-[520px] relative rounded-xl border border-slate-200 bg-slate-900 overflow-hidden cursor-crosshair shadow-inner">
                        <canvas id="main-canvas" class="w-full h-full block"></canvas>
                    </div>

                    <div id="legend" class="w-full flex flex-wrap items-center gap-x-4 gap-y-1 mt-3 px-1 text-xs text-slate-600"></div>

                    <div class="w-full flex flex-wrap justify-between items-center gap-2 mt-2 px-1 text-xs sm:text-sm text-slate-600">
                        <div class="flex flex-wrap items-center gap-x-4 gap-y-1">
                            <label class="flex items-center space-x-1.5 cursor-pointer select-none">
                                <input type="checkbox" id="toggle-region" checked class="w-4 h-4 text-indigo-600 rounded border-slate-300 focus:ring-indigo-500">
                                <span>결정 영역</span>
                            </label>
                            <label class="flex items-center space-x-1.5 cursor-pointer select-none">
                                <input type="checkbox" id="toggle-test" checked class="w-4 h-4 text-indigo-600 rounded border-slate-300 focus:ring-indigo-500">
                                <span>테스트 데이터</span>
                            </label>
                            <label class="flex items-center space-x-1.5 cursor-pointer select-none">
                                <input type="checkbox" id="toggle-wrong" class="w-4 h-4 text-indigo-600 rounded border-slate-300 focus:ring-indigo-500">
                                <span>틀린 예측 표시</span>
                            </label>
                        </div>
                        <span class="text-slate-400 text-xs"><i class="fa-solid fa-circle-info mr-1"></i>캔버스를 클릭하면 그 자리의 새 펭귄을 예측해요</span>
                    </div>
                </div>

                <!-- 데이터 설정 -->
                <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
                    <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-1">
                        <i class="fa-solid fa-table text-indigo-500"></i> 데이터 설정 (Palmer Penguins 데이터 342마리)
                    </h3>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div>
                            <label for="feature-x" class="text-xs font-semibold text-slate-700 block mb-1">가로축 특성 (x₁)</label>
                            <select id="feature-x" class="w-full px-3 py-2 rounded-xl border border-slate-300 bg-slate-50 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"></select>
                        </div>
                        <div>
                            <label for="feature-y" class="text-xs font-semibold text-slate-700 block mb-1">세로축 특성 (x₂)</label>
                            <select id="feature-y" class="w-full px-3 py-2 rounded-xl border border-slate-300 bg-slate-50 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"></select>
                        </div>
                    </div>

                    <div class="mt-4">
                        <div class="flex justify-between items-center mb-1">
                            <label for="test-slider" class="text-xs sm:text-sm font-semibold text-slate-700">테스트 데이터 비율</label>
                            <span id="test-val" class="font-mono font-bold text-indigo-600 text-sm bg-indigo-50 px-2 py-0.5 rounded">30%</span>
                        </div>
                        <input type="range" id="test-slider" min="10" max="50" step="5" value="30" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600">
                        <p class="text-[11px] text-slate-400 mt-1 break-keep">AI는 훈련 데이터로만 배우고, 테스트 데이터는 '처음 보는 문제'처럼 실력을 확인하는 데 써요. 종별 비율이 같도록 나눕니다.</p>
                    </div>

                    <div class="mt-3 flex flex-wrap items-center justify-between gap-2">
                        <div id="species-table" class="flex flex-wrap gap-1.5 text-[11px]"></div>
                        <button id="reshuffle-btn" class="px-3 py-1.5 bg-slate-100 hover:bg-indigo-50 text-slate-600 hover:text-indigo-700 font-medium rounded-lg text-xs sm:text-sm transition flex items-center gap-1 border border-slate-200">
                            <i class="fa-solid fa-shuffle"></i> 다시 섞어 나누기 <span id="seed-val" class="font-mono text-[11px] text-slate-400"></span>
                        </button>
                    </div>
                </div>

                <!-- 새 펭귄 측정값 입력 -->
                <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
                    <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1">
                        <i class="fa-solid fa-keyboard text-indigo-500"></i> 새 펭귄 측정값 입력하기
                    </h3>
                    <div class="flex flex-col sm:flex-row gap-2">
                        <input id="query-input" type="text" spellcheck="false" autocomplete="off"
                            class="flex-grow px-3 py-2 rounded-xl border border-slate-300 bg-slate-50 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:bg-white"
                            placeholder="예) (45, 17)   또는   45 17">
                        <button id="query-btn" class="sm:w-24 px-3 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow-sm transition flex items-center justify-center gap-1.5 text-xs sm:text-sm">
                            <i class="fa-solid fa-magnifying-glass"></i> 예측
                        </button>
                        <button id="query-clear-btn" class="sm:w-24 px-3 py-2 bg-slate-100 hover:bg-red-50 text-slate-600 hover:text-red-600 font-medium rounded-xl border border-slate-200 transition flex items-center justify-center gap-1.5 text-xs sm:text-sm">
                            <i class="fa-solid fa-eraser"></i> 지우기
                        </button>
                    </div>
                    <p id="query-hint" class="text-[11px] text-slate-500 mt-2 leading-relaxed break-keep"></p>
                    <div id="query-feedback" class="hidden mt-2 p-2.5 rounded-xl text-xs border"></div>
                </div>
            </section>

            <!-- Right Panel: Model controls & Metrics (5 cols) -->
            <section class="lg:col-span-5 flex flex-col gap-4">

                <!-- KNN 제어 -->
                <div data-tab="knn" class="tab-panel bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
                    <h2 class="text-base font-bold text-slate-800 mb-3 flex items-center">
                        <i class="fa-solid fa-sliders text-indigo-600 mr-2"></i>KNN 하이퍼파라미터
                    </h2>
                    <div class="space-y-4">
                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <label for="k-slider" class="text-xs sm:text-sm font-semibold text-slate-700">이웃의 수 (K)</label>
                                <span id="k-val" class="font-mono font-bold text-indigo-600 text-sm bg-indigo-50 px-2 py-0.5 rounded">5</span>
                            </div>
                            <input type="range" id="k-slider" min="1" max="30" step="1" value="5" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600">
                            <p class="text-[11px] text-slate-400 mt-1 break-keep">투표가 동점이면 가장 가까운 이웃의 종을 따라요.</p>
                        </div>
                        <label class="flex items-start gap-2 cursor-pointer select-none p-3 bg-slate-50 border border-slate-200 rounded-xl">
                            <input type="checkbox" id="knn-scale" checked class="mt-0.5 w-4 h-4 text-indigo-600 rounded border-slate-300 focus:ring-indigo-500">
                            <span class="text-xs text-slate-700 break-keep">
                                <strong>특성 표준화</strong> (단위 맞추기)<br>
                                <span class="text-slate-500">끄면 숫자가 큰 특성(예: 몸무게 g)이 거리 계산을 독차지해요. 가로축이나 세로축을 몸무게로 바꾸고 꺼 보세요!</span>
                            </span>
                        </label>
                    </div>
                </div>

                <!-- 로지스틱 회귀 제어 -->
                <div data-tab="logi" class="tab-panel hidden bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
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

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 mb-4">
                        <div>
                            <label for="pair-select" class="text-xs font-semibold text-slate-700 block mb-1">분류할 두 종 <span class="text-slate-400 font-normal">(오른쪽 종 = 1)</span></label>
                            <select id="pair-select" class="w-full px-3 py-2 rounded-xl border border-slate-300 bg-slate-50 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
                                <option value="0,2">아델리 vs 젠투</option>
                                <option value="0,1">아델리 vs 턱끈</option>
                                <option value="1,2">턱끈 vs 젠투</option>
                            </select>
                        </div>
                        <label class="flex items-start gap-2 cursor-pointer select-none p-2.5 bg-amber-50 border border-amber-200 rounded-xl">
                            <input type="checkbox" id="ovr-toggle" class="mt-0.5 w-4 h-4 text-amber-600 rounded border-slate-300 focus:ring-amber-500">
                            <span class="text-xs text-amber-900 break-keep">
                                <strong>⭐ 도전: 3종 모두 분류</strong><br>
                                <span class="text-amber-700">일대다(One-vs-Rest) 방식</span>
                            </span>
                        </label>
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
                                <span id="epochs-val" class="font-mono font-bold text-indigo-600 text-sm bg-indigo-50 px-2 py-0.5 rounded">200회</span>
                            </div>
                            <input type="range" id="epochs-slider" min="10" max="1000" step="10" value="200" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600">
                        </div>
                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <label for="lr-slider" class="text-xs sm:text-sm font-semibold text-slate-700">학습률 (Learning Rate, α)</label>
                                <span id="lr-val" class="font-mono font-bold text-indigo-600 text-sm bg-indigo-50 px-2 py-0.5 rounded">0.50</span>
                            </div>
                            <input type="range" id="lr-slider" min="0.01" max="2" step="0.01" value="0.5" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600">
                            <p class="text-[11px] text-slate-400 mt-1 break-keep">학습률이 작으면 결정 경계가 아주 천천히 움직여요. 0.05와 1.5를 비교해 보세요.</p>
                        </div>
                    </div>

                    <div class="mt-4 p-3 bg-slate-900 text-white rounded-xl font-mono text-center shadow-inner">
                        <span class="text-slate-400 text-xs block mb-1">현재 AI 식 (z = w₁x₁ + w₂x₂ + b,  p = σ(z))</span>
                        <div id="logi-equation" class="text-yellow-300 font-bold text-xs sm:text-sm break-words space-y-0.5"></div>
                    </div>
                </div>

                <!-- 시그모이드 그래프 (로지스틱 전용) -->
                <div data-tab="logi" class="tab-panel hidden bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
                    <div class="flex flex-wrap justify-between items-center mb-2 gap-2">
                        <h2 class="text-base font-bold text-slate-800 flex items-center gap-2">
                            <i class="fa-solid fa-wave-square text-indigo-600"></i> 시그모이드 함수 σ(z)
                        </h2>
                        <div id="sigmoid-class-btns" class="hidden inline-flex rounded-lg p-0.5 bg-slate-100 border border-slate-200 text-[11px]"></div>
                    </div>
                    <div class="w-full h-[200px] rounded-xl border border-slate-200 bg-slate-900 overflow-hidden">
                        <canvas id="sigmoid-canvas" class="w-full h-full block"></canvas>
                    </div>
                    <p id="sigmoid-caption" class="text-[11px] text-slate-500 mt-2 leading-relaxed break-keep"></p>
                </div>

                <!-- 결정트리 제어 -->
                <div data-tab="tree" class="tab-panel hidden bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
                    <h2 class="text-base font-bold text-slate-800 mb-3 flex items-center">
                        <i class="fa-solid fa-sliders text-indigo-600 mr-2"></i>결정트리 하이퍼파라미터
                    </h2>
                    <div class="space-y-4">
                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <label for="depth-slider" class="text-xs sm:text-sm font-semibold text-slate-700">최대 깊이 (max depth)</label>
                                <span id="depth-val" class="font-mono font-bold text-indigo-600 text-sm bg-indigo-50 px-2 py-0.5 rounded">3</span>
                            </div>
                            <input type="range" id="depth-slider" min="1" max="10" step="1" value="3" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600">
                            <p class="text-[11px] text-slate-400 mt-1">질문을 최대 몇 번까지 이어서 할지 정해요.</p>
                        </div>
                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <label for="leaf-slider" class="text-xs sm:text-sm font-semibold text-slate-700">잎 노드의 최소 펭귄 수</label>
                                <span id="leaf-val" class="font-mono font-bold text-indigo-600 text-sm bg-indigo-50 px-2 py-0.5 rounded">1마리</span>
                            </div>
                            <input type="range" id="leaf-slider" min="1" max="30" step="1" value="1" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600">
                            <p class="text-[11px] text-slate-400 mt-1 break-keep">값을 키우면 너무 적은 펭귄만 남는 질문을 막아서 과적합이 줄어요.</p>
                        </div>
                        <div id="tree-info" class="grid grid-cols-3 gap-2 text-center"></div>
                    </div>
                </div>

                <!-- 새 펭귄 예측 결과 (공통) -->
                <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
                    <h2 class="text-base font-bold text-slate-800 mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-star text-yellow-500"></i> 새 펭귄 예측 결과
                    </h2>
                    <div id="prediction-box" class="text-xs text-slate-700 leading-relaxed break-keep"></div>
                </div>

                <!-- 평가 지표 (공통) -->
                <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
                    <h2 class="text-base font-bold text-slate-800 mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-square-poll-vertical text-emerald-600"></i> 실시간 AI 평가 지표
                    </h2>
                    <div class="grid grid-cols-2 gap-2">
                        <div class="p-3 bg-indigo-50/70 border border-indigo-200 rounded-xl">
                            <span class="text-xs text-indigo-700 font-semibold block mb-0.5">훈련 정확도</span>
                            <span id="metric-train" class="text-xl font-extrabold text-indigo-800 font-mono">-</span>
                        </div>
                        <div class="p-3 bg-emerald-50/70 border border-emerald-200 rounded-xl">
                            <span class="text-xs text-emerald-700 font-semibold block mb-0.5">테스트 정확도</span>
                            <span id="metric-test" class="text-xl font-extrabold text-emerald-800 font-mono">-</span>
                        </div>
                    </div>
                    <div id="fit-message" class="mt-2 p-2.5 rounded-xl text-xs border break-keep"></div>

                    <div class="mt-4 flex flex-wrap justify-between items-center gap-2 mb-2">
                        <h3 class="text-sm font-bold text-slate-700 flex items-center gap-1.5">
                            <i class="fa-solid fa-border-all text-indigo-500"></i> 혼동 행렬 (Confusion Matrix)
                        </h3>
                        <div class="inline-flex rounded-lg p-0.5 bg-slate-100 border border-slate-200 text-[11px]">
                            <button data-cm="test" class="cm-btn px-2.5 py-1 rounded-md font-semibold">테스트</button>
                            <button data-cm="train" class="cm-btn px-2.5 py-1 rounded-md font-semibold">훈련</button>
                        </div>
                    </div>
                    <div id="confusion-matrix" class="overflow-x-auto"></div>
                    <p class="text-[11px] text-slate-400 mt-2 break-keep">가로줄은 실제 종, 세로줄은 AI가 예측한 종이에요. 대각선(초록)이 맞힌 개수, 나머지(빨강)가 틀린 개수입니다.</p>
                </div>

                <!-- 하이퍼파라미터 / 학습 그래프 (공통, 탭마다 내용이 바뀜) -->
                <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
                    <h2 id="chart-title" class="text-base font-bold text-slate-800 mb-2 flex items-center gap-2"></h2>
                    <div class="w-full h-[190px] rounded-xl border border-slate-200 bg-white overflow-hidden">
                        <canvas id="chart-canvas" class="w-full h-full block"></canvas>
                    </div>
                    <p id="chart-caption" class="text-[11px] text-slate-500 mt-2 leading-relaxed break-keep"></p>
                </div>

                <!-- 개념 정리 -->
                <div data-tab="knn" class="tab-panel bg-amber-50/80 border border-amber-200 p-5 rounded-2xl shadow-sm">
                    <h3 class="text-sm font-bold text-amber-900 flex items-center gap-1.5 mb-2">
                        <i class="fa-solid fa-lightbulb text-amber-600"></i> KNN(K-최근접 이웃)은 어떻게 분류할까?
                    </h3>
                    <div class="space-y-2 text-xs text-amber-900 break-keep">
                        <div class="bg-white p-2.5 rounded-xl border border-amber-200">새 펭귄과 <strong>가장 가까운 K마리</strong>를 찾아서, 그중 가장 많은 종으로 정해요. (다수결)</div>
                        <div class="bg-white p-2.5 rounded-xl border border-amber-200">
                            <span class="font-bold">K가 작으면</span> · 주변 한두 마리에 휘둘려 경계가 울퉁불퉁 <span class="text-amber-700">→ 과적합</span><br>
                            <span class="font-bold">K가 크면</span> · 경계가 지나치게 단순해짐 <span class="text-amber-700">→ 과소적합</span>
                        </div>
                        <p class="text-amber-800">KNN은 미리 규칙을 만들지 않고, 예측할 때마다 모든 훈련 데이터와의 거리를 계산해요. 그래서 '게으른 학습(lazy learning)'이라고 불러요.</p>
                    </div>
                </div>

                <div data-tab="logi" class="tab-panel hidden bg-amber-50/80 border border-amber-200 p-5 rounded-2xl shadow-sm">
                    <h3 class="text-sm font-bold text-amber-900 flex items-center gap-1.5 mb-2">
                        <i class="fa-solid fa-lightbulb text-amber-600"></i> 이름은 '회귀'인데 왜 분류일까?
                    </h3>
                    <div class="space-y-2 text-xs text-amber-900 break-keep">
                        <div class="bg-white p-2.5 rounded-xl border border-amber-200">
                            <span class="font-bold">① 다중 회귀처럼</span> z = w₁x₁ + w₂x₂ + b 를 계산해요.
                            <span class="block text-amber-700 mt-0.5"><span class="font-bold">② 시그모이드</span> σ(z) = 1 / (1 + e<sup>−z</sup>) 로 0~1 사이의 <strong>확률</strong>로 바꿔요.</span>
                            <span class="block text-amber-700 mt-0.5"><span class="font-bold">③ 확률 0.5 이상</span>이면 1번 종으로 분류해요. z = 0 인 곳이 결정 경계(직선)예요.</span>
                        </div>
                        <div class="bg-white p-2.5 rounded-xl border border-amber-200">
                            학습은 선형 회귀와 같은 <strong>경사하강법</strong>이지만, 줄이는 값이 MSE가 아니라 <strong>교차 엔트로피 손실</strong>이에요. 정답에 낮은 확률을 줄수록 손실이 크게 늘어나요.
                        </div>
                        <p class="text-amber-800">3종을 분류할 때는 '아델리 vs 나머지', '턱끈 vs 나머지', '젠투 vs 나머지' 분류기 3개를 따로 학습하고, 확률이 가장 높은 종을 골라요(일대다, One-vs-Rest).</p>
                    </div>
                </div>

                <div data-tab="tree" class="tab-panel hidden bg-amber-50/80 border border-amber-200 p-5 rounded-2xl shadow-sm">
                    <h3 class="text-sm font-bold text-amber-900 flex items-center gap-1.5 mb-2">
                        <i class="fa-solid fa-lightbulb text-amber-600"></i> 결정트리는 스무고개!
                    </h3>
                    <div class="space-y-2 text-xs text-amber-900 break-keep">
                        <div class="bg-white p-2.5 rounded-xl border border-amber-200">'부리 길이 ≤ 42.4mm?' 같은 <strong>예/아니오 질문</strong>을 이어 가며 펭귄을 나눠요. 마지막 칸(잎 노드)에서 가장 많은 종이 정답이에요.</div>
                        <div class="bg-white p-2.5 rounded-xl border border-amber-200">질문은 <strong>지니 불순도</strong>(여러 종이 섞인 정도)를 가장 많이 줄이는 것으로 골라요. 지니 0 = 한 종만 남은 상태예요.</div>
                        <p class="text-amber-800">질문 하나가 특성 하나만 보기 때문에 결정 영역이 <strong>축에 평행한 직사각형</strong> 모양이 돼요. 깊이를 키우면 훈련 정확도는 오르지만 테스트 정확도는 떨어질 수 있어요.</p>
                    </div>
                </div>
            </section>

            <!-- 트리 그림 (결정트리 전용, 전체 너비) -->
            <section data-tab="tree" class="tab-panel hidden lg:col-span-12 bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
                <div class="flex flex-wrap justify-between items-center mb-3 gap-2">
                    <h2 class="text-base font-bold text-slate-800 flex items-center gap-2">
                        <i class="fa-solid fa-sitemap text-indigo-600"></i> AI가 만든 결정트리
                    </h2>
                    <span class="text-xs text-slate-400"><i class="fa-solid fa-circle-info mr-1"></i>왼쪽 가지 = 예(≤), 오른쪽 가지 = 아니오(&gt;) · 새 펭귄의 경로는 노란색 · 옆으로 스크롤할 수 있어요</span>
                </div>
                <div id="tree-diagram" class="w-full overflow-x-auto overflow-y-hidden rounded-xl border border-slate-200 bg-slate-50 p-2"></div>
            </section>
        </div>
    </main>

    <div id="toast-container" class="fixed bottom-5 right-5 z-50 flex flex-col gap-2"></div>

    <footer class="bg-slate-100 border-t border-slate-200 py-3 text-center text-xs text-slate-500">
        머신러닝 인터랙티브 교구 | HTML5 Canvas · 데이터: Palmer Penguins (Gorman 외, 2014 / CC0)
    </footer>

    <script>
        // ================================================================
        // 펭귄 데이터: [종 번호, 부리 길이(mm), 부리 깊이(mm), 날개 길이(mm), 몸무게(g)]
        //  - 종 번호 0: 아델리, 1: 턱끈, 2: 젠투
        //  - 원본 344마리 중 측정값이 비어 있는(NA) 2마리를 뺀 342마리
        // ================================================================
        const PENGUINS = [
            [0,39.1,18.7,181,3750],[0,39.5,17.4,186,3800],[0,40.3,18.0,195,3250],[0,36.7,19.3,193,3450],[0,39.3,20.6,190,3650],[0,38.9,17.8,181,3625],[0,39.2,19.6,195,4675],[0,34.1,18.1,193,3475],
            [0,42.0,20.2,190,4250],[0,37.8,17.1,186,3300],[0,37.8,17.3,180,3700],[0,41.1,17.6,182,3200],[0,38.6,21.2,191,3800],[0,34.6,21.1,198,4400],[0,36.6,17.8,185,3700],[0,38.7,19.0,195,3450],
            [0,42.5,20.7,197,4500],[0,34.4,18.4,184,3325],[0,46.0,21.5,194,4200],[0,37.8,18.3,174,3400],[0,37.7,18.7,180,3600],[0,35.9,19.2,189,3800],[0,38.2,18.1,185,3950],[0,38.8,17.2,180,3800],
            [0,35.3,18.9,187,3800],[0,40.6,18.6,183,3550],[0,40.5,17.9,187,3200],[0,37.9,18.6,172,3150],[0,40.5,18.9,180,3950],[0,39.5,16.7,178,3250],[0,37.2,18.1,178,3900],[0,39.5,17.8,188,3300],
            [0,40.9,18.9,184,3900],[0,36.4,17.0,195,3325],[0,39.2,21.1,196,4150],[0,38.8,20.0,190,3950],[0,42.2,18.5,180,3550],[0,37.6,19.3,181,3300],[0,39.8,19.1,184,4650],[0,36.5,18.0,182,3150],
            [0,40.8,18.4,195,3900],[0,36.0,18.5,186,3100],[0,44.1,19.7,196,4400],[0,37.0,16.9,185,3000],[0,39.6,18.8,190,4600],[0,41.1,19.0,182,3425],[0,37.5,18.9,179,2975],[0,36.0,17.9,190,3450],
            [0,42.3,21.2,191,4150],[0,39.6,17.7,186,3500],[0,40.1,18.9,188,4300],[0,35.0,17.9,190,3450],[0,42.0,19.5,200,4050],[0,34.5,18.1,187,2900],[0,41.4,18.6,191,3700],[0,39.0,17.5,186,3550],
            [0,40.6,18.8,193,3800],[0,36.5,16.6,181,2850],[0,37.6,19.1,194,3750],[0,35.7,16.9,185,3150],[0,41.3,21.1,195,4400],[0,37.6,17.0,185,3600],[0,41.1,18.2,192,4050],[0,36.4,17.1,184,2850],
            [0,41.6,18.0,192,3950],[0,35.5,16.2,195,3350],[0,41.1,19.1,188,4100],[0,35.9,16.6,190,3050],[0,41.8,19.4,198,4450],[0,33.5,19.0,190,3600],[0,39.7,18.4,190,3900],[0,39.6,17.2,196,3550],
            [0,45.8,18.9,197,4150],[0,35.5,17.5,190,3700],[0,42.8,18.5,195,4250],[0,40.9,16.8,191,3700],[0,37.2,19.4,184,3900],[0,36.2,16.1,187,3550],[0,42.1,19.1,195,4000],[0,34.6,17.2,189,3200],
            [0,42.9,17.6,196,4700],[0,36.7,18.8,187,3800],[0,35.1,19.4,193,4200],[0,37.3,17.8,191,3350],[0,41.3,20.3,194,3550],[0,36.3,19.5,190,3800],[0,36.9,18.6,189,3500],[0,38.3,19.2,189,3950],
            [0,38.9,18.8,190,3600],[0,35.7,18.0,202,3550],[0,41.1,18.1,205,4300],[0,34.0,17.1,185,3400],[0,39.6,18.1,186,4450],[0,36.2,17.3,187,3300],[0,40.8,18.9,208,4300],[0,38.1,18.6,190,3700],
            [0,40.3,18.5,196,4350],[0,33.1,16.1,178,2900],[0,43.2,18.5,192,4100],[0,35.0,17.9,192,3725],[0,41.0,20.0,203,4725],[0,37.7,16.0,183,3075],[0,37.8,20.0,190,4250],[0,37.9,18.6,193,2925],
            [0,39.7,18.9,184,3550],[0,38.6,17.2,199,3750],[0,38.2,20.0,190,3900],[0,38.1,17.0,181,3175],[0,43.2,19.0,197,4775],[0,38.1,16.5,198,3825],[0,45.6,20.3,191,4600],[0,39.7,17.7,193,3200],
            [0,42.2,19.5,197,4275],[0,39.6,20.7,191,3900],[0,42.7,18.3,196,4075],[0,38.6,17.0,188,2900],[0,37.3,20.5,199,3775],[0,35.7,17.0,189,3350],[0,41.1,18.6,189,3325],[0,36.2,17.2,187,3150],
            [0,37.7,19.8,198,3500],[0,40.2,17.0,176,3450],[0,41.4,18.5,202,3875],[0,35.2,15.9,186,3050],[0,40.6,19.0,199,4000],[0,38.8,17.6,191,3275],[0,41.5,18.3,195,4300],[0,39.0,17.1,191,3050],
            [0,44.1,18.0,210,4000],[0,38.5,17.9,190,3325],[0,43.1,19.2,197,3500],[0,36.8,18.5,193,3500],[0,37.5,18.5,199,4475],[0,38.1,17.6,187,3425],[0,41.1,17.5,190,3900],[0,35.6,17.5,191,3175],
            [0,40.2,20.1,200,3975],[0,37.0,16.5,185,3400],[0,39.7,17.9,193,4250],[0,40.2,17.1,193,3400],[0,40.6,17.2,187,3475],[0,32.1,15.5,188,3050],[0,40.7,17.0,190,3725],[0,37.3,16.8,192,3000],
            [0,39.0,18.7,185,3650],[0,39.2,18.6,190,4250],[0,36.6,18.4,184,3475],[0,36.0,17.8,195,3450],[0,37.8,18.1,193,3750],[0,36.0,17.1,187,3700],[0,41.5,18.5,201,4000],[1,46.5,17.9,192,3500],
            [1,50.0,19.5,196,3900],[1,51.3,19.2,193,3650],[1,45.4,18.7,188,3525],[1,52.7,19.8,197,3725],[1,45.2,17.8,198,3950],[1,46.1,18.2,178,3250],[1,51.3,18.2,197,3750],[1,46.0,18.9,195,4150],
            [1,51.3,19.9,198,3700],[1,46.6,17.8,193,3800],[1,51.7,20.3,194,3775],[1,47.0,17.3,185,3700],[1,52.0,18.1,201,4050],[1,45.9,17.1,190,3575],[1,50.5,19.6,201,4050],[1,50.3,20.0,197,3300],
            [1,58.0,17.8,181,3700],[1,46.4,18.6,190,3450],[1,49.2,18.2,195,4400],[1,42.4,17.3,181,3600],[1,48.5,17.5,191,3400],[1,43.2,16.6,187,2900],[1,50.6,19.4,193,3800],[1,46.7,17.9,195,3300],
            [1,52.0,19.0,197,4150],[1,50.5,18.4,200,3400],[1,49.5,19.0,200,3800],[1,46.4,17.8,191,3700],[1,52.8,20.0,205,4550],[1,40.9,16.6,187,3200],[1,54.2,20.8,201,4300],[1,42.5,16.7,187,3350],
            [1,51.0,18.8,203,4100],[1,49.7,18.6,195,3600],[1,47.5,16.8,199,3900],[1,47.6,18.3,195,3850],[1,52.0,20.7,210,4800],[1,46.9,16.6,192,2700],[1,53.5,19.9,205,4500],[1,49.0,19.5,210,3950],
            [1,46.2,17.5,187,3650],[1,50.9,19.1,196,3550],[1,45.5,17.0,196,3500],[1,50.9,17.9,196,3675],[1,50.8,18.5,201,4450],[1,50.1,17.9,190,3400],[1,49.0,19.6,212,4300],[1,51.5,18.7,187,3250],
            [1,49.8,17.3,198,3675],[1,48.1,16.4,199,3325],[1,51.4,19.0,201,3950],[1,45.7,17.3,193,3600],[1,50.7,19.7,203,4050],[1,42.5,17.3,187,3350],[1,52.2,18.8,197,3450],[1,45.2,16.6,191,3250],
            [1,49.3,19.9,203,4050],[1,50.2,18.8,202,3800],[1,45.6,19.4,194,3525],[1,51.9,19.5,206,3950],[1,46.8,16.5,189,3650],[1,45.7,17.0,195,3650],[1,55.8,19.8,207,4000],[1,43.5,18.1,202,3400],
            [1,49.6,18.2,193,3775],[1,50.8,19.0,210,4100],[1,50.2,18.7,198,3775],[2,46.1,13.2,211,4500],[2,50.0,16.3,230,5700],[2,48.7,14.1,210,4450],[2,50.0,15.2,218,5700],[2,47.6,14.5,215,5400],
            [2,46.5,13.5,210,4550],[2,45.4,14.6,211,4800],[2,46.7,15.3,219,5200],[2,43.3,13.4,209,4400],[2,46.8,15.4,215,5150],[2,40.9,13.7,214,4650],[2,49.0,16.1,216,5550],[2,45.5,13.7,214,4650],
            [2,48.4,14.6,213,5850],[2,45.8,14.6,210,4200],[2,49.3,15.7,217,5850],[2,42.0,13.5,210,4150],[2,49.2,15.2,221,6300],[2,46.2,14.5,209,4800],[2,48.7,15.1,222,5350],[2,50.2,14.3,218,5700],
            [2,45.1,14.5,215,5000],[2,46.5,14.5,213,4400],[2,46.3,15.8,215,5050],[2,42.9,13.1,215,5000],[2,46.1,15.1,215,5100],[2,44.5,14.3,216,4100],[2,47.8,15.0,215,5650],[2,48.2,14.3,210,4600],
            [2,50.0,15.3,220,5550],[2,47.3,15.3,222,5250],[2,42.8,14.2,209,4700],[2,45.1,14.5,207,5050],[2,59.6,17.0,230,6050],[2,49.1,14.8,220,5150],[2,48.4,16.3,220,5400],[2,42.6,13.7,213,4950],
            [2,44.4,17.3,219,5250],[2,44.0,13.6,208,4350],[2,48.7,15.7,208,5350],[2,42.7,13.7,208,3950],[2,49.6,16.0,225,5700],[2,45.3,13.7,210,4300],[2,49.6,15.0,216,4750],[2,50.5,15.9,222,5550],
            [2,43.6,13.9,217,4900],[2,45.5,13.9,210,4200],[2,50.5,15.9,225,5400],[2,44.9,13.3,213,5100],[2,45.2,15.8,215,5300],[2,46.6,14.2,210,4850],[2,48.5,14.1,220,5300],[2,45.1,14.4,210,4400],
            [2,50.1,15.0,225,5000],[2,46.5,14.4,217,4900],[2,45.0,15.4,220,5050],[2,43.8,13.9,208,4300],[2,45.5,15.0,220,5000],[2,43.2,14.5,208,4450],[2,50.4,15.3,224,5550],[2,45.3,13.8,208,4200],
            [2,46.2,14.9,221,5300],[2,45.7,13.9,214,4400],[2,54.3,15.7,231,5650],[2,45.8,14.2,219,4700],[2,49.8,16.8,230,5700],[2,46.2,14.4,214,4650],[2,49.5,16.2,229,5800],[2,43.5,14.2,220,4700],
            [2,50.7,15.0,223,5550],[2,47.7,15.0,216,4750],[2,46.4,15.6,221,5000],[2,48.2,15.6,221,5100],[2,46.5,14.8,217,5200],[2,46.4,15.0,216,4700],[2,48.6,16.0,230,5800],[2,47.5,14.2,209,4600],
            [2,51.1,16.3,220,6000],[2,45.2,13.8,215,4750],[2,45.2,16.4,223,5950],[2,49.1,14.5,212,4625],[2,52.5,15.6,221,5450],[2,47.4,14.6,212,4725],[2,50.0,15.9,224,5350],[2,44.9,13.8,212,4750],
            [2,50.8,17.3,228,5600],[2,43.4,14.4,218,4600],[2,51.3,14.2,218,5300],[2,47.5,14.0,212,4875],[2,52.1,17.0,230,5550],[2,47.5,15.0,218,4950],[2,52.2,17.1,228,5400],[2,45.5,14.5,212,4750],
            [2,49.5,16.1,224,5650],[2,44.5,14.7,214,4850],[2,50.8,15.7,226,5200],[2,49.4,15.8,216,4925],[2,46.9,14.6,222,4875],[2,48.4,14.4,203,4625],[2,51.1,16.5,225,5250],[2,48.5,15.0,219,4850],
            [2,55.9,17.0,228,5600],[2,47.2,15.5,215,4975],[2,49.1,15.0,228,5500],[2,47.3,13.8,216,4725],[2,46.8,16.1,215,5500],[2,41.7,14.7,210,4700],[2,53.4,15.8,219,5500],[2,43.3,14.0,208,4575],
            [2,48.1,15.1,209,5500],[2,50.5,15.2,216,5000],[2,49.8,15.9,229,5950],[2,43.5,15.2,213,4650],[2,51.5,16.3,230,5500],[2,46.2,14.1,217,4375],[2,55.1,16.0,230,5850],[2,44.5,15.7,217,4875],
            [2,48.8,16.2,222,6000],[2,47.2,13.7,214,4925],[2,46.8,14.3,215,4850],[2,50.4,15.7,222,5750],[2,45.2,14.8,212,5200],[2,49.9,16.1,213,5400]
        ];

        const SPECIES = [
            { name: '아델리펭귄', short: '아델리', en: 'Adelie',    color: '#f97316', rgb: [249, 115, 22] },
            { name: '턱끈펭귄',   short: '턱끈',   en: 'Chinstrap', color: '#a855f7', rgb: [168, 85, 247] },
            { name: '젠투펭귄',   short: '젠투',   en: 'Gentoo',    color: '#14b8a6', rgb: [20, 184, 166] }
        ];
        const FEATURES = [
            { name: '부리 길이', unit: 'mm', en: 'culmen length' },
            { name: '부리 깊이', unit: 'mm', en: 'culmen depth' },
            { name: '날개 길이', unit: 'mm', en: 'flipper length' },
            { name: '몸무게',   unit: 'g',  en: 'body mass' }
        ];
        const GRID = 110;        // 결정 영역을 계산할 격자 수 (가로·세로)
        const K_MAX = 30;        // K별 정확도 그래프의 최대 K
        const DEPTH_MAX = 10;    // 깊이별 정확도 그래프의 최대 깊이

        const DATA = PENGUINS.map(r => ({ s: r[0], v: [r[1], r[2], r[3], r[4]], test: false }));

        // 특성별 화면 범위 (전체 데이터의 최솟값~최댓값에 여유 6%, 깔끔한 숫자로 반올림)
        const RANGES = FEATURES.map((_, f) => {
            const vals = DATA.map(p => p.v[f]);
            const lo = Math.min(...vals), hi = Math.max(...vals);
            const pad = (hi - lo) * 0.06;
            const unit = Math.pow(10, Math.floor(Math.log10(hi - lo)) - 1);   // mm → 1, g → 100
            return { min: Math.floor((lo - pad) / unit) * unit, max: Math.ceil((hi + pad) / unit) * unit };
        });

        const state = {
            tab: 'knn',
            fx: 0,
            fy: 1,
            testRatio: 0.3,
            seed: 42,
            showRegion: true,
            showTest: true,
            showWrong: false,
            cmSet: 'test',
            query: null,           // 새 펭귄 { x, y } (현재 축의 실제 단위)
            knn: { k: 5, scale: true },
            logi: {
                pair: [0, 2], ovr: false, epochs: 200, lr: 0.5,
                models: [], st: null, key: '', totalEpochs: 0, isTraining: false,
                history: { train: [], test: [] }, viewClass: 2
            },
            tree: { depth: 3, minLeaf: 1, root: null }
        };

        let model = null;           // 현재 탭의 모델: { predict(x, y) → { proba: [3], cls } }
        let evaluation = null;      // 정확도·혼동 행렬 계산 결과
        let regionDirty = true;
        let chartCache = { key: '', data: null };

        const $ = (id) => document.getElementById(id);
        const canvas = $('main-canvas');
        const ctx = canvas.getContext('2d');
        const regionCanvas = document.createElement('canvas');
        regionCanvas.width = GRID;
        regionCanvas.height = GRID;
        const regionCtx = regionCanvas.getContext('2d');

        // ---------------- 공통 도우미 ----------------
        function mulberry32(a) {
            return function () {
                a |= 0; a = a + 0x6D2B79F5 | 0;
                let t = Math.imul(a ^ a >>> 15, 1 | a);
                t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
                return ((t ^ t >>> 14) >>> 0) / 4294967296;
            };
        }

        // 종별로 같은 비율이 되도록 훈련/테스트 나누기 (층화 추출)
        function splitData() {
            const rand = mulberry32(state.seed);
            [0, 1, 2].forEach(s => {
                const idx = DATA.map((p, i) => (p.s === s ? i : -1)).filter(i => i >= 0);
                for (let i = idx.length - 1; i > 0; i--) {
                    const j = Math.floor(rand() * (i + 1));
                    [idx[i], idx[j]] = [idx[j], idx[i]];
                }
                const nTest = Math.round(idx.length * state.testRatio);
                idx.forEach((di, order) => { DATA[di].test = order < nTest; });
            });
        }

        const fx = (p) => p.v[state.fx];
        const fy = (p) => p.v[state.fy];
        const argmax = (arr) => arr.reduce((best, v, i) => (v > arr[best] ? i : best), 0);
        const sigmoid = (z) => 1 / (1 + Math.exp(-z));
        const pct = (v) => `${(v * 100).toFixed(1)}%`;

        function activeClasses() {
            if (state.tab === 'logi' && !state.logi.ovr) return state.logi.pair.slice();
            return [0, 1, 2];
        }
        const activePoints = () => { const cls = activeClasses(); return DATA.filter(p => cls.includes(p.s)); };
        const trainPoints = () => activePoints().filter(p => !p.test);

        function stats(pts) {
            const n = pts.length || 1;
            const mx = pts.reduce((s, p) => s + fx(p), 0) / n;
            const my = pts.reduce((s, p) => s + fy(p), 0) / n;
            const sx = Math.sqrt(pts.reduce((s, p) => s + (fx(p) - mx) ** 2, 0) / n) || 1;
            const sy = Math.sqrt(pts.reduce((s, p) => s + (fy(p) - my) ** 2, 0) / n) || 1;
            return { mx, my, sx, sy };
        }

        function fmtNum(v) {
            if (!Number.isFinite(v)) return '∞';
            const a = Math.abs(v);
            if (a === 0) return '0';
            if (a >= 100) return v.toFixed(1);
            if (a >= 1) return v.toFixed(2);
            if (a >= 0.01) return v.toFixed(3);
            return v.toExponential(2);
        }
        const fmtVal = (v) => String(Math.round(v * 100) / 100);
        const featLabel = (f) => `${FEATURES[f].name}(${FEATURES[f].unit})`;

        function escapeHtml(str) {
            return String(str).replace(/[&<>"']/g, (c) => ({
                '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
            }[c]));
        }

        // ================================================================
        // 모델 1: KNN
        // ================================================================
        function buildKNN() {
            const tr = trainPoints();
            const st = stats(tr);
            const scale = state.knn.scale;
            const tx = (x) => (scale ? (x - st.mx) / st.sx : x);
            const ty = (y) => (scale ? (y - st.my) / st.sy : y);
            const T = tr.map(p => ({ x: tx(fx(p)), y: ty(fy(p)), s: p.s, p }));

            // 가까운 순서로 k개의 이웃 찾기
            function neighbors(x, y, k) {
                const qx = tx(x), qy = ty(y);
                const best = [];
                for (const t of T) {
                    const d = (t.x - qx) ** 2 + (t.y - qy) ** 2;
                    let i;
                    if (best.length < k) { best.push({ d, t }); i = best.length - 1; }
                    else if (d < best[k - 1].d) { best[k - 1] = { d, t }; i = k - 1; }
                    else continue;
                    while (i > 0 && best[i - 1].d > best[i].d) {
                        [best[i - 1], best[i]] = [best[i], best[i - 1]];
                        i--;
                    }
                }
                return best;
            }

            // 다수결 (동점이면 더 가까운 이웃이 먼저 나온 종)
            function vote(list, k) {
                const counts = [0, 0, 0];
                const first = [Infinity, Infinity, Infinity];
                for (let i = 0; i < k && i < list.length; i++) {
                    const s = list[i].t ? list[i].t.s : list[i].s;
                    counts[s]++;
                    if (first[s] === Infinity) first[s] = i;
                }
                let cls = 0;
                for (let s = 1; s < 3; s++) {
                    if (counts[s] > counts[cls] || (counts[s] === counts[cls] && first[s] < first[cls])) cls = s;
                }
                return { counts, cls };
            }

            return {
                type: 'knn',
                neighbors,
                predict(x, y) {
                    const k = Math.min(state.knn.k, T.length);
                    const list = neighbors(x, y, k);
                    const { counts, cls } = vote(list, k);
                    return { proba: counts.map(c => c / k), cls, list };
                },
                // K별 정확도 그래프용: 각 점의 '모든 훈련 데이터까지 거리' 순서를 한 번만 계산
                accuracyByK() {
                    const result = { train: [], test: [] };
                    const pts = activePoints();
                    const sorted = pts.map(p => {
                        const qx = tx(fx(p)), qy = ty(fy(p));
                        return { p, list: T.map(t => ({ d: (t.x - qx) ** 2 + (t.y - qy) ** 2, s: t.s })).sort((a, b) => a.d - b.d) };
                    });
                    for (let k = 1; k <= K_MAX; k++) {
                        let trOk = 0, trN = 0, teOk = 0, teN = 0;
                        sorted.forEach(({ p, list }) => {
                            const ok = vote(list, k).cls === p.s;
                            if (p.test) { teN++; if (ok) teOk++; } else { trN++; if (ok) trOk++; }
                        });
                        result.train.push(trN ? trOk / trN : 0);
                        result.test.push(teN ? teOk / teN : 0);
                    }
                    return result;
                }
            };
        }

        // ================================================================
        // 모델 2: 로지스틱 회귀 (경사하강법, 내부적으로 표준화한 값으로 학습)
        // ================================================================
        function logiKey() {
            const L = state.logi;
            return `${state.fx},${state.fy},${state.seed},${state.testRatio},${L.pair},${L.ovr}`;
        }

        function resetLogi() {
            const L = state.logi;
            L.st = stats(trainPoints());
            L.models = L.ovr ? [0, 1, 2].map(c => ({ cls: c, w1: 0, w2: 0, b: 0 }))
                             : [{ cls: L.pair[1], w1: 0, w2: 0, b: 0 }];
            L.totalEpochs = 0;
            L.isTraining = false;
            L.history = { train: [], test: [] };
            L.key = logiKey();
            if (L.ovr && !L.models.some(m => m.cls === L.viewClass)) L.viewClass = 2;
            setStatus('idle');
        }

        function logiZ(m, x, y) {
            const st = state.logi.st;
            return m.w1 * (x - st.mx) / st.sx + m.w2 * (y - st.my) / st.sy + m.b;
        }

        // 실제 단위의 식으로 바꾸기: z = W1·x + W2·y + B
        function rawWeights(m) {
            const st = state.logi.st;
            const W1 = m.w1 / st.sx, W2 = m.w2 / st.sy;
            return { W1, W2, B: m.b - W1 * st.mx - W2 * st.my };
        }

        function logiLoss(pts) {
            const L = state.logi;
            if (!pts.length) return 0;
            let total = 0;
            L.models.forEach(m => {
                let sum = 0;
                pts.forEach(p => {
                    const y = p.s === m.cls ? 1 : 0;
                    const q = Math.min(1 - 1e-12, Math.max(1e-12, sigmoid(logiZ(m, fx(p), fy(p)))));
                    sum += -(y * Math.log(q) + (1 - y) * Math.log(1 - q));
                });
                total += sum / pts.length;
            });
            return total / L.models.length;
        }

        function recordLoss() {
            const pts = activePoints();
            state.logi.history.train.push(logiLoss(pts.filter(p => !p.test)));
            state.logi.history.test.push(logiLoss(pts.filter(p => p.test)));
        }

        function stepLogi() {
            const L = state.logi;
            const tr = trainPoints();
            const N = tr.length;
            if (!N) return;
            L.models.forEach(m => {
                let g1 = 0, g2 = 0, gb = 0;
                tr.forEach(p => {
                    const u1 = (fx(p) - L.st.mx) / L.st.sx;
                    const u2 = (fy(p) - L.st.my) / L.st.sy;
                    const err = sigmoid(m.w1 * u1 + m.w2 * u2 + m.b) - (p.s === m.cls ? 1 : 0);
                    g1 += err * u1; g2 += err * u2; gb += err;
                });
                m.w1 -= L.lr * g1 / N;
                m.w2 -= L.lr * g2 / N;
                m.b -= L.lr * gb / N;
            });
            L.totalEpochs += 1;
            recordLoss();
        }

        function buildLogi() {
            const L = state.logi;
            if (L.key !== logiKey()) resetLogi();
            return {
                type: 'logi',
                predict(x, y) {
                    const proba = [0, 0, 0];
                    if (!L.ovr) {
                        const z = logiZ(L.models[0], x, y);
                        const p = sigmoid(z);
                        proba[L.pair[1]] = p;
                        proba[L.pair[0]] = 1 - p;
                        return { proba, cls: p >= 0.5 ? L.pair[1] : L.pair[0], z, p };
                    }
                    const sig = L.models.map(m => sigmoid(logiZ(m, x, y)));
                    const sum = sig.reduce((a, b) => a + b, 0) || 1;
                    sig.forEach((v, c) => { proba[c] = v / sum; });
                    return { proba, cls: argmax(sig), sig };
                }
            };
        }

        // ================================================================
        // 모델 3: 결정트리 (CART, 지니 불순도)
        // ================================================================
        function gini(counts, n) {
            if (!n) return 0;
            return 1 - counts.reduce((s, c) => s + (c / n) ** 2, 0);
        }

        function buildTreeNode(pts, depth, maxDepth, minLeaf) {
            const counts = [0, 0, 0];
            pts.forEach(p => counts[p.s]++);
            const n = pts.length;
            const g = gini(counts, n);
            const node = { counts, n, gini: g, pred: argmax(counts), depth };
            if (depth >= maxDepth || g === 0 || n < 2 * minLeaf) return node;

            let best = null;
            [0, 1].forEach(f => {
                const get = f === 0 ? fx : fy;
                const sorted = pts.slice().sort((a, b) => get(a) - get(b));
                const left = [0, 0, 0];
                const right = counts.slice();
                for (let i = 1; i < n; i++) {
                    const prev = sorted[i - 1];
                    left[prev.s]++; right[prev.s]--;
                    if (i < minLeaf || n - i < minLeaf) continue;
                    const a = get(prev), b = get(sorted[i]);
                    if (a === b) continue;
                    const score = (i * gini(left, i) + (n - i) * gini(right, n - i)) / n;
                    if (!best || score < best.score - 1e-12) best = { f, threshold: (a + b) / 2, score };
                }
            });
            if (!best || best.score >= g - 1e-12) return node;   // 불순도가 줄지 않으면 멈춤

            node.feature = best.f;
            node.threshold = best.threshold;
            const get = best.f === 0 ? fx : fy;
            node.left = buildTreeNode(pts.filter(p => get(p) <= best.threshold), depth + 1, maxDepth, minLeaf);
            node.right = buildTreeNode(pts.filter(p => get(p) > best.threshold), depth + 1, maxDepth, minLeaf);
            return node;
        }

        function treePath(root, x, y) {
            const path = [root];
            let node = root;
            while (node.left) {
                const v = node.feature === 0 ? x : y;
                node = v <= node.threshold ? node.left : node.right;
                path.push(node);
            }
            return path;
        }

        function buildTree() {
            const root = buildTreeNode(trainPoints(), 0, state.tree.depth, state.tree.minLeaf);
            state.tree.root = root;
            return {
                type: 'tree',
                predict(x, y) {
                    const path = treePath(root, x, y);
                    const leaf = path[path.length - 1];
                    return { proba: leaf.counts.map(c => c / leaf.n), cls: leaf.pred, path };
                },
                accuracyByDepth() {
                    const result = { train: [], test: [] };
                    const tr = trainPoints();
                    const pts = activePoints();
                    for (let d = 1; d <= DEPTH_MAX; d++) {
                        const r = buildTreeNode(tr, 0, d, state.tree.minLeaf);
                        let trOk = 0, trN = 0, teOk = 0, teN = 0;
                        pts.forEach(p => {
                            const path = treePath(r, fx(p), fy(p));
                            const ok = path[path.length - 1].pred === p.s;
                            if (p.test) { teN++; if (ok) teOk++; } else { trN++; if (ok) trOk++; }
                        });
                        result.train.push(trN ? trOk / trN : 0);
                        result.test.push(teN ? teOk / teN : 0);
                    }
                    return result;
                }
            };
        }

        // ================================================================
        // 평가: 정확도 + 혼동 행렬
        // ================================================================
        function evaluate() {
            const cls = activeClasses();
            const res = {
                classes: cls,
                train: { ok: 0, n: 0, cm: [[0, 0, 0], [0, 0, 0], [0, 0, 0]] },
                test: { ok: 0, n: 0, cm: [[0, 0, 0], [0, 0, 0], [0, 0, 0]] },
                wrong: new Set()
            };
            activePoints().forEach(p => {
                const pred = model.predict(fx(p), fy(p)).cls;
                const set = p.test ? res.test : res.train;
                set.n++;
                set.cm[p.s][pred]++;
                if (pred === p.s) set.ok++;
                else res.wrong.add(p);
            });
            return res;
        }

        // ================================================================
        // 메인 캔버스 그리기
        // ================================================================
        let plot = { x: 0, y: 0, w: 0, h: 0 };
        const PAD = { left: 56, right: 14, top: 14, bottom: 44 };

        function resizeCanvas() {
            const rect = canvas.parentElement.getBoundingClientRect();
            const dpr = window.devicePixelRatio || 1;
            canvas.width = rect.width * dpr;
            canvas.height = rect.height * dpr;
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
            plot = {
                x: PAD.left, y: PAD.top,
                w: Math.max(10, rect.width - PAD.left - PAD.right),
                h: Math.max(10, rect.height - PAD.top - PAD.bottom),
                cssW: rect.width, cssH: rect.height
            };
            draw();
        }

        const rx = () => RANGES[state.fx];
        const ry = () => RANGES[state.fy];
        const toPx = (x, y) => [
            plot.x + (x - rx().min) / (rx().max - rx().min) * plot.w,
            plot.y + (1 - (y - ry().min) / (ry().max - ry().min)) * plot.h
        ];
        const fromPx = (px, py) => [
            rx().min + (px - plot.x) / plot.w * (rx().max - rx().min),
            ry().min + (1 - (py - plot.y) / plot.h) * (ry().max - ry().min)
        ];

        function niceTicks(min, max, count = 6) {
            const raw = (max - min) / count;
            const mag = Math.pow(10, Math.floor(Math.log10(raw)));
            const norm = raw / mag;
            const step = (norm < 1.5 ? 1 : norm < 3 ? 2 : norm < 7 ? 5 : 10) * mag;
            const ticks = [];
            for (let t = Math.ceil(min / step) * step; t <= max + 1e-9; t += step) ticks.push(Math.round(t * 1e6) / 1e6);
            return ticks;
        }

        // 격자마다 예측해서 결정 영역 이미지를 만들기
        function computeRegion() {
            const img = regionCtx.createImageData(GRID, GRID);
            const nc = activeClasses().length;
            for (let j = 0; j < GRID; j++) {
                const y = ry().max - (j + 0.5) / GRID * (ry().max - ry().min);
                for (let i = 0; i < GRID; i++) {
                    const x = rx().min + (i + 0.5) / GRID * (rx().max - rx().min);
                    const { proba, cls } = model.predict(x, y);
                    const conf = Math.max(0, (proba[cls] - 1 / nc) / (1 - 1 / nc));
                    const k = (j * GRID + i) * 4;
                    const [r, g, b] = SPECIES[cls].rgb;
                    img.data[k] = r; img.data[k + 1] = g; img.data[k + 2] = b;
                    img.data[k + 3] = Math.round(255 * (0.07 + 0.33 * conf));
                }
            }
            regionCtx.putImageData(img, 0, 0);
            regionDirty = false;
        }

        function drawLine(W1, W2, B, color, dash, width) {
            // W1·x + W2·y + B = 0 인 직선을 화면 끝에서 끝까지 그리기
            const X = rx(), Y = ry();
            let p1, p2;
            if (Math.abs(W2) * (Y.max - Y.min) > Math.abs(W1) * (X.max - X.min)) {
                p1 = [X.min, -(W1 * X.min + B) / W2];
                p2 = [X.max, -(W1 * X.max + B) / W2];
            } else if (Math.abs(W1) > 1e-12) {
                p1 = [-(W2 * Y.min + B) / W1, Y.min];
                p2 = [-(W2 * Y.max + B) / W1, Y.max];
            } else return;
            const a = toPx(...p1), b = toPx(...p2);
            ctx.save();
            ctx.beginPath();
            ctx.rect(plot.x, plot.y, plot.w, plot.h);
            ctx.clip();
            ctx.strokeStyle = color;
            ctx.lineWidth = width;
            ctx.setLineDash(dash);
            ctx.beginPath();
            ctx.moveTo(a[0], a[1]);
            ctx.lineTo(b[0], b[1]);
            ctx.stroke();
            ctx.restore();
        }

        function drawStar(cx, cy, r) {
            ctx.beginPath();
            for (let i = 0; i < 10; i++) {
                const ang = -Math.PI / 2 + i * Math.PI / 5;
                const rr = i % 2 === 0 ? r : r * 0.45;
                ctx.lineTo(cx + rr * Math.cos(ang), cy + rr * Math.sin(ang));
            }
            ctx.closePath();
            ctx.fillStyle = '#facc15';
            ctx.fill();
            ctx.lineWidth = 2;
            ctx.strokeStyle = '#0f172a';
            ctx.stroke();
        }

        function draw() {
            if (!plot.cssW) return;
            ctx.clearRect(0, 0, plot.cssW, plot.cssH);
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(0, 0, plot.cssW, plot.cssH);

            // 결정 영역
            if (state.showRegion && model) {
                if (regionDirty) computeRegion();
                ctx.imageSmoothingEnabled = model.type === 'logi';
                ctx.drawImage(regionCanvas, plot.x, plot.y, plot.w, plot.h);
            }

            // 격자와 눈금
            ctx.font = "11px 'Noto Sans KR', sans-serif";
            ctx.lineWidth = 1;
            ctx.setLineDash([]);
            niceTicks(rx().min, rx().max).forEach(t => {
                const [px] = toPx(t, 0);
                ctx.strokeStyle = 'rgba(148,163,184,0.15)';
                ctx.beginPath(); ctx.moveTo(px, plot.y); ctx.lineTo(px, plot.y + plot.h); ctx.stroke();
                ctx.fillStyle = '#94a3b8';
                ctx.textAlign = 'center';
                ctx.fillText(fmtVal(t), px, plot.y + plot.h + 15);
            });
            niceTicks(ry().min, ry().max).forEach(t => {
                const [, py] = toPx(0, t);
                ctx.strokeStyle = 'rgba(148,163,184,0.15)';
                ctx.beginPath(); ctx.moveTo(plot.x, py); ctx.lineTo(plot.x + plot.w, py); ctx.stroke();
                ctx.fillStyle = '#94a3b8';
                ctx.textAlign = 'right';
                ctx.fillText(fmtVal(t), plot.x - 6, py + 4);
            });
            ctx.strokeStyle = '#64748b';
            ctx.strokeRect(plot.x, plot.y, plot.w, plot.h);

            // 축 이름
            ctx.fillStyle = '#e2e8f0';
            ctx.font = "bold 12px 'Noto Sans KR', sans-serif";
            ctx.textAlign = 'center';
            ctx.fillText(`${featLabel(state.fx)} →`, plot.x + plot.w / 2, plot.y + plot.h + 34);
            ctx.save();
            ctx.translate(16, plot.y + plot.h / 2);
            ctx.rotate(-Math.PI / 2);
            ctx.fillText(`${featLabel(state.fy)} →`, 0, 0);
            ctx.restore();

            // 로지스틱 회귀의 결정 경계 직선 (p = 0.5)
            if (model && model.type === 'logi' && state.logi.totalEpochs > 0) {
                state.logi.models.forEach(m => {
                    const { W1, W2, B } = rawWeights(m);
                    if (state.logi.ovr) drawLine(W1, W2, B, SPECIES[m.cls].color, [6, 4], 2);
                    else drawLine(W1, W2, B, '#fde047', [], 2.5);
                });
            }

            // 데이터 점
            const cls = activeClasses();
            ctx.save();
            ctx.beginPath();
            ctx.rect(plot.x, plot.y, plot.w, plot.h);
            ctx.clip();
            DATA.forEach(p => {
                if (p.test && !state.showTest) return;
                const [px, py] = toPx(fx(p), fy(p));
                if (!cls.includes(p.s)) {
                    ctx.fillStyle = 'rgba(148,163,184,0.25)';
                    ctx.beginPath(); ctx.arc(px, py, 2.5, 0, Math.PI * 2); ctx.fill();
                    return;
                }
                const color = SPECIES[p.s].color;
                ctx.beginPath();
                ctx.arc(px, py, 4.5, 0, Math.PI * 2);
                if (p.test) {
                    ctx.fillStyle = '#0f172a';
                    ctx.fill();
                    ctx.lineWidth = 2.2;
                    ctx.strokeStyle = color;
                    ctx.stroke();
                } else {
                    ctx.fillStyle = color;
                    ctx.fill();
                    ctx.lineWidth = 1.2;
                    ctx.strokeStyle = '#ffffff';
                    ctx.stroke();
                }
                if (state.showWrong && evaluation && evaluation.wrong.has(p)) {
                    ctx.beginPath();
                    ctx.arc(px, py, 8.5, 0, Math.PI * 2);
                    ctx.lineWidth = 2;
                    ctx.strokeStyle = '#f43f5e';
                    ctx.stroke();
                }
            });

            // 새 펭귄 (+ KNN 이웃 연결선)
            if (state.query && model) {
                const [qx, qy] = toPx(state.query.x, state.query.y);
                if (model.type === 'knn') {
                    const { list } = model.predict(state.query.x, state.query.y);
                    ctx.setLineDash([4, 3]);
                    ctx.lineWidth = 1.5;
                    list.forEach(({ t }) => {
                        const [px, py] = toPx(fx(t.p), fy(t.p));
                        ctx.strokeStyle = SPECIES[t.s].color;
                        ctx.beginPath(); ctx.moveTo(qx, qy); ctx.lineTo(px, py); ctx.stroke();
                    });
                    ctx.setLineDash([]);
                    list.forEach(({ t }) => {
                        const [px, py] = toPx(fx(t.p), fy(t.p));
                        ctx.beginPath(); ctx.arc(px, py, 7, 0, Math.PI * 2);
                        ctx.lineWidth = 2; ctx.strokeStyle = '#facc15'; ctx.stroke();
                    });
                }
                drawStar(qx, qy, 11);
            }
            ctx.restore();
        }

        // ================================================================
        // 보조 그래프: 시그모이드, 정확도/손실
        // ================================================================
        function setupCanvas(cv) {
            const rect = cv.parentElement.getBoundingClientRect();
            const dpr = window.devicePixelRatio || 1;
            cv.width = rect.width * dpr;
            cv.height = rect.height * dpr;
            const c = cv.getContext('2d');
            c.setTransform(dpr, 0, 0, dpr, 0, 0);
            return { c, w: rect.width, h: rect.height };
        }

        function drawSigmoid() {
            const cv = $('sigmoid-canvas');
            if (cv.offsetParent === null) return;
            const { c, w, h } = setupCanvas(cv);
            const L = state.logi;
            const m = L.ovr ? L.models.find(mm => mm.cls === L.viewClass) : L.models[0];
            const P = { l: 34, r: 10, t: 10, b: 26 };
            const pw = w - P.l - P.r, ph = h - P.t - P.b;
            const Z = 8;
            const X = (z) => P.l + (Math.max(-Z, Math.min(Z, z)) + Z) / (2 * Z) * pw;
            const Yp = (v) => P.t + (1 - v) * ph;

            c.fillStyle = '#0f172a'; c.fillRect(0, 0, w, h);
            c.font = "10px 'Noto Sans KR', sans-serif";
            c.strokeStyle = 'rgba(148,163,184,0.2)'; c.lineWidth = 1;
            [0, 0.5, 1].forEach(v => {
                c.beginPath(); c.moveTo(P.l, Yp(v)); c.lineTo(P.l + pw, Yp(v)); c.stroke();
                c.fillStyle = '#94a3b8'; c.textAlign = 'right'; c.fillText(v.toFixed(1), P.l - 5, Yp(v) + 3);
            });
            [-8, -4, 0, 4, 8].forEach(z => {
                c.fillStyle = '#94a3b8'; c.textAlign = 'center'; c.fillText(String(z), X(z), P.t + ph + 14);
            });
            c.fillStyle = '#e2e8f0'; c.textAlign = 'right';
            c.fillText('z →', P.l + pw, P.t + ph + 24);
            c.strokeStyle = 'rgba(253,224,71,0.6)'; c.setLineDash([3, 3]);
            c.beginPath(); c.moveTo(X(0), P.t); c.lineTo(X(0), P.t + ph); c.stroke();
            c.setLineDash([]);

            // 훈련 데이터: 1번 종은 위(1), 나머지는 아래(0)에 흩뿌리기
            const rand = mulberry32(7);
            if (m) {
                trainPoints().forEach(p => {
                    const z = logiZ(m, fx(p), fy(p));
                    const yv = p.s === m.cls ? 1 - rand() * 0.08 : rand() * 0.08;
                    c.fillStyle = SPECIES[p.s].color;
                    c.globalAlpha = 0.75;
                    c.beginPath(); c.arc(X(z), Yp(yv), 2.6, 0, Math.PI * 2); c.fill();
                });
                c.globalAlpha = 1;
            }

            // 시그모이드 곡선
            c.strokeStyle = '#818cf8'; c.lineWidth = 2.5;
            c.beginPath();
            for (let i = 0; i <= 160; i++) {
                const z = -Z + i / 160 * 2 * Z;
                if (i === 0) c.moveTo(X(z), Yp(sigmoid(z))); else c.lineTo(X(z), Yp(sigmoid(z)));
            }
            c.stroke();

            // 새 펭귄의 위치
            if (state.query && m) {
                const z = logiZ(m, state.query.x, state.query.y);
                const px = X(z), py = Yp(sigmoid(z));
                c.strokeStyle = '#facc15'; c.setLineDash([3, 3]); c.lineWidth = 1;
                c.beginPath(); c.moveTo(px, P.t + ph); c.lineTo(px, py); c.lineTo(P.l, py); c.stroke();
                c.setLineDash([]);
                c.fillStyle = '#facc15'; c.beginPath(); c.arc(px, py, 5, 0, Math.PI * 2); c.fill();
                c.strokeStyle = '#0f172a'; c.lineWidth = 1.5; c.stroke();
            }

            const pos = SPECIES[m ? m.cls : L.pair[1]].short;
            $('sigmoid-caption').innerHTML = L.ovr
                ? `'<strong>${pos}</strong> vs 나머지' 분류기의 시그모이드예요. 위쪽(1) 점은 ${pos}, 아래쪽(0) 점은 나머지 종이에요. 버튼으로 다른 분류기를 볼 수 있어요.`
                : `세로축은 '<strong>${pos}일 확률</strong>'이에요. 위쪽(1) 점은 ${pos}, 아래쪽(0) 점은 ${SPECIES[L.pair[0]].short}이에요. 학습할수록 점들이 곡선의 양 끝으로 벌어져요. (z가 ±8을 넘으면 끝에 모아 표시)`;
        }

        function drawLineChart(series, opts) {
            const cv = $('chart-canvas');
            const { c, w, h } = setupCanvas(cv);
            const P = { l: 40, r: 12, t: 24, b: 30 };
            const pw = w - P.l - P.r, ph = h - P.t - P.b;
            const n = Math.max(1, opts.n);
            const X = (i) => P.l + (n === 1 ? 0.5 : (i) / (n - 1)) * pw;
            const Y = (v) => P.t + (1 - (v - opts.yMin) / (opts.yMax - opts.yMin)) * ph;

            c.fillStyle = '#ffffff'; c.fillRect(0, 0, w, h);
            c.font = "10px 'Noto Sans KR', sans-serif";
            c.lineWidth = 1;
            opts.yTicks.forEach(v => {
                c.strokeStyle = '#e2e8f0';
                c.beginPath(); c.moveTo(P.l, Y(v)); c.lineTo(P.l + pw, Y(v)); c.stroke();
                c.fillStyle = '#64748b'; c.textAlign = 'right';
                c.fillText(opts.yFmt(v), P.l - 5, Y(v) + 3);
            });
            opts.xTicks.forEach(i => {
                c.fillStyle = '#64748b'; c.textAlign = 'center';
                c.fillText(opts.xFmt(i), X(i), P.t + ph + 14);
            });
            c.fillStyle = '#334155'; c.textAlign = 'right';
            c.fillText(opts.xLabel, P.l + pw, P.t + ph + 26);

            if (opts.marker !== undefined) {
                c.strokeStyle = '#facc15'; c.lineWidth = 6; c.globalAlpha = 0.35;
                c.beginPath(); c.moveTo(X(opts.marker), P.t); c.lineTo(X(opts.marker), P.t + ph); c.stroke();
                c.globalAlpha = 1;
            }
            series.forEach(s => {
                if (!s.values.length) return;
                c.strokeStyle = s.color; c.lineWidth = 2;
                c.beginPath();
                s.values.forEach((v, i) => { if (i === 0) c.moveTo(X(i), Y(v)); else c.lineTo(X(i), Y(v)); });
                c.stroke();
                if (s.values.length <= 40) {
                    c.fillStyle = s.color;
                    s.values.forEach((v, i) => { c.beginPath(); c.arc(X(i), Y(v), 2.2, 0, Math.PI * 2); c.fill(); });
                }
            });
            // 범례
            let lx = P.l + 6;
            c.font = "bold 10px 'Noto Sans KR', sans-serif";
            c.textAlign = 'left';
            series.forEach(s => {
                c.fillStyle = s.color; c.fillRect(lx, 7, 10, 3);
                c.fillText(s.name, lx + 14, 12);
                lx += c.measureText(s.name).width + 30;
            });
        }

        function accTicks(lo) {
            const t = [];
            for (let v = lo; v <= 1.0001; v += 0.1) t.push(Math.round(v * 10) / 10);
            return t;
        }

        function drawChart() {
            const TRAIN = '#4f46e5', TEST = '#10b981';
            if (state.tab === 'logi') {
                const H = state.logi.history;
                $('chart-title').innerHTML = `<i class="fa-solid fa-chart-line text-indigo-600"></i> 학습 손실 그래프 (교차 엔트로피)`;
                const n = H.train.length;
                const maxV = Math.max(0.8, ...H.train, ...H.test);
                const yMax = Math.ceil(maxV * 5) / 5;
                const ticks = [];
                for (let v = 0; v <= yMax + 1e-9; v += yMax / 4) ticks.push(v);
                const xt = n <= 1 ? [] : [0, Math.round((n - 1) / 2), n - 1];
                drawLineChart(
                    [{ name: '훈련 손실', color: TRAIN, values: H.train }, { name: '테스트 손실', color: TEST, values: H.test }],
                    { n, yMin: 0, yMax, yTicks: ticks, yFmt: v => v.toFixed(2), xTicks: xt, xFmt: i => String(i + 1), xLabel: '에포크 →' }
                );
                $('chart-caption').innerHTML = n
                    ? `현재 훈련 손실 <strong class="font-mono">${H.train[n - 1].toFixed(3)}</strong>, 테스트 손실 <strong class="font-mono">${H.test[n - 1].toFixed(3)}</strong>. 손실이 0에 가까울수록 정답 종에 높은 확률을 주고 있다는 뜻이에요.`
                    : `학습을 시작하면 에포크마다 손실이 어떻게 줄어드는지 그려져요. 처음(가중치 0)에는 모든 펭귄에게 확률 0.5를 줘서 손실이 약 0.69예요.`;
                return;
            }

            const key = `${state.tab},${state.fx},${state.fy},${state.seed},${state.testRatio},${state.knn.scale},${state.tree.minLeaf}`;
            if (chartCache.key !== key) {
                chartCache = { key, data: state.tab === 'knn' ? model.accuracyByK() : model.accuracyByDepth() };
            }
            const d = chartCache.data;
            const lo = Math.max(0, Math.floor(Math.min(...d.train, ...d.test) * 10) / 10 - 0.1);
            const isKnn = state.tab === 'knn';
            const n = isKnn ? K_MAX : DEPTH_MAX;
            const cur = (isKnn ? state.knn.k : state.tree.depth) - 1;
            $('chart-title').innerHTML = isKnn
                ? `<i class="fa-solid fa-chart-line text-indigo-600"></i> K에 따른 정확도 변화`
                : `<i class="fa-solid fa-chart-line text-indigo-600"></i> 깊이에 따른 정확도 변화`;
            drawLineChart(
                [{ name: '훈련 정확도', color: TRAIN, values: d.train }, { name: '테스트 정확도', color: TEST, values: d.test }],
                {
                    n, yMin: lo, yMax: 1, yTicks: accTicks(lo), yFmt: v => `${Math.round(v * 100)}%`,
                    xTicks: isKnn ? [0, 4, 9, 14, 19, 24, 29] : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    xFmt: i => String(i + 1), xLabel: isKnn ? 'K →' : '최대 깊이 →', marker: cur
                }
            );
            const bestIdx = d.test.indexOf(Math.max(...d.test));
            $('chart-caption').innerHTML = isKnn
                ? `노란 띠가 지금의 K예요. 테스트 정확도가 가장 높은 K는 <strong>${bestIdx + 1}</strong>(${pct(d.test[bestIdx])})이에요. K = 1이면 자기 자신이 가장 가까운 이웃이라 훈련 정확도가 거의 100%가 돼요.`
                : `노란 띠가 지금의 깊이예요. 테스트 정확도가 가장 높은 깊이는 <strong>${bestIdx + 1}</strong>(${pct(d.test[bestIdx])})이에요. 훈련 정확도만 계속 오르고 테스트 정확도가 멈추거나 떨어지면 과적합이에요.`;
        }

        // ================================================================
        // 결정트리 그림 (SVG)
        // ================================================================
        function renderTreeDiagram(highlight) {
            const root = state.tree.root;
            if (!root) return;
            const NW = 136, NH = 64, GAP = 12, LH = 100;
            let leaf = 0, maxDepth = 0, nodes = 0, leaves = 0;
            (function layout(n) {
                nodes++;
                maxDepth = Math.max(maxDepth, n.depth);
                if (!n.left) { n.lx = leaf++; leaves++; return; }
                layout(n.left); layout(n.right);
                n.lx = (n.left.lx + n.right.lx) / 2;
            })(root);
            const W = leaf * (NW + GAP) + GAP;
            const H = (maxDepth + 1) * LH - (LH - NH) + 24;
            const cx = (n) => GAP + n.lx * (NW + GAP) + NW / 2;
            const cy = (n) => 12 + n.depth * LH;
            const onPath = new Set(highlight || []);

            let edges = '', boxes = '';
            (function walk(n) {
                const x = cx(n), y = cy(n);
                if (n.left) {
                    [[n.left, '예'], [n.right, '아니오']].forEach(([ch, label]) => {
                        const x2 = cx(ch), y2 = cy(ch);
                        const hl = onPath.has(n) && onPath.has(ch);
                        edges += `<path d="M${x},${y + NH} C${x},${y + NH + 22} ${x2},${y2 - 22} ${x2},${y2}" fill="none" stroke="${hl ? '#eab308' : '#94a3b8'}" stroke-width="${hl ? 3.5 : 1.5}"/>`;
                        edges += `<text x="${(x + x2) / 2}" y="${(y + NH + y2) / 2 + 4}" text-anchor="middle" font-size="10" font-weight="700" fill="${label === '예' ? '#4f46e5' : '#e11d48'}" paint-order="stroke" stroke="#f8fafc" stroke-width="3">${label}</text>`;
                    });
                }
                const sp = SPECIES[n.pred];
                const hl = onPath.has(n);
                const isLeaf = !n.left;
                const title = isLeaf
                    ? `🍃 ${sp.short}`
                    : `${FEATURES[n.feature === 0 ? state.fx : state.fy].name} ≤ ${fmtVal(n.threshold)}`;
                let bar = '', bx = x - NW / 2 + 10;
                n.counts.forEach((c, s) => {
                    const bw = (NW - 20) * c / n.n;
                    if (bw > 0) bar += `<rect x="${bx}" y="${y + NH - 14}" width="${bw}" height="7" fill="${SPECIES[s].color}"/>`;
                    bx += bw;
                });
                boxes += `<g><title>${SPECIES.map((s, i) => `${s.short} ${n.counts[i]}`).join(' · ')}</title>`
                    + `<rect x="${x - NW / 2}" y="${y}" width="${NW}" height="${NH}" rx="10" fill="${isLeaf ? `rgba(${sp.rgb.join(',')},0.14)` : '#ffffff'}" stroke="${hl ? '#eab308' : isLeaf ? sp.color : '#cbd5e1'}" stroke-width="${hl ? 3.5 : 1.5}"/>`
                    + `<text x="${x}" y="${y + 19}" text-anchor="middle" font-size="12" font-weight="700" fill="${isLeaf ? sp.color : '#1e293b'}">${escapeHtml(title)}</text>`
                    + `<text x="${x}" y="${y + 35}" text-anchor="middle" font-size="10" fill="#64748b">지니 ${n.gini.toFixed(3)} · ${n.n}마리</text>`
                    + bar + `</g>`;
                if (n.left) { walk(n.left); walk(n.right); }
            })(root);

            $('tree-diagram').innerHTML = `<svg width="${Math.max(W, 300)}" height="${H}" viewBox="0 0 ${Math.max(W, 300)} ${H}" style="font-family:'Noto Sans KR',sans-serif;display:block;margin:0 auto">${edges}${boxes}</svg>`;
            $('tree-info').innerHTML = [['질문 노드', nodes - leaves], ['잎 노드', leaves], ['실제 깊이', maxDepth]]
                .map(([k, v]) => `<div class="p-2 bg-slate-50 border border-slate-200 rounded-xl"><span class="text-[11px] text-slate-500 block">${k}</span><span class="font-mono font-bold text-indigo-700">${v}</span></div>`).join('');
        }

        // ================================================================
        // 화면 갱신
        // ================================================================
        function setStatus(kind) {
            const map = {
                idle:     ['대기 중', 'bg-slate-100 text-slate-600 font-semibold'],
                training: ['학습 중...', 'bg-indigo-600 text-white font-semibold animate-pulse'],
                done:     ['학습 완료', 'bg-emerald-100 text-emerald-700 font-bold']
            };
            const [text, cls] = map[kind];
            $('status-tag').textContent = text;
            $('status-tag').className = `text-xs px-2.5 py-1 rounded-full ${cls}`;
        }

        function updateLegend() {
            const cls = activeClasses();
            let html = SPECIES.map((s, i) => cls.includes(i)
                ? `<span class="flex items-center gap-1.5"><span class="inline-block w-3 h-3 rounded-full ring-2 ring-white shadow" style="background:${s.color}"></span>${s.name}</span>`
                : `<span class="flex items-center gap-1.5 text-slate-300 line-through"><span class="inline-block w-2 h-2 rounded-full bg-slate-300"></span>${s.name}</span>`).join('');
            html += `<span class="flex items-center gap-1.5 text-slate-500">● 훈련</span>`
                + `<span class="flex items-center gap-1.5 text-slate-500">○ 테스트</span>`
                + `<span class="flex items-center gap-1.5 text-slate-500"><span class="text-yellow-500">★</span> 새 펭귄</span>`;
            if (state.tab === 'logi') {
                html += state.logi.ovr
                    ? `<span class="flex items-center gap-1.5 text-slate-500"><span class="inline-block w-4 border-t-2 border-dashed border-slate-500"></span> 종별 경계(p=0.5)</span>`
                    : `<span class="flex items-center gap-1.5 text-slate-500"><span class="inline-block w-4 border-t-2 border-yellow-400"></span> 결정 경계(p=0.5)</span>`;
            }
            $('legend').innerHTML = html;
        }

        function updateSplitInfo() {
            const tr = DATA.filter(p => !p.test).length;
            $('split-count').textContent = `훈련 ${tr} · 테스트 ${DATA.length - tr}`;
            $('species-table').innerHTML = SPECIES.map((s, i) => {
                const all = DATA.filter(p => p.s === i);
                const te = all.filter(p => p.test).length;
                return `<span class="px-2 py-1 rounded-lg border bg-white" style="border-color:${s.color}55"><strong style="color:${s.color}">${s.short}</strong> <span class="font-mono text-slate-600">${all.length - te}/${te}</span></span>`;
            }).join('') + `<span class="px-1 py-1 text-slate-400">(훈련/테스트)</span>`;
            $('seed-val').textContent = `#${state.seed}`;
        }

        function updateMetrics() {
            const e = evaluation;
            const tr = e.train.n ? e.train.ok / e.train.n : 0;
            const te = e.test.n ? e.test.ok / e.test.n : 0;
            $('metric-train').textContent = pct(tr);
            $('metric-test').textContent = pct(te);

            let msg, tone;
            const untrained = state.tab === 'logi' && state.logi.totalEpochs === 0;
            if (untrained) {
                msg = `💡 아직 학습 전이에요. '학습 시작'을 눌러 보세요. 지금은 모든 펭귄을 한 종으로만 예측하고 있어요.`;
                tone = 'bg-slate-50 text-slate-700 border-slate-200';
            } else if (tr - te >= 0.1) {
                msg = `⚠️ 훈련 정확도(${pct(tr)})보다 테스트 정확도(${pct(te)})가 많이 낮아요. 훈련 데이터를 '외워 버린' <strong>과적합(overfitting)</strong>일 수 있어요.`;
                tone = 'bg-rose-50 text-rose-800 border-rose-200';
            } else if (tr - te >= 0.05) {
                msg = `🔍 테스트 정확도(${pct(te)})가 훈련 정확도(${pct(tr)})보다 조금 낮아요. 아래 그래프에서 하이퍼파라미터를 바꾸면 차이가 어떻게 변하는지 살펴보세요. ('다시 섞어 나누기'로 우연인지도 확인해 보세요.)`;
                tone = 'bg-amber-50 text-amber-800 border-amber-200';
            } else if (tr < 0.8) {
                msg = `🤔 훈련 데이터도 잘 못 맞혀요. 모델이 너무 단순한 <strong>과소적합(underfitting)</strong>이거나, 고른 두 특성으로는 종을 구분하기 어려울 수 있어요. 축을 바꿔 보세요.`;
                tone = 'bg-amber-50 text-amber-800 border-amber-200';
            } else {
                msg = `👍 훈련 정확도와 테스트 정확도가 비슷해요. 처음 보는 펭귄에도 잘 통하는(일반화가 잘 된) 모델이에요.`;
                tone = 'bg-emerald-50 text-emerald-800 border-emerald-200';
            }
            $('fit-message').className = `mt-2 p-2.5 rounded-xl text-xs border break-keep ${tone}`;
            $('fit-message').innerHTML = msg;

            // 혼동 행렬
            const set = e[state.cmSet];
            const cls = e.classes;
            const maxCell = Math.max(1, ...cls.flatMap(a => cls.map(b => set.cm[a][b])));
            let html = `<table class="w-full text-xs text-center border-separate" style="border-spacing:3px"><thead><tr>`
                + `<th class="text-[10px] text-slate-400 font-normal text-right pr-1">실제 ↓ / 예측 →</th>`
                + cls.map(c => `<th class="font-bold pb-1" style="color:${SPECIES[c].color}">${SPECIES[c].short}</th>`).join('')
                + `<th class="text-[10px] text-slate-400 font-normal">재현율</th></tr></thead><tbody>`;
            cls.forEach(a => {
                const rowSum = cls.reduce((s, b) => s + set.cm[a][b], 0);
                html += `<tr><th class="font-bold text-right pr-1" style="color:${SPECIES[a].color}">${SPECIES[a].short}</th>`;
                cls.forEach(b => {
                    const v = set.cm[a][b];
                    const alpha = v ? 0.15 + 0.6 * v / maxCell : 0;
                    const bg = a === b ? `rgba(16,185,129,${alpha})` : `rgba(244,63,94,${alpha})`;
                    html += `<td class="py-2 rounded-lg font-mono font-bold ${v ? 'text-slate-900' : 'text-slate-300'} border border-slate-200" style="background:${bg}">${v}</td>`;
                });
                html += `<td class="font-mono text-slate-500">${rowSum ? pct(set.cm[a][a] / rowSum) : '-'}</td></tr>`;
            });
            html += `</tbody></table>`;
            $('confusion-matrix').innerHTML = html;
            document.querySelectorAll('.cm-btn').forEach(b => {
                b.className = `cm-btn px-2.5 py-1 rounded-md font-semibold ${b.dataset.cm === state.cmSet ? 'bg-white text-indigo-700 shadow-sm' : 'text-slate-500'}`;
            });
        }

        function probaBars(proba, label) {
            return `<div class="text-[11px] text-slate-500 mb-1">${label}</div>` + activeClasses().map(c => `
                <div class="flex items-center gap-2 mb-1">
                    <span class="w-12 font-bold" style="color:${SPECIES[c].color}">${SPECIES[c].short}</span>
                    <div class="flex-grow h-3 bg-slate-100 rounded-full overflow-hidden"><div class="h-full rounded-full" style="width:${(proba[c] * 100).toFixed(1)}%;background:${SPECIES[c].color}"></div></div>
                    <span class="w-12 text-right font-mono text-slate-600">${pct(proba[c])}</span>
                </div>`).join('');
        }

        function updatePrediction() {
            const box = $('prediction-box');
            if (!state.query) {
                box.innerHTML = `<div class="p-3 bg-slate-50 border border-dashed border-slate-300 rounded-xl text-slate-500 text-center">캔버스를 클릭하거나 왼쪽 아래에 측정값을 입력하면<br>새 펭귄이 어떤 종인지 AI가 예측해요. 🐧</div>`;
                return;
            }
            const { x, y } = state.query;
            const r = model.predict(x, y);
            const sp = SPECIES[r.cls];
            let html = `<div class="flex items-center justify-between gap-2 p-3 rounded-xl border mb-3" style="background:rgba(${sp.rgb.join(',')},0.1);border-color:${sp.color}66">
                    <div><div class="text-[11px] text-slate-500 font-mono">${FEATURES[state.fx].name} ${fmtVal(x)}${FEATURES[state.fx].unit} · ${FEATURES[state.fy].name} ${fmtVal(y)}${FEATURES[state.fy].unit}</div>
                    <div class="text-lg font-extrabold" style="color:${sp.color}">🐧 ${sp.name}</div></div>
                    <span class="text-xs text-slate-500">(으)로 예측했어요</span></div>`;

            if (model.type === 'knn') {
                const k = r.list.length;
                html += probaBars(r.proba, `가장 가까운 이웃 ${k}마리의 투표 결과`);
                const counts = activeClasses().map(c => `${SPECIES[c].short} ${Math.round(r.proba[c] * k)}마리`).join(', ');
                const tie = activeClasses().filter(c => Math.round(r.proba[c] * k) === Math.round(r.proba[r.cls] * k)).length > 1;
                html += `<div class="mt-2 p-2.5 bg-indigo-50/60 border border-indigo-100 rounded-xl text-indigo-900">이웃 ${k}마리 중 ${counts} → <strong>다수결로 ${sp.short}</strong>${tie ? ' (동점이라 가장 가까운 이웃의 종을 따랐어요)' : ''}.<br><span class="text-indigo-700">캔버스에서 노란 원으로 표시된 펭귄들이 이웃이에요.</span></div>`;
            } else if (model.type === 'logi') {
                const L = state.logi;
                if (!L.ovr) {
                    const pos = SPECIES[L.pair[1]].short;
                    html += probaBars(r.proba, '로지스틱 회귀가 계산한 확률');
                    html += `<div class="mt-2 p-2.5 bg-indigo-50/60 border border-indigo-100 rounded-xl text-indigo-900 font-mono text-[11px] leading-relaxed">z = ${fmtNum(r.z)} → σ(z) = ${r.p.toFixed(3)}<br><span class="font-sans">${pos}일 확률이 ${pct(r.p)}로 0.5 ${r.p >= 0.5 ? '이상' : '미만'}이라서 <strong>${sp.short}</strong>로 분류했어요.</span></div>`;
                } else {
                    html += probaBars(r.proba, '세 분류기의 σ 값을 합이 1이 되도록 나눈 확률');
                    html += `<div class="mt-2 p-2.5 bg-indigo-50/60 border border-indigo-100 rounded-xl text-indigo-900 text-[11px] leading-relaxed">`
                        + L.models.map(m => `• ${SPECIES[m.cls].short} vs 나머지: σ = <span class="font-mono">${r.sig[m.cls].toFixed(3)}</span>`).join('<br>')
                        + `<br>→ σ 값이 가장 큰 <strong>${sp.short}</strong>를 골랐어요.</div>`;
                }
            } else {
                const leaf = r.path[r.path.length - 1];
                html += probaBars(r.proba, `도착한 잎 노드의 펭귄 비율 (${leaf.n}마리)`);
                const steps = r.path.slice(0, -1).map(n => {
                    const f = n.feature === 0 ? state.fx : state.fy;
                    const v = n.feature === 0 ? x : y;
                    const yes = v <= n.threshold;
                    return `${FEATURES[f].name} ≤ ${fmtVal(n.threshold)}? <strong class="${yes ? 'text-indigo-700' : 'text-rose-600'}">${yes ? '예' : '아니오'}</strong>`;
                });
                html += `<div class="mt-2 p-2.5 bg-indigo-50/60 border border-indigo-100 rounded-xl text-indigo-900 text-[11px] leading-relaxed">`
                    + (steps.length ? steps.map((s, i) => `${i + 1}. ${s}`).join('<br>') + `<br>` : '')
                    + `→ 잎 노드에서 가장 많은 종인 <strong>${sp.short}</strong>로 예측했어요. 아래 트리 그림에 노란색으로 경로를 표시했어요.</div>`;
            }
            box.innerHTML = html;
        }

        function updateLogiEquation() {
            const L = state.logi;
            const fxn = FEATURES[state.fx].name, fyn = FEATURES[state.fy].name;
            const sign = (v) => `${v >= 0 ? '+' : '−'} ${fmtNum(Math.abs(v))}`;
            $('logi-equation').innerHTML = L.models.map(m => {
                const { W1, W2, B } = rawWeights(m);
                const head = L.ovr ? `<span class="text-slate-400">[${SPECIES[m.cls].short}]</span> ` : '';
                return `<div>${head}z = ${fmtNum(W1)}×${fxn} ${sign(W2)}×${fyn} ${sign(B)}</div>`;
            }).join('') + (L.ovr ? '' : `<div class="text-slate-300 text-[11px] font-normal mt-1">p = ${SPECIES[L.pair[1]].short}일 확률 = 1 / (1 + e<sup>−z</sup>)</div>`);
            $('cumulative-val').textContent = L.totalEpochs;

            const btns = $('sigmoid-class-btns');
            btns.classList.toggle('hidden', !L.ovr);
            if (L.ovr) {
                btns.innerHTML = [0, 1, 2].map(c => `<button data-view="${c}" class="px-2 py-0.5 rounded-md font-semibold ${c === L.viewClass ? 'bg-white shadow-sm' : 'text-slate-500'}" style="${c === L.viewClass ? `color:${SPECIES[c].color}` : ''}">${SPECIES[c].short} vs 나머지</button>`).join('');
            }
        }

        function updateQueryHint() {
            const f1 = FEATURES[state.fx], f2 = FEATURES[state.fy];
            $('query-hint').innerHTML = `<i class="fa-solid fa-circle-info mr-1 text-slate-400"></i>순서는 <strong class="text-indigo-600">(${f1.name} ${f1.unit}, ${f2.name} ${f2.unit})</strong>이고, `
                + `${f1.name}는 <strong class="text-indigo-600">${fmtVal(rx().min)}~${fmtVal(rx().max)}</strong>, ${f2.name}는 <strong class="text-indigo-600">${fmtVal(ry().min)}~${fmtVal(ry().max)}</strong> 사이로 입력하세요. <kbd>Enter</kbd> 예측`;
        }

        // 모델을 다시 만들고 모든 화면을 갱신 (modelChanged=false 면 그림만 다시 그림)
        function refresh(modelChanged = true) {
            if (modelChanged) {
                if (state.tab === 'knn') model = buildKNN();
                else if (state.tab === 'logi') model = buildLogi();
                else model = buildTree();
                evaluation = evaluate();
                regionDirty = true;
                updateMetrics();
                drawChart();
                if (state.tab === 'logi') updateLogiEquation();
            }
            updateLegend();
            updateSplitInfo();
            updatePrediction();
            draw();
            if (state.tab === 'logi') drawSigmoid();
            if (state.tab === 'tree') {
                const path = state.query ? model.predict(state.query.x, state.query.y).path : null;
                renderTreeDiagram(path);
            }
        }

        // ================================================================
        // 로지스틱 회귀 학습 제어
        // ================================================================
        function startTraining() {
            const L = state.logi;
            if (L.isTraining) return;
            L.isTraining = true;
            setStatus('training');
            let done = 0;
            const duration = Math.min(2500, Math.max(600, L.epochs * 6));
            const startTime = performance.now();
            function runFrame(now) {
                if (!L.isTraining) return;
                const progress = Math.min(1, (now - startTime) / duration);
                const target = Math.max(done + 1, Math.round(L.epochs * progress));
                while (done < Math.min(target, L.epochs)) { stepLogi(); done++; }
                refresh();
                if (done >= L.epochs) {
                    L.isTraining = false;
                    setStatus('done');
                    return;
                }
                requestAnimationFrame(runFrame);
            }
            requestAnimationFrame(runFrame);
        }

        // ================================================================
        // 새 펭귄 입력
        // ================================================================
        function setQueryFromInput() {
            const text = $('query-input').value.replace(/（/g, '(').replace(/）/g, ')').replace(/，/g, ',');
            const nums = (text.match(/[-+]?(?:\d+\.?\d*|\.\d+)/g) || []).map(parseFloat);
            const fb = $('query-feedback');
            const fail = (msg) => {
                fb.className = 'mt-2 p-2.5 rounded-xl text-xs border bg-rose-50 text-rose-800 border-rose-200';
                fb.innerHTML = msg;
                showToast('측정값을 읽지 못했어요. 입력창 아래 안내를 확인하세요.', 'warning');
            };
            if (!text.trim()) return fail('❌ 측정값을 입력해 주세요. 예) (45, 17)');
            if (nums.length !== 2) return fail(`❌ 숫자 2개가 필요해요. (지금 ${nums.length}개) 예) (45, 17)`);
            const [x, y] = nums;
            if (x < rx().min || x > rx().max || y < ry().min || y > ry().max) {
                return fail(`⚠️ 화면 범위를 벗어났어요. ${FEATURES[state.fx].name} ${fmtVal(rx().min)}~${fmtVal(rx().max)}, ${FEATURES[state.fy].name} ${fmtVal(ry().min)}~${fmtVal(ry().max)} 사이로 입력하세요.`);
            }
            fb.className = 'mt-2 p-2.5 rounded-xl text-xs border bg-emerald-50 text-emerald-800 border-emerald-200';
            fb.innerHTML = `✅ (${fmtVal(x)}, ${fmtVal(y)}) 위치에 새 펭귄을 놓았어요. 오른쪽에서 예측 결과를 확인하세요.`;
            state.query = { x, y };
            refresh(false);
        }

        function clearQuery() {
            state.query = null;
            $('query-feedback').classList.add('hidden');
            $('query-input').value = '';
            refresh(false);
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

        // ================================================================
        // 이벤트 연결
        // ================================================================
        function setTab(tab) {
            state.tab = tab;
            state.logi.isTraining = false;
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('tab-btn-active', b.dataset.tabBtn === tab));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('text-slate-600', b.dataset.tabBtn !== tab));
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.toggle('hidden', p.dataset.tab !== tab));
            if (tab === 'logi' && state.logi.key === logiKey()) setStatus(state.logi.totalEpochs ? 'done' : 'idle');
            refresh();
        }
        document.querySelectorAll('.tab-btn').forEach(b => b.addEventListener('click', () => setTab(b.dataset.tabBtn)));

        function fillFeatureSelects() {
            ['feature-x', 'feature-y'].forEach((id, axis) => {
                $(id).innerHTML = FEATURES.map((f, i) => `<option value="${i}">${f.name} (${f.unit})</option>`).join('');
                $(id).value = axis === 0 ? state.fx : state.fy;
            });
        }
        function onFeatureChange(axis, value) {
            const v = parseInt(value, 10);
            if (axis === 0) {
                if (v === state.fy) state.fy = state.fx;   // 같은 특성을 고르면 두 축을 서로 바꿈
                state.fx = v;
            } else {
                if (v === state.fx) state.fx = state.fy;
                state.fy = v;
            }
            $('feature-x').value = state.fx;
            $('feature-y').value = state.fy;
            state.query = null;
            $('query-feedback').classList.add('hidden');
            updateQueryHint();
            refresh();
        }
        $('feature-x').addEventListener('change', e => onFeatureChange(0, e.target.value));
        $('feature-y').addEventListener('change', e => onFeatureChange(1, e.target.value));

        $('test-slider').addEventListener('input', e => {
            state.testRatio = parseInt(e.target.value, 10) / 100;
            $('test-val').textContent = `${e.target.value}%`;
            splitData();
            refresh();
        });
        $('reshuffle-btn').addEventListener('click', () => {
            state.seed = Math.floor(Math.random() * 9000) + 1000;
            splitData();
            refresh();
            showToast('훈련/테스트 데이터를 새로 나눴어요. 정확도가 어떻게 바뀌는지 보세요.');
        });

        $('toggle-region').addEventListener('change', e => { state.showRegion = e.target.checked; draw(); });
        $('toggle-test').addEventListener('change', e => { state.showTest = e.target.checked; draw(); });
        $('toggle-wrong').addEventListener('change', e => { state.showWrong = e.target.checked; draw(); });
        document.querySelectorAll('.cm-btn').forEach(b => b.addEventListener('click', () => { state.cmSet = b.dataset.cm; updateMetrics(); }));

        $('k-slider').addEventListener('input', e => {
            state.knn.k = parseInt(e.target.value, 10);
            $('k-val').textContent = state.knn.k;
            refresh();
        });
        $('knn-scale').addEventListener('change', e => { state.knn.scale = e.target.checked; refresh(); });

        $('pair-select').addEventListener('change', e => {
            state.logi.pair = e.target.value.split(',').map(Number);
            state.query = null;
            refresh();
        });
        $('ovr-toggle').addEventListener('change', e => {
            state.logi.ovr = e.target.checked;
            $('pair-select').disabled = state.logi.ovr;
            $('pair-select').classList.toggle('opacity-50', state.logi.ovr);
            refresh();
            showToast(state.logi.ovr ? '3종 모두 분류 모드예요. 분류기 3개를 동시에 학습해요.' : '두 종 분류 모드로 돌아왔어요.');
        });
        $('sigmoid-class-btns').addEventListener('click', e => {
            const b = e.target.closest('button[data-view]');
            if (!b) return;
            state.logi.viewClass = parseInt(b.dataset.view, 10);
            updateLogiEquation();
            drawSigmoid();
        });
        $('epochs-slider').addEventListener('input', e => {
            state.logi.epochs = parseInt(e.target.value, 10);
            $('epochs-val').textContent = `${state.logi.epochs}회`;
        });
        $('lr-slider').addEventListener('input', e => {
            state.logi.lr = parseFloat(e.target.value);
            $('lr-val').textContent = state.logi.lr.toFixed(2);
        });
        $('train-btn').addEventListener('click', startTraining);
        $('step-btn').addEventListener('click', () => { if (!state.logi.isTraining) { stepLogi(); setStatus('done'); refresh(); } });
        $('reset-model-btn').addEventListener('click', () => {
            resetLogi();
            refresh();
            showToast('가중치 및 누적 에포크가 초기화되었습니다.');
        });

        $('depth-slider').addEventListener('input', e => {
            state.tree.depth = parseInt(e.target.value, 10);
            $('depth-val').textContent = state.tree.depth;
            refresh();
        });
        $('leaf-slider').addEventListener('input', e => {
            state.tree.minLeaf = parseInt(e.target.value, 10);
            $('leaf-val').textContent = `${state.tree.minLeaf}마리`;
            refresh();
        });

        // 캔버스: 클릭하면 새 펭귄, 마우스를 올리면 좌표 표시
        function eventToData(e) {
            const rect = canvas.getBoundingClientRect();
            const px = e.clientX - rect.left, py = e.clientY - rect.top;
            if (px < plot.x || px > plot.x + plot.w || py < plot.y || py > plot.y + plot.h) return null;
            return fromPx(px, py);
        }
        canvas.addEventListener('pointerdown', e => {
            const d = eventToData(e);
            if (!d) return;
            state.query = { x: Math.round(d[0] * 10) / 10, y: Math.round(d[1] * 10) / 10 };
            $('query-input').value = `(${fmtVal(state.query.x)}, ${fmtVal(state.query.y)})`;
            $('query-feedback').classList.add('hidden');
            refresh(false);
        });
        canvas.addEventListener('pointermove', e => {
            const d = eventToData(e);
            const badge = $('hover-badge');
            if (!d) { badge.classList.add('hidden'); return; }
            const { cls } = model.predict(d[0], d[1]);
            badge.innerHTML = `${FEATURES[state.fx].name} <span class="font-bold text-yellow-300">${fmtVal(Math.round(d[0] * 10) / 10)}</span> · ${FEATURES[state.fy].name} <span class="font-bold text-yellow-300">${fmtVal(Math.round(d[1] * 10) / 10)}</span> ➔ <span class="font-bold" style="color:${SPECIES[cls].color}">${SPECIES[cls].short}</span>`;
            badge.classList.remove('hidden');
        });
        canvas.addEventListener('pointerleave', () => $('hover-badge').classList.add('hidden'));

        $('query-btn').addEventListener('click', setQueryFromInput);
        $('query-clear-btn').addEventListener('click', clearQuery);
        $('query-input').addEventListener('keydown', e => {
            if (e.key === 'Enter' && !e.isComposing && e.keyCode !== 229) {
                e.preventDefault();
                setQueryFromInput();
            }
        });

        window.addEventListener('resize', () => {
            resizeCanvas();
            if (model) { drawChart(); if (state.tab === 'logi') drawSigmoid(); }
        });

        window.onload = function () {
            fillFeatureSelects();
            updateQueryHint();
            splitData();
            setTab('knn');
            resizeCanvas();
        };
    </script>
</body>
</html>
"""

# HTML을 화면에 배치
#  - streamlit 1.56 이상: st.iframe 사용 (내용 높이에 맞춰 화면 높이가 자동으로 조절됨)
#  - 그보다 낮은 버전: 예전 방식인 components.html 사용 (고정 높이 + 스크롤)
#    ※ 결정트리 탭은 트리 그림까지 있어서 다른 단계보다 화면이 깁니다.
if hasattr(st, "iframe"):
    st.iframe(html_code, height="content")
else:
    components.html(html_code, height=2300, scrolling=True)
