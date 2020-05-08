<template>
  <div>
    <el-row style="margin: 18px 0px 0px 18px ">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/admin/dashboard' }">管理中心</el-breadcrumb-item>
        <el-breadcrumb-item>数据管理</el-breadcrumb-item>
        <el-breadcrumb-item>人员管理</el-breadcrumb-item>
      </el-breadcrumb>
    </el-row>
    <edit-form @onSubmit="loadStaff()" ref="edit"></edit-form>
    <el-card style="margin: 18px 2%;width: 95%">
      <el-table
        :data="books"
        stripe
        style="width: 100%"
        :max-height="tableHeight">
        <el-table-column
          type="selection"
          width="55">
        </el-table-column>
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline>
              <el-form-item>
                <span>{{ props.row.abs }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column
          prop="title"
          label="姓名"
          fit>
        </el-table-column>
        <el-table-column
          prop="category.name"
          label="职工级别"
          width="100">
        </el-table-column>
        <el-table-column
          prop="author"
          label="电话号码"
          fit>
        </el-table-column>
        <el-table-column
          prop="date"
          label="邮箱"
          width="120">
        </el-table-column>
        <!--<el-table-column-->
          <!--prop="abs"-->
          <!--label="摘要"-->
          <!--show-overflow-tooltip-->
          <!--fit>-->
        <!--</el-table-column>-->
        <el-table-column
          fixed="right"
          label="操作"
          width="120">
          <template slot-scope="scope">
            <el-button
              @click.native.prevent="editStaff(scope.row)"
              type="text"
              size="small">
              编辑
            </el-button>
            <el-button
              @click.native.prevent="deleteStaff(scope.row.id)"
              type="text"
              size="small">
              移除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div style="margin: 20px 0 20px 0;float: left">
        <el-button>取消选择</el-button>
        <el-button>批量删除</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
  import EditForm from './EditForm'
  export default {
    name: 'StaffManagement',
    components: {EditForm},
    data () {
      return {
        staff: []
      }
    },
    mounted () {
      this.loadStaff()
    },
    computed: {
      tableHeight () {
        return window.innerHeight - 320
      }
    },
    methods: {
      deleteStaff (id) {
        this.$confirm('此操作将永久删除该人员, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
            this.$axios
              .post('/admin/content/books/delete', {id: id}).then(resp => {
              if (resp && resp.data.code === 200) {
                this.loadStaff()
              }
            })
          }
        ).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
      },
      editStaff (item) {
        this.$refs.edit.dialogFormVisible = true
        this.$refs.edit.form = {
          id: this.id,
          name: this.name,
          staffid: this.staffid,
          staffcol: this.staffcol,
          email: this.email,
          telnumber: this.telnumber
        }
        // this.$refs.edit.category = {
        //   id: item.category.id.toString()
        // }
      },
      loadStaff () {
        var _this = this
        this.$axios.get('/staff').then(resp => {
          if (resp && resp.data.code === 200) {
            _this.books = resp.data.result
          }
        })
      }
    }
  }
</script>

<style scoped>
</style>
