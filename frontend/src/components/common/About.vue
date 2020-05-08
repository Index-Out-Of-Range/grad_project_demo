<template>
  <div
    style="background:#212523; height:10%; color:#999; display:flex; align-items: center; justify-content:center;"
  >
    <div
      style="display:flex; justify-content: space-between; width: 100%; padding:0 20%;"
    >
      <a>{{ $t('message.home.down_menu.reference') }}</a>
      <a>{{ $t('message.home.down_menu.contributor') }}</a>
      <a>{{ $t('message.home.down_menu.statistics') }}</a>
      <a>{{ $t('message.home.down_menu.data_source') }}</a>
      <a>{{ $t('message.home.down_menu.faq') }}</a>
      <a>{{ $t('message.home.down_menu.api') }}</a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>

</style>
