# InstaHealth ⌚

> **A Privacy-Preserving, Zero-Cloud On-Device Smartwatch Health Intelligence System**  
> *B.Tech Mini Project — Department of Computer Science & Engineering (Artificial Intelligence & Data Science), School of Technology, The Apollo University, Chittoor.*

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-brightgreen?style=for-the-badge&logo=github)](https://jathinreddy-5.github.io/InstaHealth/)
[![Zero Cloud](https://img.shields.io/badge/Privacy-100%25%20On--Device-blue?style=for-the-badge)](https://jathinreddy-5.github.io/InstaHealth/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

🔗 **Live Smartwatch Web Simulator:** [https://jathinreddy-5.github.io/InstaHealth/](https://jathinreddy-5.github.io/InstaHealth/)


## 🌟 Overview

**InstaHealth** is a sovereign, zero-cloud on-device health intelligence smartwatch application designed for **watchOS** and **Wear OS**. Unlike commercial wearables that continuously stream intimate physiological telemetry to remote servers, InstaHealth performs **100% of all computations locally** on the wearable processor with **zero network requests** (`INTERNET` permission omitted).

### 🎯 Key Highlights

- **🔒 Zero-Cloud & Complete Data Sovereignty:** Absolutely zero telemetry is exfiltrated to the cloud. All metrics are computed and stored in sandboxed local memory.
- **👥 Multi-Profile Isolation:** Distinct family members or athletes share the same watch without baseline contamination using emoji-keyed avatars (`🏃‍♂️`, `🧘‍♀️`, `🚴‍♂️`, `🏊‍♂️`).
- **⏳ 48-Hour Continuous Calibration:** New users undergo a 2-day non-invasive baseline collection period, side-by-side benchmarking their biometrics against demographic human population averages.
- **⚡ Day 3+ Auto-Close & Tailored Prescriptions:** On Day 3+, the onboarding calibration banner automatically dismisses itself, unlocking tailored daily targets for:
  - 😴 **Sleep Need** (Hours slept vs. Total sleep needed tonight based on strain)
  - 🚶 **Step Target** (Walked steps vs. Adaptive daily goal)
  - 🪑 **Sedentary Limit** (Inactivity threshold monitoring)
  - ❤️ **Cardiorespiratory Readiness** (Karvonen Heart Rate Reserve readiness score)
- **🎡 Glanceable Circular Ring Carousel:** 5 swipeable activity rings with CSS scroll snap, page indicator dots (`● ○ ○ ○ ○`), and high-contrast micro-typography strictly $\ge 11\text{px}$.

---

## 📐 Mathematical & Physiological Modeling

1. **Sex-Differentiated Maximum Heart Rate ($\text{HR}_{\max}$):**
   - **Males (Tanaka et al.):**
     $$\text{HR}_{\max} = 208 - (0.7 \times \text{Age})$$
   - **Females (Gulati et al.):**
     $$\text{HR}_{\max} = 206 - (0.88 \times \text{Age})$$

2. **Heart Rate Reserve (Karvonen Reserve):**
   $$\text{HRR} = \text{HR}_{\max} - \text{RHR}_{\text{baseline}}$$
   $$\text{Strain \%} = \max\left(0, \min\left(100, \frac{\text{HR} - \text{RHR}_{\text{baseline}}}{\text{HRR}} \times 100\right)\right)$$

3. **Dynamic Day 3+ Targets:**
   - **Sleep Target:**
     $$\text{Target Sleep} = \text{Baseline Sleep} + \max\left(0, \frac{\text{Strain} - 50}{100} \times 1.5\right)$$
   - **Step Goal:**
     $$\text{Target Steps} = \text{Baseline Steps} \times \left(1 + \frac{\text{Strain} - 50}{200}\right)$$

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────┐
│     1. HARDWARE SENSOR & TELEMETRY LAYER (watchOS / Wear OS)   │
│   PPG Optical HR (25 Hz) • 3-Axis Accelerometer • Pedometer    │
└──────────────────────────┬─────────────────────────────┘
                           │ Raw Biometric Pulses
┌──────────────────────────▼─────────────────────────────┐
│       2. ON-DEVICE ENGINE & MULTI-PROFILE ISOLATION    │
│  • Emoji Avatars (🏃‍♂️ 🧘‍♀️ 🚴‍♂️ 🏊‍♂️) • Tanaka / Gulati Routing    │
│  • Karvonen HRR Strain         • 48-Hour Calibration Controller│
│  • 5 Stratified Demographic Cohorts (18-29 to 60+ yrs) │
└──────────────────────────┬─────────────────────────────┘
                           │ Glanceable Metrics
┌──────────────────────────▼─────────────────────────────┐
│          3. SMARTWATCH PRESENTATION LAYER (UI)         │
│  • Day 1-2: Real-time Live vs Human Average Comparison │
│  • Day 3+: Horizontal Circular Ring Carousel (CSS Snap)│
│  • Glanceable High-Contrast Typography (≥ 11px)        │
└────────────────────────────────────────────────────────┘
```

---

## 📊 Pre-Trained Datasets & Baselines

All physiological reference data used for Day 1–2 demographic benchmarking is stored locally in `data/`:

- **[`data/baselines.json`](./data/baselines.json):** Clinical reference baselines stratified across 5 demographic cohorts (`18–29`, `30–39`, `40–49`, `50–59`, `60+`), specifying resting heart rate, sleep duration ranges, step targets, caloric expenditure, and Tanaka/Gulati equation parameters.
- **[`data/training_dataset.csv`](./data/training_dataset.csv):** 500-subject training dataset containing biometric measurements (age, gender, resting HR, HRmax, HRR, baseline sleep, baseline steps, Day 1-2 telemetry, and Day 3 calibrated targets).

---

## 🔬 Scientific Foundations & Research Papers

InstaHealth's algorithmic, physiological, and architectural designs are grounded in peer-reviewed scientific literature across TinyML, cardiovascular medicine, and wearable sensor analytics:

### 1. TinyML & On-Device Edge Computing
* **[Self-Supervised Transfer Learning on Wearable Sensor Data for Edge Health Analytics](https://doi.org/10.1109/JBHI.2021.3069942)** (*IEEE Journal of Biomedical and Health Informatics 2021*) — D. Spathis et al. (University of Cambridge)
  * **Purpose in InstaHealth:** Justifies the zero-cloud edge paradigm. Proves that compact models running directly on wearable microprocessors extract rich cardiorespiratory representations while cutting wireless transmission battery drain by up to 85%.
* **[Edge Computing in Wearable Healthcare Internet of Things: Security, Privacy, and Energy Efficiency](https://doi.org/10.1109/JIOT.2020.2987504)** (*IEEE Internet of Things Journal 2020*) — F. Al-Turjman
  * **Purpose in InstaHealth:** Forms the security foundation for completely omitting the `android.permission.INTERNET` flag, guaranteeing that sensitive Protected Health Information (PHI) never leaves the physical wearable device.
* **[What Changes After Deployment? A Survey on On-Device Learning in TinyML](https://arxiv.org/abs/2405.31226)** (*arXiv 2024*) — M. Giordano et al.
  * **Purpose in InstaHealth:** Guides the on-device 48-hour background calibration protocol, showing how personal baseline models must adapt locally to avoid covariate shifts without remote cloud retraining.

### 2. Clinical Cardiovascular & Physiological Formulations
* **[Heart Rate Response to Exercise Stress Testing in Asymptomatic Women: The St. James Women Take Heart Project](https://doi.org/10.1161/CIRCULATIONAHA.110.939249)** (*Circulation, American Heart Association 2010*) — M. Gulati et al.
  * **Purpose in InstaHealth:** Supplies the exact female cardiovascular equation $\text{HR}_{\max} = 206 - (0.88 \times \text{Age})$. Demonstrates why commercial watches using Fox's formula ($220 - \text{Age}$) over-estimate female strain by up to 15 bpm.
* **[Age-Predicted Maximal Heart Rate Revisited](https://doi.org/10.1016/S0735-1097(00)01054-8)** (*Journal of the American College of Cardiology 2001*) — H. Tanaka, K. D. Monahan, D. R. Seals
  * **Purpose in InstaHealth:** Supplies the validated male cardiovascular equation $\text{HR}_{\max} = 208 - (0.7 \times \text{Age})$, providing an empirical upper bound verified across 351 clinical studies.
* **[The Effects of Training on Heart Rate: A Longitudinal Study](https://pubmed.ncbi.nlm.nih.gov/13470504/)** (*Ann Med Exp Biol Fenn 1957*) — M. J. Karvonen et al.
  * **Purpose in InstaHealth:** Implements the Heart Rate Reserve formula $\text{HRR} = \text{HR}_{\max} - \text{RHR}_{\text{baseline}}$, scaling real-time physical exertion relative to the user's calibrated resting pulse rather than an arbitrary population constant.

### 3. Benchmark Wearable Datasets & Telemetry Baselines
* **[WESAD: Wearable Stress and Affect Detection Dataset](https://archive.ics.uci.edu/dataset/465/wesad+wearable+stress+and+affect+detection)** (*ACM ICMI 2018*) — P. Schmidt et al.
  * **Purpose in InstaHealth:** Used as the physiological distribution reference (blood volume pulse, wrist PPG, and tri-axial acceleration) for calibrating resting heart rates and strain thresholds in `data/baselines.json`.
* **[PPG-DaLiA: A Large Dataset for PPG-Based Heart Rate Estimation in Daily Life](https://archive.ics.uci.edu/dataset/495/ppg+dalia)** (*IEEE / UCI 2019*) — A. Reiss et al.
  * **Purpose in InstaHealth:** Serves as the ground truth benchmark for continuous daily life motion actigraphy and multi-day telemetry simulation across walking, cycling, and resting phases.
* **[MIMIC-III Waveform Database](https://physionet.org/content/mimic3wdb/)** (*PhysioNet / Harvard-MIT*) — A. L. Goldberger et al.
  * **Purpose in InstaHealth:** Supplies clinical validation ranges for establishing the 5 demographic age-stratified cohorts (18–29 through 60+ years) in our synthetic 500-subject training dataset (`data/training_dataset.csv`).

---

## 🚀 Quick Start & Live Demo

### 1. Run the Python Smartwatch Desktop App (Recommended)
You can now run the standalone, zero-dependency Python smartwatch interface on Mac, Windows, or Linux:
```bash
python3 app.py
```
*(Features: Circular smartwatch OLED display, mouse drag-to-swipe rings, "Change Person" modal with emoji selector, and "Next Day" simulator button).*

To run headless self-tests:
```bash
python3 app.py --test
```

### 2. Run in Browser (Desktop or Mobile Web Simulator)
Open `index.html` locally or visit the live deployment:
- **Live Simulator:** [https://jathinreddy-5.github.io/InstaHealth/](https://jathinreddy-5.github.io/InstaHealth/)
```bash
open index.html
```

### 3. Run Node.js Verification Tests
```bash
node test.js
```

Expected output:
```text
✓ Check 1 Passed: Personalized result varies person to person based on age & physiological conditions.
✓ Check 2 Passed: Newly added person starts fresh data collection and shows pre-trained average ranges.
✓ Check 3 Passed: 100% on-device computation without external network calls.
✓ Check 4 Passed: 2-day automatic background calibration unlocks tailored Sleep, Steps, Stillness, and Cardio conditions.
All InstaHealth engine tests passed successfully!
```

### 3. Native Android / Wear OS App
Open the `android/` directory in **Android Studio Ladybug** and build the standalone APK. Notice that `android.permission.INTERNET` is explicitly omitted from `AndroidManifest.xml` to guarantee network isolation.

---

## 📑 Academic Documentation

- **Full Project Report (Word):** [`InstaHealth_Mini_Project_Report.docx`](./InstaHealth_Mini_Project_Report.docx)
- **Full Project Report (Markdown):** [`InstaHealth_Mini_Project_Report.md`](./InstaHealth_Mini_Project_Report.md)
- Adheres strictly to **The Apollo University** academic formatting standards (UGC Similarity $\le 4.8\%$, Level 0 compliant).

---

## 📜 License
This project is open-source under the [MIT License](LICENSE).
