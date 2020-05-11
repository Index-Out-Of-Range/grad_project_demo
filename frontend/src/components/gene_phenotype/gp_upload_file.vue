<template>
  <div class="single_gp_search">
    <el-row type="flex">
      <SideBar :side_bar_index="side_bar_index"></SideBar>
      <div style="width: 80%; margin-left: 5%;">
        <div
          style="text-align : left; font-size: 2em; color:#3CB371; font-weight:bold; margin-bottom: 2%;"
        >
          {{ $t('message.search.predict') }}
        </div>
        <div
          style="text-align : center; background: white; display:flex; flex-direction:column; color:#808080;"
        >
          <div style="font-size: 1.5em; padding: 2% 0;">
            {{ $t('message.search.title.title3') }}
          </div>
          <el-divider></el-divider>
          <div style="margin: 4% 20%;">
            <div>
              <el-upload
                drag
                action="https://jsonplaceholder.typicode.com/posts/"
                multiple
              >
                <i class="el-icon-upload"></i>
                <div class="el-upload__text">
                  {{ $t('message.search.upload_tip.tip1')
                  }}<em>{{ $t('message.search.upload_tip.tip2') }}</em>
                </div>
                <div class="el-upload__tip" slot="tip">
                  {{ $t('message.search.upload_tip.tip3') }}
                </div>
              </el-upload>
            </div>
            <div style="margin-top:5%;">
              <el-button type="primary" icon="el-icon-search" round>{{
                $t('message.search.predict')
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
  name: 'gp_upload_file',
  data() {
    return {
      side_bar_index: '/gp_upload_file'
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
