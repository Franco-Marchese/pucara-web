# Generated by Django 4.1.3 on 2023-07-27 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Usuario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("contraseña", models.CharField(max_length=255)),
                ("nombre", models.CharField(max_length=255)),
                ("equipo", models.CharField(max_length=255)),
                ("es_admin", models.CharField(max_length=255)),
            ],
        ),
    ]
