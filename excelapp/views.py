from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from pathlib import Path
import pandas as pd
from docxtpl import DocxTemplate
import shutil
import os
from .serializers import FileUploadSerializer
import os
from pathlib import Path
import excel2json


def count_student():
    excel2json.convert_from_file('records.xlsx')



def save_uploaded_file(upload_dir, uploaded_file):
    upload_dir.mkdir(parents=True, exist_ok=True)  # UPLOAD katalogini yaratish
    file_path = upload_dir / uploaded_file.name
    with open(file_path, 'wb') as new_file:
        for chunk in uploaded_file.chunks():
            new_file.write(chunk)
    return file_path


class GenerateContracts(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    permission_classes = (permissions.IsAdminUser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        excel_file = serializer.validated_data.get('excel_file')
        if not excel_file:
            return Response({'error': 'Excel faylni yuboring'}, status=status.HTTP_400_BAD_REQUEST)

        # Fayllarni va direktoriyalarni aniqlash
        base_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
        word_template_path = base_dir / "amaliyot11.docx"
        output_dir = base_dir / f"user_id_{request.user.id}" # yuklanadigan papka
        upload_dir = base_dir / "UPLOAD_excel"  # UPLOAD katalogi

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

        return Response({'success': 'Fayl yuborildi', 'output_papka': str(output_dir)},
                        status=status.HTTP_200_OK)


class DownloadOutputView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        base_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
        output_dir = base_dir / f"user_id_{request.user.id}"
        zip_file_path = base_dir / f"user_id_{request.user.id}.zip"

        # Check if OUTPUT directory exists
        if not output_dir.exists():
            return Response({'error': f'user_id_{request.user.id} topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        # Check if OUTPUT directory is empty
        if not os.listdir(output_dir):
            return Response({'error': f'yuklanadigan katalogi bo\'sh'}, status=status.HTTP_204_NO_CONTENT)

        # Create ZIP archive of OUTPUT directory
        shutil.make_archive(output_dir, 'zip', output_dir)

        # Return ZIP archive as FileResponse
        try:
            response = FileResponse(open(zip_file_path, 'rb'), as_attachment=True)
            return response
        except FileNotFoundError:
            return Response({'error': 'ZIP arxiv topilmadi'}, status=status.HTTP_404_NOT_FOUND)