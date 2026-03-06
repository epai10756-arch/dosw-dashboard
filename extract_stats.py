
import zipfile, xml.etree.ElementTree as ET
import os, glob

# Find the docx file dynamically
base_dir = r"d:/projetcts/dosw-dashboard(claude)"
docx_files = glob.glob(base_dir + "/*.docx")
if not docx_files:
    raise FileNotFoundError("No .docx file found in " + base_dir)
docx_path = docx_files[0]
print("Using file:", docx_path)

with zipfile.ZipFile(docx_path) as z:
    xml_bytes = z.read("word/document.xml").decode("utf-8")

ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
root = ET.fromstring(xml_bytes)

def get_para_text(para):
    return "".join(r.text or "" for r in para.findall(".//w:t", ns))

paras = root.findall(".//w:p", ns)
texts = [get_para_text(p) for p in paras]

output_lines = []
keywords = ["\u6848\u4ef6\u7d71\u8a08", "\u516c\u8fa6\u516c\u71df", "\u516c\u8fa6\u6c11\u71df", "\u65b9\u6848\u59d4\u8a17", "\u5e02\u6709\u623f\u5730", "\u6848\u4ef6\u985e\u578b", "\u5b30\u5e7c\u5152", "\u8eab\u5fc3\u969c\u7919", "\u9280\u9aee\u65cf"]
for i, t in enumerate(texts):
    if any(k in t for k in keywords) and len(t.strip()) > 3:
        output_lines.append("[" + str(i) + "] " + t[:200])

tables = root.findall(".//w:tbl", ns)
output_lines.append("")
output_lines.append("Total tables found: " + str(len(tables)))

for ti, tbl in enumerate(tables):
    rows = tbl.findall(".//w:tr", ns)
    row_texts = []
    for row in rows:
        cells = row.findall(".//w:tc", ns)
        cell_texts = ["".join(r.text or "" for r in cell.findall(".//w:t", ns)) for cell in cells]
        row_texts.append(" | ".join(cell_texts))
    full_text = "".join(row_texts)
    if any(k in full_text for k in ["\u5b30\u5e7c\u5152", "\u6848\u4ef6\u7d71\u8a08", "\u516c\u8fa6\u516c\u71df", "\u65b9\u6848\u59d4\u8a17"]):
        output_lines.append("")
        output_lines.append("=== TABLE " + str(ti) + " ===")
        for r in row_texts:
            if r.strip():
                output_lines.append(r)

out_path = base_dir + "/stats_table_extract.txt"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))
print("Done. Written to: " + out_path)
print("Lines written:", len(output_lines))
