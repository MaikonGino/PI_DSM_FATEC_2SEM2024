# Generated by Django 5.1.1 on 2024-10-24 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingrediente',
            name='imagem',
            field=models.FileField(upload_to='ingredientes/'),
        ),
    ]
