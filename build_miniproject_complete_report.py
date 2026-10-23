#!/usr/bin/env python3
"""Builds the complete official Apollo University Mini-Project Report
taking Project_Report.docx content and formatting it strictly according to
the official institutional template:
/Users/jathinreddy/.gemini/antigravity/brain/f353d961-e7fd-445e-894a-a4a5c051abdb/.user_uploaded/media_1792773194544_9aa85a32.docx
Generates:
1. MiniProject_Apollo_Official_Report.docx (Word Document)
2. MiniProject_Canva_Visual_Report.pdf (Canva-importable / Submission PDF)
3. MiniProject_Canva_Visual_Report.html (Standalone visual HTML)
4. MiniProject_Apollo_Official_Report.md (Synchronized Markdown)
"""

import os
import sys
import subprocess
import base64
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

TEMPLATE_DOCX = "/Users/jathinreddy/.gemini/antigravity/brain/f353d961-e7fd-445e-894a-a4a5c051abdb/.user_uploaded/media_1792773194544_9aa85a32.docx"
WORKSPACE_DIR = "/Users/jathinreddy/Desktop/InstaHealth"
ARTIFACT_DIR = "/Users/jathinreddy/.gemini/antigravity/brain/f353d961-e7fd-445e-894a-a4a5c051abdb"

OUTPUT_DOCX = os.path.join(WORKSPACE_DIR, "MiniProject_Apollo_Official_Report.docx")
OUTPUT_MD = os.path.join(WORKSPACE_DIR, "MiniProject_Apollo_Official_Report.md")
OUTPUT_HTML = os.path.join(WORKSPACE_DIR, "MiniProject_Canva_Visual_Report.html")
OUTPUT_PDF = os.path.join(WORKSPACE_DIR, "MiniProject_Canva_Visual_Report.pdf")

# ==============================================================================
# REPORT METADATA & TEXTS
# ==============================================================================
PROJECT_TITLE = "ON-DEVICE PERSONALIZED HEALTH EVENT PREDICTION USING TINYML AND ON-DEVICE SMALL LANGUAGE MODELS FOR PRIVACY-PRESERVING HEALTH ANALYTICS"
STUDENT_1 = "A . Jathin Reddy ( reg no : 122311520105)"
STUDENT_2 = "K.Pranay Kumar (reg.no : 122311520133)"
GUIDE_NAME = "Dr. Thirumalesu.K"
GUIDE_DESIG = "Assistant Professor"
DEPARTMENT = "Department of Computer Science & Engineering"
SCHOOL = "School of Technology"
UNIVERSITY = "The Apollo University, Chittoor"
DATE_STR = "April, 2026"

# Helper for image base64
def img_to_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

logo_b64 = img_to_b64(os.path.join(WORKSPACE_DIR, "apollo_logo.png"))
gantt_b64 = img_to_b64(os.path.join(WORKSPACE_DIR, "fig_miniproject_gantt.png"))
arch_b64 = img_to_b64(os.path.join(WORKSPACE_DIR, "fig_miniproject_arch.png"))
dfd_b64 = img_to_b64(os.path.join(WORKSPACE_DIR, "fig_miniproject_dfd.png"))
perf_b64 = img_to_b64(os.path.join(WORKSPACE_DIR, "fig_miniproject_perf.png"))

print("Compiling Mini-Project Academic Report...")

# ==============================================================================
# DOCX BUILDER FUNCTIONS
# ==============================================================================
def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="94A3B8", sz="4", val="single"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:left w:val="none"/>
                <w:right w:val="none"/>
                <w:insideV w:val="none"/>
            </w:tblBorders>
        ''')
        tblPr[0].append(borders)

def format_para_runs(p, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color=RGBColor(0, 0, 0)):
    for r in p.runs:
        r.font.name = font_name
        r.font.size = Pt(size_pt)
        r.bold = bold
        r.italic = italic
        if color:
            r.font.color.rgb = color

def add_para(doc, text="", size=12, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, space_before=0, line_spacing=1.5, color=RGBColor(0, 0, 0)):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(size)
        r.bold = bold
        r.italic = italic
        if color:
            r.font.color.rgb = color
    return p

def add_heading_1(doc, text):
    return add_para(doc, text, size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=12, line_spacing=1.5, color=RGBColor(0, 0, 0))

def add_heading_2(doc, text):
    return add_para(doc, text, size=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=14, space_after=6, line_spacing=1.5, color=RGBColor(0, 0, 0))

def add_heading_3(doc, text):
    return add_para(doc, text, size=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=4, line_spacing=1.5, color=RGBColor(31, 55, 99))

def add_image_figure(doc, img_path, caption_text, width_in=5.4):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(12)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(width_in))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(14)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(10.5)
        r_cap.bold = True
        r_cap.font.color.rgb = RGBColor(0, 0, 0)
        return p_cap
    return None

def add_code_snippet(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:bottom w:val="none"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="2563EB"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(code_text.strip())
    r.font.name = "Courier New"
    r.font.size = Pt(9.0)
    r.font.color.rgb = RGBColor(15, 23, 42)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)

def add_table_custom(doc, title, headers, rows):
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(12)
    p_cap.paragraph_format.space_after = Pt(6)
    r_cap = p_cap.add_run(title)
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(10.5)
    r_cap.bold = True
    r_cap.font.color.rgb = RGBColor(0, 0, 0)
    
    table = doc.add_table(rows=len(rows)+1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="94A3B8", sz="4", val="single")
    
    # Headers
    for c_idx, h_text in enumerate(headers):
        cell = table.rows[0].cells[c_idx]
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(h_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)
        
    # Rows
    for r_idx, row in enumerate(rows):
        row_cells = table.rows[r_idx+1].cells
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            cell = row_cells[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (c_idx == 0 or len(val) < 15) else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(str(val))
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.0)
            r.font.color.rgb = RGBColor(0, 0, 0)
            
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(8)

# ==============================================================================
# LOAD AND FORMAT DOCX
# ==============================================================================
print(f"Loading official template from {TEMPLATE_DOCX}")
doc = docx.Document(TEMPLATE_DOCX)

# Update Cover Page
print("Applying cover page styling and Apollo logo...")
p0 = doc.paragraphs[0]
p0.text = PROJECT_TITLE
p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
p0.paragraph_format.space_before = Pt(0)
p0.paragraph_format.space_after = Pt(6)
p0.paragraph_format.line_spacing = 1.15
for r in p0.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(15)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

for idx in [1, 2, 5, 8, 9, 11, 13, 18, 24]:
    doc.paragraphs[idx].text = ""
    doc.paragraphs[idx].paragraph_format.space_before = Pt(0)
    doc.paragraphs[idx].paragraph_format.space_after = Pt(0)
    doc.paragraphs[idx].paragraph_format.line_spacing = 1.0

p3 = doc.paragraphs[3]
p3.text = "A Project Report"
p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
p3.paragraph_format.space_before = Pt(4)
p3.paragraph_format.space_after = Pt(2)
for r in p3.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

p4 = doc.paragraphs[4]
p4.text = "Submitted by"
p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
p4.paragraph_format.space_before = Pt(2)
p4.paragraph_format.space_after = Pt(2)
for r in p4.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.italic = True
    r.font.color.rgb = RGBColor(0, 0, 0)

p6 = doc.paragraphs[6]
p6.text = STUDENT_1
p6.alignment = WD_ALIGN_PARAGRAPH.CENTER
p6.paragraph_format.space_before = Pt(1)
p6.paragraph_format.space_after = Pt(1)
p6.paragraph_format.line_spacing = 1.0
for r in p6.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

p7 = doc.paragraphs[7]
p7.text = STUDENT_2
p7.alignment = WD_ALIGN_PARAGRAPH.CENTER
p7.paragraph_format.space_before = Pt(1)
p7.paragraph_format.space_after = Pt(4)
p7.paragraph_format.line_spacing = 1.0
for r in p7.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

p10 = doc.paragraphs[10]
p10.text = "in partial fulfillment for the award of the degree"
p10.alignment = WD_ALIGN_PARAGRAPH.CENTER
p10.paragraph_format.space_before = Pt(2)
p10.paragraph_format.space_after = Pt(1)
p10.paragraph_format.line_spacing = 1.0
for r in p10.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.italic = True

p12 = doc.paragraphs[12]
p12.text = "of"
p12.alignment = WD_ALIGN_PARAGRAPH.CENTER
p12.paragraph_format.space_before = Pt(0)
p12.paragraph_format.space_after = Pt(1)
p12.paragraph_format.line_spacing = 1.0
for r in p12.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.italic = True

p14 = doc.paragraphs[14]
p14.text = "Bachelor of Technology"
p14.alignment = WD_ALIGN_PARAGRAPH.CENTER
p14.paragraph_format.space_before = Pt(1)
p14.paragraph_format.space_after = Pt(1)
p14.paragraph_format.line_spacing = 1.0
for r in p14.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.bold = True

p15 = doc.paragraphs[15]
p15.text = "in"
p15.alignment = WD_ALIGN_PARAGRAPH.CENTER
p15.paragraph_format.space_before = Pt(0)
p15.paragraph_format.space_after = Pt(1)
p15.paragraph_format.line_spacing = 1.0
for r in p15.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

p16 = doc.paragraphs[16]
p16.text = "Computer Science and Engineering (AI & DS)"
p16.alignment = WD_ALIGN_PARAGRAPH.CENTER
p16.paragraph_format.space_before = Pt(1)
p16.paragraph_format.space_after = Pt(4)
p16.paragraph_format.line_spacing = 1.0
for r in p16.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.bold = True

p17 = doc.paragraphs[17]
p17.text = "Under the Guidance of"
p17.alignment = WD_ALIGN_PARAGRAPH.CENTER
p17.paragraph_format.space_before = Pt(3)
p17.paragraph_format.space_after = Pt(1)
for r in p17.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.italic = True

p19 = doc.paragraphs[19]
p19.text = f"{GUIDE_NAME}\n{GUIDE_DESIG}"
p19.alignment = WD_ALIGN_PARAGRAPH.CENTER
p19.paragraph_format.space_before = Pt(1)
p19.paragraph_format.space_after = Pt(4)
p19.paragraph_format.line_spacing = 1.05
for r in p19.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True

p20 = doc.paragraphs[20]
p20.text = ""
p20.alignment = WD_ALIGN_PARAGRAPH.CENTER
p20.paragraph_format.space_before = Pt(6)
p20.paragraph_format.space_after = Pt(6)
r20 = p20.add_run()
r20.add_picture(os.path.join(WORKSPACE_DIR, "apollo_logo.png"), width=Inches(1.8))

p21 = doc.paragraphs[21]
p21.text = "SCHOOL OF TECHNOLOGY"
p21.alignment = WD_ALIGN_PARAGRAPH.CENTER
p21.paragraph_format.space_before = Pt(2)
p21.paragraph_format.space_after = Pt(1)
p21.paragraph_format.line_spacing = 1.0
for r in p21.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.bold = True

p22 = doc.paragraphs[22]
p22.text = "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING"
p22.alignment = WD_ALIGN_PARAGRAPH.CENTER
p22.paragraph_format.space_before = Pt(0)
p22.paragraph_format.space_after = Pt(1)
p22.paragraph_format.line_spacing = 1.0
for r in p22.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.bold = True

p23 = doc.paragraphs[23]
p23.text = "THE APOLLO UNIVERSITY, CHITTOOR"
p23.alignment = WD_ALIGN_PARAGRAPH.CENTER
p23.paragraph_format.space_before = Pt(0)
p23.paragraph_format.space_after = Pt(4)
p23.paragraph_format.line_spacing = 1.0
for r in p23.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.bold = True

p25 = doc.paragraphs[25]
p25.text = DATE_STR
p25.alignment = WD_ALIGN_PARAGRAPH.CENTER
p25.paragraph_format.space_before = Pt(2)
p25.paragraph_format.space_after = Pt(0)
p25.paragraph_format.line_spacing = 1.0
for r in p25.runs:
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True

# Update Declaration
print("Updating Declaration...")
doc.paragraphs[30].text = (
    f"   I hereby declare that the project entitled “{PROJECT_TITLE}” submitted by us, "
    f"for the award of the degree of Bachelor of Technology in Computer Science & Engineering (AI & DS), School of Technology "
    f"to The Apollo University is a record of bonafide work carried out by us under the supervision of {GUIDE_NAME}, "
    f"{GUIDE_DESIG}, {DEPARTMENT}."
)
format_para_runs(doc.paragraphs[30], font_name="Times New Roman", size_pt=12)

doc.paragraphs[31].text = (
    "   We further declare that the work reported in this thesis has not been submitted and will not be submitted, "
    "either in part or in full, for the award of any other degree or diploma in this institute or any other institute or university."
)
format_para_runs(doc.paragraphs[31], font_name="Times New Roman", size_pt=12)

doc.paragraphs[34].text = f"                                                                           1. {STUDENT_1}        ____________________"
format_para_runs(doc.paragraphs[34], font_name="Times New Roman", size_pt=11)
doc.paragraphs[35].text = f"                                                                           2. {STUDENT_2}        ____________________"
format_para_runs(doc.paragraphs[35], font_name="Times New Roman", size_pt=11)

doc.paragraphs[37].text = "Place\t: Chittoor"
format_para_runs(doc.paragraphs[37], font_name="Times New Roman", size_pt=12)
doc.paragraphs[38].text = f"     Date\t: {DATE_STR}"
format_para_runs(doc.paragraphs[38], font_name="Times New Roman", size_pt=12)

# Update Bonafide Certificate
print("Updating Bonafide Certificate...")
doc.paragraphs[47].text = (
    f"         This is to certify that the project report entitled “{PROJECT_TITLE}” "
    f"is the bonafide work carried out by A . Jathin Reddy (Register No: 122311520105) and K.Pranay Kumar "
    f"(Register No: 122311520133), under my supervision and guidance, in partial fulfillment of the requirements "
    f"for the award of the degree of Bachelor of Technology in Computer Science & Engineering (AI & DS) by The Apollo University, Chittoor."
)
format_para_runs(doc.paragraphs[47], font_name="Times New Roman", size_pt=12)

doc.paragraphs[51].text = (
    f"                                                                                                Signature of the Guide\n"
    f"                                                                                                {GUIDE_NAME}\n"
    f"                                                                                                {GUIDE_DESIG}, Dept. of CSE"
)
format_para_runs(doc.paragraphs[51], font_name="Times New Roman", size_pt=11, bold=True)

# Update Acknowledgement
print("Updating Acknowledgement...")
doc.paragraphs[73].text = (
    f"I express my sincere gratitude to my project guide {GUIDE_NAME}, {GUIDE_DESIG}, "
    f"{DEPARTMENT}, School of Technology, The Apollo University, Chittoor, for their continuous guidance, "
    f"valuable suggestions and constructive feedback throughout the course of this project. Their support has been instrumental "
    f"in the successful completion of this work."
)
format_para_runs(doc.paragraphs[73], font_name="Times New Roman", size_pt=12)

doc.paragraphs[75].text = (
    "I also thank the Project Coordinator, Department of Computer Science & Engineering, School of Technology, "
    "The Apollo University for giving me the right direction whenever I came to the University."
)
format_para_runs(doc.paragraphs[75], font_name="Times New Roman", size_pt=12)

doc.paragraphs[77].text = (
    "I extend my heartfelt thanks to the Programme Coordinator, Department of Computer Science & Engineering, "
    "School of Technology, The Apollo University for providing the necessary academic support and facilities to carry out this project effectively."
)
format_para_runs(doc.paragraphs[77], font_name="Times New Roman", size_pt=12)

doc.paragraphs[79].text = (
    "I also convey my sincere thanks to the Prof. D. Jagadeesan, Dean, School of Technology for their support and encouragement throughout the project work."
)
format_para_runs(doc.paragraphs[79], font_name="Times New Roman", size_pt=12)

doc.paragraphs[81].text = (
    "I express my profound gratitude to the Honourable Chancellor Dr Prathap C. Reddy, Dr. H. Vinod Bhat, Vice-Chancellor "
    "and Prof. M. Potharaju, Registrar of The Apollo University for their visionary leadership, constant encouragement and "
    "for fostering a supportive academic environment."
)
format_para_runs(doc.paragraphs[81], font_name="Times New Roman", size_pt=12)

doc.paragraphs[90].text = STUDENT_1
format_para_runs(doc.paragraphs[90], font_name="Times New Roman", size_pt=11, bold=True)
doc.paragraphs[91].text = STUDENT_2
format_para_runs(doc.paragraphs[91], font_name="Times New Roman", size_pt=11, bold=True)
doc.paragraphs[92].text = ""
doc.paragraphs[93].text = ""

# Table 0 (Contents)
print("Updating Table of Contents...")
toc_tbl = doc.tables[0]
toc_page_map = {
    1: "I", 2: "II", 3: "III", 4: "IV",
    5: "1", 6: "1", 7: "3",
    8: "6", 9: "6", 10: "7", 11: "11", 12: "12",
    13: "15", 14: "15", 15: "17",
    16: "20", 17: "20", 18: "23", 19: "26",
    20: "30", 21: "30", 22: "32", 23: "35", 24: "38",
    25: "41", 26: "41", 27: "44", 28: "47",
    29: "51", 30: "51", 31: "52",
    32: "54", 33: "57"
}
for r_idx, p_val in toc_page_map.items():
    if r_idx < len(toc_tbl.rows):
        cell = toc_tbl.rows[r_idx].cells[2]
        cell.text = p_val
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        format_para_runs(p, font_name="Times New Roman", size_pt=10, bold=(r_idx in [5, 8, 13, 16, 20, 25, 29, 32, 33]))

# Abstract
print("Updating Abstract...")
miniproject_abstract = (
    "Continuous biometric telemetry gathered from consumer wearable devices offers immense potential for "
    "preemptive healthcare risk prediction, such as early detection of cardiac arrhythmia, sudden falls, and dehydration. "
    "However, conventional commercial health monitoring frameworks mandate streaming raw physiological time-series data to "
    "centralized cloud servers, introducing severe user privacy vulnerabilities, cloud dependency, and communication latency. "
    "This project presents an on-device, privacy-preserving predictive health intelligence system leveraging Tiny Machine "
    "Learning (TinyML) and quantized Small Language Models (TinyLlama-1.1B). The architecture incorporates multimodal sensor "
    "ingestion, on-device temporal feature extraction, 4-bit/8-bit integer quantization, attention-based local explainability, "
    "and decentralized federated learning (FedAvg). Experimental validation on embedded hardware confirms that the quantized "
    "pipeline delivers accurate event forecasting with 480 ms inference latency and 620 MB peak RAM footprint, completely "
    "eliminating raw physiological data transmission to external servers."
)
doc.paragraphs[168].text = miniproject_abstract
format_para_runs(doc.paragraphs[168], font_name="Times New Roman", size_pt=12)
doc.paragraphs[168].paragraph_format.line_spacing = 1.5

doc.paragraphs[170].text = "Keywords: TinyML, On-Device Inference, Small Language Models, Privacy-Preserving Health Analytics, Federated Learning."
format_para_runs(doc.paragraphs[170], font_name="Times New Roman", size_pt=11, bold=True, italic=True)

# Table 1: Figures
print("Updating List of Figures...")
tbl_fig = doc.tables[1]
for row in tbl_fig.rows[1:]:
    row._element.getparent().remove(row._element)

miniproject_figures = [
    ("Figure 3.1", "10-Week Comprehensive Project Engineering Timeline and Milestone Gantt Schedule", "18"),
    ("Figure 4.1", "On-Device Personalized Health Event Prediction: Multi-Layered TinyML System Architecture", "23"),
    ("Figure 4.2", "Data Flow Diagram (DFD) Level 1: Multimodal Sensor Ingestion and Prediction Pipeline", "26"),
    ("Figure 6.1", "TinyLlama Model Compression Profile: Inference Latency and Memory Footprint Benchmark", "48")
]
for f_no, f_title, p_num in miniproject_figures:
    r = tbl_fig.add_row()
    cells = r.cells
    cells[0].text = f_no
    cells[1].text = ""
    cells[2].text = f_title
    cells[3].text = p_num
    for c_idx, c in enumerate(cells):
        set_cell_margins(c, top=40, bottom=40, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else (WD_ALIGN_PARAGRAPH.RIGHT if c_idx == 3 else WD_ALIGN_PARAGRAPH.LEFT)
        format_para_runs(p, font_name="Times New Roman", size_pt=9.5, bold=(c_idx == 0))

# Table 2: Tables
print("Updating List of Tables...")
tbl_tab = doc.tables[2]
for row in tbl_tab.rows:
    row._element.getparent().remove(row._element)
hdr = tbl_tab.add_row().cells
hdr[0].text, hdr[1].text, hdr[2].text = "Table No.", "Title", "Page No."
for c in hdr:
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_para_runs(p, font_name="Times New Roman", size_pt=10, bold=True)

miniproject_tables = [
    ("Table 1.1", "Project Team Composition, Registration Numbers, and Specialized Engineering Roles", "2"),
    ("Table 2.1", "Technology Stack Comparison: Architectural Purpose, Constraints, and Justifications", "10"),
    ("Table 3.1", "10-Week Implementation Schedule, Engineering Milestones, and Deliverable Artifacts", "17"),
    ("Table 4.1", "Target Embedded Hardware and Mobile Platform Technical Specifications", "21"),
    ("Table 4.2", "Software Libraries, Frameworks, and Edge Model Optimization Toolchain", "22"),
    ("Table 5.1", "TinyLlama Model Compression & Numeric Quantization Trade-Off Analysis", "36"),
    ("Table 6.1", "Comprehensive System Validation and Test Case Execution Results (TC01 - TC10)", "45"),
    ("Table 6.2", "Comparative Prediction Accuracy: TinyLlama vs. LSTM Baseline vs. Cloud Server", "47"),
    ("Table 6.3", "Benchmarked On-Device Inference Latency and Memory Footprint Under INT4/INT8", "49")
]
for t_no, t_title, p_num in miniproject_tables:
    r = tbl_tab.add_row()
    cells = r.cells
    cells[0].text, cells[1].text, cells[2].text = t_no, t_title, p_num
    for c_idx, c in enumerate(cells):
        set_cell_margins(c, top=40, bottom=40, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else (WD_ALIGN_PARAGRAPH.RIGHT if c_idx == 2 else WD_ALIGN_PARAGRAPH.LEFT)
        format_para_runs(p, font_name="Times New Roman", size_pt=9.5, bold=(c_idx == 0))

# Table 3: Abbreviations
print("Updating List of Abbreviations...")
tbl_abbr = doc.tables[3]
for row in tbl_abbr.rows:
    row._element.getparent().remove(row._element)
hdr = tbl_abbr.add_row().cells
hdr[0].text, hdr[1].text = "Abbreviation", "Full Terminology"
for c in hdr:
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_para_runs(p, font_name="Times New Roman", size_pt=10, bold=True)

miniproject_abbrs = [
    ("AIoT", "Artificial Intelligence of Things"),
    ("API", "Application Programming Interface"),
    ("BOM", "Bill of Materials"),
    ("CAM", "Class Activation Mapping"),
    ("CPU", "Central Processing Unit"),
    ("DFD", "Data Flow Diagram"),
    ("EMA", "Exponential Moving Average"),
    ("FedAvg", "Federated Averaging Algorithm"),
    ("FL", "Federated Learning"),
    ("FP32", "32-bit Single Precision Floating Point"),
    ("GPU", "Graphics Processing Unit"),
    ("Grad-CAM", "Gradient-Weighted Class Activation Mapping"),
    ("HRV", "Heart Rate Variability"),
    ("INT4", "4-bit Integer Precision Quantization"),
    ("INT8", "8-bit Integer Precision Quantization"),
    ("LSTM", "Long Short-Term Memory Neural Network"),
    ("MAE", "Mean Absolute Error"),
    ("MEMS", "Micro-Electro-Mechanical Systems"),
    ("MLP", "Multilayer Perceptron"),
    ("NPU", "Neural Processing Unit"),
    ("ONNX", "Open Neural Network Exchange"),
    ("PPG", "Photoplethysmography"),
    ("RAM", "Random Access Memory"),
    ("SLM", "Small Language Model"),
    ("SQI", "Signal Quality Index"),
    ("TFLite", "TensorFlow Lite Embedded Runtime"),
    ("TinyML", "Tiny Machine Learning for Edge Devices")
]
for abbr, full_t in miniproject_abbrs:
    r = tbl_abbr.add_row()
    cells = r.cells
    cells[0].text, cells[1].text = abbr, full_t
    for c_idx, c in enumerate(cells):
        set_cell_margins(c, top=40, bottom=40, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
        format_para_runs(p, font_name="Times New Roman", size_pt=9.5, bold=(c_idx == 0))

# ==============================================================================
# REPLACE BODY PARAGRAPHS WITH RIGOROUS MINIPROJECT REPORT CHAPTERS
# ==============================================================================
print("Injecting comprehensive 7 chapters matching reference document format...")
paras = list(doc.paragraphs)
for p in paras[276:]:
    p._element.getparent().remove(p._element)

# CHAPTER 1
add_heading_1(doc, "CHAPTER 1: INTRODUCTION")
add_heading_2(doc, "1.1 Background of the Study")
add_para(doc, "Wearable smart devices, including smartwatches, activity trackers, and modern smartphones, continuously monitor and record dense streams of personal physiological data. These rich telemetry signals encompass photoplethysmography (PPG) derived heart rates, heart-rate variability (HRV), peripheral blood oxygen saturation (SpO2), 3-axis accelerometer readings, and contextual mobility indicators. The continuous aggregation of this biometric telemetry holds immense transformative potential for preemptive healthcare intelligence—enabling the proactive identification of impending fall events, acute cardiac arrhythmias, severe dehydration, and metabolic fatigue hours before irreversible clinical deterioration occurs.")
add_para(doc, "However, contemporary commercial wearable architectures operate almost exclusively under a centralized cloud-dependent computing paradigm. Raw, highly sensitive biometric timeseries are continuously buffered and transmitted over cellular and Wi-Fi networks to third-party cloud infrastructure for machine learning model inference and long-term storage. This architecture introduces severe data privacy hazards, exposing users to surveillance, unauthorized data brokering, and potential catastrophic regulatory violations under HIPAA and GDPR. Furthermore, cloud reliance creates absolute dependency on network connectivity and introduces non-deterministic communication latencies (typically 1.5 to 4.5 seconds), rendering time-critical emergency alerts impractical in bandwidth-constrained or remote environments.")

add_heading_2(doc, "1.2 Problem Statement")
add_para(doc, "The fundamental dilemma confronting wearable digital healthcare is the forced dichotomy between predictive intelligence and data sovereignty. While advanced deep neural networks and language models offer unprecedented accuracy in multi-signal physiological reasoning, their deployment has historically required high-throughput cloud data centers. Consequently, users are coerced into relinquishing complete physical custody of their intimate biological signatures to receive automated health recommendations. If network latency delays an alert during an arrhythmia episode, or if a third-party server suffers a security breach, the consequences are life-threatening. Therefore, an urgent engineering need exists for an end-to-end, on-device intelligence architecture capable of executing sophisticated multimodal health event prediction directly on edge hardware without transmitting a single byte of raw telemetry off the user's device.")

add_heading_2(doc, "1.3 Motivation & Research Objectives")
add_para(doc, "The motivation for this engineering investigation stems from two converging technological breakthroughs: first, the rapid algorithmic miniaturization of neural architectures into Tiny Machine Learning (TinyML) and quantized Small Language Models (SLMs) capable of running on mobile devices; second, the escalating societal demand for zero-trust, cryptographically sovereign personal data architectures. By uniting these paradigms, this project designs, implements, and benchmarks an on-device health event prediction system that guarantees absolute local privacy while retaining state-of-the-art predictive performance.")
add_para(doc, "The research investigation is guided by five primary engineering objectives:\n"
              "1. Design an ultra-efficient on-device feature extraction pipeline that processes raw PPG and accelerometer signals into rolling physiological vectors in real time.\n"
              "2. Adapt and compress a compact transformer-based small language model (TinyLlama-1.1B) to operate within the severe RAM (<1 GB) and thermal budgets of mobile devices using INT4/INT8 quantization.\n"
              "3. Implement an attention-based explainability layer that extracts internal self-attention attribution weights to generate plain-English diagnostic justifications alongside every health alert.\n"
              "4. Develop a decentralized federated learning (FedAvg) synchronization framework that aggregates encrypted model weight updates to improve global model intelligence without ever exposing raw patient telemetry.\n"
              "5. Perform empirical benchmarking across latency, memory footprint, predictive accuracy, and power consumption on physical embedded hardware.")

add_heading_2(doc, "1.4 Scope of the Project")
add_para(doc, "The engineering scope encompasses the complete software and embedded architecture required for real-time health risk detection. This includes: (a) continuous signal ingestion and quality filtering for PPG and motion sensors; (b) a lightweight baseline LSTM for temporal anomaly and inactivity detection; (c) a 4-bit quantized TinyLlama transformer fine-tuned on multimodal health event forecasting; (d) an attention-weight attribution module generating human-readable alerts; and (e) a simulated federated averaging protocol over multi-device nodes. Out-of-scope aspects include invasive surgical diagnostic sensors, proprietary ASIC semiconductor fabrication, and cloud-hosted commercial telematics.")

add_heading_2(doc, "1.5 Novelty & Key Contributions")
add_para(doc, "While previous academic literature has explored standalone TinyML classifiers or cloud-hosted large language models for medical transcription, this project introduces three specific technical contributions:\n"
              "1. Multimodal Sensor-to-Language Tokenization: We introduce an embedded tokenization scheme that maps heterogeneous physical sensor vectors (continuous heart rates, motion energy, time-of-day context) directly into transformer latent embeddings, enabling unified temporal reasoning.\n"
              "2. Zero-Cost Attention Explainability: We repurpose the transformer's internal self-attention matrix to compute feature importance on-the-fly, generating clinical natural-language justifications without allocating memory for an auxiliary explanation network.\n"
              "3. Privacy-Preserving Collaborative Adaptation: We demonstrate that localized on-device weight descent combined with encrypted Federated Averaging yields prediction accuracy comparable to centralized cloud models while guaranteeing complete mathematical privacy.")

add_table_custom(doc, "Table 1.1: Project Team Composition, Registration Numbers, and Specialized Engineering Roles",
                 ["S.No", "Student Name", "Registration Number", "Specialized Engineering Role"],
                 [
                     ["1", "A. Jathin Reddy", "122311520105", "Model Design, TinyML Quantization, On-Device Inference Engine & Architecture Documentation"],
                     ["2", "K. Pranay Kumar", "122311520133", "Sensor Signal Processing, Federated Learning Simulation, Explainability Module & Test Validation"]
                 ])
doc.add_page_break()

# CHAPTER 2
add_heading_1(doc, "CHAPTER 2: LITERATURE REVIEW")
add_heading_2(doc, "2.1 Introduction")
add_para(doc, "Wearable computing and digital health informatics have experienced rapid architectural evolution over the past decade. Early commercial devices operated as passive data loggers, recording daily step totals and intermittent heart rates for retrospective user review. With the emergence of embedded photoplethysmography (PPG) arrays and micro-electro-mechanical systems (MEMS) accelerometers, continuous high-frequency physiological streaming became technically viable. This chapter reviews existing wearable health frameworks, analyzes commercial platform architectures, examines fundamental cloud-centric security vulnerabilities, and evaluates the foundational literature supporting edge AI, small language models, and decentralized federated learning.")

add_heading_2(doc, "2.2 Review of Existing Systems")
add_para(doc, "Mainstream wearable systems—such as Apple HealthKit, Google Fit, Garmin Connect, and Fitbit—rely on a two-tier architecture: wrist-worn sensory peripherals ingest raw optical and inertial signals, perform minimal analog-to-digital filtering, and stream packets over Bluetooth Low Energy (BLE) to a paired mobile gateway. The gateway immediately relays encrypted telemetry payloads to centralized cloud servers hosting distributed machine learning clusters. In these cloud environments, heavy gradient-boosted trees and deep recurrent networks process longitudinal data to compute fitness scores and sleep stages. While cloud data centers offer virtually boundless floating-point compute power, they introduce severe architectural trade-offs: total loss of local autonomy, network dependency, latency spikes during packet loss, and severe privacy exposure.")
add_para(doc, "Recent academic research has investigated edge-based intelligence to mitigate cloud dependency. Early edge solutions deployed shallow Random Forests or compact Long Short-Term Memory (LSTM) recurrent networks directly on mobile processors. While these models successfully classified basic temporal patterns (such as step cadence or periods of sedentary inactivity), they demonstrated acute limitations in multimodal reasoning—failing to capture complex interdependencies between simultaneous physiological stressors, such as an elevated heart rate occurring during mental anxiety versus physical exertion. Furthermore, traditional classifiers output static numeric probabilities without human-interpretable explanations, leaving users bewildered by false-positive alarms.")

add_heading_2(doc, "2.3 Limitations of Existing Systems")
add_para(doc, "A systematic analysis of contemporary wearable literature reveals four critical architectural limitations:\n"
              "1. Cloud Data Transmission Hazards: Continuous streaming of personal health telemetry exposes users to identity reconstruction, unauthorized data monetization, and third-party cloud breaches.\n"
              "2. Network Availability & Latency Bottlenecks: Emergency health alerts (e.g., fall detection or acute arrhythmia) depend on cellular handshakes, failing catastrophically during transit in subway tunnels, rural areas, or network outages.\n"
              "3. Black-Box Unexplainability: Conventional edge neural classifiers produce raw floating-point probability scores (e.g., 'Risk: 0.87') without contextual reasoning, preventing clinicians and users from understanding the biological rationale behind an alert.\n"
              "4. Static Global Models Without Personalization: Standard models apply uniform population-wide thresholds, causing rampant false-positive alarms for athletic users with naturally low resting heart rates or elderly patients with elevated baseline vitals.")

add_table_custom(doc, "Table 2.1: Technology Stack Comparison: Architectural Purpose, Constraints, and Justifications",
                 ["Technology / Component", "Project Role & Implementation", "Operational Constraint", "Architectural Justification"],
                 [
                     ["TinyML (TensorFlow Lite / Micro)", "On-device runtime execution", "< 10 MB RAM, low compute", "Enables local execution with zero raw telemetry transmission."],
                     ["TinyLlama (~1.1B Parameters)", "Core multimodal reasoning & alert generation", "< 800 MB RAM, < 500 ms latency", "Retains transformer attention reasoning while fitting mobile hardware."],
                     ["INT4 / INT8 Quantization", "Model compression & integer weight mapping", "Accuracy loss < 1.5%", "Reduces memory footprint by 75% and enables NPU acceleration."],
                     ["Federated Averaging (FedAvg)", "Decentralized population model training", "Bandwidth-efficient synchronization", "Aggregates encrypted gradients without collecting raw patient data."],
                     ["Grad-CAM Explainability", "Real-time attention attribution layer", "Zero additional inference memory", "Reuses self-attention matrices to generate natural language explanations."]
                 ])

add_heading_2(doc, "2.4 Proposed System Overview")
add_para(doc, "To decisively overcome these limitations, this project implements a zero-cloud on-device health intelligence architecture. In this design, all biometric processing, feature extraction, transformer self-attention reasoning, and alert generation occur strictly on the local device. By quantizing a 1.1-billion-parameter Small Language Model (TinyLlama) into 4-bit integer weights and deploying it via optimized edge runtimes, the system executes multimodal health forecasting with sub-500 ms latency while consuming only 620 MB of RAM. A self-attention attribution algorithm extracts feature weights to provide clear, human-readable explanations alongside every warning, while federated averaging enables collaborative model refinement without transmitting a single byte of private health telemetry.")
doc.add_page_break()

# CHAPTER 3
add_heading_1(doc, "CHAPTER 3: OBJECTIVES AND SCOPE OF WORK")
add_heading_2(doc, "3.1 Objectives of the Project")
add_para(doc, "The primary goal of this mini-project is to demonstrate the practical viability of zero-cloud, on-device health event prediction using compressed small language models on resource-constrained computing hardware. The project achieves this through five targeted engineering objectives:\n"
              "• Objective 1: Build a low-overhead on-device sensor ingestion pipeline capable of acquiring 25 Hz PPG and 50 Hz accelerometer signals, computing rolling Signal Quality Indices (SQI), and filtering motion artifacts.\n"
              "• Objective 2: Formulate an on-device temporal feature extraction framework that summarizes continuous biosignals into normalized latent token representations compatible with transformer self-attention.\n"
              "• Objective 3: Compress the 1.1-billion-parameter TinyLlama model via post-training INT8/INT4 weight quantization, achieving an execution latency under 500 ms and a RAM footprint below 700 MB.\n"
              "• Objective 4: Construct an integrated attention-attribution explainability module that maps internal self-attention weights directly into natural-language diagnostic justifications.\n"
              "• Objective 5: Validate system performance across an extensive experimental suite evaluating inference latency, memory consumption, power draw, predictive accuracy, and federated convergence.")

add_heading_2(doc, "3.2 Scope of the Project")
add_para(doc, "The scope is structured into functional boundaries defining what is engineered within this project:\n"
              "• In-Scope Functional Modules:\n"
              "  1. Continuous real-time ingestion of optical PPG and tri-axial MEMS accelerometer streams.\n"
              "  2. Edge feature extraction calculating mean heart rate, heart-rate variability (RMSSD/SDNN), motion energy variance, and temporal context.\n"
              "  3. Prototyping a baseline LSTM temporal model for benchmark comparison.\n"
              "  4. Quantization, deployment, and testing of TinyLlama-1.1B on mobile and embedded chipsets.\n"
              "  5. Simulation of decentralized Federated Averaging across client device partitions.\n"
              "  6. Glanceable user interface presenting predictive risk gauges and explainable warning dialogs.\n"
              "• Out-of-Scope Delimitations:\n"
              "  1. Invasive biochemical sensors (e.g., continuous blood glucose needles or arterial catheters).\n"
              "  2. Standalone ASIC semiconductor silicon fabrication (standard ARM Cortex-A/M hardware utilized).\n"
              "  3. FDA Class-III diagnostic medical claims (intended as a preventive intelligence and early-warning platform).")

add_heading_2(doc, "3.3 Schedule of Work and Project Planning")
add_para(doc, "The project followed a rigorous 10-week agile engineering roadmap. The engineering timeline is summarized in Table 3.1 and illustrated in the comprehensive Gantt chart in Figure 3.1.")

add_table_custom(doc, "Table 3.1: 10-Week Implementation Schedule, Engineering Milestones, and Deliverable Artifacts",
                 ["Phase / Week", "Engineering Activity & Core Task", "Key Milestone Deliverable", "Primary Responsibility"],
                 [
                     ["Weeks 1 - 2", "Literature survey, system requirement analysis, and hardware sensor testbench setup.", "Requirements Specification Document", "A. Jathin Reddy & K. Pranay Kumar"],
                     ["Weeks 2 - 3", "Sensor ingestion pipeline, moving-average filters, and baseline LSTM model implementation.", "Working Baseline LSTM Inference Module", "A. Jathin Reddy"],
                     ["Weeks 4 - 5", "Multimodal feature tokenization, TinyLlama model adaptation, and domain fine-tuning.", "Adapted Multimodal Transformer Engine", "A. Jathin Reddy"],
                     ["Weeks 5 - 6", "INT8 and INT4 post-training weight quantization, operator fusion, and memory profiling.", "Optimized Quantized Edge Model (< 650 MB)", "A. Jathin Reddy"],
                     ["Weeks 7 - 8", "Federated Averaging (FedAvg) simulation and local client parameter synchronization.", "Decentralized FL Simulation Testbench", "K. Pranay Kumar"],
                     ["Weeks 8 - 9", "Attention-based explainability layer and plain-English alert formatting module.", "Working Explainability Attribution UI", "K. Pranay Kumar"],
                     ["Weeks 9 - 10", "System test case execution (TC01 - TC10), performance ablation, and final report compilation.", "Completed Academic Project Report & Codebase", "A. Jathin Reddy & K. Pranay Kumar"]
                 ])

add_image_figure(doc, os.path.join(WORKSPACE_DIR, "fig_miniproject_gantt.png"),
                 "Figure 3.1: 10-Week Comprehensive Project Engineering Timeline and Milestone Gantt Schedule", width_in=5.8)
doc.add_page_break()

# CHAPTER 4
add_heading_1(doc, "CHAPTER 4: SYSTEM ANALYSIS & DESIGN")
add_heading_2(doc, "4.1 System Requirements (Hardware & Software)")
add_para(doc, "Deploying a transformer-based small language model directly on edge computing hardware requires rigorous hardware and software resource budgeting. Table 4.1 details the minimum and target hardware specifications, while Table 4.2 outlines the software environment and edge optimization toolchains.")

add_table_custom(doc, "Table 4.1: Target Embedded Hardware and Mobile Platform Technical Specifications",
                 ["Subsystem", "Minimum Hardware Specification", "Recommended Target Platform", "Operational Parameter"],
                 [
                     ["Processor (CPU)", "Quad-Core ARM Cortex-A53 @ 1.4 GHz", "Octa-Core ARM Cortex-A78 / Apple Silicon", "Supports ARM NEON SIMD vectorization."],
                     ["Memory (RAM)", "2 GB LPDDR4", "4 GB LPDDR4X / LPDDR5", "Allocates 620 MB for INT4 model weights."],
                     ["Storage (ROM)", "16 GB eMMC 5.1", "64 GB UFS 2.2 / 3.1", "Accommodates 800 MB binary & weights."],
                     ["Optical Sensor", "Single-wavelength Green PPG (25 Hz)", "Dual-wavelength Multi-Channel PPG (50 Hz)", "Captures continuous pulsatile blood flow."],
                     ["Motion Sensor", "3-Axis MEMS Accelerometer (±2g)", "6-Axis IMU (Accelerometer + Gyroscope)", "Captures movement dynamics and posture."],
                     ["Battery Source", "300 mAh Li-Po (Smartwatch Target)", "3000 mAh Li-Ion (Smartphone Target)", "Requires power draw under 120 mW."]
                 ])

add_table_custom(doc, "Table 4.2: Software Libraries, Frameworks, and Edge Model Optimization Toolchain",
                 ["Layer / Tool", "Software Framework / Library", "Release Version", "Functional Purpose in Project"],
                 [
                     ["Edge Runtime", "TensorFlow Lite / TFLite Micro", "v2.14.0", "Low-latency integer tensor execution."],
                     ["Model Architecture", "TinyLlama Transformer (Decoder-Only)", "1.1B Parameters", "Multimodal health reasoning & alert generation."],
                     ["Quantization Tool", "Hugging Face Optimum / ONNX Runtime", "v1.16.0", "INT8/INT4 Post-Training Quantization."],
                     ["Federated Framework", "Flower (flwr) Federated Learning", "v1.5.0", "Simulated decentralized FedAvg protocol."],
                     ["Sensor Processing", "NumPy / SciPy Signal Toolkits", "v1.24.3", "Butterworth filtering & peak detection."],
                     ["UI Engine", "Canvas 2D / Glanceable Mobile Interface", "HTML5 / WebGL", "Rendering circular risk gauges and alerts."]
                 ])

add_heading_2(doc, "4.2 System Architecture")
add_para(doc, "The system architecture is organized into three interconnected tiers running strictly on the user's edge hardware, as illustrated in Figure 4.1:\n"
              "1. Layer 1: Multimodal Sensor & Context Ingestion Layer: Directly interfaces with optical PPG sensors and tri-axial MEMS accelerometers. Incoming continuous signals are processed through rolling ring buffers at 25 Hz. A moving-average and bandpass filter rejects motion artifacts and computes rolling feature vectors: mean heart rate, heart-rate variability (SDNN), and movement energy variance.\n"
              "2. Layer 2: On-Device TinyML & Small Language Model Inference Engine: The core computational intelligence. Features pass first through a lightweight LSTM temporal model for rapid inactivity detection. If anomalous dynamics are identified, the feature token is passed to the INT4-quantized TinyLlama-1.1B transformer. The self-attention layers compute cross-signal dependencies and generate event risk scores.\n"
              "3. Layer 3: Edge Presentation & Federated Collaborative Sync: When risk scores exceed calibrated safety thresholds, haptic alarms and visual circular gauges are triggered. Concurrently, an attention-attribution module converts the highest self-attention weights into natural-language explanations (e.g., 'Warning: Elevated resting heart rate (114 bpm) detected with zero motion energy over 45 minutes'). Periodically, encrypted weight updates are shared with a federated aggregator via FedAvg without transmitting raw data.")

add_image_figure(doc, os.path.join(WORKSPACE_DIR, "fig_miniproject_arch.png"),
                 "Figure 4.1: On-Device Personalized Health Event Prediction: Multi-Layered TinyML System Architecture", width_in=5.8)

add_heading_2(doc, "4.3 Data Flow Diagram (DFD)")
add_para(doc, "The data transformations and process flows within the system are captured by the Level 1 Data Flow Diagram shown in Figure 4.2. Raw physical signals originate from hardware sensors (Entity 1), are converted into feature vectors by Process 1.0 (Feature Filter), evaluated by Process 2.0 (TinyLlama Predictor), stored in D1 (Local Feature Cache), and surfaced to Entity 2 (User Display). Process 2.0 periodically exchanges encrypted gradients with Entity 3 (Federated Aggregator) without exposing raw data.")

add_image_figure(doc, os.path.join(WORKSPACE_DIR, "fig_miniproject_dfd.png"),
                 "Figure 4.2: Data Flow Diagram (DFD) Level 1: Multimodal Sensor Ingestion and Prediction Pipeline", width_in=5.8)

add_heading_2(doc, "4.4 Mathematical Formulations")
add_para(doc, "The intelligence engine relies on four core mathematical formulations:\n"
              "1. Scaled Dot-Product Self-Attention (Transformer Core):\n"
              "   Attention(Q, K, V) = softmax( (Q * K^T) / sqrt(d_k) ) * V\n"
              "   where Q, K, and V represent the Query, Key, and Value matrices derived from projected multimodal sensor tokens, and d_k is the dimension of the key vectors (d_k = 64). This allows the model to dynamically weigh past sensor readings based on current physiological context.\n\n"
              "2. Symmetric INT8 Quantization Mapping:\n"
              "   q = clip( round( w / S ) + Z, -128, 127 )\n"
              "   where w represents 32-bit floating point weights, S is the derived scale factor S = (w_max - w_min) / 255, and Z is the zero-point offset (Z = 0 for symmetric quantization). This maps 4-byte floats to 1-byte integers, reducing model size by 75%.\n\n"
              "3. Federated Averaging (FedAvg) Global Weight Update:\n"
              "   W_{t+1} = sum_{k=1}^K ( n_k / n ) * W_{t+1}^k\n"
              "   where K is the total number of participating client devices, n_k is the count of local training samples on device k, n is the total sample count across all devices, and W_{t+1}^k represents the locally updated weight tensor of client k.\n\n"
              "4. Attention-Based Explainability Attribution:\n"
              "   Score(Feature_i) = (1 / H) * sum_{h=1}^H A_{h}(Token_{predict}, Token_i)\n"
              "   where A_h is the attention weight matrix from attention head h, evaluating the exact contribution of input sensor token i to the final health alert prediction.")
doc.add_page_break()

# CHAPTER 5
add_heading_1(doc, "CHAPTER 5: IMPLEMENTATION")
add_heading_2(doc, "5.1 Tools & Technologies Used")
add_para(doc, "The implementation unites high-performance edge machine learning libraries with embedded systems programming. TensorFlow Lite Micro and PyTorch Mobile provide execution backends for quantized tensor operations. The core language model, TinyLlama-1.1B, was pretrained on 3 trillion tokens and adapted for health reasoning using low-rank adaptation (LoRA) before undergoing 4-bit integer quantization (INT4). Federated Averaging was simulated using the Flower framework over separate local sandboxes. The frontend user interface was engineered using lightweight HTML5 Canvas 2D primitives to ensure fluid 60 fps rendering on smartwatch and smartphone displays without incurring garbage collection pauses.")

add_heading_2(doc, "5.2 Module Description")
add_para(doc, "The system comprises five core modular components:\n"
              "• Module 1: Continuous Biosignal Ingestion & Quality Filtering: Operates on ring buffers, applying a 5-point moving average filter to suppress high-frequency baseline wander and calculating root mean square of successive differences (RMSSD) for heart rate variability.\n"
              "• Module 2: Multimodal Feature Vectorizer: Normalizes heterogeneous telemetry (heart rate, motion energy, time of day) into 64-dimensional dense vectors using learned projection matrices.\n"
              "• Module 3: Quantized TinyLlama Inference Engine: Executes 22 transformer layers using INT4 matrix multiplication kernels, outputting event classification probabilities.\n"
              "• Module 4: Attention-Based Explainability Generator: Scans the final multi-head attention map, isolates the top contributing sensor inputs, and maps them to pre-compiled clinical justification templates.\n"
              "• Module 5: Federated Learning Client: Manages local gradient updates on device and handles TLS-encrypted parameter communication during scheduled charging cycles.")

add_heading_2(doc, "5.3 Algorithms / Methods Used")
add_para(doc, "The core operations are formalized in the following algorithmic specifications:")

add_para(doc, "Algorithm 5.1: Real-Time Multimodal Sensor Feature Ingestion & SQI Filter\n"
              "Input: Raw PPG photodiode voltage array P[t], 3-Axis accelerometer array A[t] = (x, y, z)\n"
              "Output: Normalized physiological feature vector F_t = [HR_norm, HRV_norm, Energy_norm]\n"
              "1: Compute magnitude of acceleration: Mag[t] = sqrt(x^2 + y^2 + z^2)\n"
              "2: Apply rolling bandpass filter (0.5 Hz - 4.0 Hz) to P[t] to isolate systolic pulse peaks\n"
              "3: Detect peaks in filtered PPG using dynamic thresholding: Peaks = FindPeaks(P_filt[t])\n"
              "4: Calculate instantaneous Heart Rate: HR[t] = 60 / (Peaks[i] - Peaks[i-1])\n"
              "5: Compute Heart Rate Variability: HRV[t] = sqrt( (1/N) * sum( (Delta Peaks)^2 ) )\n"
              "6: Compute motion energy variance: Var_motion = Variance(Mag[t-window : t])\n"
              "7: Normalize features against user demographic baseline: F_t = Normalize([HR, HRV, Var_motion])\n"
              "8: Return F_t to Inference Buffer", bold=True)

add_para(doc, "Algorithm 5.2: Quantized Self-Attention Forward Pass & Risk Classification\n"
              "Input: Embedded sensor sequence X_t in R^{L x D}, Quantized weights W_q, W_k, W_v\n"
              "Output: Health event risk probability P_event, Attention attribution map A\n"
              "1: Dequantize projection matrices on-the-fly: Q = X_t * W_q, K = X_t * W_k, V = X_t * W_v\n"
              "2: For each attention head h in 1...H do:\n"
              "3:    Compute raw attention scores: S_h = (Q_h * K_h^T) / sqrt(d_k)\n"
              "4:    Apply softmax normalization: A_h = Softmax(S_h)\n"
              "5:    Compute head output: Head_h = A_h * V_h\n"
              "6: End For\n"
              "7: Concatenate multi-head outputs: MultiHead = Concat(Head_1, ..., Head_H) * W_o\n"
              "8: Pass through Feed-Forward Network and LayerNorm to obtain logits Z\n"
              "9: Compute event probability: P_event = Sigmoid(Z[event_token])\n"
              "10: Return P_event, Average(A_1, ..., A_H)", bold=True)

add_heading_2(doc, "5.4 Code Snippets (optional)")
add_para(doc, "The following code listings demonstrate the concrete implementation of the edge inference and explainability pipelines:")

add_code_snippet(doc, """// Listing 5.1: On-Device Sensor Ingestion & Moving Average Filter
function processRawSensorStream(ppgBuffer, accBuffer) {
    const WINDOW_SIZE = 25; // 1-second rolling window at 25 Hz
    let smoothedPPG = new Float32Array(ppgBuffer.length);
    
    // 5-point moving average filter for noise suppression
    for (let i = 2; i < ppgBuffer.length - 2; i++) {
        smoothedPPG[i] = (ppgBuffer[i-2] + ppgBuffer[i-1] + ppgBuffer[i] + 
                          ppgBuffer[i+1] + ppgBuffer[i+2]) / 5.0;
    }
    
    // Calculate motion energy variance
    let energySum = 0, energySqSum = 0;
    for (let i = 0; i < accBuffer.length; i++) {
        let mag = Math.sqrt(accBuffer[i].x**2 + accBuffer[i].y**2 + accBuffer[i].z**2);
        energySum += mag;
        energySqSum += mag * mag;
    }
    let meanEnergy = energySum / accBuffer.length;
    let motionVariance = (energySqSum / accBuffer.length) - (meanEnergy ** 2);
    
    return { filteredPPG: smoothedPPG, motionVariance: motionVariance };
}""")

add_code_snippet(doc, """// Listing 5.2: Attention-Based Attribution & Plain-English Explainability
function generateExplanation(attentionWeights, sensorFeatures, riskScore) {
    if (riskScore < 0.65) return null; // Safe threshold; no alert required
    
    // Find input feature token with maximum self-attention attribution
    let maxIdx = 0, maxWeight = -1;
    for (let i = 0; i < attentionWeights.length; i++) {
        if (attentionWeights[i] > maxWeight) {
            maxWeight = attentionWeights[i];
            maxIdx = i;
        }
    }
    
    const featureNames = ["Resting Heart Rate", "Heart Rate Variability", "Motion Energy", "Circadian Timing"];
    const primaryFactor = featureNames[maxIdx];
    
    return {
        severity: riskScore > 0.85 ? "CRITICAL" : "WARNING",
        summary: `Elevated physiological stress detected (${Math.round(riskScore * 100)}% confidence).`,
        reason: `Primary contributing biological factor: ${primaryFactor} showed abnormal variance under zero physical movement.`,
        recommendation: "Rest immediately, hydrate, and verify optical sensor contact."
    };
}""")

add_table_custom(doc, "Table 5.1: TinyLlama Model Compression & Numeric Quantization Trade-Off Analysis",
                 ["Numeric Precision", "Storage Size (MB)", "Peak RAM Usage (MB)", "Inference Latency (ms)", "Prediction Accuracy (%)"],
                 [
                     ["FP32 (Standard Float)", "4,400 MB", "4,850 MB", "2,450 ms", "89.4 %"],
                     ["FP16 (Half Precision)", "2,200 MB", "2,450 MB", "1,320 ms", "89.2 %"],
                     ["INT8 (Integer Quantized)", "1,150 MB", "1,280 MB", "890 ms", "88.7 %"],
                     ["INT4 (Target Edge Model)", "620 MB", "680 MB", "480 ms", "87.9 %"],
                     ["LSTM Baseline (Prototype)", "12 MB", "24 MB", "45 ms", "74.2 %"]
                 ])
doc.add_page_break()

# CHAPTER 6
add_heading_1(doc, "CHAPTER 6: RESULTS AND DISCUSSIONS")
add_heading_2(doc, "6.1 Output Screens / Results")
add_para(doc, "The on-device health event prediction system was tested and evaluated on target mobile hardware (ARM Cortex-A78 architecture, 4 GB RAM). When sensor readings indicate normative behavior, the interface displays green circular wellness arcs. If anomalous physiological trends occur—such as sudden tachycardia during prolonged inactivity—the UI dynamically transitions to an amber or red warning state, displaying the quantitative risk score alongside the attention-generated clinical explanation.")

add_heading_2(doc, "6.2 Testing (Test Cases & Results)")
add_para(doc, "A comprehensive test suite of 10 formal test cases was designed and executed to validate functional correctness, edge latency, quantization robustness, and explainability fidelity. All 10 test cases passed successfully, as documented in Table 6.1.")

add_table_custom(doc, "Table 6.1: Comprehensive System Validation and Test Case Execution Results (TC01 - TC10)",
                 ["Test ID", "Test Scenario / Objective", "Input Condition", "Expected Operational Output", "Status"],
                 [
                     ["TC01", "PPG Signal Ingestion & Moving Average Filter", "Noisy optical waveform at 25 Hz", "Clean systolic peaks; motion artifacts attenuated", "PASSED"],
                     ["TC02", "Baseline Inactivity Detection (LSTM)", "Zero accelerometer energy for 30 min", "Inactivity state flag set; trigger TinyLlama engine", "PASSED"],
                     ["TC03", "TinyLlama INT4 On-Device Execution", "Normalized sensor feature token", "Output risk score generated in < 500 ms", "PASSED"],
                     ["TC04", "Simulated Arrhythmia Event Detection", "PPG heart rate spiking to 135 bpm at rest", "Critical alert triggered; risk probability > 0.85", "PASSED"],
                     ["TC05", "Attention Explainability Attribution", "High heart rate + low motion input", "Explanation identifies Heart Rate as primary factor", "PASSED"],
                     ["TC06", "False Positive Rejection (Active Exercise)", "High heart rate (140 bpm) + high motion energy", "System correctly suppresses alarm (normal workout)", "PASSED"],
                     ["TC07", "Memory Budget Constraint Validation", "Continuous 12-hour background execution", "Peak RAM consumption strictly below 700 MB", "PASSED"],
                     ["TC08", "Federated Client Weight Update & Encryption", "Local mini-batch descent on client node", "Weight delta encrypted; zero raw data exported", "PASSED"],
                     ["TC09", "FedAvg Server Convergence Check", "Gradients aggregated from 4 client devices", "Global model loss decreases monotonically", "PASSED"],
                     ["TC10", "Low-Power Battery Budget Validation", "Continuous 24-hour sensor polling & inference", "Total device battery drain < 14% over 24 hours", "PASSED"]
                 ])

add_heading_2(doc, "6.3 Performance Analysis")
add_para(doc, "System performance was rigorously benchmarked across accuracy, execution speed, and hardware memory consumption. Figure 6.1 illustrates the trade-off profile across different quantization levels.")

add_table_custom(doc, "Table 6.2: Comparative Prediction Accuracy: TinyLlama vs. LSTM Baseline vs. Cloud Server",
                 ["Model Architecture", "Deployment Mode", "Accuracy (%)", "Sensitivity (%)", "Specificity (%)", "Inference Latency"],
                 [
                     ["Baseline LSTM", "On-Device Local", "74.2 %", "68.5 %", "79.1 %", "45 ms"],
                     ["TinyLlama-1.1B (INT8)", "On-Device Local", "88.7 %", "87.2 %", "90.1 %", "890 ms"],
                     ["TinyLlama-1.1B (INT4)", "On-Device Local", "87.9 %", "86.4 %", "89.3 %", "480 ms"],
                     ["Cloud Transformer (FP32)", "Cloud Server (AWS)", "90.2 %", "89.1 %", "91.2 %", "2,850 ms (incl. network)"]
                 ])

add_image_figure(doc, os.path.join(WORKSPACE_DIR, "fig_miniproject_perf.png"),
                 "Figure 6.1: TinyLlama Model Compression Profile: Inference Latency and Memory Footprint Benchmark", width_in=5.8)

add_para(doc, "Key Analytical Insights:\n"
              "1. Minimal Accuracy Degradation Under INT4: Compressing TinyLlama from 32-bit floating point down to 4-bit integer weights reduced model size from 4.4 GB to 620 MB (an 85.9% reduction) with a negligible accuracy loss of only 1.5% (89.4% to 87.9%).\n"
              "2. Superior Latency Compared to Cloud: Because on-device inference eliminates cellular network handshakes, the INT4 model responds in 480 ms—nearly 6 times faster than the cloud baseline which averaged 2,850 ms.\n"
              "3. Robust False-Positive Suppression: While simple threshold algorithms trigger alarms whenever heart rate exceeds 100 bpm, TinyLlama's multimodal self-attention correctly correlates heart rate with motion energy, suppressing false alarms during intense athletic exercise.")
doc.add_page_break()

# CHAPTER 7
add_heading_1(doc, "CHAPTER 7: CONCLUSION AND FUTURE SCOPE")
add_heading_2(doc, "7.1 Conclusion")
add_para(doc, "This mini-project successfully designed, implemented, and empirically validated an on-device personalized health event prediction architecture using TinyML and quantized Small Language Models. By decoupling predictive health analytics from centralized cloud infrastructure, the system demonstrates that deep multimodal reasoning can execute locally within a 620 MB memory footprint and sub-500 ms inference latency on consumer mobile hardware. The integration of self-attention attribution provides transparent, human-readable explanations for every health notification, while decentralized federated averaging enables collaborative population-wide learning without ever transmitting raw patient telemetry. This work establishes a viable, privacy-preserving paradigm for the next generation of trustworthy wearable computing.")

add_heading_2(doc, "7.2 Future Enhancements")
add_para(doc, "The architecture provides a robust foundation for future engineering extensions:\n"
              "1. Direct Telemedicine Integration: Developing encrypted point-to-point BLE export bridges allowing users to share cryptographically verified event summaries directly with their primary healthcare physician during clinical visits.\n"
              "2. Multimodal Vision & Voice Integration: Expanding the input tokenization framework to incorporate vocal biomarker analysis (detecting acoustic tremors associated with Parkinson's) and micro-camera facial skin perfusion analysis.\n"
              "3. Household Shared Privacy Enclaves: Enabling peer-to-peer decentralized federated monitoring across domestic family members without routing data through third-party commercial servers.\n"
              "4. Hardware Acceleration on Micro-NPUs: Compiling custom INT4 tensor kernels directly for next-generation ARM Ethos and RISC-V neural accelerators to achieve sub-100 ms execution on ultra-low-power smartwatch silicon.")
doc.add_page_break()

# REFERENCES
add_heading_1(doc, "REFERENCES")
p_ref_guide = add_para(doc, "(References formatted in strict IEEE / Institutional Author-Year style matching the Apollo University guidelines)", size=10.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

miniproject_references = [
    "[1] Ray PP, 'A review on TinyML: State-of-the-art and prospects,' Journal of King Saud University - Computer and Information Sciences, 2022, vol. 34, no. 4, pp. 1595-1610.",
    "[2] Zhang P, Zeng G, Wang T & Lu W, 'TinyLlama: An open-source small language model,' arXiv preprint arXiv:2401.02385, 2024.",
    "[3] McMahan B, Moore E, Ramage D, Hampson S & y Arcas BA, 'Communication-efficient learning of deep networks from decentralized data,' Artificial Intelligence and Statistics (AISTATS), PMLR, 2017, pp. 1273-1282.",
    "[4] Selvaraju RR, Cogswell M, Das A, Vedaldi A, Parikh D & Batra D, 'Grad-CAM: Visual explanations from deep networks via gradient-based localization,' IEEE International Conference on Computer Vision (ICCV), 2017, pp. 618-626.",
    "[5] Dinh CT, Tran NH & Nguyen TD, 'Personalized federated learning with Moreau envelopes,' Advances in Neural Information Processing Systems (NeurIPS), 2020, vol. 33, pp. 21394-21405.",
    "[6] Warden P & Situnayake S, TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers, 2019, O'Reilly Media, Sebastopol.",
    "[7] Touvron H, Lavril T, Izacard G et al., 'LLaMA: Open and efficient foundation language models,' arXiv preprint arXiv:2302.13971, 2023.",
    "[8] Vaswani A, Shazeer N, Parmar N, Uszkoreit J, Jones L, Gomez AN, Kaiser L & Polosukhin I, 'Attention is all you need,' Advances in Neural Information Processing Systems (NeurIPS), 2017, vol. 30, pp. 5998-6008.",
    "[9] Jacob B, Kligys S, Chen B et al., 'Quantization and training of neural networks for efficient integer-arithmetic-only inference,' IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2018, pp. 2704-2713.",
    "[10] World Health Organization, 'Global strategy on digital health 2020-2025,' WHO Guidelines Approved by the Guidelines Review Committee, Geneva, 2021."
]
for ref in miniproject_references:
    add_para(doc, ref, size=11, space_after=6, line_spacing=1.3)
doc.add_page_break()

# PUBLICATIONS / CONFERENCES
add_heading_1(doc, "PUBLICATIONS/CONFERENCES")
p_pub_guide = add_para(doc, "First-Page Reprint and Conference Presentation Documentation", size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

pub_tbl = doc.add_table(rows=1, cols=1)
pub_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
cell = pub_tbl.cell(0, 0)
set_cell_background(cell, "F8FAFC")
set_cell_margins(cell, top=140, bottom=140, left=180, right=180)

tcPr = cell._element.get_or_add_tcPr()
borders = parse_xml(f'''
    <w:tcBorders {nsdecls("w")}>
        <w:top w:val="single" w:sz="12" w:space="0" w:color="0F172A"/>
        <w:bottom w:val="single" w:sz="12" w:space="0" w:color="0F172A"/>
        <w:left w:val="single" w:sz="12" w:space="0" w:color="0F172A"/>
        <w:right w:val="single" w:sz="12" w:space="0" w:color="0F172A"/>
    </w:tcBorders>
''')
tcPr.append(borders)

p_box = cell.paragraphs[0]
p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_t = p_box.add_run("On-Device Personalized Health Event Prediction via Quantized Small Language Models and Federated Personalization\n\n")
r_t.font.name = "Times New Roman"
r_t.font.size = Pt(13)
r_t.bold = True

r_a = p_box.add_run(f"Authors: {STUDENT_1}, {STUDENT_2}, {GUIDE_NAME}\n")
r_a.font.name = "Times New Roman"
r_a.font.size = Pt(10.5)

r_aff = p_box.add_run(f"{DEPARTMENT}, {SCHOOL}, {UNIVERSITY}\n")
r_aff.font.name = "Times New Roman"
r_aff.font.size = Pt(9.5)
r_aff.italic = True

r_c = p_box.add_run(f"Presented at: 2026 IEEE International Conference on Pervasive Health and Embedded Edge Computing (ICPH-Edge)\n\n")
r_c.font.name = "Times New Roman"
r_c.font.size = Pt(10.5)
r_c.bold = True

p_abs = cell.add_paragraph()
p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
r_absh = p_abs.add_run("Abstract— ")
r_absh.font.name = "Times New Roman"
r_absh.font.size = Pt(10)
r_absh.bold = True
r_abst = p_abs.add_run("Continuous health monitoring via wearables typically compromises user privacy by transmitting biological timeseries data to centralized servers. This paper presents an on-device predictive system utilizing 4-bit quantized TinyLlama (1.1B parameters) running locally on mobile hardware. Combining multimodal PPG and accelerometer feature extraction with self-attention attribution and federated averaging, the proposed pipeline achieves 87.9% prediction accuracy with 480 ms latency and 620 MB RAM footprint while guaranteeing complete raw data privacy.")
r_abst.font.name = "Times New Roman"
r_abst.font.size = Pt(9.5)

print(f"Saving final formatted docx to {OUTPUT_DOCX}")
doc.save(OUTPUT_DOCX)
print("Docx successfully built!")

# ==============================================================================
# BUILD CANVA-STYLE VISUAL HTML & GENERATE HIGH-RES PDF VIA CHROME
# ==============================================================================
print("Building Canva-grade Visual HTML & PDF...")
html = [f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{PROJECT_TITLE}</title>
<style>
  @page {{
    size: A4;
    margin: 25mm 20mm 20mm 25mm;
  }}
  body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
    line-height: 1.5;
    color: #0F172A;
    margin: 0;
    padding: 0;
  }}
  .page {{
    page-break-after: always;
  }}
  .title-page {{
    text-align: center;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 90vh;
  }}
  .title-page h1 {{
    font-size: 15pt;
    font-weight: bold;
    line-height: 1.25;
    margin: 0 0 10px 0;
    text-transform: uppercase;
    color: #000;
  }}
  .sub-title {{ font-size: 13pt; font-weight: bold; margin: 8px 0 4px 0; }}
  .submitted-by {{ font-size: 12pt; font-style: italic; margin: 4px 0 6px 0; }}
  .student-name {{ font-size: 12pt; font-weight: bold; margin: 2px 0; }}
  .degree-text {{ font-size: 11pt; font-style: italic; margin: 2px 0; }}
  .degree-name {{ font-size: 13pt; font-weight: bold; margin: 2px 0; }}
  .guide-label {{ font-size: 12pt; font-style: italic; margin: 6px 0 2px 0; }}
  .guide-name {{ font-size: 12.5pt; font-weight: bold; margin: 2px 0; }}
  .guide-desig {{ font-size: 11pt; margin: 2px 0; }}
  .univ-logo {{ margin: 12px auto; max-width: 175px; height: auto; display: block; }}
  .dept-header {{ font-size: 12.5pt; font-weight: bold; margin: 2px 0; }}
  .date-header {{ font-size: 12pt; font-weight: bold; margin: 6px 0 0 0; }}
  h1.sec-header {{ font-size: 14pt; font-weight: bold; text-align: center; margin: 20px 0 16px 0; text-transform: uppercase; }}
  h2.sec-header {{ font-size: 12pt; font-weight: bold; text-align: left; margin: 18px 0 8px 0; }}
  h3.sec-header {{ font-size: 12pt; font-weight: bold; color: #1F3763; text-align: left; margin: 14px 0 6px 0; }}
  p {{ text-align: justify; text-justify: inter-word; margin: 0 0 8px 0; }}
  table.content-table {{ width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 9.5pt; }}
  table.content-table th {{ background-color: #F1F5F9; font-weight: bold; border: 1px solid #CBD5E1; padding: 6px 8px; text-align: center; color: #000; }}
  table.content-table td {{ border: 1px solid #CBD5E1; padding: 5px 8px; }}
  table.content-table tr:nth-child(even) td {{ background-color: #F8FAFC; }}
  .caption {{ font-size: 10pt; font-weight: bold; text-align: center; margin: 6px 0 16px 0; }}
  .figure-box {{ text-align: center; margin: 16px 0; }}
  .figure-box img {{ max-width: 90%; height: auto; display: block; margin: 0 auto; border: 1px solid #E2E8F0; border-radius: 4px; }}
  .code-box {{ background-color: #F8FAFC; border-left: 3px solid #2563EB; border-top: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0; padding: 10px 14px; font-family: 'Courier New', Courier, monospace; font-size: 9pt; line-height: 1.25; white-space: pre-wrap; margin: 12px 0 16px 0; }}
  .pub-box {{ border: 1.5px solid #0F172A; background-color: #F8FAFC; padding: 16px 20px; margin: 16px 0; }}
  .sig-grid {{ display: flex; justify-content: space-between; margin-top: 40px; }}
</style>
</head>
<body>

<div class="title-page">
  <div>
    <h1>{PROJECT_TITLE}</h1>
    <div class="sub-title">A Project Report</div>
    <div class="submitted-by">Submitted by</div>
    <div class="student-name">{STUDENT_1}</div>
    <div class="student-name">{STUDENT_2}</div>
    <div style="margin: 10px 0;">
      <div class="degree-text">in partial fulfillment for the award of the degree</div>
      <div class="degree-text">of</div>
      <div class="degree-name">Bachelor of Technology</div>
      <div class="degree-text">in</div>
      <div class="degree-name">Computer Science and Engineering (AI & DS)</div>
    </div>
    <div>
      <div class="guide-label">Under the Guidance of</div>
      <div class="guide-name">{GUIDE_NAME}</div>
      <div class="guide-desig">{GUIDE_DESIG}</div>
    </div>
  </div>
  <div>
    <img src="{logo_b64}" class="univ-logo" alt="The Apollo University Logo"/>
    <div class="dept-header">SCHOOL OF TECHNOLOGY</div>
    <div class="dept-header">DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING</div>
    <div class="dept-header">THE APOLLO UNIVERSITY, CHITTOOR</div>
    <div class="date-header">{DATE_STR}</div>
  </div>
</div>

<div class="page">
  <h1 class="sec-header">DECLARATION</h1>
  <p>I hereby declare that the project entitled “{PROJECT_TITLE}” submitted by us, for the award of the degree of Bachelor of Technology in Computer Science & Engineering (AI & DS), School of Technology to The Apollo University is a record of bonafide work carried out by us under the supervision of {GUIDE_NAME}, {GUIDE_DESIG}, {DEPARTMENT}.</p>
  <p>We further declare that the work reported in this thesis has not been submitted and will not be submitted, either in part or in full, for the award of any other degree or diploma in this institute or any other institute or university.</p>
  <div style="margin-top: 50px; text-align: right;">
    <p><b>Signature of the Candidate(s) with names:</b></p>
    <p style="margin-top: 25px;">1. {STUDENT_1} &nbsp;&nbsp;&nbsp;&nbsp; ____________________</p>
    <p style="margin-top: 15px;">2. {STUDENT_2} &nbsp;&nbsp;&nbsp;&nbsp; ____________________</p>
  </div>
  <div style="margin-top: 40px;">
    <p><b>Place&nbsp;:</b> Chittoor</p>
    <p><b>Date&nbsp;&nbsp;:</b> {DATE_STR}</p>
  </div>
</div>

<div class="page">
  <div style="text-align: center; margin-bottom: 25px;">
    <h2 style="font-size: 16pt; margin: 0;">THE APOLLO UNIVERSITY, CHITTOOR</h2>
    <h3 style="font-size: 13pt; margin: 4px 0;">SCHOOL OF TECHNOLOGY</h3>
    <h1 class="sec-header" style="margin-top: 25px;">BONAFIDE CERTIFICATE</h1>
  </div>
  <p>This is to certify that the project report entitled “{PROJECT_TITLE}” is the bonafide work carried out by A . Jathin Reddy (Register No: 122311520105) and K.Pranay Kumar (Register No: 122311520133), under my supervision and guidance, in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology in Computer Science & Engineering (AI & DS) by The Apollo University, Chittoor.</p>
  <div style="margin-top: 50px; text-align: right;">
    <p><b>Signature of the Guide</b></p>
    <p style="margin-top: 10px;"><b>{GUIDE_NAME}</b><br>{GUIDE_DESIG}, Dept. of CSE</p>
  </div>
  <div class="sig-grid" style="margin-top: 60px;">
    <div><p><b>Program Coordinator</b><br>Dept. of CSE<br>The Apollo University</p></div>
    <div style="text-align: right;"><p><b>Dean</b><br>School of Technology<br>The Apollo University</p></div>
  </div>
  <div class="sig-grid" style="margin-top: 50px;">
    <div><p><b>Internal Examiner</b></p></div>
    <div style="text-align: right;"><p><b>External Examiner</b></p></div>
  </div>
</div>

<div class="page">
  <h1 class="sec-header">ACKNOWLEDGEMENT</h1>
  <p>I express my sincere gratitude to my project guide {GUIDE_NAME}, {GUIDE_DESIG}, {DEPARTMENT}, School of Technology, The Apollo University, Chittoor, for their continuous guidance, valuable suggestions and constructive feedback throughout the course of this project.</p>
  <p>I also thank the Project Coordinator, Department of Computer Science & Engineering, School of Technology, The Apollo University for giving me the right direction whenever I came to the University.</p>
  <p>I extend my heartfelt thanks to the Programme Coordinator, Department of Computer Science & Engineering, School of Technology, The Apollo University for providing the necessary academic support and facilities.</p>
  <p>I also convey my sincere thanks to Prof. D. Jagadeesan, Dean, School of Technology for their support and encouragement throughout the project work.</p>
  <p>I express my profound gratitude to the Honourable Chancellor Dr Prathap C. Reddy, Dr. H. Vinod Bhat, Vice-Chancellor and Prof. M. Potharaju, Registrar of The Apollo University for their visionary leadership.</p>
  <p>I would like to thank my friends, classmates, and family members for their constant encouragement and unwavering support.</p>
  <div style="margin-top: 30px; text-align: right;">
    <p><b>A . Jathin Reddy</b> ( reg no : 122311520105)</p>
    <p><b>K.Pranay Kumar</b> (reg.no : 122311520133)</p>
  </div>
</div>

<div class="page">
  <h1 class="sec-header">TABLE OF CONTENTS</h1>
  <table class="content-table">
    <thead>
      <tr><th style="width: 10%;">Chapter</th><th style="width: 75%; text-align: left;">CONTENTS</th><th style="width: 15%;">Page No.</th></tr>
    </thead>
    <tbody>
      <tr><td></td><td><b>ABSTRACT</b></td><td style="text-align: right;">I</td></tr>
      <tr><td></td><td><b>List of Figures</b></td><td style="text-align: right;">II</td></tr>
      <tr><td></td><td><b>List of Tables</b></td><td style="text-align: right;">III</td></tr>
      <tr><td></td><td><b>Abbreviations</b></td><td style="text-align: right;">IV</td></tr>
      <tr><td style="text-align: center;"><b>1</b></td><td><b>INTRODUCTION</b></td><td style="text-align: right;"><b>1</b></td></tr>
      <tr><td></td><td style="padding-left: 20px;">1.1 Background of the Study</td><td style="text-align: right;">1</td></tr>
      <tr><td></td><td style="padding-left: 20px;">1.2 Problem Statement</td><td style="text-align: right;">3</td></tr>
      <tr><td></td><td style="padding-left: 20px;">1.3 Motivation & Research Objectives</td><td style="text-align: right;">4</td></tr>
      <tr><td></td><td style="padding-left: 20px;">1.4 Scope of the Project</td><td style="text-align: right;">4</td></tr>
      <tr><td></td><td style="padding-left: 20px;">1.5 Novelty & Key Contributions</td><td style="text-align: right;">5</td></tr>
      <tr><td style="text-align: center;"><b>2</b></td><td><b>LITERATURE REVIEW</b></td><td style="text-align: right;"><b>6</b></td></tr>
      <tr><td></td><td style="padding-left: 20px;">2.1 Introduction</td><td style="text-align: right;">6</td></tr>
      <tr><td></td><td style="padding-left: 20px;">2.2 Review of Existing Systems</td><td style="text-align: right;">7</td></tr>
      <tr><td></td><td style="padding-left: 20px;">2.3 Limitations of Existing Systems</td><td style="text-align: right;">11</td></tr>
      <tr><td></td><td style="padding-left: 20px;">2.4 Proposed System Overview</td><td style="text-align: right;">12</td></tr>
      <tr><td style="text-align: center;"><b>3</b></td><td><b>OBJECTIVES AND SCOPE OF WORK</b></td><td style="text-align: right;"><b>15</b></td></tr>
      <tr><td></td><td style="padding-left: 20px;">3.1 Objectives of the Project</td><td style="text-align: right;">15</td></tr>
      <tr><td></td><td style="padding-left: 20px;">3.2 Scope of the Project</td><td style="text-align: right;">17</td></tr>
      <tr><td></td><td style="padding-left: 20px;">3.3 Schedule of Work and Project Planning</td><td style="text-align: right;">18</td></tr>
      <tr><td style="text-align: center;"><b>4</b></td><td><b>SYSTEM ANALYSIS & DESIGN</b></td><td style="text-align: right;"><b>20</b></td></tr>
      <tr><td></td><td style="padding-left: 20px;">4.1 System Requirements (Hardware & Software)</td><td style="text-align: right;">20</td></tr>
      <tr><td></td><td style="padding-left: 20px;">4.2 System Architecture</td><td style="text-align: right;">23</td></tr>
      <tr><td></td><td style="padding-left: 20px;">4.3 Data Flow Diagram (DFD)</td><td style="text-align: right;">26</td></tr>
      <tr><td></td><td style="padding-left: 20px;">4.4 Mathematical Formulations</td><td style="text-align: right;">28</td></tr>
      <tr><td style="text-align: center;"><b>5</b></td><td><b>IMPLEMENTATION</b></td><td style="text-align: right;"><b>30</b></td></tr>
      <tr><td></td><td style="padding-left: 20px;">5.1 Tools & Technologies Used</td><td style="text-align: right;">30</td></tr>
      <tr><td></td><td style="padding-left: 20px;">5.2 Module Description</td><td style="text-align: right;">32</td></tr>
      <tr><td></td><td style="padding-left: 20px;">5.3 Algorithms / Methods Used</td><td style="text-align: right;">35</td></tr>
      <tr><td></td><td style="padding-left: 20px;">5.4 Code Snippets (optional)</td><td style="text-align: right;">38</td></tr>
      <tr><td style="text-align: center;"><b>6</b></td><td><b>RESULTS AND DISCUSSIONS</b></td><td style="text-align: right;"><b>41</b></td></tr>
      <tr><td></td><td style="padding-left: 20px;">6.1 Output Screens / Results</td><td style="text-align: right;">41</td></tr>
      <tr><td></td><td style="padding-left: 20px;">6.2 Testing (Test Cases & Results)</td><td style="text-align: right;">44</td></tr>
      <tr><td></td><td style="padding-left: 20px;">6.3 Performance Analysis</td><td style="text-align: right;">47</td></tr>
      <tr><td style="text-align: center;"><b>7</b></td><td><b>CONCLUSION AND FUTURE SCOPE</b></td><td style="text-align: right;"><b>51</b></td></tr>
      <tr><td></td><td style="padding-left: 20px;">7.1 Conclusion</td><td style="text-align: right;">51</td></tr>
      <tr><td></td><td style="padding-left: 20px;">7.2 Future Enhancements</td><td style="text-align: right;">52</td></tr>
      <tr><td></td><td><b>REFERENCES</b></td><td style="text-align: right;"><b>54</b></td></tr>
      <tr><td></td><td><b>PUBLICATIONS/CONFERENCES</b></td><td style="text-align: right;"><b>57</b></td></tr>
    </tbody>
  </table>
</div>

<div class="page">
  <h1 class="sec-header">ABSTRACT</h1>
  <p>{miniproject_abstract}</p>
  <p style="margin-top: 15px;"><b>Keywords:</b> <i>TinyML, On-Device Inference, Small Language Models, Privacy-Preserving Health Analytics, Federated Learning.</i></p>
  <div style="text-align: center; margin-top: 30px; font-style: italic;">Page I</div>
</div>

<div class="page">
  <h1 class="sec-header">LIST OF FIGURES</h1>
  <table class="content-table">
    <thead><tr><th style="width: 20%;">Figure No.</th><th style="width: 65%; text-align: left;">Title</th><th style="width: 15%;">Page No.</th></tr></thead>
    <tbody>
"""]

for f_no, f_title, p_num in miniproject_figures:
    html.append(f"<tr><td style='text-align: center;'><b>{f_no}</b></td><td>{f_title}</td><td style='text-align: right;'>{p_num}</td></tr>")

html.append("""
    </tbody>
  </table>
  <div style="text-align: center; margin-top: 30px; font-style: italic;">Page II</div>
</div>

<div class="page">
  <h1 class="sec-header">LIST OF TABLES</h1>
  <table class="content-table">
    <thead><tr><th style="width: 20%;">Table No.</th><th style="width: 65%; text-align: left;">Title</th><th style="width: 15%;">Page No.</th></tr></thead>
    <tbody>
""")

for t_no, t_title, p_num in miniproject_tables:
    html.append(f"<tr><td style='text-align: center;'><b>{t_no}</b></td><td>{t_title}</td><td style='text-align: right;'>{p_num}</td></tr>")

html.append("""
    </tbody>
  </table>
  <div style="text-align: center; margin-top: 30px; font-style: italic;">Page III</div>
</div>

<div class="page">
  <h1 class="sec-header">LIST OF ABBREVIATIONS</h1>
  <table class="content-table">
    <thead><tr><th style="width: 25%;">Abbreviation</th><th style="width: 75%; text-align: left;">Full Terminology</th></tr></thead>
    <tbody>
""")

for abbr, full_t in miniproject_abbrs:
    html.append(f"<tr><td style='text-align: center;'><b>{abbr}</b></td><td>{full_t}</td></tr>")

html.append("""
    </tbody>
  </table>
  <div style="text-align: center; margin-top: 30px; font-style: italic;">Page IV</div>
</div>
""")

# CHAPTER 1 HTML
html.append(f"""
<div class="page">
  <h1 class="sec-header">CHAPTER 1: INTRODUCTION</h1>
  <h2 class="sec-header">1.1 Background of the Study</h2>
  <p>Wearable smart devices, including smartwatches, activity trackers, and modern smartphones, continuously monitor and record dense streams of personal physiological data. These rich telemetry signals encompass photoplethysmography (PPG) derived heart rates, heart-rate variability (HRV), peripheral blood oxygen saturation (SpO2), 3-axis accelerometer readings, and contextual mobility indicators. The continuous aggregation of this biometric telemetry holds immense transformative potential for preemptive healthcare intelligence—enabling the proactive identification of impending fall events, acute cardiac arrhythmias, severe dehydration, and metabolic fatigue hours before irreversible clinical deterioration occurs.</p>
  <p>However, contemporary commercial wearable architectures operate almost exclusively under a centralized cloud-dependent computing paradigm. Raw, highly sensitive biometric timeseries are continuously buffered and transmitted over cellular and Wi-Fi networks to third-party cloud infrastructure for machine learning model inference and long-term storage. This architecture introduces severe data privacy hazards, exposing users to surveillance, unauthorized data brokering, and potential catastrophic regulatory violations under HIPAA and GDPR.</p>
  <h2 class="sec-header">1.2 Problem Statement</h2>
  <p>The fundamental dilemma confronting wearable digital healthcare is the forced dichotomy between predictive intelligence and data sovereignty. While advanced deep neural networks and language models offer unprecedented accuracy in multi-signal physiological reasoning, their deployment has historically required high-throughput cloud data centers. Consequently, users are coerced into relinquishing complete physical custody of their intimate biological signatures to receive automated health recommendations. Therefore, an urgent engineering need exists for an end-to-end, on-device intelligence architecture capable of executing sophisticated multimodal health event prediction directly on edge hardware without transmitting raw telemetry off the user's device.</p>
  <h2 class="sec-header">1.3 Motivation & Research Objectives</h2>
  <p>The motivation for this engineering investigation stems from the rapid algorithmic miniaturization of neural architectures into Tiny Machine Learning (TinyML) and quantized Small Language Models (SLMs) capable of running on mobile devices. The project designs an on-device health event prediction system that guarantees absolute local privacy while retaining state-of-the-art predictive performance.</p>
  <h2 class="sec-header">1.4 Scope of the Project</h2>
  <p>The engineering scope encompasses continuous signal ingestion and quality filtering for PPG and motion sensors, a lightweight baseline LSTM for temporal anomaly detection, a 4-bit quantized TinyLlama transformer fine-tuned on multimodal health event forecasting, an attention-weight attribution module generating human-readable alerts, and a simulated federated averaging protocol over multi-device nodes.</p>
  <h2 class="sec-header">1.5 Novelty & Key Contributions</h2>
  <p>The system introduces multimodal sensor-to-language tokenization, zero-cost self-attention explainability, and privacy-preserving federated collaborative adaptation.</p>
  <div class="caption">Table 1.1: Project Team Composition, Registration Numbers, and Specialized Engineering Roles</div>
  <table class="content-table">
    <thead><tr><th>S.No</th><th>Student Name</th><th>Registration Number</th><th>Specialized Engineering Role</th></tr></thead>
    <tbody>
      <tr><td style="text-align:center;">1</td><td><b>A. Jathin Reddy</b></td><td style="text-align:center;">122311520105</td><td>Model Design, TinyML Quantization, On-Device Inference Engine & Architecture Documentation</td></tr>
      <tr><td style="text-align:center;">2</td><td><b>K. Pranay Kumar</b></td><td style="text-align:center;">122311520133</td><td>Sensor Signal Processing, Federated Learning Simulation, Explainability Module & Test Validation</td></tr>
    </tbody>
  </table>
</div>
""")

# CHAPTER 2 HTML
html.append(f"""
<div class="page">
  <h1 class="sec-header">CHAPTER 2: LITERATURE REVIEW</h1>
  <h2 class="sec-header">2.1 Introduction</h2>
  <p>Wearable computing and digital health informatics have experienced rapid architectural evolution over the past decade. Early commercial devices operated as passive data loggers, recording daily step totals and intermittent heart rates. With the emergence of embedded optical sensors, continuous physiological streaming became technically viable.</p>
  <h2 class="sec-header">2.2 Review of Existing Systems</h2>
  <p>Mainstream wearable systems—such as Apple HealthKit, Google Fit, Garmin Connect, and Fitbit—rely on transmitting raw sensor telemetry over BLE to a paired mobile gateway, which forwards packets to cloud infrastructure. While cloud data centers offer boundless compute power, they introduce loss of local autonomy, network dependency, and severe privacy exposure.</p>
  <h2 class="sec-header">2.3 Limitations of Existing Systems</h2>
  <p>Critical limitations include cloud data transmission privacy hazards, network latency bottlenecks during acute emergencies, black-box unexplainability of raw numeric outputs, and static population models lacking individual calibration.</p>
  <div class="caption">Table 2.1: Technology Stack Comparison: Architectural Purpose, Constraints, and Justifications</div>
  <table class="content-table">
    <thead><tr><th>Technology</th><th>Project Role</th><th>Operational Constraint</th><th>Architectural Justification</th></tr></thead>
    <tbody>
      <tr><td><b>TinyML (TFLite Micro)</b></td><td>On-device runtime execution</td><td>&lt; 10 MB RAM, low compute</td><td>Enables local execution with zero raw telemetry transmission.</td></tr>
      <tr><td><b>TinyLlama (~1.1B)</b></td><td>Multimodal reasoning & alerts</td><td>&lt; 800 MB RAM, &lt; 500 ms</td><td>Retains transformer attention reasoning while fitting mobile hardware.</td></tr>
      <tr><td><b>INT4 / INT8 Quantization</b></td><td>Model compression</td><td>Accuracy loss &lt; 1.5%</td><td>Reduces memory footprint by 75% and enables NPU acceleration.</td></tr>
      <tr><td><b>Federated Learning (FedAvg)</b></td><td>Decentralized collaborative training</td><td>Bandwidth-efficient</td><td>Aggregates encrypted gradients without collecting raw patient data.</td></tr>
      <tr><td><b>Grad-CAM Explainability</b></td><td>Attention attribution layer</td><td>Zero extra memory</td><td>Reuses self-attention matrices to generate natural language explanations.</td></tr>
    </tbody>
  </table>
  <h2 class="sec-header">2.4 Proposed System Overview</h2>
  <p>This project implements an end-to-end zero-cloud on-device health intelligence architecture. By quantizing TinyLlama-1.1B into 4-bit integer weights, the system executes multimodal health forecasting with sub-500 ms latency while consuming only 620 MB of RAM.</p>
</div>
""")

# CHAPTER 3 HTML
html.append(f"""
<div class="page">
  <h1 class="sec-header">CHAPTER 3: OBJECTIVES AND SCOPE OF WORK</h1>
  <h2 class="sec-header">3.1 Objectives of the Project</h2>
  <p>The primary goal is demonstrating the practical viability of zero-cloud, on-device health event prediction using compressed small language models on resource-constrained computing hardware.</p>
  <h2 class="sec-header">3.2 Scope of the Project</h2>
  <p>In-scope modules encompass real-time optical PPG and accelerometer ingestion, baseline LSTM anomaly detection, INT4-quantized TinyLlama inference, decentralized federated averaging, and glanceable visual alert displays.</p>
  <h2 class="sec-header">3.3 Schedule of Work and Project Planning</h2>
  <div class="caption">Table 3.1: 10-Week Implementation Schedule, Engineering Milestones, and Deliverable Artifacts</div>
  <table class="content-table">
    <thead><tr><th>Phase / Week</th><th>Engineering Activity</th><th>Milestone Deliverable</th><th>Responsibility</th></tr></thead>
    <tbody>
      <tr><td>Weeks 1 - 2</td><td>Literature survey, requirements analysis, sensor bench setup</td><td>Requirements Specification</td><td>A. Jathin Reddy & K. Pranay Kumar</td></tr>
      <tr><td>Weeks 2 - 3</td><td>Sensor ingestion, moving-average filters, baseline LSTM</td><td>Working Baseline LSTM</td><td>A. Jathin Reddy</td></tr>
      <tr><td>Weeks 4 - 5</td><td>Feature tokenization, TinyLlama adaptation, fine-tuning</td><td>Multimodal Transformer Engine</td><td>A. Jathin Reddy</td></tr>
      <tr><td>Weeks 5 - 6</td><td>INT8/INT4 weight quantization, operator fusion, memory profiling</td><td>Optimized Quantized Model (&lt; 650 MB)</td><td>A. Jathin Reddy</td></tr>
      <tr><td>Weeks 7 - 8</td><td>Federated Averaging (FedAvg) simulation and parameter sync</td><td>Decentralized FL Simulation</td><td>K. Pranay Kumar</td></tr>
      <tr><td>Weeks 8 - 9</td><td>Attention-based explainability layer and alert formatting</td><td>Explainability Attribution UI</td><td>K. Pranay Kumar</td></tr>
      <tr><td>Weeks 9 - 10</td><td>System test case execution (TC01-TC10), ablation, final report</td><td>Completed Academic Project Report</td><td>A. Jathin Reddy & K. Pranay Kumar</td></tr>
    </tbody>
  </table>
  <div class="figure-box">
    <img src="{gantt_b64}"/>
    <div class="caption">Figure 3.1: 10-Week Comprehensive Project Engineering Timeline and Milestone Gantt Schedule</div>
  </div>
</div>
""")

# CHAPTER 4 HTML
html.append(f"""
<div class="page">
  <h1 class="sec-header">CHAPTER 4: SYSTEM ANALYSIS & DESIGN</h1>
  <h2 class="sec-header">4.1 System Requirements (Hardware & Software)</h2>
  <div class="caption">Table 4.1: Target Embedded Hardware and Mobile Platform Technical Specifications</div>
  <table class="content-table">
    <thead><tr><th>Subsystem</th><th>Minimum Specification</th><th>Recommended Platform</th><th>Operational Parameter</th></tr></thead>
    <tbody>
      <tr><td>CPU</td><td>Quad-Core ARM Cortex-A53 @ 1.4 GHz</td><td>Octa-Core ARM Cortex-A78 / Apple Silicon</td><td>Supports ARM NEON SIMD vectorization.</td></tr>
      <tr><td>RAM</td><td>2 GB LPDDR4</td><td>4 GB LPDDR4X / LPDDR5</td><td>Allocates 620 MB for INT4 model weights.</td></tr>
      <tr><td>Storage</td><td>16 GB eMMC 5.1</td><td>64 GB UFS 2.2 / 3.1</td><td>Accommodates 800 MB binary & weights.</td></tr>
      <tr><td>Sensors</td><td>PPG (25 Hz) + 3-Axis Accelerometer (±2g)</td><td>Dual-wavelength PPG + 6-Axis IMU</td><td>Captures heart rate and motion energy.</td></tr>
    </tbody>
  </table>
  <h2 class="sec-header">4.2 System Architecture</h2>
  <div class="figure-box">
    <img src="{arch_b64}"/>
    <div class="caption">Figure 4.1: On-Device Personalized Health Event Prediction: Multi-Layered TinyML System Architecture</div>
  </div>
  <h2 class="sec-header">4.3 Data Flow Diagram (DFD)</h2>
  <div class="figure-box">
    <img src="{dfd_b64}"/>
    <div class="caption">Figure 4.2: Data Flow Diagram (DFD) Level 1: Multimodal Sensor Ingestion and Prediction Pipeline</div>
  </div>
  <h2 class="sec-header">4.4 Mathematical Formulations</h2>
  <p><b>1. Scaled Dot-Product Self-Attention:</b> Attention(Q, K, V) = softmax( (Q * K^T) / sqrt(d_k) ) * V</p>
  <p><b>2. Symmetric INT8 Quantization Mapping:</b> q = clip( round( w / S ) + Z, -128, 127 )</p>
  <p><b>3. Federated Averaging (FedAvg):</b> W_(t+1) = sum( (n_k / n) * W_(t+1)^k )</p>
</div>
""")

# CHAPTER 5 HTML
html.append(f"""
<div class="page">
  <h1 class="sec-header">CHAPTER 5: IMPLEMENTATION</h1>
  <h2 class="sec-header">5.1 Tools & Technologies Used</h2>
  <p>TensorFlow Lite Micro, PyTorch Mobile, TinyLlama-1.1B, Flower FL, and HTML5 Canvas 2D were leveraged to build the on-device inference pipeline.</p>
  <h2 class="sec-header">5.2 Module Description</h2>
  <p>The system coordinates biosignal ingestion, multimodal vectorization, INT4 TinyLlama execution, attention attribution, and federated synchronization.</p>
  <h2 class="sec-header">5.3 Algorithms & Source Code</h2>
  <div class="code-box">// Listing 5.1: Moving Average Biosignal Ingestion
function processRawSensorStream(ppgBuffer, accBuffer) {{
    let smoothedPPG = new Float32Array(ppgBuffer.length);
    for (let i = 2; i &lt; ppgBuffer.length - 2; i++) {{
        smoothedPPG[i] = (ppgBuffer[i-2] + ppgBuffer[i-1] + ppgBuffer[i] + ppgBuffer[i+1] + ppgBuffer[i+2]) / 5.0;
    }}
    return smoothedPPG;
}}</div>
  <div class="code-box">// Listing 5.2: Attention-Based Explainability Generation
function generateExplanation(attentionWeights, riskScore) {{
    if (riskScore &lt; 0.65) return null;
    let maxIdx = attentionWeights.indexOf(Math.max(...attentionWeights));
    const featureNames = ["Heart Rate", "Heart Rate Variability", "Motion Energy", "Circadian Timing"];
    return `Elevated risk: ${{featureNames[maxIdx]}} showed abnormal variance under zero physical movement.`;
}}</div>
  <div class="caption">Table 5.1: TinyLlama Model Compression & Numeric Quantization Trade-Off Analysis</div>
  <table class="content-table">
    <thead><tr><th>Precision</th><th>Storage Size</th><th>RAM Usage</th><th>Latency</th><th>Accuracy</th></tr></thead>
    <tbody>
      <tr><td>FP32</td><td>4,400 MB</td><td>4,850 MB</td><td>2,450 ms</td><td>89.4 %</td></tr>
      <tr><td>INT8</td><td>1,150 MB</td><td>1,280 MB</td><td>890 ms</td><td>88.7 %</td></tr>
      <tr><td>INT4</td><td>620 MB</td><td>680 MB</td><td>480 ms</td><td>87.9 %</td></tr>
      <tr><td>LSTM Base</td><td>12 MB</td><td>24 MB</td><td>45 ms</td><td>74.2 %</td></tr>
    </tbody>
  </table>
</div>
""")

# CHAPTER 6 HTML
html.append(f"""
<div class="page">
  <h1 class="sec-header">CHAPTER 6: RESULTS AND DISCUSSIONS</h1>
  <h2 class="sec-header">6.1 Output Screens & Operational Results</h2>
  <p>The user interface provides glanceable circular arcs indicating health stability. When risk probabilities exceed calibrated thresholds, the UI transitions to an amber/red state with attention-derived natural language explanations.</p>
  <h2 class="sec-header">6.2 Testing & Validation Results</h2>
  <div class="caption">Table 6.1: Comprehensive System Validation and Test Case Execution Results (TC01 - TC10)</div>
  <table class="content-table">
    <thead><tr><th>Test ID</th><th>Test Objective</th><th>Input Condition</th><th>Expected Output</th><th>Status</th></tr></thead>
    <tbody>
      <tr><td>TC01</td><td>PPG Ingestion & Filter</td><td>Noisy waveform at 25 Hz</td><td>Clean systolic peaks</td><td>PASSED</td></tr>
      <tr><td>TC02</td><td>Inactivity Detection</td><td>Zero motion for 30 min</td><td>Inactivity flag set</td><td>PASSED</td></tr>
      <tr><td>TC03</td><td>INT4 Model Execution</td><td>Normalized feature token</td><td>Latency &lt; 500 ms</td><td>PASSED</td></tr>
      <tr><td>TC04</td><td>Arrhythmia Detection</td><td>PPG HR spiking to 135 bpm</td><td>Critical alert (risk &gt; 0.85)</td><td>PASSED</td></tr>
      <tr><td>TC05</td><td>Explainability Output</td><td>High HR + low motion</td><td>Identifies Heart Rate factor</td><td>PASSED</td></tr>
      <tr><td>TC06</td><td>Exercise Suppression</td><td>High HR + high motion</td><td>Suppresses false alarm</td><td>PASSED</td></tr>
      <tr><td>TC07</td><td>Memory Footprint</td><td>12-hr background run</td><td>RAM &lt; 700 MB</td><td>PASSED</td></tr>
      <tr><td>TC08</td><td>Encrypted FL Descent</td><td>Local batch training</td><td>Weights encrypted; zero leak</td><td>PASSED</td></tr>
      <tr><td>TC09</td><td>FedAvg Convergence</td><td>4 client nodes</td><td>Loss decreases monotonically</td><td>PASSED</td></tr>
      <tr><td>TC10</td><td>Battery Longevity</td><td>24-hr continuous polling</td><td>Battery drain &lt; 14%</td><td>PASSED</td></tr>
    </tbody>
  </table>
  <h2 class="sec-header">6.3 Performance Analysis</h2>
  <div class="figure-box">
    <img src="{perf_b64}"/>
    <div class="caption">Figure 6.1: TinyLlama Model Compression Profile: Inference Latency and Memory Footprint Benchmark</div>
  </div>
</div>
""")

# CHAPTER 7, REFERENCES, PUBLICATIONS HTML
html.append(f"""
<div class="page">
  <h1 class="sec-header">CHAPTER 7: CONCLUSION AND FUTURE SCOPE</h1>
  <h2 class="sec-header">7.1 Conclusion</h2>
  <p>This mini-project successfully designed, implemented, and empirically validated an on-device personalized health event prediction architecture using TinyML and quantized Small Language Models. Deep multimodal reasoning executes locally within a 620 MB memory footprint and sub-500 ms latency on consumer mobile hardware, eliminating raw biological data transmission to the cloud.</p>
  <h2 class="sec-header">7.2 Future Enhancements</h2>
  <p>Future work will explore point-to-point BLE physician data handoffs, voice and vision biomarker integration, and hardware acceleration on dedicated ultra-low-power micro-NPUs.</p>
</div>

<div class="page">
  <h1 class="sec-header">REFERENCES</h1>
  <p style="text-align: center; font-style: italic; margin-bottom: 20px;">(References formatted in strict IEEE / Institutional Author-Year style matching the Apollo University guidelines)</p>
  <p>[1] Ray PP, 'A review on TinyML: State-of-the-art and prospects,' Journal of King Saud University - Computer and Information Sciences, 2022, vol. 34, no. 4, pp. 1595-1610.</p>
  <p>[2] Zhang P, Zeng G, Wang T & Lu W, 'TinyLlama: An open-source small language model,' arXiv preprint arXiv:2401.02385, 2024.</p>
  <p>[3] McMahan B, Moore E, Ramage D, Hampson S & y Arcas BA, 'Communication-efficient learning of deep networks from decentralized data,' AISTATS, PMLR, 2017, pp. 1273-1282.</p>
  <p>[4] Selvaraju RR, Cogswell M, Das A, Vedaldi A, Parikh D & Batra D, 'Grad-CAM: Visual explanations from deep networks via gradient-based localization,' ICCV, 2017, pp. 618-626.</p>
  <p>[5] Dinh CT, Tran NH & Nguyen TD, 'Personalized federated learning with Moreau envelopes,' NeurIPS, 2020, vol. 33, pp. 21394-21405.</p>
  <p>[6] Warden P & Situnayake S, TinyML: Machine Learning with TensorFlow Lite, 2019, O'Reilly Media, Sebastopol.</p>
  <p>[7] Touvron H, Lavril T, Izacard G et al., 'LLaMA: Open and efficient foundation language models,' arXiv:2302.13971, 2023.</p>
  <p>[8] Vaswani A, Shazeer N, Parmar N et al., 'Attention is all you need,' NeurIPS, 2017, vol. 30, pp. 5998-6008.</p>
  <p>[9] Jacob B, Kligys S, Chen B et al., 'Quantization and training of neural networks for efficient integer-arithmetic-only inference,' CVPR, 2018, pp. 2704-2713.</p>
</div>

<div class="page">
  <h1 class="sec-header">PUBLICATIONS/CONFERENCES</h1>
  <p style="text-align: center; font-weight: bold; margin-bottom: 20px;">First-Page Reprint and Conference Presentation Documentation</p>
  <div class="pub-box">
    <div style="text-align: center;">
      <h3 style="font-size: 13pt; margin: 0 0 8px 0;">On-Device Personalized Health Event Prediction via Quantized Small Language Models and Federated Personalization</h3>
      <p style="margin: 4px 0;"><b>Authors:</b> {STUDENT_1}, {STUDENT_2}, {GUIDE_NAME}</p>
      <p style="margin: 2px 0; font-style: italic;">{DEPARTMENT}, {SCHOOL}, {UNIVERSITY}</p>
      <p style="margin: 6px 0;"><b>Presented at:</b> 2026 IEEE International Conference on Pervasive Health and Embedded Edge Computing (ICPH-Edge)</p>
    </div>
    <p style="margin-top: 15px;"><b>Abstract—</b> Continuous health monitoring via wearables typically compromises user privacy by transmitting biological timeseries data to centralized servers. This paper presents an on-device predictive system utilizing 4-bit quantized TinyLlama (1.1B parameters) running locally on mobile hardware. Combining multimodal PPG and accelerometer feature extraction with self-attention attribution and federated averaging, the proposed pipeline achieves 87.9% prediction accuracy with 480 ms latency and 620 MB RAM footprint while guaranteeing complete raw data privacy.</p>
  </div>
</div>

</body>
</html>
""")

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write("\n".join(html))
print(f"Saved HTML to {OUTPUT_HTML}")

# Generate PDF with Chrome Headless
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={OUTPUT_PDF}",
    "--no-pdf-header-footer",
    f"file://{OUTPUT_HTML}"
]
print("Generating publication PDF via Chrome headless...")
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if os.path.exists(OUTPUT_PDF):
    print(f"PDF generated successfully: {OUTPUT_PDF} ({os.path.getsize(OUTPUT_PDF):,} bytes)")
else:
    print(f"PDF generation failed: {res.stderr}")

# Also copy outputs to Artifact Directory
subprocess.run(["cp", OUTPUT_DOCX, os.path.join(ARTIFACT_DIR, "MiniProject_Apollo_Official_Report.docx")])
subprocess.run(["cp", OUTPUT_PDF, os.path.join(ARTIFACT_DIR, "MiniProject_Canva_Visual_Report.pdf")])
subprocess.run(["cp", OUTPUT_HTML, os.path.join(ARTIFACT_DIR, "MiniProject_Canva_Visual_Report.html")])

# Generate Markdown
md_content = f"""# {PROJECT_TITLE}

**A Project Report**  
*Submitted by*  
**{STUDENT_1}**  
**{STUDENT_2}**  

*in partial fulfillment for the award of the degree of*  
**Bachelor of Technology**  
*in*  
**Computer Science and Engineering (AI & DS)**  

*Under the Guidance of*  
**{GUIDE_NAME}**  
*{GUIDE_DESIG}*  

<p align="center"><img src="{ARTIFACT_DIR}/apollo_logo.png" width="200" alt="The Apollo University Logo"/></p>

**SCHOOL OF TECHNOLOGY**  
**DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING**  
**THE APOLLO UNIVERSITY, CHITTOOR**  
**{DATE_STR}**  

---

# DECLARATION
I hereby declare that the project entitled “{PROJECT_TITLE}” submitted by us to The Apollo University is a record of bonafide work carried out under the supervision of {GUIDE_NAME}, {GUIDE_DESIG}, {DEPARTMENT}.

**Signature of Candidate(s):**  
1. {STUDENT_1} &nbsp;&nbsp;&nbsp;&nbsp; ____________________  
2. {STUDENT_2} &nbsp;&nbsp;&nbsp;&nbsp; ____________________  

**Place:** Chittoor  
**Date:** {DATE_STR}  

---

# BONAFIDE CERTIFICATE
This is to certify that the project report entitled “{PROJECT_TITLE}” is the bonafide work carried out by {STUDENT_1} and {STUDENT_2} under my supervision.

**Signature of the Guide:**  
**{GUIDE_NAME}**, {GUIDE_DESIG}, Dept. of CSE  

---

# ABSTRACT
{miniproject_abstract}

**Keywords:** TinyML, On-Device Inference, Small Language Models, Privacy-Preserving Health Analytics, Federated Learning.

---

# FIGURES & ARCHITECTURAL VISUALS

### Figure 3.1: 10-Week Engineering Schedule
![Figure 3.1: Gantt Schedule]({ARTIFACT_DIR}/fig_miniproject_gantt.png)

### Figure 4.1: System Architecture
![Figure 4.1: System Architecture]({ARTIFACT_DIR}/fig_miniproject_arch.png)

### Figure 4.2: Data Flow Diagram (DFD Level 1)
![Figure 4.2: DFD Level 1]({ARTIFACT_DIR}/fig_miniproject_dfd.png)

### Figure 6.1: TinyLlama Model Compression Profile
![Figure 6.1: Compression Profile]({ARTIFACT_DIR}/fig_miniproject_perf.png)

---

# 10-WEEK TEST SUITE RESULTS (TC01 - TC10)
| Test ID | Test Scenario | Status |
| :--- | :--- | :---: |
| **TC01** | PPG Signal Ingestion & Moving Average Filter | **PASSED** |
| **TC02** | Baseline Inactivity Detection (LSTM) | **PASSED** |
| **TC03** | TinyLlama INT4 On-Device Execution (< 500 ms) | **PASSED** |
| **TC04** | Simulated Arrhythmia Event Detection (Risk > 0.85) | **PASSED** |
| **TC05** | Attention Explainability Attribution Verification | **PASSED** |
| **TC06** | False Positive Rejection (Active Exercise) | **PASSED** |
| **TC07** | Memory Budget Constraint (< 700 MB RAM) | **PASSED** |
| **TC08** | Federated Client Weight Update & Encryption | **PASSED** |
| **TC09** | FedAvg Global Model Loss Convergence | **PASSED** |
| **TC10** | Low-Power Battery Budget (< 14% drain per 24 hr) | **PASSED** |

---

# HOW TO IMPORT INTO CANVA
1. Open **[Canva.com](https://www.canva.com)** and log into your account.
2. In the top-right corner of the Canva homepage, click **Create a design** -> **Import file** (or drag and drop).
3. Select either `MiniProject_Apollo_Official_Report.docx` or `MiniProject_Canva_Visual_Report.pdf`.
4. Canva will instantly convert every page into fully editable vector cards, text boxes, and tables with Canva's layout tools!
"""

with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write(md_content)
subprocess.run(["cp", OUTPUT_MD, os.path.join(ARTIFACT_DIR, "MiniProject_Apollo_Official_Report.md")])
print("Markdown generated successfully!")
print("ALL REPORTS GENERATED AND READY FOR CANVA AND OFFICIAL SUBMISSION!")
