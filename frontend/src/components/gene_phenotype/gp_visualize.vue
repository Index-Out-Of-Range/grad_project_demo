<template>
  <div style="margin: 5% 15%; background:white; padding: 0 2% 2% 2%;">
    <el-row v-loading="loading" style="margin-bottom:2%;">
      <H2>{{ $t('message.visulization.visulization_result') }}</H2>
      <div id="my_chart" style="width: 100%; height: 600px; "></div>
    </el-row>
    <el-divider></el-divider>
    <div style="padding: 0 2%;">
      <el-row style="display:flex; margin:2% 0; justify-content:space-between;">
        <el-input
          style="width:60%;"
          :placeholder="$t('message.visulization.search_tips.add_gene')"
        ></el-input>
        <el-button
          type="primary"
          style="width:20%;"
          icon="el-icon-circle-plus-outline"
          >{{ $t('message.visulization.buttons.add_gene') }}</el-button
        >
      </el-row>
      <el-row style="display:flex; margin:2% 0; justify-content:space-between;">
        <el-input
          style="width:60%;"
          :placeholder="$t('message.visulization.search_tips.add_phenotype')"
        ></el-input>
        <el-button
          type="primary"
          style="width:20%;"
          icon="el-icon-circle-plus-outline"
          >{{ $t('message.visulization.buttons.add_phenotype') }}</el-button
        >
      </el-row>
      <el-row style="display:flex; margin:2% 0; justify-content:space-between;">
        <el-input
          style="width:60%;"
          :placeholder="$t('message.visulization.search_tips.remove_gene')"
        ></el-input>
        <el-button
          type="danger"
          style="width:20%;"
          icon="el-icon-remove-outline"
          >{{ $t('message.visulization.buttons.remove_gene') }}</el-button
        >
      </el-row>
      <el-row style="display:flex; margin:2% 0; justify-content:space-between;">
        <el-input
          style="width:60%;"
          :placeholder="$t('message.visulization.search_tips.remove_phenotype')"
        ></el-input>
        <el-button
          type="danger"
          style="width:20%;"
          icon="el-icon-remove-outline"
          >{{ $t('message.visulization.buttons.remove_phenotype') }}</el-button
        >
      </el-row>
    </div>
    <el-divider></el-divider>
    <div style="padding: 0 10%;">
      <div
        style="display:flex; align-items:center; justify-content:space-between;"
      >
        <div style="color:gray;">
          {{ $t('message.visulization.sliders.known_nodes') }}:
        </div>
        <el-slider
          v-model="slide_known"
          show-input
          style="margin:2% 0; width: 80%;"
          :max="known_length"
        >
        </el-slider>
      </div>
      <div
        style="display:flex; align-items:center;justify-content:space-between;"
      >
        <div style="color:gray;">
          {{ $t('message.visulization.sliders.predict_nodes') }}:
        </div>
        <el-slider
          v-model="slide_predict"
          show-input
          style="margin:2% 0; width: 80%;"
          :max="predict_length"
        >
        </el-slider>
      </div>
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
      save_data: {},
      loading: false,
      known_data: [],
      predict_data: [],
      nodes: [],
      links: [],
      categories: [],
      slide_known: 0,
      slide_predict: 0,
      known_length: 0,
      predict_length: 0
    }
  },
  created() {
    if (sessionStorage.getItem('save_data') != null) {
      this.save_data = JSON.parse(sessionStorage.getItem('save_data'))
      this.search_kind = this.save_data['search_kind']
      this.search_target = this.save_data['search_target']
      this.predict_data = this.save_data['predict_data']
      this.known_data = this.save_data['known_data']
    } else {
      this.$message.error('出错！！！')
    }

    this.update_data()

    this.slide_known = this.known_data.length
    this.slide_predict = this.predict_data.length
    this.known_length = this.known_data.length
    this.predict_length = this.predict_data.length
  },
  mounted() {
    this.save_data = {
      search_kind: this.search_kind,
      search_target: this.search_target,
      predict_data: this.predict_data,
      known_data: this.known_data
    }
    sessionStorage.setItem('save_data', JSON.stringify(this.save_data))
    this.draw_chart()
  },
  destroyed() {
    this.save_data = {
      search_kind: this.search_kind,
      search_target: this.search_target,
      predict_data: this.predict_data,
      known_data: this.known_data
    }
    sessionStorage.setItem('save_data', JSON.stringify(this.save_data))
  },
  methods: {
    draw_chart() {
      let my_chart = this.$echarts.init(document.getElementById('my_chart'))
      let option = {
        title: {
          text: this.$t('message.visulization.predict_result')
        },
        tooltip: {
          formatter: function(param) {
            return param.data.value
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
            data: this.categories.map(function(a) {
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
      my_chart.on('click', function(param) {
        if (param.dataType === 'node') {
          if (
            param.data.category.indexOf('GENE') !== -1 &&
            that.search_kind === '2'
          ) {
            that.loading = true
            console.log('GENE:' + param.name)
            that.$axios
              .get(
                'http://127.0.0.1:8000/api/search_gene?gene_name=' + param.name
              )
              .then(res => {
                console.log(res)
                if (res.status === 200) {
                  that.loading = false
                  that.search_kind = '1'
                  that.search_target = param.name
                  that.known_data = res.data.known_results
                  that.predict_data = res.data.predict_results
                  that.update_data()
                  that.save_data = {
                    search_kind: that.search_kind,
                    search_target: that.search_target,
                    predict_data: that.predict_data,
                    known_data: that.known_data
                  }
                  sessionStorage.setItem(
                    'save_data',
                    JSON.stringify(that.save_data)
                  )

                  var option = my_chart.getOption()
                  option.series[0].data = that.nodes
                  option.series[0].links = that.links
                  option.series[0].categories = that.categories
                  option.legend = [
                    {
                      orient: 'vertical',
                      left: 'right',
                      top: 'bottom',
                      data: that.categories.map(function(a) {
                        return a.name
                      })
                    }
                  ]
                  my_chart.setOption(option, true)
                } else {
                  that.$message.error('查询基因失败，请重试')
                  console.log(res.data.msg)
                }
              })
          } else if (
            param.data.category.indexOf('PHENOTYPE') !== -1 &&
            that.search_kind === '1'
          ) {
            that.loading = true
            console.log('PHENOTYPE:' + param.name)
            that.$axios
              .get(
                'http://127.0.0.1:8000/api/search_phenotype?phenotype_name=' +
                  param.name
              )
              .then(res => {
                console.log(res)
                if (res.status === 200) {
                  that.loading = false
                  that.search_kind = '2'
                  that.search_target = String(param.name)
                  that.known_data = res.data.known_results
                  that.predict_data = res.data.predict_results
                  that.update_data()
                  that.save_data = {
                    search_kind: that.search_kind,
                    search_target: that.search_target,
                    predict_data: that.predict_data,
                    known_data: that.known_data
                  }
                  sessionStorage.setItem(
                    'save_data',
                    JSON.stringify(that.save_data)
                  )
                  var option = my_chart.getOption()
                  option.series[0].data = that.nodes
                  option.series[0].links = that.links
                  option.series[0].categories = that.categories
                  option.legend = [
                    {
                      orient: 'vertical',
                      left: 'right',
                      top: 'bottom',
                      data: that.categories.map(function(a) {
                        return a.name
                      })
                    }
                  ]
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
    update_data() {
      this.nodes = []
      this.links = []
      this.categories = []

      if (this.search_kind === '1') {
        this.categories = [
          { name: 'GENE' },
          { name: 'PREDICT PHENOTYPE' },
          { name: 'KNOWN PHENOTYPE' }
        ]
        this.nodes.push({
          name: this.search_target,
          symbolSize: 100,
          category: 'GENE'
        })
      } else if (this.search_kind === '2') {
        this.categories = [
          { name: 'PHENOTYPE' },
          { name: 'PREDICT GENE' },
          { name: 'KNOWN GENE' }
        ]
        this.nodes.push({
          name: this.search_target,
          symbolSize: 100,
          category: 'PHENOTYPE'
        })
      }

      let target_name =
        this.search_kind === '1' ? 'phenotype_name' : 'gene_name'

      for (let i = 0, len = this.predict_data.length; i < len; i++) {
        let item = this.predict_data[i]
        if (this.search_kind === '1') {
          this.nodes.push({
            name: item[target_name],
            symbolSize: 50,
            category: 'PREDICT PHENOTYPE'
          })
        } else if (this.search_kind === '2') {
          this.nodes.push({
            name: item[target_name],
            symbolSize: 50,
            category: 'PREDICT GENE'
          })
        }
        this.links.push({
          source: String(this.search_target),
          target: String(item[target_name]),
          value: item['gp_relation'],
          lineStyle: {
            width: 1,
            type: 'dashed',
            color: 'target',
            curveness: 0.2
          }
        })
      }
      for (let i = 0, len = this.known_data.length; i < len; i++) {
        let item = this.known_data[i]
        if (this.search_kind === '1') {
          this.nodes.push({
            name: item[target_name],
            symbolSize: 50,
            category: 'KNOWN PHENOTYPE'
          })
        } else if (this.search_kind === '2') {
          this.nodes.push({
            name: item[target_name],
            symbolSize: 50,
            category: 'KNOWN GENE'
          })
        }
        this.links.push({
          source: String(this.search_target),
          target: String(item[target_name]),
          value: item['gp_relation'],
          lineStyle: {
            width: 2,
            color: 'target',
            curveness: 0.2
          }
        })
      }
    }
  }
}
</script>

<style scoped>
.el-divider--horizontal{
  margin:1px 0;
}

.el-button--primary{
  color: #fff;
  background-color: #3CB371;
  border-color: #3CB371;
}
</style>
