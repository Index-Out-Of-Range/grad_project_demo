<template>
  <div class="single_gp_search">
    <el-row type="flex">
      <SideBar :side_bar_index="side_bar_index"></SideBar>
      <div style="width: 80%; margin-left: 5%;">
        <div style="text-align : left; font-size: 2em; color:#3CB371; font-weight:bold; margin-bottom: 2%;">
          {{ $t('message.search.predict') }}
        </div>
        <div style="text-align : center; background: white; display:flex; flex-direction:column; color:#808080;">
          <div style="font-size: 1.5em; padding: 2% 0;">
            {{ $t('message.search.title.title3') }}
          </div>
          <el-divider></el-divider>
          <div v-if="start_predicting">
            <el-progress type="circle" :percentage="predicting_percentage" :color="customColorMethod" style="padding: 4% 0;"></el-progress>
            <div style="padding-bottom: 4%; font-size: 20px; font-weight:bold;">
              <div v-if="predicting_percentage===100"> {{ $t('message.message_tip.predict_complete_tip')}}</div>
              <div v-else>{{ $t('message.message_tip.predicting_tip')}}</div>
            </div>
            <div style="padding-bottom: 4%;">
              <el-button round type="primary" icon="el-icon-back" @click="goBack">返回</el-button>
              <el-button round type="primary" icon="el-icon-download" :disabled="!predicting_complete" @click="downloadPredictFile">下载结果</el-button>
            </div>
          </div>
          <div v-else>
            <div style="margin: 4% 0;">
              <div>
                <el-upload drag action="#" ref="upload" :on-change="fileChange" :limit="1" :auto-upload="false" :multiple="false" :file-list="file_list" :before-upload="onBeforeUpload" :on-success="onSuccessUpload" :on-exceed="onFileExceed" :on-error="onError">
                  <i class="el-icon-upload"></i>
                  <div class="el-upload__text">
                    {{ $t('message.search.upload_tip.tip1')}}
                    <em>{{ $t('message.search.upload_tip.tip2') }}</em>
                  </div>
                  <div class="el-upload__tip" slot="tip">
                    {{ $t('message.search.upload_tip.tip3') }}
                  </div>
                </el-upload>
              </div>
              <div style="margin-top:5%;">
                <el-button type="primary" icon="el-icon-upload2" round @click="submitUpload">
                  {{$t('message.search.upload')}}
                </el-button>
                <el-button type="primary" icon="el-icon-search" round @click="predictFile">
                  {{$t('message.search.predict')}}
                </el-button>
              </div>
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
      side_bar_index: '/gp_upload_file',
      file_list: [],
      form: {
        file: ''
      },
      upload_file_path: '',
      start_predicting: false,
      predicting_complete: false,
      predicting_percentage: 0,
      process_key: '',
      my_interval: '',
      result_file_path: ''
    }
  },
  components: { SideBar },
  watch: {
    predicting_percentage: function (newval, oldval) {
      console.log(newval, oldval)
      // 当返回的新值为成功的时候,关闭定时器,结束轮询
      if (newval === 100) {
        clearInterval(this.my_interval)
        this.getResultFilePath()
      }
      // 当页面关闭的时候,结束轮询,否则就会一直发请求,
      // 使用$once(eventName, eventHandler)一次性监听事件
      this.$once('hook:boforeDestory', () => {
        clearInterval(this.my_interval)
      })
    }
  },
  methods: {
    fileChange(file, fileList) {
      // console.log('change')
      // console.log(file)
      this.form.file = file.raw
      this.file_list = fileList
      // console.log(this.form.file)
      // console.log(fileList)
      // console.log(this.file_list.length)
    },
    onBeforeUpload(file) {
      console.log('before upload')
      console.log(file)
      let extension = file.name.substring(file.name.lastIndexOf('.') + 1)
      if (extension !== 'mat') {
        this.$message({
          type: 'warning',
          message: this.$t('message.message_tip.file_type_tip')
        })
      }
    },
    onSuccessUpload(res, file, fileList) {
      this.$message({
        message: this.$t('message.message_tip.file_upload_success_tip'),
        type: 'success'
      })
    },
    onFileExceed(files, fileList) {
      this.$message({
        type: 'warning',
        message: this.$t('message.message_tip.file_num_tip')
      })
    },
    onError() {
      this.$message.error(this.$t('message.message_tip.file_upload_fail_tip'))
    },
    submitUpload() {
      if (this.file_list.length === 0) {
        this.$message({ type: 'warning', message: this.$t('message.message_tip.select_file_tip') })
        return
      }
      let headers = { headers: { 'Content-Type': 'multipart/form-data' } }
      let formData = new FormData()
      formData.append('file', this.form.file)
      this.$axios.post('http://127.0.0.1:8000/api/upload_mat_file',
        formData, headers
      ).then(res => {
        console.log(res)
        if (res.status === 200) {
          this.upload_file_path = res.data.file_path
          this.$message({
            message: this.$t('message.message_tip.file_upload_success_tip'),
            type: 'success'
          })
        } else {
          this.$message.error(this.$t('message.message_tip.file_upload_fail_tip'))
          console.log(res.data.msg)
        }
      }).catch(error => console.log(error))
    },
    predictFile() {
      if (this.upload_file_path === '') {
        this.$message({
          type: 'warning',
          message: this.$t('message.message_tip.upload_file_tip')
        })
        return
      }
      this.start_predicting = true
      const random = require('string-random')
      this.process_key = random(16)
      console.log(this.process_key)
      this.$axios.get('http://127.0.0.1:8000/api/predict_file', {
        params: { upload_file_path: this.upload_file_path, process_key: this.process_key }
      }).then(res => {
        console.log(res)
        if (res.status === 200) {
          this.my_interval = window.setInterval(() => { setTimeout(() => { this.getProcess() }, 1) }, 2000)
        } else {
          this.$message.error(this.$t('message.message_tip.predict_file_fail_tip'))
          console.log(res.data.msg)
        }
      }).catch(error => console.log(error))
    },
    customColorMethod() {
      if (this.predicting_percentage < 20) {
        return '#f56c6c'
      } else if (this.predicting_percentage < 40) {
        return '#e6a23c'
      } else if (this.predicting_percentage < 60) {
        return '#1989fa'
      } else if (this.predicting_percentage < 80) {
        return '#6f7ad3'
      } else {
        return '#3cb371'
      }
    },
    downloadPredictFile() {
      console.log('Start download!')
      const qs = require('qs')
      let postData = qs.stringify({
        file_path: this.result_file_path
      })
      this.$axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/api/download_file',
        data: postData
      }).then(res => {
        console.log(res)
        if (res.status === 200) {
          if (!res.data) {
            return
          }
          let url = window.URL.createObjectURL(new Blob([res.data]))
          let a = document.createElement('a')
          a.style.display = 'none'
          a.href = url
          let temp_arr = this.result_file_path.split('/')
          console.log(String(temp_arr[temp_arr.length - 1]))
          a.setAttribute('download', String(temp_arr[temp_arr.length - 1]))
          document.body.appendChild(a)
          a.click()
          window.URL.revokeObjectURL(a.href)
          document.body.removeChild(a)
        } else {
          this.$message.error(this.$t('message.message_tip.download_file_fail_tip'))
          console.log(res.data.msg)
        }
      }).catch(error => console.log(error))
    },
    goBack() {
      this.start_predicting = false
      this.my_interval = ''
      this.result_file_path = ''
      this.predicting_complete = false
      this.upload_file_path = ''
      this.file_list = []
      this.form = { file: '' }
      this.upload_file_path = ''
      this.predicting_percentage = 0
      this.process_key = ''
    },
    getProcess() {
      this.$axios.get('http://127.0.0.1:8000/api/predict_process', {
        params: { process_key: this.process_key }
      }).then(res => {
        console.log(res)
        if (res.status === 200) {
          let process = res.data.process
          this.predicting_percentage = process
          console.log(process)
        } else {
          this.$message.error(this.$t('message.message_tip.get_process_fail_tip'))
          console.log(res.data.msg)
        }
      }).catch(error => console.log(error))
    },
    getResultFilePath() {
      this.$axios.get('http://127.0.0.1:8000/api/get_result_file_path', {
        params: { process_key: this.process_key }
      }).then(res => {
        console.log(res)
        if (res.status === 200) {
          let result_file_path = res.data.result_file_path
          this.result_file_path = result_file_path
          console.log(result_file_path)
          this.predicting_complete = true
        } else {
          this.$message.error(this.$t('message.message_tip.get_file_link_tip'))
          console.log(res.data.msg)
        }
      }).catch(error => console.log(error))
    }
  },
  destroyed() {
    clearInterval(this.my_interval)
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
