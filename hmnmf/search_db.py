import pymysql
import numpy


# 判断传入的参数是ID还是Name, ID返回True, 否则返回False
def judge_arg(parameter):
    try:
        x = int(parameter)
        return isinstance(x, int)
    except ValueError:
        return False


def search_target_info(kind, search_target):
    search_target_info = {}
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='dipo123', db='grad_project', charset='utf8')
    cursor = connection.cursor()
    if kind == 1:
        if judge_arg(search_target):
            sql = '''select * from hmnmf_gene where gene_id=%s;''' % search_target
        else:
            sql = '''select * from hmnmf_gene where gene_name='%s';''' % search_target
    elif kind == 2:
        if judge_arg(search_target):
            sql = '''select * from hmnmf_phenotype where phenotype_id=%s;''' % search_target
        else:
            sql = '''select * from hmnmf_phenotype where phenotype_name='%s';''' % search_target
    try:
        cursor.execute(sql)
        relation = cursor.fetchone()
        search_target_info['id'] = relation[0]
        search_target_info['name'] = relation[1]
        search_target_info['detail'] = relation[2]
    except Exception as e:
        print(str(e))
        return {}
    connection.close()
    return search_target_info


# 从已知关联表和预测关联表中搜索和gene_name关联的phenotype,并按照关联度从大到小的顺序返回
def search_gene_from_db(gene):
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='dipo123', db='grad_project', charset='utf8')
    cursor = connection.cursor()
    if judge_arg(gene):
        sql1 = '''select * from hmnmf_predict_gp_relation where gene_id=%s order by gp_predict_relation desc;''' % gene
        sql2 = '''select * from hmnmf_known_gp_relation where gp_known_relation=1 and gene_id=%s;''' % gene
    else:
        sql1 = '''select * from hmnmf_predict_gp_relation where gene_name='%s' order by gp_predict_relation desc;''' % gene
        sql2 = '''select * from hmnmf_known_gp_relation where gp_known_relation=1 and gene_name='%s';''' % gene
    predict_results = []
    known_results = []
    try:
        cursor.execute(sql1)
        relations = cursor.fetchall()
        for relation in relations:
            gp_relation = float(relation[3])
            phenotype_name = relation[2]
            phenotype_id = relation[5]
            predict_results.append({'phenotype_id': phenotype_id, 'phenotype_name': phenotype_name, 'gp_relation': gp_relation})
        cursor.execute(sql2)
        relations = cursor.fetchall()
        for relation in relations:
            gp_relation = float(relation[3])
            phenotype_name = relation[2]
            phenotype_id = relation[5]
            known_results.append({'phenotype_id': phenotype_id, 'phenotype_name': phenotype_name, 'gp_relation': gp_relation})
    except Exception as e:
        print(str(e))
    connection.close()
    if predict_results:
        predict_results = delete_duplicate_node(1, known_results, predict_results)
        predict_results = normalization(predict_results)
    return known_results, predict_results


def search_phenotype_from_db(phenotype):
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='dipo123', db='grad_project', charset='utf8')
    cursor = connection.cursor()
    if judge_arg(phenotype):
        sql1 = '''select * from hmnmf_predict_gp_relation where phenotype_id=%s order by gp_predict_relation desc;''' % phenotype
        sql2 = '''select * from hmnmf_known_gp_relation where gp_known_relation=1 and phenotype_id=%s;''' % phenotype
    else:
        sql1 = '''select * from hmnmf_predict_gp_relation where phenotype_name='%s' order by gp_predict_relation desc;''' % phenotype
        sql2 = '''select * from hmnmf_known_gp_relation where gp_known_relation=1 and phenotype_name='%s';''' % phenotype
    predict_results = []
    known_results = []
    try:
        cursor.execute(sql1)
        relations = cursor.fetchall()
        for relation in relations:
            gp_relation = float(relation[3])
            gene_name = relation[1]
            gene_id = relation[4]
            predict_results.append({'gene_id': gene_id, 'gene_name': gene_name, 'gp_relation': gp_relation})
        cursor.execute(sql2)
        relations = cursor.fetchall()
        for relation in relations:
            gp_relation = float(relation[3])
            gene_name = relation[1]
            gene_id = relation[4]
            known_results.append({'gene_id': gene_id, 'gene_name': gene_name, 'gp_relation': gp_relation})
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
        key = 'phenotype_id'
    elif kind == 2:
        key = 'gene_id'
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
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='dipo123', db='grad_project', charset='utf8')
    cursor = connection.cursor()
    gp_relation = {}
    if type == 1:
        print(gene_nodes, phenotype_nodes)
        for gene in gene_nodes:
            gp_relation[gene] = {}
            gene_result = {}
            if judge_arg(gene):
                sql1 = '''select * from hmnmf_known_gp_relation where gene_id=%s;''' % gene
                sql2 = '''select * from hmnmf_predict_gp_relation where gene_id=%s order by gp_predict_relation desc;''' % gene
            else:
                sql1 = '''select * from hmnmf_known_gp_relation where gene_name='%s';''' % gene
                sql2 = '''select * from hmnmf_predict_gp_relation where gene_name='%s' order by gp_predict_relation desc;''' % gene
            cursor.execute(sql1)
            result1 = cursor.fetchall()
            cursor.execute(sql2)
            result2 = cursor.fetchall()
            result_dict1 = {}
            result_dict2 = {}
            result_list = []
            for result in result1:
                # print(result)
                result_dict1[result[5]] = [int(result[3]), result[2]]
            for result in result2:
                # print(result)
                result_list.append({'phenotype_id': result[5], 'phenotype_name': result[2], 'gp_relation': float(result[3])})
            result_list = normalization(result_list)
            for result in result_list:
                result_dict2[result['phenotype_id']] = [result['gp_relation'], result['phenotype_name']]
            print('result_dict1: ', result_dict1)
            print('result_dict2: ', result_dict2)
            for phenotype_node in phenotype_nodes:
                if result_dict1[str(phenotype_node)][0] == 1:
                    gene_result[phenotype_node] = {'name': result_dict1[str(phenotype_node)][1], 'type': 'known', 'relation': 1}
                else:
                    gene_result[phenotype_node] = {'name': result_dict2[str(phenotype_node)][1], 'type': 'predict', 'relation': result_dict2[str(phenotype_node)][0]}
            gp_relation[gene] = gene_result
    elif type == 2:
        print(gene_nodes, phenotype_nodes)
        for phenotype in phenotype_nodes:
            gp_relation[phenotype] = {}
            phenotype_result = {}
            if judge_arg(phenotype):
                sql1 = '''select * from hmnmf_known_gp_relation where phenotype_id=%s;''' % phenotype
                sql2 = '''select * from hmnmf_predict_gp_relation where phenotype_id=%s order by gp_predict_relation desc;''' % phenotype
            else:
                sql1 = '''select * from hmnmf_known_gp_relation where phenotype_name='%s';''' % phenotype
                sql2 = '''select * from hmnmf_predict_gp_relation where phenotype_name='%s' order by gp_predict_relation desc;''' % phenotype
            cursor.execute(sql1)
            result1 = cursor.fetchall()
            cursor.execute(sql2)
            result2 = cursor.fetchall()
            result_dict1 = {}
            result_dict2 = {}
            result_list = []
            for result in result1:
                result_dict1[result[4]] = [int(result[3]), result[1]]
            for result in result2:
                result_list.append({'gene_id': result[4], 'gene_name': result[1], 'gp_relation': float(result[3])})
            result_list = normalization(result_list)
            for result in result_list:
                result_dict2[result['gene_id']] = [result['gp_relation'], result['gene_name']]
            print('result_dict1: ', result_dict1)
            print('result_dict2: ', result_dict2)
            for gene_node in gene_nodes:
                if result_dict1[str(gene_node)][0] == 1:
                    phenotype_result[gene_node] = {'name': result_dict1[str(gene_node)][1], 'type': 'known', 'relation': 1}
                else:
                    phenotype_result[gene_node] = {'name': result_dict2[str(gene_node)][1], 'type': 'predict', 'relation': result_dict2[str(gene_node)][0]}
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
        if(judge_arg(gene_nodes[0])):
            sql1 = '''select * from hmnmf_known_gp_relation where gene_id=%s;''' % gene_nodes[0]
            sql2 = '''select * from hmnmf_predict_gp_relation where gene_id=%s;''' % gene_nodes[0]
        else:
            sql1 = '''select * from hmnmf_known_gp_relation where gene_name='%s';''' % gene_nodes[0]
            sql2 = '''select * from hmnmf_predict_gp_relation where gene_name='%s';''' % gene_nodes[0]
        cursor.execute(sql1)
        result1 = cursor.fetchall()
        cursor.execute(sql2)
        result2 = cursor.fetchall()
        print(result1)
        print(result2)
        if len(result1) == 0 and len(result2) == 0:
            return []
        for result in result1:
            result_dict1[result[5]] = [int(result[3]), result[2]]
        result_list = []
        for result in result2:
            result_list.append({'phenotype_id': result[5], 'phenotype_name': result[2], 'gp_relation': float(result[3])})
        result_list = normalization(result_list)
        for result in result_list:
            result_dict2[result['phenotype_id']] = [result['gp_relation'], result['phenotype_name']]
        print(result_dict1)
        print(result_dict2)
        for phenotype in phenotype_nodes:
            if result_dict1[str(phenotype)][0] == 1:
                new_gp_relation.append({'gene': gene_nodes[0], 'phenotype': phenotype, 'name': result_dict1[str(phenotype)][1], 'gp_relation': 1, 'type': 'known'})
            else:
                new_gp_relation.append({'gene': gene_nodes[0], 'phenotype': phenotype, 'name': result_dict2[str(phenotype)][1], 'gp_relation': result_dict2[str(phenotype)][0], 'type': 'predict'})
    elif add_type == '2':
        if judge_arg(phenotype_nodes[0]):
            sql1 = '''select * from hmnmf_known_gp_relation where phenotype_id=%s;''' % phenotype_nodes[0]
            sql2 = '''select * from hmnmf_predict_gp_relation where phenotype_id=%s;''' % phenotype_nodes[0]
        else:
            sql1 = '''select * from hmnmf_known_gp_relation where phenotype_name='%s';''' % phenotype_nodes[0]
            sql2 = '''select * from hmnmf_predict_gp_relation where phenotype_name='%s';''' % phenotype_nodes[0]
        cursor.execute(sql1)
        result1 = cursor.fetchall()
        cursor.execute(sql2)
        result2 = cursor.fetchall()
        print(result1)
        print(result2)
        if len(result1) == 0 and len(result2) == 0:
            return []
        for result in result1:
            result_dict1[result[4]] = [int(result[3]), result[1]]
        result_list = []
        for result in result2:
            result_list.append({'gene_id': result[4], 'gene_name': result[1], 'gp_relation': float(result[3])})
        result_list = normalization(result_list)
        for result in result_list:
            result_dict2[result['gene_id']] = [result['gp_relation'], result['gene_name']]
        print(result_dict1)
        print(result_dict2)
        for gene in gene_nodes:
            if result_dict1[str(gene)][0] == 1:
                new_gp_relation.append({'gene': gene, 'name': result_dict1[str(gene)][1], 'phenotype': phenotype_nodes[0], 'gp_relation': 1, 'type': 'known'})
            else:
                new_gp_relation.append({'gene': gene, 'name': result_dict2[str(gene)][1], 'phenotype': phenotype_nodes[0], 'gp_relation': result_dict2[str(gene)][0], 'type': 'predict'})

    connection.close()
    print(new_gp_relation)
    return new_gp_relation
