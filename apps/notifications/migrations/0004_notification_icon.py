# Generated by Django 3.2.16 on 2023-03-07 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_auto_20230307_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='icon',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
