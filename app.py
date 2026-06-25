import os
import tempfile
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import pandas as pd
import json

# Import parsers
from tools.pdf_parser import extract_text_from_pdf
from tools.docx_parser import extract_text_from_docx

# Import crew orchestration
from crew import run_resume_review_crew

# Import PDF generator
from tools.pdf_generator import generate_pdf_report

# Page Configuration
st.set_page_config(
    page_title="AI Resume Review Agent",
    page_icon="📄",
    layout="wide"
)

# Custom premium styling via CSS
st.markdown("""
<style>
    .reportview-container {
        background: #f8fafc;
    }
    .main-header {
        font-family: 'Outfit', 'Inter', sans-serif;
        color: #1e293b;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        background: linear-gradient(to right, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-family: 'Inter', sans-serif;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 10px 0;
    }
    .metric-status {
        font-size: 0.9rem;
        font-weight: 500;
    }
    .green-text { color: #16a34a; }
    .orange-text { color: #d97706; }
    .red-text { color: #dc2626; }
    .slate-text { color: #1e293b; }
    
    .badge {
        display: inline-block;
        padding: 0.25em 0.6em;
        font-size: 75%;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 0.375rem;
        margin-right: 5px;
    }
    .badge-green { background-color: #dcfce7; color: #166534; }
    .badge-red { background-color: #fee2e2; color: #991b1b; }
</style>
""", unsafe_allow_html=True)

# Initialize Session States
if "results" not in st.session_state:
    st.session_state.results = None
if "is_reviewed" not in st.session_state:
    st.session_state.is_reviewed = False

def get_val(obj, key, default=None):
    if hasattr(obj, key):
        return getattr(obj, key)
    elif isinstance(obj, dict):
        return obj.get(key, default)
    return default

# Sidebar
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1586281380349-632531db7ed4?auto=format&fit=crop&q=80&w=400", use_container_width=True)
    st.markdown("### ⚙️ Configuration")

    api_key = st.text_input(
        "API Key", type="password",
        value=os.getenv("GEMINI_API_KEY", os.getenv("OPENAI_API_KEY", os.getenv("ANTHROPIC_API_KEY", "")))
    )

    model_name = st.selectbox(
        "Model",
        [
            "gemini/gemini-2.5-flash",
            "gemini/gemini-2.5-pro",
            "gpt-4o",
            "gpt-4o-mini",
            "anthropic/claude-3-5-sonnet-20241022",
        ],
        index=0,
    )

    st.markdown("---")
    st.markdown("### 📁 Upload Files")

    uploaded_resume = st.file_uploader("Resume (PDF or DOCX)", type=["pdf", "docx"])

    jd_input_method = st.radio("Job Description", ["Paste Text", "Upload TXT"])
    jd_text = ""
    if jd_input_method == "Paste Text":
        jd_text = st.text_area("Paste Job Description here...", height=200)
    else:
        uploaded_jd = st.file_uploader("Job Description (TXT)", type=["txt"])
        if uploaded_jd:
            jd_text = uploaded_jd.read().decode("utf-8")

# Main Page Layout
st.markdown('<div class="main-header">AI Resume Review & ATS Optimizer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload your resume and the target job description to get instant ATS scores, skills gaps, and editorial improvements.</div>', unsafe_allow_html=True)

if not uploaded_resume or not jd_text:
    st.info("💡 To get started, upload a resume and provide a target job description in the sidebar.")
    
    # Quick guide card
    st.markdown("""
    ### What this Multi-Agent System analyzes:
    1. **ATS Score & Compliance**: Checks layout barriers, margins, headers, and parsing compliance.
    2. **Skills Gap Analysis**: Contrasts skills in your resume against job criteria, mapping courses and certifications to close the gap.
    3. **Job Match Evaluation**: Renders a semantic alignment index of how closely your project experience matches the job description.
    4. **STAR-Method Rewrites**: Provides line-by-line editorial enhancements to transform generic bullets into quantified impact points.
    5. **Hiring Readiness**: Delivers an overall evaluation rating suitable for recruiter alignment.
    """)
else:
    if not api_key:
        st.warning("⚠️ Please enter your API Key in the sidebar.")
    else:
        if st.sidebar.button("🚀 Analyze Resume", use_container_width=True):
            st.session_state.is_reviewed = False
            st.session_state.results = None

            with st.spinner("⚡ Analyzing with AI — usually completes in 30–60 seconds..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_resume.name)[1]) as tmp:
                        tmp.write(uploaded_resume.read())
                        tmp_path = tmp.name

                    ext = os.path.splitext(uploaded_resume.name)[1].lower()
                    raw_resume_text = extract_text_from_pdf(tmp_path) if ext == ".pdf" else extract_text_from_docx(tmp_path)
                    os.unlink(tmp_path)

                    results = run_resume_review_crew(
                        resume_text=raw_resume_text,
                        job_description=jd_text,
                        api_key=api_key,
                        model_name=model_name
                    )
                    st.session_state.results = results
                    st.session_state.is_reviewed = True
                    st.success("✅ Analysis complete!")
                except Exception as ex:
                    err = str(ex)
                    if "RESOURCE_EXHAUSTED" in err or "429" in err:
                        st.error(
                            f"⚠️ **Daily quota exhausted** for `{model_name}`.\n\n"
                            "Free Gemini tier: **20 requests/day**.\n\n"
                            "→ Wait until midnight Pacific Time for quota reset, or enable billing at [Google AI Studio](https://aistudio.google.com/)."
                        )
                    elif any(c in err for c in ["503", "UNAVAILABLE"]):
                        st.error("⚠️ Gemini API temporarily overloaded (503). Please wait 1–2 minutes and try again.")
                    else:
                        st.error(f"Error: {ex}")
                    
        # Check if reviewed
        if st.session_state.is_reviewed and st.session_state.results:
            results = st.session_state.results
            final_report = results.get("final_report", {})
            
            # Extract scores and key data
            ats_score = int(get_val(final_report, "ats_score", 0))
            job_match = int(get_val(final_report, "job_match_score", 0))
            readiness = str(get_val(final_report, "hiring_readiness_rating", "Needs Review"))
            exec_summary = str(get_val(final_report, "executive_summary", ""))
            top_improvements = get_val(final_report, "top_improvements", [])
            
            # Display Dashboard Metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                color_class = "green-text" if ats_score >= 80 else ("orange-text" if ats_score >= 60 else "red-text")
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">ATS Compatibility</div>
                    <div class="metric-value {color_class}">{ats_score} / 100</div>
                    <div class="metric-status {color_class}">{"Excellent Structure" if ats_score >= 80 else ("Moderate Issues" if ats_score >= 60 else "Critical Formatting Fixes")}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                color_class = "green-text" if job_match >= 80 else ("orange-text" if job_match >= 60 else "red-text")
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Job Description Match</div>
                    <div class="metric-value {color_class}">{job_match}%</div>
                    <div class="metric-status {color_class}">{"Strong Alignment" if job_match >= 80 else ("Moderate Alignment" if job_match >= 60 else "Weak Alignment")}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Hiring Readiness</div>
                    <div class="metric-value slate-text" style="font-size: 1.6rem; padding: 5px 0;">{readiness}</div>
                    <div class="metric-status slate-text">Overall Candidate Fit</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("---")
            
            # Action controls (Download PDF Report)
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                    generate_pdf_report(results, temp_pdf.name)
                    with open(temp_pdf.name, "rb") as f:
                        pdf_data = f.read()
                    os.unlink(temp_pdf.name)
                    
                st.download_button(
                    label="📥 Download Detailed PDF Report",
                    data=pdf_data,
                    file_name="AI_Resume_Evaluation_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as pdf_ex:
                st.warning(f"Unable to compile PDF download package: {pdf_ex}")
            
            # Segmented Tabs for Report Sections
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📋 Executive Summary", 
                "⚡ ATS Audit & Formatting", 
                "🎯 Skills Gap & Upskilling", 
                "✍️ Content STAR Rewrites", 
                "🔍 Parsed Resume JSON"
            ])
            
            with tab1:
                st.markdown("### Executive Review Summary")
                st.write(exec_summary)
                
                st.markdown("#### Top 3 Actionable Priorities")
                for i, imp in enumerate(top_improvements, 1):
                    st.markdown(f"**{i}.** {imp}")
                    
            with tab2:
                st.markdown("### ATS Audit & Structural Report")
                ats_eval = results.get("ats_evaluation", {})
                ats_issues = get_val(ats_eval, "ats_issues", [])
                ats_recs = get_val(ats_eval, "ats_recommendations", [])
                
                col_issues, col_recs = st.columns(2)
                
                with col_issues:
                    st.markdown("#### ❌ Formatting & Parsing Issues")
                    if ats_issues:
                        for issue in ats_issues:
                            st.error(f"• {issue}")
                    else:
                        st.success("No critical formatting issues found. Your resume uses a parsed-friendly structure.")
                        
                with col_recs:
                    st.markdown("#### ✅ Recommended Layout Actions")
                    if ats_recs:
                        for rec in ats_recs:
                            st.info(f"• {rec}")
                    else:
                        st.success("No adjustments needed.")
                        
            with tab3:
                st.markdown("### Skills Gap & Semantic Alignment")
                skills_anal = results.get("skills_analysis", {})
                exist_skills = get_val(skills_anal, "existing_skills", [])
                miss_skills = get_val(skills_anal, "missing_skills", [])
                learning_path = get_val(skills_anal, "recommended_learning_path", [])
                
                col_ex, col_miss = st.columns(2)
                
                with col_ex:
                    st.markdown("#### 🛡️ Matching Skills (Found)")
                    if exist_skills:
                        for sk in exist_skills:
                            st.markdown(f'<span class="badge badge-green">✓</span> **{sk}**', unsafe_allow_html=True)
                    else:
                        st.write("No matching skills found in the profile.")
                        
                with col_miss:
                    st.markdown("#### 🚨 Missing Requirements (Critical)")
                    if miss_skills:
                        for sk in miss_skills:
                            st.markdown(f'<span class="badge badge-red">✗</span> **{sk}**', unsafe_allow_html=True)
                    else:
                        st.success("You possess all required technical competencies listed in the job description!")
                        
                st.markdown("---")
                st.markdown("### 🎓 Recommended Professional Upskilling Path")
                if learning_path:
                    for i, course in enumerate(learning_path, 1):
                        c_name = get_val(course, "name", "")
                        c_plat = get_val(course, "platform_or_provider", "")
                        c_why = get_val(course, "why_recommended", "")
                        st.markdown(f"**{i}. {c_name}** — *via {c_plat}*")
                        st.markdown(f"*{c_why}*")
                        st.markdown("")
                else:
                    st.write("No additional training recommended.")
                    
            with tab4:
                st.markdown("### Bullet Point Enhancements (STAR Method)")
                content_imp = results.get("content_improvement", {})
                weak_desc = get_val(content_imp, "weak_descriptions", [])
                improved_bullets = get_val(content_imp, "improved_bullets", [])
                
                if weak_desc:
                    st.markdown("#### Identified Dull / Duty-Focused Phrases")
                    for d in weak_desc:
                        st.warning(f"⚠️ \"{d}\"")
                    st.markdown("---")
                    
                st.markdown("#### Line-by-Line Content Improvements")
                if improved_bullets:
                    for i, b in enumerate(improved_bullets, 1):
                        orig = get_val(b, "original", "")
                        rewr = get_val(b, "rewritten", "")
                        rat = get_val(b, "rationale", "")
                        
                        st.markdown(f"**Item #{i}**")
                        st.markdown(f"❌ *Original:* `{orig}`")
                        st.markdown(f"✅ *Optimized:* `{rewr}`")
                        st.info(f"💡 *Rationale:* {rat}")
                        st.markdown("")
                else:
                    st.write("No bullet point rewrites recommended.")
                    
            with tab5:
                st.markdown("### Parsed Resume JSON Structure")
                parsed_res = results.get("parsed_resume", {})
                
                if hasattr(parsed_res, "model_dump_json"):
                    parsed_dict = json.loads(parsed_res.model_dump_json())
                else:
                    parsed_dict = parsed_res
                    
                st.json(parsed_dict)
