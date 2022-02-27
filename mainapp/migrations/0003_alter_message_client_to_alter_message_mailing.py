# Generated by Django 4.0.2 on 2022-02-27 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_message_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='client_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clients_messages', to='mainapp.client'),
        ),
        migrations.AlterField(
            model_name='message',
            name='mailing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mailings_messages', to='mainapp.mailing'),
        ),
    ]
