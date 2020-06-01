module.exports = {
  message: {
    language: '选择语言',
    system_name: 'BIAPMC',
    zh: '中文',
    en: '英文',
    search_btn: '搜索',
    home: {
      version: '版本',
      login: '登录',
      register: '注册',
      menu: {
        menu1: '基因-表型',
        menu2: '药物-药物',
        menu3: '下载',
        menu4: '帮助',
        menu5: '管理中心'
      },
      input_tip: '请输入疾病 / 基因',
      search_example: '查询示例',
      button: '快速查询',
      down_menu: {
        reference: '参考文献',
        contributor: '贡献者',
        statistics: '数据集',
        data_source: '数据源',
        faq: '常见问题',
        api: '接口'
      }
    },
    search: {
      search: '查询',
      predict: '预测',
      upload: '上传',
      menu: {
        menu1: '单个基因查询',
        menu2: '单个表型查询',
        menu3: '组合基因查询',
        menu4: '组合表型查询',
        menu5: '上传文件预测'
      },
      title: {
        title1: '通过Name / ID查询基因',
        title2: '通过Name / ID查询表型',
        title3: '上传文件进行预测'
      },
      search_example: '查询示例',
      tip: {
        tip1: '请输入ID / Name',
        tip2: '请输入ID / Name, 每行一个.'
      },
      subtitle: {
        gene: '基因 ID / Name',
        phenotype: '表型 ID / Name'
      },
      upload_tip: {
        tip1: '将文件拖到此处，或者',
        tip2: '点击上传',
        tip3: '请上传.mat文件'
      }
    },
    search_result: {
      search_result: '查询结果',
      detail: '详情',
      known_relation: '已知关联',
      predict_relation: '预测关联',
      visulaize: '可视化',
      download: {
        download: '下载结果',
        download_current: '下载当前结果',
        download_all: '下载所有结果'
      },
      table: {
        index: '序号',
        relation: '关联',
        option: '操作',
        detail: '简介'
      },
      delete: '删除',
      goto: '跳转',
      tip: {
        tip1: '查询目标',
        tip2: '不在数据库中!',
        tip3: '返回'
      }
    },
    visulization: {
      visulization_result: '可视化结果',
      predict_result: '预测结果',
      search_tips: {
        add_gene: '通过ID / Name添加基因',
        add_phenotype: '通过ID / Name添加表型',
        remove_gene: '通过ID / Name删除基因',
        remove_phenotype: '通过ID / Name删除表型'
      },
      buttons: {
        add_gene: '添加基因',
        add_phenotype: '添加表型',
        remove_gene: '删除基因',
        remove_phenotype: '删除表型'
      },
      sliders: {
        known_nodes: '已知节点',
        predict_nodes: '预测节点'
      }
    },
    message_tip: {
      not_null_tip: '输入不能为空',
      search_gene_fail_tip: '查询基因失败，请重试',
      search_phenotype_fail_tip: '查询表型失败，请重试',
      delete_info: {
        confirm_info: '无法撤回！确定删除？',
        ok: '确定',
        cancel: '取消',
        success_info: '删除成功',
        cancel_info: '取消删除'
      },
      error_tip: 'Error!',
      gene_exist_tip: '该基因已在图中',
      phenotype_exist_tip: '该表型已在图中',
      no_gene_in_db: '数据库中没有该基因',
      no_phenotype_in_db: '数据库中没有该表型',
      delete_gene_tip: '请不要删除基因节点',
      delete_phenotype_tip: '请不要删除表型节点',
      no_gene_in_figure: '图中没有该基因',
      no_phenotype_in_figure: '图中没有该表型',
      remove_success: '删除成功！',

      file_type_tip: '只能上传.mat类型的文件',
      file_upload_success_tip: '文件上传成功',
      file_num_tip: '最多只能上传一个文件',
      file_upload_fail_tip: '文件上传失败',
      select_file_tip: '请先选择文件',
      file_upload_retry_tip: '文件上传失败，请重试',
      upload_file_tip: '请先上传文件',
      predict_file_fail_tip: '预测失败，请重试',
      download_file_fail_tip: '下载文件失败，请重试',
      get_process_fail_tip: '获取进度失败，请重试',
      get_file_link_tip: '获取文件链接失败，请重试',

      predicting_tip: '正在预测,请稍候',
      predict_complete_tip: '预测完成!'
    }
  }
}
