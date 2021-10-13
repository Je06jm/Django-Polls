# Generated by Django 3.2.7 on 2021-10-11 23:03

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0004_auto_20211011_1635"),
    ]

    operations = [
        migrations.CreateModel(
            name="Option",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="UUID",
                    ),
                ),
                ("option_text", models.CharField(max_length=200)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="polls.question"
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="vote",
            name="choice",
        ),
        migrations.DeleteModel(
            name="Choice",
        ),
        migrations.AddField(
            model_name="vote",
            name="option",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="polls.option",
            ),
        ),
    ]
