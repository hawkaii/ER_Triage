# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Synthetic patient data for the ER Triage environment.

Based on the public Emergency Severity Index (ESI) handbook and vignette libraries.
"""

PATIENTS = [
    # CRITICAL (ESI 1-2)
    {
        "patient_id": "P001",
        "chief_complaint": "Chest pain, shortness of breath",
        "vitals": {"hr": 120, "bp": "90/60", "rr": 28, "temp": 37.0, "spo2": 88},
        "history": "History of heart disease",
        "demographics": {"age": 65, "gender": "Male"},
        "ground_truth_esi": 1,
        "ground_truth_priority": "critical",
        "ideal_steps": 1, # Should be triaged immediately based on vitals
    },
    {
        "patient_id": "P002",
        "chief_complaint": "Altered mental status",
        "vitals": {"hr": 110, "bp": "100/70", "rr": 22, "temp": 38.5, "spo2": 92},
        "history": "Diabetes",
        "demographics": {"age": 72, "gender": "Female"},
        "ground_truth_esi": 2,
        "ground_truth_priority": "critical",
        "ideal_steps": 2, # Vitals suggest problem, question about blood sugar would confirm
    },
    {
        "patient_id": "P003",
        "chief_complaint": "Severe abdominal pain",
        "vitals": {"hr": 115, "bp": "110/70", "rr": 20, "temp": 37.2, "spo2": 98},
        "history": "None",
        "demographics": {"age": 34, "gender": "Male"},
        "ground_truth_esi": 2, # High risk due to severe pain
        "ground_truth_priority": "critical",
        "ideal_steps": 2,
    },

    # URGENT (ESI 3)
    {
        "patient_id": "P004",
        "chief_complaint": "Headache and dizziness after falling",
        "vitals": {"hr": 80, "bp": "130/85", "rr": 18, "temp": 37.1, "spo2": 99},
        "history": "On blood thinners",
        "demographics": {"age": 78, "gender": "Female"},
        "ground_truth_esi": 3, # Needs multiple resources (CT scan, labs) due to fall + blood thinners
        "ground_truth_priority": "urgent",
        "ideal_steps": 3,
    },
    {
        "patient_id": "P005",
        "chief_complaint": "Cough and fever for 3 days",
        "vitals": {"hr": 95, "bp": "120/80", "rr": 20, "temp": 38.8, "spo2": 95},
        "history": "Asthma",
        "demographics": {"age": 45, "gender": "Male"},
        "ground_truth_esi": 3, # Needs chest x-ray and labs
        "ground_truth_priority": "urgent",
        "ideal_steps": 2,
    },

    # NON-URGENT (ESI 4-5)
    {
        "patient_id": "P006",
        "chief_complaint": "Sore throat and runny nose",
        "vitals": {"hr": 70, "bp": "110/70", "rr": 16, "temp": 37.5, "spo2": 99},
        "history": "None",
        "demographics": {"age": 25, "gender": "Female"},
        "ground_truth_esi": 5, # No resources needed
        "ground_truth_priority": "non-urgent",
        "ideal_steps": 1,
    },
    {
        "patient_id": "P007",
        "chief_complaint": "Twisted ankle",
        "vitals": {"hr": 85, "bp": "120/80", "rr": 18, "temp": 37.0, "spo2": 100},
        "history": "None",
        "demographics": {"age": 30, "gender": "Male"},
        "ground_truth_esi": 4, # Needs one resource (x-ray)
        "ground_truth_priority": "non-urgent",
        "ideal_steps": 2,
    },
    {
        "patient_id": "P008",
        "chief_complaint": "Needs a prescription refill",
        "vitals": {"hr": 75, "bp": "115/75", "rr": 16, "temp": 37.0, "spo2": 98},
        "history": "Hypertension (stable)",
        "demographics": {"age": 68, "gender": "Male"},
        "ground_truth_esi": 5,
        "ground_truth_priority": "non-urgent",
        "ideal_steps": 1,
    }
]