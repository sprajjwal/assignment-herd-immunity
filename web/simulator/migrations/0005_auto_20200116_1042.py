# Generated by Django 3.0.2 on 2020-01-16 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0004_auto_20200115_1648'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experiment',
            old_name='init_infected',
            new_name='initial_infected',
        ),
        migrations.AlterField(
            model_name='experiment',
            name='mortality_chance',
            field=models.FloatField(help_text='How likely is a patient infected with the virus likely to succumb? Must be a percentage between 0.00 and 1.00.'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='reproductive_rate',
            field=models.FloatField(help_text='How effective is the virus at spreading between individuals? Must be a percentage between 0.00 and 1.00.'),
        ),
    ]