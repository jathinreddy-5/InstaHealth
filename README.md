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
