# Generated by Django 3.1.7 on 2021-05-10 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_auto_20210510_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='remember_token',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
    ]
