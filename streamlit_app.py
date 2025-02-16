import streamlit as st
import pdf2image
import io
import json
import base64
import google.generativeai as genai

# AIzaSyALL7qeWD1wQylmcIuBd4tzz6P-lfzAt1Y
#AIzaSyALL7qeWD1wQylmcIuBd4tzz6P-lfzAt1Y
#genai.configure(api_key=st.secrets.GOOGLE_API_KEY)

genai.configure(api_key="AIzaSyALL7qeWD1wQylmcIuBd4tzz6P-lfzAt1Y")


# Define cached functions
@st.cache_data()
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

@st.cache_data()
def get_gemini_response_keywords(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

@st.cache_data()
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("لا توجد سيرة ذاتية مرفوعة")

# Streamlit App

st.set_page_config(page_title="ATS Resume Scanner")

input_text = st.text_area(" الوصف الكامل للوظيفة", key="input")
uploaded_file = st.file_uploader("قم برفع سيرتك الذاتية (PDF)...", type=["pdf"],
                     help="الحد الأقصى لحجم الملف: 200MB • PDF فقط" )

# 3. إخفاء الهيدر والفوتر باستخدام CSS
rtl_css = """
<style>
    /* تطبيق RTL على كل العناصر */
    * {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* تعديلات خاصة لعناصر Streamlit */
    .stTextArea textarea { padding-right: 15px !important; }
    .stButton>button { margin-right: auto !important; }
    .stFileUploader { text-align: right !important; }
    .stSelectbox select { padding-right: 20px !important; }
    
    /* إخفاء العناصر غير المرغوبة */
    #MainMenu, footer, header, _profileContainer_gzau3_53 { visibility: hidden !important; }
</style>
"""
st.markdown(rtl_css, unsafe_allow_html=True)

if 'resume' not in st.session_state:
    st.session_state.resume = None

if uploaded_file is not None:
    st.write("تم تحميل ملف الـ PDF بنجاح.")
    st.session_state.resume = uploaded_file

col1, col2 = st.columns(2, gap="medium")

with col1:
    submit1 = st.button("تقييم السيرة الذاتية")

with col2:
    submit2 = st.button("فحص مطابقة السيرة الذاتية لنضام ATS")

    

input_prompt1 = """
أنت مدير موارد بشرية تقني ذو خبرة، ومهمتك هي مراجعة السيرة الذاتية المقدمة مقارنةً بوصف الوظيفة.
يرجى مشاركة تقييمك المهني حول ما إذا كان ملف المرشح يتماشى مع متطلبات الدور.
قم بتسليط الضوء على نقاط القوة والضعف للمتقدم فيما يتعلق بمتطلبات الوظيفة المحددة.
"""

input_prompt2 = """
أنت خبير في أنظمة تتبع المتقدمين (ATS) ولديك فهم عميق لعلوم البيانات ووظائف ATS،
مهمتك هي تقييم السيرة الذاتية مقارنة بوصف الوظيفة المقدم. يجب أن تكون النتيجة أولًا كنسبة مئوية من المطابقة،
ثم الكلمات الرئيسية المفقودة وأخيرًا الأفكار النهائية متضمنةالأخطاء وطريقة تصحيحها
"""

if submit1:
    if st.session_state.resume is not None:
        pdf_content = input_pdf_setup(st.session_state.resume)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
     #   st.subheader("يتم الآن تحليل المعلومات...")
        st.write(response)
    else:
        st.write("من فضلك قم برفع سيرتك الذاتية لتحليلها")

elif submit2:
    if st.session_state.resume is not None:
        pdf_content = input_pdf_setup(st.session_state.resume)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
    #    st.subheader("يتم الآن تحليل المعلومات...")
        st.write(response)
    else:
        st.write("من فضلك قم برفع سيرتك الذاتية لتحليلها")
        