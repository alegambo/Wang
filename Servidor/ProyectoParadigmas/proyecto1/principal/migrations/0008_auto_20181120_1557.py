# Generated by Django 2.1.3 on 2018-11-20 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0007_auto_20181120_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propuesta',
            name='respuesta',
            field=models.TextField(null=True),
        ),
    ]
