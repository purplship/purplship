# Generated by Django 4.2.10 on 2024-02-25 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("providers", "0067_fedexsettings"),
    ]

    operations = [
        migrations.AddField(
            model_name="fedexsettings",
            name="track_api_key",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="fedexsettings",
            name="track_secret_key",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="fedexsettings",
            name="account_number",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="fedexsettings",
            name="api_key",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="fedexsettings",
            name="secret_key",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
