# Generated by Django 4.1.5 on 2023-01-10 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_delete_cart'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-id']},
        ),
    ]
