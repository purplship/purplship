# Generated by Django 4.2.10 on 2024-02-25 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("providers", "0068_fedexsettings_track_api_key_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="canadapostsettings",
            name="contract_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="canadapostsettings",
            name="customer_number",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
