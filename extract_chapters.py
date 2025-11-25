import pdfplumber

pdf_path = r"D:\Nueva carpeta\OneDrive\AGENTES A2A\BIBLIOGRAFIA\Ai_agents_in_action.pdf"

# Mapping of Chapter Title to Output Name
chapters_to_find = {
    "Exploring multi-agent systems": "Chapter_4_MultiAgent",
    "Understanding agent memory and knowledge": "Chapter_8_Memory",
    "Agent planning and feedback": "Chapter_11_Planning"
}

extracted_content = {name: "" for name in chapters_to_find.values()}
active_extraction = {name: 0 for name in chapters_to_find.values()} # Pages left to read

try:
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Scanning {len(pdf.pages)} pages for chapters...")
        
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text: continue
            
            # Check for chapter starts
            for title, name in chapters_to_find.items():
                # Heuristic: Title must be in the first 10 lines of the page
                # and "Chapter" must also be present nearby or just the title is unique enough as a header
                lines = text.split('\n')[:10]
                if any(title in line for line in lines):
                    # Avoid TOC matches: TOC usually has "......" or page numbers at the end of the line
                    # But let's just check if we haven't started extracting yet
                    if active_extraction[name] == 0:
                        print(f"Found '{title}' at page {i+1}")
                        active_extraction[name] = 15 # Extract 15 pages
            
            # Extract content if active
            for name, pages_left in active_extraction.items():
                if pages_left > 0:
                    extracted_content[name] += f"\n\n--- Page {i+1} ---\n{text}"
                    active_extraction[name] -= 1

        # Save to file
        with open("book_analysis_extract_v2.txt", "w", encoding="utf-8") as f:
            for name, content in extracted_content.items():
                f.write(f"\n\n=== {name} ===\n{content}")
                
        print("Extraction complete. Saved to book_analysis_extract_v2.txt")

except Exception as e:
    print(f"Error: {e}")
