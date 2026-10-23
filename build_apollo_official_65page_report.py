#!/usr/bin/env python3
"""Master Builder for The Apollo University Official 60+ Page Academic Project Report.
Strictly adheres to:
1. Institutional Template: media_1792773194544_9aa85a32.docx
2. Reference Title, Cover, Declaration, Certificate, Acknowledgement, Tables 0-3
3. Exact word placement, alignments, page numbers, logos, Times New Roman font, 1.5 line spacing
4. Generates 65+ pages of comprehensive academic prose, figures, tables, code, and references.
5. Produces:
   - InstaHealth_60_Page_Official_Apollo_Report.docx
   - InstaHealth_60_Page_Official_Apollo_Report.html
   - InstaHealth_60_Page_Official_Apollo_Report.pdf (Sanitized ISO PDF)
"""

import os
import sys
import subprocess
import shutil
import base64
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

import pypdf

# Import comprehensive technical chapters from report_sections
from report_sections.preliminary import (
    TITLE_DATA, DECLARATION_TEXT, BONAFIDE_CERTIFICATE_TEXT,
    ACKNOWLEDGEMENT_PARAGRAPHS, ABSTRACT_TEXT, ABSTRACT_KEYWORDS,
    FIGURES_LIST, TABLES_LIST, ABBREVIATIONS_LIST
)
from report_sections.chapter1 import CHAPTER_1_TITLE, SECTIONS as CH1_SECTIONS
from report_sections.chapter2 import CHAPTER_2_TITLE, SECTIONS as CH2_SECTIONS
from report_sections.chapter3 import CHAPTER_3_TITLE, SECTIONS as CH3_SECTIONS
from report_sections.chapter4 import CHAPTER_4_TITLE, SECTIONS as CH4_SECTIONS
from report_sections.chapter5 import CHAPTER_5_TITLE, SECTIONS as CH5_SECTIONS
from report_sections.chapter6 import CHAPTER_6_TITLE, SECTIONS as CH6_SECTIONS
from report_sections.chapter7 import CHAPTER_7_TITLE, SECTIONS as CH7_SECTIONS
from report_sections.references_pubs import (
    REFERENCES_TITLE, REFERENCES_LIST,
    PUBLICATIONS_TITLE, PUBLICATION_SUMMARY
)
from report_sections.tables_data import TABLES

TEMPLATE_DOCX = "/Users/jathinreddy/.gemini/antigravity/brain/f353d961-e7fd-445e-894a-a4a5c051abdb/.user_uploaded/media_1792773194544_9aa85a32.docx"
WORKSPACE_DIR = "/Users/jathinreddy/Desktop/InstaHealth"
ARTIFACT_DIR = "/Users/jathinreddy/.gemini/antigravity/brain/f353d961-e7fd-445e-894a-a4a5c051abdb"
DOWNLOADS_DIR = "/Users/jathinreddy/Downloads"

OUT_DOCX_WS = os.path.join(WORKSPACE_DIR, "InstaHealth_60_Page_Official_Apollo_Report.docx")
OUT_DOCX_DL = os.path.join(DOWNLOADS_DIR, "InstaHealth_60_Page_Official_Apollo_Report.docx")
OUT_HTML_WS = os.path.join(WORKSPACE_DIR, "InstaHealth_60_Page_Official_Apollo_Report.html")
OUT_PDF_WS  = os.path.join(WORKSPACE_DIR, "InstaHealth_60_Page_Official_Apollo_Report.pdf")
OUT_PDF_DL  = os.path.join(DOWNLOADS_DIR, "InstaHealth_60_Page_Official_Apollo_Report.pdf")

# Standard Project Details strictly matching prompt
PROJECT_TITLE = "ON-DEVICE PERSONALIZED HEALTH EVENT PREDICTION USING TINYML AND ON-DEVICE SMALL LANGUAGE MODELS FOR PRIVACY-PRESERVING HEALTH ANALYTICS"
STUDENT_1 = "A. Jathin Reddy (122311520105)"
STUDENT_2 = "K. Pranay Kumar (122311520133)"
GUIDE_NAME = "Dr. Thirumalesu.K"
GUIDE_DESIG = "Assistant Professor"
DEPARTMENT = "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING"
SCHOOL = "SCHOOL OF TECHNOLOGY"
UNIVERSITY = "THE APOLLO UNIVERSITY, CHITTOOR"
DATE_STR = "April, 2026"

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="000000", sz="4", val="single"):
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

def format_run(run, text=None, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color=RGBColor(0,0,0)):
    if text is not None:
        run.text = text
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color

def add_para(doc, text="", size=12, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.5, color=RGBColor(0,0,0)):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        r = p.add_run(text)
        format_run(r, font_name="Times New Roman", size_pt=size, bold=bold, italic=italic, color=color)
    return p

def add_heading_1(doc, text):
    p = add_para(doc, text, size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=18, space_after=12, line_spacing=1.5, color=RGBColor(0,0,0))
    return p

def add_heading_2(doc, text):
    p = add_para(doc, text, size=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=14, space_after=6, line_spacing=1.5, color=RGBColor(0,0,0))
    return p

def add_heading_3(doc, text):
    p = add_para(doc, text, size=12, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=4, line_spacing=1.5, color=RGBColor(0,0,0))
    return p

def add_image_figure(doc, img_path, caption_text, width_in=5.6):
    if not os.path.exists(img_path):
        print(f"Warning: image not found {img_path}")
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(12)
    p_img.paragraph_format.space_after = Pt(4)
    r_img = p_img.add_run()
    r_img.add_picture(img_path, width=Inches(width_in))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(14)
    r_cap = p_cap.add_run(caption_text)
    format_run(r_cap, font_name="Times New Roman", size_pt=10.5, bold=True, italic=False, color=RGBColor(0,0,0))

def add_table_data(doc, table_key):
    if table_key not in TABLES:
        print(f"Warning: table key not found {table_key}")
        return
    tdata = TABLES[table_key]
    
    # Caption
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(12)
    p_cap.paragraph_format.space_after = Pt(6)
    r_cap = p_cap.add_run(tdata["title"])
    format_run(r_cap, font_name="Times New Roman", size_pt=10.5, bold=True, color=RGBColor(0,0,0))
    
    cols = len(tdata["headers"])
    rows = len(tdata["rows"]) + 1
    table = doc.add_table(rows=rows, cols=cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="000000", sz="4", val="single")
    
    # Header Row
    hdr_cells = table.rows[0].cells
    for c_idx, title in enumerate(tdata["headers"]):
        cell = hdr_cells[c_idx]
        set_cell_background(cell, "E2E8F0")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(title)
        format_run(r, font_name="Times New Roman", size_pt=9.5, bold=True, color=RGBColor(0,0,0))
        
    # Data Rows
    for r_idx, row in enumerate(tdata["rows"]):
        row_cells = table.rows[r_idx + 1].cells
        bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            cell = row_cells[c_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (c_idx > 0 and len(val) < 25) else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(val)
            format_run(r, font_name="Times New Roman", size_pt=9.0, color=RGBColor(0,0,0))
            
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(8)

def add_code_snippet(doc, code_text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.05
    
    # Border
    pPr = p._element.get_or_add_pPr()
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:left w:val="single" w:sz="16" w:space="8" w:color="000000"/><w:top w:val="single" w:sz="4" w:space="4" w:color="E2E8F0"/><w:right w:val="single" w:sz="4" w:space="4" w:color="E2E8F0"/><w:bottom w:val="single" w:sz="4" w:space="4" w:color="E2E8F0"/></w:pBdr>')
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8FAFC"/>')
    pPr.append(pBdr)
    pPr.append(shd)
    
    lines = code_text.strip().split("\n")
    for l_idx, line in enumerate(lines):
        r = p.add_run(line + ("\n" if l_idx < len(lines)-1 else ""))
        format_run(r, font_name="Courier New", size_pt=8.5, color=RGBColor(0,0,0))

def render_paragraph_or_element(doc, p_text):
    if p_text.startswith("Algorithm ") or p_text.startswith("// =="):
        add_code_snippet(doc, p_text)
    elif p_text == "[FIGURE 3.1: GANTT CHART]":
        add_image_figure(doc, os.path.join(WORKSPACE_DIR, "fig_miniproject_gantt.png"),
                         "Figure 3.1: InstaHealth 10-Week Comprehensive Engineering Gantt Schedule", width_in=5.8)
    elif p_text == "[FIGURE 4.1: SYSTEM ARCHITECTURE]":
        add_image_figure(doc, os.path.join(WORKSPACE_DIR, "fig_miniproject_arch.png"),
                         "Figure 4.1: Three-Tier On-Device Health Intelligence Architecture", width_in=5.8)
    elif p_text == "[FIGURE 4.2: DFD LEVEL 0]":
        add_image_figure(doc, os.path.join(WORKSPACE_DIR, "fig_dfd_level0.png"),
                         "Figure 4.2: Data Flow Diagram Level 0: Context Level Zero-Cloud Representation", width_in=5.8)
    elif p_text == "[FIGURE 4.3: DFD LEVEL 1]":
        add_image_figure(doc, os.path.join(WORKSPACE_DIR, "fig_miniproject_dfd.png"),
                         "Figure 4.3: Data Flow Diagram Level 1: Subsystem Level Functional Decomposition", width_in=5.8)
    elif p_text == "[FIGURE 4.4: DFD LEVEL 2]":
        add_image_figure(doc, os.path.join(WORKSPACE_DIR, "fig_dfd_level2.png"),
                         "Figure 4.4: Data Flow Diagram Level 2: Detailed Process Flow for Edge Gating & Inference", width_in=5.8)
    elif p_text == "[FIGURE 5.1: CALIBRATION WORKFLOW]":
        add_image_figure(doc, os.path.join(WORKSPACE_DIR, "fig_3_2_workflow.png"),
                         "Figure 5.1: InstaHealth 48-Hour On-Device Calibration and Lifecycle State Machine Workflow", width_in=5.8)
    elif p_text == "[FIGURE 6.1: DAY 1 CALIBRATION SCREENSHOT]":
        add_image_figure(doc, os.path.join(WORKSPACE_DIR, "screenshot_day1_calibration.png"),
                         "Figure 6.1: InstaHealth Day 1 & Day 2 Calibration UI: Real-Time Telemetry vs Demographic Benchmarks", width_in=3.6)
    elif p_text == "[FIGURE 6.2: DAY 3 PRESCRIPTION SCREENSHOT]":
        add_image_figure(doc, os.path.join(WORKSPACE_DIR, "screenshot_day3_prescriptions.png"),
                         "Figure 6.2: InstaHealth Day 3+ Calibrated Prescription UI: Multi-Metric Circular Ring Carousel", width_in=3.6)
    elif p_text == "[FIGURE 6.3: ABLATION CHART]":
        add_image_figure(doc, os.path.join(WORKSPACE_DIR, "fig_ablation_chart.png"),
                         "Figure 6.3: Empirical Model Compression and Latency vs RAM Trade-off", width_in=5.8)
    elif p_text == "[FIGURE 6.4: BATTERY POWER PROFILE]":
        add_image_figure(doc, os.path.join(WORKSPACE_DIR, "fig_battery_chart.png"),
                         "Figure 6.4: Hardware Subsystem Current Draw Profile and 48-Hour Smartwatch Battery Budget", width_in=5.8)
    else:
        add_para(doc, p_text, size=12, space_after=6, line_spacing=1.5, color=RGBColor(0,0,0))

def render_section_content(doc, sec):
    add_heading_2(doc, sec["title"])
    for p_text in sec.get("paragraphs", []):
        render_paragraph_or_element(doc, p_text)
    
    for sub in sec.get("subsections", []):
        add_heading_3(doc, sub["title"])
        for p_text in sub.get("paragraphs", []):
            render_paragraph_or_element(doc, p_text)

print("Building 60+ Page Official Apollo University Academic Report...")
doc = docx.Document(TEMPLATE_DOCX)

# 1. Update Cover Page (Page 1)
print("Applying cover page styling and centered Apollo logo...")
p0 = doc.paragraphs[0]
p0.text = PROJECT_TITLE
p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
p0.paragraph_format.space_before = Pt(0)
p0.paragraph_format.space_after = Pt(6)
p0.paragraph_format.line_spacing = 1.15
for r in p0.runs:
    format_run(r, font_name="Times New Roman", size_pt=15, bold=True)

# Clear unused placeholder paragraphs on title page
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
    format_run(r, font_name="Times New Roman", size_pt=13, bold=True)

p4 = doc.paragraphs[4]
p4.text = "Submitted by"
p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
p4.paragraph_format.space_before = Pt(2)
p4.paragraph_format.space_after = Pt(2)
for r in p4.runs:
    format_run(r, font_name="Times New Roman", size_pt=12, italic=True)

p6 = doc.paragraphs[6]
p6.text = STUDENT_1
p6.alignment = WD_ALIGN_PARAGRAPH.CENTER
p6.paragraph_format.space_before = Pt(1)
p6.paragraph_format.space_after = Pt(1)
p6.paragraph_format.line_spacing = 1.0
for r in p6.runs:
    format_run(r, font_name="Times New Roman", size_pt=12, bold=True)

p7 = doc.paragraphs[7]
p7.text = STUDENT_2
p7.alignment = WD_ALIGN_PARAGRAPH.CENTER
p7.paragraph_format.space_before = Pt(1)
p7.paragraph_format.space_after = Pt(4)
p7.paragraph_format.line_spacing = 1.0
for r in p7.runs:
    format_run(r, font_name="Times New Roman", size_pt=12, bold=True)

p10 = doc.paragraphs[10]
p10.text = "in partial fulfillment for the award of the degree"
p10.alignment = WD_ALIGN_PARAGRAPH.CENTER
p10.paragraph_format.space_before = Pt(2)
p10.paragraph_format.space_after = Pt(1)
for r in p10.runs:
    format_run(r, font_name="Times New Roman", size_pt=11, italic=True)

p12 = doc.paragraphs[12]
p12.text = "of"
p12.alignment = WD_ALIGN_PARAGRAPH.CENTER
p12.paragraph_format.space_before = Pt(0)
p12.paragraph_format.space_after = Pt(1)
for r in p12.runs:
    format_run(r, font_name="Times New Roman", size_pt=11, italic=True)

p14 = doc.paragraphs[14]
p14.text = "Bachelor of Technology"
p14.alignment = WD_ALIGN_PARAGRAPH.CENTER
p14.paragraph_format.space_before = Pt(1)
p14.paragraph_format.space_after = Pt(1)
for r in p14.runs:
    format_run(r, font_name="Times New Roman", size_pt=13, bold=True)

p15 = doc.paragraphs[15]
p15.text = "in"
p15.alignment = WD_ALIGN_PARAGRAPH.CENTER
p15.paragraph_format.space_before = Pt(0)
p15.paragraph_format.space_after = Pt(1)
for r in p15.runs:
    format_run(r, font_name="Times New Roman", size_pt=11)

p16 = doc.paragraphs[16]
p16.text = "Computer Sciences & Engineering"
p16.alignment = WD_ALIGN_PARAGRAPH.CENTER
p16.paragraph_format.space_before = Pt(1)
p16.paragraph_format.space_after = Pt(4)
for r in p16.runs:
    format_run(r, font_name="Times New Roman", size_pt=13, bold=True)

p17 = doc.paragraphs[17]
p17.text = "Under the Guidance of"
p17.alignment = WD_ALIGN_PARAGRAPH.CENTER
p17.paragraph_format.space_before = Pt(2)
p17.paragraph_format.space_after = Pt(1)
for r in p17.runs:
    format_run(r, font_name="Times New Roman", size_pt=12, italic=True)

p19 = doc.paragraphs[19]
p19.text = f"{GUIDE_NAME}\n{GUIDE_DESIG}"
p19.alignment = WD_ALIGN_PARAGRAPH.CENTER
p19.paragraph_format.space_before = Pt(1)
p19.paragraph_format.space_after = Pt(4)
p19.paragraph_format.line_spacing = 1.05
for r in p19.runs:
    format_run(r, font_name="Times New Roman", size_pt=12, bold=True)

p20 = doc.paragraphs[20]
p20.text = ""
p20.alignment = WD_ALIGN_PARAGRAPH.CENTER
p20.paragraph_format.space_before = Pt(4)
p20.paragraph_format.space_after = Pt(4)
r20 = p20.add_run()
r20.add_picture(os.path.join(WORKSPACE_DIR, "apollo_logo.png"), width=Inches(1.65))

p21 = doc.paragraphs[21]
p21.text = SCHOOL
p21.alignment = WD_ALIGN_PARAGRAPH.CENTER
p21.paragraph_format.space_before = Pt(2)
p21.paragraph_format.space_after = Pt(1)
for r in p21.runs:
    format_run(r, font_name="Times New Roman", size_pt=13, bold=True)

p22 = doc.paragraphs[22]
p22.text = DEPARTMENT
p22.alignment = WD_ALIGN_PARAGRAPH.CENTER
p22.paragraph_format.space_before = Pt(0)
p22.paragraph_format.space_after = Pt(1)
for r in p22.runs:
    format_run(r, font_name="Times New Roman", size_pt=13, bold=True)

p23 = doc.paragraphs[23]
p23.text = UNIVERSITY
p23.alignment = WD_ALIGN_PARAGRAPH.CENTER
p23.paragraph_format.space_before = Pt(0)
p23.paragraph_format.space_after = Pt(4)
for r in p23.runs:
    format_run(r, font_name="Times New Roman", size_pt=13, bold=True)

p25 = doc.paragraphs[25]
p25.text = DATE_STR
p25.alignment = WD_ALIGN_PARAGRAPH.CENTER
p25.paragraph_format.space_before = Pt(2)
p25.paragraph_format.space_after = Pt(0)
for r in p25.runs:
    format_run(r, font_name="Times New Roman", size_pt=12, bold=True)

# 2. Update Declaration (Page 2)
print("Updating Declaration...")
doc.paragraphs[30].text = (
    f"   I hereby declare that the project entitled “{PROJECT_TITLE}” submitted by us, "
    f"for the award of the degree of Bachelor of Technology in Computer Sciences & Engineering, School of Technology to "
    f"The Apollo University is a record of bonafide work carried out by us under the supervision of “{GUIDE_NAME}”."
)
doc.paragraphs[30].alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
doc.paragraphs[30].paragraph_format.line_spacing = 1.5
for r in doc.paragraphs[30].runs:
    format_run(r, font_name="Times New Roman", size_pt=12)

doc.paragraphs[31].text = (
    "   We further declare that the work reported in this thesis has not been submitted and will not be "
    "submitted, either in part or in full, for the award of any other degree or diploma in this institute "
    "or any other institute or university."
)
doc.paragraphs[31].alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
doc.paragraphs[31].paragraph_format.line_spacing = 1.5
for r in doc.paragraphs[31].runs:
    format_run(r, font_name="Times New Roman", size_pt=12)

doc.paragraphs[33].text = "                                                     Signature of the Candidate(s) with names"
for r in doc.paragraphs[33].runs:
    format_run(r, font_name="Times New Roman", size_pt=12, bold=True)

doc.paragraphs[34].text = f"                                                                           1. {STUDENT_1}"
for r in doc.paragraphs[34].runs:
    format_run(r, font_name="Times New Roman", size_pt=12)

doc.paragraphs[35].text = f"                                                                           2. {STUDENT_2}"
for r in doc.paragraphs[35].runs:
    format_run(r, font_name="Times New Roman", size_pt=12)

doc.paragraphs[37].text = "Place\t: Chittoor"
for r in doc.paragraphs[37].runs:
    format_run(r, font_name="Times New Roman", size_pt=12, bold=True)

doc.paragraphs[38].text = f"Date\t: {DATE_STR}"
for r in doc.paragraphs[38].runs:
    format_run(r, font_name="Times New Roman", size_pt=12, bold=True)

# 3. Update Bonafide Certificate (Page 3)
print("Updating Bonafide Certificate...")
doc.paragraphs[47].text = (
    f"         This is to certify that the project report entitled “{PROJECT_TITLE}” is the bonafide work carried "
    f"out by {STUDENT_1} and {STUDENT_2}, under my supervision and guidance, in partial fulfillment of the requirements "
    f"for the award of the degree of Bachelor of Technology in Computer Sciences & Engineering by The Apollo University, Chittoor."
)
doc.paragraphs[47].alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
doc.paragraphs[47].paragraph_format.line_spacing = 1.5
for r in doc.paragraphs[47].runs:
    format_run(r, font_name="Times New Roman", size_pt=12)

doc.paragraphs[51].text = f"                                                                                                Signature of the Guide\n                                                                                                {GUIDE_NAME}\n                                                                                                {GUIDE_DESIG}, Dept. of CSE"
for r in doc.paragraphs[51].runs:
    format_run(r, font_name="Times New Roman", size_pt=12, bold=True)

# 4. Update Acknowledgement (Page 4)
print("Updating Acknowledgement...")
doc.paragraphs[73].text = (
    f"I express my sincere gratitude to my project guide Dr. Thirumalesu.K, Assistant Professor, "
    f"Department of Computer Science & Engineering, School of Technology, The Apollo University, Chittoor, "
    f"for their continuous guidance, valuable suggestions and constructive feedback throughout the course of this project. "
    f"Their support has been instrumental in the successful completion of this work."
)
for r in doc.paragraphs[73].runs:
    format_run(r, font_name="Times New Roman", size_pt=12)

doc.paragraphs[75].text = (
    "I also thank the Project Coordinator, Department of Computer Science & Engineering, School of Technology, "
    "The Apollo University for giving me the right direction whenever I came to the University."
)
for r in doc.paragraphs[75].runs:
    format_run(r, font_name="Times New Roman", size_pt=12)

doc.paragraphs[77].text = (
    "I extend my heartfelt thanks to the Programme Coordinator, Department of Computer Science & Engineering, "
    "School of Technology, The Apollo University for providing the necessary academic support and facilities to carry out this project effectively."
)
for r in doc.paragraphs[77].runs:
    format_run(r, font_name="Times New Roman", size_pt=12)

doc.paragraphs[79].text = (
    "I also convey my sincere thanks to Prof. D. Jagadeesan, Dean, School of Technology for their support and encouragement throughout the project work."
)
for r in doc.paragraphs[79].runs:
    format_run(r, font_name="Times New Roman", size_pt=12)

doc.paragraphs[81].text = (
    "I express my profound gratitude to the Honourable Chancellor Emeritus Dr Prathap C. Reddy, Dr. H. Vinod Bhat, "
    "Vice-Chancellor and Prof. M. Potharaju, Registrar of The Apollo University for their visionary leadership, constant "
    "encouragement and for fostering a supportive academic environment."
)
for r in doc.paragraphs[81].runs:
    format_run(r, font_name="Times New Roman", size_pt=12)

doc.paragraphs[83].text = (
    "I acknowledge the support of all faculty members of the department for their cooperation and valuable inputs during the project period."
)
for r in doc.paragraphs[83].runs:
    format_run(r, font_name="Times New Roman", size_pt=12)

doc.paragraphs[85].text = (
    "I would like to thank my friends and classmates for their constant encouragement and support.\n\n"
    "Finally, I express my deepest gratitude to my parents and family members for their unwavering support, motivation and blessings."
)
for r in doc.paragraphs[85].runs:
    format_run(r, font_name="Times New Roman", size_pt=12)

doc.paragraphs[90].text = STUDENT_1
doc.paragraphs[91].text = STUDENT_2
doc.paragraphs[92].text = ""
doc.paragraphs[93].text = ""

# 5. Internship Certificate Page (Page 5)
doc.paragraphs[114].text = "INTERNSHIP STUDENTS PLACE YOUR"
doc.paragraphs[115].text = "CERTIFICATE"
for r in doc.paragraphs[114].runs + doc.paragraphs[115].runs:
    format_run(r, font_name="Times New Roman", size_pt=14, bold=True)

# 6. Table of Contents (Table 0)
print("Updating Table of Contents...")
tbl_toc = doc.tables[0]
toc_rows_data = [
    ("", "ABSTRACT", "I"),
    ("", "List of Figures", "II"),
    ("", "List of Tables", "III"),
    ("", "Abbreviations", "IV"),
    ("1", "INTRODUCTION", "1"),
    ("", "1.1 Background of the Study", "1"),
    ("", "1.2 Problem Statement", "4"),
    ("", "1.3 Motivation & Objectives", "6"),
    ("", "1.4 Scope of the Project", "8"),
    ("2", "LITERATURE REVIEW", "10"),
    ("", "2.1 Introduction", "10"),
    ("", "2.2 Review of Existing Systems", "12"),
    ("", "2.3 Limitations of Existing Systems", "16"),
    ("", "2.4 Proposed System Overview", "19"),
    ("3", "OBJECTIVES AND SCHEDULE OF WORK", "22"),
    ("", "3.1 Objectives of the Project", "22"),
    ("", "3.2 Scope of the Project", "24"),
    ("", "3.3 Schedule of Work (Gantt Chart)", "26"),
    ("4", "SYSTEM ANALYSIS & DESIGN", "29"),
    ("", "4.1 System Requirements (Hardware & Software)", "29"),
    ("", "4.2 System Architecture", "32"),
    ("", "4.3 Data Flow Diagram (DFD)", "36"),
    ("", "4.4 Mathematical Formulations", "39"),
    ("5", "IMPLEMENTATION", "43"),
    ("", "5.1 Tools & Technologies Used", "43"),
    ("", "5.2 Module Description", "46"),
    ("", "5.3 Algorithms / Methods Used", "49"),
    ("", "5.4 Code Snippets", "53"),
    ("6", "RESULTS AND DISCUSSIONS", "56"),
    ("", "6.1 Output Screens / Results", "56"),
    ("", "6.2 Testing (Test Cases & Results)", "59"),
    ("", "6.3 Performance Analysis", "62"),
    ("7", "CONCLUSION AND FUTURE SCOPE", "65"),
    ("", "7.1 Conclusion", "65"),
    ("", "7.2 Future Enhancements", "67"),
    ("", "REFERENCES", "69"),
    ("", "PUBLICATIONS/CONFERENCES", "72")
]

for i in range(1, len(tbl_toc.rows)):
    if i - 1 < len(toc_rows_data):
        c0, c1, c2 = toc_rows_data[i-1]
        tbl_toc.rows[i].cells[0].text = c0
        tbl_toc.rows[i].cells[1].text = c1
        tbl_toc.rows[i].cells[2].text = c2
        for cell in tbl_toc.rows[i].cells:
            for r in cell.paragraphs[0].runs:
                format_run(r, font_name="Times New Roman", size_pt=10.5, bold=(bool(c0) or c1.isupper()))

# 7. Abstract (Page 8 / Roman I)
print("Updating Abstract...")
doc.paragraphs[163].text = "ABSTRACT"
doc.paragraphs[168].text = ABSTRACT_TEXT
doc.paragraphs[168].alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
doc.paragraphs[168].paragraph_format.line_spacing = 1.5
for r in doc.paragraphs[168].runs:
    format_run(r, font_name="Times New Roman", size_pt=12)

doc.paragraphs[170].text = f"Keywords: {', '.join(ABSTRACT_KEYWORDS)}"
for r in doc.paragraphs[170].runs:
    format_run(r, font_name="Times New Roman", size_pt=11, bold=True)

doc.paragraphs[195].text = "I"
doc.paragraphs[195].alignment = WD_ALIGN_PARAGRAPH.CENTER

# 8. List of Figures (Table 1 / Roman II)
print("Updating List of Figures...")
doc.paragraphs[196].text = "LIST OF FIGURES"
doc.paragraphs[196].alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in doc.paragraphs[196].runs:
    format_run(r, font_name="Times New Roman", size_pt=14, bold=True)

tbl_lof = doc.tables[1]
lof_entries = [
    ("Figure 3.1", "10-Week Engineering Schedule Gantt Chart", "28"),
    ("Figure 4.1", "Three-Tier On-Device Health Intelligence Architecture", "34"),
    ("Figure 4.2", "Data Flow Diagram Level 0: Context Level Representation", "37"),
    ("Figure 4.3", "Data Flow Diagram Level 1: Subsystem Functional Decomposition", "38"),
    ("Figure 4.4", "Data Flow Diagram Level 2: Detailed Process Flow for Model Execution", "39"),
    ("Figure 5.1", "Day 1 & Day 2 Demographic Baseline Calibration Interface", "57"),
    ("Figure 5.2", "Day 3+ Calibrated Activity Ring Carousel & Personal Prescriptions", "58"),
    ("Figure 6.1", "Model Compression Benchmarks (Footprint, Latency, and AUC-ROC)", "63"),
    ("Figure 6.2", "Battery Discharge Characterization (Continuous 48-Hour Profile)", "64")
]

tbl_lof.rows[0].cells[0].text = "Figure No."
tbl_lof.rows[0].cells[2].text = "Title"
tbl_lof.rows[0].cells[3].text = "Page No."

while len(tbl_lof.rows) < len(lof_entries) + 1:
    tbl_lof.add_row()

for idx, (fnum, ftitle, fpage) in enumerate(lof_entries):
    row_cells = tbl_lof.rows[idx+1].cells
    row_cells[0].text = fnum
    row_cells[2].text = ftitle
    row_cells[3].text = fpage
    for cell in row_cells:
        for r in cell.paragraphs[0].runs:
            format_run(r, font_name="Times New Roman", size_pt=10.5)

doc.paragraphs[219].text = "II"
doc.paragraphs[219].alignment = WD_ALIGN_PARAGRAPH.CENTER

# 9. List of Tables (Table 2 / Roman III)
print("Updating List of Tables...")
doc.paragraphs[220].text = "LIST OF TABLES"
doc.paragraphs[220].alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in doc.paragraphs[220].runs:
    format_run(r, font_name="Times New Roman", size_pt=14, bold=True)

tbl_lot = doc.tables[2]
lot_entries = [
    ("Table 2.1", "Comparative Architectural and Privacy Matrix: InstaHealth vs Commercial Platforms", "18"),
    ("Table 3.1", "Project Risk Assessment, Likelihood-Impact Rating, and Mitigation Matrix", "27"),
    ("Table 4.1", "Embedded Microcontroller and Biometric Hardware Sensor Specifications", "30"),
    ("Table 4.2", "InstaHealth System Comprehensive Data Dictionary and Flow Specifications", "31"),
    ("Table 4.3", "Clinically Stratified Demographic Population Baseline Lookup Table", "41"),
    ("Table 4.4", "Karvonen Heart Rate Reserve (HRR) Training Intensity Zones and Metabolic Demands", "42"),
    ("Table 5.1", "Embedded Hardware Platform Comparison and Compute Resource Allocation", "47"),
    ("Table 5.2", "Software Toolchains, Libraries, Compilers, and Runtime Dependencies", "48"),
    ("Table 5.3", "InstaHealth Multi-Profile Avatar Sandboxing and Namespace Partitioning", "49"),
    ("Table 6.1", "Comprehensive System Test Cases (TC01 to TC12) and Experimental Validation Results", "59"),
    ("Table 6.2", "Signal Quality Index (SQI) Artifact Rejection Performance Across Activity Modalities", "60"),
    ("Table 6.3", "Empirical Model Ablation Performance: TinyML MLP vs Linear Regression vs Static Rules", "62"),
    ("Table 6.4", "On-Device Execution Latency and Memory Footprint Profile on ARM Cortex-M4F", "63"),
    ("Table 6.5", "Subsystem Current Consumption Profile and 65 mAh Battery Life Budget", "64")
]

while len(tbl_lot.rows) < len(lot_entries):
    tbl_lot.add_row()

for idx, (tnum, ttitle, tpage) in enumerate(lot_entries):
    if idx < len(tbl_lot.rows):
        row_cells = tbl_lot.rows[idx].cells
        row_cells[0].text = tnum
        row_cells[1].text = ttitle
        row_cells[2].text = tpage
        for cell in row_cells:
            for r in cell.paragraphs[0].runs:
                format_run(r, font_name="Times New Roman", size_pt=10.5)

doc.paragraphs[254].text = "III"
doc.paragraphs[254].alignment = WD_ALIGN_PARAGRAPH.CENTER

# 10. List of Abbreviations (Table 3 / Roman IV)
print("Updating List of Abbreviations...")
doc.paragraphs[255].text = "LIST OF ABBREVIATIONS"
doc.paragraphs[255].alignment = WD_ALIGN_PARAGRAPH.CENTER
for r in doc.paragraphs[255].runs:
    format_run(r, font_name="Times New Roman", size_pt=14, bold=True)

tbl_abb = doc.tables[3]
while len(tbl_abb.rows) < len(ABBREVIATIONS_LIST):
    tbl_abb.add_row()

for idx, (acronym, expansion) in enumerate(ABBREVIATIONS_LIST):
    if idx < len(tbl_abb.rows):
        tbl_abb.rows[idx].cells[0].text = acronym
        tbl_abb.rows[idx].cells[1].text = expansion
        for cell in tbl_abb.rows[idx].cells:
            for r in cell.paragraphs[0].runs:
                format_run(r, font_name="Times New Roman", size_pt=10.5)

doc.paragraphs[274].text = "IV"
doc.paragraphs[274].alignment = WD_ALIGN_PARAGRAPH.CENTER

# 11. Clear out original placeholder body paragraphs after line 275
print("Clearing placeholder template text after paragraph 275...")
for idx in range(275, len(doc.paragraphs)):
    p = doc.paragraphs[idx]
    p.text = ""
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)

# ==============================================================================
# INJECT FULL 7 CHAPTERS (15,000+ WORDS ACROSS 60+ PAGES)
# ==============================================================================
print("Injecting comprehensive 7 academic chapters...")

# Chapter 1
add_heading_1(doc, CHAPTER_1_TITLE)
for sec in CH1_SECTIONS:
    render_section_content(doc, sec)
doc.add_page_break()

# Chapter 2
add_heading_1(doc, CHAPTER_2_TITLE)
for sec in CH2_SECTIONS:
    render_section_content(doc, sec)
    if sec["id"] == "2.3":
        add_table_data(doc, "table_2_1")
doc.add_page_break()

# Chapter 3
add_heading_1(doc, CHAPTER_3_TITLE)
for sec in CH3_SECTIONS:
    render_section_content(doc, sec)
    if sec["id"] == "3.3":
        add_table_data(doc, "table_3_1")
doc.add_page_break()

# Chapter 4
add_heading_1(doc, CHAPTER_4_TITLE)
for sec in CH4_SECTIONS:
    render_section_content(doc, sec)
    if sec["id"] == "4.1":
        add_table_data(doc, "table_4_1")
    elif sec["id"] == "4.3":
        add_table_data(doc, "table_4_2")
    elif sec["id"] == "4.4":
        add_table_data(doc, "table_4_3")
        add_table_data(doc, "table_4_4")
doc.add_page_break()

# Chapter 5
add_heading_1(doc, CHAPTER_5_TITLE)
for sec in CH5_SECTIONS:
    render_section_content(doc, sec)
    if sec["id"] == "5.1":
        add_table_data(doc, "table_5_1")
        add_table_data(doc, "table_5_2")
    elif sec["id"] == "5.2":
        add_table_data(doc, "table_5_3")
doc.add_page_break()

# Chapter 6
add_heading_1(doc, CHAPTER_6_TITLE)
for sec in CH6_SECTIONS:
    render_section_content(doc, sec)
    if sec["id"] == "6.2":
        add_table_data(doc, "table_6_1")
        add_table_data(doc, "table_6_2")
    elif sec["id"] == "6.3":
        add_table_data(doc, "table_6_3")
        add_table_data(doc, "table_6_4")
        add_table_data(doc, "table_6_5")
doc.add_page_break()

# Chapter 7
add_heading_1(doc, CHAPTER_7_TITLE)
for sec in CH7_SECTIONS:
    render_section_content(doc, sec)
doc.add_page_break()

# REFERENCES
add_heading_1(doc, "REFERENCES")
p_ref_guide = add_para(doc, "(For reference use the style given below, cite the reference in the text using “[1]” brackets)\nFont: Times new roman, 12pt.\nExample:\n[1] Author 1, Author 2, Article title, Journal name (italics), Year, Volume no., Page number", italic=True)
p_ref_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER

add_heading_2(doc, "Institutional Citation Style Examples:")
template_refs = [
    "Journal Article : with Single Author\nWaldron S, Generalized Welch bound equality sequences are tight frames, IEEE Transactions on Information Theory, 2008, vol. 49, pp. 2307-2309.",
    "2. Journal Article : with Two Authors\nConley TG & Galeson, DW, Nativity and wealth in mid-nineteenth century cities, Journal of Economic History, 1998, vol. 58, no. 2, pp. 468-493.",
    "3. Journal Article : with more than two Authors\nAlishahi K, Marvasti F, Aref VA & Pad P, Bounds on the sum capacity of synchronous binary CDMA channels, Journal of Chemical Education, 2009, vol. 55, no.8, pp. 3577-3593.",
    "4. Books\nHolt DH, Management Principles and Practices, 1997, Prentice-Hall, Sydney.",
    "5. E-book\nAghion, P & Durlauf S (eds.), Handbook of Economic Growth, 2005, Elsevier, Amsterdam.",
    "6. Conference Proceeding Paper with editors\nRiley D, Industrial relations in Australian education, in Contemporary Australasian industrial relations: proceedings of the sixth AIRAANZ conference, 1992, ed. D. Blackmur, AIRAANZ, Sydney, pp. 124-140.",
    "7. Conference Proceeding Paper without editors\nFan W, Gordon MD & Pathak R, Personalization of search engine services for effective retrieval and knowledge management, Proceedings of the twenty-first international conference on information systems, 2000, pp. 20-34.",
    "8. Website\nAustralian Securities Exchange, Market Information, 2009. Available from: <http://www.asx.com.au/professionals/market_information/index.htm>. [5 July 2009].",
    "9. Patent\nCookson AH, Particle trap for compressed gas insulated transmission systems, 1985, US Patent 4554399."
]
for t_ref in template_refs:
    add_para(doc, t_ref, size=11, space_after=4)

add_heading_2(doc, "Project Technical Literature Citations:")
for ref in REFERENCES_LIST:
    add_para(doc, ref, size=11, space_after=4)

# PUBLICATIONS / CONFERENCES
doc.add_page_break()
add_heading_1(doc, "PUBLICATIONS/CONFERENCES")
add_para(doc, "Attach the first page of re-print of the published article if any.\nAttach the conference proceedings (first page and your article page) and presentation certificate if any.", italic=True)
add_heading_2(doc, PUBLICATION_SUMMARY["paper_title"])
add_para(doc, f"Authors: {PUBLICATION_SUMMARY['authors']}", bold=True)
add_para(doc, f"Venue: {PUBLICATION_SUMMARY['conference']}")
add_para(doc, f"Affiliations: {PUBLICATION_SUMMARY['affiliations']}")
add_para(doc, f"Index Terms: {PUBLICATION_SUMMARY['keywords']}")
add_para(doc, f"Abstract: {PUBLICATION_SUMMARY['abstract']}")

print(f"Saving final 60+ page DOCX to {OUT_DOCX_WS}...")
doc.save(OUT_DOCX_WS)
shutil.copyfile(OUT_DOCX_WS, OUT_DOCX_DL)
shutil.copyfile(OUT_DOCX_WS, os.path.join(ARTIFACT_DIR, "InstaHealth_60_Page_Official_Apollo_Report.docx"))
print("DOCX successfully generated and saved to Workspace and Downloads!")

# ==============================================================================
# BUILD SYNCHRONIZED HTML & RENDER PDF VIA CHROME HEADLESS
# ==============================================================================
print("Generating publication HTML & PDF...")

with open("generate_academic_pdf.py", "r") as f:
    pdf_gen_code = f.read()

# Replace the title and color overrides in generate_academic_pdf.py
pdf_gen_code = pdf_gen_code.replace(
    "<h1>INSTAHEALTH: A PRIVACY-PRESERVING ZERO-CLOUD ON-DEVICE SMARTWATCH HEALTH INTELLIGENCE SYSTEM WITH ADAPTIVE MULTI-PROFILE PHYSIOLOGICAL MODELING</h1>",
    f"<h1>{PROJECT_TITLE}</h1>"
)
pdf_gen_code = pdf_gen_code.replace(
    'color: #1F3763;',
    'color: #000000;'
)
pdf_gen_code = pdf_gen_code.replace(
    'border-left: 3px solid #2563EB;',
    'border-left: 3px solid #000000;'
)
pdf_gen_code = pdf_gen_code.replace(
    'max-width: 175px;',
    'max-width: 135px;'
)
pdf_gen_code = pdf_gen_code.replace(
    'min-height: 92vh;',
    'min-height: 84vh;'
)
pdf_gen_code = pdf_gen_code.replace(
    'PDF_PATH = os.path.join(WORKSPACE_DIR, "InstaHealth_60_Page_Project_Report.pdf")',
    f'PDF_PATH = "{OUT_PDF_WS}"'
)

with open("generate_official_65page_pdf.py", "w") as f:
    f.write(pdf_gen_code)

print("Executing generate_official_65page_pdf.py...")
subprocess.run([sys.executable, "generate_official_65page_pdf.py"], check=True)

# Sanitize PDF with pypdf to ensure ISO standard xref table and zero stream errors
print("Sanitizing PDF xref tables for universal Canva and viewer compatibility...")
reader = pypdf.PdfReader(OUT_PDF_WS)
total_pages = len(reader.pages)
print(f"Rendered PDF page count: {total_pages} pages!")

writer = pypdf.PdfWriter()
for page in reader.pages:
    writer.add_page(page)

with open(OUT_PDF_WS, "wb") as f:
    writer.write(f)

shutil.copyfile(OUT_PDF_WS, OUT_PDF_DL)
shutil.copyfile(OUT_PDF_WS, os.path.join(ARTIFACT_DIR, "InstaHealth_60_Page_Official_Apollo_Report.pdf"))

print(f"SUCCESS! Official Apollo University Report generated: {total_pages} pages!")
print(f"Files saved:\n- {OUT_DOCX_WS}\n- {OUT_DOCX_DL}\n- {OUT_PDF_WS}\n- {OUT_PDF_DL}")
