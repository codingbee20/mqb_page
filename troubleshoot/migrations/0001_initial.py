# Generated by Django 2.2.2 on 2020-06-16 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='issue',
            fields=[
                ('issueID', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('issueType', models.CharField(default='', max_length=30)),
                ('issueDescription', models.CharField(default='', max_length=250)),
            ],
        ),
    ]