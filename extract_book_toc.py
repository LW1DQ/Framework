import pdfplumber

pdf_path = r"D:\Nueva carpeta\OneDrive\AGENTES A2A\BIBLIOGRAFIA\Ai_agents_in_action.pdf"

try:
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total Pages: {len(pdf.pages)}")
        print("-" * 20)
        # Read first 20 pages to find TOC
        for i, page in enumerate(pdf.pages[:20]):
            text = page.extract_text()
            print(f"--- PAGE {i+1} ---")
            print(text)
            print("\n")
except Exception as e:
    print(f"Error reading PDF: {e}")
