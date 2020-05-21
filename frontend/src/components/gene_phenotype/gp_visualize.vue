<template>
  <div style="margin: 5% 15%; background:white; padding: 0 2% 2% 2%;" v-loading="loading">
    <el-row style="margin-bottom:2%;">
      <H2>{{ $t('message.visulization.visulization_result') }}</H2>
      <div id="my_chart" style="width: 100%; height: 600px; "></div>
    </el-row>
    <el-divider></el-divider>
    <div style="padding: 0 2%;">
      <el-row style="display:flex; margin:2% 0; justify-content:space-between;">
        <el-input style="width:60%;" :placeholder="$t('message.visulization.search_tips.add_gene')" v-model="addGene" clearable></el-input>
        <el-button type="primary" style="width:25%;" icon="el-icon-circle-plus-outline" @click="add_gene">{{ $t('message.visulization.buttons.add_gene') }}</el-button>
      </el-row>
      <el-row style="display:flex; margin:2% 0; justify-content:space-between;">
        <el-input style="width:60%;" :placeholder="$t('message.visulization.search_tips.add_phenotype')" v-model="addPhenotype" clearable></el-input>
        <el-button type="primary" style="width:25%;" icon="el-icon-circle-plus-outline" @click="add_phenotype">{{ $t('message.visulization.buttons.add_phenotype') }}</el-button>
      </el-row>
      <el-row style="display:flex; margin:2% 0; justify-content:space-between;">
        <el-input style="width:60%;" :placeholder="$t('message.visulization.search_tips.remove_gene')" v-model="removeGene" clearable></el-input>
        <el-button type="danger" style="width:25%;" icon="el-icon-remove-outline" @click="remove_gene">{{ $t('message.visulization.buttons.remove_gene') }}</el-button>
      </el-row>
      <el-row style="display:flex; margin:2% 0; justify-content:space-between;">
        <el-input style="width:60%;" :placeholder="$t('message.visulization.search_tips.remove_phenotype')" v-model="removePhenotype" clearable></el-input>
        <el-button type="danger" style="width:25%;" icon="el-icon-remove-outline" @click="remove_phenotype">{{ $t('message.visulization.buttons.remove_phenotype') }}</el-button>
      </el-row>
    </div>
  </div>
</template>

<script>
import echarts from 'echarts'
export default {
  name: 'gp_visualize',
  data() {
    return {
      search_kind: '',
      search_target: '',
      visualize_data: {},
      loading: false,

      nodes: [],
      links: [],
      categories: [],

      all_results: '',
      all_multi_gp_relations: '',

      addGene: '',
      addPhenotype: '',
      removeGene: '',
      removePhenotype: ''
    }
  },
  created() {
    if (sessionStorage.getItem('visualize_data') != null) {
      this.visualize_data = JSON.parse(sessionStorage.getItem('visualize_data'))
      this.search_kind = this.visualize_data['search_kind']
      this.search_target = this.visualize_data['search_target']
      this.all_results = this.visualize_data['all_results']
      this.all_multi_gp_relations = this.visualize_data['all_multi_gp_relations']
    } else {
      this.$message.error(this.$t('message.message_tip.error_tip'))
    }

    this.update_data()
  },
  mounted() {
    this.save_data()
    this.draw_chart()
  },
  destroyed() {
    this.save_data()
  },
  methods: {
    save_data() {
      this.visualize_data = {
        search_kind: this.search_kind,
        search_target: this.search_target,
        all_results: this.all_results,
        all_multi_gp_relations: this.all_multi_gp_relations
      }
      sessionStorage.setItem('visualize_data', JSON.stringify(this.visualize_data))
    },
    draw_chart() {
      let my_chart = this.$echarts.init(document.getElementById('my_chart'))
      let that = this
      let option = {
        title: {
          text: this.$t('message.visulization.predict_result')
        },
        tooltip: {
          trigger: 'item',
          formatter: function (param) {
            if (param.data.value !== undefined) {
              if (that.$i18n.locale === 'zh-CN') {
                return '节点' + param.data.source + '与节点' + param.data.target + '之间的关联是:' + param.data.value
              } else if (that.$i18n.locale === 'en-US') {
                return 'The relation between ' + param.data.source + ' and ' + param.data.target + ' is : ' + param.data.value
              }
            } else {
              if (that.$i18n.locale === 'zh-CN') {
                return '节点 : ' + param.data.name
              } else if (that.$i18n.locale === 'en-US') {
                return 'Node : ' + param.data.name
              }
            }
          }
        },
        toolbox: {
          show: true,
          feature: {
            saveAsImage: {
              show: true,
              excludeComponents: ['toolbox'],
              pixelRatio: 2
            }
          }
        },
        legend: [
          {
            orient: 'vertical',
            left: 'right',
            top: 'bottom',
            data: this.categories.map(function (a) {
              return a.name
            })
          }
        ],
        animationDuration: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [
          {
            type: 'graph',
            layout: 'force',
            // layoutAnimation: true,
            focusNodeAdjacency: true,
            roam: true,
            edgeSymbolSize: [10, 10],
            force: {
              repulsion: 2000,
              edgeLength: [20, 40, 60, 80, 100]
            },
            // draggable: true,
            edgeLabel: {
              show: true,
              color: '#000'
            },
            label: {
              show: true,
              fontSize: 10
            },
            data: this.nodes,
            links: this.links,
            categories: this.categories,
            emphasis: {
              lineStyle: {
                width: 5
              }
            }
          }
        ]
      }
      my_chart.setOption(option, true)
      const qs = require('qs')
      my_chart.on('click', function (param) {
        if (param.dataType === 'node') {
          if (param.data.category.indexOf('GENE') !== -1 && that.search_kind === '2') {
            that.loading = true
            console.log('GENE:' + param.name)
            let gene_list = []
            gene_list.push(param.name)
            that.$axios.get('http://127.0.0.1:8000/api/search_genes', {
              params: { gene_list: gene_list },
              paramsSerializer: function (params) {
                return qs.stringify(params, { arrayFormat: 'repeat' })
              }
            })
              .then(res => {
                console.log(res)
                if (res.status === 200) {
                  that.loading = false
                  that.search_kind = '1'
                  that.search_target = gene_list
                  that.all_results = res.data.results
                  that.all_multi_gp_relations = res.data.multi_gp_relations
                  that.update_data()
                  that.save_data()
                  var option = my_chart.getOption()
                  option.series[0].data = that.nodes
                  option.series[0].links = that.links
                  option.series[0].categories = that.categories
                  option.legend = [
                    {
                      orient: 'vertical',
                      left: 'right',
                      top: 'bottom',
                      data: that.categories.map(function (a) {
                        return a.name
                      })
                    }
                  ]
                  my_chart.setOption(option, true)
                } else {
                  this.$message.error(this.$t('message.message_tip.search_gene_fail_tip'))
                  console.log(res.data.msg)
                }
              })
              .catch(error => console.log(error))
          } else if (param.data.category.indexOf('PHENOTYPE') !== -1 && that.search_kind === '1') {
            that.loading = true
            console.log('PHENOTYPE:' + param.name)
            let phenotype_list = []
            phenotype_list.push(param.name)
            that.$axios.get('http://127.0.0.1:8000/api/search_phenotypes', {
              params: { phenotype_list: phenotype_list },
              paramsSerializer: function (params) {
                return qs.stringify(params, { arrayFormat: 'repeat' })
              }
            })
              .then(res => {
                console.log(res)
                if (res.status === 200) {
                  that.loading = false
                  that.search_kind = '2'
                  that.search_target = phenotype_list
                  that.all_results = res.data.results
                  that.all_multi_gp_relations = res.data.multi_gp_relations
                  that.save_data()
                  that.update_data()
                  var option = my_chart.getOption()
                  option.series[0].data = that.nodes
                  option.series[0].links = that.links
                  option.series[0].categories = that.categories
                  option.legend = [
                    {
                      orient: 'vertical',
                      left: 'right',
                      top: 'bottom',
                      data: that.categories.map(function (a) {
                        return a.name
                      })
                    }
                  ]
                  my_chart.setOption(option, true)
                } else {
                  this.$message.error(this.$t('message.message_tip.search_phenotype_fail_tip'))
                  console.log(res.data.msg)
                }
              })
              .catch(error => console.log(error))
          }
        } else {
          //   alert('点击了边' + param.value)
        }
      })
    },
    update_data() {
      this.nodes = []
      this.links = []
      this.categories = []

      let add_nodes = false

      if (this.search_kind === '1') {
        this.categories = [
          { name: 'GENE' },
          { name: 'PREDICT PHENOTYPE' },
          { name: 'KNOWN PHENOTYPE' }
        ]
        for (let i = 0; i < this.search_target.length; i++) {
          this.nodes.push({
            name: this.search_target[i],
            symbolSize: 80,
            category: 'GENE'
          })
        }
      } else if (this.search_kind === '2') {
        this.categories = [
          { name: 'PHENOTYPE' },
          { name: 'PREDICT GENE' },
          { name: 'KNOWN GENE' }
        ]
        for (let i = 0; i < this.search_target.length; i++) {
          this.nodes.push({
            name: this.search_target[i],
            symbolSize: 80,
            category: 'PHENOTYPE'
          })
        }
      }

      for (var key1 in this.all_multi_gp_relations) {
        for (var key2 in this.all_multi_gp_relations[key1]) {
          var node = {
            name: key2,
            symbolSize: 50
          }
          if (this.all_multi_gp_relations[key1][key2]['type'] === 'predict') {
            if (this.search_kind === '1') {
              node['category'] = 'PREDICT PHENOTYPE'
            } else if (this.search_kind === '2') {
              node['category'] = 'PREDICT GENE'
            }
            let link = {
              source: String(key1),
              target: String(key2),
              value: this.all_multi_gp_relations[key1][key2]['relation'],
              lineStyle: {
                width: 1,
                type: 'dashed',
                color: 'target',
                curveness: 0.2
              }
            }
            if (this.all_multi_gp_relations[key1][key2]['relation'] === 0) {
              link['lineStyle']['opacity'] = 0
            }
            this.links.push(link)
          } else {
            if (this.search_kind === '1') {
              node['category'] = 'KNOWN PHENOTYPE'
            } else if (this.search_kind === '2') {
              node['category'] = 'KNOWN GENE'
            }
            let link = {
              source: String(key1),
              target: String(key2),
              value: this.all_multi_gp_relations[key1][key2]['relation'],
              lineStyle: {
                width: 2,
                color: 'target',
                curveness: 0.2
              }
            }
            if (this.all_multi_gp_relations[key1][key2]['relation'] === 0) {
              link['lineStyle']['opacity'] = 0
            }
            this.links.push(link)
          }
          if (!add_nodes) {
            this.nodes.push(node)
          }
        }
        add_nodes = true
      }
    },
    add_gene() {
      if (this.isNull(this.addGene)) {
        this.$message({ message: this.$t('message.message_tip.not_null_tip'), type: 'warning' })
        return
      }

      const qs = require('qs')
      let phenotype_nodes = []
      let gene_nodes = []
      let add_type = 1
      gene_nodes.push(this.addGene)
      if (this.search_kind === '1') {
        if (this.search_target.indexOf(this.addGene) > -1) {
          this.$message({ message: this.$t('message.message_tip.gene_exist_tip'), type: 'warning' })
          return
        }
        let flag = false
        for (let key1 in this.all_multi_gp_relations) {
          for (let key2 in this.all_multi_gp_relations[key1]) {
            if (!flag) {
              phenotype_nodes.push(key2)
            }
          }
          flag = true
        }
      } else if (this.search_kind === '2') {
        let flag = false
        let genes = []
        for (let key1 in this.all_multi_gp_relations) {
          for (let key2 in this.all_multi_gp_relations[key1]) {
            if (!flag) {
              genes.push(key2)
            }
          }
          flag = true
        }
        if (genes.indexOf(this.addGene) > -1) {
          this.$message({ message: this.$t('message.message_tip.gene_exist_tip'), type: 'warning' })
          return
        }
        for (let key1 in this.all_multi_gp_relations) {
          phenotype_nodes.push(key1)
        }
      }
      this.loading = true
      this.$axios.get('http://127.0.0.1:8000/api/add_gene', {
        params: { gene_nodes: gene_nodes, phenotype_nodes: phenotype_nodes, add_type: add_type },
        paramsSerializer: function (params) {
          return qs.stringify(params, { arrayFormat: 'repeat' })
        }
      }).then(res => {
        console.log(res)
        if (res.status === 200) {
          this.loading = false
          let new_gp_relation = res.data.new_gp_relation
          if (new_gp_relation.length === 0) {
            this.$message({ message: this.$t('message.message_tip.no_gene_in_db'), type: 'warning' })
            return
          }
          if (this.search_kind === '1') {
            let temp_relation = {}
            temp_relation[String(new_gp_relation[0]['gene'])] = {}
            for (let i = 0, len = new_gp_relation.length; i < len; i++) {
              let item = new_gp_relation[i]
              temp_relation[String(item['gene'])][String(item['phenotype'])] = { 'relation': item['gp_relation'], 'type': item['type'] }
            }
            for (var key1 in temp_relation) {
              this.all_multi_gp_relations[key1] = temp_relation[key1]
            }
            this.search_target.push(this.addGene)
          } else if (this.search_kind === '2') {
            for (let i = 0, len = new_gp_relation.length; i < len; i++) {
              this.all_multi_gp_relations[new_gp_relation[i]['phenotype']][new_gp_relation[i]['gene']] = { 'relation': new_gp_relation[i]['gp_relation'], 'type': new_gp_relation[i]['type'] }
            }
          }
          this.update_chart()
          this.addGene = ''
        } else {
          this.$message.error(this.$t('message.message_tip.search_gene_fail_tip'))
          console.log(res.data.msg)
        }
      }).catch(error => console.log(error))
    },
    add_phenotype() {
      if (this.isNull(this.addPhenotype)) {
        this.$message({ message: this.$t('message.message_tip.not_null_tip'), type: 'warning' })
        return
      }

      const qs = require('qs')
      let phenotype_nodes = []
      let gene_nodes = []
      let add_type = 2
      phenotype_nodes.push(this.addPhenotype)
      if (this.search_kind === '1') {
        let flag = false
        let phenotypes = []
        for (let key1 in this.all_multi_gp_relations) {
          for (let key2 in this.all_multi_gp_relations[key1]) {
            if (!flag) {
              phenotypes.push(key2)
            }
          }
          flag = true
        }
        if (phenotypes.indexOf(this.addPhenotype) > -1) {
          this.$message({ message: this.$t('message.message_tip.phenotype_exist_tip'), type: 'warning' })
          return
        }
        for (let key1 in this.all_multi_gp_relations) {
          gene_nodes.push(key1)
        }
      } else if (this.search_kind === '2') {
        if (this.search_target.indexOf(this.addPhenotype) > -1) {
          this.$message({ message: this.$t('message.message_tip.phenotype_exist_tip'), type: 'warning' })
          return
        }
        let flag = false
        for (let key1 in this.all_multi_gp_relations) {
          for (let key2 in this.all_multi_gp_relations[key1]) {
            if (!flag) {
              gene_nodes.push(key2)
            }
          }
          flag = true
        }
      }
      this.loading = true
      this.$axios.get('http://127.0.0.1:8000/api/add_phenotype', {
        params: { gene_nodes: gene_nodes, phenotype_nodes: phenotype_nodes, add_type: add_type },
        paramsSerializer: function (params) {
          return qs.stringify(params, { arrayFormat: 'repeat' })
        }
      }).then(res => {
        console.log(res)
        if (res.status === 200) {
          this.loading = false
          let new_gp_relation = res.data.new_gp_relation
          if (new_gp_relation.length === 0) {
            this.$message({ message: this.$t('message.message_tip.no_phenotype_in_db'), type: 'warning' })
            return
          }
          if (this.search_kind === '1') {
            for (let i = 0, len = new_gp_relation.length; i < len; i++) {
              this.all_multi_gp_relations[new_gp_relation[i]['gene']][new_gp_relation[i]['phenotype']] = { 'relation': new_gp_relation[i]['gp_relation'], 'type': new_gp_relation[i]['type'] }
            }
          } else if (this.search_kind === '2') {
            let temp_relation = {}
            temp_relation[String(new_gp_relation[0]['phenotype'])] = {}
            for (let i = 0, len = new_gp_relation.length; i < len; i++) {
              let item = new_gp_relation[i]
              temp_relation[String(item['phenotype'])][String(item['gene'])] = { 'relation': item['gp_relation'], 'type': item['type'] }
            }
            for (var key1 in temp_relation) {
              this.all_multi_gp_relations[key1] = temp_relation[key1]
            }
            this.search_target.push(this.addPhenotype)
          }
          this.update_chart()
          this.addPhenotype = ''
        } else {
          this.$message.error(this.$t('message.message_tip.search_phenotype_fail_tip'))
          console.log(res.data.msg)
        }
      }).catch(error => console.log(error))
    },
    remove_gene() {
      if (this.isNull(this.removeGene)) {
        this.$message({ message: this.$t('message.message_tip.not_null_tip'), type: 'warning' })
        return
      }
      if (this.search_kind === '1') {
        this.$message({ message: this.$t('message.message_tip.delete_gene_tip'), type: 'warning' })
        return
      }
      if (this.search_kind === '2') {
        let gene_delete = false
        for (var key1 in this.all_multi_gp_relations) {
          for (var key2 in this.all_multi_gp_relations[key1]) {
            if (key2 === this.removeGene) {
              delete this.all_multi_gp_relations[key1][key2]
              gene_delete = true
            }
          }
        }
        if (!gene_delete) {
          this.$message({ message: this.$t('message.message_tip.no_gene_in_figure'), type: 'warning' })
          return
        }
      }
      this.removeGene = ''
      this.$message({ message: this.$t('message.message_tip.remove_success'), type: 'success' })
      this.update_chart()
    },
    remove_phenotype() {
      if (this.isNull(this.removePhenotype)) {
        this.$message({ message: this.$t('message.message_tip.not_null_tip'), type: 'warning' })
        return
      }
      if (this.search_kind === '2') {
        this.$message({ message: this.$t('message.message_tip.delete_phenotype_tip'), type: 'warning' })
        return
      }
      if (this.search_kind === '1') {
        let phenotype_delete = false
        for (var key1 in this.all_multi_gp_relations) {
          for (var key2 in this.all_multi_gp_relations[key1]) {
            if (key2 === this.removePhenotype) {
              delete this.all_multi_gp_relations[key1][key2]
              phenotype_delete = true
            }
          }
        }
        if (!phenotype_delete) {
          this.$message({ message: this.$t('message.message_tip.no_phenotype_in_figure'), type: 'warning' })
          return
        }
      }
      this.removePhenotype = ''
      this.$message({ message: this.$t('message.message_tip.remove_success'), type: 'success' })
      this.update_chart()
    },
    update_chart() {
      this.save_data()
      this.update_data()
      let my_chart = this.$echarts.init(document.getElementById('my_chart'))
      var option = my_chart.getOption()
      option.series[0].data = this.nodes
      option.series[0].links = this.links
      my_chart.setOption(option, true)
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
