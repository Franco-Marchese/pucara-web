# Generated by Django 4.1.3 on 2023-08-28 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appUsuarios", "0002_alter_usuario_es_admin"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="telefono",
            field=models.CharField(default="", max_length=255),
        ),
    ]
