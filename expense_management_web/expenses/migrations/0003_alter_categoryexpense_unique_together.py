# Generated by Django 5.0.6 on 2024-05-09 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_alter_categoryexpense_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='categoryexpense',
            unique_together=set(),
        ),
    ]