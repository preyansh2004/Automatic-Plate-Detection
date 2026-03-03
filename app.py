import streamlit as st
import subprocess
import shutil
import os

st.set_page_config(
    page_title="PlateDetect - Automatic Number Plate Recognition",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove default padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }
    
    /* Light gradient background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #eff6ff 0%, #e0e7ff 50%, #f3e8ff 100%);
        min-height: 100vh;
    }
    
    [data-testid="stAppViewContainer"] > .main {
        background: transparent;
    }
    
    /* FIX: Prevent content from fading during processing */
    .stApp [data-testid="stAppViewContainer"] {
        opacity: 1 !important;
    }
    
    section[data-testid="stSidebar"] ~ [data-testid="stVerticalBlock"] {
        opacity: 1 !important;
    }
    
    [data-testid="stVerticalBlock"] {
        opacity: 1 !important;
    }
    
    /* HOME PAGE */
    .home-hero {
        padding: 60px 5% 40px;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .main-title {
        font-size: 5rem;
        font-weight: 900;
        color: #1e293b;
        margin-bottom: 20px;
        letter-spacing: -2px;
        line-height: 1;
    }
    
    .main-subtitle {
        font-size: 1.8rem;
        font-weight: 600;
        color: #64748b;
        margin-bottom: 25px;
        line-height: 1.3;
    }
    
    .main-description {
        font-size: 1.15rem;
        color: #94a3b8;
        line-height: 1.8;
        margin-bottom: 40px;
        max-width: 580px;
    }
    
    .illustration-image {
        width: 100%;
        max-width: 650px;
        height: auto;
        border-radius: 24px;
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.15);
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    
    /* How It Works Section */
    .how-it-works {
        background: white;
        border-radius: 24px;
        padding: 60px 50px;
        margin: 60px auto 50px;
        max-width: 1400px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
    }
    
    .section-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 900;
        color: #1e293b;
        margin-bottom: 50px;
    }
    
    .steps-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 40px;
    }
    
    .step-item {
        text-align: center;
        padding: 30px 20px;
    }
    
    .step-number {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        font-size: 2rem;
        font-weight: 900;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 25px;
    }
    
    .step-title {
        font-size: 1.3rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 15px;
    }
    
    .step-desc {
        font-size: 1rem;
        color: #64748b;
        line-height: 1.7;
    }
    
    /* Use Cases */
    .use-cases {
        max-width: 1400px;
        margin: 0 auto 60px;
        padding: 0 5%;
    }
    
    .use-case-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 20px;
        padding: 40px 30px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        height: 100%;
    }
    
    .use-case-card:hover {
        border-color: #6366f1;
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(99, 102, 241, 0.2);
    }
    
    .use-case-icon {
        font-size: 3.5rem;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .use-case-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 15px;
        text-align: center;
    }
    
    .use-case-desc {
        font-size: 1rem;
        color: #64748b;
        line-height: 1.7;
        text-align: center;
    }
    
    /* CTA Section */
    .cta-section {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 24px;
        padding: 60px 50px;
        margin: 60px auto 60px;
        max-width: 1400px;
        text-align: center;
        box-shadow: 0 20px 60px rgba(99, 102, 241, 0.3);
    }
    
    .cta-title {
        font-size: 2.5rem;
        font-weight: 900;
        color: white;
        margin-bottom: 20px;
    }
    
    .cta-subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 0px;
    }
    
    /* Buttons */
    .stButton {
        display: flex;
        justify-content: center;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px;
        padding: 18px 50px !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
        width: auto !important;
        min-width: 200px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(99, 102, 241, 0.4) !important;
        color: white !important;
    }
    
    /* FIX: Make Download and Process Another Video buttons same size */
    .stDownloadButton > button {
        background: white !important;
        color: #6366f1 !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 14px;
        padding: 18px 50px !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        width: 100% !important;
        min-width: 220px !important;
    }
    
    .stDownloadButton > button:hover {
        border-color: #6366f1 !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3) !important;
    }
    
    /* UPLOAD PAGE */
    .upload-page-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 900;
        color: #1e293b;
        margin: 40px 0 20px;
    }
    
    .upload-page-subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #64748b;
        margin-bottom: 50px;
    }
    
    .back-button button {
        background: white !important;
        color: #64748b !important;
        border: 2px solid #e2e8f0 !important;
        padding: 12px 28px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        width: auto !important;
        margin-bottom: 30px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    }
    
    .back-button button:hover {
        border-color: #6366f1 !important;
        color: #6366f1 !important;
        transform: translateX(-5px) !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2) !important;
    }
    
    [data-testid="stFileUploader"] {
        background: white;
        border: 3px dashed #cbd5e0;
        border-radius: 20px;
        padding: 50px;
        transition: all 0.3s ease;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
        margin-bottom: 60px;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #6366f1;
        background: linear-gradient(135deg, #f0f4ff 0%, #e8eeff 100%);
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(99, 102, 241, 0.15);
    }
    
    [data-testid="stFileUploader"] label {
        color: #1e293b !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }
    
    .features-section-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 900;
        color: #1e293b;
        margin: 20px 0 50px;
    }
    
    .feature-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 24px;
        padding: 45px 35px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .feature-card:hover {
        border-color: #6366f1;
        transform: translateY(-10px);
        box-shadow: 0 20px 50px rgba(99, 102, 241, 0.2);
    }
    
    .feature-icon {
        font-size: 4rem;
        margin-bottom: 25px;
        display: inline-block;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover .feature-icon {
        transform: scale(1.15) rotate(5deg);
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 18px;
    }
    
    .feature-desc {
        font-size: 1.05rem;
        color: #64748b;
        line-height: 1.7;
        margin-bottom: 25px;
        flex-grow: 1;
    }
    
    .tech-badge {
        display: inline-block;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 8px 18px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        border-radius: 10px;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 5px solid #10b981;
        border-radius: 14px;
        color: #065f46 !important;
        font-weight: 600;
        padding: 1.2rem;
    }
    
    .stError {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border-left: 5px solid #ef4444;
        border-radius: 14px;
        color: #991b1b !important;
        padding: 1.2rem;
    }
    
    video {
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        border: 3px solid #e2e8f0;
    }
    
    h3 {
        color: #1e293b !important;
        font-weight: 800;
        font-size: 2rem;
        text-align: center;
        margin: 40px 0 30px;
    }
    
    @media (max-width: 968px) {
        .main-title { font-size: 3rem; }
        .steps-grid { grid-template-columns: 1fr; }
    }
    
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

if 'show_welcome' not in st.session_state:
    st.session_state.show_welcome = True
if 'processed' not in st.session_state:
    st.session_state.processed = False

if st.session_state.show_welcome:
    st.markdown('<div class="home-hero">', unsafe_allow_html=True)
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        st.markdown("""
        <div class="main-title">PlateDetect</div>
        <div class="main-subtitle">Automatic Number Plate Recognition</div>
        <div class="main-description">
            Upload your video footage and let our AI-powered system automatically detect and recognize license plates with advanced computer vision technology.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Detection"):
            st.session_state.show_welcome = False
            st.rerun()
    
    with col_right:
        st.markdown("""
        <img src="https://f5b623aa.delivery.rocketcdn.me/wp-content/uploads/2022/08/Blog_Automatic-Number-Plate-Recognition-ANPR.jpg" 
             class="illustration-image" 
             alt="ANPR Illustration">
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="how-it-works">
        <div class="section-title">How It Works</div>
        <div class="steps-grid">
            <div class="step-item">
                <div class="step-number">1</div>
                <div class="step-title">Upload Video</div>
                <div class="step-desc">Select and upload your video file containing vehicles with license plates</div>
            </div>
            <div class="step-item">
                <div class="step-number">2</div>
                <div class="step-title">AI Processing</div>
                <div class="step-desc">Our system detects vehicles and extracts license plate information using YOLO and OCR</div>
            </div>
            <div class="step-item">
                <div class="step-number">3</div>
                <div class="step-title">Get Results</div>
                <div class="step-desc">Download annotated video with detected plates highlighted and recognized text</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="use-cases"><div class="section-title">Use Cases</div></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div class="use-case-card">
            <div class="use-case-icon">🅿️</div>
            <div class="use-case-title">Parking Management</div>
            <div class="use-case-desc">Automate entry/exit tracking and payment systems in parking facilities</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="use-case-card">
            <div class="use-case-icon">🚦</div>
            <div class="use-case-title">Traffic Monitoring</div>
            <div class="use-case-desc">Monitor traffic flow, detect violations, and analyze vehicle patterns</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="use-case-card">
            <div class="use-case-icon">🔒</div>
            <div class="use-case-title">Security Systems</div>
            <div class="use-case-desc">Enhance security with automated vehicle identification and access control</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cta-section">
        <div class="cta-title">Ready to Try?</div>
        <div class="cta-subtitle">Upload your video and see the results in action</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

else:
    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    if st.button("← Back to Home"):
        st.session_state.show_welcome = True
        st.session_state.processed = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="upload-page-title">Upload Your Video</div>
    <div class="upload-page-subtitle">Select a video file to begin automatic number plate detection</div>
    """, unsafe_allow_html=True)
    
    def cleanup():
        st.session_state.processed = False
        st.rerun()
    
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        target_name = 'sample.mp4'
        
        if not os.path.exists(target_name):
            if os.path.exists(target_name):
                shutil.move(target_name, f"{target_name}.bak")
            with open(target_name, "wb") as f:
                f.write(uploaded_file.getbuffer())
        
        st.success("✅ Video uploaded successfully! Ready to process.")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Start Detection"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.text("🔍 Running Detection...")
                    subprocess.run(["python", "-u", "main.py"], check=True)
                    progress_bar.progress(33)
                    
                    status_text.text("📊 Interpolating Data...")
                    subprocess.run(["python", "-u", "add_missing_data.py"], check=True)
                    progress_bar.progress(66)
                    
                    status_text.text("🎬 Generating Output Video...")
                    subprocess.run(["python", "-u", "visualize.py"], check=True)
                    
                    st.session_state.processed = True
                    progress_bar.progress(100)
                    status_text.success("✅ Processing complete!")
                    st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    st.markdown('<div class="features-section-title">Why Choose PlateDetect?</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">High Accuracy</div>
            <div class="feature-desc">State-of-the-art YOLO object detection combined with advanced OCR technology for precise license plate recognition</div>
            <div class="tech-badge">YOLO v8</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Fast Processing</div>
            <div class="feature-desc">Optimized processing pipeline with GPU acceleration delivers quick results without compromising quality</div>
            <div class="tech-badge">GPU Accelerated</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎨</div>
            <div class="feature-title">Visual Output</div>
            <div class="feature-desc">Get beautifully annotated videos with highlighted plates, bounding boxes, and text overlay in real-time</div>
            <div class="tech-badge">HD Quality</div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.processed:
        st.markdown("---")
        st.markdown("### 🎥 Result Video")
        
        if os.path.exists("out.mp4"):
            st.video("out.mp4")
            
            col1, col2 = st.columns(2, gap="large")
            with col1:
                with open("out.mp4", "rb") as file:
                    st.download_button(
                        label="⬇️ Download Video",
                        data=file,
                        file_name="detected_license_plates.mp4",
                        mime="video/mp4"
                    )
            with col2:
                if st.button("🔄 Process Another Video"):
                    cleanup()
    
    st.markdown("<br><br>", unsafe_allow_html=True)