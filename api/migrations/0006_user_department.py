# Generated by Django 3.1.5 on 2021-01-14 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_user_university'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='api.department'),
            preserve_default=False,
        ),
    ]