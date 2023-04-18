# Generated by Django 4.2 on 2023-04-18 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("coin", models.CharField(max_length=8)),
                ("address", models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name="Master",
            fields=[
                (
                    "coin",
                    models.CharField(max_length=8, primary_key=True, serialize=False),
                ),
                ("seed", models.CharField(max_length=128)),
                ("private_key", models.CharField(max_length=128)),
                ("chain_code", models.CharField(max_length=128)),
            ],
        ),
    ]