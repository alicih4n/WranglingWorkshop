from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Lab 3 - Data Engineering & EDA Submission', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, body)
        self.ln()

pdf = PDF()
pdf.add_page()

# student Info
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Student Name: Ali Cihan Ozdemir', 0, 1)
pdf.cell(0, 10, 'Student ID: 9091405', 0, 1)
pdf.cell(0, 10, 'Date: 2026-02-06', 0, 1)
pdf.ln(10)

# Repository Link
pdf.chapter_title('GitHub Repository')
pdf.set_font('Arial', 'U', 11)
pdf.set_text_color(0, 0, 255)
pdf.cell(0, 6, 'https://github.com/alicih4n/Lab3-DataEngineering.git', 0, 1, link='https://github.com/alicih4n/Lab3-DataEngineering.git')
pdf.set_text_color(0, 0, 0)
pdf.ln(5)

# Project Summary
pdf.chapter_title('Project Summary')
summary_text = (
    "1. Cloud Database & Advanced Architecture: Established a PostgreSQL connection on Neon. "
    "Designed a multi-table schema with 'employees' and 'departments' connected via Foreign Keys to simulate enterprise data complexity. "
    "Created a Python script (lab3_sdg.py) to generate 500 synthetic employee records linked to 5 departments, utilizing 20% 'dirty data' logic.\n\n"
    "2. Data Wrangling & Cleaning: Developed a Jupyter Notebook to extract data from multiple SQL tables. "
    "Used Pandas to inspect quality, impute missing salaries, standardize job titles, and resolve logic errors. "
    "Performed a SQL-style Inner Join in Pandas to enrich employee records with departmental metadata.\n\n"
    "3. Feature Engineering & Scaling: Created 'start_year' and 'years_of_service' features. "
    "Applied Z-Score standardization (StandardScaler) to salary data to prepare it for potential Neural Network applications.\n\n"
    "4. Visual Intelligence: Built advanced visualizations including a Grouped Bar Chart for salary trends "
    "and a FacetGrid Heatmap for departmental salary distributions using the joined dataset."
)
pdf.chapter_body(summary_text)

# Contribution Note
pdf.chapter_title('Contribution Validation')
contribution_text = (
    "Please note that this project was completed entirely by Ali Cihan Ozdemir.\n"
    "Group partner Roshan was absent from class and did not contribute to this lab submission."
)
pdf.set_font('Arial', 'B', 11) # Bold for emphasis
pdf.set_text_color(200, 0, 0) # Dark Red for visibility
pdf.multi_cell(0, 6, contribution_text)

pdf.output('Lab3_Submission_AliCihanOzdemir.pdf')
print("PDF Generated Successfully")
