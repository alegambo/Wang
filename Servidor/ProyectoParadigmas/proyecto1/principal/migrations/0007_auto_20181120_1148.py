# Generated by Django 2.1.3 on 2018-11-20 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0006_auto_20181120_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propuesta',
            name='respuesta',
            field=models.TextField(default='lo que sea'),
        ),
    ]