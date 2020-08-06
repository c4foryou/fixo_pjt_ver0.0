# Generated by Django 3.0.7 on 2020-07-31 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalStatement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=50, null=True)),
                ('job_position', models.CharField(max_length=50, null=True)),
                ('is_answer_completed', models.BooleanField(null=True)),
                ('is_correction_completed', models.BooleanField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('applicant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Applicant')),
                ('corrector', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Corrector')),
            ],
            options={
                'db_table': 'personal_statements',
            },
        ),
        migrations.CreateModel(
            name='StatementList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement_question', models.TextField(max_length=50000, null=True)),
                ('statement_answer', models.TextField(max_length=50000, null=True)),
                ('statement_correction', models.TextField(max_length=50000, null=True)),
                ('statement_comment', models.TextField(max_length=50000, null=True)),
                ('order', models.IntegerField(null=True)),
                ('statement', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='statement.PersonalStatement')),
            ],
            options={
                'db_table': 'statement_lists',
            },
        ),
    ]
