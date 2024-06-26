# Generated by Django 4.1.2 on 2023-01-31 10:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_category_options_alter_coupon_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Piska',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('piska_size', models.IntegerField(default=50)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
