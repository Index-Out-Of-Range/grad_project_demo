from celery.result import AsyncResult
from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from algorithm_demo.celery import app
import requests
import json
import math

from .models import Gene, Phenotype
from hmnmf import tasks
from .search_db import search_gene_from_db, search_phenotype_from_db


def insert_known_data_api(requests):
    res = tasks.insert_known_data.delay()
    async = AsyncResult(id=res.id, app=app)
    while async.successful():
        result = async.get()
        print(result)
    return HttpResponse('Insert known data successfully!!!')


def insert_predict_data_api(requests):
    res = tasks.insert_predict_data.delay()
    async = AsyncResult(id=res.id, app=app)
    while async.successful():
        result = async.get()
        print(result)
    return HttpResponse('Insert predict data successfully!!!')


def hmnmf_api(requests):
    parameter_cell = {
        'method_dir': 'HMNMF_Codes/L21_CMNMF/',
        'dataset': 'pathway',
        'partition': 0,
        'alpha_set': math.pow(10, 3),
        'beta_set': 0 * math.pow(10, 3),
        'gamma_set': math.pow(3, 4),
        'miu_set': math.pow(10, -2),
        'rou_set': 1.2,
        'max_ites': 100,
        'cv_criteria': 'AUC100',
        'file_num': 1,
        'feature_num': 50,
        'hier_del': 0
    }
    res = tasks.excute_hmnmf.delay(parameter_cell)
    async = AsyncResult(id=res.id, app=app)
    while async.successful():
        result = async.get()
        print(result)
    # while not async.ready():
    #     print("任务仍在进行中")
    # result = async.get()
    # print(result)
    return HttpResponse('HMNMF algorithm runs successfully!!!')


@require_http_methods(['GET'])
def search_gene(request):
    response = {}
    try:
        gene_name = request.GET.get('gene_name')
        # n = int(request.GET.get('n', 10))
        known_results, predict_results = search_gene_from_db(gene_name)
        response['msg'] = 'success'
        response['error_num'] = 0
        response['known_results'] = known_results
        response['predict_results'] = predict_results
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(['GET'])
def search_phenotype(request):
    response = {}
    try:
        phenotype_name = request.GET.get('phenotype_name')
        # n = int(request.GET.get('n', 10))
        known_results, predict_results = search_phenotype_from_db(phenotype_name)
        response['msg'] = 'success'
        response['error_num'] = 0
        response['known_results'] = known_results
        response['predict_results'] = predict_results
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

