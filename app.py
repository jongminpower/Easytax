import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 (심리적 안정감을 주는 컬러 테마)
st.set_page_config(page_title="정선식 세법 힐링센터", page_icon="🌿", layout="centered")

# --- 🎨 본부장님 전용 힐링 컬러 디자인 (CSS) ---
st.markdown("""
    <style>
    /* 메인 배경: 아주 연한 크림색 */
    .stApp {
        background-color: #fdfdfa;
    }
    /* 타이틀 색상: 짙은 웜 그레이 */
    h1, h2, h3, p {
        color: #4a4a4a !important;
        font-family: 'Nanum Gothic', sans-serif;
    }
    /* 입력창: 부드러운 화이트 */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
    }
    /* 버튼: 마음을 평온하게 하는 소프트 민트 */
    .stButton > button {
        background-color: #a3d9c9;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #8dcabd;
        transform: translateY(-2px);
    }
    /* 결과 박스: 따뜻한 아이보리 */
    .stMarkdown {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_value=True)

# 2. 사이드바 - 열쇠(API 키) 입력창 (최소한의 노출)
with st.sidebar:
    st.markdown("### 🗝️ 시스템 연결")
    api_key = st.text_input("Gemini API Key를 넣어주세요", type="password")
    st.caption("본부장님의 소중한 키는 안전하게 보호됩니다.")

# 3. 메인 타이틀 (친근하고 편안하게)
st.title("🌿 정선식 세법 힐링센터")
st.subheader("외우지 마세요. 그냥 '이야기'로 들으세요.")
st.write("---")

# --- 🚀 [본부장님 특명] 단순화된 퀵 버튼 (UX 개선) ---
st.write("💡 많은 분들이 억울해하는 주제들입니다. 클릭해 보세요.")
col1, col2, col3 = st.columns(3)

# 버튼을 누르면 그 용어가 입력창에 자동으로 들어가게 하는 로직
preset_query = ""
with col1:
    if st.button("🚛 타사업장 반출"):
        preset_query = "타사업장 반출"
with col2:
    if st.button("🏠 간주임대료"):
        preset_query = "간주임대료"
with col3:
    if st.button("💰 매입세액 공제"):
        preset_query = "매입세액 공제"

st.write("---")

# 4. 사용자 입력 (질문을 부드럽게 변형)
query = st.text_input("지금 어떤 세법 용어가 당신을 괴롭히나요?", value=preset_query, placeholder="예: 간주공급, 부가가치세...")

# 5. AI 엔진 로직 (본부장님의 페르소나 + 힐링 멘트 주입)
if query:
    if not api_key:
        st.warning("⚠️ 왼쪽 사이드바에 'API Key'를 먼저 넣어주셔야 제가 움직일 수 있습니다.")
    else:
        try:
            # AI 세팅
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 본부장님이 원하시는 '정선식 + 힐링' 지시서(프롬프트)
            prompt = f"""
            너는 대한민국에서 세법을 가장 쉽게 가르치는 '정선식 세법 힐링 멘토'다. 
            사용자의 질문을 아래 4단계 원칙에 따라, 아주 친근하고 다정하게 설명해라.
            
            1. [공감]: "그 마음 이해합니다. 참 난해하죠?" 같은 멘트로 시작.
            2. [본질/Why]: 이 법이 생긴 이유를 '나랏돈'과 '세무서 사정' 관점에서 억울함을 풀어주듯 설명.
            3. [정선식 비유]: 일상생활의 사례나 상황극(경선식 스타일)으로 비유하여 머리에 박히게 설명.
            4. [힐링 한줄]: 시험장이나 실무에서 절대 까먹지 않을 결정적 한 줄 요약.
            
            용어: {query}
            """
            
            with st.spinner('본부장님, 가장 편안한 비유를 가져오는 중입니다... ☕'):
                response = model.generate_content(prompt)
                
            # 결과 출력 (깔끔한 카드 형식)
            st.success(f"'{query}'에 대한 정선식 힐링 풀이입니다.")
            st.markdown(response.text)
            
            st.divider()
            st.caption("💡 이 설명이 부족하다면? '더 쉽게 사례를 들어줘'라고 다시 물어보세요.")

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

# 6. 하단 안내 (본부장님의 브랜딩)
st.write("---")
st.caption("웅지세무대학교 이종민 본부장 x AI 협업 시스템 v2.0 (RELAX Edition)")
