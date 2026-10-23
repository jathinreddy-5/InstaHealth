#!/usr/bin/env python3
"""Builds the complete 60-page academic project report by directly using the
official institutional template docx:
/Users/jathinreddy/.gemini/antigravity/brain/f353d961-e7fd-445e-894a-a4a5c051abdb/.user_uploaded/media_1792773194544_9aa85a32.docx
Preserving 100% of the original university layout, logo, styles, and tables,
while populating all sections with rigorous 60-page content, 11 figures, and 14 tables.
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

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
OUTPUT_DOCX = "/Users/jathinreddy/Desktop/InstaHealth/InstaHealth_60_Page_Project_Report.docx"
OUTPUT_MD = "/Users/jathinreddy/Desktop/InstaHealth/InstaHealth_60_Page_Project_Report.md"
WORKSPACE_DIR = "/Users/jathinreddy/Desktop/InstaHealth"

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

def format_para_runs(p, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color=None):
    for r in p.runs:
        r.font.name = font_name
        r.font.size = Pt(size_pt)
        r.bold = bold
        r.italic = italic
        if color:
            r.font.color.rgb = color

def add_para(doc, text="", size=12, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, space_before=0, line_spacing=1.5, color=None):
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
    p = add_para(doc, text, size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=14, line_spacing=1.5, color=RGBColor(30, 58, 138))
    return p

def add_heading_2(doc, text):
    p = add_para(doc, text, size=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=14, space_after=6, line_spacing=1.5, color=RGBColor(15, 23, 42))
    return p

def add_heading_3(doc, text):
    p = add_para(doc, text, size=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=4, line_spacing=1.5, color=RGBColor(30, 41, 59))
    return p

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
        r_cap.font.color.rgb = RGBColor(51, 65, 85)
        return p_cap
    else:
        print(f"Warning: Image file not found: {img_path}")
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
            <w:left w:val="single" w:sz="24" w:space="0" w:color="3B82F6"/>
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

def add_table_data(doc, table_key):
    tdata = TABLES.get(table_key)
    if not tdata:
        return
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(12)
    p_cap.paragraph_format.space_after = Pt(6)
    r_cap = p_cap.add_run(tdata["title"])
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(10.5)
    r_cap.bold = True
    r_cap.font.color.rgb = RGBColor(30, 58, 138)
    
    cols = len(tdata["headers"])
    rows = len(tdata["rows"]) + 1
    table = doc.add_table(rows=rows, cols=cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="94A3B8", sz="4", val="single")
    
    hdr_cells = table.rows[0].cells
    for c_idx, title in enumerate(tdata["headers"]):
        cell = hdr_cells[c_idx]
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(title)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    for r_idx, row in enumerate(tdata["rows"]):
        row_cells = table.rows[r_idx + 1].cells
        bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            cell = row_cells[c_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (c_idx > 0 and len(val) < 25) else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.0)
            r.font.color.rgb = RGBColor(15, 23, 42)
            
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(8)

def render_paragraph_or_element(doc, p_text):
    if p_text.startswith("Algorithm ") or p_text.startswith("// =="):
        add_code_snippet(doc, p_text)
    elif p_text == "[FIGURE 3.1: GANTT CHART]":
        add_image_figure(doc, os.path.join(WORKSPACE_DIR, "fig_gantt_chart.png"),
                         "Figure 3.1: InstaHealth 12-Week Comprehensive Project Engineering Gantt Schedule", width_in=5.8)
    elif p_text == "[FIGURE 4.1: SYSTEM ARCHITECTURE]":
        add_image_figure(doc, os.path.join(WORKSPACE_DIR, "fig_3_1_architecture.png"),
                         "Figure 4.1: InstaHealth Multi-Layered Zero-Cloud On-Device Smartwatch Architecture", width_in=5.8)
    elif p_text == "[FIGURE 4.2: DFD LEVEL 0]":
        add_image_figure(doc, os.path.join(WORKSPACE_DIR, "fig_dfd_level0.png"),
                         "Figure 4.2: Data Flow Diagram (DFD) Level 0: Context Level System Representation", width_in=5.8)
    elif p_text == "[FIGURE 4.3: DFD LEVEL 1]":
        add_image_figure(doc, os.path.join(WORKSPACE_DIR, "fig_dfd_level1.png"),
                         "Figure 4.3: Data Flow Diagram (DFD) Level 1: Subsystem Level Functional Decomposition", width_in=5.8)
    elif p_text == "[FIGURE 4.4: DFD LEVEL 2]":
        add_image_figure(doc, os.path.join(WORKSPACE_DIR, "fig_dfd_level2.png"),
                         "Figure 4.4: Data Flow Diagram (DFD) Level 2: Detailed Process Flow for TinyML Micro-SGD Engine", width_in=5.8)
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
                         "Figure 6.3: Empirical Ablation Study: Mean Absolute Error (MAE) Across Physiological Models", width_in=5.8)
    elif p_text == "[FIGURE 6.4: BATTERY POWER PROFILE]":
        add_image_figure(doc, os.path.join(WORKSPACE_DIR, "fig_battery_chart.png"),
                         "Figure 6.4: Hardware Subsystem Current Draw Profile and 48-Hour Smartwatch Battery Budget", width_in=5.8)
    else:
        add_para(doc, p_text, size=12, space_after=6, line_spacing=1.5)

def render_section_content(doc, sec):
    add_heading_2(doc, sec["title"])
    for p_text in sec.get("paragraphs", []):
        render_paragraph_or_element(doc, p_text)
    
    for sub in sec.get("subsections", []):
        add_heading_3(doc, sub["title"])
        for p_text in sub.get("paragraphs", []):
            render_paragraph_or_element(doc, p_text)

print(f"Loading official institutional template from: {TEMPLATE_DOCX}")
doc = docx.Document(TEMPLATE_DOCX)

# ==============================================================================
# 1. UPDATE TITLE PAGE PARAGRAPHS (Retaining original styles & Apollo Logo at P20)
# ==============================================================================
print("Updating Title Page with exact student and guide details...")
doc.paragraphs[0].text = "INSTAHEALTH: A PRIVACY-PRESERVING ZERO-CLOUD ON-DEVICE SMARTWATCH HEALTH INTELLIGENCE SYSTEM WITH ADAPTIVE MULTI-PROFILE PHYSIOLOGICAL MODELING"
doc.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
format_para_runs(doc.paragraphs[0], font_name="Times New Roman", size_pt=18, bold=True, color=RGBColor(30, 58, 138))

# Clear template instruction line "(Times new roman pt.18)"
doc.paragraphs[1].text = ""

# Student Names
doc.paragraphs[6].text = "A . Jathin Reddy ( reg no : 122311520105)"
doc.paragraphs[6].alignment = WD_ALIGN_PARAGRAPH.CENTER
format_para_runs(doc.paragraphs[6], font_name="Times New Roman", size_pt=13, bold=True)

doc.paragraphs[7].text = "K.Pranay Kumar (reg.no : 122311520133)"
doc.paragraphs[7].alignment = WD_ALIGN_PARAGRAPH.CENTER
format_para_runs(doc.paragraphs[7], font_name="Times New Roman", size_pt=13, bold=True)

# Clear unused candidate lines 3 & 4
doc.paragraphs[8].text = ""
doc.paragraphs[9].text = ""

# Guide Details
doc.paragraphs[19].text = "Dr. Thirumalesu.K\nAssistant Professor, Department of Computer Science & Engineering"
doc.paragraphs[19].alignment = WD_ALIGN_PARAGRAPH.CENTER
format_para_runs(doc.paragraphs[19], font_name="Times New Roman", size_pt=13, bold=True)

# Note: doc.paragraphs[20] holds the exact Apollo University logo image! Preserved untouched.
doc.paragraphs[25].text = "April, 2026"
doc.paragraphs[25].alignment = WD_ALIGN_PARAGRAPH.CENTER
format_para_runs(doc.paragraphs[25], font_name="Times New Roman", size_pt=12, bold=True)

# ==============================================================================
# 2. UPDATE DECLARATION
# ==============================================================================
print("Updating Declaration...")
doc.paragraphs[30].text = (
    "   I hereby declare that the project entitled “INSTAHEALTH: A PRIVACY-PRESERVING ZERO-CLOUD ON-DEVICE "
    "SMARTWATCH HEALTH INTELLIGENCE SYSTEM WITH ADAPTIVE MULTI-PROFILE PHYSIOLOGICAL MODELING” submitted by us, "
    "for the award of the degree of Bachelor of Technology in Computer Sciences & Engineering, School of Technology "
    "to The Apollo University is a record of bonafide work carried out by us under the supervision of Dr. Thirumalesu.K, "
    "Assistant Professor, Department of Computer Science & Engineering."
)
format_para_runs(doc.paragraphs[30], font_name="Times New Roman", size_pt=12)

doc.paragraphs[31].text = (
    "   We further declare that the work reported in this thesis has not been submitted and will not be submitted, "
    "either in part or in full, for the award of any other degree or diploma in this institute or any other institute or university."
)
format_para_runs(doc.paragraphs[31], font_name="Times New Roman", size_pt=12)

doc.paragraphs[34].text = "                                                                           1. A . Jathin Reddy ( reg no : 122311520105)        ____________________"
format_para_runs(doc.paragraphs[34], font_name="Times New Roman", size_pt=11)
doc.paragraphs[35].text = "                                                                           2. K.Pranay Kumar (reg.no : 122311520133)        ____________________"
format_para_runs(doc.paragraphs[35], font_name="Times New Roman", size_pt=11)

doc.paragraphs[37].text = "Place\t: Chittoor"
format_para_runs(doc.paragraphs[37], font_name="Times New Roman", size_pt=12)
doc.paragraphs[38].text = "     Date\t: April, 2026"
format_para_runs(doc.paragraphs[38], font_name="Times New Roman", size_pt=12)

# ==============================================================================
# 3. UPDATE BONAFIDE CERTIFICATE
# ==============================================================================
print("Updating Bonafide Certificate...")
doc.paragraphs[47].text = (
    "         This is to certify that the project report entitled “INSTAHEALTH: A PRIVACY-PRESERVING ZERO-CLOUD "
    "ON-DEVICE SMARTWATCH HEALTH INTELLIGENCE SYSTEM WITH ADAPTIVE MULTI-PROFILE PHYSIOLOGICAL MODELING” "
    "is the bonafide work carried out by A . Jathin Reddy (Register No: 122311520105) and K.Pranay Kumar "
    "(Register No: 122311520133), under my supervision and guidance, in partial fulfillment of the requirements "
    "for the award of the degree of Bachelor of Technology in Computer Sciences & Engineering by The Apollo University, Chittoor."
)
format_para_runs(doc.paragraphs[47], font_name="Times New Roman", size_pt=12)

doc.paragraphs[51].text = (
    "                                                                                                Signature of the Guide\n"
    "                                                                                                Dr. Thirumalesu.K\n"
    "                                                                                                Assistant Professor, Dept. of CSE"
)
format_para_runs(doc.paragraphs[51], font_name="Times New Roman", size_pt=11, bold=True)

# ==============================================================================
# 4. UPDATE ACKNOWLEDGEMENT
# ==============================================================================
print("Updating Acknowledgement...")
doc.paragraphs[73].text = (
    "I express my sincere gratitude to my project guide Dr. Thirumalesu.K, Assistant Professor, "
    "Computer Sciences & Engineering, School of Technology, The Apollo University, Chittoor, for their continuous guidance, "
    "valuable suggestions and constructive feedback throughout the course of this project. Their support has been instrumental "
    "in the successful completion of this work."
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

doc.paragraphs[90].text = "A . Jathin Reddy ( reg no : 122311520105)"
format_para_runs(doc.paragraphs[90], font_name="Times New Roman", size_pt=11, bold=True)
doc.paragraphs[91].text = "K.Pranay Kumar (reg.no : 122311520133)"
format_para_runs(doc.paragraphs[91], font_name="Times New Roman", size_pt=11, bold=True)
doc.paragraphs[92].text = ""
doc.paragraphs[93].text = ""

# ==============================================================================
# 5. UPDATE TABLE 0 (TABLE OF CONTENTS)
# ==============================================================================
print("Updating Table 0 (Table of Contents)...")
toc_tbl = doc.tables[0]
toc_page_map = {
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "1",
    6: "1",
    7: "2",
    8: "6",
    9: "6",
    10: "7",
    11: "11",
    12: "12",
    13: "14",
    14: "14",
    15: "16",
    16: "20",
    17: "20",
    18: "23",
    19: "26",
    20: "33",
    21: "33",
    22: "35",
    23: "38",
    24: "41",
    25: "43",
    26: "43",
    27: "46",
    28: "49",
    29: "54",
    30: "54",
    31: "55",
    32: "58",
    33: "61"
}

for row_idx, page_val in toc_page_map.items():
    if row_idx < len(toc_tbl.rows):
        cell = toc_tbl.rows[row_idx].cells[2]
        cell.text = page_val
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        format_para_runs(p, font_name="Times New Roman", size_pt=10, bold=(row_idx in [5, 8, 13, 16, 20, 25, 29, 32, 33]))

# ==============================================================================
# 6. UPDATE ABSTRACT
# ==============================================================================
print("Updating Abstract...")
doc.paragraphs[168].text = ABSTRACT_TEXT
format_para_runs(doc.paragraphs[168], font_name="Times New Roman", size_pt=12)
doc.paragraphs[168].paragraph_format.line_spacing = 1.5

doc.paragraphs[170].text = "Keywords: " + ", ".join(ABSTRACT_KEYWORDS)
format_para_runs(doc.paragraphs[170], font_name="Times New Roman", size_pt=11, bold=True, italic=True)

# Roman numeral I is already at paragraph 195!

# ==============================================================================
# 7. UPDATE TABLE 1 (LIST OF FIGURES)
# ==============================================================================
print("Updating Table 1 (List of Figures)...")
tbl_fig = doc.tables[1]

# Clear existing sample row in template
for row in tbl_fig.rows[1:]:
    row._element.getparent().remove(row._element)

for f_no, f_title, p_num in FIGURES_LIST:
    r = tbl_fig.add_row()
    cells = r.cells
    cells[0].text = f_no
    cells[1].text = ""
    cells[2].text = f_title
    cells[3].text = p_num
    
    for c_idx, c in enumerate(cells):
        set_cell_margins(c, top=40, bottom=40, left=60, right=60)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        align = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else (WD_ALIGN_PARAGRAPH.RIGHT if c_idx == 3 else WD_ALIGN_PARAGRAPH.LEFT)
        p.alignment = align
        format_para_runs(p, font_name="Times New Roman", size_pt=9.5, bold=(c_idx == 0))

# ==============================================================================
# 8. UPDATE TABLE 2 (LIST OF TABLES)
# ==============================================================================
print("Updating Table 2 (List of Tables)...")
tbl_tab = doc.tables[2]

for row in tbl_tab.rows:
    row._element.getparent().remove(row._element)

# Header Row
hdr_row = tbl_tab.add_row()
hdr_cells = hdr_row.cells
hdr_cells[0].text = "Table No."
hdr_cells[1].text = "Title"
hdr_cells[2].text = "Page No."
for c in hdr_cells:
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_para_runs(p, font_name="Times New Roman", size_pt=10, bold=True)

for t_no, t_title, p_num in TABLES_LIST:
    r = tbl_tab.add_row()
    cells = r.cells
    cells[0].text = t_no
    cells[1].text = t_title
    cells[2].text = p_num
    
    for c_idx, c in enumerate(cells):
        set_cell_margins(c, top=40, bottom=40, left=60, right=60)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        align = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else (WD_ALIGN_PARAGRAPH.RIGHT if c_idx == 2 else WD_ALIGN_PARAGRAPH.LEFT)
        p.alignment = align
        format_para_runs(p, font_name="Times New Roman", size_pt=9.5, bold=(c_idx == 0))

# ==============================================================================
# 9. UPDATE TABLE 3 (LIST OF ABBREVIATIONS)
# ==============================================================================
print("Updating Table 3 (List of Abbreviations)...")
tbl_abbr = doc.tables[3]

for row in tbl_abbr.rows:
    row._element.getparent().remove(row._element)

# Header Row
hdr_row = tbl_abbr.add_row()
hdr_cells = hdr_row.cells
hdr_cells[0].text = "Abbreviation"
hdr_cells[1].text = "Full Terminology"
for c in hdr_cells:
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_para_runs(p, font_name="Times New Roman", size_pt=10, bold=True)

for abbr, full_t in ABBREVIATIONS_LIST:
    r = tbl_abbr.add_row()
    cells = r.cells
    cells[0].text = abbr
    cells[1].text = full_t
    
    for c_idx, c in enumerate(cells):
        set_cell_margins(c, top=40, bottom=40, left=60, right=60)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        align = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
        p.alignment = align
        format_para_runs(p, font_name="Times New Roman", size_pt=9.5, bold=(c_idx == 0))

# ==============================================================================
# 10. REPLACE PLACEHOLDER TAIL (PARAGRAPHS 276 ONWARD) WITH COMPLETE CHAPTERS
# ==============================================================================
print("Replacing template placeholder body with full 60-page content...")
paras = list(doc.paragraphs)
for p in paras[276:]:
    p._element.getparent().remove(p._element)

# Chapter 1: Introduction
add_heading_1(doc, CHAPTER_1_TITLE)
for sec in CH1_SECTIONS:
    render_section_content(doc, sec)
doc.add_page_break()

# Chapter 2: Literature Review
add_heading_1(doc, CHAPTER_2_TITLE)
for sec in CH2_SECTIONS:
    render_section_content(doc, sec)
    if sec["id"] == "2.3":
        add_table_data(doc, "table_2_1")
doc.add_page_break()

# Chapter 3: Objectives and Scope of Work
add_heading_1(doc, CHAPTER_3_TITLE)
for sec in CH3_SECTIONS:
    render_section_content(doc, sec)
    if sec["id"] == "3.3":
        add_table_data(doc, "table_3_1")
doc.add_page_break()

# Chapter 4: System Analysis & Design
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

# Chapter 5: Implementation
add_heading_1(doc, CHAPTER_5_TITLE)
for sec in CH5_SECTIONS:
    render_section_content(doc, sec)
    if sec["id"] == "5.1":
        add_table_data(doc, "table_5_1")
        add_table_data(doc, "table_5_2")
    elif sec["id"] == "5.2":
        add_table_data(doc, "table_5_3")
doc.add_page_break()

# Chapter 6: Results and Discussion
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

# Chapter 7: Conclusion and Future Scope
add_heading_1(doc, CHAPTER_7_TITLE)
for sec in CH7_SECTIONS:
    render_section_content(doc, sec)
doc.add_page_break()

# References
add_heading_1(doc, REFERENCES_TITLE)
add_para(doc, "The references below conform strictly to institutional citation guidelines across all required publication categories (single author, two authors, more than two authors, books, e-books, conference proceedings with and without editors, websites, and patents).", size=11, italic=True, space_before=4, space_after=14)

for ref_text in REFERENCES_LIST:
    add_para(doc, ref_text, size=11, space_before=2, space_after=6, line_spacing=1.25)

doc.add_page_break()

# Publications / Conferences
add_heading_1(doc, PUBLICATIONS_TITLE)
add_para(doc, "CONFERENCE PUBLICATION PREPRINT DRAFT SUMMARY", size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=6)
add_para(doc, "Target Conference: " + PUBLICATION_SUMMARY["conference"], size=11, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=12)

add_para(doc, PUBLICATION_SUMMARY["paper_title"], size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=6, color=RGBColor(30, 58, 138))
add_para(doc, PUBLICATION_SUMMARY["authors"], size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2)
add_para(doc, PUBLICATION_SUMMARY["affiliations"], size=10, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=14)

add_para(doc, "Abstract—" + PUBLICATION_SUMMARY["abstract"], size=10.5, space_before=4, space_after=8, line_spacing=1.3)
add_para(doc, "Index Terms—" + PUBLICATION_SUMMARY["keywords"], size=10, bold=True, italic=True, space_before=2, space_after=12)

add_heading_2(doc, "I. Introduction & System Motivation")
add_para(doc, PUBLICATION_SUMMARY["section_1_intro_summary"], size=11, space_before=2, space_after=6, line_spacing=1.3)

add_heading_2(doc, "II. Proposed Edge TinyML Architecture & Micro-SGD Optimization")
add_para(doc, PUBLICATION_SUMMARY["section_2_methods_summary"], size=11, space_before=2, space_after=6, line_spacing=1.3)

add_heading_2(doc, "III. Experimental Evaluation & Hardware Benchmark Results")
add_para(doc, PUBLICATION_SUMMARY["section_3_results_summary"], size=11, space_before=2, space_after=6, line_spacing=1.3)

add_heading_2(doc, "IV. Conclusion & Edge Privacy Implications")
add_para(doc, PUBLICATION_SUMMARY["section_4_conclusion_summary"], size=11, space_before=2, space_after=14, line_spacing=1.3)

print(f"Saving compiled Word document to: {OUTPUT_DOCX}")
doc.save(OUTPUT_DOCX)
print("InstaHealth_60_Page_Project_Report.docx created successfully from official template!")

# ==============================================================================
# 11. SYNCHRONIZE MATCHING MARKDOWN DOCUMENT
# ==============================================================================
print("Generating matching Markdown document mirroring the exact template layout...")

md_lines = []
def md_h1(text): md_lines.append(f"\n# {text}\n")
def md_h2(text): md_lines.append(f"\n## {text}\n")
def md_h3(text): md_lines.append(f"\n### {text}\n")
def md_p(text): md_lines.append(f"\n{text}\n")

# Title Page
md_h1("INSTAHEALTH: A PRIVACY-PRESERVING ZERO-CLOUD ON-DEVICE SMARTWATCH HEALTH INTELLIGENCE SYSTEM WITH ADAPTIVE MULTI-PROFILE PHYSIOLOGICAL MODELING")
md_p("**(Times new roman pt.18)**  \n**A Project Report**  \n*Submitted by*  \n**A . Jathin Reddy** ( reg no : 122311520105)  \n**K.Pranay Kumar** (reg.no : 122311520133)  \n\n*in partial fulfillment for the award of the degree of*\n**Bachelor of Technology**\n*in*\n**Computer Sciences & Engineering**  \n\n*Under the Guidance of*  \n**Dr. Thirumalesu.K**  \n*Assistant Professor*")
md_p("<p align=\"center\"><img src=\"apollo_logo.png\" width=\"180\" alt=\"The Apollo University Logo\"/></p>")
md_p("**SCHOOL OF TECHNOLOGY**  \n**DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING**  \n**THE APOLLO UNIVERSITY, CHITTOOR**  \n**April, 2026**")
md_lines.append("\n---\n")

# Declaration
md_h1("DECLARATION")
md_p("   I hereby declare that the project entitled “INSTAHEALTH: A PRIVACY-PRESERVING ZERO-CLOUD ON-DEVICE SMARTWATCH HEALTH INTELLIGENCE SYSTEM WITH ADAPTIVE MULTI-PROFILE PHYSIOLOGICAL MODELING” submitted by us, for the award of the degree of Bachelor of Technology in Computer Sciences & Engineering, School of Technology to The Apollo University is a record of bonafide work carried out by us under the supervision of Dr. Thirumalesu.K, Assistant Professor, Department of Computer Science & Engineering.\n\n   We further declare that the work reported in this thesis has not been submitted and will not be submitted, either in part or in full, for the award of any other degree or diploma in this institute or any other institute or university.")
md_lines.append("**Signature of the Candidate(s) with names:**\n\n1. A . Jathin Reddy ( reg no : 122311520105)        ____________________  \n2. K.Pranay Kumar (reg.no : 122311520133)        ____________________  \n\n**Place:** Chittoor  \n**Date:** April, 2026\n")
md_lines.append("\n---\n")

# Bonafide Certificate
md_p("**THE APOLLO UNIVERSITY, CHITTOOR**  \n**SCHOOL OF TECHNOLOGY**")
md_h1("BONAFIDE CERTIFICATE")
md_p("         This is to certify that the project report entitled “INSTAHEALTH: A PRIVACY-PRESERVING ZERO-CLOUD ON-DEVICE SMARTWATCH HEALTH INTELLIGENCE SYSTEM WITH ADAPTIVE MULTI-PROFILE PHYSIOLOGICAL MODELING” is the bonafide work carried out by A . Jathin Reddy (Register No: 122311520105) and K.Pranay Kumar (Register No: 122311520133), under my supervision and guidance, in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology in Computer Sciences & Engineering by The Apollo University, Chittoor.")
md_lines.append("**Signature of the Guide**  \n**Dr. Thirumalesu.K**  \nAssistant Professor, Dept. of CSE\n\n| **Program Coordinator** | **Dean** |\n| :--- | :--- |\n| Department of Computer Science & Engineering | School of Technology |\n| The Apollo University | The Apollo University |\n\n**Internal Examiner:** _______________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **External Examiner:** _______________________\n")
md_lines.append("\n---\n")

# Acknowledgement
md_h1("ACKNOWLEDGEMENT")
md_p("I express my sincere gratitude to my project guide Dr. Thirumalesu.K, Assistant Professor, Computer Sciences & Engineering, School of Technology, The Apollo University, Chittoor, for their continuous guidance, valuable suggestions and constructive feedback throughout the course of this project. Their support has been instrumental in the successful completion of this work.")
md_p("I also thank the Project Coordinator, Department of Computer Science & Engineering, School of Technology, The Apollo University for giving me the right direction whenever I came to the University.")
md_p("I extend my heartfelt thanks to the Programme Coordinator, Department of Computer Science & Engineering, School of Technology, The Apollo University for providing the necessary academic support and facilities to carry out this project effectively.")
md_p("I also convey my sincere thanks to the Prof. D. Jagadeesan, Dean, School of Technology for their support and encouragement throughout the project work.")
md_p("I express my profound gratitude to the Honourable Chancellor Dr Prathap C. Reddy, Dr. H. Vinod Bhat, Vice-Chancellor and Prof. M. Potharaju, Registrar of The Apollo University for their visionary leadership, constant encouragement and for fostering a supportive academic environment.")
md_p("I acknowledge the support of all faculty members of the department for their cooperation and valuable inputs during the project period.")
md_p("I would like to thank my friends and classmates for their constant encouragement and support.")
md_p("Finally, I express my deepest gratitude to my parents and family members for their unwavering support, motivation and blessings.\n\n*For Internship Students*\nI would like to express my sincere gratitude to the organization for providing me with the opportunity to undergo internship training.")
md_lines.append("**A . Jathin Reddy** ( reg no : 122311520105)  \n**K.Pranay Kumar** (reg.no : 122311520133)\n\n*(INTERNSHIP STUDENTS PLACE YOUR CERTIFICATE)*\n")
md_lines.append("\n---\n")

# Table of Contents Table
md_h1("TABLE OF CONTENTS")
md_lines.append("| | CONTENTS | Page No. |\n| :--- | :--- | :---: |\n| | **ABSTRACT** | I |\n| | **List of Figures** | II |\n| | **List of Tables** | III |\n| | **Abbreviations** | IV |\n| 1 | **INTRODUCTION** | 1 |\n| | 1.1 Background of the Study | 1 |\n| | 1.2 Problem Statement | 2 |\n| 2 | **LITERATURE REVIEW** | 6 |\n| | 2.1 Introduction | 6 |\n| | 2.2 Review of Existing Systems | 7 |\n| | 2.3 Limitations of Existing Systems | 11 |\n| | 2.4 Proposed System Overview | 12 |\n| 3 | **OBJECTIVES AND SCOPE OF WORK** | 14 |\n| | 3.1 Objectives of the Project | 14 |\n| | 3.2 Scope of the Project | 16 |\n| 4 | **SYSTEM ANALYSIS & DESIGN** | 20 |\n| | 4.1 System Requirements (Hardware & Software) | 20 |\n| | 4.2 System Architecture | 23 |\n| | 4.3 Data Flow Diagram (DFD) | 26 |\n| 5 | **IMPLEMENTATION** | 33 |\n| | 5.1 Tools & Technologies Used | 33 |\n| | 5.2 Module Description | 35 |\n| | 5.3 Algorithms / Methods Used | 38 |\n| | 5.4 Code Snippets (optional) | 41 |\n| 6 | **RESULTS AND DISCUSSION** | 43 |\n| | 6.1 Output Screens / Results | 43 |\n| | 6.2 Testing (Test Cases & Results) | 46 |\n| | 6.3 Performance Analysis | 49 |\n| 7 | **CONCLUSION AND FUTURE SCOPE** | 54 |\n| | 7.1 Conclusion | 54 |\n| | 7.2 Future Enhancements | 55 |\n| | **REFERENCES** | 58 |\n| | **PUBLICATIONS/CONFERENCES** | 61 |\n")
md_lines.append("\n---\n")

# Abstract
md_h1("ABSTRACT")
md_p(ABSTRACT_TEXT)
md_p("**Keywords:** " + ", ".join(ABSTRACT_KEYWORDS))
md_p("*Page I*")
md_lines.append("\n---\n")

# List of Figures Table
md_h1("LIST OF FIGURES")
md_lines.append("| Figure No. | Title | Page No. |\n| :--- | :--- | :---: |")
for f_no, f_title, p_num in FIGURES_LIST:
    md_lines.append(f"| {f_no} | {f_title} | {p_num} |")
md_p("*Page II*")
md_lines.append("\n---\n")

# List of Tables Table
md_h1("LIST OF TABLES")
md_lines.append("| Table No. | Title | Page No. |\n| :--- | :--- | :---: |")
for t_no, t_title, p_num in TABLES_LIST:
    md_lines.append(f"| {t_no} | {t_title} | {p_num} |")
md_p("*Page III*")
md_lines.append("\n---\n")

# List of Abbreviations Table
md_h1("LIST OF ABBREVIATIONS")
md_lines.append("| Abbreviation | Full Terminology |\n| :--- | :--- |")
for abbr, full_t in ABBREVIATIONS_LIST:
    md_lines.append(f"| **{abbr}** | {full_t} |")
md_p("*Page IV*")
md_lines.append("\n---\n")

# Chapters
def md_table(tkey):
    t = TABLES.get(tkey)
    if not t: return
    md_lines.append(f"\n#### {t['title']}\n")
    headers = t["headers"]
    md_lines.append("| " + " | ".join(headers) + " |")
    md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in t["rows"]:
        clean_row = [c.replace("\n", " ") for c in row]
        md_lines.append("| " + " | ".join(clean_row) + " |")
    md_lines.append("\n")

def md_render_p_or_element(p):
    if p.startswith("Algorithm ") or p.startswith("// =="):
        md_lines.append(f"\n```javascript\n{p}\n```\n")
    elif "[FIGURE " in p:
        tag = p.strip()
        if "3.1" in tag: md_lines.append(f"\n![Figure 3.1 Gantt Chart](fig_gantt_chart.png)\n*Figure 3.1: InstaHealth 12-Week Comprehensive Project Engineering Gantt Schedule*\n")
        elif "4.1" in tag: md_lines.append(f"\n![Figure 4.1 Architecture](fig_3_1_architecture.png)\n*Figure 4.1: InstaHealth Multi-Layered Zero-Cloud On-Device Smartwatch Architecture*\n")
        elif "4.2" in tag: md_lines.append(f"\n![Figure 4.2 DFD Level 0](fig_dfd_level0.png)\n*Figure 4.2: Data Flow Diagram (DFD) Level 0: Context Level System Representation*\n")
        elif "4.3" in tag: md_lines.append(f"\n![Figure 4.3 DFD Level 1](fig_dfd_level1.png)\n*Figure 4.3: Data Flow Diagram (DFD) Level 1: Subsystem Level Functional Decomposition*\n")
        elif "4.4" in tag: md_lines.append(f"\n![Figure 4.4 DFD Level 2](fig_dfd_level2.png)\n*Figure 4.4: Data Flow Diagram (DFD) Level 2: Detailed Process Flow for TinyML Micro-SGD Engine*\n")
        elif "5.1" in tag: md_lines.append(f"\n![Figure 5.1 Workflow](fig_3_2_workflow.png)\n*Figure 5.1: InstaHealth 48-Hour On-Device Calibration and Lifecycle State Machine Workflow*\n")
        elif "6.1" in tag: md_lines.append(f"\n![Figure 6.1 Calibration UI](screenshot_day1_calibration.png)\n*Figure 6.1: InstaHealth Day 1 & Day 2 Calibration UI: Real-Time Telemetry vs Demographic Benchmarks*\n")
        elif "6.2" in tag: md_lines.append(f"\n![Figure 6.2 Prescription UI](screenshot_day3_prescriptions.png)\n*Figure 6.2: InstaHealth Day 3+ Calibrated Prescription UI: Multi-Metric Circular Ring Carousel*\n")
        elif "6.3" in tag: md_lines.append(f"\n![Figure 6.3 Ablation](fig_ablation_chart.png)\n*Figure 6.3: Empirical Ablation Study: Mean Absolute Error (MAE) Across Physiological Models*\n")
        elif "6.4" in tag: md_lines.append(f"\n![Figure 6.4 Battery Profile](fig_battery_chart.png)\n*Figure 6.4: Hardware Subsystem Current Draw Profile and 48-Hour Smartwatch Battery Budget*\n")
    else:
        md_p(p)

def md_section(sec):
    md_h2(sec["title"])
    for p in sec.get("paragraphs", []):
        md_render_p_or_element(p)
    for sub in sec.get("subsections", []):
        md_h3(sub["title"])
        for p in sub.get("paragraphs", []):
            md_render_p_or_element(p)

md_h1(CHAPTER_1_TITLE)
for s in CH1_SECTIONS: md_section(s)

md_h1(CHAPTER_2_TITLE)
for s in CH2_SECTIONS:
    md_section(s)
    if s["id"] == "2.3": md_table("table_2_1")

md_h1(CHAPTER_3_TITLE)
for s in CH3_SECTIONS:
    md_section(s)
    if s["id"] == "3.3": md_table("table_3_1")

md_h1(CHAPTER_4_TITLE)
for s in CH4_SECTIONS:
    md_section(s)
    if s["id"] == "4.1": md_table("table_4_1")
    elif s["id"] == "4.3": md_table("table_4_2")
    elif s["id"] == "4.4":
        md_table("table_4_3")
        md_table("table_4_4")

md_h1(CHAPTER_5_TITLE)
for s in CH5_SECTIONS:
    md_section(s)
    if s["id"] == "5.1":
        md_table("table_5_1")
        md_table("table_5_2")
    elif s["id"] == "5.2": md_table("table_5_3")

md_h1(CHAPTER_6_TITLE)
for s in CH6_SECTIONS:
    md_section(s)
    if s["id"] == "6.2":
        md_table("table_6_1")
        md_table("table_6_2")
    elif s["id"] == "6.3":
        md_table("table_6_3")
        md_table("table_6_4")
        md_table("table_6_5")

md_h1(CHAPTER_7_TITLE)
for s in CH7_SECTIONS: md_section(s)

md_h1(REFERENCES_TITLE)
for r in REFERENCES_LIST:
    md_lines.append(f"- {r}")

md_h1(PUBLICATIONS_TITLE)
md_p(f"### {PUBLICATION_SUMMARY['paper_title']}")
md_p(f"**Target Venue:** {PUBLICATION_SUMMARY['conference']}  \n**Authors:** {PUBLICATION_SUMMARY['authors']}  \n*{PUBLICATION_SUMMARY['affiliations']}*")
md_p(f"**Abstract:** {PUBLICATION_SUMMARY['abstract']}")
md_p(f"**Keywords:** {PUBLICATION_SUMMARY['keywords']}")
md_p(f"**I. Introduction:** {PUBLICATION_SUMMARY['section_1_intro_summary']}")
md_p(f"**II. Methodology:** {PUBLICATION_SUMMARY['section_2_methods_summary']}")
md_p(f"**III. Results:** {PUBLICATION_SUMMARY['section_3_results_summary']}")
md_p(f"**IV. Conclusion:** {PUBLICATION_SUMMARY['section_4_conclusion_summary']}")

with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print("InstaHealth_60_Page_Project_Report.md synchronized successfully!")
