import uuid
from django.db import migrations


def gen_uuids(apps, schema_editor):
    Company = apps.get_model('companies', 'Company')
    db_alias = schema_editor.connection.alias
    for company in Company.objects.using(db_alias).all():
        company.uuid = uuid.uuid4()
        company.save(update_fields=['uuid'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_company_uuid'),
    ]

    operations = [
        migrations.RunPython(gen_uuids, noop),
    ]