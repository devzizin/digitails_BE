import uuid
from django.db import migrations


def gen_uuids(apps, schema_editor):
    User = apps.get_model('users', 'User')
    db_alias = schema_editor.connection.alias
    for user in User.objects.using(db_alias).all():
        user.uuid = uuid.uuid4()
        user.save(update_fields=['uuid'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_uuid'),
    ]

    operations = [
        migrations.RunPython(gen_uuids, noop),
    ]