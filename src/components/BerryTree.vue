<template>
  <div class='tree' :style="{left: position.x + 'px', top: position.y + 'px'}" @mouseenter="triggerHover()" @mouseleave="clearHover">
    <img @touchstart="toggleHover()" :src="found ? '/icons/tree.png' : '/icons/tree-notfound.png'" :style='{transform: found ? "scale(1.0)" : "scale(0.5)"}'>
    <v-container v-if='hover && treeBerries' class='tree-hover' fluid>
      <v-row style="justify-content: center;"><img :src='screenshotImg' width="80%"/></v-row>
      <v-row>
        <div class='tree-berries'>
          <a class='name' :href='treeInfo.link'>{{treeInfo.name}}</a>
          <div class='bt version'>Berries</div>
          <div class='btb pokemon-list'>
            <img v-for='(berryID, index) in treeBerries' :key='index' :src='`/sprites/${berryID}.png`' />
          </div>
          <div class='btt version'>Pokemon</div>
          <div class='btp pokemon-list'>
            <img v-for='(pokeID, index) in treePokemon' :key='index' :src='`/sprites/${pokeID}.png`' />
          </div>
        </div>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: 'BerryTree',
  data() {
    return {
      hover: false,
    }
  },
  props: {
    position: Object,
    treeBerries: Array,
    treePokemon: Array,
    treeInfo: Object,
    screenshotImg: String,
    searchIDs: Array,
  },
  methods: {
    triggerHover() {
      this.hover = true
    },
    clearHover(e) {
      if(e.relatedTarget && e.relatedTarget.tagName == "PINCH-ZOOM") {
        return
      }
      this.hover = false
    },
    toggleHover() {
      this.hover = !this.hover
    }
  },
  computed: {
    // NOTE: found doesn't search for the Pokemon found in this berry tree (eg. Skowvet, Greedent, Cherubi, etc.)
    // return true if we're not searching for berries
    found() {
      if (!this.searchIDs || this.searchIDs.length === 0) return true
      let searchingForBerry = false
      for (const i in this.searchIDs) {
        if (!this.searchIDs[i].endsWith('berry')) {
          continue
        }
        searchingForBerry = true
        if (this.treeBerries.berries.indexOf(this.searchIDs[i]) >= 0) {
            return true
          }
      }
      if (!searchingForBerry) return true
      return false
    }
  }
}
</script>

<style scoped>
.tree {
  position: absolute;
}
.tree-hover {
  background-color: #ffffff;
  position: relative;
  z-index: 100;
  overflow: visible;
  width: max-content;
}

.bt { background-color: #00d1f6; color: #002b33; }
.btb { background-color: #ccf7ff; }

.btt { background-color: #9e2306; color: #190501; }
.btp { background-color: #fdd6ce; }

.name {
  justify-self: center;
  color: #000;
  font-weight: 600;
  padding-bottom: 10px;
}
.version {
  line-height: 100%;
  font-weight: 600;
  padding: 10px;
}
.tree-berries {
  background-color: #ffffff;
  padding: 5px;
  display: grid;
  grid-template:
    "name" 1fr
    "bt btb" auto
    "btt btp" auto / 1fr 5fr;
}
.pokemon-list {
  display: grid;
  grid: repeat(2, 50px) / auto-flow 60px;
}
</style>
