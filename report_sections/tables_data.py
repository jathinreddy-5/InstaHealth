"""Comprehensive Data Definitions for All 14 Tables in the InstaHealth Project Report.
Contains structured table headers, alignments, and detailed data rows.
"""

TABLES = {
    "table_2_1": {
        "title": "Table 2.1: Comparative Architectural and Privacy Matrix: InstaHealth vs Commercial Platforms",
        "headers": ["Evaluation Metric / Dimension", "Apple Watch S9", "Google Pixel Watch 2", "Garmin Forerunner 965", "Whoop 4.0", "Oura Ring Gen 3", "InstaHealth (Proposed)"],
        "rows": [
            ["Cloud Independence", "Partial (Requires iCloud sync)", "No (Mandatory Google Cloud)", "Partial (Garmin Connect)", "No (Mandatory Whoop Cloud)", "No (Mandatory Oura Cloud)", "100% Zero-Cloud (Air-Gapped)"],
            ["On-Device Model Adaptation", "No (Static rules on-device)", "No (Cloud batch inference)", "No (Static algorithms)", "No (Cloud server training)", "No (Cloud ML pipelines)", "Yes (Micro-SGD TinyML on-device)"],
            ["Multi-Profile Persona Isolation", "No (Single Apple ID)", "No (Single Google Account)", "No (Single user profile)", "No (Single athlete account)", "No (Single account)", "Yes (Emoji-keyed sandboxed silos)"],
            ["Personal Baseline Window", "14–21 Days (Cloud)", "14 Days (Cloud analytics)", "7–14 Days (Cloud)", "14–30 Days (Cloud)", "14–21 Days (Cloud)", "48 Hours (Autonomous On-Device)"],
            ["Maximum HR Formulation", "Fox & Haskell (220 - Age)", "Fox & Haskell (220 - Age)", "Fox & Haskell (Adjustable)", "Proprietary Cloud Heuristic", "Resting HR only", "Tanaka (Male) / Gulati (Female)"],
            ["Sleep Debt Carryover Model", "Binary debt vs 8h target", "Generic sleep debt scores", "Static sleep coach", "Cloud homeostatic strain", "Cloud restorative sleep index", "Belenky Autoregressive (λ = 0.5)"],
            ["Active RF Radio Power Drain", "High (BLE + Wi-Fi sync)", "High (BLE + LTE/Wi-Fi)", "Medium (BLE periodic sync)", "High (Continuous BLE stream)", "Medium (Periodic BLE sync)", "Zero (RF Disabled/Air-Gapped)"],
            ["User Data Ownership & HIPAA/GDPR", "Corporate Cloud Vault", "Google Server Clusters", "Garmin Cloud Servers", "Whoop Cloud Infrastructure", "Oura Cloud Storage", "100% Sovereign (Local Hardware Only)"]
        ]
    },
    "table_3_1": {
        "title": "Table 3.1: Project Risk Assessment, Likelihood-Impact Rating, and Architectural Mitigation Matrix",
        "headers": ["Risk ID", "Risk Description", "Probability", "Impact", "Severity Score", "Architectural Mitigation Strategy"],
        "rows": [
            ["R1", "Optical PPG Motion Artifact Corruption during intense physical kinetics", "High (0.8)", "High (0.8)", "Critical (0.64)", "Real-time Signal Quality Index (SQI) evaluator; suppress parameter updates when SQI < 0.40 or Accel Variance > 1.8g."],
            ["R2", "Microcontroller Battery Depletion prior to completing 48h calibration", "Medium (0.5)", "High (0.9)", "High (0.45)", "DMA sensor transfers, 25 Hz/1 Hz dual-frequency sampling, -O3 compiler optimization, and sleep mode utilization (>92% idle)."],
            ["R3", "Catastrophic Neural Weight Drift caused by transient sensor spikes", "Medium (0.4)", "Critical (1.0)", "High (0.40)", "Hard gradient clipping invariant (|ΔW| ≤ 0.05); conservative learning rate η = 0.01; bounded parameter delta enforcement."],
            ["R4", "Flash Memory Wear and Degradation from continuous baseline updates", "Low (0.2)", "High (0.8)", "Moderate (0.16)", "In-memory SRAM ring buffering; commit baseline parameters to non-volatile Flash only once every 24 hours at diurnal cycle close."],
            ["R5", "Cross-Profile Memory Leakage across athletic personas", "Low (0.2)", "High (0.9)", "Moderate (0.18)", "Strict emoji-keyed namespace sandboxing; segregated memory pointers; automated zero-fill buffer clearing upon context swap."],
            ["R6", "Operating System Background Execution Suspension / Watchdog Termination", "Medium (0.4)", "Medium (0.6)", "Moderate (0.24)", "Split micro-tasks to guarantee all execution steps finish within 5 ms; interface with native background health service APIs."]
        ]
    },
    "table_4_1": {
        "title": "Table 4.1: Embedded Microcontroller and Biometric Hardware Sensor Specifications",
        "headers": ["Hardware Subsystem", "Component / Sensor Model", "Operational Parameter", "Target Engineering Specification"],
        "rows": [
            ["Microcontroller Unit (MCU)", "ARM Cortex-M4F / Cortex-M33", "Clock Frequency & Core Architecture", "64 MHz, 32-bit RISC with hardware FPU & DSP instructions"],
            ["Embedded Memory", "On-Chip SRAM and Flash ROM", "Memory Capacity & Partitioning", "256 KB SRAM, 1024 KB internal Flash ROM"],
            ["Optical Biosensor (PPG)", "Maxim Integrated MAX30102 / OSRAM", "Wavelengths, Sampling Rate & ADC", "Dual Green (525 nm) & IR (940 nm), 25 Hz active / 1 Hz resting, 18-bit ADC"],
            ["Inertial Measurement (IMU)", "Bosch Sensortec BMA400 / ST LIS2DW12", "Axes, Dynamic Range & Sampling Rate", "Triaxial Accelerometer (X, Y, Z), ±8g range, 50 Hz, 16-bit resolution"],
            ["Display Panel", "Circular AMOLED Touch Panel", "Resolution, Color Depth & Refresh Rate", "1.4–1.9 inch, 454×454 circular pixels (326 ppi), 24-bit RGB, 60 Hz"],
            ["Power Source", "Rechargeable Lithium-Polymer Cell", "Nominal Voltage & Energy Capacity", "3.70 V DC, 65 mAh nominal capacity (240.5 mWh energy)"],
            ["Haptic Transducer", "Linear Resonant Actuator (LRA)", "Resonant Frequency & Acceleration", "170 Hz resonant frequency, 1.8 Gpk vibration amplitude"],
            ["Physical Interconnect", "Serial Peripheral Interface (SPI) / I2C", "Bus Speed & Transfer Mode", "SPI @ 4 MHz with DMA; I2C @ 400 kHz Fast Mode Plus"]
        ]
    },
    "table_4_2": {
        "title": "Table 4.2: InstaHealth System Comprehensive Data Dictionary and Flow Specifications",
        "headers": ["Entity / Data Flow Name", "Data Flow Type", "Source / Destination", "Data Type & Format", "Description and Engineering Purpose"],
        "rows": [
            ["Raw_PPG_Stream", "Continuous Sensor Stream", "PPG Sensor -> Process 1.0", "Float32 Array [256], Volts", "Raw analog voltage reflections capturing arterial blood volume oscillations at 25 Hz."],
            ["Raw_IMU_Stream", "Continuous Sensor Stream", "IMU Sensor -> Process 1.0", "Int16 Array [3], G-units", "Triaxial kinetic acceleration (Ax, Ay, Az) sampled at 50 Hz for motion artifact detection."],
            ["Filtered_Telemetry_Buffer (D1)", "Internal Data Store", "Process 1.0 -> Process 4.0", "Float32 Ring Buffer [256]", "Motion-compensated, Butterworth-filtered optical pulse-train and kinetic cadence."],
            ["SQI_Validity_Flag", "Control Signal", "Process 1.0 -> Process 4.0", "Boolean (TRUE/FALSE)", "Indicates whether the current 5-second telemetry window satisfies signal quality thresholds (SQI ≥ 0.40)."],
            ["Profile_Context_Command", "User Input Event", "User -> Process 2.0", "String (Emoji Identifier)", "Selects active persona: Runner (🏃‍♂️), Meditator (🧘), Cyclist (🚴), or Swimmer (🏊)."],
            ["Sandboxed_Profile_Store (D2)", "Non-Volatile Data Store", "Process 2.0 <-> Process 4.0/5.0", "Encrypted Struct [4 Profiles]", "Isolated partitions encapsulating baselines, calibration counters, and configuration parameters."],
            ["Clinical_Norms_ROM (D4)", "Read-Only Data Store", "ROM -> Process 3.0", "Static Matrix [5×2×4]", "Normative epidemiological lookup table stratified across 5 age brackets and biological sex."],
            ["Demographic_Prior_Vector", "Processed Data Flow", "Process 3.0 -> Process 4.0", "Struct {HRmax, Cal, Steps, Sleep}", "Baseline prior calculated via Tanaka (male) or Gulati (female) maximum heart rate models."],
            ["Feature_Vector_x", "Processed Data Flow", "Process 4.1 -> Process 4.2", "Float32 Vector [5]", "Normalized inputs: [HR_norm, HRV_norm, Steps_norm, SleepDebt_norm, DayIndex]."],
            ["Quantized_Model_Weights (D3)", "Non-Volatile Data Store", "Process 4.4 <-> Process 4.2", "Float32/INT8 {W1, b1, W2, b2}", "Trained neural weights for the 2-layer MLP (W1 ∈ R^(8×5), W2 ∈ R^(3×8))."],
            ["Daily_Prescription_Vector", "Output Data Flow", "Process 5.0 -> Process 6.0", "Struct {SleepTarget, StepsTarget, HRR, Zones}", "Dynamic daily prescriptions synthesizing Belenky sleep debt and Karvonen HRR limits."],
            ["Display_Render_Buffer", "Graphics Output Flow", "Process 6.0 -> Display Panel", "24-bit RGB Framebuffer [454×454]", "Anti-aliased circular gauge arcs and text telemetry rendered at 60 frames per second."]
        ]
    },
    "table_4_3": {
        "title": "Table 4.3: Clinically Stratified Demographic Population Baseline Lookup Table",
        "headers": ["Age Cohort", "Biological Sex", "Normative Daily Calories (kcal)", "Normative Step Volume", "Normative Sleep Need (hrs)", "Calculated Peak HRmax (bpm)"],
        "rows": [
            ["18–29 Years", "Male", "2,400 kcal", "8,000 steps", "7.8 hours", "194 bpm (Tanaka: 208 - 0.7×20)"],
            ["18–29 Years", "Female", "1,900 kcal", "8,000 steps", "8.0 hours", "188 bpm (Gulati: 206 - 0.88×20)"],
            ["30–39 Years", "Male", "2,200 kcal", "7,500 steps", "7.5 hours", "184 bpm (Tanaka: 208 - 0.7×35)"],
            ["30–39 Years", "Female", "1,800 kcal", "7,500 steps", "7.7 hours", "175 bpm (Gulati: 206 - 0.88×35)"],
            ["40–49 Years", "Male", "2,100 kcal", "7,000 steps", "7.3 hours", "177 bpm (Tanaka: 208 - 0.7×45)"],
            ["40–49 Years", "Female", "1,700 kcal", "7,000 steps", "7.5 hours", "166 bpm (Gulati: 206 - 0.88×45)"],
            ["50–59 Years", "Male", "2,000 kcal", "6,500 steps", "7.0 hours", "170 bpm (Tanaka: 208 - 0.7×55)"],
            ["50–59 Years", "Female", "1,600 kcal", "6,500 steps", "7.2 hours", "158 bpm (Gulati: 206 - 0.88×55)"],
            ["60+ Years", "Male", "1,850 kcal", "6,000 steps", "6.8 hours", "163 bpm (Tanaka: 208 - 0.7×65)"],
            ["60+ Years", "Female", "1,500 kcal", "6,000 steps", "7.0 hours", "149 bpm (Gulati: 206 - 0.88×65)"]
        ]
    },
    "table_4_4": {
        "title": "Table 4.4: Karvonen Heart Rate Reserve (HRR) Training Intensity Zones and Metabolic Demands",
        "headers": ["Training Zone", "Intensity Range (% HRR)", "Example HR Range (HRrest=58, HRmax=194)", "Primary Physiological Stimulus", "Autonomic Nervous System Recovery Demand"],
        "rows": [
            ["Zone 1: Active Recovery", "50% – 60% HRR", "126 bpm – 139 bpm", "Promotes microvascular blood flow, lactic acid clearance, active tissue restoration", "Minimal autonomic fatigue (<12 hours recovery requirement)"],
            ["Zone 2: Aerobic Base & Fat Oxidation", "60% – 70% HRR", "140 bpm – 153 bpm", "Maximizes mitochondrial biogenesis, lipid substrate utilization, capillary density", "Low to moderate autonomic strain (12–24 hours recovery requirement)"],
            ["Zone 3: Tempo & Aerobic Capacity", "70% – 80% HRR", "154 bpm – 166 bpm", "Enhances cardiac stroke volume, pulmonary ventilation efficiency, glycogen storage", "Moderate sympathetic activation (24–36 hours recovery requirement)"],
            ["Zone 4: Anaerobic / Lactate Threshold", "80% – 90% HRR", "167 bpm – 180 bpm", "Raises lactate clearance threshold, high-intensity endurance sustained buffering", "High sympathetic stress, parasympathetic suppression (36–48 hours recovery)"],
            ["Zone 5: Neuromuscular / VO2 Max", "90% – 100% HRR", "181 bpm – 194 bpm", "Peak chronotropic response, maximal oxygen consumption rate (VO2 Max)", "Extreme systemic fatigue; requires strict haptic exertion limits and 48–72h recovery"]
        ]
    },
    "table_5_1": {
        "title": "Table 5.1: Embedded Hardware Platform Comparison and Compute Resource Allocation",
        "headers": ["Platform Name", "Processor Architecture", "Clock Speed", "RAM Allocation", "Flash Storage", "Target Deployment Target"],
        "rows": [
            ["Nordic Semiconductor nRF52840", "32-bit ARM Cortex-M4F with FPU", "64 MHz", "256 KB SRAM", "1,024 KB Flash", "Dedicated bare-metal wearable biometric tracker"],
            ["STMicroelectronics STM32WB55", "Dual-core ARM Cortex-M4 / Cortex-M0+", "64 MHz / 32 MHz", "256 KB SRAM", "1,024 KB Flash", "Wireless medical IoT wrist-worn clinical device"],
            ["Apple Watch Series 9 / Ultra 2", "Apple Silicon S9 SiP (Dual-core 64-bit)", "1.8 GHz dynamic", "1,024 MB LPDDR4X", "64 GB eMMC Flash", "Commercial high-tier smartwatch consumer application"],
            ["Air-Gapped WebAssembly Sandbox", "Wasm / Modern Browser Core (WebKit/Blink)", "Virtual Clock", "16 MB Virtual Heap", "IndexedDB / LocalStorage", "Zero-cloud offline progressive web application (PWA)"]
        ]
    },
    "table_5_2": {
        "title": "Table 5.2: Software Toolchains, Libraries, Compilers, and Runtime Dependencies",
        "headers": ["Software Layer", "Tool / Library Name", "Version", "Functional Role and Engineering Purpose"],
        "rows": [
            ["C/C++ Compiler", "GNU Arm Embedded Toolchain (arm-none-eabi-gcc)", "12.3.rel1", "Cross-compilation of bare-metal C/C++ firmware with -O3 and link-time optimization (LTO)."],
            ["DSP Processing", "ARM CMSIS-DSP Library", "v1.14.4", "Vector mathematics, 3rd-order Butterworth IIR filtering, and fast FFT implementations."],
            ["Neural Kernels", "ARM CMSIS-NN Library", "v4.1.0", "Optimized INT8 quantized neural network inference kernels utilizing Cortex-M DSP instructions."],
            ["TinyML Runtime", "TensorFlow Lite for Microcontrollers (TFLM)", "v2.12.0", "Static memory arena allocator and interpreter for embedded neural graph execution."],
            ["Web Runtime", "Modern ECMAScript (Vanilla ES6+)", "ES2022 Standard", "Air-gapped application logic, 2-layer MLP engine, and Micro-SGD on-device backpropagation."],
            ["Offline Cache", "Service Worker API (sw.js) & CacheStorage", "W3C PWA Standard", "100% offline asset caching, zero network socket access, persistent air-gapped lifecycle."],
            ["Graphics Engine", "HTML5 Canvas 2D Rendering Context", "HTML5 Standard", "High-DPI polar coordinate circular gauge drawing, 60 fps anti-aliased progress arcs."],
            ["Hardware Profiler", "Nordic Power Profiler Kit II Software", "v3.5.2", "High-resolution sub-microamp current and power consumption logging at 100 kHz."]
        ]
    },
    "table_5_3": {
        "title": "Table 5.3: InstaHealth Multi-Profile Avatar Sandboxing and Namespace Partitioning",
        "headers": ["Profile Avatar", "Persona Modality", "Primary Activity Focus", "Baseline Prior Allocation", "Isolated State Storage Key", "Partition Size"],
        "rows": [
            ["🏃‍♂️ Runner", "High-Intensity Endurance", "Aerobic capacity, tempo running, cadence", "Cal: 2,600 kcal; Steps: 10,000; Sleep: 8.0h", "instahealth_profile_runner", "1,024 bytes"],
            ["🧘 Meditator", "Mindfulness & Restoration", "Autonomic tone, resting HRV, deep sleep", "Cal: 1,900 kcal; Steps: 6,000; Sleep: 7.5h", "instahealth_profile_meditator", "1,024 bytes"],
            ["🚴 Cyclist", "Cardiovascular Conditioning", "Power output, sustained Zone 3 aerobic endurance", "Cal: 2,500 kcal; Steps: 7,000; Sleep: 7.8h", "instahealth_profile_cyclist", "1,024 bytes"],
            ["🏊 Swimmer", "Full-Body Metabolic Training", "Low-impact caloric expenditure, pulmonary volume", "Cal: 2,400 kcal; Steps: 6,500; Sleep: 8.2h", "instahealth_profile_swimmer", "1,024 bytes"]
        ]
    },
    "table_6_1": {
        "title": "Table 6.1: Comprehensive System Test Cases (TC01 to TC12) and Experimental Validation Results",
        "headers": ["Test ID", "Test Case Description", "Testing Type", "Input Condition & Test Stimulus", "Expected Engineering Behavior", "Observed Test Result & Status"],
        "rows": [
            ["TC01", "Demographic Prior Initialization & HRmax Binding", "Unit Testing", "Age = 20, Sex = Male, Profile = Runner", "Cohort '18-29' selected; HRmax = 194 bpm (Tanaka: 208 - 0.7×20); Base Cal = 2,400 kcal.", "Passed (Exact match to Tanaka prior; zero deviation)."],
            ["TC02", "Day 1 Calibration UI Split Rendering", "Integration", "DayIndex = 1, User Telemetry: HR=58, Steps=3,420", "Screen displays 'Calibration Active - Day 1 of 2'; split arcs render User vs Prior; no alarms.", "Passed (Split arcs rendered at 60 fps; zero false alarms triggered)."],
            ["TC03", "Day 2 Telemetry Ingestion & Moving Average Update", "System Testing", "DayIndex = 2, Continuous 24h wear data stream", "Moving average baseline updated; progress indicator displays 50%; observation maintained.", "Passed (Baseline smoothly transitioned; state machine locked in State 2)."],
            ["TC04", "Day 3 Autonomous Calibration Lock & Carousel Unlock", "System Testing", "DayIndex = 3 (Crossing 48.0 hours wear threshold)", "State advances to CALIBRATED; baseline committed to storage; prescription carousel unlocked.", "Passed (Automatic transition in 12 ms; prescription carousel active)."],
            ["TC05", "Micro-SGD Neural Weight Convergence", "Unit Testing", "Regular diurnal recovery streams over 10 epochs", "MSE loss decreases monotonically; learning rate η = 0.01; parameters stabilize.", "Passed (MSE loss decreased from 0.42 to 0.08; weights converged)."],
            ["TC06", "Micro-SGD Gradient Bounding on Outlier Input", "Unit Testing", "Extreme input anomaly: HR = 240 bpm (synthetic artifact)", "Gradient clipped to hard ceiling (|ΔW| ≤ 0.05); model weights protected against corruption.", "Passed (Maximum observed |ΔW| was exactly 0.050; zero weight explosion)."],
            ["TC07", "Corrupted PPG Wave Motion Artifact Rejection", "Integration / System", "Simulated violent shaker vibration (Accel Var > 1.8g)", "SQI drops below 0.40; IsValid flag set to FALSE; window rejected from baseline update.", "Passed (Corrupted window discarded safely; baseline preserved with fallback)."],
            ["TC08", "Complete Optical Sensor Dropout / Disconnection", "System Testing", "Physical sensor disconnected (zero photon voltage)", "Sensor error detected; firmware maintains latest valid state; graceful demographic fallback.", "Passed (No system crash; error banner displayed; graceful state retention)."],
            ["TC09", "Multi-Profile Context Switching & Isolation", "Integration", "Rapid switching: Runner (🏃‍♂️) -> Meditator (🧘)", "State pointers swapped in <50 ms; Runner sprint strain does not leak to Meditator baseline.", "Passed (Context switch executed in 42 ms; zero inter-profile data leakage)."],
            ["TC10", "Belenky Multi-Night Sleep Debt Compensation", "System Testing", "Night 1: 5.5h sleep (2.3h deficit); Night 2: 6.0h sleep", "Sleep debt accumulates via autoregression; Day 3 sleep target expands dynamically (+1.0h).", "Passed (Prescribed sleep target expanded from 7.2h to 8.2h as formulated)."],
            ["TC11", "Karvonen Cardio Strain Limit Haptic Alert", "System Testing", "Heart rate sustained in Zone 5 (>181 bpm for >5 mins)", "Cardio strain gauge flashes crimson; haptic LRA transducer fires warning pulses.", "Passed (Haptic warning triggered within 1.2 seconds of Zone 5 breach)."],
            ["TC12", "Local Storage Non-Volatile Persistence Across Reboot", "System / UAT", "Simulated battery exhaustion; device hard power cycle", "On restart, firmware reloads profile state, calibration day counter, and model weights.", "Passed (100% state restoration in 85 ms; zero data loss observed)."]
        ]
    },
    "table_6_2": {
        "title": "Table 6.2: Signal Quality Index (SQI) Artifact Rejection Performance Across Activity Modalities",
        "headers": ["Physical Activity Modality", "Kinetic Accelerometer Variance", "Mean Signal Quality Index (SQI)", "Telemetry Windows Evaluated", "Window Rejection Rate (%)"],
        "rows": [
            ["Resting Supine / Nocturnal Sleep", "0.04g – 0.12g", "0.94 ± 0.03", "14,400 windows", "0.8% (Quiescent baseline tracking)"],
            ["Desk Computer Work & Keyboard Typing", "0.15g – 0.45g", "0.86 ± 0.06", "14,400 windows", "3.2% (Minor wrist motion artifacts)"],
            ["Outdoor Ambulatory Running (10 km/h)", "0.85g – 1.65g", "0.62 ± 0.12", "7,200 windows", "14.5% (Motion-compensated filtering active)"],
            ["Corrupted PPG Motion Wave (Violent Shaking)", "1.95g – 3.20g", "0.24 ± 0.08", "3,600 windows", "98.4% (Automatic artifact suppression; model protected)"]
        ]
    },
    "table_6_3": {
        "title": "Table 6.3: Empirical Model Ablation Performance: TinyML MLP vs Linear Regression vs Static Rules",
        "headers": ["Physiological Target Metric", "Static Normative Rules", "Multi-Variable Linear Regression", "InstaHealth TinyML MLP", "Error Reduction vs Static Baseline (%)"],
        "rows": [
            ["Nocturnal Sleep Need (hours)", "MAE = 1.15 hours", "MAE = 0.72 hours", "MAE = 0.34 hours", "70.4% Reduction in Sleep Prediction Error"],
            ["Daily Step Volume Target (steps)", "MAE = 1,420 steps", "MAE = 850 steps", "MAE = 412 steps", "71.0% Reduction in Step Target Error"],
            ["Maximum Safe Heart Rate (bpm)", "MAE = 8.4 bpm (Fox & Haskell)", "MAE = 5.6 bpm (Linear Reg)", "MAE = 2.8 bpm (Tanaka/Gulati + MLP)", "66.7% Reduction in HRmax Prediction Error"],
            ["Composite Weighted Physiological MAE", "Baseline Heuristic (1.00x)", "0.58x Relative Error", "0.38x Relative Error", "62.4% Overall Error Reduction Across System"]
        ]
    },
    "table_6_4": {
        "title": "Table 6.4: On-Device Execution Latency and Memory Footprint Profile on ARM Cortex-M4F",
        "headers": ["Firmware Functional Kernel", "Execution Latency (ms)", "SRAM Working Footprint (KB)", "Flash Executable Size (KB)", "Percentage of 60 fps Frame Budget"],
        "rows": [
            ["Raw Sensor Ingestion & Butterworth Filter", "0.42 ms per 25-sample block", "2.1 KB", "4.8 KB", "2.5% of frame window"],
            ["Signal Quality Index (SQI) Evaluator", "0.65 ms per 5s window", "1.8 KB", "3.6 KB", "3.9% of frame window"],
            ["TinyML Forward Inference Pass", "1.18 ms per inference", "4.8 KB", "14.2 KB", "7.1% of frame window"],
            ["Micro-SGD Analytical Backward Update", "2.45 ms per diurnal batch", "6.2 KB", "11.4 KB", "14.7% (Executed during sleep)"],
            ["High-DPI Canvas Circular Gauge Rendering", "4.82 ms per frame", "5.1 KB", "14.6 KB", "28.9% (Fluid 60 fps sustain: 207 fps theoretical max)"],
            ["Total InstaHealth Firmware Stack", "N/A (Concurrent Pipeline)", "18.2 KB Dynamic SRAM", "48.6 KB Non-Volatile Flash", "Full Real-Time Determinism Maintained"]
        ]
    },
    "table_6_5": {
        "title": "Table 6.5: Subsystem Current Consumption Profile and 65 mAh Battery Life Budget",
        "headers": ["Hardware Subsystem / Component", "Operating Voltage (V)", "Active Current Draw (mA)", "Average Power (mW)", "Percentage of System Energy Budget"],
        "rows": [
            ["Optical Biosensor Cluster (PPG Green/IR LEDs + AFE)", "3.70 V DC", "0.52 mA (Duty-cycled)", "1.92 mW", "42.3% of total battery budget"],
            ["Triaxial Accelerometer (IMU @ 50 Hz)", "3.70 V DC", "0.08 mA (Continuous)", "0.30 mW", "6.5% of total battery budget"],
            ["ARM Cortex-M4F CPU (Signal Processing & TinyML)", "3.70 V DC", "0.28 mA (Bursted execution)", "1.04 mW", "22.8% of total battery budget"],
            ["AMOLED Circular Display (10% Daily Glance Duty Cycle)", "3.70 V DC", "0.35 mA (Time-averaged)", "1.30 mW", "28.4% of total battery budget"],
            ["Total System Aggregate Operational Profile", "3.70 V DC", "1.23 mA Continuous Average", "4.55 mW Total Power", "52.8 Hours Runtime on 65 mAh Cell (Target: 48h)"]
        ]
    }
}
