<template>
  <div class="home">
    <el-row v-loading="loading">
      <el-row>
        <el-input v-model="input" placeholder="请输入基因ID" style="display:inline-table; width: 30%;"/>
        <el-button type="primary" @click="search()" style="margin: 2px;">搜索</el-button>
      </el-row>
      <el-row style="margin-top: 2em">
        <el-radio v-model="radio" label="1">搜索基因</el-radio>
        <el-radio v-model="radio" label="2">搜索表型</el-radio>
      </el-row>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data () {
    return {
      radio: '1',
      input: '',
      loading: false
    }
  },
  mounted: function () {
    // this.showGenes()
  },
  methods: {
    search () {
      if (this.radio === '1') {
        this.loading = true
        this.search_gene()
      } else if (this.radio === '2') {
        this.loading = true
        this.search_phenotype()
      }
    },
    search_gene () {
      this.$axios.get('http://127.0.0.1:8000/api/search_gene?gene_name=' + this.input)
        .then(res => {
          console.log(res)
          if (res.status === 200) {
            this.loading = false
            this.$router.push({
              name: 'Visualize',
              params: {
                para: {
                  'search_kind': this.radio,
                  'search_target': this.input,
                  'known_results': res.data.known_results,
                  'predict_results': res.data.predict_results
                }
              }
            })
          } else {
            this.$message.error('查询基因失败，请重试')
            console.log(res.data.msg)
          }
        })
        .catch(error => console.log(error))
    },
    search_phenotype () {
      this.$axios.get('http://127.0.0.1:8000/api/search_phenotype?phenotype_name=' + this.input)
        .then(res => {
          console.log(res)
          if (res.status === 200) {
            this.loading = false
            this.$router.push({
              name: 'Visualize',
              params: {
                para: {
                  'search_kind': this.radio,
                  'search_target': this.input,
                  'known_results': res.data.known_results,
                  'predict_results': res.data.predict_results
                }
              }
            })
          } else {
            this.$message.error('查询基因失败，请重试')
            console.log(res.data.msg)
          }
        })
        .catch(error => console.log(error))
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
