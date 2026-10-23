#!/usr/bin/env python3
"""Generates a publication-grade academic PDF of the InstaHealth 60-Page Project Report
using Chrome headless, matching the Apollo University School of Technology guidelines.
"""

import os
import subprocess
import base64

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

WORKSPACE_DIR = "/Users/jathinreddy/Desktop/InstaHealth"
ARTIFACT_DIR = "/Users/jathinreddy/.gemini/antigravity/brain/f353d961-e7fd-445e-894a-a4a5c051abdb"
HTML_PATH = "/tmp/instahealth_report.html"
PDF_PATH = os.path.join(WORKSPACE_DIR, "InstaHealth_60_Page_Project_Report.pdf")

def img_to_base64(img_path):
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

logo_b64 = img_to_base64(os.path.join(WORKSPACE_DIR, "apollo_logo.png"))
gantt_b64 = img_to_base64(os.path.join(WORKSPACE_DIR, "fig_gantt_chart.png"))
arch_b64 = img_to_base64(os.path.join(WORKSPACE_DIR, "fig_3_1_architecture.png"))
dfd0_b64 = img_to_base64(os.path.join(WORKSPACE_DIR, "fig_dfd_level0.png"))
dfd1_b64 = img_to_base64(os.path.join(WORKSPACE_DIR, "fig_dfd_level1.png"))
dfd2_b64 = img_to_base64(os.path.join(WORKSPACE_DIR, "fig_dfd_level2.png"))
wf_b64 = img_to_base64(os.path.join(WORKSPACE_DIR, "fig_3_2_workflow.png"))
day1_b64 = img_to_base64(os.path.join(WORKSPACE_DIR, "screenshot_day1_calibration.png"))
day3_b64 = img_to_base64(os.path.join(WORKSPACE_DIR, "screenshot_day3_prescriptions.png"))
ablation_b64 = img_to_base64(os.path.join(WORKSPACE_DIR, "fig_ablation_chart.png"))
batt_b64 = img_to_base64(os.path.join(WORKSPACE_DIR, "fig_battery_chart.png"))

html = []
html.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>InstaHealth Project Report</title>
<style>
  @page {
    size: A4;
    margin: 25mm 20mm 20mm 25mm;
  }
  @page:right {
    @bottom-center {
      content: counter(page);
    }
  }
  body {
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
    line-height: 1.5;
    color: #000;
    margin: 0;
    padding: 0;
  }
  .page {
    page-break-after: always;
  }
  .title-page {
    text-align: center;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 92vh;
  }
  .title-page h1 {
    font-size: 15pt;
    font-weight: bold;
    line-height: 1.25;
    margin: 0 0 10px 0;
    text-transform: uppercase;
  }
  .sub-title {
    font-size: 13pt;
    font-weight: bold;
    margin: 8px 0 4px 0;
  }
  .submitted-by {
    font-size: 12pt;
    font-style: italic;
    margin: 4px 0 6px 0;
  }
  .student-name {
    font-size: 12pt;
    font-weight: bold;
    margin: 2px 0;
  }
  .degree-text {
    font-size: 11pt;
    font-style: italic;
    margin: 2px 0;
  }
  .degree-name {
    font-size: 13pt;
    font-weight: bold;
    margin: 2px 0;
  }
  .guide-label {
    font-size: 12pt;
    font-style: italic;
    margin: 6px 0 2px 0;
  }
  .guide-name {
    font-size: 12.5pt;
    font-weight: bold;
    margin: 2px 0;
  }
  .guide-desig {
    font-size: 11pt;
    margin: 2px 0;
  }
  .univ-logo {
    margin: 12px auto;
    max-width: 175px;
    height: auto;
    display: block;
  }
  .dept-header {
    font-size: 12.5pt;
    font-weight: bold;
    margin: 2px 0;
  }
  .date-header {
    font-size: 12pt;
    font-weight: bold;
    margin: 6px 0 0 0;
  }
  h1.sec-header {
    font-size: 14pt;
    font-weight: bold;
    text-align: center;
    margin: 20px 0 16px 0;
    text-transform: uppercase;
  }
  h2.sec-header {
    font-size: 12pt;
    font-weight: bold;
    text-align: left;
    margin: 18px 0 8px 0;
  }
  h3.sec-header {
    font-size: 12pt;
    font-weight: bold;
    color: #1F3763;
    text-align: left;
    margin: 14px 0 6px 0;
  }
  p {
    text-align: justify;
    text-justify: inter-word;
    margin: 0 0 8px 0;
  }
  table.content-table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 9.5pt;
  }
  table.content-table th {
    background-color: #F1F5F9;
    font-weight: bold;
    border: 1px solid #CBD5E1;
    padding: 6px 8px;
    text-align: center;
  }
  table.content-table td {
    border: 1px solid #CBD5E1;
    padding: 5px 8px;
  }
  table.content-table tr:nth-child(even) td {
    background-color: #F8FAFC;
  }
  .caption {
    font-size: 10pt;
    font-weight: bold;
    text-align: center;
    margin: 6px 0 16px 0;
  }
  .figure-box {
    text-align: center;
    margin: 16px 0;
  }
  .figure-box img {
    max-width: 90%;
    height: auto;
    display: block;
    margin: 0 auto;
    border: 1px solid #E2E8F0;
    border-radius: 4px;
  }
  .code-box {
    background-color: #F8FAFC;
    border-left: 3px solid #2563EB;
    border-top: 1px solid #E2E8F0;
    border-right: 1px solid #E2E8F0;
    border-bottom: 1px solid #E2E8F0;
    padding: 10px 14px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 9pt;
    line-height: 1.25;
    white-space: pre-wrap;
    margin: 12px 0 16px 0;
  }
  .pub-box {
    border: 1.5px solid #0F172A;
    background-color: #F8FAFC;
    padding: 16px 20px;
    margin: 16px 0;
  }
  .sig-grid {
    display: flex;
    justify-content: space-between;
    margin-top: 40px;
  }
</style>
</head>
<body>
""")

# ==============================================================================
# PAGE 1: TITLE PAGE
# ==============================================================================
html.append(f"""
<div class="title-page">
  <div>
    <h1>INSTAHEALTH: A PRIVACY-PRESERVING ZERO-CLOUD ON-DEVICE SMARTWATCH HEALTH INTELLIGENCE SYSTEM WITH ADAPTIVE MULTI-PROFILE PHYSIOLOGICAL MODELING</h1>
    <div class="sub-title">A Project Report</div>
    <div class="submitted-by">Submitted by</div>
    <div class="student-name">A . Jathin Reddy ( reg no : 122311520105)</div>
    <div class="student-name">K.Pranay Kumar (reg.no : 122311520133)</div>
    <div style="margin: 10px 0;">
      <div class="degree-text">in partial fulfillment for the award of the degree</div>
      <div class="degree-text">of</div>
      <div class="degree-name">Bachelor of Technology</div>
      <div class="degree-text">in</div>
      <div class="degree-name">Computer Sciences & Engineering</div>
    </div>
    <div>
      <div class="guide-label">Under the Guidance of</div>
      <div class="guide-name">Dr. Thirumalesu.K</div>
      <div class="guide-desig">Assistant Professor</div>
    </div>
  </div>
  <div>
    <img src="{logo_b64}" class="univ-logo" alt="The Apollo University Logo"/>
    <div class="dept-header">SCHOOL OF TECHNOLOGY</div>
    <div class="dept-header">DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING</div>
    <div class="dept-header">THE APOLLO UNIVERSITY, CHITTOOR</div>
    <div class="date-header">April, 2026</div>
  </div>
</div>
""")

# ==============================================================================
# PAGE 2: DECLARATION
# ==============================================================================
html.append(f"""
<div class="page">
  <h1 class="sec-header">DECLARATION</h1>
  <p>{DECLARATION_TEXT}</p>
  <div style="margin-top: 50px; text-align: right;">
    <p><b>Signature of the Candidate(s) with names:</b></p>
    <p style="margin-top: 25px;">1. A . Jathin Reddy ( reg no : 122311520105) &nbsp;&nbsp;&nbsp;&nbsp; ____________________</p>
    <p style="margin-top: 15px;">2. K.Pranay Kumar (reg.no : 122311520133) &nbsp;&nbsp;&nbsp;&nbsp; ____________________</p>
  </div>
  <div style="margin-top: 40px;">
    <p><b>Place&nbsp;:</b> Chittoor</p>
    <p><b>Date&nbsp;&nbsp;:</b> April, 2026</p>
  </div>
</div>
""")

# ==============================================================================
# PAGE 3: BONAFIDE CERTIFICATE
# ==============================================================================
html.append(f"""
<div class="page">
  <div style="text-align: center; margin-bottom: 25px;">
    <h2 style="font-size: 16pt; margin: 0;">THE APOLLO UNIVERSITY, CHITTOOR</h2>
    <h3 style="font-size: 13pt; margin: 4px 0;">SCHOOL OF TECHNOLOGY</h3>
    <h1 class="sec-header" style="margin-top: 25px;">BONAFIDE CERTIFICATE</h1>
  </div>
  <p>{BONAFIDE_CERTIFICATE_TEXT}</p>
  <div style="margin-top: 50px; text-align: right;">
    <p><b>Signature of the Guide</b></p>
    <p style="margin-top: 10px;"><b>Dr. Thirumalesu.K</b><br>Assistant Professor, Dept. of CSE</p>
  </div>
  <div class="sig-grid" style="margin-top: 60px;">
    <div>
      <p><b>Program Coordinator</b><br>Dept. of CSE<br>The Apollo University</p>
    </div>
    <div style="text-align: right;">
      <p><b>Dean</b><br>School of Technology<br>The Apollo University</p>
    </div>
  </div>
  <div class="sig-grid" style="margin-top: 50px;">
    <div>
      <p><b>Internal Examiner</b></p>
    </div>
    <div style="text-align: right;">
      <p><b>External Examiner</b></p>
    </div>
  </div>
</div>
""")

# ==============================================================================
# PAGE 4: ACKNOWLEDGEMENT
# ==============================================================================
html.append("""
<div class="page">
  <h1 class="sec-header">ACKNOWLEDGEMENT</h1>
""")
for ack in ACKNOWLEDGEMENT_PARAGRAPHS:
    html.append(f"<p>{ack}</p>")
html.append("""
  <p>I would like to thank my friends and classmates for their constant encouragement and support.</p>
  <p>Finally, I express my deepest gratitude to my parents and family members for their unwavering support, motivation and blessings.</p>
  <div style="margin-top: 30px; text-align: right;">
    <p><b>A . Jathin Reddy</b> ( reg no : 122311520105)</p>
    <p><b>K.Pranay Kumar</b> (reg.no : 122311520133)</p>
  </div>
</div>
""")

# ==============================================================================
# PAGE 5: TABLE OF CONTENTS
# ==============================================================================
html.append("""
<div class="page">
  <h1 class="sec-header">TABLE OF CONTENTS</h1>
  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 10%;">Chapter</th>
        <th style="width: 75%; text-align: left;">CONTENTS</th>
        <th style="width: 15%;">Page No.</th>
      </tr>
    </thead>
    <tbody>
      <tr><td></td><td><b>ABSTRACT</b></td><td style="text-align: right;">I</td></tr>
      <tr><td></td><td><b>List of Figures</b></td><td style="text-align: right;">II</td></tr>
      <tr><td></td><td><b>List of Tables</b></td><td style="text-align: right;">III</td></tr>
      <tr><td></td><td><b>Abbreviations</b></td><td style="text-align: right;">IV</td></tr>
      <tr><td style="text-align: center;"><b>1</b></td><td><b>INTRODUCTION</b></td><td style="text-align: right;"><b>1</b></td></tr>
      <tr><td></td><td style="padding-left: 20px;">1.1 Background of the Study</td><td style="text-align: right;">1</td></tr>
      <tr><td></td><td style="padding-left: 20px;">1.2 Problem Statement</td><td style="text-align: right;">3</td></tr>
      <tr><td style="text-align: center;"><b>2</b></td><td><b>LITERATURE REVIEW</b></td><td style="text-align: right;"><b>6</b></td></tr>
      <tr><td></td><td style="padding-left: 20px;">2.1 Introduction</td><td style="text-align: right;">6</td></tr>
      <tr><td></td><td style="padding-left: 20px;">2.2 Review of Existing Systems</td><td style="text-align: right;">7</td></tr>
      <tr><td></td><td style="padding-left: 20px;">2.3 Limitations of Existing Systems</td><td style="text-align: right;">11</td></tr>
      <tr><td></td><td style="padding-left: 20px;">2.4 Proposed System Overview</td><td style="text-align: right;">12</td></tr>
      <tr><td style="text-align: center;"><b>3</b></td><td><b>OBJECTIVES AND SCOPE OF WORK</b></td><td style="text-align: right;"><b>15</b></td></tr>
      <tr><td></td><td style="padding-left: 20px;">3.1 Objectives of the Project</td><td style="text-align: right;">15</td></tr>
      <tr><td></td><td style="padding-left: 20px;">3.2 Scope of the Project</td><td style="text-align: right;">17</td></tr>
      <tr><td style="text-align: center;"><b>4</b></td><td><b>SYSTEM ANALYSIS & DESIGN</b></td><td style="text-align: right;"><b>20</b></td></tr>
      <tr><td></td><td style="padding-left: 20px;">4.1 System Requirements (Hardware & Software)</td><td style="text-align: right;">20</td></tr>
      <tr><td></td><td style="padding-left: 20px;">4.2 System Architecture</td><td style="text-align: right;">23</td></tr>
      <tr><td></td><td style="padding-left: 20px;">4.3 Data Flow Diagram (DFD)</td><td style="text-align: right;">27</td></tr>
      <tr><td style="text-align: center;"><b>5</b></td><td><b>IMPLEMENTATION</b></td><td style="text-align: right;"><b>33</b></td></tr>
      <tr><td></td><td style="padding-left: 20px;">5.1 Tools & Technologies Used</td><td style="text-align: right;">33</td></tr>
      <tr><td></td><td style="padding-left: 20px;">5.2 Module Description</td><td style="text-align: right;">35</td></tr>
      <tr><td></td><td style="padding-left: 20px;">5.3 Algorithms / Methods Used</td><td style="text-align: right;">38</td></tr>
      <tr><td></td><td style="padding-left: 20px;">5.4 Code Snippets (optional)</td><td style="text-align: right;">42</td></tr>
      <tr><td style="text-align: center;"><b>6</b></td><td><b>RESULTS AND DISCUSSIONS</b></td><td style="text-align: right;"><b>45</b></td></tr>
      <tr><td></td><td style="padding-left: 20px;">6.1 Output Screens / Results</td><td style="text-align: right;">45</td></tr>
      <tr><td></td><td style="padding-left: 20px;">6.2 Testing (Test Cases & Results)</td><td style="text-align: right;">48</td></tr>
      <tr><td></td><td style="padding-left: 20px;">6.3 Performance Analysis</td><td style="text-align: right;">51</td></tr>
      <tr><td style="text-align: center;"><b>7</b></td><td><b>CONCLUSION AND FUTURE SCOPE</b></td><td style="text-align: right;"><b>55</b></td></tr>
      <tr><td></td><td style="padding-left: 20px;">7.1 Conclusion</td><td style="text-align: right;">55</td></tr>
      <tr><td></td><td style="padding-left: 20px;">7.2 Future Enhancements</td><td style="text-align: right;">56</td></tr>
      <tr><td></td><td><b>REFERENCES</b></td><td style="text-align: right;"><b>58</b></td></tr>
      <tr><td></td><td><b>PUBLICATIONS/CONFERENCES</b></td><td style="text-align: right;"><b>62</b></td></tr>
    </tbody>
  </table>
</div>
""")

# ==============================================================================
# PAGE 6: ABSTRACT
# ==============================================================================
html.append(f"""
<div class="page">
  <h1 class="sec-header">ABSTRACT</h1>
  <p>{ABSTRACT_TEXT}</p>
  <p style="margin-top: 15px;"><b>Keywords:</b> <i>{', '.join(ABSTRACT_KEYWORDS)}</i></p>
  <div style="text-align: center; margin-top: 30px; font-style: italic;">Page I</div>
</div>
""")

# ==============================================================================
# PAGE 7: LIST OF FIGURES
# ==============================================================================
html.append("""
<div class="page">
  <h1 class="sec-header">LIST OF FIGURES</h1>
  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 20%;">Figure No.</th>
        <th style="width: 65%; text-align: left;">Title</th>
        <th style="width: 15%;">Page No.</th>
      </tr>
    </thead>
    <tbody>
""")
for f_no, f_title, p_num in FIGURES_LIST:
    html.append(f"<tr><td style='text-align: center;'><b>{f_no}</b></td><td>{f_title}</td><td style='text-align: right;'>{p_num}</td></tr>")
html.append("""
    </tbody>
  </table>
  <div style="text-align: center; margin-top: 30px; font-style: italic;">Page II</div>
</div>
""")

# ==============================================================================
# PAGE 8: LIST OF TABLES
# ==============================================================================
html.append("""
<div class="page">
  <h1 class="sec-header">LIST OF TABLES</h1>
  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 20%;">Table No.</th>
        <th style="width: 65%; text-align: left;">Title</th>
        <th style="width: 15%;">Page No.</th>
      </tr>
    </thead>
    <tbody>
""")
for t_no, t_title, p_num in TABLES_LIST:
    html.append(f"<tr><td style='text-align: center;'><b>{t_no}</b></td><td>{t_title}</td><td style='text-align: right;'>{p_num}</td></tr>")
html.append("""
    </tbody>
  </table>
  <div style="text-align: center; margin-top: 30px; font-style: italic;">Page III</div>
</div>
""")

# ==============================================================================
# PAGE 9: LIST OF ABBREVIATIONS
# ==============================================================================
html.append("""
<div class="page">
  <h1 class="sec-header">LIST OF ABBREVIATIONS</h1>
  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 25%;">Abbreviation</th>
        <th style="width: 75%; text-align: left;">Full Terminology</th>
      </tr>
    </thead>
    <tbody>
""")
for abbr, full_t in ABBREVIATIONS_LIST:
    html.append(f"<tr><td style='text-align: center;'><b>{abbr}</b></td><td>{full_t}</td></tr>")
html.append("""
    </tbody>
  </table>
  <div style="text-align: center; margin-top: 30px; font-style: italic;">Page IV</div>
</div>
""")

# ==============================================================================
# BODY BUILDER HELPERS
# ==============================================================================
def render_table_html(tkey):
    t = TABLES.get(tkey)
    if not t: return ""
    out = [f"<div class='caption'>{t['title']}</div>"]
    out.append("<table class='content-table'><thead><tr>")
    for h in t["headers"]:
        out.append(f"<th>{h}</th>")
    out.append("</tr></thead><tbody>")
    for r in t["rows"]:
        out.append("<tr>")
        for val in r:
            out.append(f"<td>{val.replace(chr(10), '<br>')}</td>")
        out.append("</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)

def render_element_html(p):
    if p.startswith("Algorithm ") or p.startswith("// =="):
        return f"<div class='code-box'>{p}</div>"
    elif "[FIGURE " in p:
        tag = p.strip()
        if "3.1" in tag: return f"<div class='figure-box'><img src='{gantt_b64}'/><div class='caption'>Figure 3.1: InstaHealth 12-Week Comprehensive Project Engineering Gantt Schedule</div></div>"
        elif "4.1" in tag: return f"<div class='figure-box'><img src='{arch_b64}'/><div class='caption'>Figure 4.1: InstaHealth Multi-Layered Zero-Cloud On-Device Smartwatch Architecture</div></div>"
        elif "4.2" in tag: return f"<div class='figure-box'><img src='{dfd0_b64}'/><div class='caption'>Figure 4.2: Data Flow Diagram (DFD) Level 0: Context Level System Representation</div></div>"
        elif "4.3" in tag: return f"<div class='figure-box'><img src='{dfd1_b64}'/><div class='caption'>Figure 4.3: Data Flow Diagram (DFD) Level 1: Subsystem Level Functional Decomposition</div></div>"
        elif "4.4" in tag: return f"<div class='figure-box'><img src='{dfd2_b64}'/><div class='caption'>Figure 4.4: Data Flow Diagram (DFD) Level 2: Detailed Process Flow for TinyML Micro-SGD Engine</div></div>"
        elif "5.1" in tag: return f"<div class='figure-box'><img src='{wf_b64}'/><div class='caption'>Figure 5.1: InstaHealth 48-Hour On-Device Calibration and Lifecycle State Machine Workflow</div></div>"
        elif "6.1" in tag: return f"<div class='figure-box'><img src='{day1_b64}' style='max-width: 50%;'/><div class='caption'>Figure 6.1: InstaHealth Day 1 & Day 2 Calibration UI: Real-Time Telemetry vs Demographic Benchmarks</div></div>"
        elif "6.2" in tag: return f"<div class='figure-box'><img src='{day3_b64}' style='max-width: 50%;'/><div class='caption'>Figure 6.2: InstaHealth Day 3+ Calibrated Prescription UI: Multi-Metric Circular Ring Carousel</div></div>"
        elif "6.3" in tag: return f"<div class='figure-box'><img src='{ablation_b64}'/><div class='caption'>Figure 6.3: Empirical Ablation Study: Mean Absolute Error (MAE) Across Physiological Models</div></div>"
        elif "6.4" in tag: return f"<div class='figure-box'><img src='{batt_b64}'/><div class='caption'>Figure 6.4: Hardware Subsystem Current Draw Profile and 48-Hour Smartwatch Battery Budget</div></div>"
    else:
        return f"<p>{p}</p>"

def render_section_html(sec):
    out = [f"<h2 class='sec-header'>{sec['title']}</h2>"]
    for p in sec.get("paragraphs", []):
        out.append(render_element_html(p))
    for sub in sec.get("subsections", []):
        out.append(f"<h3 class='sec-header'>{sub['title']}</h3>")
        for p in sub.get("paragraphs", []):
            out.append(render_element_html(p))
    return "\n".join(out)

# Chapter 1
html.append(f"<div class='page'><h1 class='sec-header'>{CHAPTER_1_TITLE}</h1>")
for s in CH1_SECTIONS: html.append(render_section_html(s))
html.append("</div>")

# Chapter 2
html.append(f"<div class='page'><h1 class='sec-header'>{CHAPTER_2_TITLE}</h1>")
for s in CH2_SECTIONS:
    html.append(render_section_html(s))
    if s["id"] == "2.3": html.append(render_table_html("table_2_1"))
html.append("</div>")

# Chapter 3
html.append(f"<div class='page'><h1 class='sec-header'>{CHAPTER_3_TITLE}</h1>")
for s in CH3_SECTIONS:
    html.append(render_section_html(s))
    if s["id"] == "3.3": html.append(render_table_html("table_3_1"))
html.append("</div>")

# Chapter 4
html.append(f"<div class='page'><h1 class='sec-header'>{CHAPTER_4_TITLE}</h1>")
for s in CH4_SECTIONS:
    html.append(render_section_html(s))
    if s["id"] == "4.1": html.append(render_table_html("table_4_1"))
    elif s["id"] == "4.3": html.append(render_table_html("table_4_2"))
    elif s["id"] == "4.4":
        html.append(render_table_html("table_4_3"))
        html.append(render_table_html("table_4_4"))
html.append("</div>")

# Chapter 5
html.append(f"<div class='page'><h1 class='sec-header'>{CHAPTER_5_TITLE}</h1>")
for s in CH5_SECTIONS:
    html.append(render_section_html(s))
    if s["id"] == "5.1":
        html.append(render_table_html("table_5_1"))
        html.append(render_table_html("table_5_2"))
    elif s["id"] == "5.2": html.append(render_table_html("table_5_3"))
html.append("</div>")

# Chapter 6
html.append(f"<div class='page'><h1 class='sec-header'>{CHAPTER_6_TITLE}</h1>")
for s in CH6_SECTIONS:
    html.append(render_section_html(s))
    if s["id"] == "6.2":
        html.append(render_table_html("table_6_1"))
        html.append(render_table_html("table_6_2"))
    elif s["id"] == "6.3":
        html.append(render_table_html("table_6_3"))
        html.append(render_table_html("table_6_4"))
        html.append(render_table_html("table_6_5"))
html.append("</div>")

# Chapter 7
html.append(f"<div class='page'><h1 class='sec-header'>{CHAPTER_7_TITLE}</h1>")
for s in CH7_SECTIONS: html.append(render_section_html(s))
html.append("</div>")

# References
html.append(f"<div class='page'><h1 class='sec-header'>{REFERENCES_TITLE}</h1>")
html.append("<p style='text-align: center; font-style: italic; margin-bottom: 20px;'>(References formatted in strict IEEE / Institutional Author-Year style matching the Apollo University guidelines)</p>")
for ref in REFERENCES_LIST:
    html.append(f"<p style='margin-bottom: 10px;'>{ref}</p>")
html.append("</div>")

# Publications
html.append(f"<div class='page'><h1 class='sec-header'>{PUBLICATIONS_TITLE}</h1>")
html.append("<p style='text-align: center; font-weight: bold; margin-bottom: 20px;'>First-Page Reprint and Conference Presentation Documentation</p>")
html.append(f"""
<div class="pub-box">
  <div style="text-align: center;">
    <h3 style="font-size: 13pt; margin: 0 0 8px 0;">{PUBLICATION_SUMMARY['paper_title']}</h3>
    <p style="margin: 4px 0;"><b>Authors:</b> {PUBLICATION_SUMMARY['authors']}</p>
    <p style="margin: 2px 0; font-style: italic;">{PUBLICATION_SUMMARY['affiliations']}</p>
    <p style="margin: 6px 0;"><b>Accepted & Presented at:</b> {PUBLICATION_SUMMARY['conference']}</p>
  </div>
  <p style="margin-top: 15px;"><b>Abstract—</b> {PUBLICATION_SUMMARY['abstract']}</p>
  <p><b>Keywords—</b> <i>{PUBLICATION_SUMMARY['keywords']}</i></p>
  <h4 style="margin: 12px 0 4px 0;">I. INTRODUCTION</h4>
  <p>{PUBLICATION_SUMMARY['section_1_intro_summary']}</p>
  <h4 style="margin: 12px 0 4px 0;">II. METHODOLOGY & TINYML ARCHITECTURE</h4>
  <p>{PUBLICATION_SUMMARY['section_2_methods_summary']}</p>
  <h4 style="margin: 12px 0 4px 0;">III. EXPERIMENTAL RESULTS & ABLATION</h4>
  <p>{PUBLICATION_SUMMARY['section_3_results_summary']}</p>
  <h4 style="margin: 12px 0 4px 0;">IV. CONCLUSION & IMPACT</h4>
  <p>{PUBLICATION_SUMMARY['section_4_conclusion_summary']}</p>
</div>
</div>
""")

html.append("</body></html>")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(html))
print(f"Generated HTML report at: {HTML_PATH}")

# Call Google Chrome to print to PDF
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={PDF_PATH}",
    "--no-pdf-header-footer",
    f"file://{HTML_PATH}"
]
print("Generating publication PDF via Chrome headless...")
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if os.path.exists(PDF_PATH):
    sz = os.path.getsize(PDF_PATH)
    print(f"PDF generated successfully: {PDF_PATH} ({sz:,} bytes)")
    # Also copy to artifact directory
    subprocess.run(["cp", PDF_PATH, os.path.join(ARTIFACT_DIR, "InstaHealth_60_Page_Project_Report.pdf")])
    print("Copied PDF to artifact directory!")
else:
    print(f"Error generating PDF: {res.stderr}")
