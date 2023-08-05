# Generated by Django 3.0.3 on 2020-03-02 08:47

from django.db import migrations, models
import djangorestfilemanager.models


class Migration(migrations.Migration):

    dependencies = [
        ('djangorestfilemanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(storage=djangorestfilemanager.models.RestFileManagerStorage(location='media'), upload_to=djangorestfilemanager.models.set_storage_file_dir, verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='file',
            name='origin',
            field=models.CharField(blank=True, default='API', max_length=3, null=True, verbose_name='Origin'),
        ),
    ]
