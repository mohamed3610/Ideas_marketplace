# Generated by Django 4.2 on 2024-02-01 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ideas', '0007_featurescore_alter_features_cost_percentage_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='score',
            old_name='originaity',
            new_name='originality',
        ),
    ]
