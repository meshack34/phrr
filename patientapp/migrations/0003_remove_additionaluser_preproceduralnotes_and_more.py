# Generated by Django 4.2.5 on 2023-11-29 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patientapp', '0002_rename_uploaded_file_additionaluser_doctors_notes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='additionaluser',
            name='preproceduralnotes',
        ),
        migrations.RemoveField(
            model_name='additionaluser',
            name='referralnotes',
        ),
        migrations.CreateModel(
            name='files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referralnotes', models.FileField(blank=True, null=True, upload_to='uploaded_files/')),
                ('preproceduralnotes', models.FileField(blank=True, null=True, upload_to='uploaded_files/')),
                ('doctors_notes', models.FileField(blank=True, null=True, upload_to='uploaded_files/')),
                ('additional_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='patientapp.additionaluser')),
            ],
        ),
    ]
