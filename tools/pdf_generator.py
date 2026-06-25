import os
import datetime
from fpdf import FPDF


class ResumeReviewPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_margins(15, 25, 15)
        self.alias_nb_pages()

    def header(self):
        self.set_fill_color(30, 41, 59)
        self.rect(0, 0, 210, 28, "F")
        self.set_y(8)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 5, "AI RESUME EVALUATION & ATS REPORT", 0, new_x="LMARGIN", new_y="NEXT", align="C")
        self.set_font("Helvetica", "I", 9)
        date_str = datetime.datetime.now().strftime("%B %d, %Y")
        self.cell(0, 4, f"Generated on {date_str} | Powered by CrewAI Multi-Agent System", 0, new_x="LMARGIN", new_y="NEXT", align="C")
        self.set_y(32)

    def footer(self):
        self.set_y(-15)
        self.set_text_color(100, 116, 139)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()} of {{nb}}", 0, align="C")

    def add_section_header(self, title: str):
        self.ln(4)
        self.set_fill_color(241, 245, 249)
        self.set_text_color(15, 23, 42)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, f"  {title.upper()}", 0, new_x="LMARGIN", new_y="NEXT", align="L", fill=True)
        self.ln(2)

    def safe_multi_cell(self, text: str, h: int = 5, font: str = "", size: int = 10,
                        r: int = 51, g: int = 65, b: int = 85, fill: bool = False):
        """Always resets cursor to left margin after multi_cell (fpdf2 compatibility)."""
        self.set_font("Helvetica", font, size)
        self.set_text_color(r, g, b)
        self.multi_cell(0, h, text, fill=fill, new_x="LMARGIN", new_y="NEXT")


def _get(obj, key, default=None):
    if hasattr(obj, key):
        return getattr(obj, key)
    elif isinstance(obj, dict):
        return obj.get(key, default)
    return default


def generate_pdf_report(results: dict, output_path: str):
    """
    Takes the structured CrewAI execution results and creates a styled PDF report.
    All multi_cell calls use new_x=LMARGIN, new_y=NEXT to avoid fpdf2 cursor issues.
    """
    pdf = ResumeReviewPDF()
    pdf.add_page()

    # 1. Executive Summary
    pdf.add_section_header("1. Executive Summary")
    final_report    = results.get("final_report", {})
    exec_summary    = _get(final_report, "executive_summary", "No executive summary available.")
    ats_score       = int(_get(final_report, "ats_score", 0) or 0)
    job_match_score = int(_get(final_report, "job_match_score", 0) or 0)
    readiness       = str(_get(final_report, "hiring_readiness_rating", "Needs Review"))
    top_improvements = _get(final_report, "top_improvements", [])

    pdf.safe_multi_cell(exec_summary, h=5)
    pdf.ln(2)

    # Score banner
    pdf.set_fill_color(248, 250, 252)
    banner_y = pdf.get_y()
    pdf.rect(pdf.get_x(), banner_y, 180, 22, "F")
    pdf.set_text_color(71, 85, 105)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_x(20)
    col_w = 60
    pdf.cell(col_w, 7, "ATS SCORE", 0, align="C")
    pdf.cell(col_w, 7, "JOB MATCH", 0, align="C")
    pdf.cell(col_w, 7, "HIRING READINESS", 0, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_x(20)
    pdf.set_font("Helvetica", "B", 14)
    if ats_score >= 80:
        pdf.set_text_color(22, 163, 74)
    elif ats_score >= 60:
        pdf.set_text_color(217, 119, 6)
    else:
        pdf.set_text_color(220, 38, 38)
    pdf.cell(col_w, 11, f"{ats_score} / 100", 0, align="C")
    if job_match_score >= 80:
        pdf.set_text_color(22, 163, 74)
    elif job_match_score >= 60:
        pdf.set_text_color(217, 119, 6)
    else:
        pdf.set_text_color(220, 38, 38)
    pdf.cell(col_w, 11, f"{job_match_score}% Match", 0, align="C")
    pdf.set_text_color(30, 41, 59)
    pdf.cell(col_w, 11, str(readiness), 0, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(6)

    # 2. Critical Recommendations
    pdf.add_section_header("2. Critical Recommendations")
    if top_improvements:
        for idx, imp in enumerate(top_improvements, 1):
            pdf.safe_multi_cell(f"{idx}. {imp}", h=6)
    else:
        pdf.safe_multi_cell("- None reported", h=6)
    pdf.ln(4)

    # 3. ATS Compatibility & Formatting
    pdf.add_section_header("3. ATS Compatibility & Formatting Analysis")
    ats_eval   = results.get("ats_evaluation", {})
    ats_issues = _get(ats_eval, "ats_issues", [])
    ats_recs   = _get(ats_eval, "ats_recommendations", [])

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(185, 28, 28)
    pdf.cell(0, 6, "Detected ATS Issues:", 0, new_x="LMARGIN", new_y="NEXT")
    if ats_issues:
        for issue in ats_issues:
            pdf.safe_multi_cell(f"  * {issue}", h=5, r=51, g=65, b=85)
    else:
        pdf.safe_multi_cell("  * No structural compatibility issues detected.", h=5)
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(22, 101, 52)
    pdf.cell(0, 6, "Formatting Fixes & Recommendations:", 0, new_x="LMARGIN", new_y="NEXT")
    if ats_recs:
        for rec in ats_recs:
            pdf.safe_multi_cell(f"  * {rec}", h=5, r=51, g=65, b=85)
    else:
        pdf.safe_multi_cell("  * Standard formatting looks correct.", h=5)
    pdf.ln(4)

    # 4. Skills Gap & Upskilling
    pdf.add_section_header("4. Skills Gap & Upskilling Pathway")
    skills_anal   = results.get("skills_analysis", {})
    exist_skills  = _get(skills_anal, "existing_skills", [])
    miss_skills   = _get(skills_anal, "missing_skills", [])
    learning_path = _get(skills_anal, "recommended_learning_path", [])

    col_w2 = 90
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(col_w2, 6, "Aligned / Matching Skills", 0, align="L")
    pdf.cell(col_w2, 6, "Missing Skills Detected", 0, new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(71, 85, 105)
    max_len = max(len(exist_skills), len(miss_skills)) if (exist_skills or miss_skills) else 0
    for i in range(max_len):
        c1 = exist_skills[i] if i < len(exist_skills) else ""
        c2 = miss_skills[i]  if i < len(miss_skills)  else ""
        pdf.cell(col_w2, 5, f"  + {c1}" if c1 else "", 0, align="L")
        pdf.cell(col_w2, 5, f"  - {c2}" if c2 else "", 0, new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 6, "Recommended Upskilling & Learning Resources:", 0, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    if learning_path:
        for course in learning_path:
            c_name = _get(course, "name", "")
            c_plat = _get(course, "platform_or_provider", "")
            c_why  = _get(course, "why_recommended", "")
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(30, 41, 59)
            pdf.cell(0, 5, f"  - {c_name} (via {c_plat})", 0, new_x="LMARGIN", new_y="NEXT")
            pdf.safe_multi_cell(f"    Why: {c_why}", h=4, font="I", size=9, r=100, g=116, b=139)
            pdf.ln(2)
    else:
        pdf.safe_multi_cell("  * No upskilling pathways needed.", h=5)
    pdf.ln(4)

    # 5. STAR Rewrites (new page)
    pdf.add_page()
    pdf.add_section_header("5. Content Optimization & STAR Rewrites")
    content_imp      = results.get("content_improvement", {})
    weak_desc        = _get(content_imp, "weak_descriptions", [])
    improved_bullets = _get(content_imp, "improved_bullets", [])

    if weak_desc:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 6, "Identified Weak Resume Phrases:", 0, new_x="LMARGIN", new_y="NEXT")
        for d in weak_desc:
            pdf.safe_multi_cell(f'  * "{d}"', h=5, size=9, r=71, g=85, b=105)
        pdf.ln(4)

    if improved_bullets:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 6, "Suggested STAR Bullet Point Rewrites:", 0, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        for b in improved_bullets:
            orig = _get(b, "original", "")
            rewr = _get(b, "rewritten", "")
            rat  = _get(b, "rationale", "")
            pdf.set_fill_color(254, 242, 242)
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(153, 27, 27)
            pdf.cell(0, 5, "  Original:", 0, new_x="LMARGIN", new_y="NEXT", fill=True)
            pdf.multi_cell(0, 4, f"    {orig}", fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
            pdf.set_fill_color(240, 253, 244)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(21, 128, 61)
            pdf.cell(0, 5, "  Optimized (STAR):", 0, new_x="LMARGIN", new_y="NEXT", fill=True)
            pdf.multi_cell(0, 4, f"    {rewr}", fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
            pdf.safe_multi_cell(f"    Why it works: {rat}", h=4, size=9, r=71, g=85, b=105)
            pdf.ln(4)

    # Output
    out_dir = os.path.dirname(os.path.abspath(output_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    pdf.output(output_path)
    print(f"Successfully generated PDF report at: {output_path}")


if __name__ == "__main__":
    print("PDF generator module loaded.")
