# Generated by Django 4.2.1 on 2023-05-16 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_mxrecordall_country_mxrecordall_state_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mxrecordall',
            name='selected_month',
            field=models.CharField(default='', max_length=70),
        ),
        migrations.AddField(
            model_name='mxrecordcurrent',
            name='selected_month',
            field=models.CharField(default='', max_length=70),
        ),
    ]
