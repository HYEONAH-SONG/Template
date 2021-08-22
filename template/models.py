# 첫번째로 개발 : Model을 이용해 Database의 ORM(Object Relational Mappling)을 설계함
from django.db import models


# 업로드 일자 / 파일명 / 설명 / 업로드 일자 
class Template(models.Model):
    upload_files = models.FileField(blank=False, null=False)
    name = models.CharField(max_length = 50, primary_key = True)
    description = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # table name
        db_table = 'Templates'
