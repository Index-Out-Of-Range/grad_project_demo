import pymysql
import numpy


# 从已知关联表和预测关联表中搜索和gene_name关联的phenotype,并按照关联度从大到小的顺序返回
def search_gene_from_db(gene_name):
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='dipo123',
                                 db='grad_project', charset='utf8')
    cursor = connection.cursor()
    sql1 = '''select * from hmnmf_predict_gp_relation where gene_id=%s order by gp_predict_relation desc;''' % gene_name
    sql2 = '''select * from hmnmf_known_gp_relation where gp_known_relation=1 and gene_id=%s;''' % gene_name
    predict_results = []
    known_results = []
    try:
        cursor.execute(sql1)
        relations = cursor.fetchall()
        for relation in relations:
            gp_relation = float(relation[1])
            phenotype_name = int(relation[3])
            predict_results.append({'phenotype_name': phenotype_name, 'gp_relation': gp_relation})
        cursor.execute(sql2)
        relations = cursor.fetchall()
        for relation in relations:
            gp_relation = float(relation[1])
            phenotype_name = int(relation[3])
            known_results.append({'phenotype_name': phenotype_name, 'gp_relation': gp_relation})
    except Exception as e:
        print(str(e))
    connection.close()
    predict_results = delete_duplicate_node(1, known_results, predict_results)
    predict_results = normalization(predict_results)
    return known_results, predict_results


def search_phenotype_from_db(phenotype_name):
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='dipo123',
                                 db='grad_project', charset='utf8')
    cursor = connection.cursor()
    sql1 = '''select * from hmnmf_predict_gp_relation where phenotype_id=%s order by gp_predict_relation desc;''' % phenotype_name
    sql2 = '''select * from hmnmf_known_gp_relation where gp_known_relation=1 and phenotype_id=%s;''' % phenotype_name
    predict_results = []
    known_results = []
    try:
        cursor.execute(sql1)
        relations = cursor.fetchall()
        for relation in relations:
            gp_relation = float(relation[1])
            gene_name = int(relation[2])
            predict_results.append({'gene_name': gene_name, 'gp_relation': gp_relation})
        cursor.execute(sql2)
        relations = cursor.fetchall()
        for relation in relations:
            gp_relation = float(relation[1])
            gene_name = int(relation[2])
            known_results.append({'gene_name': gene_name, 'gp_relation': gp_relation})
    except Exception as e:
        print(str(e))
    connection.close()
    predict_results = delete_duplicate_node(2, known_results, predict_results)
    print(predict_results)
    predict_results = normalization(predict_results)
    print(predict_results)
    return known_results, predict_results


def delete_duplicate_node(kind, known_results, predict_results):
    # 如果known_results中存在和predict_results相同的值，把它从predict_results中去掉
    if kind == 1:
        key = 'phenotype_name'
    elif kind == 2:
        key = 'gene_name'
    for i in range(len(predict_results)-1, -1, -1):
        predict_result = predict_results[i]
        for j in range(len(known_results)):
            known_result = known_results[j]
            if predict_result[key] == known_result[key]:
                del predict_results[i]
                continue
    return predict_results


def normalization(results):
    relations = []
    for i in range(len(results)):
        relations.append(results[i]['gp_relation'])
    min_relation = numpy.min(relations)
    max_relation = numpy.max(relations)
    normalize_result = (relations-min_relation)/(max_relation - min_relation)
    for i in range(len(results)):
        results[i]['gp_relation'] = round(float(normalize_result[i]), 4)
    return results
