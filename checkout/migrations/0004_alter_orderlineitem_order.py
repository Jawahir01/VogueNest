# Generated by Django 3.2.25 on 2025-03-26 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20250326_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlineitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineitems', to='checkout.order'),
        ),
    ]
