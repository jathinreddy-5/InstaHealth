"""Chapter 3: Objectives and Scope of Work
Detailed academic articulation of primary research objectives, engineering goals,
in-scope and out-of-scope boundaries, 12-week schedule with Gantt chart reference,
and comprehensive risk mitigation matrix.
"""

CHAPTER_3_TITLE = "CHAPTER 3: OBJECTIVES AND SCOPE OF WORK"

SECTIONS = [
    {
        "id": "3.1",
        "title": "3.1 Project Objectives",
        "paragraphs": [
            "The overarching purpose of the InstaHealth project is to develop and validate a fully autonomous, privacy-preserving, on-device smartwatch health intelligence system that supersedes conventional cloud-dependent architectures and static population heuristics. To achieve this vision, the project defines specific primary research objectives and detailed engineering objectives."
        ],
        "subsections": [
            {
                "id": "3.1.1",
                "title": "3.1.1 Primary Research Objectives",
                "paragraphs": [
                    "The primary research objectives governing this investigation are formulated as follows:",
                    "1. Guarantee Absolute Physiological Data Sovereignty: Prove the feasibility of deploying an end-to-end continuous health intelligence system that operates in an entirely air-gapped configuration. The system must establish a zero-cloud invariant, requiring zero external server connections, zero network socket allocations, and zero telemetry exfiltration, thereby providing mathematical immunity against remote eavesdropping, data broker monetization, and cloud breaches.",
                    "2. Formulate and Validate an Autonomous On-Device Calibration Paradigm: Design a deterministic state machine that bridges the gap between cold-start demographic population priors and individual biological baselines. The system must autonomously assimilate continuous optical and inertial biosignals over a standardized 48-hour continuous wear cycle, achieving statistical convergence without requiring cloud-side batch processing, external paired smartphones, or clinical calibration procedures.",
                    "3. Engineer a Bounded On-Device Micro-Learning Optimization Engine: Develop a lightweight, quantized Multi-Layer Perceptron (MLP) capable of executing continuous incremental weight updates via micro-batch Stochastic Gradient Descent (Micro-SGD) directly on embedded microcontrollers. The engine must incorporate rigorous mathematical gradient bounding (|ΔW| ≤ 0.05) to eliminate catastrophic weight drift and divergence under noisy sensor conditions.",
                    "4. Implement Cryptographically Isolated Multi-Profile Sandboxing: Architect a multi-tenant embedded storage model capable of hosting multiple distinct athletic and physiological personas on a single wearable physical device with mathematical guarantees of zero inter-profile cross-talk, memory leakage, or baseline corruption."
                ]
            },
            {
                "id": "3.1.2",
                "title": "3.1.2 Specific Functional and Engineering Objectives",
                "paragraphs": [
                    "To translate the primary research objectives into functional embedded software, the following concrete engineering goals were established:",
                    "• Biosignal Ingestion and Quality Filtering: Engineer an embedded sensor ingestion pipeline sampling optical PPG at 25 Hz and triaxial accelerometry at 50 Hz. Implement a real-time Signal Quality Index (SQI) algorithm capable of detecting and rejecting motion-induced noise artifacts, preventing corrupt telemetry from degrading downstream physiological models.",
                    "• Clinical Prior Grounding: Construct an on-device ROM lookup matrix containing age- and sex-stratified normative baselines across five clinical cohorts (18-29, 30-39, 40-49, 50-59, 60+), integrating the clinically validated Tanaka (male) and Gulati (female) maximum heart rate regression formulas.",
                    "• Dynamic Multi-Metric Prescription Synthesis: Replace static targets with closed-loop dynamic prescriptions. Synthesize daily targets for nocturnal sleep need (incorporating the Belenky sleep debt carryover model with λ = 0.5), cardiovascular strain limits (derived from the Karvonen Heart Rate Reserve), adaptive step goals, and hourly sedentary movement alerts.",
                    "• High-Performance Glanceable Circular Display: Develop an ultra-low-power, high-DPI circular gauge rendering engine optimized for smartwatch displays (360x360 to 454x454 pixels). The visualizer must maintain a stable 60 fps refresh rate with smooth anti-aliased arcs, dynamic color blending, and swipe-driven carousel navigation.",
                    "• Extreme Embedded Resource Budgeting: Constrain the entire system footprint to under 50 KB of Flash ROM and under 20 KB of active SRAM. Maintain an average operational current draw below 1.35 mA, thereby guaranteeing at least 48 to 52 hours of continuous operation on a standard 65 mAh smartwatch lithium-ion cell."
                ]
            }
        ]
    },
    {
        "id": "3.2",
        "title": "3.2 Scope of the Project",
        "paragraphs": [
            "To maintain rigorous scientific focus and engineering feasibility within embedded microcontroller constraints, the functional scope and operational boundaries of InstaHealth are clearly delimited into in-scope capabilities and out-of-scope constraints."
        ],
        "subsections": [
            {
                "id": "3.2.1",
                "title": "3.2.1 In-Scope Capabilities and Features",
                "paragraphs": [
                    "The operational capabilities falling strictly within the scope of this project include:",
                    "1. Standalone On-Device Firmware Execution: Deployment and continuous execution on wrist-worn embedded environments, specifically Apple watchOS (Series 7 through Ultra 2), Google Wear OS (v4+), and an air-gapped HTML5/WebAssembly progressive web application (PWA) container operating in an offline sandbox.",
                    "2. Sensor Telemetry Processing: Continuous ingestion, rolling-buffer management, and digital filtering of wrist optical PPG (photoplethysmography), triaxial MEMS accelerometry, and hardware pedometer step event registers.",
                    "3. Physiological Metrics and Indices: Real-time calculation of instantaneous heart rate (bpm), root mean square of successive differences (RMSSD) heart rate variability, Karvonen Heart Rate Reserve percentage (% HRR), active calorie expenditure via MET-based kinetic estimation, nocturnal sleep duration, and cumulative sleep debt.",
                    "4. Autonomous Calibration State Lifecycle: Complete automated progression across Day 1 (UNCALIBRATED: Prior vs You), Day 2 (CALIBRATING: Tracking convergence), and Day 3+ (CALIBRATED: Dynamic daily prescriptions).",
                    "5. Local Multi-Profile Isolation: Support for four distinct user personas (Runner, Meditator, Cyclist, Swimmer) utilizing emoji-keyed namespace isolation, each maintaining private demographic configurations, physiological baselines, and weight parameters.",
                    "6. Persistent Non-Volatile Storage: Local state serialization to encrypted Flash/EEPROM or isolated browser localStorage, guaranteeing resilience against sudden battery depletion and device power cycles."
                ]
            },
            {
                "id": "3.2.2",
                "title": "3.2.2 Out-of-Scope Constraints and Delimitations",
                "paragraphs": [
                    "The deliberate boundaries and operational exclusions of this research project comprise:",
                    "1. Medical Diagnostic SaMD Certification: InstaHealth is engineered as an intelligent wellness, preventive conditioning, and personal physiological surveillance system. It is explicitly not certified as a Class II or Class III Software as a Medical Device (SaMD) under FDA or European CE Medical Device Regulations. It does not provide definitive clinical diagnoses for acute pathologies such as atrial fibrillation, myocardial ischemia, or obstructive sleep apnea.",
                    "2. Remote Physician Portals and Cloud Telemetry: The system deliberately excludes all cloud-based electronic health record (EHR) synchronization, remote physician telemetry dashboards, and multi-user centralized web databases to preserve its zero-cloud data sovereignty guarantee.",
                    "3. Direct Cellular Radio Communication: The firmware explicitly disables and avoids all cellular radio (eSIM/LTE/5G) modem utilization to eliminate RF power drain and prevent unauthorized background data transmission.",
                    "4. Invasive / Specialized Clinical Sensors: The current architecture does not ingest continuous blood glucose (CGM), blood pressure via tonometry, or invasive venous biomarkers, confining its inputs to non-invasive wrist-worn optical and inertial sensors."
                ]
            }
        ]
    },
    {
        "id": "3.3",
        "title": "3.3 Schedule of Work and Project Planning",
        "paragraphs": [
            "The engineering development and experimental validation of InstaHealth were systematically executed across a rigorous 12-week schedule, organized into six consecutive phases of two weeks each."
        ],
        "subsections": [
            {
                "id": "3.3.1",
                "title": "3.3.1 Detailed 12-Week Milestone Breakdown",
                "paragraphs": [
                    "The comprehensive milestone breakdown across the 12-week development lifecycle is structured as follows:",
                    "• Phase 1 (Weeks 1–2: Requirements Analysis, Literature Review & Dataset Grounding): Conducted a systematic review of commercial wearable architectures, privacy attack surfaces, and physiological modeling literature. Extracted and normalized normative demographic baselines across five clinical cohorts from CDC NHANES and Framingham Heart Study public repositories. Formulated project requirements and functional boundaries.",
                    "• Phase 2 (Weeks 3–4: System Architecture & Mathematical Modeling): Formalized the multi-layered on-device architectural topology. Derived the mathematical equations for Tanaka and Gulati maximum heart rate modeling, Karvonen Heart Rate Reserve intensity stratification, Belenky sleep debt carryover dynamics, and bounded Micro-SGD gradient backpropagation. Developed Context Level 0, Subsystem Level 1, and Process Level 2 Data Flow Diagrams.",
                    "• Phase 3 (Weeks 5–6: Biosignal Ingestion Engine & SQI Filtering): Implemented the continuous sensor ingestion pipeline on ARM Cortex-M4F and web sandbox environments. Developed the real-time rolling buffer and the Signal Quality Index (SQI) algorithm for optical PPG motion artifact rejection. Validated ingestion stability under mechanical shaker vibration.",
                    "• Phase 4 (Weeks 7–8: TinyML Micro-SGD Engine & Multi-Profile Sandboxing): Constructed the 2-layer quantized Multi-Layer Perceptron (5 inputs, 8 hidden neurons, 3 outputs). Implemented on-device backpropagation with hard gradient clipping (|ΔW| ≤ 0.05). Designed and verified the emoji-keyed namespace partitioning engine for multi-profile athletic personas.",
                    "• Phase 5 (Weeks 9–10: Glanceable Circular UI & Canvas Visualization): Engineered the high-performance circular gauge visualizer using high-DPI HTML5 Canvas. Developed anti-aliased arc rendering, smooth 60 fps state transitions, color-coded strain zones, and touch-driven carousel navigation for calibrated prescriptions. Optimized layout for 360x360 and 454x454 smartwatch screens.",
                    "• Phase 6 (Weeks 11–12: Hardware Profiling, Ablation Testing & Documentation): Deployed the system on Nordic PPK2 power profiling testbenches to measure subsystem current draw and battery endurance. Executed the complete test suite (TC01 to TC12). Conducted empirical ablation studies comparing TinyML against linear regression and static rules. Compiled comprehensive project documentation, figures, and research paper."
                ]
            },
            {
                "id": "3.3.2",
                "title": "3.3.2 Gantt Schedule Diagram",
                "paragraphs": [
                    "The sequential progression, phase dependencies, and milestone delivery dates of the 12-week schedule are visually represented in Figure 3.1.",
                    "[FIGURE 3.1: GANTT CHART]",
                    "As illustrated in Figure 3.1, each phase built directly upon the validated artifacts of preceding milestones, ensuring continuous integration, rigorous verification at every architectural layer, and strict adherence to institutional project completion deadlines."
                ]
            },
            {
                "id": "3.3.3",
                "title": "3.3.3 Risk Assessment and Mitigation Matrix",
                "paragraphs": [
                    "Embedded medical IoT development presents multifaceted risks across hardware noise, algorithmic divergence, memory constraints, and platform power limitations. Table 3.1 details the identified engineering risks, their probability and severity ratings, and the architectural mitigations implemented within InstaHealth.",
                    "By deploying these architectural mitigations—specifically hard gradient clipping, Signal Quality Index thresholding, wear-leveling flash writes, and DMA sensor buffering—InstaHealth achieved exceptional operational stability, recording zero system crashes, memory leaks, or unhandled exceptions across thousands of hours of automated hardware testing."
                ]
            }
        ]
    }
]
