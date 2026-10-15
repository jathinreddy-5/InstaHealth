# InstaHealth Smartwatch: End-to-End Operational Workflow & Lifecycle Specification

## 1. System Philosophy & Zero-Cloud Edge Foundation
InstaHealth is an on-device, zero-cloud smartwatch health intelligence platform designed to eliminate privacy risks, cloud latency, and wireless telemetry battery drain. 

- **Protected Health Information (PHI) Isolation**: Operates with complete omission of network communication (`android.permission.INTERNET` is excluded).
- **Embedded Inference**: Runs an on-device 8 → 16 → 8 → 4 Multilayer Perceptron (MLP) containing 316 parameters (1.26 KB RAM footprint, <1.5 ms execution latency).
- **Hardware-Level Sandboxing**: Each wearable profile maintains its own isolated neural network weights and baseline states in local storage, preventing cross-user data contamination.

---

## 2. Step-by-Step Operational Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: MINUTE 0 — ZERO-CLOUD SETUP & DEMOGRAPHIC SEEDING                 │
│ • User selects profile (e.g., 🏃‍♂️ Runner, 22y Male) directly on-watch         │
│ • Memory sandbox allocated with fresh FP32 weight matrices                  │
│ • Initial baselines seeded from clinical demographic reference tables       │
│ • Sex-differentiated HRmax calculated (Tanaka: 192.6 bpm / Gulati formula)  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: HOURS 0 TO 48 — BACKGROUND CALIBRATION & MICRO-SGD LEARNING        │
│ • Continuous optical PPG sampling & 3-axis accelerometer actigraphy         │
│ • Real-time Karvonen HRR Strain calculation displayed on watch rings        │
│ • Lower screen renders Live Demographic Benchmarking comparison table       │
│ • On-device gradient descent (Micro-SGD) updates output heads (W3, b3)      │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: HOUR 48+ (DAY 3) — AUTO-DISMISSAL & TAILORED PRESCRIPTIONS        │
│ • Demographic comparison card automatically closes and disappears           │
│ • Tailored daily prescriptions unlocked (Sleep, Steps, Stillness, Readiness)│
│ • Continuous acute strain anomaly detection active                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Phase 1: Zero-Cloud Initialization & Profile Seeding (Minute 0)

1. **User Selection on Watch Screen**:
   - The user selects or adds their profile directly on the smartwatch face (e.g., `🏃‍♂️ Runner`, `22 years old`, `Male`).
   - The setup occurs entirely locally without login credentials, account creation, or paired smartphone reliance.

2. **Isolated Model Sandbox Allocation**:
   - The on-device engine clones weight matrices (`W1`, `b1`, `W2`, `b2`, `W3`, `b3`) into a private profile sandbox in local memory.
   - If multiple profiles share the device, their models remain isolated with zero cross-user covariate leakage.

3. **Demographic Seeding (`data/baselines.json`)**:
   - The model seeds its initial health expectations from clinical demographic tables stratified across five age cohorts: `18–29`, `30–39`, `40–49`, `50–59`, `60+`.
   - For an 18–29 year old male:
     - Baseline Resting Heart Rate: `60 bpm` (normal range: `55–66 bpm`)
     - Baseline Sleep Target: `7.8 hours` (normal range: `7.5–8.5 hrs`)
     - Baseline Daily Step Goal: `8,000 steps` (normal range: `7,000–10,000`)
     - Inactivity Stillness Limit: `60 minutes`
     - Caloric Burn Expectation: `2,400 kcal`

4. **Cardiovascular Ceiling Computation**:
   - The engine computes the age-predicted maximal heart rate ceiling using clinically validated formulas:
     - **Male** (Tanaka et al., *JACC 2001*):
       $$\text{HR}_{\max} = 208 - (0.7 \times \text{Age}) = 208 - (0.7 \times 22) = 192.6\text{ bpm}$$
     - **Female** (Gulati et al., *Circulation 2010*):
       $$\text{HR}_{\max} = 206 - (0.88 \times \text{Age})$$
   - Establishes the user's Heart Rate Reserve ($\text{HRR} = \text{HR}_{\max} - \text{RHR}_{\text{baseline}}$).

---

### Phase 2: The 48-Hour Continuous Calibration (Days 1 & 2)

During the first 48 hours of wear, the smartwatch acts as an adaptive baseline learner:

1. **Continuous Biometric Sampling**:
   - **Optical PPG Sensor (25 Hz)**: Samples pulse waveforms to record true nocturnal resting heart rate during Stage 3/4 NREM sleep and peak exercise pulses.
   - **3-Axis Accelerometer (50 Hz)**: Tracks step cadence, daily displacement, and sedentary continuous stillness.

2. **Real-Time Karvonen Heart Rate Reserve (HRR) Calculation**:
   - Real-time physiological exertion is calculated dynamically on every glance:
     $$\text{Cardio Strain \%} = \max\left(0.0, \min\left(100.0, \frac{\text{HR}_{\text{live}} - \text{RHR}_{\text{learned}}}{\text{HR}_{\max} - \text{RHR}_{\text{learned}}} \times 100\right)\right)$$
   - This scales exertion relative to personal cardiorespiratory fitness rather than an arbitrary population constant.

3. **On-Screen Demographic Benchmarking Interface**:
   - The lower half of the watch face displays the active **Calibration Card**:
     - Status Badge: `⏳ Calibrating: Day 1 of 2` (or `Day 2 of 2`)
     - Clinical Benchmark Comparison Table:
       - **Resting HR**: Clinical Avg (`55–66 bpm`) vs. You (`58 bpm`)
       - **Sleep Need**: Clinical Avg (`7.5–8.5 hrs`) vs. You (`7.2 hrs`)
       - **Step Target**: Clinical Avg (`7,000–10,000`) vs. You (`6,400`)
     - Subtitle note: `🔒 Day 3 closes this card automatically`

4. **On-Device Micro-Learning (Online Micro-SGD)**:
   - At the conclusion of Day 1 and Day 2, the smartwatch executes on-device backpropagation (`adapt_micro_sgd`):
     - Extracts the 8 normalized input features:
       $$x = [\text{Age}_{\text{norm}}, \text{Sex}_{\text{bin}}, \text{RHR}_{\text{norm}}, \text{HR}_{\text{norm}}, \text{Sleep}_{\text{norm}}, \text{Steps}_{\text{norm}}, \text{Still}_{\text{norm}}, \text{Day}_{\text{norm}}]$$
     - Calculates loss between the model's forward prediction and observed physical telemetry:
       $$\text{Error}_{\text{sleep}} = \frac{\text{Predicted Sleep Target} - \text{Observed Target}}{7.0}$$
       $$\text{Error}_{\text{steps}} = \frac{\text{Predicted Step Target} - \text{Observed Target}}{15,000.0}$$
     - Adapts output weights ($W_3$) and biases ($b_3$) using a learning rate of $\eta = 0.01$:
       $$b_{3}[j] \leftarrow b_{3}[j] - \eta \cdot \text{Error}[j]$$
       $$W_{3}[i][j] \leftarrow W_{3}[i][j] - \eta \cdot \text{Error}[j] \cdot h_{2}[i]$$

---

### Phase 3: Day 3+ Auto-Dismissal & Personalized Prescriptions

At hour 48 (start of Day 3), the watch transitions from demographic benchmarking to tailored health intelligence:

1. **Automatic Calibration Card Dismissal**:
   - The `Calibrating: Day 1/2` table **automatically closes and unmounts**.
   - An on-watch confirmation toast notification displays: `🎉 Day 3 Complete! Calibrated.`

2. **Tailored Daily Prescriptions Activation**:
   - The lower half of the watch display transforms into the **Calibrated Model Active** dashboard:
     - 😴 **Sleep Needed Tonight**: Dynamically calculated using daytime cumulative strain:
       $$\text{Sleep Target} = \text{Baseline Sleep} + \max\left(0, \frac{\text{Strain} - 50}{100} \times 1.5\right)$$
       *(Ensures slow-wave muscular recovery during sleep after high-exertion days).*
     - 🚶 **Daily Step Target**: Adapted to personal cardiovascular recovery capacity without inducing overtraining:
       $$\text{Step Target} = \text{Baseline Steps} \times \left(1 + \frac{\text{Strain} - 50}{200}\right)$$
     - 🪑 **Max Stillness Limit**: Fixed at `60 mins` based on WHO/Lancet clinical guidelines to prevent lipoprotein lipase suppression.
     - ❤️ **Cardio Readiness Score**: Systemic recovery percentage ($0–100\%$) balancing accumulated strain against overnight sleep debt.

3. **Acute Strain Anomaly Detection**:
   - If real-time strain exceeds $85\%$ while cardiorespiratory readiness drops below $25\%$, the model flags an anomaly (`is_anomaly = True`), alerting the user on-wrist to suspend high-intensity training.

---

## 3. Smartwatch Interaction & Gestures

| User Action | Watch Response |
|---|---|
| **Swipe Left / Right** | Flips between the **5 Circular Activity Rings**: Cardio Strain (Red) $\to$ Sleep (Cyan) $\to$ Steps (Green) $\to$ Stillness (Yellow) $\to$ Energy Burn (Orange). |
| **Tap Top Status Pill `[ 🏃‍♂️ Day 1 ▾ ]`** | Slides open the **On-Watch Profile Drawer** to switch users or view current baseline metrics. |
| **Tap Hardware Digital Crown** | Acts as the physical **Home Button**: instantly returns to the main watch face from any drawer, dial, or menu. |
| **Tap `[ ⏩ Advance 24h Wear ]`** | Simulates 24 hours of continuous wear to test Day 1 $\to$ Day 2 $\to$ Day 3 transitions directly on the display. |
| **Tap Indicator Dots `● ○ ○ ○ ○`** | Directly navigates to the selected ring index. |
| **Tap `+ Add Custom Person`** | Opens the on-watch creation dial to adjust emoji avatar, biological sex, and age with touch steppers (`-5`, `-1`, `+1`, `+5`). |

---

## 4. Scientific Literature & Standards References

1. **Cardiovascular Ceilings & Exertion**:
   - **Tanaka et al. (2001)** — *JACC*: $\text{HR}_{\max} = 208 - (0.7 \times \text{Age})$ ([DOI: 10.1016/S0735-1097(00)01054-8](https://doi.org/10.1016/S0735-1097(00)01054-8)).
   - **Gulati et al. (2010)** — *Circulation, AHA*: $\text{HR}_{\max} = 206 - (0.88 \times \text{Age})$ ([DOI: 10.1161/CIRCULATIONAHA.110.939249](https://doi.org/10.1161/CIRCULATIONAHA.110.939249)).
   - **Karvonen et al. (1957)** — *Ann Med Exp Biol Fenn*: Heart Rate Reserve formulation ([PMID: 13470504](https://pubmed.ncbi.nlm.nih.gov/13470504/)).
2. **Sleep Duration & Dynamic Strain Recovery**:
   - **Hirshkowitz et al. (2015)** — *National Sleep Foundation*: Age-stratified sleep duration guidelines ([DOI: 10.1016/j.sleh.2014.12.010](https://doi.org/10.1016/j.sleh.2014.12.010)).
   - **Belenky et al. (2003)** — *Journal of Sleep Research*: Sleep restriction and recovery dynamics ([DOI: 10.1046/j.1365-2869.2003.00337.x](https://doi.org/10.1046/j.1365-2869.2003.00337.x)).
3. **Sedentary Inactivity & Step Guidelines**:
   - **Ekelund et al. (2016 / 2019)** — *The Lancet / The BMJ*: Continuous sitting thresholds ($\le 60\text{ min}$) ([DOI: 10.1136/bmj.l4570](https://doi.org/10.1136/bmj.l4570)).
   - **Saint-Maurice et al. (2020)** — *JAMA / NIH / CDC*: Actigraphy step counts and mortality association ([DOI: 10.1001/jama.2020.1382](https://doi.org/10.1001/jama.2020.1382)).
