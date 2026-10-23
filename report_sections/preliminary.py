"""Preliminary Pages for InstaHealth Project Report:
Title, Declaration, Bonafide Certificate, Acknowledgement, Table of Contents,
Abstract, List of Figures, List of Tables, List of Abbreviations.
"""

TITLE_DATA = {
    "title": "INSTAHEALTH: A PRIVACY-PRESERVING ZERO-CLOUD ON-DEVICE SMARTWATCH HEALTH INTELLIGENCE SYSTEM WITH ADAPTIVE MULTI-PROFILE PHYSIOLOGICAL MODELING",
    "subtitle": "A Project Report",
    "submission_text": "Submitted by",
    "students": [
        ("A. JATHIN REDDY", "122311520105"),
        ("K. PRANAY KUMAR", "122311520133")
    ],
    "degree_text": "in partial fulfillment for the award of the degree\nof\nBachelor of Technology\nin\nComputer Science & Engineering",
    "guide_header": "Under the Guidance of",
    "guide_name": "Dr. Thirumalesu.K",
    "guide_title": "Assistant Professor, Department of Computer Science & Engineering",
    "institution": "SCHOOL OF TECHNOLOGY\nDEPARTMENT OF COMPUTER SCIENCE & ENGINEERING\nTHE APOLLO UNIVERSITY, CHITTOOR",
    "date": "April, 2026"
}

DECLARATION_TEXT = (
    "We hereby declare that the project entitled “INSTAHEALTH: A PRIVACY-PRESERVING ZERO-CLOUD "
    "ON-DEVICE SMARTWATCH HEALTH INTELLIGENCE SYSTEM WITH ADAPTIVE MULTI-PROFILE PHYSIOLOGICAL MODELING” "
    "submitted by us, for the award of the degree of Bachelor of Technology in Computer Science & Engineering, "
    "School of Technology to The Apollo University is a record of bonafide work carried out by us under the "
    "supervision of Dr. Thirumalesu.K, Assistant Professor, Department of Computer Science & Engineering.\n\n"
    "We further declare that the work reported in this thesis has not been submitted and will not be submitted, "
    "either in part or in full, for the award of any other degree or diploma in this institute or any other institute or university."
)

BONAFIDE_CERTIFICATE_TEXT = (
    "This is to certify that the project report entitled “INSTAHEALTH: A PRIVACY-PRESERVING ZERO-CLOUD "
    "ON-DEVICE SMARTWATCH HEALTH INTELLIGENCE SYSTEM WITH ADAPTIVE MULTI-PROFILE PHYSIOLOGICAL MODELING” "
    "is the bonafide work carried out by A. JATHIN REDDY (Register No: 122311520105) and K. PRANAY KUMAR "
    "(Register No: 122311520133), under my supervision and guidance, in partial fulfillment of the requirements "
    "for the award of the degree of Bachelor of Technology in Computer Science & Engineering by The Apollo University, Chittoor."
)

ACKNOWLEDGEMENT_PARAGRAPHS = [
    "We express our sincere gratitude to our project guide Dr. Thirumalesu.K, Assistant Professor, Department of Computer Science & Engineering, School of Technology, The Apollo University, Chittoor, for his continuous guidance, valuable suggestions and constructive feedback throughout the course of this project. His academic rigor and support have been instrumental in the successful completion of this work.",
    "We also thank the Project Coordinator, Department of Computer Science & Engineering, School of Technology, The Apollo University for providing direction, structured milestone reviews, and invaluable technical counsel throughout the progression of this research.",
    "We extend our heartfelt thanks to the Programme Coordinator, Department of Computer Science & Engineering, School of Technology, The Apollo University for providing the necessary academic support, laboratories, and computing infrastructure to carry out this project effectively.",
    "We convey our sincere thanks to Prof. D. Jagadeesan, Dean, School of Technology, for his encouragement, leadership, and administrative support throughout the tenure of our project work.",
    "We express our profound gratitude to the Honourable Chancellor Emeritus Dr. Prathap C. Reddy, Dr. H. Vinod Bhat, Vice-Chancellor, and Prof. M. Potharaju, Registrar of The Apollo University for their visionary leadership, institutional inspiration, and continuous fostering of a vibrant research and innovation culture.",
    "We gratefully acknowledge the support of all faculty members and technical staff of the Department of Computer Science & Engineering for their cooperation, critical reviews, and valuable inputs during the project period.",
    "We also thank our fellow classmates, peers, and friends for their camaraderie, constructive debates, and collaborative assistance during the experimental benchmarking phases.",
    "Finally, we express our deepest gratitude to our parents and family members for their unconditional love, moral support, patient understanding, and perpetual blessings throughout our academic journey."
]

ABSTRACT_TEXT = (
    "Modern wearable health intelligence predominantly relies on continuous cloud transmission of raw photoplethysmography "
    "(PPG) and inertial telemetry, introducing profound privacy vulnerabilities, non-ephemeral data exposure, and high energy "
    "overheads. Concurrently, commercial wearables enforce static normative population thresholds that disregard individual "
    "circadian rhythms, athletic conditioning, and accumulated recovery deficits. This project introduces InstaHealth, a "
    "strictly zero-cloud, privacy-preserving on-device smartwatch health intelligence system featuring adaptive multi-profile "
    "physiological modeling. InstaHealth executes entirely within the resource constraints of wearable microcontrollers without "
    "network permissions. The architecture integrates a real-time Signal Quality Index (SQI) motion-artifact filter, a 48-hour "
    "autonomous calibration state machine transitioning from clinically grounded Tanaka and Gulati demographic priors to personalized "
    "baselines, and an on-device TinyML Multi-Layer Perceptron utilizing micro-batch Stochastic Gradient Descent with bounded gradient "
    "clipping (|ΔW| ≤ 0.05). Sandboxed multi-profile isolation enables concurrent, zero-leakage tracking across disparate athletic "
    "personas. Deployed and evaluated on embedded smartwatch runtimes, InstaHealth achieves a 62.4% reduction in target prediction "
    "Mean Absolute Error over static population baselines, executes forward inference in 1.18 ms with 18.2 KB RAM utilization, and "
    "sustains 52.8 hours continuous operation on a standard 65 mAh battery cell, demonstrating sovereign, clinically rigorous personal health intelligence."
)

ABSTRACT_KEYWORDS = [
    "Edge Computing",
    "On-Device TinyML",
    "Zero-Cloud Privacy",
    "Adaptive Physiological Modeling",
    "Smartwatch Health Intelligence"
]

TOC_ENTRIES = [
    ("DECLARATION", "", "ii"),
    ("BONAFIDE CERTIFICATE", "", "iii"),
    ("ACKNOWLEDGEMENT", "", "iv"),
    ("ABSTRACT", "", "I"),
    ("LIST OF FIGURES", "", "II"),
    ("LIST OF TABLES", "", "III"),
    ("LIST OF ABBREVIATIONS", "", "IV"),
    ("CHAPTER 1: INTRODUCTION", "", "1"),
    ("  1.1 Background and Context", "1.1", "1"),
    ("  1.2 Problem Statement", "1.2", "2"),
    ("  1.3 Motivation and Research Questions", "1.3", "3"),
    ("  1.4 Overview of Proposed Solution and Key Contributions", "1.4", "4"),
    ("  1.5 Organization of the Project Report", "1.5", "5"),
    ("CHAPTER 2: LITERATURE REVIEW", "", "6"),
    ("  2.1 Introduction to Wearable Health Informatics", "2.1", "6"),
    ("  2.2 Review of Existing Wearable Systems & Commercial Health Platforms", "2.2", "7"),
    ("    2.2.1 Cloud-Centric Wearables and Privacy Vulnerabilities", "2.2.1", "7"),
    ("    2.2.2 Static Normative Health Thresholds vs. Adaptive Modeling", "2.2.2", "8"),
    ("    2.2.3 Edge AI and TinyML in Wearable Computing", "2.2.3", "9"),
    ("  2.3 Comparative Limitations of Existing Work", "2.3", "11"),
    ("  2.4 Proposed System Overview and Theoretical Foundations", "2.4", "12"),
    ("    2.4.1 Tanaka, Gulati, and Karvonen Heart Rate Reserve Formulations", "2.4.1", "12"),
    ("    2.4.2 Belenky Sleep Debt Accumulation and Homeostatic Recovery", "2.4.2", "13"),
    ("    2.4.3 On-Device Edge Learning via Micro-SGD", "2.4.3", "13"),
    ("CHAPTER 3: OBJECTIVES AND SCOPE OF WORK", "", "14"),
    ("  3.1 Project Objectives", "3.1", "14"),
    ("    3.1.1 Primary Research Objectives", "3.1.1", "14"),
    ("    3.1.2 Specific Functional and Engineering Objectives", "3.1.2", "15"),
    ("  3.2 Scope of the Project", "3.2", "16"),
    ("    3.2.1 In-Scope Capabilities and Features", "3.2.1", "16"),
    ("    3.2.2 Out-of-Scope Constraints and Delimitations", "3.2.2", "17"),
    ("  3.3 Schedule of Work and Project Planning", "3.3", "17"),
    ("    3.3.1 Detailed 12-Week Milestone Breakdown", "3.3.1", "17"),
    ("    3.3.2 Gantt Schedule Diagram", "3.3.2", "18"),
    ("    3.3.3 Risk Assessment and Mitigation Matrix", "3.3.3", "19"),
    ("CHAPTER 4: SYSTEM ANALYSIS & DESIGN", "", "20"),
    ("  4.1 Requirements Analysis", "4.1", "20"),
    ("    4.1.1 Functional Requirements", "4.1.1", "20"),
    ("    4.1.2 Non-Functional Requirements", "4.1.2", "21"),
    ("    4.1.3 Hardware and Embedded Sensor Specifications", "4.1.3", "22"),
    ("  4.2 System Architecture Design", "4.2", "23"),
    ("    4.2.1 Multi-Layered On-Device Architecture Overview", "4.2.1", "23"),
    ("    4.2.2 Hardware Sensor & Ingestion Subsystem", "4.2.2", "24"),
    ("    4.2.3 Profile Sandboxing & Cryptographic Separation Subsystem", "4.2.3", "24"),
    ("    4.2.4 Physiological Inference Engine & Adaptive TinyML Module", "4.2.4", "25"),
    ("    4.2.5 Glanceable UI & Circular Gauge Rendering Subsystem", "4.2.5", "25"),
    ("  4.3 Data Flow Diagrams (DFDs)", "4.3", "26"),
    ("    4.3.1 Context Level DFD (Level 0)", "4.3.1", "26"),
    ("    4.3.2 Subsystem Level DFD (Level 1)", "4.3.2", "27"),
    ("    4.3.3 Detailed Process Flow DFD (Level 2)", "4.3.3", "28"),
    ("    4.3.4 Comprehensive Data Dictionary and Entity Descriptions", "4.3.4", "29"),
    ("  4.4 Physiological Modeling and Mathematical Formulations", "4.4", "30"),
    ("    4.4.1 Maximum Heart Rate Modeling (Tanaka & Gulati Equations)", "4.4.1", "30"),
    ("    4.4.2 Karvonen Heart Rate Reserve (HRR) and Zone Stratification", "4.4.2", "31"),
    ("    4.4.3 Belenky Multi-Night Sleep Debt Carryover Formulation", "4.4.3", "31"),
    ("    4.4.4 Adaptive Exponential Moving Average (EMA) Baseline Tracking", "4.4.4", "32"),
    ("    4.4.5 Micro-SGD On-Device Learning & Gradient Bounding", "4.4.5", "32"),
    ("CHAPTER 5: IMPLEMENTATION", "", "33"),
    ("  5.1 Tools, Frameworks, and Operating Environments", "5.1", "33"),
    ("    5.1.1 Embedded Hardware Platforms and System Specifications", "5.1.1", "33"),
    ("    5.1.2 Software Libraries, Frameworks, and Toolchains", "5.1.2", "34"),
    ("    5.1.3 Development Environment, Tooling, and Testbenches", "5.1.3", "35"),
    ("  5.2 Detailed Subsystem and Module Descriptions", "5.2", "35"),
    ("    5.2.1 Module 1: Continuous Biosignal Ingestion & Quality Filtering", "5.2.1", "35"),
    ("    5.2.2 Module 2: Demographic Baseline Stratification & Profile Manager", "5.2.2", "36"),
    ("    5.2.3 Module 3: 48-Hour Calibration State Machine", "5.2.3", "36"),
    ("    5.2.4 Module 4: Dynamic Prescription Synthesis Generator", "5.2.4", "37"),
    ("    5.2.5 Module 5: On-Device TinyML Micro-SGD Optimization Engine", "5.2.5", "37"),
    ("    5.2.6 Module 6: Glanceable Canvas-Based Circular Ring Visualizer", "5.2.6", "38"),
    ("  5.3 Algorithmic Workflows and Methods", "5.3", "38"),
    ("    5.3.1 Algorithm 5.1: Real-Time Signal Quality Index (SQI) and Artifact Filter", "5.3.1", "38"),
    ("    5.3.2 Algorithm 5.2: 48-Hour Multi-Phase Calibration State Machine", "5.3.2", "39"),
    ("    5.3.3 Algorithm 5.3: On-Device Micro-SGD Bounded Weight Descent", "5.3.3", "40"),
    ("    5.3.4 Algorithm 5.4: Dynamic Health Metric Prescription Synthesis", "5.3.4", "40"),
    ("  5.4 Core Implementation Source Code Listings", "5.4", "41"),
    ("    Listing 5.1: High-Frequency Biosignal Ingestion & Moving Average Filter", "5.4.1", "41"),
    ("    Listing 5.2: Clinical Demographic Baseline Stratification & HRmax Calculator", "5.4.2", "41"),
    ("    Listing 5.3: TinyML 2-Layer Perceptron Forward Pass and Micro-SGD Optimizer", "5.4.3", "42"),
    ("    Listing 5.4: High-Performance Canvas Circular Arc Visualizer", "5.4.4", "42"),
    ("CHAPTER 6: RESULTS AND DISCUSSION", "", "43"),
    ("  6.1 User Interface and Operational Output Screens", "6.1", "43"),
    ("    6.1.1 Calibration Phase Display (Day 1 & Day 2)", "6.1.1", "43"),
    ("    6.1.2 Fully Calibrated Prescription Display (Day 3+)", "6.1.2", "44"),
    ("    6.1.3 Multi-Profile Persona Switching Output", "6.1.3", "45"),
    ("  6.2 Experimental Testing and Validation Results", "6.2", "46"),
    ("    6.2.1 Test Methodology, Hardware Setup, and Test Matrix", "6.2.1", "46"),
    ("    6.2.2 Comprehensive Test Cases (TC01 to TC12) Execution Results", "6.2.2", "46"),
    ("    6.2.3 Signal Quality Index & Motion Artifact Rejection Testing", "6.2.3", "48"),
    ("  6.3 Performance Analysis and Ablation Study", "6.3", "49"),
    ("    6.3.1 Comparative Accuracy: TinyML MLP vs. Linear Regression vs. Static Rules", "6.3.1", "49"),
    ("    6.3.2 On-Device Execution Latency and Memory Footprint Profile", "6.3.2", "50"),
    ("    6.3.3 Power Consumption & 48-Hour Battery Life Analysis", "6.3.3", "51"),
    ("    6.3.4 Detailed Discussion, Clinical Grounding, and Key Insights", "6.3.4", "52"),
    ("CHAPTER 7: CONCLUSION AND FUTURE SCOPE", "", "54"),
    ("  7.1 Conclusion", "7.1", "54"),
    ("    7.1.1 Summary of Contributions", "7.1.1", "54"),
    ("    7.1.2 Impact on Wearable Privacy and Preventive Healthcare", "7.1.2", "55"),
    ("  7.2 Future Enhancements and Research Directions", "7.2", "55"),
    ("    7.2.1 Multi-Modal Sensor Expansion (SpO2, ECG, Cortisol EDA)", "7.2.1", "56"),
    ("    7.2.2 Federated Privacy-Preserving Differential Learning", "7.2.2", "56"),
    ("    7.2.3 Ultra-Quantized Edge Large Language Models for Conversational Health", "7.2.3", "57"),
    ("REFERENCES", "", "58"),
    ("PUBLICATIONS / CONFERENCES", "", "61")
]

FIGURES_LIST = [
    ("Figure 3.1", "InstaHealth 12-Week Comprehensive Project Engineering Gantt Schedule", "18"),
    ("Figure 4.1", "InstaHealth Multi-Layered Zero-Cloud On-Device Smartwatch Architecture", "23"),
    ("Figure 4.2", "Data Flow Diagram (DFD) Level 0: Context Level System Representation", "26"),
    ("Figure 4.3", "Data Flow Diagram (DFD) Level 1: Subsystem Level Functional Decomposition", "27"),
    ("Figure 4.4", "Data Flow Diagram (DFD) Level 2: Detailed Process Flow for TinyML Micro-SGD Engine", "28"),
    ("Figure 5.1", "InstaHealth 48-Hour On-Device Calibration and Lifecycle State Machine Workflow", "36"),
    ("Figure 6.1", "InstaHealth Day 1 & Day 2 Calibration UI: Real-Time Telemetry vs Demographic Benchmarks", "43"),
    ("Figure 6.2", "InstaHealth Day 3+ Calibrated Prescription UI: Multi-Metric Circular Ring Carousel", "44"),
    ("Figure 6.3", "Empirical Ablation Study: Mean Absolute Error (MAE) Across Physiological Models", "49"),
    ("Figure 6.4", "Hardware Subsystem Current Draw Profile and 48-Hour Smartwatch Battery Budget", "51")
]

TABLES_LIST = [
    ("Table 2.1", "Comparative Architectural and Privacy Matrix: InstaHealth vs Commercial Platforms", "11"),
    ("Table 3.1", "Project Risk Assessment, Likelihood-Impact Rating, and Architectural Mitigation Matrix", "19"),
    ("Table 4.1", "Embedded Microcontroller and Biometric Hardware Sensor Specifications", "22"),
    ("Table 4.2", "InstaHealth System Comprehensive Data Dictionary and Flow Specifications", "29"),
    ("Table 4.3", "Clinically Stratified Demographic Population Baseline Lookup Table", "30"),
    ("Table 4.4", "Karvonen Heart Rate Reserve (HRR) Training Intensity Zones and Metabolic Demands", "31"),
    ("Table 5.1", "Embedded Hardware Platform Comparison and Compute Resource Allocation", "33"),
    ("Table 5.2", "Software Toolchains, Libraries, Compilers, and Runtime Dependencies", "34"),
    ("Table 5.3", "InstaHealth Multi-Profile Avatar Sandboxing and Namespace Partitioning", "36"),
    ("Table 6.1", "Comprehensive System Test Cases (TC01 to TC12) and Experimental Validation Results", "46"),
    ("Table 6.2", "Signal Quality Index (SQI) Artifact Rejection Performance Across Activity Modalities", "48"),
    ("Table 6.3", "Empirical Model Ablation Performance: TinyML MLP vs Linear Regression vs Static Rules", "49"),
    ("Table 6.4", "On-Device Execution Latency and Memory Footprint Profile on ARM Cortex-M4F", "50"),
    ("Table 6.5", "Subsystem Current Consumption Profile and 65 mAh Battery Life Budget", "51")
]

ABBREVIATIONS_LIST = [
    ("API", "Application Programming Interface"),
    ("BLE", "Bluetooth Low Energy"),
    ("BPM", "Beats Per Minute"),
    ("CDC", "Centers for Disease Control and Prevention"),
    ("CMSIS-NN", "Cortex Microcontroller Software Interface Standard - Neural Network"),
    ("DFD", "Data Flow Diagram"),
    ("DMA", "Direct Memory Access"),
    ("DSP", "Digital Signal Processing"),
    ("ECG", "Electrocardiogram"),
    ("EDA", "Electrodermal Activity"),
    ("EEPROM", "Electrically Erasable Programmable Read-Only Memory"),
    ("EMA", "Exponential Moving Average"),
    ("FFT", "Fast Fourier Transform"),
    ("FPU", "Floating Point Unit"),
    ("GDPR", "General Data Protection Regulation"),
    ("GUI", "Graphical User Interface"),
    ("HIPAA", "Health Insurance Portability and Accountability Act"),
    ("HR", "Heart Rate"),
    ("HRmax", "Maximum Heart Rate"),
    ("HRR", "Heart Rate Reserve"),
    ("HRV", "Heart Rate Variability"),
    ("IMU", "Inertial Measurement Unit"),
    ("INT8", "8-Bit Signed Integer Quantization"),
    ("IoT", "Internet of Things"),
    ("MAE", "Mean Absolute Error"),
    ("MCU", "Microcontroller Unit"),
    ("MLP", "Multi-Layer Perceptron"),
    ("MSE", "Mean Squared Error"),
    ("PPG", "Photoplethysmography"),
    ("PWA", "Progressive Web Application"),
    ("RAM", "Random Access Memory"),
    ("ReLU", "Rectified Linear Unit"),
    ("RMSSD", "Root Mean Square of Successive Differences"),
    ("ROM", "Read-Only Memory"),
    ("SaMD", "Software as a Medical Device"),
    ("SGD", "Stochastic Gradient Descent"),
    ("SoC", "System on Chip"),
    ("SQI", "Signal Quality Index"),
    ("SRAM", "Static Random Access Memory"),
    ("TFLM", "TensorFlow Lite for Microcontrollers"),
    ("TinyML", "Tiny Machine Learning"),
    ("UI", "User Interface"),
    ("UX", "User Experience"),
    ("VO2 Max", "Maximal Oxygen Consumption Rate"),
    ("WHO", "World Health Organization")
]
