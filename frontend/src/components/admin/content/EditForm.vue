<template>
  <div style="text-align: left">
    <el-button class="add-button" type="success" @click="dialogFormVisible = true">添加人员</el-button>
    <el-dialog
      title="添加/修改人员"
      :visible.sync="dialogFormVisible"
      @close="clear">
      <el-form v-model="form" style="text-align: left" ref="dataForm">
        <el-form-item label="姓名" :label-width="formLabelWidth" prop="name">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="编号" :label-width="formLabelWidth" prop="staffid">
          <el-input v-model="form.staffid" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="职工单位" :label-width="formLabelWidth" prop="staffcol">
          <el-input v-model="form.staffcol" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" :label-width="formLabelWidth" prop="email">
          <el-input v-model="form.email" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="电话号码" :label-width="formLabelWidth" prop="telnumber">
          <el-input v-model="form.telnumber" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item prop="id" style="height: 0">
          <el-input type="hidden" v-model="form.id" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="onSubmit">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import fileUpload from './fileUpload'
  export default {
    name: 'EditForm',
    components: {fileUpload},
    data () {
      return {
        dialogFormVisible: false,
        form: {
          id: '',
          name: '',
          staffid: '',
          staffcol: '',
          email: '',
          telnumber: ''
        },
        formLabelWidth: '120px'
      }
    },
    methods: {
      clear () {
        this.$refs.imgUpload.clear()
        this.form = {
          id: '',
          name: '',
          staffid: '',
          staffcol: '',
          email: '',
          telnumber: ''
        }
      },
      onSubmit () {
        this.$axios
          .post('/admin/content/drugs', {
            id: this.id,
            name: this.name,
            staffid: this.staffid,
            staffcol: this.staffcol,
            email: this.email,
            telnumber: this.telnumber
          }).then(resp => {
            if (resp && resp.data.code === 200) {
              this.dialogFormVisible = false
              this.$emit('onSubmit')
            }
        })
      },
      uploadImg () {
        this.form.cover = this.$refs.imgUpload.url
      }
    }
  }
</script>

<style scoped>
  .add-button {
    margin: 18px 0 0 10px;
  }
</style>
