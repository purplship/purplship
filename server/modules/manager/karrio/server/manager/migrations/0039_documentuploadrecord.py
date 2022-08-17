# Generated by Django 3.2.14 on 2022-08-17 01:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import functools
import karrio.server.core.models.base
import karrio.server.core.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('providers', '0035_alter_carrier_capabilities'),
        ('manager', '0038_alter_tracking_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentUploadRecord',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(default=functools.partial(karrio.server.core.models.base.uuid, *(), **{'prefix': 'uprec_'}), editable=False, max_length=50, primary_key=True, serialize=False)),
                ('documents', models.JSONField(blank=True, default=functools.partial(karrio.server.core.utils.identity, *(), **{'value': []}), null=True)),
                ('messages', models.JSONField(blank=True, default=functools.partial(karrio.server.core.utils.identity, *(), **{'value': []}), null=True)),
                ('meta', models.JSONField(blank=True, default=functools.partial(karrio.server.core.utils.identity, *(), **{'value': {}}), null=True)),
                ('options', models.JSONField(blank=True, default=functools.partial(karrio.server.core.utils.identity, *(), **{'value': {}}), null=True)),
                ('reference', models.CharField(blank=True, max_length=100, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('shipment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shipment_upload_record', to='manager.shipment')),
                ('upload_carrier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='providers.carrier')),
            ],
            options={
                'verbose_name': 'Document Upload Record',
                'verbose_name_plural': 'Document Upload Records',
                'db_table': 'document-upload-record',
                'ordering': ['-created_at'],
            },
            bases=(karrio.server.core.models.base.ControlledAccessModel, models.Model),
        ),
    ]
