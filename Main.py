# ~~~~~~~~~~~~ Imports ~~~~~~~~~~~~
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from Utils.Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam

# ~~~~~~~~~~~~ Load Environment Variables ~~~~~~~~~~~~
load_dotenv('apikey.env')

# ~~~~~~~~~~~~ Read Medical Report File Safely ~~~~~~~~~~~~
report_path = os.path.join("Medical Reports", "Medical Rerort - Michael Johnson - Panic Attack Disorder.txt")
try:
    with open(report_path, "r", encoding="utf-8") as file:
        medical_report = file.read()
except FileNotFoundError:
    print(f"❌ Medical report file not found at: {report_path}")
    exit(1)

# ~~~~~~~~~~~~ Initialize Specialist Agents ~~~~~~~~~~~~
agents = {
    "Cardiologist": Cardiologist(medical_report),
    "Psychologist": Psychologist(medical_report),
    "Pulmonologist": Pulmonologist(medical_report)
}

# ~~~~~~~~~~~~ Concurrent Agent Execution ~~~~~~~~~~~~
def get_response(agent_name, agent):
    try:
        return agent_name, agent.run()
    except Exception as e:
        print(f"⚠️ Error in {agent_name}: {e}")
        return agent_name, "No response."

responses = {}
with ThreadPoolExecutor() as executor:
    futures = {executor.submit(get_response, name, agent): name for name, agent in agents.items()}
    for future in as_completed(futures):
        agent_name, response = future.result()
        responses[agent_name] = response

# ~~~~~~~~~~~~ Run Multidisciplinary Team Agent ~~~~~~~~~~~~
team_agent = MultidisciplinaryTeam(
    cardiologist_report=responses.get("Cardiologist", ""),
    psychologist_report=responses.get("Psychologist", ""),
    pulmonologist_report=responses.get("Pulmonologist", "")
)

final_diagnosis = team_agent.run()
final_diagnosis_text = "### Final Diagnosis:\n\n" + (final_diagnosis or "No diagnosis returned.")

# ~~~~~~~~~~~~ Save Output to File ~~~~~~~~~~~~
output_path = os.path.join("results", "final_diagnosis.txt")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as txt_file:
    txt_file.write(final_diagnosis_text)

print(f"\n✅ Final diagnosis saved to: {output_path}")

# Run the MultidisciplinaryTeam agent to generate the final diagnosis
final_diagnosis = team_agent.run()
final_diagnosis_text = "### Final Diagnosis:\n\n" + final_diagnosis
txt_output_path = "results/final_diagnosis.txt"

# Ensure the directory exists
os.makedirs(os.path.dirname(txt_output_path), exist_ok=True)

# Write the final diagnosis to the text file
with open(txt_output_path, "w") as txt_file:
    txt_file.write(final_diagnosis_text)

print(f"Final diagnosis has been saved to {txt_output_path}")


