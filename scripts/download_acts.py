"""
Green Guardian: Environmental Law PDF Downloader
Downloads the 10 foundational US & Global Environmental Acts/Treaties from official GovInfo / UN repositories.
"""

import os
import ssl
import urllib.request
from pathlib import Path

LAWS = [
    {
        "filename": "1_National_Environmental_Policy_Act_NEPA.pdf",
        "title": "National Environmental Policy Act of 1969 (NEPA)",
        "citation": "42 U.S.C. § 4321 et seq.",
        "url": "https://www.govinfo.gov/content/pkg/COMPS-10352/pdf/COMPS-10352.pdf"
    },
    {
        "filename": "2_Clean_Air_Act_CAA.pdf",
        "title": "Clean Air Act (CAA - Full Compilation)",
        "citation": "42 U.S.C. § 7401 et seq.",
        "url": "https://www.govinfo.gov/content/pkg/COMPS-8160/pdf/COMPS-8160.pdf"
    },
    {
        "filename": "3_Clean_Water_Act_CWA.pdf",
        "title": "Clean Water Act (CWA - Federal Water Pollution Control Act)",
        "citation": "33 U.S.C. § 1251 et seq.",
        "url": "https://www.govinfo.gov/content/pkg/COMPS-2989/pdf/COMPS-2989.pdf"
    },
    {
        "filename": "4_Endangered_Species_Act_ESA.pdf",
        "title": "Endangered Species Act of 1973 (ESA - Full Compilation)",
        "citation": "16 U.S.C. § 1531 et seq.",
        "url": "https://www.govinfo.gov/content/pkg/COMPS-3002/pdf/COMPS-3002.pdf"
    },
    {
        "filename": "5_Superfund_CERCLA.pdf",
        "title": "Comprehensive Environmental Response, Compensation, and Liability Act (CERCLA / Superfund)",
        "citation": "42 U.S.C. § 9601 et seq.",
        "url": "https://www.govinfo.gov/content/pkg/COMPS-886/pdf/COMPS-886.pdf"
    },
    {
        "filename": "6_Safe_Drinking_Water_Act_SDWA.pdf",
        "title": "Safe Drinking Water Act (SDWA)",
        "citation": "42 U.S.C. § 300f et seq.",
        "url": "https://www.govinfo.gov/content/pkg/COMPS-892/pdf/COMPS-892.pdf"
    },
    {
        "filename": "7_Resource_Conservation_and_Recovery_Act_RCRA.pdf",
        "title": "Resource Conservation and Recovery Act (RCRA / Solid Waste Disposal Act)",
        "citation": "42 U.S.C. § 6901 et seq.",
        "url": "https://www.govinfo.gov/content/pkg/COMPS-893/pdf/COMPS-893.pdf"
    },
    {
        "filename": "8_Toxic_Substances_Control_Act_TSCA.pdf",
        "title": "Toxic Substances Control Act (TSCA)",
        "citation": "15 U.S.C. § 2601 et seq.",
        "url": "https://www.govinfo.gov/content/pkg/COMPS-1045/pdf/COMPS-1045.pdf"
    },
    {
        "filename": "9_Paris_Climate_Agreement.pdf",
        "title": "The Paris Agreement (UNFCCC)",
        "citation": "UN Treaty Series No. 54113 / FCCC/CP/2015/L.9/Rev.1",
        "url": "https://unfccc.int/resource/docs/2015/cop21/eng/l09r01.pdf"
    },
    {
        "filename": "10_Kunming_Montreal_Global_Biodiversity_Framework.pdf",
        "title": "Kunming-Montreal Global Biodiversity Framework (CBD / COP15)",
        "citation": "CBD/COP/15/L.25",
        "url": "https://www.cbd.int/doc/c/e6d3/cd1d/daf663719a03902a9b116c34/cop-15-l-25-en.pdf"
    }
]

def download_all_laws(output_dir: str = "data/pdfs"):
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    print(f"Downloading {len(LAWS)} verified environmental acts/treaties to '{output_dir}'...\n")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/pdf,*/*"
    }

    success_count = 0
    for idx, law in enumerate(LAWS, 1):
        target_file = out_path / law["filename"]
        print(f"[{idx}/{len(LAWS)}] {law['title']} ({law['citation']})")
        print(f"    Source URL: {law['url']}")
        
        try:
            req = urllib.request.Request(law["url"], headers=headers)
            with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
                content = response.read()
                
                # Verify PDF header
                if not content.startswith(b"%PDF"):
                    print(f"    ERROR: Content is not a valid PDF (header: {content[:15]})\n")
                    continue
                
                with open(target_file, "wb") as f:
                    f.write(content)
                
                size_kb = len(content) / 1024
                print(f"    SUCCESS -> Valid PDF saved as {law['filename']} ({size_kb:.1f} KB)\n")
                success_count += 1
        except Exception as e:
            print(f"    FAILED -> {e}\n")

    print(f"Finished! Successfully verified and downloaded {success_count}/{len(LAWS)} official PDF statutes.")

if __name__ == "__main__":
    download_all_laws()
