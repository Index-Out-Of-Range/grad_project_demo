from django.db import models


# Create your models here.
class Gene(models.Model):
    gene_id = models.CharField(max_length=64, primary_key=True)
    gene_name = models.CharField(max_length=256)
    gene_detail = models.CharField(max_length=4096)

    def __str__(self):
        return self.gene_name


class Phenotype(models.Model):
    phenotype_id = models.CharField(max_length=64, primary_key=True)
    phenotype_name = models.CharField(max_length=256)
    phenotype_detail = models.CharField(max_length=4096)

    def __str__(self):
        return self.phenotype_name


class Known_GP_Relation(models.Model):
    gene = models.ForeignKey('Gene', on_delete=models.CASCADE)
    gene_name = models.CharField(max_length=256)
    phenotype = models.ForeignKey('Phenotype', on_delete=models.CASCADE)
    phenotype_name = models.CharField(max_length=256)
    gp_known_relation = models.DecimalField(max_digits=10, decimal_places=6)


class Predict_GP_Relation(models.Model):
    gene = models.ForeignKey('Gene', on_delete=models.CASCADE)
    gene_name = models.CharField(max_length=256)
    phenotype = models.ForeignKey('Phenotype', on_delete=models.CASCADE)
    phenotype_name = models.CharField(max_length=256)
    gp_predict_relation = models.DecimalField(max_digits=10, decimal_places=6)
