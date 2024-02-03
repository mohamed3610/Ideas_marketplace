# Generated by Django 4.2 on 2024-02-02 16:41

import Ideas.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ideas', '0008_rename_originaity_score_originality'),
    ]

    operations = [
        migrations.RenameField(
            model_name='score',
            old_name='cost_efective',
            new_name='cost_effective',
        ),
        migrations.AddField(
            model_name='score',
            name='COST_EFFECTIVE_WEIGHT',
            field=models.FloatField(default=0.1, validators=[Ideas.models.validate_minmax]),
        ),
        migrations.AddField(
            model_name='score',
            name='FEASIBILITY_WEIGHT',
            field=models.FloatField(default=0.2, validators=[Ideas.models.validate_minmax]),
        ),
        migrations.AddField(
            model_name='score',
            name='MARKET_VALUE_WEIGHT',
            field=models.FloatField(default=0.3, validators=[Ideas.models.validate_minmax]),
        ),
        migrations.AddField(
            model_name='score',
            name='ORIGINALITY_WEIGHT',
            field=models.FloatField(default=0.1, validators=[Ideas.models.validate_minmax]),
        ),
        migrations.AddField(
            model_name='score',
            name='RISK_WEIGHT',
            field=models.FloatField(default=0.15, validators=[Ideas.models.validate_minmax]),
        ),
        migrations.AddField(
            model_name='score',
            name='VALUE_PROPOSITION_WEIGHT',
            field=models.FloatField(default=0.15, validators=[Ideas.models.validate_minmax]),
        ),
    ]