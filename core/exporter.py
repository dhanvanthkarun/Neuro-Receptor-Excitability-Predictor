import os
from fpdf import FPDF
from datetime import datetime

class ReportExporter:
    def __init__(self, reports_dir="exports/reports"):
        """
        Initializes the export engine and ensures the target directories exist.
        """
        self.reports_dir = reports_dir
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_pdf_report(self, protein_id, report_text):
        """
        Converts the AI structural analysis into a formatted PDF and saves it locally.
        """
        # Clean up markdown symbols (like **bold**) for the PDF compiler
        clean_text = report_text.replace('**', '').replace('*', '').replace('#', '')
        
        pdf = FPDF()
        pdf.add_page()
        
        # Add Header
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, f"NREP Excitability Report: {protein_id}", align="C", new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("helvetica", "I", 10)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pdf.cell(0, 10, f"Generated on: {timestamp} | Engine: TRIADS NREP Pipeline", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.line(10, 30, 200, 30)
        pdf.ln(10)
        
        # Add AI Analytical Content
        pdf.set_font("helvetica", size=11)
        pdf.multi_cell(0, 7, clean_text)
        
        # Construct exact file path
        filename = f"NREP_{protein_id}_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.reports_dir, filename)
        
        # Save securely to local disk
        pdf.output(filepath)
        print(f"[NREP] Report securely exported to: {filepath}")
        
        return filepath

