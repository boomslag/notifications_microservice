# Generated by Django 3.2.16 on 2023-03-06 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.UUIDField(blank=True, null=True)),
                ('product', models.UUIDField(blank=True, null=True)),
                ('order', models.UUIDField(blank=True, null=True)),
                ('order_item', models.UUIDField(blank=True, null=True)),
                ('thread', models.UUIDField(blank=True, null=True)),
                ('from_user', models.UUIDField(blank=True, null=True)),
                ('to_user', models.UUIDField(blank=True, null=True)),
                ('notification_type', models.IntegerField(choices=[(1, 'Like'), (2, 'Comment'), (3, 'Followed'), (4, 'Purchased'), (5, 'Delivery'), (6, 'Message')])),
                ('text_preview', models.CharField(blank=True, max_length=255)),
                ('url', models.CharField(blank=True, max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_seen', models.BooleanField(default=False)),
            ],
        ),
    ]
