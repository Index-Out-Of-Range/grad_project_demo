<template>
  <div class="single_gp_search" v-loading="loading">
    <el-row type="flex">
      <SideBar :side_bar_index="side_bar_index"></SideBar>
      <div style="width: 80%; margin-left: 5%;">
        <div style="text-align : left; font-size: 2em; color:#3CB371; font-weight:bold; margin-bottom: 2%;">{{ $t('message.search.search') }}</div>
        <div style="text-align : center; background: white; display:flex; flex-direction:column; color:#808080;">
          <div style="font-size: 1.5em; padding: 2% 0;">{{ $t('message.search.title.title2') }}</div>
          <el-divider></el-divider>
          <div style="margin: 5% 20%;">
            <div style="margin-bottom:2%; text-align: left;">
              <div>{{ $t('message.search.subtitle.phenotype') }} :</div>
            </div>
            <el-input prefix-icon="el-icon-search" v-model="phenotype_input"></el-input>
            <div style="margin-top: 2%; text-align: right;">
              <div>
                ({{ $t('message.search.search_example') }}: &nbsp;
                <a href="/#">#1</a>
                &nbsp;
                <a href="/#">#2</a>)
              </div>
            </div>
            <div style="margin-top:10%;">
              <el-button @click="search()" type="primary" icon="el-icon-search" round>{{ $t('message.search.search') }}</el-button>
            </div>
          </div>
        </div>
      </div>
    </el-row>
  </div>
</template>

<script>
import SideBar from './SideBar'
export default {
  name: 'single_phenotype_search',
  data() {
    return {
      side_bar_index: '/single_phenotype_search',
      phenotype_input: '',
      loading: false
    }
  },
  components: { SideBar },
  methods: {
    search() {
      if (this.isNull(this.phenotype_input)) {
        this.$message({
          message: '输入不能为空',
          type: 'warning'
        })
      } else {
        this.loading = true
        let phenotype_list = []
        phenotype_list.push(this.phenotype_input)
        console.log(phenotype_list)
        const qs = require('qs')
        this.$axios
          .get(
            'http://127.0.0.1:8000/api/search_phenotypes', {
            params: { phenotype_list: phenotype_list },
            paramsSerializer: function (params) {
              return qs.stringify(params, { arrayFormat: 'repeat' })
            }
          })
          .then(res => {
            console.log(res)
            if (res.status === 200) {
              this.loading = false
              this.$router.push({
                name: 'multi_search_result',
                params: {
                  para: {
                    search_kind: '2',
                    search_target: phenotype_list,
                    results: res.data.results,
                    multi_gp_relations: res.data.multi_gp_relations
                  }
                }
              })
            } else {
              this.$message.error('查询表型失败，请重试')
              console.log(res.data.msg)
            }
          })
          .catch(error => console.log(error))
      }
    }
  }
}
</script>

<style scoped>
.single_gp_search {
  margin: 5% 15%;
}

.el-divider--horizontal {
  margin: 1px 0;
}

a:link {
  color: #a0b5d1;
} /* 未访问链接*/
a:visited {
  color: #a0b5d1;
} /* 已访问链接 */
a:hover {
  color: #a0b5d1;
} /* 鼠标移动到链接上 */
a:active {
  color: #a0b5d1;
} /* 鼠标点击时 */

.el-button--primary {
  color: #fff;
  background-color: #3cb371;
  border-color: #3cb371;
}
</style>
