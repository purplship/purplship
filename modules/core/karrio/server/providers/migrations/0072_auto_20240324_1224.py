# Generated by Django 4.2.11 on 2024-03-24 12:24

from django.db import migrations


def forwards_func(apps, schema_editor):
    import karrio.server.providers.models as providers

    db_alias = schema_editor.connection.alias

    if "canadapost" in providers.MODELS:
        Config = apps.get_model("providers", "CarrierConfig")
        configs = (
            Config.objects.using(db_alias)
            .filter(carrier__canadapostsettings__isnull=False)
            .iterator()
        )

        Carrier = apps.get_model("providers", "Carrier")
        carriers = (
            Carrier.objects.using(db_alias)
            .filter(
                canadapostsettings__isnull=False,
                configs__isnull=True,
            )
            .iterator()
        )

        _configs = []

        for config in configs:
            config.config = {
                **config.config,
                "transmit_shipment_by_default": True,
            }
            _configs.append(config)

        if any(_configs):
            Config.objects.using(db_alias).bulk_update(_configs, ["config"])

        for carrier in carriers:
            carrier.configs.create(
                carrier=carrier.pk,
                config={
                    "transmit_shipment_by_default": True,
                },
                created_by=carrier.created_by,
            )


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("providers", "0071_alter_tgesettings_my_toll_token"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
