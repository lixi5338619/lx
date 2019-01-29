# Generated by Django 2.1.5 on 2019-01-17 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0003_buycar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.CharField(max_length=32)),
                ('order_time', models.DateTimeField(auto_now=True)),
                ('order_statue', models.CharField(max_length=32)),
                ('total', models.FloatField()),
                ('order_address', models.ForeignKey(on_delete=True, to='Buyer.Address')),
                ('user', models.ForeignKey(on_delete=True, to='Buyer.Buyer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_id', models.IntegerField()),
                ('goods_name', models.CharField(max_length=32)),
                ('goods_price', models.FloatField()),
                ('goods_num', models.IntegerField()),
                ('goods_picture', models.ImageField(upload_to='images')),
                ('order', models.ForeignKey(on_delete=True, to='Buyer.Order')),
            ],
        ),
    ]
