# Generated by Django 5.0.7 on 2024-07-12 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='watches',
            name='brand',
            field=models.CharField(default='Casio', max_length=155, verbose_name='Brand'),
            preserve_default=False,
        ),
    ]