module.exports = {
  message: {
    language: 'Language',
    system_name: 'BIAPMC',
    zh: 'Chinese',
    en: 'English',
    search_btn: 'search',
    home: {
      version: 'VERSION',
      login: 'LOGIN',
      register: 'REGISTER',
      menu: {
        menu1: 'Gene-Phenotype',
        menu2: 'Drug-Drug',
        menu3: 'Download',
        menu4: 'Help',
        menu5: 'Manage Center'
      },
      input_tip: 'Input phenotype / gene',
      search_example: 'Search Example',
      button: 'Quick Search',
      down_menu: {
        reference: 'Reference',
        contributor: 'Contributor',
        statistics: 'Statistics',
        data_source: 'Data Source',
        faq: 'FAQ',
        api: 'API'
      }
    },
    search: {
      search: 'SEARCH',
      predict: 'PREDICT',
      upload: 'UPLOAD',
      menu: {
        menu1: 'Single Gene Search',
        menu2: 'Single Phenotype Search',
        menu3: 'Multi Gene Search',
        menu4: 'Multi Phenotype Search',
        menu5: 'Upload File'
      },
      title: {
        title1: 'Search Gene By Name / ID',
        title2: 'Search Phenotype By Name / ID',
        title3: 'Upload file to predict'
      },
      search_example: 'Search Example',
      tip: {
        tip1: 'Please input ID / Name',
        tip2: 'Please input ID / Name, one per line.'
      },
      subtitle: {
        gene: 'Gene ID / Name',
        phenotype: 'Phenotype ID / Name'
      },
      upload_tip: {
        tip1: 'Drag file to here, or ',
        tip2: 'click to upload',
        tip3: 'please upload .mat file'
      }
    },
    search_result: {
      search_result: 'Search Result',
      detail: 'Details',
      known_relation: 'Known Relations',
      predict_relation: 'Predict Relations',
      visulaize: 'Visualize',
      download: {
        download: 'Download Result',
        download_current: 'Download Current',
        download_all: 'Download All'
      },
      table: {
        index: 'Index',
        relation: 'Relation',
        option: 'Option',
        detail: 'Details'
      },
      delete: 'DELETE',
      goto: 'GOTO',
      tip: {
        tip1: 'Search target',
        tip2: 'is not in database!',
        tip3: 'Return'
      }
    },
    visulization: {
      visulization_result: 'Visualization Result',
      predict_result: 'Predict Result',
      search_tips: {
        add_gene: 'Add Gene by ID / Name',
        add_phenotype: 'Add Phenotype by ID / Name',
        remove_gene: 'Remove Gene by ID / Name',
        remove_phenotype: 'Remove Phenotype by ID /Name'
      },
      buttons: {
        add_gene: 'Add Gene',
        add_phenotype: 'Add Phenotype',
        remove_gene: 'Remove Gene',
        remove_phenotype: 'Remove Phenotype'
      },
      sliders: {
        known_nodes: 'Known Nodes',
        predict_nodes: 'Predict Nodes'
      }
    },
    message_tip: {
      not_null_tip: 'Input can not be empty',
      search_gene_fail_tip: 'Gene query failed, please try again',
      search_phenotype_fail_tip: 'Phenotype query failed, please try again',
      delete_info: {
        confirm_info: "Can't withdraw! confirm delete?",
        ok: 'OK',
        cancel: 'Cancel',
        success_info: 'Successfully deleted',
        cancel_info: 'Cancel delete'
      },
      error_tip: 'Error!',
      gene_exist_tip: 'The gene is already in the figure',
      phenotype_exist_tip: 'The phenotype is already in the figure',
      no_gene_in_db: 'The gene is not in the database',
      no_phenotype_in_db: 'The phenotype is not in the database',
      delete_gene_tip: "Please don't delete the gene node",
      delete_phenotype_tip: "Please don't delete the phenotype node",
      no_gene_in_figure: 'The gene is not in the figure',
      no_phenotype_in_figure: 'The phenotype is not in the figure',
      remove_success: 'Remove success!',

      file_type_tip: 'Only files of type ".mat" can be uploaded',
      file_upload_success_tip: 'File uploaded successfully',
      file_num_tip: 'You can only upload at most one file',
      file_upload_fail_tip: 'File upload failed',
      select_file_tip: 'Please select the file first',
      file_upload_retry_tip: 'File upload failed, please try again',
      upload_file_tip: 'Please upload the file first',
      predict_file_fail_tip: 'Prediction failed, please try again',
      download_file_fail_tip: 'File download failed, please try again',
      get_process_fail_tip: 'Failed to get progress, please try again',
      get_file_link_tip: 'Failed to get file link, please try again',

      predicting_tip: 'Predicting, please wait',
      predict_complete_tip: 'The prediction is complete!'
    }
  }
}
