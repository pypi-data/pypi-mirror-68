# Generated by Django 3.0.5 on 2020-04-28 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appel_crises', '0007_emailoffset'),
    ]

    operations = [
        migrations.AddField(
            model_name='signature',
            name='from_asso',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
