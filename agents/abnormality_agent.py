class AbnormalityAgent:
    def __init__(self):
        # Reference ranges (Simplified WHO/Standard)
        self.ranges = {
            "Male": {
                "hb": (13.5, 17.5),
                "wbc": (4500, 11000),
                "platelets": (150000, 450000)
            },
            "Female": {
                "hb": (12.0, 15.5),
                "wbc": (4500, 11000),
                "platelets": (150000, 450000)
            }
        }

    def analyze(self, gender, hb, wbc, platelets):
        """
        Analyzes the patient's values against the reference ranges.
        Returns a dictionary with status for each parameter.
        """
        gender = gender.capitalize()
        if gender not in self.ranges:
            gender = "Male" # Default fall back if error

        ref = self.ranges[gender]
        
        report = {}
        
        # Hemoglobin Analysis
        if hb < ref["hb"][0]:
            report["hb"] = {"status": "Low", "severity": "Anemia"}
        elif hb > ref["hb"][1]:
            report["hb"] = {"status": "High", "severity": "High Hb"}
        else:
            report["hb"] = {"status": "Normal", "severity": "Normal"}

        # WBC Analysis
        if wbc < ref["wbc"][0]:
            report["wbc"] = {"status": "Low", "severity": "Leukopenia"}
        elif wbc > ref["wbc"][1]:
            report["wbc"] = {"status": "High", "severity": "Leukocytosis (Infection check)"}
        else:
            report["wbc"] = {"status": "Normal", "severity": "Normal"}

        # Platelets Analysis
        if platelets < ref["platelets"][0]:
            report["platelets"] = {"status": "Low", "severity": "Thrombocytopenia"}
        elif platelets > ref["platelets"][1]:
            report["platelets"] = {"status": "High", "severity": "Thrombocytosis"}
        else:
            report["platelets"] = {"status": "Normal", "severity": "Normal"}

        return report
