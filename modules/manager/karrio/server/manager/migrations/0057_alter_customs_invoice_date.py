# Generated by Django 4.2.10 on 2024-03-16 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0056_tracking_delivery_image_tracking_signature_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customs",
            name="invoice_date",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
