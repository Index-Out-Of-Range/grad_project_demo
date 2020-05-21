from django.db import models


# Create your models here.
class Gene(models.Model):
    gene_name = models.CharField(max_length=16, primary_key=True)
    # gene_id = models.CharField(max_length=16)
    # gene_detail = models.CharField(max_length=1024)

    def __str__(self):
        return self.gene_name


class Phenotype(models.Model):
    phenotype_name = models.CharField(max_length=16, primary_key=True)
    # phenotype_id = models.CharField(max_length=16)
    # phenotype_detail = models.CharField(max_length=1024)

    def __str__(self):
        return self.phenotype_name


class Known_GP_Relation(models.Model):
    gene = models.ForeignKey('Gene', on_delete=models.CASCADE)
    phenotype = models.ForeignKey('Phenotype', on_delete=models.CASCADE)
    gp_known_relation = models.DecimalField(max_digits=10, decimal_places=6)


class Predict_GP_Relation(models.Model):
    gene = models.ForeignKey('Gene', on_delete=models.CASCADE)
    phenotype = models.ForeignKey('Phenotype', on_delete=models.CASCADE)
    gp_predict_relation = models.DecimalField(max_digits=10, decimal_places=6)


class Predict_Process(models.Model):
    process_key = models.CharField(max_length=64, primary_key=True)
    process = models.IntegerField()