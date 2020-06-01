<template>
  <div class="single_gp_search" v-loading="loading">
    <el-row type="flex">
      <SideBar :side_bar_index="side_bar_index"></SideBar>
      <div style="width: 80%; margin-left: 5%;">
        <div style="text-align : left; font-size: 2em; color:#3CB371; font-weight:bold; margin-bottom: 2%;">
          {{ $t('message.search.search') }}
        </div>
        <div style="text-align : center; background: white; display:flex; flex-direction:column; color:#808080;">
          <div style="font-size: 1.5em; padding: 2% 0;">
            {{ $t('message.search.title.title1') }}
          </div>
          <el-divider></el-divider>
          <div style="margin: 5% 20%;">
            <div style="margin-bottom:2%; text-align: left;">
              <div>{{ $t('message.search.subtitle.gene') }} :</div>
            </div>
            <el-input type="textarea" :rows="4" :placeholder="$t('message.search.tip.tip2')" v-model="multi_gene_input">
            </el-input>
            <div style="margin-top: 2%; text-align: right;">
              <div>
                ({{ $t('message.search.search_example') }}: &nbsp;
                <a href="javascript:void(0);" @click="handleClick1">#1</a> &nbsp;
                <a href="javascript:void(0);" @click="handleClick2">#2</a>)
              </div>
            </div>
            <div style="margin-top:8%;">
              <el-button type="primary" icon="el-icon-search" round @click="search_genes">{{
                $t('message.search.search')
              }}</el-button>
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
  name: 'multi_gene_search',
  data() {
    return {
      side_bar_index: '/multi_gene_search',
      multi_gene_input: '',
      loading: false
    }
  },
  components: { SideBar },
  methods: {
    handleClick1() {
      this.multi_gene_input = '16\n100131801'
    },
    handleClick2() {
      this.multi_gene_input = 'ATP binding cassette subfamily A member 1\nATP binding cassette subfamily A member 3\nATP binding cassette subfamily B member 7'
    },
    search_genes() {
      if (this.isNull(this.multi_gene_input)) {
        this.$message({
          message: this.$t('message.message_tip.not_null_tip'),
          type: 'warning'
        })
      } else {
        let gene_list = this.filterNoneStr(this.multi_gene_input.split(/[\n]/))
        console.log(gene_list)
        const qs = require('qs')
        this.loading = true
        this.$axios
          .get(
            'http://127.0.0.1:8000/api/search_genes', {
            params: { gene_list: gene_list },
            paramsSerializer: function (params) {
              return qs.stringify(params, { arrayFormat: 'repeat' })
            }
          }
          )
          .then(res => {
            console.log(res)
            if (res.status === 200) {
              this.loading = false
              this.$router.push({
                name: 'multi_search_result',
                params: {
                  para: {
                    search_kind: '1',
                    search_target: gene_list,
                    results: res.data.results,
                    multi_gp_relations: res.data.multi_gp_relations
                  }
                }
              })
            } else {
              this.$message.error(this.$t('message.message_tip.search_gene_fail_tip'))
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
