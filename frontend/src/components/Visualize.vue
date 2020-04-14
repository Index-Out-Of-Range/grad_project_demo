<template>
    <div>
        <el-row v-loading="loading">
        <H1>可视化结果</H1>
        <div id="my_chart" style="width: 90%; height: 600px">
        </div>
        </el-row>
    </div>
</template>

<script>
import echarts from 'echarts'
export default {
  name: 'Visualize',
  data () {
    return {
      search_kind: '',
      search_target: '',
      predict_results: {},
      known_results: {},
      save_data: {},
      nodes: [],
      links: [],
      categories: [],
      loading: false
    }
  },
  created () {
    console.log('create!!!!!!!!!')
    if (typeof this.$route.params.para !== 'undefined') {
      console.log('++++++++++++++++++++++++++')
      this.search_kind = this.$route.params.para['search_kind']
      this.search_target = this.$route.params.para['search_target']
      this.predict_results = this.$route.params.para['predict_results']
      this.known_results = this.$route.params.para['known_results']
    } else if (sessionStorage.getItem('save_data') != null) {
      this.save_data = JSON.parse(sessionStorage.getItem('save_data'))
      console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~')
      this.search_kind = this.save_data['search_kind']
      this.search_target = this.save_data['search_target']
      this.predict_results = this.save_data['predict_results']
      this.known_results = this.save_data['known_results']
    } else {
      this.$message.error('出错！！！')
    }

    if (this.isEmptyObject(this.known_results) && this.isEmptyObject(this.predict_results)) {
      this.$message.error('数据库中没有ID为' + String(this.search_target) + '的记录！')
    }

    this.update_data()
  },
  mounted () {
    console.log('mounted...................')
    this.save_data = {
      'search_kind': this.search_kind,
      'search_target': this.search_target,
      'predict_results': this.predict_results,
      'known_results': this.known_results
    }
    sessionStorage.setItem('save_data', JSON.stringify(this.save_data))
    this.draw_chart()
  },
  destroyed () {
    console.log('destroyed...................')
    this.save_data = {
      'search_kind': this.search_kind,
      'search_target': this.search_target,
      'predict_results': this.predict_results,
      'known_results': this.known_results
    }
    sessionStorage.setItem('save_data', JSON.stringify(this.save_data))
  },
  methods: {
    isEmptyObject (obj) {
      for (var n in obj) {
        return false
      }
      return true
    },
    draw_chart () {
      let my_chart = this.$echarts.init(document.getElementById('my_chart'))
      let option = {
        title: {
          text: 'Prediction Result'
        },
        tooltip: {
          formatter: function (param) {
            return param.data.value
          }
        },
        legend: [{
          orient: 'vertical',
          left: 'right',
          top: 'bottom',
          data: this.categories.map(function (a) {
            return a.name
          })
        }],
        animationDuration: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [
          {
            type: 'graph',
            layout: 'force',
            focusNodeAdjacency: true,
            roam: true,
            edgeSymbolSize: [10, 10],
            force: {
              repulsion: 2000,
              edgeLength: [20, 40, 60, 80, 100]
            },
            draggable: true,
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
      let that = this
      my_chart.on('click', function (param) {
        console.log('param->', param, 'search_kind->', that.search_kind, 'search_target->', that.search_target)
        if (param.dataType === 'node') {
          if (param.data.category.indexOf('GENE') !== -1 && that.search_kind === '2') {
            that.loading = true
            console.log('GENE:' + param.name)
            that.$axios.get('http://127.0.0.1:8000/api/search_gene?gene_name=' + param.name)
              .then(res => {
                console.log(res)
                if (res.status === 200) {
                  that.loading = false
                  that.search_kind = '1'
                  that.search_target = param.name
                  that.known_results = res.data.known_results
                  that.predict_results = res.data.predict_results
                  that.update_data()
                  that.save_data = {
                    'search_kind': that.search_kind,
                    'search_target': that.search_target,
                    'predict_results': that.predict_results,
                    'known_results': that.known_results
                  }
                  sessionStorage.setItem('save_data', JSON.stringify(that.save_data))

                  var option = my_chart.getOption()
                  option.series[0].data = that.nodes
                  option.series[0].links = that.links
                  option.series[0].categories = that.categories
                  option.legend = [{
                    orient: 'vertical',
                    left: 'right',
                    top: 'bottom',
                    data: that.categories.map(function (a) {
                      return a.name
                    })
                  }]
                  my_chart.setOption(option, true)
                } else {
                  that.$message.error('查询基因失败，请重试')
                  console.log(res.data.msg)
                }
              })
          } else if (param.data.category.indexOf('PHENOTYPE') !== -1 && that.search_kind === '1') {
            that.loading = true
            console.log('PHENOTYPE:' + param.name)
            that.$axios.get('http://127.0.0.1:8000/api/search_phenotype?phenotype_name=' + param.name)
              .then(res => {
                console.log(res)
                if (res.status === 200) {
                  that.loading = false
                  that.search_kind = '2'
                  that.search_target = String(param.name)
                  that.known_results = res.data.known_results
                  that.predict_results = res.data.predict_results
                  that.update_data()
                  that.save_data = {
                    'search_kind': that.search_kind,
                    'search_target': that.search_target,
                    'predict_results': that.predict_results,
                    'known_results': that.known_results
                  }
                  sessionStorage.setItem('save_data', JSON.stringify(that.save_data))
                  var option = my_chart.getOption()
                  option.series[0].data = that.nodes
                  option.series[0].links = that.links
                  option.series[0].categories = that.categories
                  option.legend = [{
                    orient: 'vertical',
                    left: 'right',
                    top: 'bottom',
                    data: that.categories.map(function (a) {
                      return a.name
                    })
                  }]
                  my_chart.setOption(option, true)
                } else {
                  that.$message.error('查询表型失败，请重试')
                  console.log(res.data.msg)
                }
              })
          }
        } else {
        //   alert('点击了边' + param.value)
        }
      })
    },
    update_data () {
      this.nodes.length = []
      this.links.length = []
      this.categories = []

      if (this.search_kind === '1') {
        this.categories = [{name: 'GENE'}, {name: 'PREDICT PHENOTYPE'}, {name: 'KNOWN PHENOTYPE'}]
        this.nodes.push({name: this.search_target, symbolSize: 100, category: 'GENE'})
      } else if (this.search_kind === '2') {
        this.categories = [{name: 'PHENOTYPE'}, {name: 'PREDICT GENE'}, {name: 'KNOWN GENE'}]
        this.nodes.push({name: this.search_target, symbolSize: 100, category: 'PHENOTYPE'})
      }

      let target_name = this.search_kind === '1' ? 'phenotype_name' : 'gene_name'

      for (let i = 0, len = this.predict_results.length; i < len; i++) {
        let item = this.predict_results[i]
        if (this.search_kind === '1') {
          this.nodes.push({name: item[target_name], symbolSize: 50, category: 'PREDICT PHENOTYPE'})
        } else if (this.search_kind === '2') {
          this.nodes.push({name: item[target_name], symbolSize: 50, category: 'PREDICT GENE'})
        }
        this.links.push(
          {
            source: String(this.search_target),
            target: String(item[target_name]),
            value: item['gp_relation'],
            lineStyle: {
              width: 1,
              type: 'dashed',
              color: 'target',
              curveness: 0.2
            }
          }
        )
      }
      for (let i = 0, len = this.known_results.length; i < len; i++) {
        let item = this.known_results[i]
        if (this.search_kind === '1') {
          this.nodes.push({name: item[target_name], symbolSize: 50, category: 'KNOWN PHENOTYPE'})
        } else if (this.search_kind === '2') {
          this.nodes.push({name: item[target_name], symbolSize: 50, category: 'KNOWN GENE'})
        }
        this.links.push(
          {
            source: String(this.search_target),
            target: String(item[target_name]),
            value: item['gp_relation'],
            lineStyle: {
              width: 2,
              color: 'target',
              curveness: 0.2
            }
          }
        )
      }
    }
  }
}
</script>

<style scoped>

</style>
