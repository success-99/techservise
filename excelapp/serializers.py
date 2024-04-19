from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    excel_file = serializers.FileField()

    def validate_excel_file(self, value):
        # Faqat Excel faylni qabul qilish
        if not value.name.endswith('.xlsx'):
            raise serializers.ValidationError("Fayl .xlsx kengaytmasida bo'lishi kerak")
        return value
