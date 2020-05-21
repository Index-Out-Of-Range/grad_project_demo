<template>
  <div style="margin: 5% 15%; background:white;" v-loading="loading">
    <div style="width:80%; padding: 0 10%;">
      <div style="font-size: 30px; font-weight:bold; padding: 2% 0;">
        {{ $t('message.search_result.search_result') }}
      </div>
    </div>
    <div>
      <div style="padding:2%;" v-for="(result,index) in results" :key="index">
        <div style="text-align:left; font-size: 2em; font-weight:bold;">
          {{search_kind==='1'?'GENE':'PHENOTYPE'}} ID: #{{ result['target'] }}
        </div>
        <el-divider></el-divider>
        <div v-if="empty_result_list[index]">
          <div style="display:flex; align-items: center; font-size: 20px;justify-content:center;margin: 3% 10%;">
            {{ $t('message.search_result.tip.tip1') }}
            <div style="color:red;">#{{ result['target'] }}</div>
            {{ $t('message.search_result.tip.tip2') }}
          </div>
        </div>
        <div v-else>
          <div style="margin: 3% 10%;">
            <div style="text-align:left; font-size: 1.5em; font-weight:bold; margin-bottom: 3%;">
              {{ $t('message.search_result.detail') }} :
            </div>
            <div>
              <el-table :data="target_detail(result['target'])" :show-header="false" border>
                <el-table-column prop="Attributes" width="100"> </el-table-column>
                <el-table-column prop="Content"> </el-table-column>
              </el-table>
            </div>
          </div>
          <el-divider></el-divider>
          <div style="margin: 3% 10%;">
            <div style="text-align:left; font-size: 1.5em; font-weight:bold; margin-bottom: 3%;">
              {{ $t('message.search_result.known_relation') }} :
            </div>
            <div>
              <div style="display:flex; justify-content:flex-end; margin:3% 0;">
                <el-input v-model="known_data_list[index].knownTableSearchID" :placeholder="$t('message.search.tip.tip1')" prefix-icon="el-icon-search" clearable @change="changeKnownInput(index)" style="width:40%;"></el-input>
                <el-button type="primary" @click="knownFilter(index)">{{ $t('message.search_btn') }}</el-button>
              </div>
              <el-table :data="known_data_list[index].knownTableCurrentData" stripe style="" border>
                <el-table-column :label="$t('message.search_result.table.index')" type="index" width="60" align="center"></el-table-column>
                <el-table-column prop="Name" label="Name" align="center">
                  -
                </el-table-column>
                <el-table-column v-if="column_gene" prop="gene_name" label="ID" align="center">
                </el-table-column>
                <el-table-column v-if="column_phenotype" prop="phenotype_name" label="ID" align="center">
                </el-table-column>
                <el-table-column prop="gp_relation" :label="$t('message.search_result.table.relation')" align="center">
                </el-table-column>
                <el-table-column :label="$t('message.search_result.table.option')" width="150" align="center">
                  <template slot-scope="scope">
                    <el-button type="text" icon="el-icon-link" style="color: #3CB371;" size="mini" @click="handleKnownGoto(scope.$index, scope.row, index)">{{ $t('message.search_result.goto') }}</el-button>
                    <el-button size="mini" type="text" icon="el-icon-delete" style="color: #F56C6C;" @click="handleKnownDelete(scope.$index, scope.row, index)">{{ $t('message.search_result.delete') }}</el-button>
                  </template>
                </el-table-column>
              </el-table>
              <el-pagination @current-change="handleKnownCurrentChange($event, index)" :current-page="known_data_list[index].knownCurrentPage" :page-size="known_data_list[index].knownPageSize" layout="total, prev, pager, next, jumper" :total="known_data_list[index].knownTotalItems" style="margin-top:3%;">
              </el-pagination>
            </div>
          </div>
          <el-divider></el-divider>
          <div style="margin: 3% 10%;">
            <div style="text-align:left; font-size: 1.5em; font-weight:bold; margin-bottom: 3%;">
              {{ $t('message.search_result.predict_relation') }} :
            </div>
            <div>
              <div style="display:flex; justify-content:flex-end; margin:3% 0;">
                <el-input v-model="predict_data_list[index].predictTableSearchID" :placeholder="$t('message.search.tip.tip1')" prefix-icon="el-icon-search" clearable @change="changePredictInput(index)" style="width:40%;"></el-input>
                <el-button type="primary" @click="predictFilter(index)">{{ $t('message.search_btn') }}</el-button>
              </div>
              <el-table :data="predict_data_list[index].predictTableCurrentData" stripe style="" border>
                <el-table-column :label="$t('message.search_result.table.index')" type="index" width="60" align="center"></el-table-column>
                <el-table-column prop="Name" label="Name" align="center">
                  -
                </el-table-column>
                <el-table-column v-if="column_gene" prop="gene_name" label="ID" align="center">
                </el-table-column>
                <el-table-column v-if="column_phenotype" prop="phenotype_name" label="ID" align="center">
                </el-table-column>
                <el-table-column prop="gp_relation" :label="$t('message.search_result.table.relation')" sortable align="center">
                </el-table-column>
                <el-table-column :label="$t('message.search_result.table.option')" width="150" align="center">
                  <template slot-scope="scope">
                    <el-button type="text" icon="el-icon-link" style="color: #3CB371;" size="mini" @click="handlePredictGoto(scope.$index, scope.row, index)">{{ $t('message.search_result.goto') }}</el-button>
                    <el-button size="mini" type="text" icon="el-icon-delete" style="color: #F56C6C;" @click="handlePredictDelete(scope.$index, scope.row, index)">{{ $t('message.search_result.delete') }}</el-button>
                  </template>
                </el-table-column>
              </el-table>
              <el-pagination @current-change="handlePredictCurrentChange($event, index)" :current-page="predict_data_list[index].predictCurrentPage" :page-size="predict_data_list[index].predictPageSize" layout="total, prev, pager, next, jumper" :total="predict_data_list[index].predictTotalItems" style="margin-top:3%;">
              </el-pagination>
            </div>
          </div>
        </div>
      </div>

      <div style="padding: 2% 10%; display:flex; justify-content:space-around;">
        <el-dropdown @command="handleCommand">
          <el-button type="primary" round>
            {{ $t('message.search_result.download.download') }}
            <i class="el-icon-arrow-down el-icon--right"></i>
          </el-button>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="current">{{
              $t('message.search_result.download.download_current')
            }}</el-dropdown-item>
            <el-dropdown-item command="all">{{
              $t('message.search_result.download.download_all')
            }}</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
        <el-button type="primary" round @click="visualize()">
          {{ $t('message.search_result.visulaize') }}
          <i class="el-icon-right el-icon--right"></i>
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      search_kind: '',
      search_target: '',
      results: '',
      multi_gp_relations: '',
      all_results: '',
      all_multi_gp_relations: '',
      save_genes_data: {},
      loading: false,

      column_gene: true,
      column_phenotype: true,
      empty_result_list: [],

      known_data_list: [],
      predict_data_list: []
    }
  },
  methods: {
    isEmptyObject(obj) {
      for (var n in obj) {
        return false
      }
      return true
    },
    save_all_data() {
      this.save_genes_data = {
        search_kind: this.search_kind,
        search_target: this.search_target,
        results: this.results,
        multi_gp_relations: this.multi_gp_relations,
        all_results: this.all_results,
        all_multi_gp_relations: this.all_multi_gp_relations,
      }
      sessionStorage.setItem('save_data', JSON.stringify(this.save_genes_data))
      sessionStorage.setItem('visualize_data', JSON.stringify(this.save_genes_data))
    },
    knownFilter(index) {
      if (this.known_data_list[index].knownTableSearchID === '') {
        this.$message.warning(this.$t('message.message_tip.not_null_tip'))
        return
      }
      this.known_data_list[index].knownTableCurrentData = []
      this.known_data_list[index].knownFilterTableData = []
      this.results[index].known_results.forEach((value, index_1) => {
        if (this.search_kind === '2') {
          if (value.gene_name) {
            if (String(value.gene_name).indexOf(this.known_data_list[index].knownTableSearchID) >= 0) {
              this.known_data_list[index].knownFilterTableData.push(value)
            }
          }
        } else if (this.search_kind === '1') {
          if (value.phenotype_name) {
            if (
              String(value.phenotype_name).indexOf(this.known_data_list[index].knownTableSearchID) >= 0
            ) {
              this.known_data_list[index].knownFilterTableData.push(value)
            }
          }
        }
      })
      this.known_data_list[index].knownCurrentPage = 1
      this.known_data_list[index].knownTotalItems = this.known_data_list[index].knownFilterTableData.length
      this.knownCurrentChangePage(index, this.known_data_list[index].knownFilterTableData)
      this.known_data_list[index].knownFlag = true
    },
    handleKnownCurrentChange(val, index) {
      this.known_data_list[index].knownCurrentPage = val
      if (!this.known_data_list[index].knownFlag) {
        this.knownCurrentChangePage(index, this.results[index].known_results)
      } else {
        this.knownCurrentChangePage(index, this.known_data_list[index].knownFilterTableData)
      }
    },
    knownCurrentChangePage(index, list) {
      let from = (this.known_data_list[index].knownCurrentPage - 1) * this.known_data_list[index].knownPageSize
      let to = this.known_data_list[index].knownCurrentPage * this.known_data_list[index].knownPageSize
      this.known_data_list[index].knownTableCurrentData = []
      for (; from < to; from++) {
        if (list[from]) {
          this.known_data_list[index].knownTableCurrentData.push(list[from])
        }
      }
    },
    changeKnownInput(index) {
      this.known_data_list[index].knownFlag = false
      this.known_data_list[index].knownTotalItems = this.results[index].known_results.length
      this.handleKnownCurrentChange(1, index)
    },
    predictFilter(index) {
      if (this.predict_data_list[index].predictTableSearchID === '') {
        this.$message.warning(this.$t('message.message_tip.not_null_tip'))
        return
      }
      this.predict_data_list[index].predictTableCurrentData = []
      this.predict_data_list[index].predictFilterTableData = []
      this.results[index].predict_results.forEach((value, index_1) => {
        if (this.search_kind === '2') {
          if (value.gene_name) {
            if (
              String(value.gene_name).indexOf(this.predict_data_list[index].predictTableSearchID) >= 0
            ) {
              this.predict_data_list[index].predictFilterTableData.push(value)
            }
          }
        } else if (this.search_kind === '1') {
          if (value.phenotype_name) {
            if (
              String(value.phenotype_name).indexOf(this.predict_data_list[index].predictTableSearchID) >= 0
            ) {
              this.predict_data_list[index].predictFilterTableData.push(value)
            }
          }
        }
      })
      this.predict_data_list[index].predictCurrentPage = 1
      this.predict_data_list[index].predictTotalItems = this.predict_data_list[index].predictFilterTableData.length
      this.predictCurrentChangePage(index, this.predict_data_list[index].predictFilterTableData)
      this.predict_data_list[index].predictFlag = true
    },
    handlePredictCurrentChange(val, index) {
      this.predict_data_list[index].predictCurrentPage = val
      if (!this.predict_data_list[index].predictFlag) {
        this.predictCurrentChangePage(index, this.results[index].predict_results)
      } else {
        this.predictCurrentChangePage(index, this.predict_data_list[index].predictFilterTableData)
      }
    },
    predictCurrentChangePage(index, list) {
      let from = (this.predict_data_list[index].predictCurrentPage - 1) * this.predict_data_list[index].predictPageSize
      let to = this.predict_data_list[index].predictCurrentPage * this.predict_data_list[index].predictPageSize
      this.predict_data_list[index].predictTableCurrentData = []
      for (; from < to; from++) {
        if (list[from]) {
          this.predict_data_list[index].predictTableCurrentData.push(list[from])
        }
      }
    },
    changePredictInput(index) {
      this.predict_data_list[index].predictFlag = false
      this.predict_data_list[index].predictTotalItems = this.results[index].predict_results.length
      this.handlePredictCurrentChange(1, index)
    },
    handleGoto(row) {
      const qs = require('qs')
      if (this.search_kind === '1') {
        let phenotype_list = []
        phenotype_list.push(row.phenotype_name)
        this.$axios.get('http://127.0.0.1:8000/api/search_phenotypes', {
          params: { phenotype_list: phenotype_list },
          paramsSerializer: function (params) {
            return qs.stringify(params, { arrayFormat: 'repeat' })
          }
        }).then(res => {
          console.log(res)
          if (res.status === 200) {
            this.loading = false
            this.search_kind = '2'
            this.search_target = phenotype_list
            this.results = res.data.results
            this.multi_gp_relations = res.data.multi_gp_relations
            this.all_results = res.data.results
            this.all_multi_gp_relations = res.data.multi_gp_relations
            this.save_all_data()
            this.update_table_data()
          } else {
            this.$message.error(this.$t('message.message_tip.search_phenotype_fail_tip'))
            console.log(res.data.msg)
          }
        })
          .catch(error => console.log(error))
      } else if (this.search_kind === '2') {
        let gene_list = []
        gene_list.push(row.gene_name)
        this.$axios.get('http://127.0.0.1:8000/api/search_genes', {
          params: { gene_list: gene_list },
          paramsSerializer: function (params) {
            return qs.stringify(params, { arrayFormat: 'repeat' })
          }
        }).then(res => {
          console.log(res)
          if (res.status === 200) {
            this.loading = false
            this.search_kind = '1'
            this.search_target = gene_list
            this.results = res.data.results
            this.multi_gp_relations = res.data.multi_gp_relations
            this.all_results = res.data.results
            this.all_multi_gp_relations = res.data.multi_gp_relations
            this.save_all_data()
            this.update_table_data()
          } else {
            this.$message.error(this.$t('message.message_tip.search_gene_fail_tip'))
            console.log(res.data.msg)
          }
        })
          .catch(error => console.log(error))
      }
    },
    handleKnownGoto(s_index, row, index) {
      console.log(s_index, row)
      this.loading = true
      this.handleGoto(row)
      this.handleKnownCurrentChange(1, index)
    },
    handleKnownDelete(s_index, row, index) {
      console.log(s_index, row, index)
      this.$confirm(this.$t('message.message_tip.delete_info.confirm_info'), {
        confirmBtnText: this.$t('message.message_tip.delete_info.ok'),
        cancelBtnText: this.$t('message.message_tip.delete_info.cancel'),
        type: 'warning'
      })
        .then(() => {
          this.results[index].known_results.splice(s_index, 1)
          this.known_data_list[index].knownTotalItems = this.results[index].known_results.length
          this.handleKnownCurrentChange(this.known_data_list[index].knownCurrentPage, index)
          this.save_all_data()
          this.$message({
            type: 'success',
            message: this.$t('message.message_tip.delete_info.success_info')
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: this.$t('message.message_tip.delete_info.cancel_info')
          })
        })
    },
    handlePredictGoto(s_index, row, index) {
      console.log(s_index, row)
      this.loading = true
      this.handleGoto(row)
      this.handlePredictCurrentChange(1, index)
    },
    handlePredictDelete(s_index, row, index) {
      this.$confirm(this.$t('message.message_tip.delete_info.confirm_info'), {
        confirmBtnText: this.$t('message.message_tip.delete_info.ok'),
        cancelBtnText: this.$t('message.message_tip.delete_info.cancel'),
        type: 'warning'
      })
        .then(() => {
          this.results[index].predict_results.splice(s_index, 1)
          this.predict_data_list[index].predictTotalItems = this.results[index].predict_results.length
          this.handlePredictCurrentChange(this.predict_data_list[index].predictCurrentPage, index)
          this.save_all_data()
          this.$message({
            type: 'success',
            message: this.$t('message.message_tip.delete_info.success_info')
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: this.$t('message.message_tip.delete_info.cancel_info')
          })
        })
    },
    set_table_data() {
      let table_num = this.search_target.length
      for (let i = 0; i < table_num; i++) {
        this.known_data_list.push({
          knownTableSearchID: '',
          knownTableCurrentData: [],
          knownCurrentPage: 1,
          knownPageSize: 10,
          knownTotalItems: 0,
          knownFilterTableData: [],
          knownFlag: false
        })
        this.predict_data_list.push({
          predictTableSearchID: '',
          predictTableCurrentData: [],
          predictCurrentPage: 1,
          predictPageSize: 10,
          predictTotalItems: 0,
          predictFilterTableData: [],
          predictFlag: false
        })
      }
    },
    update_table_data() {
      if (this.search_kind === '1') {
        this.column_gene = false
        this.column_phenotype = true
      } else if (this.search_kind === '2') {
        this.column_gene = true
        this.column_phenotype = false
      }
      let table_num = this.search_target.length
      for (let i = 0; i < table_num; i++) {
        if (this.empty_result_list[i]) {
          return
        }
        this.known_data_list[i].knownTableCurrentData = []
        this.predict_data_list[i].predictTableCurrentData = []
        this.known_data_list[i].knownTotalItems = this.results[i].known_results.length
        this.predict_data_list[i].predictTotalItems = this.results[i].predict_results.length
        if (this.known_data_list[i].knownTotalItems > this.known_data_list[i].knownPageSize) {
          for (let index = 0; index < this.known_data_list[i].knownPageSize; index++) {
            this.known_data_list[i].knownTableCurrentData.push(this.results[i].known_results[index])
          }
        } else {
          this.known_data_list[i].knownTableCurrentData = this.results[i].known_results
        }
        if (this.predict_data_list[i].predictTotalItems > this.predict_data_list[i].predictPageSize) {
          for (let index = 0; index < this.predict_data_list[i].predictPageSize; index++) {
            this.predict_data_list[i].predictTableCurrentData.push(this.results[i].predict_results[index])
          }
        } else {
          this.predict_data_list[i].predictTableCurrentData = this.results[i].predict_results
        }
      }
    },
    handleCommand(command) {
      let filename = ''
      let data = {}
      if (command === 'current') {
        data = this.results
        filename = 'current_multi_result.json'
      } else if (command === 'all') {
        data = this.all_results
        filename = 'all_multi_result.json'
      }
      var FileSaver = require('file-saver')
      var blob = new Blob([JSON.stringify(data, null, 4)], {
        type: 'text/plain;charset=utf-8'
      })
      FileSaver.saveAs(blob, filename)
    },
    visualize() {
      this.$router.push({
        name: 'gp_visualize',
        // params: {
        //   para: {
        //     multi: true,
        //     search_target: this.search_target,
        //     all_results: this.all_results,
        //     all_multi_gp_relations: this.all_multi_gp_relations
        //   }
        // }
      })
    }
  },
  created() {
    console.log('created...')
    if (typeof this.$route.params.para !== 'undefined') {
      this.search_kind = this.$route.params.para['search_kind']
      this.search_target = this.$route.params.para['search_target']
      for (let i = 0; i < this.$route.params.para['results'].length; i++) {
        this.empty_result_list.push(this.isEmptyObject(this.$route.params.para['results'][i]['known_results']) && this.isEmptyObject(this.$route.params.para['results'][i]['predict_results']))
      }
      this.results = this.$route.params.para['results']
      this.multi_gp_relations = this.$route.params.para['multi_gp_relations']
      this.all_results = this.$route.params.para['results']
      this.all_multi_gp_relations = this.$route.params.para['multi_gp_relations']
    } else if (sessionStorage.getItem('save_data') != null) {
      this.save_genes_data = JSON.parse(sessionStorage.getItem('save_data'))
      this.search_kind = this.save_genes_data['search_kind']
      this.search_target = this.save_genes_data['search_target']
      this.results = this.save_genes_data['results']
      this.multi_gp_relations = this.save_genes_data['multi_gp_relations']
      this.all_results = this.save_genes_data['all_results']
      this.all_multi_gp_relations = this.save_genes_data['all_multi_gp_relations']
    }
    this.set_table_data()
  },
  mounted() {
    console.log('mounted...')
    this.save_all_data()
    this.update_table_data()
  },
  destroyed() {
    console.log('destroyed...')
    this.save_all_data()
  },
  computed: {
    target_detail() {
      return function (target) {
        return [
          { Attributes: 'Name', Content: '-' },
          { Attributes: 'ID', Content: target },
          { Attributes: 'Detail', Content: '-' }
        ]
      }
    }
  }
}
</script>

<style scoped>
.el-divider--horizontal {
  margin: 1px 0;
}

.el-button--primary {
  color: #fff;
  background-color: #3cb371;
  border-color: #3cb371;
}
</style>

<style>
.el-pager li.active {
  color: #3cb371 !important;
}
.el-pager li:hover {
  color: #3cb371 !important;
}
.el-pagination .btn-next .el-icon,
.el-pagination .btn-prev .el-icon {
  color: #3cb371 !important;
}
</style>
