# Generated by Django 4.2.16 on 2024-12-10 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0060_pickup_meta_alter_address_country_code_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customs",
            name="incoterm",
            field=models.CharField(
                choices=[
                    ("CFR", "CFR"),
                    ("CIF", "CIF"),
                    ("CIP", "CIP"),
                    ("CPT", "CPT"),
                    ("DAP", "DAP"),
                    ("DAF", "DAF"),
                    ("DDP", "DDP"),
                    ("DDU", "DDU"),
                    ("DEQ", "DEQ"),
                    ("DES", "DES"),
                    ("EXW", "EXW"),
                    ("FAS", "FAS"),
                    ("FCA", "FCA"),
                    ("FOB", "FOB"),
                ],
                db_index=True,
                max_length=20,
            ),
        ),
    ]
