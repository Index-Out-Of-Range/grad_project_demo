import time

import pymysql
import scipy.io
import requests
from lxml import etree


def get_gene_list():
    pathway_path = r"../../HMNMF_Codes/2_useful_data/pathway/pathway.mat"
    pathway_data = scipy.io.loadmat(pathway_path)
    genes = pathway_data['gene_id']
    gene_list = []
    for gene in genes:
        gene_list.append(gene[0])
    # print(gene_list)
    return gene_list


def spider_info(gene_list):
    url = 'https://www.ncbi.nlm.nih.gov/gene/?term='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    }
    for gene in gene_list:
        try:
            gene_url = url + str(gene)
            gene_html = requests.get(gene_url, headers=headers)
            gene_html.encoding = 'utf-8'
            root = etree.HTML(gene_html.content)
            official_symbol = root.xpath('//*[@id="summaryDl"]/dd[1]/text()')
            official_full_name = root.xpath('//*[@id="summaryDl"]/dd[2]/text()')
            summary = root.xpath('//*[@id="summaryDl"]/dd[10]/text()')
            gene_dict = {
                'id': gene,
                'official_symbol': official_symbol,
                'official_full_name': official_full_name,
                'summary': summary
            }
            print(official_symbol)
            print(official_full_name)
            print(summary)
            print(gene_dict)
            with open('gene_info.txt', 'a') as f:
                f.write(str(gene_dict) + '\n')
            time.sleep(5)
        except:
            with open('gene_error.txt', 'a') as f:
                f.write(str(gene) + '\n')
            continue


def format_gene(kind):
    # gene_result_list = []

    db_arg = []
    with open('gene_info.txt', 'r') as f:
        for line in f.readlines():
            temp_dict = eval(line)

            summary = temp_dict['summary'][0] if temp_dict['summary'] else '-'
            index_ = summary.rfind('[')
            if index_ != -1:
                summary = summary[:index_].rstrip()
            # print(summary)
            # format_dict = {
            #     'id': str(temp_dict['id']),
            #     'official_full_name': temp_dict['official_full_name'][0],
            #     'summary': summary
            # }
            # print((str(temp_dict['id']),temp_dict['official_full_name'][0],temp_dict['summary'][0] if temp_dict['summary'] else '-'))
            db_arg.append((str(temp_dict['id']), temp_dict['official_full_name'][0], summary))
            # gene_result_list.append(format_dict)
    if kind == 1:
        connection = pymysql.connect(host='localhost', port=3306, user='root', password='dipo123', db='grad_project', charset='utf8')
        cursor = connection.cursor()
        sql = '''insert into hmnmf_gene(gene_id, gene_name, gene_detail) values(%s, %s, %s)'''
        try:
            cursor.executemany(sql, db_arg)
            connection.commit()
        except:
            connection.rollback()

        connection.close()

    return db_arg


if __name__ == '__main__':
    # step 1
    # gene_list = get_gene_list()
    # spider_info(gene_list)

    # step 2
    format_gene(kind=1)
