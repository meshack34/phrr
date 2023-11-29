# Generated by Django 4.2.5 on 2023-11-29 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patientapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='additionaluser',
            old_name='uploaded_file',
            new_name='doctors_notes',
        ),
        migrations.AddField(
            model_name='additionaluser',
            name='preproceduralnotes',
            field=models.FileField(blank=True, null=True, upload_to='uploaded_files/'),
        ),
        migrations.AddField(
            model_name='additionaluser',
            name='referralnotes',
            field=models.FileField(blank=True, null=True, upload_to='uploaded_files/'),
        ),
    ]
