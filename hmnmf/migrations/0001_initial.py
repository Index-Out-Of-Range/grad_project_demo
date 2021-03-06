# Generated by Django 3.0.1 on 2020-05-31 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('gene_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('gene_name', models.CharField(max_length=256)),
                ('gene_detail', models.CharField(max_length=4096)),
            ],
        ),
        migrations.CreateModel(
            name='Phenotype',
            fields=[
                ('phenotype_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('phenotype_name', models.CharField(max_length=256)),
                ('phenotype_detail', models.CharField(max_length=4096)),
            ],
        ),
        migrations.CreateModel(
            name='Predict_GP_Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gene_name', models.CharField(max_length=256)),
                ('phenotype_name', models.CharField(max_length=256)),
                ('gp_predict_relation', models.DecimalField(decimal_places=6, max_digits=10)),
                ('gene', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hmnmf.Gene')),
                ('phenotype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hmnmf.Phenotype')),
            ],
        ),
        migrations.CreateModel(
            name='Known_GP_Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gene_name', models.CharField(max_length=256)),
                ('phenotype_name', models.CharField(max_length=256)),
                ('gp_known_relation', models.DecimalField(decimal_places=6, max_digits=10)),
                ('gene', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hmnmf.Gene')),
                ('phenotype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hmnmf.Phenotype')),
            ],
        ),
    ]
