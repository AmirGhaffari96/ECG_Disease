>

# 🫀 ECG-Based Cardiovascular Disease Detection Algorithm

A Python implementation of a **rule-based algorithm** for interpreting 12-lead ECG findings and detecting major cardiovascular diseases. This tool mimics clinical workflow, providing readable outputs for use in research, prototyping, and educational environments.

GitHub: [https://github.com/AmirGhaffari96/ECG_Disease]

---

## 🔬 Medical Background & Algorithmic Scope

This repository provides a **clinical reasoning-inspired approach** to ECG analysis. The algorithm detects:

- **ST-segment elevation and depression** (ischemia/infarction, localization by affected wall)
- **Arrhythmias** (sinus, atrial fibrillation, tachy/bradycardia, junctional rhythms)
- **Bundle branch/conduction blocks** (RBBB, LBBB, IVCD)
- **Atrioventricular (AV) conduction disturbances** (Mobitz I, Mobitz II, 3rd-degree block)
- **Ventricular hypertrophy** (LVH, RVH)

**References and criteria** are based on widely-accepted sources such as AHA/ACC/HRS 2017, European Society of Cardiology (ESC) 2020, and core cardiology texts (see below).

---

## 🔑 Required Parameters (Inputs)

The algorithm processes **lead-wise ECG parameter values**, which can be extracted from digitized signals or exported from ECG interpretation software.  
**Typical inputs:**

- **ST-segment deviation** (in mV) for all 12 leads
- **QRS duration** (ms)
- **PR interval** (ms)
- **Heart rate** (bpm)
- **Presence/absence of P waves** (per beat or per lead)
- **R-wave and S-wave amplitudes** (for Sokolow–Lyon, Cornell criteria)
- **RR intervals** (for rhythm analysis)
- **Other morphological features** (optional: T-wave, U-wave, axis, etc.)

Inputs can be provided as Python dictionaries, NumPy arrays, or Pandas DataFrames depending on your integration.

---

## 🩺 Medical Evidence for Algorithm Components

Each major step in the code uses **clinically validated rules:**

- **ST-Segment Elevation/Depression**
  - **Criteria:** ≥1 mm (0.1 mV) elevation in contiguous leads; localized to anterior (V1–V4), inferior (II, III, aVF), lateral (I, aVL, V5–V6), posterior (V7–V9).
  - **Medical Evidence:** [AHA/ACC STEMI Guidelines](https://www.ahajournals.org/doi/10.1161/CIR.0000000000000560)

- **Bundle Branch Block**
  - **RBBB:** QRS ≥120 ms, rsR’/broad R in V1, wide S in I/V6.
  - **LBBB:** QRS ≥120 ms, broad/notched R in I/V6, absent Q in I/V6.
  - **IVCD:** QRS ≥110 ms, but not fulfilling RBBB/LBBB.
  - **Reference:** [AHA/ACC/HRS 2017 Recommendations](https://www.ahajournals.org/doi/10.1161/CIR.0000000000000504)

- **AV Conduction Blocks**
  - **First-degree:** PR >200 ms.
  - **Mobitz I (Wenckebach):** Progressive PR lengthening then dropped QRS.
  - **Mobitz II:** Sudden non-conducted P wave(s) without PR change.
  - **Third-degree:** P and QRS dissociated.
  - **Reference:** [ESC 2021 AV Block Guidelines](https://academic.oup.com/eurheartj/article/42/14/1387/6289186)

- **Ventricular Hypertrophy**
  - **LVH:** Sokolow–Lyon (S in V1 + R in V5/V6 > 3.5 mV), Cornell (R in aVL + S in V3 > 2.8 mV [men], >2.0 mV [women])
  - **RVH:** Tall R in V1, right axis, S in V5/V6.
  - **Reference:** [ESC ECG Criteria for LVH/RVH](https://academic.oup.com/eurheartj/article/43/36/3627/6672732)

- **Rhythm Analysis**
  - Sinus rhythm, tachycardia (>100 bpm), bradycardia (<60 bpm), AF (irregular RR, absent P), etc.

---

## 🏥 Predicted Diseases and Conditions

| Algorithm Output        | Typical Clinical Interpretation             |
|------------------------|---------------------------------------------|
| **ST elevation**       | Acute MI/STEMI, pericarditis, etc.          |
| **ST depression**      | Ischemia, NSTEMI, digoxin effect            |
| **LBBB/RBBB/IVCD**     | Conduction disease, risk stratification     |
| **Mobitz/3rd-degree**  | High-grade AV block, pacemaker indications  |
| **LVH/RVH**            | Hypertension, valvular/congenital disease   |
| **Rhythm findings**    | Atrial fibrillation, flutter, brady/tachy   |

Always correlate algorithmic output with **clinical context and 12-lead ECG review**.

---

## 🖥 File Structure

- `Conventional ECG_edited.py` – Main rule-based diagnostic algorithm  
- `README.md` – Project documentation  
- `requirements.txt` – Dependencies

---

## 🚀 Usage

Clone and run:

```bash
git clone https://github.com/AmirGhaffari96/ECG_Disease.git
cd ECG_Disease
python Conventional\ ECG_edited.py

Provide ECG parameter data as described in the script. The program will print diagnostic findings to the console or output file (see code for details).
📊 Example Output

{
  "st_analysis": {
    "st_elevation": true,
    "localization": {
      "region": "Anterior",
      "leads": ["V1", "V2", "V3"],
      "max_st_elev": 0.4
    },
    "st_depression": true
  },
  "av_conduction": {
    "p_waves": 5,
    "qrs_complexes": 5,
    "missing_beats": 0,
    "classification": "Normal conduction"
  },
  "conduction_abnormality": "IVCD",
  "hypertrophy": "LVH",
  "rhythm": "Normal sinus rhythm"
}

🛠 Requirements

    Python 3.7+

    numpy

    pandas

    matplotlib

    sklearn

Install all requirements with:

pip install -r requirements.txt

⚠️ Disclaimer

This code is for research and educational use only. It is not a substitute for professional medical advice, diagnosis, or treatment.
Do not use for patient care or clinical decision-making.
📚 References

    AHA/ACC/HRS 2017 Guidelines for ECG Interpretation

    ESC 2020/2021 Recommendations

    Marriot’s Practical Electrocardiography, 13th Ed.

    Braunwald’s Heart Disease, 12th Ed.
