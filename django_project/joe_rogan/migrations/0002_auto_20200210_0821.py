# Generated by Django 3.0.3 on 2020-02-10 08:21

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('joe_rogan', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='joeroganpost',
            managers=[
                ('posts', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name='joeroganpost',
            name='quotes',
        ),
        migrations.AddField(
            model_name='joeroganpost',
            name='_quotes',
            field=models.CharField(default='[]', max_length=2048),
        ),
    ]
