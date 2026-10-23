# ON-DEVICE PERSONALIZED HEALTH EVENT PREDICTION USING TINYML AND ON-DEVICE SMALL LANGUAGE MODELS FOR PRIVACY-PRESERVING HEALTH ANALYTICS

**A Project Report**  
*Submitted by*  
**A . Jathin Reddy ( reg no : 122311520105)**  
**K.Pranay Kumar (reg.no : 122311520133)**  

*in partial fulfillment for the award of the degree of*  
**Bachelor of Technology**  
*in*  
**Computer Science and Engineering (AI & DS)**  

*Under the Guidance of*  
**Dr. Thirumalesu.K**  
*Assistant Professor*  

<p align="center"><img src="/Users/jathinreddy/.gemini/antigravity/brain/f353d961-e7fd-445e-894a-a4a5c051abdb/apollo_logo.png" width="200" alt="The Apollo University Logo"/></p>

**SCHOOL OF TECHNOLOGY**  
**DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING**  
**THE APOLLO UNIVERSITY, CHITTOOR**  
**April, 2026**  

---

# DECLARATION
I hereby declare that the project entitled “ON-DEVICE PERSONALIZED HEALTH EVENT PREDICTION USING TINYML AND ON-DEVICE SMALL LANGUAGE MODELS FOR PRIVACY-PRESERVING HEALTH ANALYTICS” submitted by us to The Apollo University is a record of bonafide work carried out under the supervision of Dr. Thirumalesu.K, Assistant Professor, Department of Computer Science & Engineering.

**Signature of Candidate(s):**  
1. A . Jathin Reddy ( reg no : 122311520105) &nbsp;&nbsp;&nbsp;&nbsp; ____________________  
2. K.Pranay Kumar (reg.no : 122311520133) &nbsp;&nbsp;&nbsp;&nbsp; ____________________  

**Place:** Chittoor  
**Date:** April, 2026  

---

# BONAFIDE CERTIFICATE
This is to certify that the project report entitled “ON-DEVICE PERSONALIZED HEALTH EVENT PREDICTION USING TINYML AND ON-DEVICE SMALL LANGUAGE MODELS FOR PRIVACY-PRESERVING HEALTH ANALYTICS” is the bonafide work carried out by A . Jathin Reddy ( reg no : 122311520105) and K.Pranay Kumar (reg.no : 122311520133) under my supervision.

**Signature of the Guide:**  
**Dr. Thirumalesu.K**, Assistant Professor, Dept. of CSE  

---

# ABSTRACT
Continuous biometric telemetry gathered from consumer wearable devices offers immense potential for preemptive healthcare risk prediction, such as early detection of cardiac arrhythmia, sudden falls, and dehydration. However, conventional commercial health monitoring frameworks mandate streaming raw physiological time-series data to centralized cloud servers, introducing severe user privacy vulnerabilities, cloud dependency, and communication latency. This project presents an on-device, privacy-preserving predictive health intelligence system leveraging Tiny Machine Learning (TinyML) and quantized Small Language Models (TinyLlama-1.1B). The architecture incorporates multimodal sensor ingestion, on-device temporal feature extraction, 4-bit/8-bit integer quantization, attention-based local explainability, and decentralized federated learning (FedAvg). Experimental validation on embedded hardware confirms that the quantized pipeline delivers accurate event forecasting with 480 ms inference latency and 620 MB peak RAM footprint, completely eliminating raw physiological data transmission to external servers.

**Keywords:** TinyML, On-Device Inference, Small Language Models, Privacy-Preserving Health Analytics, Federated Learning.

---

# FIGURES & ARCHITECTURAL VISUALS

### Figure 3.1: 10-Week Engineering Schedule
![Figure 3.1: Gantt Schedule](/Users/jathinreddy/.gemini/antigravity/brain/f353d961-e7fd-445e-894a-a4a5c051abdb/fig_miniproject_gantt.png)

### Figure 4.1: System Architecture
![Figure 4.1: System Architecture](/Users/jathinreddy/.gemini/antigravity/brain/f353d961-e7fd-445e-894a-a4a5c051abdb/fig_miniproject_arch.png)

### Figure 4.2: Data Flow Diagram (DFD Level 1)
![Figure 4.2: DFD Level 1](/Users/jathinreddy/.gemini/antigravity/brain/f353d961-e7fd-445e-894a-a4a5c051abdb/fig_miniproject_dfd.png)

### Figure 6.1: TinyLlama Model Compression Profile
![Figure 6.1: Compression Profile](/Users/jathinreddy/.gemini/antigravity/brain/f353d961-e7fd-445e-894a-a4a5c051abdb/fig_miniproject_perf.png)

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
