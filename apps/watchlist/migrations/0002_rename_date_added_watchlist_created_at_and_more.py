# Generated by Django 5.1.6 on 2025-06-10 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("watchlist", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="watchlist",
            old_name="date_added",
            new_name="created_at",
        ),
        migrations.AddField(
            model_name="watchlist",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
