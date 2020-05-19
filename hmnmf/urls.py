from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'hmnmf$', views.hmnmf_api),
    re_path(r'insert_known_data$', views.insert_known_data_api),
    re_path(r'insert_predict_data$', views.insert_predict_data_api),
    re_path(r'search_gene$', views.search_gene),
    re_path(r'search_phenotype$', views.search_phenotype),
    re_path(r'search_genes$', views.search_genes),
    re_path(r'search_phenotypes$', views.search_phenotypes),
    re_path(r'add_gene$', views.add_gene),
    re_path(r'add_phenotype$', views.add_phenotype)
]
