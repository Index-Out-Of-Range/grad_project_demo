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
    if predict_results:
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
    if predict_results:
        predict_results = delete_duplicate_node(2, known_results, predict_results)
        predict_results = normalization(predict_results)
    return known_results, predict_results


def delete_duplicate_node(kind, known_results, predict_results):
    # 如果known_results中存在和predict_results相同的值，把它从predict_results中去掉
    if kind == 1:
        key = 'phenotype_name'
    elif kind == 2:
        key = 'gene_name'
    for i in range(len(predict_results) - 1, -1, -1):
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
    normalize_result = (relations - min_relation) / (max_relation - min_relation)
    for i in range(len(results)):
        results[i]['gp_relation'] = round(float(normalize_result[i]), 4)
    return results


def multi_gp_relations(gene_nodes, phenotype_nodes, type):
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='dipo123',
                                 db='grad_project', charset='utf8')
    cursor = connection.cursor()
    gp_relation = {}
    if type == 1:
        print(gene_nodes, phenotype_nodes)
        for gene in gene_nodes:
            gp_relation[gene] = {}
            gene_result = {}
            sql1 = '''select * from hmnmf_known_gp_relation where gene_id=%s;''' % gene
            sql2 = '''select * from hmnmf_predict_gp_relation where gene_id=%s order by gp_predict_relation desc;''' % gene
            cursor.execute(sql1)
            result1 = cursor.fetchall()
            cursor.execute(sql2)
            result2 = cursor.fetchall()
            result_dict1 = {}
            result_dict2 = {}
            result_list = []
            for result in result1:
                result_dict1[result[3]] = int(result[1])
            for result in result2:
                result_list.append({'phenotype_id': result[3], 'gp_relation': float(result[1])})
            result_list = normalization(result_list)
            for result in result_list:
                result_dict2[result['phenotype_id']] = result['gp_relation']
            print('result_dict1: ', result_dict1)
            print('result_dict2: ', result_dict2)
            for phenotype_node in phenotype_nodes:
                if result_dict1[str(phenotype_node)] == 1:
                    gene_result[phenotype_node] = {'type': 'known', 'relation': 1}
                else:
                    gene_result[phenotype_node] = {'type': 'predict', 'relation': result_dict2[str(phenotype_node)]}
            gp_relation[gene] = gene_result
    elif type == 2:
        print(gene_nodes, phenotype_nodes)
        for phenotype in phenotype_nodes:
            gp_relation[phenotype] = {}
            phenotype_result = {}
            sql1 = '''select * from hmnmf_known_gp_relation where phenotype_id=%s;''' % phenotype
            sql2 = '''select * from hmnmf_predict_gp_relation where phenotype_id=%s order by gp_predict_relation desc;''' % phenotype
            cursor.execute(sql1)
            result1 = cursor.fetchall()
            cursor.execute(sql2)
            result2 = cursor.fetchall()
            result_dict1 = {}
            result_dict2 = {}
            result_list = []
            for result in result1:
                result_dict1[result[2]] = int(result[1])
            for result in result2:
                result_list.append({'gene_id': result[2], 'gp_relation': float(result[1])})
            result_list = normalization(result_list)
            for result in result_list:
                result_dict2[result['gene_id']] = result['gp_relation']
            print('result_dict1: ', result_dict1)
            print('result_dict2: ', result_dict2)
            for gene_node in gene_nodes:
                if result_dict1[str(gene_node)] == 1:
                    phenotype_result[gene_node] = {'type': 'known', 'relation': 1}
                else:
                    phenotype_result[gene_node] = {'type': 'predict', 'relation': result_dict2[str(gene_node)]}
            gp_relation[phenotype] = phenotype_result
    connection.close()
    print('gp_relation: ', gp_relation)
    return gp_relation


def search_new_gp(gene_nodes, phenotype_nodes, add_type):
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='dipo123', db='grad_project', charset='utf8')
    cursor = connection.cursor()
    new_gp_relation = []
    result_dict1 = {}
    result_dict2 = {}
    if add_type == '1':
        sql1 = '''select * from hmnmf_known_gp_relation where gene_id=%s;''' % gene_nodes[0]
        sql2 = '''select * from hmnmf_predict_gp_relation where gene_id=%s;''' % gene_nodes[0]
        cursor.execute(sql1)
        result1 = cursor.fetchall()
        cursor.execute(sql2)
        result2 = cursor.fetchall()
        print(result1)
        print(result2)
        if len(result1) == 0 and len(result2) == 0:
            return []
        for result in result1:
            result_dict1[result[3]] = float(result[1])
        result_list = []
        for result in result2:
            result_list.append({'phenotype_id': result[3], 'gp_relation': float(result[1])})
        result_list = normalization(result_list)
        for result in result_list:
            result_dict2[result['phenotype_id']] = result['gp_relation']
        print(result_dict1)
        print(result_dict2)
        for phenotype in phenotype_nodes:
            if result_dict1[phenotype] == 1:
                new_gp_relation.append({'gene': gene_nodes[0], 'phenotype': phenotype, 'gp_relation': 1, 'type': 'known'})
            else:
                new_gp_relation.append({'gene': gene_nodes[0], 'phenotype': phenotype, 'gp_relation': result_dict2[phenotype], 'type': 'predict'})
    elif add_type == '2':
        sql1 = '''select * from hmnmf_known_gp_relation where phenotype_id=%s;''' % phenotype_nodes[0]
        sql2 = '''select * from hmnmf_predict_gp_relation where phenotype_id=%s;''' % phenotype_nodes[0]
        cursor.execute(sql1)
        result1 = cursor.fetchall()
        cursor.execute(sql2)
        result2 = cursor.fetchall()
        print(result1)
        print(result2)
        if len(result1) == 0 and len(result2) == 0:
            return []
        for result in result1:
            result_dict1[result[2]] = float(result[1])
        result_list = []
        for result in result2:
            result_list.append({'gene_id': result[2], 'gp_relation': float(result[1])})
        result_list = normalization(result_list)
        for result in result_list:
            result_dict2[result['gene_id']] = result['gp_relation']
        print(result_dict1)
        print(result_dict2)
        for gene in gene_nodes:
            if result_dict1[gene] == 1:
                new_gp_relation.append({'gene': gene, 'phenotype': phenotype_nodes[0], 'gp_relation': 1, 'type': 'known'})
            else:
                new_gp_relation.append({'gene': gene, 'phenotype': phenotype_nodes[0], 'gp_relation': result_dict2[gene], 'type': 'predict'})

    connection.close()
    print(new_gp_relation)
    return new_gp_relation
