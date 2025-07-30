You're right! Here's a working way to **download the final files** directly:

---

### ✅ `README.md`

**Download Link:** [Click to Download README.md](sandbox:/mnt/data/README.md)

Or manually copy content:

````markdown
# 🫀 ECG-Based Cardiovascular Disease Detection Algorithm

This repository provides a Python implementation of a rule-based algorithm for analyzing 12-lead ECG parameters to detect various cardiovascular abnormalities. The algorithm mimics clinical reasoning to interpret ECG findings and integrates components such as rhythm analysis, ST-segment evaluation, bundle branch block diagnosis, AV conduction assessment, and hypertrophy detection.

GitHub: [https://github.com/AmirGhaffari96/ECG_Disease](https://github.com/AmirGhaffari96/ECG_Disease)

## 🔍 Features

- **ST-Segment Elevation & Depression Analysis**
  - Localizes abnormalities to Anterior, Inferior, Lateral, or Posterior walls
- **Rhythm Detection**
  - Identifies sinus rhythms, junctional rhythms, tachycardia, bradycardia, atrial fibrillation, and more
- **Bundle Branch Block Diagnosis**
  - Detects RBBB, LBBB, and IVCD based on QRS morphology and duration
- **AV Conduction Abnormalities**
  - Differentiates Mobitz I, Mobitz II, and 3rd-degree AV blocks
- **Ventricular Hypertrophy**
  - Diagnoses LVH and RVH using Cornell and Sokolow–Lyon criteria

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/AmirGhaffari96/ECG_Disease.git
cd ECG_Disease
````

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🧪 Usage

Run the main script with sample ECG data:

```bash
python ecg_diagnosis.py
```

Example output:

```json
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
```

## 📁 File Structure

* `ecg_diagnosis.py` – Main ECG diagnostic algorithm
* `README.md` – Project documentation
* `requirements.txt` – Python dependencies

## 🛠 Requirements

```text
numpy
```

Install via:

```bash
pip install numpy
```

## ⚠️ Disclaimer

This software is for **educational and research purposes only** and is **not a medical device**. It is not approved for clinical use or diagnostic decision-making.

## 👨‍💻 Author

Amirhossein Ghaffari
📧 [ghaffari.amr@gmail.com](mailto:ghaffari.amr@gmail.com)
🌐 GitHub: [AmirGhaffari96](https://github.com/AmirGhaffari96)

```

---

### ✅ `requirements.txt`  
**Download Link:** [Click to Download requirements.txt](sandbox:/mnt/data/requirements.txt)

Or manually copy:

```

numpy

```

---

Let me know if you'd like me to also generate:
- `setup.py` to make it pip-installable,
- `ecg_diagnosis.py` as a separate file for GitHub upload, or
- a sample Jupyter notebook for demo.
```
