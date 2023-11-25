# Generated by Django 4.2.5 on 2023-11-25 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patientapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionaluser',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='additionaluser',
            name='gender',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='additionaluser',
            name='uploaded_file',
            field=models.FileField(blank=True, null=True, upload_to='uploaded_files/'),
        ),
    ]
