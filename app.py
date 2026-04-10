import streamlit as st
import google.generativeai as genai

# 1. 프리미엄 학습 UX 설정
st.set_page_config(page_title="Invisible Hand | 지식의 본질", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #0A0B0D; color: #D1D5DB; }
    .main-card { background-color: #16181D; padding: 24px; border-radius: 16px; border: 1px solid #2D3139; margin-bottom: 20px; }
    .stTextArea textarea { background-color: #1F2229; border: 1px solid #3F444E; color: #FFFFFF; border-radius: 12px; }
    .stButton button { 
        background: linear-gradient(135deg, #2D5BFF 0%, #1A44D1 100%); 
        color: white; border-radius: 10px; border: none; padding: 12px; font-weight: 700; width: 100%;
    }
    .sidebar-content { background-color: #111318; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 3px solid #2D5BFF; }
    </style>
    """, unsafe_allow_html=True)

# 2. 사이드바: 학습 기록 (오르비식 리스트 모방)
with st.sidebar:
    st.markdown("### 📚 **나의 학습 창고**")
    st.markdown("<div class='sidebar-content'>행정소송법 - 경원자 소송</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-content'>부가가치세법 - 간주공급</div>", unsafe_allow_html=True)
    st.divider()
    api_key = st.text_input("Gemini API Key", type="password", help="AI Studio에서 발급받은 키를 입력하세요.")

# 3. 메인 대시보드 (2컬럼 구조)
st.markdown("### 🍎 **Invisible Hand** <span style='font-size:14px; color:#6B7280;'>| 전문직 수험 직관화 플랫폼</span>", unsafe_allow_html=True)

col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        subject = st.selectbox("과목 선택", ["세법", "회계학", "재정학", "상법"])
    with c2:
        chapter = st.text_input("챕터 입력", placeholder="예: 소득세법 - 이자소득")
    
    raw_input = st.text_area("분석할 조문 또는 개념을 입력하세요", height=250)
    
    if st.button("본질 추출 및 AI 영상 시나리오 생성"):
        if api_key and raw_input:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            당신은 한국 최고의 수험 전문가입니다. {subject} 과목의 {chapter} 내용을 분석하세요.
            [입력]: {raw_input}
            1. [직관 비유]: 사과처럼 쉬운 한 줄 비유로 '본질' 정의.
            2. [핵심 키워드]: 시험장에 가져갈 암기용 키워드 3개와 설명.
            3. [실제 사례]: 이 조문이 적용된 실제 판례나 상황 스토리텔링.
            4. [AI 영상 연출]: 이 사례를 30초 영상으로 만든다면 필요한 3장면 묘사.
            5. [내 언어 챌린지]: "결국 이 내용은 [ ] 이다" 빈칸 채우기 유도.
            """
            
            with st.spinner('사고의 본질을 추출 중...'):
                response = model.generate_content(prompt)
                st.session_state['result'] = response.text
        else:
            st.error("API 키와 내용을 모두 입력해 주세요.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("#### 💡 **공부 고수의 넛지**")
    st.info("이윤규 변호사의 '패턴 학습법'이 적용 중입니다. 이해가 안 갈 땐 '비유'에 집중하세요.")
    st.divider()
    st.markdown("#### 🎬 **영상 제작 가이드**")
    st.write("생성된 시나리오는 향후 Veo API를 통해 실제 영상으로 제작될 예정입니다.")
    st.markdown("</div>", unsafe_allow_html=True)

# 4. 결과 출력
if 'result' in st.session_state:
    st.markdown(f"<div class='main-card'><h4>📍 {subject} > {chapter} 분석 결과</h4><br>{st.session_state['result']}</div>", unsafe_allow_html=True)