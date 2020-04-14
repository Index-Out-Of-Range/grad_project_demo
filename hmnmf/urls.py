from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r'hmnmf$', views.hmnmf_api),
    re_path(r'insert_known_data$', views.insert_known_data_api),
    re_path(r'insert_predict_data$', views.insert_predict_data_api),
    re_path(r'search_gene$', views.search_gene),
    re_path(r'search_phenotype$', views.search_phenotype)
]