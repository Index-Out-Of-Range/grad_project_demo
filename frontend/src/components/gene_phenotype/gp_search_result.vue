<template>
  <div style="margin: 5% 15%; background:white;">
    <el-row v-loading="loading">
      <div style="display:flex; justify-content:space-between; padding:2%;">
        <div style="text-align:left; font-size: 2em; font-weight:bold;">
          {{ $t('message.search_result.search_result') }} : #{{ search_target }}
        </div>
        <el-dropdown>
          <el-button type="primary" round>
            {{ $t('message.search_result.download.download')
            }}<i class="el-icon-arrow-down el-icon--right"></i>
          </el-button>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>{{
              $t('message.search_result.download.download_current')
            }}</el-dropdown-item>
            <el-dropdown-item>{{
              $t('message.search_result.download.download_all')
            }}</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
      <el-divider></el-divider>
      <div style="margin: 3% 10%;">
        <div
          style="text-align:left; font-size: 1.5em; font-weight:bold; margin-bottom: 3%;"
        >
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
        <div
          style="text-align:left; font-size: 1.5em; font-weight:bold; margin-bottom: 3%;"
        >
          {{ $t('message.search_result.known_relation') }} :
        </div>
        <div>
          <el-table :data="known_data" stripe style="" border>
            <el-table-column
              :label="$t('message.search_result.table.index')"
              type="index"
              width="60"
              align="center"
            ></el-table-column>
            <el-table-column prop="Name" label="Name" align="center">
              -
            </el-table-column>
            <el-table-column prop="phenotype_name" label="ID" align="center">
            </el-table-column>
            <el-table-column
              prop="gp_relation"
              :label="$t('message.search_result.table.relation')"
              align="center"
            >
            </el-table-column>
            <el-table-column
              :label="$t('message.search_result.table.option')"
              width="150"
              align="center"
            >
              <template slot-scope="scope">
                <el-button
                  type="text"
                  icon="el-icon-link"
                  style="color: #3CB371;"
                  size="mini"
                  @click="handleEdit(scope.$index, scope.row)"
                  >{{ $t('message.search_result.goto') }}</el-button
                >
                <el-button
                  size="mini"
                  type="text"
                  icon="el-icon-delete"
                  style="color: #F56C6C;"
                  @click="handleDelete(scope.$index, scope.row)"
                  >{{ $t('message.search_result.delete') }}</el-button
                >
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div style="padding: 2% 0;">
          <el-slider v-model="slide_known" show-input :max="known_length">
          </el-slider>
        </div>
      </div>
      <el-divider></el-divider>
      <div style="margin: 3% 10%;">
        <div
          style="text-align:left; font-size: 1.5em; font-weight:bold; margin-bottom: 3%;"
        >
          {{ $t('message.search_result.predict_relation') }} :
        </div>
        <div>
          <el-table :data="predict_data" stripe style="" border height="500">
            <el-table-column
              :label="$t('message.search_result.table.index')"
              type="index"
              width="60"
              align="center"
            ></el-table-column>
            <el-table-column prop="Name" label="Name" align="center">
              -
            </el-table-column>
            <el-table-column prop="phenotype_name" label="ID" align="center">
            </el-table-column>
            <el-table-column
              prop="gp_relation"
              :label="$t('message.search_result.table.relation')"
              sortable
              align="center"
            >
            </el-table-column>
            <el-table-column
              :label="$t('message.search_result.table.option')"
              width="150"
              align="center"
            >
              <template slot-scope="scope">
                <el-button
                  type="text"
                  icon="el-icon-link"
                  style="color: #3CB371;"
                  size="mini"
                  @click="handleEdit(scope.$index, scope.row)"
                  >{{ $t('message.search_result.goto') }}</el-button
                >
                <el-button
                  size="mini"
                  type="text"
                  icon="el-icon-delete"
                  style="color: #F56C6C;"
                  @click="handleDelete(scope.$index, scope.row)"
                  >{{ $t('message.search_result.delete') }}</el-button
                >
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div style="padding: 2% 0;">
          <el-slider v-model="slide_predict" show-input :max="predict_length">
          </el-slider>
        </div>
      </div>
      <div style="padding: 2%;">
        <el-button type="primary" round @click="visualize()">
          {{ $t('message.search_result.visulaize') }}
        </el-button>
      </div>
    </el-row>
  </div>
</template>

<script>
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
      slide_known: 0,
      slide_predict: 0,
      known_length: 0,
      predict_length: 0
    }
  },
  created() {
    console.log('created...................')
    if (typeof this.$route.params.para !== 'undefined') {
      this.search_kind = this.$route.params.para['search_kind']
      this.search_target = this.$route.params.para['search_target']
      this.predict_data = this.$route.params.para['predict_data']
      this.known_data = this.$route.params.para['known_data']
    } else if (sessionStorage.getItem('save_data') != null) {
      this.save_data = JSON.parse(sessionStorage.getItem('save_data'))
      this.search_kind = this.save_data['search_kind']
      this.search_target = this.save_data['search_target']
      this.predict_data = this.save_data['predict_data']
      this.known_data = this.save_data['known_data']
    } else {
      this.$message.error('出错！！！')
    }

    this.target_info = [
      {
        Attributes: 'Name',
        Content: '-'
      },
      {
        Attributes: 'ID',
        Content: this.search_target
      },
      {
        Attributes: 'Detail',
        Content: '-'
      }
    ]

    this.slide_known = this.known_data.length
    this.slide_predict = this.predict_data.length
    this.known_length = this.known_data.length
    this.predict_length = this.predict_data.length

    if (
      this.isEmptyObject(this.known_data) &&
      this.isEmptyObject(this.predict_data)
    ) {
      this.$message.error(
        '数据库中没有ID为' + String(this.search_target) + '的记录！'
      )
    }
  },
  mounted() {
    console.log('mounted...................')
    this.save_data = {
      search_kind: this.search_kind,
      search_target: this.search_target,
      predict_data: this.predict_data,
      known_data: this.known_data
    }
    sessionStorage.setItem('save_data', JSON.stringify(this.save_data))
  },
  destroyed() {
    console.log('destroyed...................')
    this.save_data = {
      search_kind: this.search_kind,
      search_target: this.search_target,
      predict_data: this.predict_data,
      known_data: this.known_data
    }
    sessionStorage.setItem('save_data', JSON.stringify(this.save_data))
  },
  methods: {
    isEmptyObject(obj) {
      for (var n in obj) {
        return false
      }
      return true
    },
    formatData() {},
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
