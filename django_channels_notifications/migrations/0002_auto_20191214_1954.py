from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('django_channels_notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='databasenotification',
            name='data',
            field=jsonfield.fields.JSONField(verbose_name='Data'),
        ),
    ]
