<template>
  <div style="margin: 5% 15%; background:white;" v-loading="loading">
    <div style="width:80%; padding: 0 10%;">
      <div style="font-size: 30px; font-weight:bold; padding: 2% 0;">
        {{ $t('message.search_result.search_result') }}
      </div>
    </div>
    <el-row v-if="empty_result">
      <div style="width:80%; padding: 0 10%;">
        <div style="display:flex; align-items: center; font-size: 20px;justify-content:center;padding-bottom:2%;">
          {{ $t('message.search_result.tip.tip1') }}
          <div style="color:red;">#{{ this.search_target }}</div>
          {{ $t('message.search_result.tip.tip2') }}
        </div>
        <div style="padding-bottom: 2%;">
          <el-button type="primary" round icon="el-icon-back" @click="go_back()">
            {{ $t('message.search_result.tip.tip3') }}
          </el-button>
        </div>
      </div>
    </el-row>
    <el-row v-else>
      <div style="display:flex; justify-content:space-between; padding:2%;">
        <div style="text-align:left; font-size: 2em; font-weight:bold;">
          {{search_kind==='1'?'GENE':'PHENOTYPE'}} ID: #{{ search_target }}
        </div>
      </div>
      <el-divider></el-divider>
      <div style="margin: 3% 10%;">
        <div style="text-align:left; font-size: 1.5em; font-weight:bold; margin-bottom: 3%;">
          {{ $t('message.search_result.detail') }} :
        </div>
        <div>
          <el-table :data="target_info" :show-header="false" border>
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
            <el-input v-model="knownTableSearchID" placeholder="请输入ID / Name" prefix-icon="el-icon-search" clearable @change="changeKnownInput" style="width:40%;"></el-input>
            <el-button type="primary" @click="knownFilter">搜索</el-button>
          </div>
          <el-table :data="knownTableCurrentData" stripe style="" border>
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
                <el-button type="text" icon="el-icon-link" style="color: #3CB371;" size="mini" @click="handleKnownGoto(scope.$index, scope.row)">{{ $t('message.search_result.goto') }}</el-button>
                <el-button size="mini" type="text" icon="el-icon-delete" style="color: #F56C6C;" @click="handleKnownDelete(scope.$index, scope.row)">{{ $t('message.search_result.delete') }}</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination @current-change="handleKnownCurrentChange" :current-page="knownCurrentPage" :page-size="knownPageSize" layout="total, prev, pager, next, jumper" :total="knownTotalItems" style="margin-top:3%;">
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
            <el-input v-model="predictTableSearchID" placeholder="请输入ID / Name" prefix-icon="el-icon-search" clearable @change="changePredictInput" style="width:40%;"></el-input>
            <el-button type="primary" @click="predictFilter">搜索</el-button>
          </div>
          <el-table :data="predictTableCurrentData" stripe style="" border>
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
                <el-button type="text" icon="el-icon-link" style="color: #3CB371;" size="mini" @click="handlePredictGoto(scope.$index, scope.row)">{{ $t('message.search_result.goto') }}</el-button>
                <el-button size="mini" type="text" icon="el-icon-delete" style="color: #F56C6C;" @click="handlePredictDelete(scope.$index, scope.row)">{{ $t('message.search_result.delete') }}</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination @current-change="handlePredictCurrentChange" :current-page="predictCurrentPage" :page-size="predictPageSize" layout="total, prev, pager, next, jumper" :total="predictTotalItems" style="margin-top:3%;">
          </el-pagination>
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
    </el-row>
  </div>
</template>

<script>
import { saveAs } from 'file-saver'

export default {
  name: 'gp_search_result',
  data() {
    return {
      search_kind: '',
      search_target: '',
      save_data: {},
      loading: false,
      target_info: [],
      known_data: [],
      predict_data: [],
      all_known_data: [],
      all_predict_data: [],

      empty_result: true,
      column_gene: true,
      column_phenotype: true,

      knownTableSearchID: '',
      knownTableCurrentData: [],
      knownCurrentPage: 1,
      knownPageSize: 5,
      knownTotalItems: 0,
      knownFilterTableData: [],
      knownFlag: false,

      predictTableSearchID: '',
      predictTableCurrentData: [],
      predictCurrentPage: 1,
      predictPageSize: 5,
      predictTotalItems: 0,
      predictFilterTableData: [],
      predictFlag: false
    }
  },
  created() {
    console.log('created...................')

    if (typeof this.$route.params.para !== 'undefined') {
      this.search_kind = this.$route.params.para['search_kind']
      this.search_target = this.$route.params.para['search_target']
      this.empty_result =
        this.isEmptyObject(this.$route.params.para['predict_data']) &&
        this.isEmptyObject(this.$route.params.para['known_data'])
      if (this.empty_result) return

      this.all_predict_data = this.$route.params.para['predict_data']
      this.all_known_data = this.$route.params.para['known_data']
      if (this.$route.params.para['predict_data'].length > 50) {
        this.predict_data = this.$route.params.para['predict_data'].slice(0, 50)
      } else {
        this.predict_data = this.$route.params.para['predict_data']
      }
      this.known_data = this.$route.params.para['known_data']
    } else if (sessionStorage.getItem('save_data') != null) {
      this.save_data = JSON.parse(sessionStorage.getItem('save_data'))
      this.search_kind = this.save_data['search_kind']
      this.search_target = this.save_data['search_target']

      this.empty_result = this.save_data['empty_result']
      if (this.empty_result) return

      this.predict_data = this.save_data['predict_data']
      this.known_data = this.save_data['known_data']
      this.all_predict_data = this.save_data['all_predict_data']
      this.all_known_data = this.save_data['all_known_data']
    } else {
      this.$message.error('出错！！！')
    }

    this.target_info = [
      { Attributes: 'Name', Content: '-' },
      { Attributes: 'ID', Content: this.search_target },
      { Attributes: 'Detail', Content: '-' }
    ]
  },
  mounted() {
    console.log('mounted...................')
    this.save_all_data()
    this.update_table_data()
    if (this.search_kind === '1') {
      this.search_type = 'Gene'
    } else if (this.search_kind === '2') {
      this.search_type = 'Phenotype'
    }
  },
  destroyed() {
    console.log('destroyed...................')
    this.save_all_data()
  },
  methods: {
    isEmptyObject(obj) {
      for (var n in obj) {
        return false
      }
      return true
    },
    formatData() { },
    visualize() {
      this.$router.push({
        name: 'gp_visualize'
        // params: {
        //   para: {
        //     search_target: this.search_target,
        //     known_data: this.known_data,
        //     predict_data: this.known_data
        //   }
        // }
      })
    },
    go_back() {
      this.$router.go(-1)
    },
    knownFilter() {
      if (this.knownTableSearchID === '') {
        this.$message.warning('查询条件不能为空！')
        return
      }
      this.knownTableCurrentData = []
      this.knownFilterTableData = []
      this.known_data.forEach((value, index) => {
        if (this.search_kind === '2') {
          if (value.gene_name) {
            if (String(value.gene_name).indexOf(this.knownTableSearchID) >= 0) {
              this.knownFilterTableData.push(value)
            }
          }
        } else if (this.search_kind === '1') {
          if (value.phenotype_name) {
            if (
              String(value.phenotype_name).indexOf(this.knownTableSearchID) >= 0
            ) {
              this.knownFilterTableData.push(value)
            }
          }
        }
      })
      this.knownCurrentPage = 1
      this.knownTotalItems = this.knownFilterTableData.length
      this.knownCurrentChangePage(this.knownFilterTableData)
      this.knownFlag = true
    },
    handleKnownCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.knownCurrentPage = val
      if (!this.knownFlag) {
        this.knownCurrentChangePage(this.known_data)
        console.log(this.knownTableCurrentData)
      } else {
        this.knownCurrentChangePage(this.knownFilterTableData)
        console.log(this.knownTableCurrentData)
      }
    },
    knownCurrentChangePage(list) {
      let from = (this.knownCurrentPage - 1) * this.knownPageSize
      let to = this.knownCurrentPage * this.knownPageSize
      this.knownTableCurrentData = []
      for (; from < to; from++) {
        if (list[from]) {
          this.knownTableCurrentData.push(list[from])
        }
      }
    },
    changeKnownInput() {
      this.knownFlag = false
      this.knownTotalItems = this.known_data.length
      this.handleKnownCurrentChange(1)
    },
    predictFilter() {
      if (this.predictTableSearchID === '') {
        this.$message.warning('查询条件不能为空！')
        return
      }
      this.predictTableCurrentData = []
      this.predictFilterTableData = []
      this.predict_data.forEach((value, index) => {
        if (this.search_kind === '2') {
          if (value.gene_name) {
            if (
              String(value.gene_name).indexOf(this.predictTableSearchID) >= 0
            ) {
              this.predictFilterTableData.push(value)
            }
          }
        } else if (this.search_kind === '1') {
          if (value.phenotype_name) {
            if (
              String(value.phenotype_name).indexOf(this.predictTableSearchID) >=
              0
            ) {
              this.predictFilterTableData.push(value)
            }
          }
        }
      })
      this.predictCurrentPage = 1
      this.predictTotalItems = this.predictFilterTableData.length
      this.predictCurrentChangePage(this.predictFilterTableData)
      this.predictFlag = true
    },
    handlePredictCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.predictCurrentPage = val
      if (!this.predictFlag) {
        this.predictCurrentChangePage(this.predict_data)
        console.log(this.predictTableCurrentData)
      } else {
        this.predictCurrentChangePage(this.predictFilterTableData)
        console.log(this.predictTableCurrentData)
      }
    },
    predictCurrentChangePage(list) {
      let from = (this.predictCurrentPage - 1) * this.predictPageSize
      let to = this.predictCurrentPage * this.predictPageSize
      this.predictTableCurrentData = []
      for (; from < to; from++) {
        if (list[from]) {
          this.predictTableCurrentData.push(list[from])
        }
      }
    },
    changePredictInput() {
      this.predictFlag = false
      this.predictTotalItems = this.predict_data.length
      this.handlePredictCurrentChange(1)
    },
    handleGoto(row) {
      if (this.search_kind === '1') {
        this.$axios
          .get(
            'http://127.0.0.1:8000/api/search_phenotype?phenotype_name=' +
            row.phenotype_name
          )
          .then(res => {
            console.log(res)
            if (res.status === 200) {
              this.loading = false
              this.search_kind = '2'
              this.search_target = row.phenotype_name
              this.all_known_data = res.data.known_results
              this.all_predict_data = res.data.predict_results
              this.known_data = res.data.known_results
              if (res.data.predict_results.length > 50) {
                this.predict_data = res.data.predict_results.slice(0, 50)
              } else {
                this.predict_data = res.data.predict_results
              }
              this.$set(this.target_info[1], 'Content', this.search_target)
              this.update_table_data()
              this.save_data = {
                search_kind: this.search_kind,
                search_target: this.search_target,
                predict_data: this.predict_data,
                known_data: this.known_data,
                all_predict_data: this.all_predict_data,
                all_known_data: this.all_known_data
              }
              sessionStorage.setItem(
                'save_data',
                JSON.stringify(this.save_data)
              )
            } else {
              this.$message.error('查询表型失败，请重试')
              console.log(res.data.msg)
            }
          })
          .catch(error => console.log(error))
      } else if (this.search_kind === '2') {
        this.$axios
          .get(
            'http://127.0.0.1:8000/api/search_gene?gene_name=' + row.gene_name
          )
          .then(res => {
            console.log(res)
            if (res.status === 200) {
              this.loading = false
              this.search_kind = '1'
              this.search_target = row.gene_name
              this.all_known_data = res.data.known_results
              this.all_predict_data = res.data.predict_results
              this.known_data = res.data.known_results
              if (res.data.predict_results.length > 50) {
                this.predict_data = res.data.predict_results.slice(0, 50)
              } else {
                this.predict_data = res.data.predict_results
              }
              this.$set(this.target_info[1], 'Content', this.search_target)
              this.update_table_data()
              this.save_data = {
                search_kind: this.search_kind,
                search_target: this.search_target,
                predict_data: this.predict_data,
                known_data: this.known_data,
                all_predict_data: this.all_predict_data,
                all_known_data: this.all_known_data
              }
              sessionStorage.setItem(
                'save_data',
                JSON.stringify(this.save_data)
              )
            } else {
              this.$message.error('查询基因失败，请重试')
              console.log(res.data.msg)
            }
          })
          .catch(error => console.log(error))
      }
    },
    handleKnownGoto(index, row) {
      console.log(index, row)
      this.loading = true
      this.handleGoto(row)
      this.handleKnownCurrentChange(1)
    },
    handleKnownDelete(index, row) {
      console.log(index, row)
      this.$confirm('无法撤回！确定删除？', {
        confirmBtnText: '确定',
        cancelBtnText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.known_data.splice(index, 1)
          this.knownTotalItems = this.known_data.length
          this.handleKnownCurrentChange(this.knownCurrentPage)
          this.save_all_data()
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消删除'
          })
        })
    },
    handlePredictGoto(index, row) {
      console.log(index, row)
      this.loading = true
      this.handleGoto(row)
      this.handlePredictCurrentChange(1)
    },
    handlePredictDelete(index, row) {
      console.log(index, row)
      this.$confirm('无法撤回！确定删除？', {
        confirmBtnText: '确定',
        cancelBtnText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.predict_data.splice(index, 1)
          this.predictTotalItems = this.predict_data.length
          this.handlePredictCurrentChange(this.predictCurrentPage)
          this.save_all_data()
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消删除'
          })
        })
    },
    update_table_data() {
      this.knownTableCurrentData = []
      this.predictTableCurrentData = []
      if (this.search_kind === '1') {
        this.column_gene = false
        this.column_phenotype = true
      } else if (this.search_kind === '2') {
        this.column_gene = true
        this.column_phenotype = false
      }
      this.knownTotalItems = this.known_data.length
      if (this.knownTotalItems > this.knownPageSize) {
        for (let index = 0; index < this.knownPageSize; index++) {
          this.knownTableCurrentData.push(this.known_data[index])
        }
      } else {
        this.knownTableCurrentData = this.known_data
      }
      this.predictTotalItems = this.predict_data.length
      if (this.predictTotalItems > this.predictPageSize) {
        for (let index = 0; index < this.predictPageSize; index++) {
          this.predictTableCurrentData.push(this.predict_data[index])
        }
      } else {
        this.predictTableCurrentData = this.predict_data
      }
    },
    save_all_data() {
      this.save_data = {
        search_kind: this.search_kind,
        search_target: this.search_target,
        predict_data: this.predict_data,
        known_data: this.known_data,
        all_predict_data: this.all_predict_data,
        all_known_data: this.all_known_data,
        empty_result: this.empty_result,
      }
      sessionStorage.setItem('save_data', JSON.stringify(this.save_data))
      sessionStorage.setItem('visualize_data', JSON.stringify(this.save_data))
    },
    handleCommand(command) {
      let filename = ''
      let data = {}
      if (command === 'current') {
        data = {
          search_target: this.search_target,
          known_data: this.known_data,
          predict_data: this.predict_data
        }
        filename = 'current_result_' + this.search_target + '.json'
      } else if (command === 'all') {
        data = {
          search_target: this.search_target,
          known_data: this.all_known_data,
          predict_data: this.all_predict_data
        }
        filename = 'all_result_' + this.search_target + '.json'
      }
      var FileSaver = require('file-saver')
      var blob = new Blob([JSON.stringify(data, null, 4)], {
        type: 'text/plain;charset=utf-8'
      })
      FileSaver.saveAs(blob, filename)
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
