import os
import streamlit as st
from google import genai
from st_copy import copy_button


# Configuration & Initialization
model_id = 'gemini-3.8-flash'

# Safe API Key Loader
api_key = None
if hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("🔑 Google API Key not found! Please set GOOGLE_API_KEY in your local environment, secrets.toml, or Streamlit secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

def generate_ats_resume(job_description, candidate_info, output_format):
    """Sends the data payload to Gemini to generate either Markdown or LaTeX source code."""
    
    if output_format == "LaTeX":
        format_instruction = """
        Format the response strictly as a single, compilable LaTeX document block using the article class. 
        Do NOT wrap the response in markdown code blocks like ```latex ... ```. Start directly with \\documentclass[11pt,a4paper]{article}.
        
        CRITICAL LAYOUT RULES (Follow the format of the provided template exactly):
        1. Page Layout: Use 0.5-inch to 0.75-inch margins via \\usepackage[margin=0.5in]{geometry}. Include \\usepackage{hyperref} and \\usepackage{enumitem} (for tight bullet lists).
        
        2. Centered Header: 
           - The Name must be large, bold, and centered at the very top: \\begin{center} \\Huge \\textbf{Candidate Name} \\\\ \\end{center}
           - Subheader: Contact parameters must be centered directly underneath using small symbols or spacing, e.g., 
             \\small Phone | Email | LinkedIn | GitHub
        
        3. Underlined Sections: Every major section (Education, Experience, Projects, Technical Skills, Extra Curricular) must feature a bold title with a full horizontal rule immediately beneath it:
           \\section*{Education}
           \\hrule
           \\vspace{0.5em}
           
        4. Alignment Architecture for Entries (Crucial for Experience & Education):
           Every job or education entry must use an exact layout structure that right-aligns dates and locations perfectly:
           
           \\noindent \\textbf{Company or Institution Name} \\hfill \\textbf{Start Date -- End Date} \\\\
           \\noindent \\textit{Job Title or Degree Program} (e.g., Bachelor of Technology) \\hfill \\textit{Location (City, State)}
           
           Follow this immediately with a tight bullet list for descriptions using:
           \\begin{itemize}[noitemsep, topsep=2pt]
               \\item Achievement bullet point...
           \\end{itemize}
           
        5. Spacing & Escaping: 
           - Keep vertical space tight using small negative or positive values like \\vspace{0.3em}.
           - Ensure all layout break flags and special characters like %, &, $, _, # are properly escaped (e.g., write \\& instead of &).
        """
    else:
        format_instruction = """
        Format the response strictly in clean, standard Markdown using professional structural headers (###).
        Do NOT use tables, multi-column blocks, or custom visual elements.
        """

    system_prompt = f"""
    Role: You are an elite Executive Resume Writer and ATS Optimization Specialist.
    Task: Create a highly accurate, professional, and ATS-friendly resume tailored precisely to the provided Job Description using the Candidate's basic information.
    
    ATS Compliance Rules:
    1. Do NOT use multi-column layouts, tables, text boxes, charts, or graphic icons.
    2. Contextually integrate highly relevant keywords, tools, and technical skills found in the Job Description without "keyword stuffing".
    3. Write experience bullets using strong action verbs and quantifiable results (e.g., "Increased efficiency by 15% using X tool").
    
    {format_instruction}
    
    Ensure the document flows through: Contact Info, Professional Summary, Technical Competencies, Professional History, Key Projects, and Education.
    """

    user_payload = f"""
    TARGET JOB DESCRIPTION:
    {job_description}
    
    CANDIDATE BASIC DETAILS:
    {candidate_info}
    """

    response = client.models.generate_content(
        model=model_id,
        contents=[system_prompt, user_payload]
    )
    return response.text


# --- Streamlit UI Presentation Layout ---
st.set_page_config(page_title="AI ATS Resume Builder", layout="wide")
st.title("📝 AI ATS-Friendly Resume Builder")
st.write("Generate a tailored resume optimized to clear Applicant Tracking Systems for your target role.")

# Two-Column Data Entry Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Target Position Context")
    job_desc = st.text_area("Paste the Job Description here:", height=300, placeholder="Requirements, responsibilities, tool stacks...")

with col2:
    st.subheader("👤 Candidate Background Profile")
    name = st.text_input("Full Name")
    contact = st.text_input("Contact Info (Email, Phone, Location, LinkedIn)")
    skills = st.text_area("Core Skills & Tools:", placeholder="Python, SQL, Git, AWS...")
    experience = st.text_area("Work History Details:", height=120, placeholder="Company, Job Title, Dates worked, and responsibilities/achievements...")
    education = st.text_area("Education & Certifications:", placeholder="Degree, Major, University, Passing Year...")

# Layout configuration options
st.write("---")
st.subheader("⚙️ Output Configuration")
resume_format = st.radio("Choose your output engine format:", ("Standard Markdown", "LaTeX Code"), horizontal=True)

# Compile input parameters
candidate_data_dump = f"Name: {name}\nContact: {contact}\nRaw Skills: {skills}\nRaw Experience: {experience}\nRaw Education: {education}"

# Start Params for local generation
# import json

# with open("./test-params.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# name = data["name"]
# contact = data["contact"]
# skills = data["skills"]
# experience = data["experience"]
# education = data["education"]

# End Params for local generation


candidate_data_dump = f"Name: {name}\nContact: {contact}\nRaw Skills: {skills}\nRaw Experience: {experience}\nRaw Education: {education}"


if st.button("🚀 Build ATS-Optimized Resume", type="primary"):
    if not job_desc.strip() or not name.strip() or not experience.strip():
        st.error("Please complete the Job Description, Name, and Work History entries to populate the metrics.")
    else:
        format_type = "LaTeX" if resume_format == "LaTeX Code" else "Markdown"
        with st.spinner(f"AI is calculating alignment vectors and compiling your {format_type} code..."):
            try:
                generated_code = generate_ats_resume(job_desc, candidate_data_dump, format_type)
                st.success("🎉 Resume generated successfully!")
                
                # Dynamic Preview Presentation UI
                if format_type == "LaTeX":
                    st.subheader("🛠️ Compiled LaTeX Source Code")
                    text = st.text_area("Copy this code directly into a LaTeX compiler (like Overleaf or TeXworks) to download your PDF:", value=generated_code, height=450)
                    copy_button(
                        text,
                        tooltip="Copy text",
                        copied_label="Copied!",
                        icon="st"  # or "material_symbols"
                    )
                    # File downloader attachment hook
                    st.download_button(
                        label="📥 Download .tex File",
                        data=generated_code,
                        file_name=f"{name.replace(' ', '_')}_ATS_Resume.tex",
                        mime="text/plain"
                    )
                else:
                    st.subheader("📄 Your Generated Resume (Markdown Preview)")
                    st.markdown(generated_code)
                    
                    st.write("---")
                    st.subheader("✂️ Copy Raw Source Text")
                    text = st.text_area("Copy text snippet block:", value=generated_code, height=400)
                    copy_button(
                        text,
                        tooltip="Copy text",
                        copied_label="Copied!",
                        icon="st"  # or "material_symbols"
                   )
                    st.download_button(
                        label="📥 Download .md File",
                        data=generated_code,
                        file_name=f"{name.replace(' ', '_')}_ATS_Resume.md",
                        mime="text/plain"
                    )
            except Exception as e:
                st.error(f"An unexpected API runtime error occurred: {str(e)}")
