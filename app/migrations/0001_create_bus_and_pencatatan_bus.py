# Generated by Django 3.0 on 2020-11-22 06:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_po', models.CharField(max_length=20)),
                ('plat_no', models.CharField(max_length=10)),
                ('jenis_trayek', models.CharField(max_length=5)),
                ('jumlah_kursi', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PencatatanBus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jenis', models.CharField(max_length=2)),
                ('asal_tujuan_trayek', models.CharField(max_length=50)),
                ('waktu_datang', models.DateTimeField()),
                ('waktu_berangkat', models.DateTimeField(default=django.utils.timezone.now)),
                ('penumpang_datang', models.PositiveIntegerField()),
                ('penumpang_naik', models.PositiveIntegerField()),
                ('penumpang_turun', models.PositiveIntegerField()),
                ('penumpang_berangkat', models.PositiveIntegerField()),
                ('keterangan', models.CharField(max_length=10)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Bus')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
