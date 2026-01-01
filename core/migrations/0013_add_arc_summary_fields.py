# Generated migration for ARC Summary fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_attendancerecord_hours'),
    ]

    operations = [
        # Change overtime_to_mandays from TimeField to CharField
        migrations.AlterField(
            model_name='attendancerecord',
            name='overtime_to_mandays',
            field=models.CharField(blank=True, max_length=20, verbose_name='OVERTIME TO MANDAYS'),
        ),
        # Add ARC Summary specific fields
        migrations.AddField(
            model_name='attendancerecord',
            name='cont_code',
            field=models.CharField(blank=True, max_length=50, verbose_name='Contractor Code'),
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='trade',
            field=models.CharField(blank=True, max_length=100, verbose_name='Trade'),
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='contract',
            field=models.CharField(blank=True, max_length=100, verbose_name='Contract'),
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='mandays',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Mandays'),
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='regular_manday_hr',
            field=models.CharField(blank=True, max_length=20, verbose_name='Regular Manday Hours'),
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='ot',
            field=models.CharField(blank=True, max_length=20, verbose_name='OT'),
        ),
        # Make shift, overstay, and status fields optional with defaults
        migrations.AlterField(
            model_name='attendancerecord',
            name='shift',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='attendancerecord',
            name='overstay',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='attendancerecord',
            name='status',
            field=models.CharField(choices=[('P', 'Present'), ('A', 'Absent'), ('PH', 'Public Holiday'), ('PD', 'Partial Day'), ('WO', 'Week Off'), ('-0.5', 'Half Day'), ('-1', 'Full Day Leave')], default='P', max_length=10),
        ),
    ]
