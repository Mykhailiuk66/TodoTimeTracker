# Generated by Django 4.1.5 on 2023-01-09 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_username'),
        ('timeline', '0006_timeline_active_timeline_owner_alter_record_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeline',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]
