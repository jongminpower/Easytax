import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 & 프리미엄 다크 테마 (넛지 디자인)
st.set_page_config(page_title="Invisible Hand | 지식의 본질", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto+Sans+KR', sans-serif; background-color: #0F1115; color: #E0E0E0; }
    
    /* 입력창 및 레이블 스타일 */
    .stSelectbox label, .stTextArea label, .stTextInput label { color: #8899A6; font-size: 14px; font-weight: 500; }
    .stTextArea textarea { background-color: #1A1D23; border: 1px solid #30363D; color: #FFFFFF; border-radius: 12px; }
    
    /* 버튼 스타일 (고급스러운 블루) */
    .stButton button { 
        background-color: #2D5BFF; color: white; border-radius: 8px; 
        width: 100%; font-weight: 700; height: 3.5em; border: none; margin-top: 20px;
    }
    .stButton button:hover { background-color: #1A44D1; border: none; }

    /* 결과 출력 박스 */
    .result-card { 
        background-color: #1A1D23; padding: 25px; border-radius: 15px; 
        border-left: 5px solid #2D5BFF; margin-top: 30px; line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 상단 네비게이션 (체계적 분류)
st.title("🍎 Invisible Hand")
st.write("전문직 시험의 복잡한 용어를 '직관'으로 바꿉니다.")

col1, col2 = st.columns(2)
with col1:
    subject = st.selectbox("과목 선택", ["세법", "회계학", "재정학", "상법"])
with col2:
    chapter = st.text_input("챕터 입력", placeholder="예: 부가가치세법-총설")

# 3. 사이드바: 보안 설정
with st.sidebar:
    st.header("⚙️ 설정")
    api_key = st.text_input("Gemini API Key", type="password", help="Google AI Studio에서 발급받은 키를 입력하세요.")
    st.info(f"선택된 과목: {subject}\n\n현재 챕터: {chapter}")

# 4. 메인 엔진 (Gemini 1.5 Flash 연결)
if api_key:
    try:
        genai.configure(api_key=api_key)
        # 404 오류 방지를 위해 정확한 모델명 'gemini-1.5-flash' 사용
        model = genai.GenerativeModel('gemini-1.5-flash')

        raw_input = st.text_area("이해하기 어려운 조문이나 개념을 입력하세요", height=180, 
                                placeholder="예: 경원자 소송이란...")

        if st.button("본질 추출 및 AI 영상 시나리오 생성"):
            if not raw_input or not chapter:
                st.warning("과목/챕터 정보와 조문 내용을 모두 입력해 주세요.")
            else:
                # 본부장님의 '공부 본질' 철학이 담긴 프롬프트
                prompt = f"""
                당신은 한국 최고의 전문직 수험 전문가입니다. {subject} 과목의 {chapter} 내용을 분석하세요.
                
                [입력된 내용]: {raw_input}

                한국인 수험생의 입장에서 다음 4단계를 한국어로 출력하세요:
                1. [직관적 비유]: 이 개념의 본질을 '빨간 사과'처럼 쉬운 실생활 비유로 설명.
                2. [핵심 키워드]: 시험장에 가져갈 단어 3개를 뽑고 이유 설명.
                3. [실제 사례 & 영상 시나리오]: 이 조문이 적용된 실제 판례/사례를 스토리텔링하고, 
                   이를 30초 영상으로 만든다면 필요한 장면(Scene) 3개를 시각적으로 묘사.
                4. [자기 언어화 넛지]: "결국 이 내용은 [ ]이다"라고 스스로 정의할 수 있게 유도.
                """
                
                with st.spinner('지식의 본질을 추출하는 중...'):
                    response = model.generate_content(prompt)
                    st.markdown(f'<div class="result-card"><h3>📍 {subject} : {chapter}</h3><br>{response.text}</div>', unsafe_allow_html=True)
                    
                    # 기록 저장 기능 (넛지)
                    st.success(f"분석 완료! 이 내용은 {subject} 지식 창고에 자동 기록 준비가 되었습니다.")
    
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
else:
    st.info("사이드바에 API Key를 입력하면 본부장님의 AI 비서가 가동됩니다.")

