# Generated by Django 3.2.8 on 2021-11-14 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portaldashboard', '0007_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answer_desc',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]