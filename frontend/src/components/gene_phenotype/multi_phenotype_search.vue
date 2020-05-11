<template>
  <div class="single_gp_search">
    <el-row type="flex">
      <SideBar :side_bar_index="side_bar_index"></SideBar>
      <div style="width: 80%; margin-left: 5%;">
        <div
          style="text-align : left; font-size: 2em; color:#3CB371; font-weight:bold; margin-bottom: 2%;"
        >
          {{ $t('message.search.search') }}
        </div>
        <div
          style="text-align : center; background: white; display:flex; flex-direction:column; color:#808080;"
        >
          <div style="font-size: 1.5em; padding: 2% 0;">
            {{ $t('message.search.title.title2') }}
          </div>
          <el-divider></el-divider>
          <div style="margin: 5% 20%;">
            <div style="margin-bottom:2%; text-align: left;">
              <div>{{ $t('message.search.subtitle.phenotype') }} :</div>
            </div>
            <el-input
              type="textarea"
              :rows="4"
              :placeholder="$t('message.search.tip.tip2')"
              v-model="multi_phenotype_input"
            >
            </el-input>
            <div style="margin-top: 2%; text-align: right;">
              <div>
                ({{ $t('message.search.search_example') }}: &nbsp;<a href="/#"
                  >#1</a
                >
                &nbsp; <a href="/#">#2</a>)
              </div>
            </div>
            <div style="margin-top:10%;">
              <el-button type="primary" icon="el-icon-search" round>{{
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
  name: 'multi_phenotype_search',
  data() {
    return {
      side_bar_index: '/multi_phenotype_search',
      multi_phenotype_input: ''
    }
  },
  components: { SideBar }
}
</script>

<style scoped>
.single_gp_search {
  margin: 5% 15%;
}

.el-divider--horizontal{
  margin:1px 0;
}

a:link {color:#A0B5D1;}      /* 未访问链接*/
a:visited {color:#A0B5D1;}  /* 已访问链接 */
a:hover {color:#A0B5D1;}  /* 鼠标移动到链接上 */
a:active {color:#A0B5D1;}  /* 鼠标点击时 */

.el-button--primary{
  color: #fff;
  background-color: #3CB371;
  border-color: #3CB371;
}
</style>
