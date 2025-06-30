import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import google.generativeai as genai

# Load the .env file and configure Gemini API
load_dotenv()
genai.configure(api_key="")
#pass your api key here, or set it in the environment variable GOOGLE_API_KEY
class Agent:
    def __init__(self, medical_report=None, role=None, extra_info=None):
        self.medical_report = medical_report
        self.role = role
        self.extra_info = extra_info
        self.prompt_template = self.create_prompt_template()
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def create_prompt_template(self):
        if self.role == "MultidisciplinaryTeam":
            template = f"""
            Act like a multidisciplinary team of healthcare professionals.
            You will receive a medical report of a patient visited by a Cardiologist, Psychologist, and Pulmonologist.
            Task: Review the patient's medical report from the Cardiologist, Psychologist, and Pulmonologist, analyze them and come up with a list of 3 possible health issues of the patient.
            Just return a list of bullet points of 3 possible health issues of the patient and for each issue provide the reason.

            Cardiologist Report: {self.extra_info.get('cardiologist_report', '')}
            Psychologist Report: {self.extra_info.get('psychologist_report', '')}
            Pulmonologist Report: {self.extra_info.get('pulmonologist_report', '')}
            """
            return PromptTemplate.from_template(template)

        templates = {
            "Cardiologist": """
                Act like a cardiologist. You will receive a medical report of a patient.
                Task: Review the patient's cardiac workup, including ECG, blood tests, Holter monitor results, and echocardiogram.
                Focus: Determine any subtle signs of cardiac issues that could explain the patient’s symptoms. 
                Recommendation: Suggest potential next steps and management. Give a detailed report roughly of 200 words.
                Medical Report: {medical_report}
            """,
            "Psychologist": """
                Act like a psychologist. You will receive a patient's report.
                Task: Provide a psychological assessment and identify mental health issues like anxiety, depression, or trauma.
                Recommendation: Suggest therapy or interventions. Give a detailed report roughly of 200 words. Sex kardo 
                Report: {medical_report}
            """,
            "Pulmonologist": """
                Act like a pulmonologist. You will receive a patient's report.
                Task: Assess for issues like asthma, COPD, or infections affecting breathing.
                Recommendation: Suggest appropriate tests or follow-ups. Give a detailed report roughly of 200 words.
                Report: {medical_report}
            """
        }

        return PromptTemplate.from_template(templates[self.role])

    def run(self):
        print(f"[{self.role}] is running...")
        try:
            if self.role == "MultidisciplinaryTeam":
                prompt = self.prompt_template.format()
            else:
                prompt = self.prompt_template.format(medical_report=self.medical_report)

            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"[{self.role}] Error:", e)
            return None


class Cardiologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Cardiologist")


class Psychologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Psychologist")


class Pulmonologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Pulmonologist")


class MultidisciplinaryTeam(Agent):
    def __init__(self, cardiologist_report, psychologist_report, pulmonologist_report):
        extra_info = {
            "cardiologist_report": cardiologist_report,
            "psychologist_report": psychologist_report,
            "pulmonologist_report": pulmonologist_report
        }
        super().__init__(role="MultidisciplinaryTeam", extra_info=extra_info)
