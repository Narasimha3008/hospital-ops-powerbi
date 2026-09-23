#!/usr/bin/env python3
"""Generate a synthetic hospital-operations dataset.

Deterministic (seeded). No real patient data — every name, DOB, and MRN is
fabricated. Tables: patients, departments, admissions (fact).

    python3 generate_data.py

Designed for the Power BI build guide in docs/BUILD_GUIDE.md.
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 7
DATA_DIR = Path(__file__).resolve().parent
START = date(2024, 1, 1)
END = date(2026, 8, 31)

DEPARTMENTS = [
    # (department, beds, base_daily_rate, avg_los)
    ("Emergency", 40, 1800, 1.2),
    ("Cardiology", 36, 3200, 4.5),
    ("Orthopedics", 30, 2800, 3.8),
    ("Pediatrics", 28, 2200, 3.2),
    ("Oncology", 24, 3500, 6.1),
    ("Neurology", 22, 3000, 5.0),
    ("General Surgery", 32, 3100, 4.2),
    ("ICU", 18, 5200, 7.5),
]

DIAGNOSES = {
    "Emergency": ["Chest Pain", "Fracture", "Laceration", "Abdominal Pain", "Asthma Attack"],
    "Cardiology": ["Heart Failure", "Arrhythmia", "Myocardial Infarction", "Hypertension"],
    "Orthopedics": ["Hip Replacement", "Knee Replacement", "Spinal Fusion", "Fracture Repair"],
    "Pediatrics": ["Pneumonia", "Bronchiolitis", "Dehydration", "Appendicitis"],
    "Oncology": ["Chemotherapy", "Lymphoma", "Lung Cancer", "Leukemia"],
    "Neurology": ["Stroke", "Seizure", "Migraine", "Parkinson's"],
    "General Surgery": ["Appendectomy", "Cholecystectomy", "Hernia Repair", "Bowel Resection"],
    "ICU": ["Sepsis", "Respiratory Failure", "Post-Surgical Care", "Trauma"],
}

PAYERS = ["Medicare", "Medicaid", "Private Insurance", "Self-Pay"]
PAYER_W = [0.34, 0.22, 0.38, 0.06]
DISPOSITIONS = ["Home", "Home Health", "Skilled Nursing", "Rehab", "Expired"]
DISP_W = [0.72, 0.12, 0.08, 0.06, 0.02]

FIRST = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael",
         "Linda", "David", "Elizabeth", "William", "Barbara", "Richard",
         "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen"]
LAST = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
CITIES = ["Madison", "Milwaukee", "Green Bay", "Kenosha", "Racine", "Appleton"]


def main():
    rng = random.Random(SEED)

    # ---- patients -------------------------------------------------------
    n_patients = 5000
    patients = []
    for i in range(1, n_patients + 1):
        age = max(1, min(98, int(rng.gauss(52, 22))))
        dob = date(2026, 1, 1) - timedelta(days=int(age * 365.25))
        patients.append({
            "patient_id": f"P{i:05d}",
            "first_name": rng.choice(FIRST),
            "last_name": rng.choice(LAST),
            "date_of_birth": dob.isoformat(),
            "gender": rng.choice(["M", "F"]),
            "city": rng.choice(CITIES),
        })

    # ---- departments ----------------------------------------------------
    departments = [
        {"department_id": i + 1, "department": d, "beds": beds,
         "base_daily_rate": rate}
        for i, (d, beds, rate, _) in enumerate(DEPARTMENTS)
    ]
    dept_by_name = {d: (beds, rate, avg_los)
                    for d, beds, rate, avg_los in DEPARTMENTS}

    # ---- admissions (fact) ----------------------------------------------
    admissions = []
    adm_id = 1

    def add_admission(pid, dept, adate):
        nonlocal adm_id
        beds, rate, avg_los = dept_by_name[dept]
        los = max(1, int(rng.expovariate(1 / avg_los)) + 1)
        los = min(los, 45)
        charges = round(rate * los * rng.uniform(0.85, 1.35)
                        + rng.uniform(500, 4000), 2)
        admissions.append({
            "admission_id": f"A{adm_id:06d}",
            "patient_id": pid,
            "department": dept,
            "diagnosis": rng.choice(DIAGNOSES[dept]),
            "admission_date": adate.isoformat(),
            "discharge_date": (adate + timedelta(days=los)).isoformat(),
            "length_of_stay": los,
            "payer": rng.choices(PAYERS, weights=PAYER_W)[0],
            "discharge_disposition": rng.choices(DISPOSITIONS, weights=DISP_W)[0],
            "total_charges": charges,
            "readmitted_30d": "FALSE",
        })
        adm_id += 1
        return adate + timedelta(days=los)

    # Base census: admissions skew toward recent dates (hospital growth story).
    n_base = 11000
    for _ in range(n_base):
        pid = f"P{rng.randint(1, n_patients):05d}"
        dept = rng.choices([d[0] for d in DEPARTMENTS],
                           weights=[d[1] for d in DEPARTMENTS])[0]
        day_offset = int((END - START).days * (rng.random() ** 0.7))
        add_admission(pid, dept, START + timedelta(days=day_offset))

    # Readmissions: ~12% of discharges return within 30 days.
    index_adms = [a for a in admissions
                  if a["discharge_disposition"] != "Expired"]
    rng.shuffle(index_adms)
    n_readmit = int(len(index_adms) * 0.12)
    for a in index_adms[:n_readmit]:
        disc = date.fromisoformat(a["discharge_date"])
        if disc > END - timedelta(days=30):
            continue
        a["readmitted_30d"] = "TRUE"
        add_admission(a["patient_id"], a["department"],
                      disc + timedelta(days=rng.randint(2, 28)))

    admissions.sort(key=lambda a: a["admission_date"])

    for name, rows in [("patients", patients),
                       ("departments", departments),
                       ("admissions", admissions)]:
        with open(DATA_DIR / f"{name}.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"{name}.csv: {len(rows):,} rows")


if __name__ == "__main__":
    main()
