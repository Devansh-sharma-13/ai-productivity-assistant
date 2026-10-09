import streamlit as st
from google import genai
import pypdf

st.set_page_config(page_title="AI Productivity Assistant", page_icon="⚡", layout="wide")

st.title("⚡ AI Productivity Assistant")
st.write("Your all-in-one AI tool for document QA, content creation, meeting notes summarization, and translation.")

# Sidebar for API Key
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.info("👈 Please enter your Gemini API Key in the sidebar to begin.")
    st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

# Feature Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📄 PDF Document Assistant", 
    "✍️ Content Creator Suite", 
    "📝 Meeting Notes & Action Items", 
    "🌐 Translator & Email Rewriter"
])

# --- TAB 1: PDF Document Assistant ---
with tab1:
    st.header("📄 PDF Document Assistant")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"], key="pdf_uploader")
    user_question = st.text_input("Ask a question about the PDF:", key="pdf_q")
    
    if st.button("Analyze PDF", key="btn_pdf"):
        if uploaded_file and user_question:
            reader = pypdf.PdfReader(uploaded_file)
            pdf_text = ""
            for page in reader.pages:
                pdf_text += page.extract_text() or ""
            
            prompt = f"Based on the following document context, answer the user's question:\n\nContext:\n{pdf_text[:8000]}\n\nQuestion: {user_question}"
            
            with st.spinner("Analyzing document..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )
                st.subheader("Answer:")
                st.write(response.text)
        else:
            st.warning("Please upload a PDF and enter a question.")

# --- TAB 2: Content Creator Suite ---
with tab2:
    st.header("✍️ Content Creator Suite")
    content_topic = st.text_input("Enter Topic/Idea:", key="content_topic")
    content_type = st.selectbox("Select Content Type:", ["LinkedIn Post", "Instagram Caption", "Twitter/X Post", "Email Draft", "Blog Outline", "Presentation Outline"])
    tone = st.selectbox("Select Tone:", ["Professional", "Casual", "Engaging", "Persuasive"])
    
    if st.button("Generate Content", key="btn_content"):
        if content_topic:
            prompt = f"Write a {tone.lower()} {content_type} about the following topic: {content_topic}. Keep it engaging and tailored for the specific format."
            with st.spinner("Generating content..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )
                st.subheader("Generated Output:")
                st.write(response.text)
        else:
            st.warning("Please enter a topic.")

# --- TAB 3: Meeting Notes & Action Items ---
with tab3:
    st.header("📝 Meeting Notes & Action Items")
    meeting_text = st.text_area("Paste Raw Meeting Notes / Transcript:", height=200, key="meeting_notes")
    
    if st.button("Summarize & Extract Action Items", key="btn_notes"):
        if meeting_text:
            prompt = f"Summarize the following meeting notes clearly with key discussions, bullet points, and a distinct list of actionable tasks/next steps:\n\n{meeting_text}"
            with st.spinner("Processing notes..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )
                st.subheader("Meeting Summary & Action Items:")
                st.write(response.text)
        else:
            st.warning("Please paste some meeting notes.")

# --- TAB 4: Translator & Email Rewriter ---
with tab4:
    st.header("🌐 Translator & Email Rewriter")
    input_text = st.text_area("Enter Text / Rough Email Draft:", height=150, key="trans_text")
    mode = st.radio("Choose Action:", ["Rewrite as Professional Email", "Translate Text"])
    target_lang = st.selectbox("Select Language (if translating):", ["Spanish", "French", "German", "Hindi", "Japanese", "Chinese"])
    
    if st.button("Process Text", key="btn_process"):
        if input_text:
            if mode == "Rewrite as Professional Email":
                prompt = f"Rewrite the following draft into a clear, professional, and polite email:\n\n{input_text}"
            else:
                prompt = f"Translate the following text into {target_lang}:\n\n{input_text}"
                
            with st.spinner("Processing..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )
                st.subheader("Result:")
                st.write(response.text)
        else:
            st.warning("Please enter text to process.")