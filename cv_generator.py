import json
import os
from fpdf import FPDF

# Get the base directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class CV_Maker:
    def __init__(self):
        # Create output directory if it doesn't exist
        self.output_dir = os.path.join(BASE_DIR, "cv_outputs")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"[INFO] Created directory: {self.output_dir}")

    def generate_cv(self, user):
        # Fix non-ASCII characters (quotes/dashes)
        user['summary'] = user['summary'].replace('\u2019', "'").replace('\u2013', "-").replace('\u2014', "-")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(15, 12, 15)
        
        # --- HEADER ---
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 10, user['name'], ln=True, align='C')
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(100, 100, 100) 
        pdf.cell(0, 7, user['title'], ln=True, align='C')
        pdf.set_text_color(0, 0, 0) 
        pdf.set_font("Arial", '', 9)
        pdf.cell(0, 5, user['contact_1'], ln=True, align='C')
        pdf.cell(0, 5, user['contact_2'], ln=True, align='C')
        pdf.ln(5)

        def add_section_header(title):
            pdf.ln(2)
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 6, title, ln=True)
            pdf.line(15, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(2)

        # --- SUMMARY ---
        add_section_header("PROFESSIONAL SUMMARY")
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 5, user['summary'])

        # --- SKILLS ---
        add_section_header("TECHNICAL SKILLS & COMPETENCIES")
        pdf.set_font("Arial", '', 10)
        expertise = user['expertise']
        for i in range(0, len(expertise), 2):
            col1 = f"- {expertise[i]}"
            col2 = f"- {expertise[i+1]}" if i+1 < len(expertise) else ""
            pdf.cell(90, 5, col1)
            pdf.cell(90, 5, col2, ln=True)

        # --- EXPERIENCE ---
        add_section_header("WORK EXPERIENCE & PROJECTS")
        for exp in user['experience']:
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(45, 5, exp['date']) 
            pdf.set_left_margin(60) 
            pdf.multi_cell(0, 5, exp['company']) 
            if exp.get('role'):
                pdf.set_font("Arial", 'I', 10)
                pdf.multi_cell(0, 5, exp['role'])
            if exp.get('desc'):
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 5, exp['desc'])
            pdf.set_left_margin(15) 
            pdf.ln(2)

        # --- EDUCATION ---
        add_section_header("EDUCATION")
        for edu in user['education']:
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(45, 5, edu['date'])
            pdf.set_left_margin(60)
            pdf.set_font("Arial", '', 10)
            pdf.multi_cell(0, 5, edu['details'])
            pdf.set_left_margin(15)
            pdf.ln(2)

        # --- ADDITIONAL ---
        add_section_header("ADDITIONAL INFORMATION")
        for key, val in user['additional'].items():
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(35, 5, f"{key}:")
            pdf.set_left_margin(50)
            pdf.set_font("Arial", '', 10)
            pdf.multi_cell(0, 5, val)
            pdf.set_left_margin(15)
            pdf.ln(1)

        # --- FILE SAVING ---
        safe_name = user['name'].replace(' ', '_')
        output_filename = f"{safe_name}_CV.pdf"
        output_path = os.path.join(self.output_dir, output_filename)
        
        pdf.output(output_path)
        print("-" * 30)
        print(f"[SUCCESS] PDF Created Successfully!")
        print(f"Location: {output_path}")
        print("-" * 30)

# --- Sample Data (Replace with your own) ---
sample_data = {
    "name": "YOUR NAME HERE",
    "title": "DESIRED JOB TITLE",
    "contact_1": "City, Country | email@example.com | +00 000 000 000",
    "contact_2": "linkedin.com/in/yourprofile",
    "summary": "Write a professional summary about your skills and career goals here.",
    "expertise": [
        "Skill One", "Skill Two",
        "Skill Three", "Skill Four",
        "Skill Five", "Skill Six"
    ],
    "experience": [
        {
            "date": "Year - Present",
            "company": "Company Name or Project Name",
            "role": "Your Position",
            "desc": "Describe your responsibilities and achievements."
        }
    ],
    "education": [
        {
            "date": "Year - Year",
            "details": "Degree Name\nUniversity or School Name"
        }
    ],
    "additional": {
        "Certifications": "List your certificates here",
        "Languages": "e.g., English, Sinhala",
        "Interests": "e.g., Photography, Coding",
        "References": "Available upon request"
    }
}

if __name__ == "__main__":
    maker = CV_Maker()
    maker.generate_cv(sample_data)
