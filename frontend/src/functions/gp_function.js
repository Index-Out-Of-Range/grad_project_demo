export default{
  install (Vue, options) {
    Vue.prototype.getData = function () {
      console.log('我是插件中的方法')
    }
    Vue.prototype.isNull = function (str) {
      if (str === '') return true
      var regu = '^[ ]+$'
      var re = new RegExp(regu)
      return re.test(str)
    }
    Vue.prototype.filterNoneStr = function (list) {
      for (let i = 0; i < list.length; i++) {
        if (list[i] === '') {
          list.splice(i, 1)
        }
      }
      return list
    }
  }
}
