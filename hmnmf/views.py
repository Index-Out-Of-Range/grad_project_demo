import os

from celery.result import AsyncResult
from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core import serializers

from algorithm_demo import settings
from django.core.cache import cache
from algorithm_demo.celery import app
import requests
import json
import math

from .models import Gene, Phenotype
from hmnmf import tasks
from .search_db import search_gene_from_db, search_phenotype_from_db, multi_gp_relations, search_new_gp


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
        'hier_del': 0,
        'user_file_path': '',
        'process_key': ''
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


@require_http_methods(['GET'])
def search_genes(request):
    response = {}
    try:
        gene_list = request.GET.getlist('gene_list')
        print('gene_list: ', gene_list)
        response['results'] = []
        gene_nodes = []
        phenotype_nodes = []
        for gene in gene_list:
            known_results, predict_results = search_gene_from_db(int(gene))
            response['results'].append({
                'target': gene, 'known_results': known_results, 'predict_results': predict_results
            })
            if known_results and predict_results:
                gene_nodes.append(int(gene))
                if len(known_results) > 10:
                    known_results = known_results[:10]
                if len(predict_results) > 10:
                    predict_results = predict_results[:10]
                for result in known_results:
                    phenotype_nodes.append(result['phenotype_name'])
                for result in predict_results:
                    phenotype_nodes.append(result['phenotype_name'])
        phenotype_nodes = list(set(phenotype_nodes))
        response['msg'] = 'success'
        response['error_num'] = 0
        response['multi_gp_relations'] = multi_gp_relations(gene_nodes, phenotype_nodes, 1)
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(['GET'])
def search_phenotypes(request):
    response = {}
    try:
        phenotype_list = request.GET.getlist('phenotype_list')
        print('phenotype_list: ', phenotype_list)
        response['results'] = []
        gene_nodes = []
        phenotype_nodes = []
        for phenotype in phenotype_list:
            known_results, predict_results = search_phenotype_from_db(int(phenotype))
            print(phenotype)
            print(known_results)
            print(predict_results)
            response['results'].append({
                'target': phenotype, 'known_results': known_results, 'predict_results': predict_results
            })
            if known_results and predict_results:
                phenotype_nodes.append(int(phenotype))
                if len(known_results) > 10:
                    known_results = known_results[:10]
                if len(predict_results) > 10:
                    predict_results = predict_results[:10]
                for result in known_results:
                    gene_nodes.append(result['gene_name'])
                for result in predict_results:
                    gene_nodes.append(result['gene_name'])
        gene_nodes = list(set(gene_nodes))
        response['msg'] = 'success'
        response['error_num'] = 0
        response['multi_gp_relations'] = multi_gp_relations(gene_nodes, phenotype_nodes, 2)
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(['GET'])
def add_gene(request):
    response = {}
    try:
        gene_nodes = request.GET.getlist('gene_nodes')
        phenotype_nodes = request.GET.getlist('phenotype_nodes')
        add_type = request.GET.get('add_type')
        print('add_type: ', add_type)
        print('gene_nodes: ', gene_nodes)
        print('phenotype_nodes: ', phenotype_nodes)
        new_gp_relation = search_new_gp(gene_nodes, phenotype_nodes, add_type)
        response['msg'] = 'success'
        response['error_num'] = 0
        response['new_gp_relation'] = new_gp_relation
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(['GET'])
def add_phenotype(request):
    response = {}
    try:
        gene_nodes = request.GET.getlist('gene_nodes')
        phenotype_nodes = request.GET.getlist('phenotype_nodes')
        add_type = request.GET.get('add_type')
        print('add_type: ', add_type)
        print('gene_nodes: ', gene_nodes)
        print('phenotype_nodes: ', phenotype_nodes)
        new_gp_relation = search_new_gp(gene_nodes, phenotype_nodes, add_type)
        response['msg'] = 'success'
        response['error_num'] = 0
        response['new_gp_relation'] = new_gp_relation
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def upload_mat_file(request):
    response = {}
    try:
        mat_file = request.FILES.get('file', None)
        if not mat_file:
            response['msg'] = 'no file upload'
            response['error_num'] = 1
            return JsonResponse(response)
        fileName = mat_file.name
        filePath = os.path.join(settings.UPLOAD_FILE_ROOT, fileName).replace('\\', '/')
        print('mat_file: ', fileName)
        print('filepath = [%s]' % filePath)
        print(mat_file.multiple_chunks())
        with open(filePath, "wb") as f:
            if mat_file.multiple_chunks():
                for content in mat_file.chunks():
                    f.write(content)
            else:
                data = mat_file.read()
                f.write(data)
        response['msg'] = 'success'
        response['error_num'] = 0
        response['file_path'] = filePath
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(['GET'])
def predict_file(request):
    response = {}
    try:
        upload_file_path = request.GET.get('upload_file_path')
        process_key = request.GET.get('process_key')
        print('file_path: ', upload_file_path)
        print('process_key: ', process_key)
        cache.set(process_key, 0, 30*60)
        # return JsonResponse(response)
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
            'hier_del': 0,
            'user_file_path': upload_file_path,
            'process_key': process_key,
        }
        res = tasks.excute_hmnmf.delay(parameter_cell)
        my_async = AsyncResult(id=res.id, app=app)
        while my_async.successful():
            result = my_async.get()
            print('111-my_result', result)
        # while not my_async.ready():
        #     print("任务仍在进行中: ", settings.PREDICT_DICT[process_key])
        # result = my_async.get()
        # print(result)
        # return HttpResponse('HMNMF algorithm runs successfully!!!')
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(['GET'])
def predict_process(request):
    response = {}
    try:
        process_key = request.GET.get('process_key')
        print('process_key: ', process_key)
        print('222: ', cache.get(process_key))
        response['process'] = cache.get(process_key)
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(['GET'])
def get_result_file_path(request):
    response = {}
    try:
        process_key = request.GET.get('process_key')
        print('process_key: ', process_key)
        result_file_path = process_key+'_result_file_path'
        print(result_file_path)
        print('222: ', cache.get(result_file_path))
        response['result_file_path'] = cache.get(result_file_path)
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def download_file(request):
    try:
        file_path = request.POST.get('file_path')
        print('file_path: ', file_path)
        # with open(file_path, 'rb') as f:
        #     response = FileResponse(f)
        #     response['content_type'] = "application/octet-stream"
        #     response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        #     return response
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
        # def file_iterator(file_name, chunk_size=512):
        #     with open(file_name) as f:
        #         while True:
        #             c = f.read(chunk_size)
        #             if c:
        #                 yield c
        #             else:
        #                 break
        #
        # response = StreamingHttpResponse(file_iterator(file_path))
        # response['Content-Type'] = 'application/octet-stream'
        # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_path)
        # response['msg'] = 'success'
        # response['error_num'] = 0
    except Exception as e:
        response = {'msg': str(e), 'error_num': 1}
        return JsonResponse(response)
    # return response
