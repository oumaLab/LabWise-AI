class ExplanationAgent:
    def __init__(self):
        # Templates for Darija Explanations
        self.templates = {
            "Anemia": "Resultat dyalek taye3tini 'Anemia' (Faqr Dam). Hada ya3ni Hemoglobin naqs chwiya. Momkin thass b l3iya aw sokhfa. Khass chof tbib bach ya3tik dwa dyal lhdid ila kan khass.",
            "High Hb": "Hemoglobin tal3a chwiya. Momkin tkun ghir men qlet lma (Dehydration) aw ila kanti tetkmi. Mzyan tchreb lma mzyan.",
            "Leukopenia": "Kriyat lbid (WBC) naqsin. Hada ya3ni lmanaa dyalek hbat chwiya. Hadian m3a rawah w mikrobat.",
            "Leukocytosis": "Kriyat lbid (WBC) tal3in. Ghaleban kayn chi ta3afon (Infection) aw kerchek darrak. Darori tchof tbib.",
            "Thrombocytopenia": "Safa2ih (Platelets) naqsin. Rod balek men jarh, hit dam ghadi yta3tal bach yahbas. Khass istichara tibiya.",
            "Thrombocytosis": "Safa2ih (Platelets) tal3in. Momkin ikon reaction dyal ljesm m3a chi inflammation.",
            "Normal": "Nata2ij dyalek mzyana. Kolchi normal, lah ykhaffef 3lik."
        }
    
    def explain(self, analysis_report):
        """
        Synthesizes the explanation based on the report flags.
        """
        explanation_parts = []
        
        # Check Hb
        hb_status = analysis_report["hb"]["status"]
        if hb_status == "Low":
            explanation_parts.append(self.templates["Anemia"])
        elif hb_status == "High":
            explanation_parts.append(self.templates["High Hb"])
            
        # Check WBC
        wbc_status = analysis_report["wbc"]["status"]
        if wbc_status == "Low":
            explanation_parts.append(self.templates["Leukopenia"])
        elif wbc_status == "High":
            explanation_parts.append(self.templates["Leukocytosis"])
            
        # Check Platelets
        plt_status = analysis_report["platelets"]["status"]
        if plt_status == "Low":
            explanation_parts.append(self.templates["Thrombocytopenia"])
        elif plt_status == "High":
            explanation_parts.append(self.templates["Thrombocytosis"])
            
        if not explanation_parts: # All normal
            return "Hamdollah, Nata2ij 'Normal'. " + self.templates["Normal"]
            
        return " \n".join(explanation_parts) + "\n\n(Hada machi tkhsis (Diagnosis), hada ghir tawjih. Sir 3and tbib b warqa dyal tahlila.)"
