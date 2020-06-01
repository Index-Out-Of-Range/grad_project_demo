import re
import scipy.io
import pymysql


def get_phenotype_list():
    pathway_path = r"../../HMNMF_Codes/2_useful_data/pathway/pathway.mat"
    pathway_data = scipy.io.loadmat(pathway_path)
    phenotypes = pathway_data['first_and_second_idx']
    phenotype_list = []
    for phenotype in phenotypes:
        phenotype_list.append(phenotype[0])
    print(phenotype_list)
    return phenotype_list


def get_result_list():
    result_list = []
    with open('hp.obo.txt', 'r', encoding='utf8') as f:
        list1 = []
        p1 = re.compile(r'["](.*)["]', re.S)
        while True:
            cont = f.readline().replace('\n', '')
            if not cont:  # 如果为空行,则表示取完一次数据,可以执行操作;
                if not list1:  # 如果列表也为空,则表示数据读完了,结束循环
                    break
                print(list1)
                # id_ = re.search(r"\'id:(.*?)\'\,", str(list1))
                # name_ = re.search(r"\'name:(.*?)\'\,", str(list1))
                # def_ = re.search(r"\'def:(.*?)\'\,", str(list1))
                # if id_ and name_:
                #     print(id_[0].replace("'", '').replace(",", "").split(':')[2], name_[0].replace("'", '').replace(",", '').split(':')[1])
                #     print(def_[0] if def_ else '-')
                #     result_list.append({
                #       'id': id_[0].replace("'", '').replace(",", "").split(':')[2],
                #       'name': name_[0].replace("'", '').replace(",", '').split(':')[1],
                #       'def': re.search(p1, def_[0]) if def_ else '-'
                #     })
                result_list.append(list1)
                list1 = []
            else:
                list1.append(cont)
    return result_list


def get_error_phenotype(phenotype_list, result_list):
    count = 0
    for phenotype in phenotype_list:
        flag = False
        for result in result_list[1:]:
            if phenotype == int(result[1].split(':')[-1]):
                count += 1
                flag = True
                with open('temp_phenotype_info.txt', 'a', encoding='utf-8') as f:
                    f.write(str(result) + '\n')
                break
        if not flag:
            with open('phenotype_error.txt', 'a') as f:
                f.write(str(phenotype) + '\n')
    print(count)


def format_result():
    result = []
    with open('temp_phenotype_info.txt', 'r') as f:
        for line in f.readlines():
            temp_dict = {}
            temp_list = eval(line)
            temp_dict['id'] = temp_list[1][7:]
            temp_dict['name'] = temp_list[2][6:]
            flag = False
            for t_l in temp_list[3:]:
                if 'def' in t_l:
                    flag = True
                    index_ = t_l.rfind('[')
                    if index_ != -1:
                        t_l = t_l[6:index_-2]
                    temp_dict['def'] = t_l
                    break
            if not flag:
                temp_dict['def'] = '-'
            # print(temp_dict)
            result.append(temp_dict)
        with open('phenotype_info.txt', 'a') as f:
            for r in result:
                f.write(str(r) + '\n')


def phenotype_to_db(kind):
    db_arg = []
    with open('phenotype_info.txt', 'r') as f:
        for line in f.readlines():
            temp_dict = eval(line)
            print(str(int(temp_dict['id'])), temp_dict['name'], temp_dict['def'])
            db_arg.append((str(int(temp_dict['id'])), temp_dict['name'], temp_dict['def']))
    if kind == 1:
        connection = pymysql.connect(host='localhost', port=3306, user='root', password='dipo123', db='grad_project', charset='utf8')
        cursor = connection.cursor()
        sql = '''insert into hmnmf_phenotype(phenotype_id, phenotype_name, phenotype_detail) values(%s, %s, %s)'''
        try:
            cursor.executemany(sql, db_arg)
            connection.commit()
        except:
            connection.rollback()

        connection.close()
    return db_arg


if __name__ == '__main__':
    # 1st step
    # phenotype_list = get_phenotype_list()
    # result_list = get_result_list()
    # get_error_phenotype(phenotype_list, result_list)

    # 2nd step
    # format_result()

    # 3rd strp
    phenotype_to_db(kind=1)
