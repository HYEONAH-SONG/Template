from django.db import models

# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length = 50, primary_key = True)
    password = models.CharField(max_length = 100)

    class Meta:
        # table name
        db_table = 'accounts'