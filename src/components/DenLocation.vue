<template>
  <div class="hello">
    <img class='den' :style="{left: position.x + 'px', top: position.y + 'px'}" :src="gmax ? gmaxImg : dmaxImg">
  </div>
</template>

<script>
const dmaxImg = require('../assets/dmax.png')
const gmaxImg = require('../assets/gmax.png')

export default {
  name: 'DenLocation',
  data() {
    return {
      dmaxImg, gmaxImg,
    }
  },
  props: {
    position: Object,
    pokemon: Array,
    gmax: Boolean,
  },
}
</script>

<style scoped>
.den {
  position: absolute;
}
</style>
