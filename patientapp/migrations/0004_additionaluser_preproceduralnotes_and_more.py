# Generated by Django 4.2.5 on 2023-11-29 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patientapp', '0003_remove_additionaluser_preproceduralnotes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionaluser',
            name='preproceduralnotes',
            field=models.FileField(blank=True, null=True, upload_to='uploaded_preprocedural/'),
        ),
        migrations.AddField(
            model_name='additionaluser',
            name='referralnotes',
            field=models.FileField(blank=True, null=True, upload_to='uploaded_referal/'),
        ),
        migrations.AlterField(
            model_name='additionaluser',
            name='doctors_notes',
            field=models.FileField(blank=True, null=True, upload_to='uploaded_doctor/'),
        ),
        migrations.DeleteModel(
            name='files',
        ),
    ]
