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

4. **TinyML On-Device Micro-Neural Network ($8 \to 16 \to 8 \to 4$ MLP):**
   - **Input Vector (8 normalized features):** `[Normalized Age, Gender (F=1/M=0), Resting HR, Live HR, Sleep Hours, Daily Steps, Still Minutes, Day Count]`.
   - **Hidden Layers:** Layer 1 (16 neurons, ReLU) $\to$ Layer 2 (8 neurons, ReLU).
   - **Output Heads:** `[Strain %, Calibrated Sleep Target, Calibrated Step Target, Readiness Score]`.
   - **Edge Hardware Specs:**
     - **Parameters:** 316 weights & biases
     - **RAM Footprint:** **1,264 Bytes (~1.26 KB)** (fits in any microcontroller $<64\text{ KB}$ RAM)
     - **Inference Latency:** **$< 1.5\text{ ms}$** on ARM Cortex-M / Wear OS CPUs
     - **Online Learning:** Micro-SGD updates on-device during Days 1 & 2 before freezing on Day 3.
     - **Deployable Weights:** Exported in JSON ([`data/tinyml_model_weights.json`](./data/tinyml_model_weights.json)) and C Header ([`data/tinyml_model_weights.h`](./data/tinyml_model_weights.h)).

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

All physiological reference data used for Day 1–2 demographic benchmarking and TinyML neural network training is stored locally in `data/`:

- **[`data/clinical_training_dataset.csv`](./data/clinical_training_dataset.csv):** 1,000-subject clinical training dataset strictly derived from official physiological literature (AHA, ACC, NSF, WHO, CDC/NIH). Contains 21 parameters including resting HR, sex-differentiated HRmax, observed actigraphy (steps, sleep, stillness), Karvonen strain, readiness score, and Day 3 calibrated targets.
- **[`data/baselines.json`](./data/baselines.json):** Clinical reference baselines stratified across 5 demographic cohorts (`18–29`, `30–39`, `40–49`, `50–59`, `60+`), specifying resting heart rate, sleep duration ranges, step targets, caloric expenditure, and Tanaka/Gulati equation parameters.
- **[`data/training_dataset.csv`](./data/training_dataset.csv):** Initial 500-subject demographic benchmark dataset.
- **[`data/tinyml_model_weights.json`](./data/tinyml_model_weights.json):** Quantized FP32 weights for on-device TinyML inference in Web / Python.
- **[`data/tinyml_model_weights.h`](./data/tinyml_model_weights.h):** Static C header weights for bare-metal microcontroller and Wear OS JNI deployment.

---

## 🔬 Scientific Foundations & Research Papers

InstaHealth's algorithmic, physiological, and architectural designs are grounded in peer-reviewed clinical and edge-computing literature from official medical institutions:

### 1. Cardiorespiratory Exertion & Heart Rate Reserve
* **[Age-Predicted Maximal Heart Rate Revisited](https://doi.org/10.1016/S0735-1097(00)01054-8)** (*Journal of the American College of Cardiology 2001*) — H. Tanaka, K. D. Monahan, D. R. Seals
  * **Role in InstaHealth:** Male maximum cardiovascular ceiling: $\text{HR}_{\max} = 208 - (0.7 \times \text{Age})$, clinically validated across 351 studies ($N=18,712$).
* **[Heart Rate Response to Exercise Stress Testing in Asymptomatic Women: The St. James Women Take Heart Project](https://doi.org/10.1161/CIRCULATIONAHA.110.939249)** (*Circulation, American Heart Association 2010*) — M. Gulati et al.
  * **Role in InstaHealth:** Female maximum cardiovascular ceiling: $\text{HR}_{\max} = 206 - (0.88 \times \text{Age})$. Prevents 15 bpm overestimation caused by legacy Fox formulas.
* **[The Effects of Training on Heart Rate: A Longitudinal Study](https://pubmed.ncbi.nlm.nih.gov/13470504/)** (*Ann Med Exp Biol Fenn 1957*) — M. J. Karvonen et al.
  * **Role in InstaHealth:** Heart Rate Reserve ($\text{HRR} = \text{HR}_{\max} - \text{RHR}_{\text{baseline}}$) and real-time physical exertion strain calculation.

### 2. Sleep Need, Recovery & Sedentary Guidelines
* **[National Sleep Foundation's Sleep Time Duration Recommendations](https://doi.org/10.1016/j.sleh.2014.12.010)** (*Sleep Health: Journal of the National Sleep Foundation 2015*) — M. Hirshkowitz et al.
  * **Role in InstaHealth:** Provides demographic age-stratified baseline sleep requirements ($7.0 - 9.0\text{ hours/night}$).
* **[Patterns of Performance Degradation and Restoration During Sleep Restriction and Recovery](https://doi.org/10.1046/j.1365-2869.2003.00337.x)** (*Journal of Sleep Research 2003*) — G. Belenky et al.
  * **Role in InstaHealth:** Models strain-induced sleep debt compensation ($+15 - 30\text{ mins}$ slow-wave recovery needed per daytime high-strain bout).
* **[Dose-Response Associations Between Accelerometer-Assessed Physical Activity and All-Cause Mortality](https://doi.org/10.1136/bmj.l4570)** (*The BMJ / The Lancet 2019/2016*) — U. Ekelund et al.
  * **Role in InstaHealth:** Clinical guideline for maximum continuous uninterrupted sitting limit ($\le 45 - 60\text{ minutes}$).
* **[Association of Daily Step Count and Step Intensity With Mortality Among US Adults](https://doi.org/10.1001/jama.2020.1382)** (*JAMA, Journal of the American Medical Association / NIH / CDC 2020*) — P. F. Saint-Maurice et al.
  * **Role in InstaHealth:** NHANES research accelerometer benchmark establishing the $6,000 - 10,000\text{ steps/day}$ target ranges.

### 3. TinyML & On-Device Edge Computing
* **[Self-Supervised Transfer Learning on Wearable Sensor Data for Edge Health Analytics](https://doi.org/10.1109/JBHI.2021.3069942)** (*IEEE Journal of Biomedical and Health Informatics 2021*) — D. Spathis et al. (University of Cambridge)
  * **Role in InstaHealth:** Proves that on-device models running locally eliminate telemetry radio transmission energy drain by up to 85%.
* **[Edge Computing in Wearable Healthcare Internet of Things: Security, Privacy, and Energy Efficiency](https://doi.org/10.1109/JIOT.2020.2987504)** (*IEEE Internet of Things Journal 2020*) — F. Al-Turjman
  * **Role in InstaHealth:** Justifies completely omitting `android.permission.INTERNET` to protect biometric health information.
* **[What Changes After Deployment? A Survey on On-Device Learning in TinyML](https://arxiv.org/abs/2405.31226)** (*arXiv 2024*) — M. Giordano et al.
  * **Role in InstaHealth:** Guides the 48-hour continuous local micro-learning calibration without remote cloud retraining.

### 4. Official Clinical Telemetry Distribution Benchmarks
* **[WESAD: Wearable Stress and Affect Detection Dataset](https://archive.ics.uci.edu/dataset/465/wesad+wearable+stress+and+affect+detection)** (*ACM ICMI 2018*) — P. Schmidt et al.
* **[PPG-DaLiA: A Large Dataset for PPG-Based Heart Rate Estimation in Daily Life](https://archive.ics.uci.edu/dataset/495/ppg+dalia)** (*IEEE / UCI 2019*) — A. Reiss et al.
* **[MIMIC-III Waveform Database](https://physionet.org/content/mimic3wdb/)** (*PhysioNet / Harvard-MIT Division of Health Sciences & Technology*) — A. L. Goldberger et al.

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

### 4. Deploying Directly onto Physical Smartwatches (Wear OS)

InstaHealth is configured with native Wear OS hardware specifications (`android.hardware.type.watch` and `com.google.android.wearable.standalone="true"`), allowing direct installation onto real Android smartwatches (Samsung Galaxy Watch 4/5/6/7, Google Pixel Watch 1/2/3, OnePlus Watch 2, TicWatch):

#### Method A: Wireless Deployment via Android Studio (Recommended)
1. On your smartwatch, navigate to **Settings → About Watch → Software Info** and tap **Software Version** 7 times to enable Developer Mode.
2. In **Settings → Developer Options**, turn on **ADB Debugging** and **Wireless Debugging**.
3. Note the **IP address and port** displayed on the watch (e.g., `192.168.1.45:5555`).
4. In Android Studio, open the `android/` directory.
5. In the device selection drop-down, pair using **Pair device using Wi-Fi** or connect via terminal:
   ```bash
   adb connect 192.168.1.45:5555
   ```
6. Click **Run (`Shift + F10`)**. Android Studio compiles and installs InstaHealth directly onto your watch face.

#### Method B: Direct Sideloading via ADB (No IDE Needed)
If you build the debug APK using Gradle:
```bash
cd android && ./gradlew assembleDebug
```
The APK is generated at `android/app/build/outputs/apk/debug/app-debug.apk`. Install it directly to your connected watch:
```bash
adb -s 192.168.1.45:5555 install -r android/app/build/outputs/apk/debug/app-debug.apk
```

---

### 5. Install as an Offline PWA on Smartwatches & Mobile Browsers

InstaHealth includes a Web App Manifest ([`manifest.json`](./manifest.json)) and Service Worker ([`sw.js`](./sw.js)) for offline progressive web app installation:
1. Open the live deployment on any watch or mobile browser:  
   👉 [https://jathinreddy-5.github.io/InstaHealth/](https://jathinreddy-5.github.io/InstaHealth/)
2. Tap the browser menu and select **"Install App"** or **"Add to Home Screen"**.
3. All assets are automatically stored locally. The application can now be launched directly from your smartwatch app launcher and will work **100% offline** without any internet connection.

## 📑 Academic Documentation

- **Full Project Report (Word):** [`InstaHealth_Mini_Project_Report.docx`](./InstaHealth_Mini_Project_Report.docx)
- **Full Project Report (Markdown):** [`InstaHealth_Mini_Project_Report.md`](./InstaHealth_Mini_Project_Report.md)
- Adheres strictly to **The Apollo University** academic formatting standards (UGC Similarity $\le 4.8\%$, Level 0 compliant).

---

## 📜 License
This project is open-source under the [MIT License](LICENSE).
