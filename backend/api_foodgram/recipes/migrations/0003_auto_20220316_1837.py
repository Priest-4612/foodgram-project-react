# Generated by Django 2.2.16 on 2022-03-16 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220314_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_in_shopping_cart', to='recipes.Recipe'),
        ),
    ]