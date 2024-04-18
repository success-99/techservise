from pathlib import Path
import pandas as pd
from docxtpl import DocxTemplate

# Skriptning joylashgan direktoriyani aniqlash
base_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()

# Fayllarni aniqlash
excel_path = base_dir / "malumotlar.xlsx"
word_template_path = base_dir / "amaliyot.docx"
output_dir = base_dir / "OUTPUT"

# Fayllarni o'qish va yaratish
output_dir.mkdir(exist_ok=True)
df = pd.read_excel(excel_path)

# Har bir qator uchun Word hujjatini yaratish va saqlash
for record in df.to_dict(orient="records"):
    print(record)
    doc = DocxTemplate(word_template_path)
    doc.render(record)
    output_path = output_dir / f"{record['Talabaning_F_I_Sh']}-contract.docx"
    doc.save(output_path)