# ~~~~~~~~~~~~ Imports ~~~~~~~~~~~~
import os
import argparse
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from Utils.Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
from Utils.PDFProcessor import PDFProcessor

# ~~~~~~~~~~~~ Load Environment Variables ~~~~~~~~~~~~
load_dotenv('apikey.env')

def process_medical_report(file_path):
    """Process medical report from either text file or PDF"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None
    
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        print("📄 Processing PDF file...")
        pdf_processor = PDFProcessor(file_path)
        extraction_result = pdf_processor.process_pdf()
        
        if extraction_result['success']:
            medical_report = pdf_processor.format_for_agents(extraction_result)
            print("✅ PDF processed successfully")
            
            # Save extracted text for reference
            extracted_text_path = os.path.join("results", "extracted_pdf_text.txt")
            os.makedirs(os.path.dirname(extracted_text_path), exist_ok=True)
            with open(extracted_text_path, "w", encoding="utf-8") as f:
                f.write(medical_report)
            print(f"📝 Extracted text saved to: {extracted_text_path}")
            
            return medical_report
        else:
            print("❌ Failed to extract text from PDF")
            return None
            
    elif file_extension == '.txt':
        print("📝 Processing text file...")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                medical_report = file.read()
            print("✅ Text file processed successfully")
            return medical_report
        except Exception as e:
            print(f"❌ Error reading text file: {e}")
            return None
    else:
        print(f"❌ Unsupported file format: {file_extension}")
        print("Supported formats: .pdf, .txt")
        return None

def main():
    # ~~~~~~~~~~~~ Parse Command Line Arguments ~~~~~~~~~~~~
    parser = argparse.ArgumentParser(description='AI Health Assist - Medical Report Analyzer')
    parser.add_argument('--file', '-f', 
                       help='Path to medical report file (.txt or .pdf)',
                       default=os.path.join("Medical Reports", "Medical Rerort - Michael Johnson - Panic Attack Disorder.txt"))
    
    args = parser.parse_args()
    
    # ~~~~~~~~~~~~ Process Medical Report ~~~~~~~~~~~~
    medical_report = process_medical_report(args.file)
    if not medical_report:
        exit(1)
    
    print(f"\n🔍 Analyzing medical report from: {args.file}")
    
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
    print("\n🤖 Running AI agents in parallel...")
    
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_response, name, agent): name for name, agent in agents.items()}
        for future in as_completed(futures):
            agent_name, response = future.result()
            responses[agent_name] = response
            print(f"✅ {agent_name} completed analysis")

    # ~~~~~~~~~~~~ Run Multidisciplinary Team Agent ~~~~~~~~~~~~
    print("\n🏥 Running multidisciplinary team analysis...")
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
    
    # ~~~~~~~~~~~~ Save Individual Agent Reports ~~~~~~~~~~~~
    for agent_name, response in responses.items():
        agent_output_path = os.path.join("results", f"{agent_name.lower()}_report.txt")
        with open(agent_output_path, "w", encoding="utf-8") as f:
            f.write(f"### {agent_name} Report:\n\n{response}")
    
    print("📊 Individual agent reports also saved to results folder")

if __name__ == "__main__":
    main()

