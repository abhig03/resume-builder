# 📝 AI ATS-Friendly Resume Builder & LaTeX Engine

An AI-powered application designed to create highly optimized, single-column, ATS-friendly resumes tailored directly to target Job Descriptions. Built with Python, Streamlit, and the current **Google Gen AI SDK (`gemini-3.8-flash`)**, this tool outputs structural source code ready for pristine compilation.

It features a custom LaTeX generation engine calibrated to produce the classic corporate resume design: clean section underlines (`\hrule`) and right-aligned timelines using perfect spacing constraints.

---

## 🌐 Live Application

🚀 **The project is officially hosted and live!** You can use the web interface directly without any local installation here:

👉 [Deploy to Streamlit]()

---

## ✨ Features

- **Dual-Engine Output:** Generate resumes in standard, readable **Markdown** or professional, compilable **LaTeX**.
- **Rigorous ATS Optimization:** Automatically embeds highly relevant keywords, technical tools, and core competencies from target job listings into your text metrics without "keyword stuffing".
- **Structured Design Template Alignment:** The LaTeX generation engine forces a high-end single-column layout:
  - Large bold centered name header with clean parameter separation.
  - Bold section titles separated by full-width horizontal divider lines (`\hrule`).
  - Strict entry alignment: Company/Institution on the left, Dates right-aligned via `\hfill`.
- **Pure-Text Architecture:** Completely eliminates complex multi-column blocks, colored boxes, graphic icons, and visual elements that trip up Applicant Tracking Systems.
- **Direct Download Hooks:** One-click download buttons for raw `.tex` and `.md` source files.

---

## 🚀 Local Getting Started (Optional)

### 1. Prerequisites
Ensure you have the following installed on your local system:
- Python 3.10 or higher
- Git

### 2. Installation & Setup

Clone the repository to your local machine:
```bash
git clone https://github.com
cd your-repo-name
```

Create a virtual environment and activate it:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install the required Python modules:
```bash
pip install -r requirements.txt
```

### 3. Configuration

Create a `.streamlit` directory in the root of your project folder and add a `secrets.toml` file inside it to securely declare your local credentials:

```toml
# .streamlit/secrets.toml
GOOGLE_API_KEY = "your_actual_gemini_api_key_here"
```

### 4. Running the Application Locally

Launch the Streamlit web server:
```bash
streamlit run resume_builder.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## 🛠️ Project Structure

```text
├── .streamlit/
│   └── secrets.toml     # Local app credentials storage (Excluded from Git)
├── resume_builder.py    # Core Streamlit app containing UI & Gen AI logic
├── requirements.txt     # Python system module package list
├── .gitignore           # Safeguards local tokens from public commits
└── README.md            # Comprehensive project documentation
```

---

## 📋 How to Compile the LaTeX Output into a PDF

Because compiling LaTeX locally requires massive compiler software packages (like MacTeX or MiKTeX), we highly recommend using a free cloud compiler for a perfect zero-setup experience:

1. Generate your resume within the application choosing **LaTeX Code**.
2. Click **Download .tex File** or copy the source code out of the application text block.
3. Open a free account on **[Overleaf (overleaf.com)](https://overleaf.com)**.
4. Create a new "Blank Project".
5. Delete the default placeholder text inside the `main.tex` editor pane, paste your generated AI code, and click **Recompile**.
6. Download your high-quality, ATS-compliant vector PDF!

---

## 🌐 Production Cloud Architecture

This repository is continuously deployed to **Streamlit Community Cloud**:
- **Secrets Isolation:** The local `.streamlit/secrets.toml` file is explicitly ignored using `.gitignore`. In production, the key **`GOOGLE_API_KEY`** is safely injected via the cloud hosting dashboard's Environment Secrets setting panel.
- **Zero Heavy Binaries:** Because text metrics are captured natively through input elements instead of visual page rendering, this tool operates without requiring complex external server dependencies like `poppler-utils` or `wkhtmltopdf`.

