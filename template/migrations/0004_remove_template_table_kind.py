# Generated by Django 3.2.5 on 2021-08-18 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0003_alter_template_table_kind'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='template_table',
            name='kind',
        ),
    ]
