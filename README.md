# 🧠 AI Health Assist – Agentic AI for Multidisciplinary Medical Diagnostics

<img width="900" alt="AI Health Assist Demo" src="img/schema.jpg">

**AI Health Assist** is an agentic AI-powered system that simulates a multidisciplinary team of medical specialists. This Python project leverages large language models (LLMs) such as GPT-4o or Gemini to create domain-specific AI agents—each offering expert-level assessments and personalized suggestions. The collaborative intelligence of these agents demonstrates how AI can augment clinical decision-making across cardiology, psychology, and pulmonology.

---

## 🚀 Project Overview

- **Parallel Agent Analysis:** Three autonomous AI agents (Cardiologist, Psychologist, Pulmonologist) analyze a shared medical report in parallel using Python threading.
- **Specialist Reasoning:** Each agent applies role-specific prompt engineering to deliver unique, field-specific insights.
- **Central Summarizer:** A final LLM-based agent synthesizes all findings, highlighting three key health issues and actionable recommendations.
- **Structured Output:** Results are saved in a user-friendly, structured format for easy review.

---

## 🧩 Active AI Agents

- **🫀 Cardiologist Agent:** Evaluates cardiac health, recommends further tests, and suggests heart-focused strategies.
- **🧘 Psychologist Agent:** Identifies psychological contributors, suggests therapy and behavioral strategies.
- **🌬️ Pulmonologist Agent:** Examines respiratory factors, advises on pulmonary testing and breathing interventions.

---

## 🛠️ Tech Stack & Workflow

- **LLM:** OpenAI GPT-4o or Gemini (Google Generative AI)
- **Concurrency:** Python `threading` for parallel agent execution
- **Prompt Engineering:** Role-specific prompts for each agent
- **PDF & OCR:** Automated extraction of medical report data
- **Summarization:** Aggregation and deduplication of agent findings

---

## 📁 File & Directory Structure

AI-Health-Assist/
├── app.py
├── main.py
├── apikey.env
├── requirements.txt
├── uploads/
├── results/
├── quick_test.py
├── setup.py
├── prettify_reports.py
├── Utils/
│   ├── Agents.py
│   └── PDFProcessor.py
├── Medical Reports/
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── components/
    │   ├── upload_section.html
    │   ├── analysis_grid.html
    │   ├── history_section.html
    │   └── report_modal.html
    └── includes/
        ├── head.html
        ├── header.html
        └── floating_stats.html

static/
├── css/
│   ├── main.css
│   ├── components.css
│   └── modal.css
└── js/
    ├── dashboard.js
    ├── analysis.js
    ├── history.js
    └── modal.js

---

## ⚡ How to Run the Project

1. **Install Python dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

2. **Install system dependencies:**
   - **Windows:**  
     - [Install Tesseract OCR](https://github.com/tesseract-ocr/tesseract/wiki)
     - [Install Poppler](https://github.com/oschwartz10612/poppler-windows/releases/)
     - Add both to your PATH.
   - **Ubuntu:**  
     ```sh
     sudo apt-get install tesseract-ocr poppler-utils
     ```

3. **Add your API key:**  
   - Place your OpenAI or Gemini API key in `apikey.env` as:
     ```
     OPENAI_API_KEY=your_key_here
     ```
     or
     ```
     GOOGLE_API_KEY=your_key_here
     ```

4. **Run the main script:**
   ```sh
   python main.py --file "Medical Reports/your_report.pdf"
   ```

5. **(Optional) Launch the dashboard:**
   ```sh
   python app.py
   ```
   Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## 👨‍⚕️ Target Use Cases

- Early-stage symptom screening
- Clinical decision support for general physicians
- AI-assisted telemedicine consultations
- Rural/remote health diagnostics where multi-specialty advice isn’t available

---

## 🔮 Future Roadmap

- Expand agent pool (neurology, endocrinology, etc.)
- Integrate OpenAI Assistant API for dynamic parsing and tool use
- Advanced multimodal input (PDFs, lab charts, x-rays)
- Patient-facing conversational interface

---

## 🧪 Disclaimer

This tool is for **educational and experimental use only**. It does **not replace professional medical advice** or diagnosis. Always consult a licensed medical practitioner.

