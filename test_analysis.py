#!/usr/bin/env python3
"""
Debug Test Script - Test if AI agents are working correctly
"""
import os
import sys
from dotenv import load_dotenv
from Utils.Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
from Utils.PDFProcessor import PDFProcessor

# Load environment variables
load_dotenv('apikey.env')

def test_pdf_processing(pdf_path):
    """Test PDF processing"""
    print(f"🔍 Testing PDF processing: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return None
    
    try:
        pdf_processor = PDFProcessor(pdf_path)
        extraction_result = pdf_processor.process_pdf()
        
        if extraction_result['success']:
            medical_report = pdf_processor.format_for_agents(extraction_result)
            print(f"✅ PDF processed successfully")
            print(f"📝 Content length: {len(medical_report)} characters")
            print(f"📄 First 200 characters: {medical_report[:200]}...")
            return medical_report
        else:
            print("❌ Failed to extract text from PDF")
            return None
    except Exception as e:
        print(f"❌ Error processing PDF: {e}")
        return None

def test_single_agent(medical_report, agent_class, agent_name):
    """Test a single AI agent"""
    print(f"\n🤖 Testing {agent_name}...")
    
    try:
        agent = agent_class(medical_report)
        result = agent.run()
        
        if result:
            print(f"✅ {agent_name} completed successfully")
            print(f"📝 Result length: {len(result)} characters")
            print(f"📄 First 300 characters: {result[:300]}...")
            return result
        else:
            print(f"❌ {agent_name} returned empty result")
            return None
    except Exception as e:
        print(f"❌ {agent_name} error: {e}")
        return None

def test_team_analysis(cardio_report, psycho_report, pulmo_report):
    """Test multidisciplinary team analysis"""
    print(f"\n🏥 Testing Multidisciplinary Team...")
    
    try:
        team_agent = MultidisciplinaryTeam(
            cardiologist_report=cardio_report,
            psychologist_report=psycho_report,
            pulmonologist_report=pulmo_report
        )
        
        result = team_agent.run()
        
        if result:
            print(f"✅ Team analysis completed successfully")
            print(f"📝 Result length: {len(result)} characters")
            print(f"📄 First 300 characters: {result[:300]}...")
            return result
        else:
            print(f"❌ Team analysis returned empty result")
            return None
    except Exception as e:
        print(f"❌ Team analysis error: {e}")
        return None

def main():
    print("🧪 AI Health Assist - Debug Test")
    print("=" * 50)
    
    # Test with the PDF you mentioned
    pdf_path = "Medical Reports/Medical Rerort - Michael Johnson - Panic Attack Disorder.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        print("Please ensure the PDF file exists or update the path")
        return
    
    # Test PDF processing
    medical_report = test_pdf_processing(pdf_path)
    if not medical_report:
        print("❌ Cannot proceed without valid medical report")
        return
    
    # Test individual agents
    agents_to_test = [
        (Cardiologist, "Cardiologist"),
        (Psychologist, "Psychologist"),
        (Pulmonologist, "Pulmonologist")
    ]
    
    agent_results = {}
    for agent_class, agent_name in agents_to_test:
        result = test_single_agent(medical_report, agent_class, agent_name)
        agent_results[agent_name] = result
    
    # Test team analysis
    team_result = test_team_analysis(
        agent_results.get("Cardiologist", ""),
        agent_results.get("Psychologist", ""), 
        agent_results.get("Pulmonologist", "")
    )
    
    # Summary
    print(f"\n📊 TEST SUMMARY")
    print("=" * 30)
    
    print(f"PDF Processing: {'✅ Success' if medical_report else '❌ Failed'}")
    for agent_name in ["Cardiologist", "Psychologist", "Pulmonologist"]:
        result = agent_results.get(agent_name)
        print(f"{agent_name}: {'✅ Success' if result else '❌ Failed'}")
    print(f"Team Analysis: {'✅ Success' if team_result else '❌ Failed'}")
    
    # Check API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print(f"\n⚠️ WARNING: GOOGLE_API_KEY not found in apikey.env")
        print(f"This could be why agents are failing!")
    else:
        print(f"\n✅ API Key found (length: {len(api_key)})")
    
    print(f"\n💡 If agents are failing, check:")
    print(f"   1. API key in apikey.env")
    print(f"   2. Internet connection")
    print(f"   3. Google AI API quotas/limits")

if __name__ == "__main__":
    main()