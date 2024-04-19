# from django.shortcuts import render
#
# # Create your views here.
# from pathlib import Path
# import pandas as pd
# from docxtpl import DocxTemplate
# import shutil
#
#
# def generate_contracts(excel_filename):
#     base_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
#     excel_path = base_dir / excel_filename
#     word_template_path = base_dir / "amaliyot11.docx"
#     output_dir = base_dir / "OUTPUT"
#
#     # Fayllarni o'qish va yaratish
#     output_dir.mkdir(exist_ok=True)
#     df = pd.read_excel(excel_path)
#
#     # Har bir qator uchun Word hujjatini yaratish va saqlash
#     for record in df.to_dict(orient="records"):
#         doc = DocxTemplate(word_template_path)
#         doc.render(record)
#         output_path = output_dir / f"{record['Talabaning_F_I_Sh']}-contract.docx"
#         doc.save(output_path)
#
#     # OUTPUT papkasini kompyuterga ko'chirish
#     shutil.make_archive("OUTPUT", "zip", output_dir)
#     shutil.move("OUTPUT.zip", str(base_dir))
#
#
# # Funksiya ishlatish
# generate_contracts("/Users/mbp13/Desktop/malumotlar.xlsx")

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from pathlib import Path
import pandas as pd
from docxtpl import DocxTemplate
import shutil
import os
from .serializers import FileUploadSerializer
#
# class GenerateContracts(APIView):
#     def post(self, request):
# class GenerateContracts(generics.CreateAPIView):
#     serializer_class = FileUploadSerializer
#     permission_classes = (permissions.AllowAny,)
#
#     def create(self, request, *args, **kwargs):
#         excel_filename = request.data.get('excel_filename')  # Excel fayl nomi
#         if not excel_filename:
#             return Response({'error': 'Excel fayl nomini yuboring'}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Fayllar va direktoriyalarni aniqlash
#         base_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
#         print(base_dir)
#         excel_path = base_dir / excel_filename
#         word_template_path = base_dir / "amaliyot11.docx"
#         output_dir = base_dir / "OUTPUT"
#
#         # Fayllarni o'qish va yaratish
#         output_dir.mkdir(exist_ok=True)
#         df = pd.read_excel(excel_path)
#
#         # Har bir qator uchun Word hujjatini yaratish va saqlash
#         for record in df.to_dict(orient="records"):
#             doc = DocxTemplate(word_template_path)
#             doc.render(record)
#             output_path = output_dir / f"{record['Talabaning_F_I_Sh']}-contract.docx"
#             doc.save(output_path)
#
#
#         return Response({'success': 'Contracts generated successfully', 'output_papka': str(output_dir)},
#                         status=status.HTTP_200_OK)



# def save_uploaded_file(upload_dir, uploaded_file):
#     file_path = os.path.join(upload_dir, uploaded_file.name)
#     with open(file_path, 'wb') as new_file:
#         for chunk in uploaded_file.chunks():
#             new_file.write(chunk)
#     return file_path
#
# class GenerateContracts(generics.CreateAPIView):
#     serializer_class = FileUploadSerializer
#     permission_classes = (permissions.AllowAny,)
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         excel_file = serializer.validated_data.get('excel_file')
#         if not excel_file:
#             return Response({'error': 'Excel faylni yuboring'}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Fayllarni va direktoriyalarni aniqlash
#         base_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
#         word_template_path = base_dir / "amaliyot11.docx"
#         output_dir = base_dir / "OUTPUT"
#         upload_dirs = base_dir / "UPLOAD"
#         # Faylni saqlash
#         saved_file_path = upload_dirs / excel_file.name
#         with open(saved_file_path, 'wb') as f:
#             for chunk in excel_file.chunks():
#                 f.write(chunk)
#
#         # Fayllarni o'qish va yaratish
#         output_dir.mkdir(exist_ok=True)
#         df = pd.read_excel(saved_file_path)
#
#         # Har bir qator uchun Word hujjatini yaratish va saqlash
#         for record in df.to_dict(orient="records"):
#             doc = DocxTemplate(word_template_path)
#             doc.render(record)
#             output_path = output_dir / f"{record['Talabaning_F_I_Sh']}-contract.docx"
#             doc.save(output_path)
#
#         return Response({'success': 'Contracts generated successfully', 'output_papka': str(output_dir)},
#                         status=status.HTTP_200_OK)


import os
from pathlib import Path

# def save_uploaded_file(upload_dir, uploaded_file):
#     file_path = os.path.join(upload_dir, uploaded_file.name)
#     with open(file_path, 'wb') as new_file:
#         for chunk in uploaded_file.chunks():
#             new_file.write(chunk)
#     return file_path


def save_uploaded_file(upload_dir, uploaded_file):
    upload_dir.mkdir(parents=True, exist_ok=True)  # UPLOAD katalogini yaratish
    file_path = upload_dir / uploaded_file.name
    with open(file_path, 'wb') as new_file:
        for chunk in uploaded_file.chunks():
            new_file.write(chunk)
    return file_path

class GenerateContracts(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        excel_file = serializer.validated_data.get('excel_file')
        if not excel_file:
            return Response({'error': 'Excel faylni yuboring'}, status=status.HTTP_400_BAD_REQUEST)

        # Fayllarni va direktoriyalarni aniqlash
        base_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
        word_template_path = base_dir / "amaliyot11.docx"
        output_dir = base_dir / "OUTPUT"
        upload_dir = base_dir / "UPLOAD"  # UPLOAD katalogi

        # Faylni saqlash
        saved_file_path = save_uploaded_file(upload_dir, excel_file)

        # Fayllarni o'qish va yaratish
        output_dir.mkdir(exist_ok=True)
        df = pd.read_excel(saved_file_path)

        # Har bir qator uchun Word hujjatini yaratish va saqlash
        for record in df.to_dict(orient="records"):
            doc = DocxTemplate(word_template_path)
            doc.render(record)
            output_path = output_dir / f"{record['Talabaning_F_I_Sh']}-contract.docx"
            doc.save(output_path)

        return Response({'success': 'Contracts generated successfully', 'output_papka': str(output_dir)},
                        status=status.HTTP_200_OK)
