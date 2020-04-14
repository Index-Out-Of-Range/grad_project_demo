from __future__ import absolute_import, unicode_literals
from celery import shared_task
from HMNMF_Codes.L21_CMNMF.L21_CMNMF import l21_cmnmf
from HMNMF_Codes.L21_CMNMF.result_to_db import data_to_db


@shared_task
def insert_known_data():
    res = (data_to_db(0), data_to_db(1))
    return res


@shared_task
def insert_predict_data():
    res = data_to_db(2)
    return res


@shared_task
def excute_hmnmf(parameter_cell):
    res = l21_cmnmf(parameter_cell)
    return res
