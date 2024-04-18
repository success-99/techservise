# import excel2json
#
# excel2json.convert_from_file('records.xlsx')
import excel2json
# import pandas
#
# excel_data_df = pandas.read_excel('records.xlsx', sheet_name='Employees')
# json_str = excel_data_df.to_json()
#
# print('Excel Sheet to JSON:\n', json_str)
import pandas as pd

def convert_excel_to_json(excel_file, json_file):
    # Excel faylini o'qish
    try:
        data = pd.read_excel(excel_file)
    except Exception as e:
        print(f"Xatolik: Excel faylini o'qishda xatolik yuz berdi: {e}")
        return

    # JSON formatiga o'zgartirish
    try:
        data.to_json(json_file, orient='records', indent=4)
    except Exception as e:
        print(f"Xatolik: JSON fayliga yozishda xatolik yuz berdi: {e}")
        return

    print(f"{excel_file} fayli {json_file} fayliga muvaffaqiyatli o'zgartirildi.")

# Eslatma: Excel va JSON fayllar nomi
excel_file = "records1.xlsx"
json_file = "rec.json"
# excel_data_df = pd.read_excel('records1.xlsx')
# json_str = excel_data_df.to_json()
#
print(excel2json.convert_from_file('records1.xlsx'))
# Excel faylini JSON formatiga o'zgartirish
convert_excel_to_json(excel_file, json_file)