# Generated by Django 3.2.7 on 2021-10-11 22:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0003_auto_20211011_1631"),
    ]

    operations = [
        migrations.AlterField(
            model_name="choice",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
                verbose_name="UUID",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
                verbose_name="UUID",
            ),
        ),
        migrations.AlterField(
            model_name="vote",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
                verbose_name="UUID",
            ),
        ),
    ]
