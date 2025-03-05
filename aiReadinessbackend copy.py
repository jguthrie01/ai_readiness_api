from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from fpdf import FPDF
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

def generate_report(score, result):
    """Generates a PDF report based on the AI Readiness Score."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "AI Readiness Assessment Report", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, f"Your AI Readiness Score: {score}", ln=True, align="C")
    pdf.ln(5)
    
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, f"Assessment Summary: {result}")
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Next Steps:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, "1. Review your AI readiness level and identify key areas for improvement.\n"
                       "2. Explore AI solutions tailored to your business needs.\n"
                       "3. Contact our team for a personalized AI strategy session.")
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Get in Touch:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, "If you're ready to take the next step, email us at contact@yourcompany.com.")
    
    file_path = "ai_readiness_report.pdf"
    pdf.output(file_path)
    return file_path

@app.route('/process_score', methods=['POST'])
def process_score():
    try:
        data = request.json  # or request.get_json()

        # Extract scores from JSON data
        score = sum([
            int(data.get("data_readiness", 0)),
            int(data.get("automation_use", 0)),
            int(data.get("ai_literacy", 0)),
            int(data.get("tech_infra", 0)),
            int(data.get("leadership_commitment", 0))
        ])
        
        # Determine AI Readiness Level
        if score <= 8:
            result = "Low AI Readiness: Start with foundational AI knowledge."
        elif score <= 14:
            result = "Medium AI Readiness: AI could benefit your business with the right strategy."
        else:
            result = "High AI Readiness: You are well-positioned to implement AI solutions!"
        
        report_path = generate_report(score, result)
        
        return jsonify({"score": score, "result": result, "report_url": "/download_report"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download_report', methods=['GET'])
def download_report():
    try:
        return send_file("ai_readiness_report.pdf", as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
