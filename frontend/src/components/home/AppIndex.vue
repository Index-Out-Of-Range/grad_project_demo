<template>
  <div>
    <div>
      <div>
        <form class="search__form" action="" style="margin-top: 8%;">
          <input
            class="search__input"
            :placeholder="$t('message.home.input_tip')"
            autocapitalize="off"
            spellcheck="false"
          />
        </form>
        <span class="search__info"
          >{{ $t('message.home.search_example') }}:&nbsp;&nbsp;
          <a href="/#">#1</a> <a href="/#">#2</a> <a href="/#">#3</a>
          <a href="/#">#4</a></span
        >
      </div>

      <div style="margin-top:5%;">
        <el-button type="primary" icon="el-icon-search" round>{{
          $t('message.home.button')
        }}</el-button>
      </div>
    </div>

    <About id="home-about"></About>
  </div>
</template>

<script>
import About from '@/components/common/About'
export default {
  name: 'AppIndex',
  data() {
    return {
      input: ''
    }
  },
  components: { About }
}
</script>

<style scoped>
a:link {color:#3CB371;}      /* 未访问链接*/
a:visited {color:#3CB371;}  /* 已访问链接 */
a:hover {color:#3CB371;}  /* 鼠标移动到链接上 */
a:active {color:#3CB371;}  /* 鼠标点击时 */

.search__input {
  border: 0;
  background: transparent;
  border-radius: 0;
  -webkit-appearance: none;

  font-family: inherit;
  font-size: 4vw;
  line-height: 1;
  display: inline-block;
  box-sizing: border-box;
  width: 50%;
  padding: 0.05em 0;
  color: #060919;
  border-bottom: 2px solid;
  opacity: 0.3;
}

.search__input:focus {
  outline: none;
}

.search__info {
  font-size: 90%;
  font-weight: bold;
  display: block;
  width: 50%;
  margin: 0 auto;
  padding: 0.85em 0;
  text-align: right;
  color: #3CB371;
}

#home-about {
  position: absolute;
  bottom: 0;
  width: 100%;
}

.el-button--primary{
  color: #fff;
  background-color: #3CB371;
  border-color: #3CB371;
}
</style>
