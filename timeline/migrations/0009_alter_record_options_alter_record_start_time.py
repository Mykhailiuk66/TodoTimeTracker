# Generated by Django 4.1.5 on 2023-01-09 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0008_alter_record_end_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='record',
            options={'ordering': ['start_time']},
        ),
        migrations.AlterField(
            model_name='record',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]