from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from fpdf import FPDF
import matplotlib
matplotlib.use('Agg')  # Force matplotlib to use a non-GUI backend
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
CORS(app)

def generate_chart(breakdown):
    """Generates a bar chart for AI Readiness Score breakdown."""
    ordered_categories = ["Data Readiness", "Automation Use", "AI Literacy", "Technology Infrastructure", "Leadership Commitment"]
    scores = [breakdown[category] for category in ordered_categories]

    plt.figure(figsize=(5.5, 3))  # Adjust size to fit better
    plt.barh(ordered_categories, scores, color=['blue', 'green', 'orange', 'red', 'purple'])
    plt.xlabel("Score (out of 5)")
    plt.title("AI Readiness Score Breakdown")
    plt.xlim(0, 5)
    plt.tight_layout()

    chart_path = "ai_readiness_chart.png"
    plt.savefig(chart_path, dpi=100)
    plt.close()
    return chart_path

def generate_report(score, breakdown, result, recommendations, readiness_timeline, explanation):
    """Generates a PDF report based on the AI Readiness Score."""
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 8, "AI Readiness Assessment Report", ln=True, align="C")
    pdf.ln(6)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(200, 8, f"Your AI Readiness Score: {score} / 20", ln=True, align="C")
    pdf.ln(8)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, "Score Breakdown:", ln=True)
    pdf.set_font("Arial", "", 10)
    for category in ["Data Readiness", "Automation Use", "AI Literacy", "Technology Infrastructure", "Leadership Commitment"]:
        pdf.cell(0, 6, f"{category}: {breakdown[category]}/5", ln=True)
    pdf.ln(6)

    # Insert AI Readiness Chart
    chart_path = generate_chart(breakdown)
    pdf.image(chart_path, x=10, w=90)
    pdf.ln(10)  # Reduce space to fit better

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, "Readiness Level:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, result)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, explanation)
    pdf.ln(6)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, "Next Steps:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, recommendations)
    pdf.ln(6)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, "Estimated AI Readiness Timeline:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, readiness_timeline, ln=True)
    pdf.ln(6)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, "Get in Touch:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, "If you're ready to take the next step, email us at contact@wysstrategies.com.")

    file_path = "/tmp/ai_readiness_report.pdf"
    pdf.output(file_path)
    os.remove(chart_path)  # Clean up chart image
    return file_path

@app.route('/process_score', methods=['POST'])
def process_score():
    try:
        data = request.json

        weights = {
            "Data Readiness": 0.30,
            "Automation Use": 0.15,
            "AI Literacy": 0.20,
            "Technology Infrastructure": 0.20,
            "Leadership Commitment": 0.15
        }

        breakdown = {category: int(float(data.get(category.lower().replace(" ", "_"), 0))) for category in weights.keys()}
        weighted_score = sum(breakdown[category] * weights[category] for category in weights.keys()) * 4
        weighted_score = round(weighted_score, 2)

        if weighted_score <= 5:
            result = "Low AI Readiness"
        elif weighted_score <= 10:
            result = "Emerging AI Readiness"
        elif weighted_score <= 15:
            result = "Moderate AI Readiness"
        elif weighted_score <= 20:
            result = "High AI Readiness"
        else:
            result = "AI Leader"

        explanations = {
            "Low AI Readiness": "Your organization is at the beginning of its AI journey. You should focus on building a strong data infrastructure and leadership alignment to prepare for AI adoption. Consider foundational AI literacy training and initial automation strategies to develop a long-term AI roadmap.",
            "Emerging AI Readiness": "Your organization has started exploring AI but lacks full integration. Strengthening AI literacy and improving automation processes will help scale AI initiatives. Prioritize structured AI experiments to assess feasibility in key business functions.",
            "Moderate AI Readiness": "Your organization is making significant progress. AI is being piloted in certain areas, but a comprehensive strategy is needed to scale AI initiatives organization-wide. Focus on integrating AI-driven decision-making and enhancing workforce capabilities.",
            "High AI Readiness": "Your organization is well-positioned for AI adoption. AI solutions should now be deployed at scale with continuous improvements based on performance analytics. Consider investing in AI governance and compliance to sustain and optimize AI-driven transformation.",
            "AI Leader": "Your organization is at the forefront of AI adoption. Focus on expanding AI innovation, refining governance frameworks, and ensuring ethical and responsible AI use. AI should be a core component of your business strategy, fostering a culture of continuous AI-driven improvement."
        }

        explanation = explanations[result]
        report_path = generate_report(weighted_score, breakdown, result, explanations[result], "6 months - 1 year", explanation)

        return jsonify({
            "score": weighted_score,
            "score_breakdown": breakdown,
            "result": result,
            "explanation": explanation,
            "report_url": "/download_report"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download_report', methods=['GET'])
def download_report():
    report_path = "/tmp/ai_readiness_report.pdf"
    if not os.path.exists(report_path):
        return jsonify({"error": "Report file not found"}), 404
    return send_file(report_path, as_attachment=True)

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render-assigned port or default to 5000
    app.run(debug=True, host='0.0.0.0', port=port)

