# from pathlib import Path
# import pandas as pd
# from docxtpl import DocxTemplate
#
# # Skriptning joylashgan direktoriyani aniqlash
# base_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
#
# # Fayllarni aniqlash
# excel_path = base_dir / "malumotlar11.xlsx"
# word_template_path = base_dir / "amaliyot11.docx"
# output_dir = base_dir / "OUTPUT"
#
# # Fayllarni o'qish va yaratish
# output_dir.mkdir(exist_ok=True)
# df = pd.read_excel(excel_path)
#
# # Har bir qator uchun Word hujjatini yaratish va saqlash
# for record in df.to_dict(orient="records"):
#     doc = DocxTemplate(word_template_path)
#     doc.render(record)
#     output_path = output_dir / f"{record['Talabaning_F_I_Sh']}-contract.docx"
#     doc.save(output_path)

from pathlib import Path
import pandas as pd
from docxtpl import DocxTemplate
import shutil


def generate_contracts(excel_filename):
    base_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    excel_path = base_dir / excel_filename
    word_template_path = base_dir / "amaliyot11.docx"
    output_dir = base_dir / "OUTPUT"

    # Fayllarni o'qish va yaratish
    output_dir.mkdir(exist_ok=True)
    df = pd.read_excel(excel_path)

    # Har bir qator uchun Word hujjatini yaratish va saqlash
    for record in df.to_dict(orient="records"):
        doc = DocxTemplate(word_template_path)
        doc.render(record)
        output_path = output_dir / f"{record['Talabaning_F_I_Sh']}-contract.docx"
        doc.save(output_path)

    # OUTPUT papkasini kompyuterga ko'chirish
    shutil.make_archive("OUTPUT", "zip", output_dir)
    shutil.move("OUTPUT.zip", str(base_dir))


# Funksiya ishlatish
generate_contracts("/Users/mbp13/Desktop/malumotlar.xlsx")