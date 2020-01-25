<template>
  <div id="app">
    <div id='searchBar'>
      <v-autocomplete
        attach='#searchBar'
        v-model='searchIDs'
        :items='allPokemon'
        chips clearable hide-details hide-selected multiple solo
        item-text='name'
        item-value='id'
        label='Search for a Pokemon...'
        ref='searchMenu'
      >
        <template v-slot:selection='{ attr, on, item, selected }'>
          <v-chip
            v-bind='attr'
            :input-value='selected'
            color='blue-grey'
            class='white--text'
            close
            @click:close='remove(item)'
            v-on='on'
          >
            <img :src='`/sprites/${item.id}.png`' />
            <span v-text='item.name'></span>
          </v-chip>
        </template>
        <template v-slot:item='{ item }'>
          <v-list-item-avatar
            color='indigo'
            class='headline font-weight-light white--text'
          >
            <img :src='`/sprites/${item.id}.png`' />
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title v-text='item.name'></v-list-item-title>
            <v-list-item-subtitle v-text='item.id'></v-list-item-subtitle>
          </v-list-item-content>
        </template>
      </v-autocomplete>
    </div>
    <div id='controls'>
      <v-row justify='center' no-gutters>
        <v-col cols='6' lg='12'><v-card class='cardBtn' tile @click='reset'>RECENTER</v-card></v-col>
        <v-col cols='3' lg='6'><v-card class='cardBtn' tile @click='scaleDown'>-</v-card></v-col>
        <v-col cols='3' lg='6'><v-card class='cardBtn' tile @click='scaleUp'>+</v-card></v-col>
      </v-row>
    </div>
    <Moveable v-bind='moveable' @drag='handleDrag' @scale='handlePinchScale' ref='moveableTarget'>
      <div id='wild-area-map' ref='wildAreaMap'>
        <img alt="Pokemon Wild Area Map" src="./assets/pokemon-wild-area.png" @touchstart='closeSearchMenu'>
        <DenLocation v-for="(den, index) in dens" :key="index"
          :position='den.position'
          :commonDen='denPokemon[den.commonID]'
          :rareDen='denPokemon[den.rareID]'
          :gmax='denPokemon[den.rareID] && (denPokemon[den.commonID].gmax || denPokemon[den.rareID].gmax)'
          :screenshotImg='den.img'
          :searchIDs='searchIDs'
          ref='denLocationElement'/>
      </div>
    </Moveable>
    <v-footer id='footer'>
      <v-icon left>mdi-information</v-icon>
      <span>Credits: <a href='https://www.youtube.com/channel/UC7tKYiFtH_6HCBD4hh7hTWw'>preethamrn</a>, <a href='https://reddit.com/u/malixx92'>/u/Malixx92</a>, <a href='https://www.serebii.net/swordshield/maxraidbattledens.shtml'>Serebii</a></span>
    </v-footer>
  </div>
</template>

<script>
/* eslint-disable no-param-reassign,no-unused-expressions,no-unused-vars,no-console */
import Moveable from 'vue-moveable'
import DenLocation from './components/DenLocation.vue'

export default {
  name: 'app',
  components: {
    DenLocation,
    Moveable,
  },
  data() {
    return {
      // support dragging map
      moveable: {
        draggable: true,
        pinchable: ['scalable'],
      },
      currentScale: 1.0,
      resetScale: 'scale(1.0)',
      resetTranslate: '',

      // Pokemon searching
      searchIDs: [],

      // den data (immutable)
      dens: [
        {location: "Axew's Eye", img: "https://www.serebii.net/swordshield/den/th/axew'seye-1.jpg", commonID: 38, rareID: 64, position: {x: 706, y: 1503}},
        {location: 'Bridge Field', img: 'https://www.serebii.net/swordshield/den/th/bridgefield-1.jpg', commonID: 16, rareID: 52, position: {x: 930, y: 1044}},
        {location: 'Bridge Field', img: 'https://www.serebii.net/swordshield/den/th/bridgefield-2.jpg', commonID: 13, rareID: 87, position: {x: 815, y: 1004}},
        {location: 'Bridge Field', img: 'https://www.serebii.net/swordshield/den/th/bridgefield-3.jpg', commonID: 27, rareID: 59, position: {x: 873, y: 963}},
        {location: 'Bridge Field', img: 'https://www.serebii.net/swordshield/den/th/bridgefield-4.jpg', commonID: 8, rareID: 44, position: {x: 1044, y: 919}},
        {location: 'Bridge Field', img: 'https://www.serebii.net/swordshield/den/th/bridgefield-5.jpg', commonID: 36, rareID: 63, position: {x: 980, y: 880}},
        {location: 'Bridge Field', img: 'https://www.serebii.net/swordshield/den/th/bridgefield-6.jpg', commonID: 4, rareID: 92, position: {x: 1116, y: 873}},
        {location: 'Bridge Field', img: 'https://www.serebii.net/swordshield/den/th/bridgefield-7.jpg', commonID: 5, rareID: 46, position: {x: 1265, y: 825}},
        {location: 'Bridge Field', img: 'https://www.serebii.net/swordshield/den/th/bridgefield-8.jpg', commonID: 40, rareID: 65, position: {x: 854, y: 892}},
        {location: 'Bridge Field', img: 'https://www.serebii.net/swordshield/den/th/bridgefield-9.jpg', commonID: 34, rareID: 82, position: {x: 645, y: 898}},
        {location: 'Dappled Grove', img: 'https://www.serebii.net/swordshield/den/th/dappledgrove-1.jpg', commonID: 26, rareID: 59, position: {x: 243, y: 1676}},
        {location: 'Dappled Grove', img: 'https://www.serebii.net/swordshield/den/th/dappledgrove-2.jpg', commonID: 4, rareID: 92, position: {x: 195, y: 1611}},
        {location: 'Dappled Grove', img: 'https://www.serebii.net/swordshield/den/th/dappledgrove-3.jpg', commonID: 26, rareID: 59, position: {x: 265, y: 1582}},
        {location: 'Dappled Grove', img: 'https://www.serebii.net/swordshield/den/th/dappledgrove-4.jpg', commonID: 26, rareID: 58, position: {x: 160, y: 1538}},
        {location: 'Dappled Grove', img: 'https://www.serebii.net/swordshield/den/th/dappledgrove-5.jpg', commonID: 28, rareID: 79, position: {x: 157, y: 1500}},
        {location: 'Dusty Bowl', img: 'https://www.serebii.net/swordshield/den/th/dustybowl-1.jpg', commonID: 10, rareID: 48, position: {x: 990, y: 545}},
        {location: 'Dusty Bowl', img: 'https://www.serebii.net/swordshield/den/th/dustybowl-2.jpg', commonID: 36, rareID: 88, position: {x: 880, y: 503}},
        {location: 'Dusty Bowl', img: 'https://www.serebii.net/swordshield/den/th/dustybowl-3.jpg', commonID: 17, rareID: 93, position: {x: 1045, y: 455}},
        {location: 'Dusty Bowl', img: 'https://www.serebii.net/swordshield/den/th/dustybowl-4.jpg', commonID: 11, rareID: 49, position: {x: 892, y: 330}},
        {location: 'Dusty Bowl', img: 'https://www.serebii.net/swordshield/den/th/dustybowl-5.jpg', commonID: 9, rareID: 75, position: {x: 1000, y: 354}},
        {location: 'Dusty Bowl', img: 'https://www.serebii.net/swordshield/den/th/dustybowl-6.jpg', commonID: 21, rareID: 55, position: {x: 1118, y: 348}},
        {location: 'Dusty Bowl', img: 'https://www.serebii.net/swordshield/den/th/dustybowl-7.jpg', commonID: 20, rareID: 54, position: {x: 1172, y: 377}},
        {location: 'Dusty Bowl', img: 'https://www.serebii.net/swordshield/den/th/dustybowl-8.jpg', commonID: 17, rareID: 52, position: {x: 1167, y: 302}},
        {location: 'Dusty Bowl', img: 'https://www.serebii.net/swordshield/den/th/dustybowl-9.jpg', commonID: 15, rareID: 93, position: {x: 1271, y: 278}},
        {location: 'East Lake Axewell', img: 'https://www.serebii.net/swordshield/den/th/eastlakeaxewell-1.jpg', commonID: 39, rareID: 65, position: {x: 652, y: 1329}},
        {location: 'East Lake Axewell', img: 'https://www.serebii.net/swordshield/den/th/eastlakeaxewell-2.jpg', commonID: 31, rareID: 61, position: {x: 724, y: 1363}},
        {location: 'East Lake Axewell', img: 'https://www.serebii.net/swordshield/den/th/eastlakeaxewell-3.jpg', commonID: 29, rareID: 86, position: {x: 810, y: 1262}},
        {location: 'East Lake Axewell', img: 'https://www.serebii.net/swordshield/den/th/eastlakeaxewell-4.jpg', commonID: 31, rareID: 61, position: {x: 815, y: 1514}},
        {location: 'East Lake Axewell', img: 'https://www.serebii.net/swordshield/den/th/eastlakeaxewell-5.jpg', commonID: 7, rareID: 44, position: {x: 764, y: 1651}},
        {location: "Giant's Cap", img: "https://www.serebii.net/swordshield/den/th/giant'scap-1.jpg", commonID: 32, rareID: 89, position: {x: 836, y: 261}},
        {location: "Giant's Cap", img: "https://www.serebii.net/swordshield/den/th/giant'scap-2.jpg", commonID: 24, rareID: 78, position: {x: 728, y: 311}},
        {location: "Giant's Cap", img: "https://www.serebii.net/swordshield/den/th/giant'scap-3.jpg", commonID: 23, rareID: 55, position: {x: 753, y: 415}},
        {location: "Giant's Cap", img: "https://www.serebii.net/swordshield/den/th/giant'scap-4.jpg", commonID: 18, rareID: 71, position: {x: 804, y: 534}},
        {location: "Giant's Cap", img: "https://www.serebii.net/swordshield/den/th/giant'scap-5.jpg", commonID: 30, rareID: 60, position: {x: 732, y: 572}},
        {location: "Giant's Mirror", img: "https://www.serebii.net/swordshield/den/th/giant'smirror-1.jpg", commonID: 28, rareID: 43, position: {x: 1169, y: 476}},
        {location: "Giant's Mirror", img: "https://www.serebii.net/swordshield/den/th/giant'smirror-2.jpg", commonID: 42, rareID: 67, position: {x: 1293, y: 462}},
        {location: "Giant's Mirror", img: "https://www.serebii.net/swordshield/den/th/giant'smirror-3.jpg", commonID: 25, rareID: 72, position: {x: 1372, y: 384}},
        {location: "Giant's Mirror", img: "https://www.serebii.net/swordshield/den/th/giant'smirror-4.jpg", commonID: 36, rareID: 69, position: {x: 1434, y: 325}},
        {location: "Giant's Mirror", img: "https://www.serebii.net/swordshield/den/th/giant'smirror-5.jpg", commonID: 27, rareID: 70, position: {x: 1434, y: 246}},
        {location: "Giant's Seat", img: "https://www.serebii.net/swordshield/den/th/giant'sseat-1.jpg", commonID: 11, rareID: 84, position: {x: 1244, y: 1441}},
        {location: "Giant's Seat", img: "https://www.serebii.net/swordshield/den/th/giant'sseat-2.jpg", commonID: 11, rareID: 49, position: {x: 1248, y: 1536}},
        {location: "Giant's Seat", img: "https://www.serebii.net/swordshield/den/th/giant'sseat-3.jpg", commonID: 12, rareID: 45, position: {x: 1132, y: 1569}},
        {location: "Giant's Seat", img: "https://www.serebii.net/swordshield/den/th/giant'sseat-4.jpg", commonID: 15, rareID: 51, position: {x: 1222, y: 1685}},
        {location: "Giant's Seat", img: "https://www.serebii.net/swordshield/den/th/giant'sseat-5.jpg", commonID: 15, rareID: 83, position: {x: 1135, y: 1721}},
        {location: 'Hammerlocke Hills', img: 'https://www.serebii.net/swordshield/den/th/hammerlockehills-1.jpg', commonID: 14, rareID: 68, position: {x: 1298, y: 204}},
        {location: 'Hammerlocke Hills', img: 'https://www.serebii.net/swordshield/den/th/hammerlockehills-2.jpg', commonID: 12, rareID: 45, position: {x: 1173, y: 98}},
        {location: 'Hammerlocke Hills', img: 'https://www.serebii.net/swordshield/den/th/hammerlockehills-3.jpg', commonID: 32, rareID: 61, position: {x: 1130, y: 213}},
        {location: 'Hammerlocke Hills', img: 'https://www.serebii.net/swordshield/den/th/hammerlockehills-4.jpg', commonID: 19, rareID: 53, position: {x: 1024, y: 270}},
        {location: 'Hammerlocke Hills', img: 'https://www.serebii.net/swordshield/den/th/hammerlockehills-5.jpg', commonID: 33, rareID: 62, position: {x: 933, y: 179}},
        {location: 'Hammerlocke Hills', img: 'https://www.serebii.net/swordshield/den/th/hammerlockehills-6.jpg', commonID: 30, rareID: 57, position: {x: 918, y: 108}},
        {location: 'Hammerlocke Hills', img: 'https://www.serebii.net/swordshield/den/th/hammerlockehills-7.jpg', commonID: 23, rareID: 73, position: {x: 827, y: 160}},
        {location: 'Lake of Outrage', img: 'https://www.serebii.net/swordshield/den/th/lakeofoutrage-1.jpg', commonID: 25, rareID: 56, position: {x: 736, y: 199}},
        {location: 'Lake of Outrage', img: 'https://www.serebii.net/swordshield/den/th/lakeofoutrage-2.jpg', commonID: 8, rareID: 44, position: {x: 609, y: 325}},
        {location: 'Lake of Outrage', img: 'https://www.serebii.net/swordshield/den/th/lakeofoutrage-3.jpg', commonID: 18, rareID: 77, position: {x: 498, y: 263}},
        {location: 'Lake of Outrage', img: 'https://www.serebii.net/swordshield/den/th/lakeofoutrage-4.jpg', commonID: 34, rareID: 74, position: {x: 621, y: 203}},
        {location: 'Motostoke Riverbank', img: 'https://www.serebii.net/swordshield/den/th/motostokeriverbank-1.jpg', commonID: 40, rareID: 65, position: {x: 1009, y: 1207}},
        {location: 'Motostoke Riverbank', img: 'https://www.serebii.net/swordshield/den/th/motostokeriverbank-2.jpg', commonID: 24, rareID: 56, position: {x: 889, y: 1185}},
        {location: 'Motostoke Riverbank', img: 'https://www.serebii.net/swordshield/den/th/motostokeriverbank-3.jpg', commonID: 14, rareID: 50, position: {x: 1043, y: 1135}},
        {location: 'Motostoke Riverbank', img: 'https://www.serebii.net/swordshield/den/th/motostokeriverbank-4.jpg', commonID: 30, rareID: 60, position: {x: 814, y: 1105}},
        {location: 'North Lake Miloch', img: 'https://www.serebii.net/swordshield/den/th/northlakemiloch-1.jpg', commonID: 29, rareID: 60, position: {x: 1071, y: 1311}},
        {location: 'North Lake Miloch', img: 'https://www.serebii.net/swordshield/den/th/northlakemiloch-2.jpg', commonID: 10, rareID: 48, position: {x: 1115, y: 1384}},
        {location: 'North Lake Miloch', img: 'https://www.serebii.net/swordshield/den/th/northlakemiloch-3.jpg', commonID: 10, rareID: 48, position: {x: 1245, y: 1399}},
        {location: 'North Lake Miloch', img: 'https://www.serebii.net/swordshield/den/th/northlakemiloch-4.jpg', commonID: 29, rareID: 60, position: {x: 1247, y: 1283}},
        {location: 'North Lake Miloch', img: 'https://www.serebii.net/swordshield/den/th/northlakemiloch-5.jpg', commonID: 41, rareID: 76, position: {x: 905, y: 1416}},
        {location: 'North Lake Miloch', img: 'https://www.serebii.net/swordshield/den/th/northlakemiloch-6.jpg', commonID: 41, rareID: 76, position: {x: 817, y: 1369}},
        {location: 'Rolling Fields', img: 'https://www.serebii.net/swordshield/den/th/rollingfields-1.jpg', commonID: 33, rareID: 62, position: {x: 976, y: 1760}},
        {location: 'Rolling Fields', img: 'https://www.serebii.net/swordshield/den/th/rollingfields-2.jpg', commonID: 3, rareID: 51, position: {x: 894, y: 1775}},
        {location: 'Rolling Fields', img: 'https://www.serebii.net/swordshield/den/th/rollingfields-3.jpg', commonID: 4, rareID: 46, position: {x: 859, y: 1711}},
        {location: 'Rolling Fields', img: 'https://www.serebii.net/swordshield/den/th/rollingfields-4.jpg', commonID: 31, rareID: 90, position: {x: 840, y: 1641}},
        {location: 'Rolling Fields', img: 'https://www.serebii.net/swordshield/den/th/rollingfields-5.jpg', commonID: 39, rareID: 65, position: {x: 639, y: 1710}},
        {location: 'Rolling Fields', img: 'https://www.serebii.net/swordshield/den/th/rollingfields-6.jpg', commonID: 16, rareID: 52, position: {x: 547, y: 1741}},
        {location: 'Rolling Fields', img: 'https://www.serebii.net/swordshield/den/th/rollingfields-7.jpg', commonID: 37, rareID: 64, position: {x: 503, y: 1815}},
        {location: 'Rolling Fields', img: 'https://www.serebii.net/swordshield/den/th/rollingfields-8.jpg', commonID: 31, rareID: 90, position: {x: 427, y: 1676}},
        {location: 'Rolling Fields', img: 'https://www.serebii.net/swordshield/den/th/rollingfields-9.jpg', commonID: 1, rareID: 48, position: {x: 549, y: 1621}},
        {location: 'South Lake Miloch', img: 'https://www.serebii.net/swordshield/den/th/southlakemiloch-1.jpg', commonID: 5, rareID: 46, position: {x: 920, y: 1459}},
        {location: 'South Lake Miloch', img: 'https://www.serebii.net/swordshield/den/th/southlakemiloch-2.jpg', commonID: 1, rareID: 43, position: {x: 1018, y: 1425}},
        {location: 'South Lake Miloch', img: 'https://www.serebii.net/swordshield/den/th/southlakemiloch-3.jpg', commonID: 8, rareID: 91, position: {x: 942, y: 1529}},
        {location: 'South Lake Miloch', img: 'https://www.serebii.net/swordshield/den/th/southlakemiloch-4.jpg', commonID: 41, rareID: 76, position: {x: 979, y: 1701}},
        {location: 'South Lake Miloch', img: 'https://www.serebii.net/swordshield/den/th/southlakemiloch-5.jpg', commonID: 41, rareID: 76, position: {x: 1077, y: 1739}},
        {location: 'Stony Wilderness', img: 'https://www.serebii.net/swordshield/den/th/stonywilderness-1.jpg', commonID: 3, rareID: 51, position: {x: 785, y: 782}},
        {location: 'Stony Wilderness', img: 'https://www.serebii.net/swordshield/den/th/stonywilderness-2.jpg', commonID: 12, rareID: 85, position: {x: 1135, y: 725}},
        {location: 'Stony Wilderness', img: 'https://www.serebii.net/swordshield/den/th/stonywilderness-3.jpg', commonID: 40, rareID: 66, position: {x: 1272, y: 737}},
        {location: 'Stony Wilderness', img: 'https://www.serebii.net/swordshield/den/th/stonywilderness-4.jpg', commonID: 2, rareID: 50, position: {x: 887, y: 702}},
        {location: 'Stony Wilderness', img: 'https://www.serebii.net/swordshield/den/th/stonywilderness-5.jpg', commonID: 27, rareID: 59, position: {x: 999, y: 661}},
        {location: 'Stony Wilderness', img: 'https://www.serebii.net/swordshield/den/th/stonywilderness-6.jpg', commonID: 35, rareID: 63, position: {x: 1062, y: 633}},
        {location: 'Stony Wilderness', img: 'https://www.serebii.net/swordshield/den/th/stonywilderness-7.jpg', commonID: 22, rareID: 55, position: {x: 1177, y: 671}},
        {location: 'Stony Wilderness', img: 'https://www.serebii.net/swordshield/den/th/stonywilderness-8.jpg', commonID: 14, rareID: 50, position: {x: 1210, y: 689}},
        {location: 'Stony Wilderness', img: 'https://www.serebii.net/swordshield/den/th/stonywilderness-9.jpg', commonID: 18, rareID: 54, position: {x: 1210, y: 654}},
        {location: 'Stony Wilderness', img: 'https://www.serebii.net/swordshield/den/th/stonywilderness-10.jpg', commonID: 1, rareID: 81, position: {x: 1296, y: 603}},
        {location: 'Stony Wilderness', img: 'https://www.serebii.net/swordshield/den/th/stonywilderness-11.jpg', commonID: 6, rareID: 43, position: {x: 1342, y: 565}},
        {location: 'Stony Wilderness', img: 'https://www.serebii.net/swordshield/den/th/stonywilderness-12.jpg', commonID: 19, rareID: 80, position: {x: 1161, y: 564}},
        {location: 'Watchtower Ruins', img: 'https://www.serebii.net/swordshield/den/th/watchtowerruins-1.jpg', commonID: 2, rareID: 50, position: {x: 287, y: 1441}},
        {location: 'Watchtower Ruins', position: {x: 343, y: 1357}}, // empty den
        {location: 'Watchtower Ruins', img: 'https://www.serebii.net/swordshield/den/th/watchtowerruins-2.jpg', commonID: 6, rareID: 47, position: {x: 363, y: 1303}},
        {location: 'West Lake Axewell', img: 'https://www.serebii.net/swordshield/den/th/westlakeaxewell-1.jpg', commonID: 35, rareID: 63, position: {x: 484, y: 1250}},
        {location: 'West Lake Axewell', img: 'https://www.serebii.net/swordshield/den/th/westlakeaxewell-2.jpg', commonID: 9, rareID: 91, position: {x: 438, y: 1422}},
        {location: 'West Lake Axewell', img: 'https://www.serebii.net/swordshield/den/th/westlakeaxewell-3.jpg', commonID: 9, rareID: 75, position: {x: 527, y: 1434}},
        {location: 'West Lake Axewell', img: 'https://www.serebii.net/swordshield/den/th/westlakeaxewell-4.jpg', commonID: 9, rareID: 75, position: {x: 492, y: 1516}},
        {location: 'West Lake Axewell', img: 'https://www.serebii.net/swordshield/den/th/westlakeaxewell-5.jpg', commonID: 42, rareID: 44, position: {x: 473, y: 1620}},
        {location: 'West Lake Axewell', img: 'https://www.serebii.net/swordshield/den/th/westlakeaxewell-6.jpg', commonID: 7, rareID: 44, position: {x: 295, y: 1629}},
      ],
      denPokemon: {
        38: {name: 'Den 38', link: 'https://www.serebii.net/swordshield/maxraidbattles/den38.shtml', gmax: false, swordPokemon: ['714', '840', '782', '885', '714', '840', '886', '715', '783', '784', '841', '887'], shieldPokemon: ['714', '840', '704', '885', '714', '840', '886', '715', '705', '706', '842', '887']},
        64: {name: 'Den 64', link: 'https://www.serebii.net/swordshield/maxraidbattles/den64.shtml', gmax: false, swordPokemon: ['328', '840', '610', '782', '885', '611', '783', '776', '784', '886', '612', '887'], shieldPokemon: ['610', '840', '328', '704', '885', '329', '705', '780', '706', '886', '330', '887']},
        16: {name: 'Den 16', link: 'https://www.serebii.net/swordshield/maxraidbattles/den16.shtml', gmax: false, swordPokemon: ['050', '749', '290', '529', '095', '339', '208', '340', '660', '051', '530', '750'], shieldPokemon: ['050', '749', '290', '529', '095', '339', '208', '340', '660', '051', '530', '750']},
        52: {name: 'Den 52', link: 'https://www.serebii.net/swordshield/maxraidbattles/den52.shtml', gmax: false, swordPokemon: ['194', '339', '562-g', '622', '536', '195', '618-g', '623', '423-e', '537', '867', '464'], shieldPokemon: ['194', '339', '562-g', '622', '536', '195', '618-g', '623', '423-e', '537', '867', '464']},
        13: {name: 'Den 13', link: 'https://www.serebii.net/swordshield/maxraidbattles/den13.shtml', gmax: false, swordPokemon: ['439', '824', '177', '856', '825', '857', '561', '178', '876', '561', '826', '858'], shieldPokemon: ['439', '824', '177', '856', '077-g', '857', '561', '178', '876-f', '765', '078-g', '858']},
        87: {name: 'Den 87', link: 'https://www.serebii.net/swordshield/maxraidbattles/den87.shtml', gmax: true, swordPokemon: ['175', '684', '859', '280', '176', '860', '685', '868', '282', '861', '468', '858-gi'], shieldPokemon: ['175', '682', '859', '280', '176', '860', '683', '868', '282', '861', '468', '858-gi']},
        27: {name: 'Den 27', link: 'https://www.serebii.net/swordshield/maxraidbattles/den27.shtml', gmax: false, swordPokemon: ['406', '829', '546', '840', '420', '315', '597', '598', '421', '830', '547', '841'], shieldPokemon: ['406', '829', '546', '840', '420', '315', '597', '598', '421', '830', '547', '842']},
        59: {name: 'Den 59', link: 'https://www.serebii.net/swordshield/maxraidbattles/den59.shtml', gmax: false, swordPokemon: ['420', '273', '829', '546', '274', '755', '421', '756', '830', '547', '275', '781'], shieldPokemon: ['420', '270', '829', '546', '271', '755', '421', '756', '830', '547', '272', '781']},
        8: {name: 'Den 8', link: 'https://www.serebii.net/swordshield/maxraidbattles/den8.shtml', gmax: false, swordPokemon: ['833', '846', '422-e', '751', '320', '550', '746', '834', '847', '752', '423-e', '321'], shieldPokemon: ['833', '846', '422-e', '751', '320', '550', '746', '834', '847', '752', '423-e', '321']},
        44: {name: 'Den 44', link: 'https://www.serebii.net/swordshield/maxraidbattles/den44.shtml', gmax: false, swordPokemon: ['129', '349', '846', '833', '747', '550', '211', '748', '771', '130', '131', '350'], shieldPokemon: ['129', '349', '846', '833', '747', '550', '211', '748', '771', '130', '131', '350']},
        36: {name: 'Den 36', link: 'https://www.serebii.net/swordshield/maxraidbattles/den36.shtml', gmax: false, swordPokemon: ['827', '263-g', '509', '859', '633', '828', '264-g', '860', '861', '634', '862', '635'], shieldPokemon: ['827', '263-g', '509', '859', '629', '828', '264-g', '860', '861', '630', '862', '248']},
        63: {name: 'Den 63', link: 'https://www.serebii.net/swordshield/maxraidbattles/den63.shtml', gmax: false, swordPokemon: ['827', '263-g', '559', '215', '510', '264-g', '828', '675', '461', '560', '862', '635'], shieldPokemon: ['827', '263-g', '629', '215', '510', '264-g', '828', '675', '461', '630', '862', '248']},
        4: {name: 'Den 4', link: 'https://www.serebii.net/swordshield/maxraidbattles/den4.shtml', gmax: false, swordPokemon: ['010', '736', '290', '595', '011', '632', '737', '291', '012', '596', '738', '632'], shieldPokemon: ['010', '736', '290', '595', '632', '011', '737', '291', '012', '596', '738', '632']},
        92: {name: 'Den 92', link: 'https://www.serebii.net/swordshield/maxraidbattles/den92.shtml', gmax: true, swordPokemon: ['767', '824', '588', '751', '616', '557', '825', '826', '752', '768', '589', '826-gi'], shieldPokemon: ['767', '824', '616', '751', '588', '557', '825', '826', '752', '768', '617', '826-gi']},
        5: {name: 'Den 5', link: 'https://www.serebii.net/swordshield/maxraidbattles/den5.shtml', gmax: false, swordPokemon: ['010', '415', '742', '824', '595', '011', '825', '596', '012', '743', '416', '826'], shieldPokemon: ['010', '415', '742', '824', '595', '011', '825', '596', '012', '743', '416', '826']},
        46: {name: 'Den 46', link: 'https://www.serebii.net/swordshield/maxraidbattles/den46.shtml', gmax: false, swordPokemon: ['767', '824', '588', '751', '616', '557', '825', '826', '752', '768', '589', '292'], shieldPokemon: ['767', '824', '616', '751', '588', '557', '825', '826', '752', '768', '617', '292']},
        40: {name: 'Den 40', link: 'https://www.serebii.net/swordshield/maxraidbattles/den40.shtml', gmax: false, swordPokemon: ['819', '831', '263-g', '446', '876', '820', '264-g', '820', '832', '660', '628', '143'], shieldPokemon: ['819', '831', '263-g', '446', '876-f', '820', '264-g', '820', '832', '660', '765', '143']},
        65: {name: 'Den 65', link: 'https://www.serebii.net/swordshield/maxraidbattles/den65.shtml', gmax: false, swordPokemon: ['659', '519', '819', '133', '520', '831', '521', '832', '628', '876', '133', '143'], shieldPokemon: ['659', '519', '819', '133', '520', '831', '521', '832', '765', '876-f', '133', '143']},
        34: {name: 'Den 34', link: 'https://www.serebii.net/swordshield/maxraidbattles/den34.shtml', gmax: false, swordPokemon: ['439', '868', '859', '280', '035', '281', '860', '036', '282', '869', '303', '861'], shieldPokemon: ['439', '868', '859', '280', '035', '281', '860', '036', '282', '869', '078-g', '861']},
        82: {name: 'Den 82', link: 'https://www.serebii.net/swordshield/maxraidbattles/den82.shtml', gmax: true, swordPokemon: ['175', '755', '859', '280', '176', '756', '860', '303', '282', '468', '861', '869-gi'], shieldPokemon: ['175', '077-g', '859', '280', '176', '756', '860', '078-g', '282', '468', '861', '869-gi']},
        26: {name: 'Den 26', link: 'https://www.serebii.net/swordshield/maxraidbattles/den26.shtml', gmax: false, swordPokemon: ['406', '273', '761', '043', '274', '315', '044', '762', '275', '763', '045', '182'], shieldPokemon: ['406', '270', '761', '043', '271', '315', '044', '762', '272', '763', '045', '182']},
        58: {name: 'Den 58', link: 'https://www.serebii.net/swordshield/maxraidbattles/den58.shtml', gmax: false, swordPokemon: ['406', '273', '829', '597', '274', '840', '315', '275', '830', '598', '407', '841'], shieldPokemon: ['406', '270', '829', '597', '271', '840', '315', '272', '830', '598', '407', '842']},
        28: {name: 'Den 28', link: 'https://www.serebii.net/swordshield/maxraidbattles/den28.shtml', gmax: false, swordPokemon: ['710', '708', '710', '755', '710', '315', '756', '556', '709', '711', '781', '710'], shieldPokemon: ['710', '708', '710', '755', '710', '315', '756', '556', '709', '711', '781', '710']},
        79: {name: 'Den 79', link: 'https://www.serebii.net/swordshield/maxraidbattles/den79.shtml', gmax: true, swordPokemon: ['406', '273', '829', '597', '274', '840', '315', '275', '830', '598', '407', '841-gi'], shieldPokemon: ['406', '270', '829', '597', '271', '840', '315', '272', '830', '598', '407', '842-gi']},
        10: {name: 'Den 10', link: 'https://www.serebii.net/swordshield/maxraidbattles/den10.shtml', gmax: false, swordPokemon: ['236', '759', '852', '674', '083-g', '539', '760', '675', '701', '865', '853', '870'], shieldPokemon: ['236', '759', '852', '674', '759', '538', '760', '675', '701', '760', '853', '870']},
        48: {name: 'Den 48', link: 'https://www.serebii.net/swordshield/maxraidbattles/den48.shtml', gmax: false, swordPokemon: ['447', '066', '559', '759', '760', '870', '067', '560', '068', '766', '448', '475'], shieldPokemon: ['447', '066', '453', '759', '760', '870', '067', '454', '068', '701', '448', '475']},
        88: {name: 'Den 88', link: 'https://www.serebii.net/swordshield/maxraidbattles/den88.shtml', gmax: true, swordPokemon: ['827', '263-g', '559', '859', '510', '264-g', '860', '828', '675', '560', '635', '861-gi'], shieldPokemon: ['827', '263-g', '629', '859', '510', '264-g', '860', '828', '675', '630', '248', '861-gi']},
        17: {name: 'Den 17', link: 'https://www.serebii.net/swordshield/maxraidbattles/den17.shtml', gmax: false, swordPokemon: ['843', '562-g', '449', '220', '328', '221', '329', '618-g', '867', '450', '330', '844'], shieldPokemon: ['843', '562-g', '449', '328', '220', '221', '618-g', '329', '867', '330', '450', '844']},
        93: {name: 'Den 93', link: 'https://www.serebii.net/swordshield/maxraidbattles/den93.shtml', gmax: true, swordPokemon: ['194', '339', '562-g', '622', '536', '195', '618-g', '623', '423-e', '537', '464', '844-gi'], shieldPokemon: ['194', '339', '562-g', '622', '536', '195', '618-g', '623', '423-e', '537', '464', '844-gi']},
        11: {name: 'Den 11', link: 'https://www.serebii.net/swordshield/maxraidbattles/den11.shtml', gmax: false, swordPokemon: ['599', '052-g', '436', '597', '624', '878', '600', '863', '437', '625', '601', '879'], shieldPokemon: ['599', '052-g', '436', '597', '624', '878', '600', '863', '437', '625', '601', '879']},
        49: {name: 'Den 49', link: 'https://www.serebii.net/swordshield/maxraidbattles/den49.shtml', gmax: false, swordPokemon: ['052-g', '436', '624', '597', '679', '437', '863', '598', '625', '618-g', '879', '884'], shieldPokemon: ['052-g', '436', '624', '597', '679', '437', '863', '598', '625', '618-g', '879', '884']},
        9: {name: 'Den 9', link: 'https://www.serebii.net/swordshield/maxraidbattles/den9.shtml', gmax: false, swordPokemon: ['833', '194', '535', '341', '090', '536', '834', '195', '771', '091', '537', '342'], shieldPokemon: ['833', '194', '535', '341', '090', '536', '834', '195', '771', '091', '537', '342']},
        75: {name: 'Den 75', link: 'https://www.serebii.net/swordshield/maxraidbattles/den75.shtml', gmax: false, swordPokemon: ['129', '751', '194', '339', '098', '746', '099', '340', '211', '195', '752', '130'], shieldPokemon: ['129', '751', '194', '339', '098', '746', '099', '340', '211', '195', '752', '130']},
        21: {name: 'Den 21', link: 'https://www.serebii.net/swordshield/maxraidbattles/den21.shtml', gmax: false, swordPokemon: ['582', '220', '459', '712', '225', '583', '221', '713', '460', '091', '584', '131'], shieldPokemon: ['582', '220', '459', '712', '225', '583', '221', '713', '460', '091', '584', '131']},
        55: {name: 'Den 55', link: 'https://www.serebii.net/swordshield/maxraidbattles/den55.shtml', gmax: false, swordPokemon: ['582', '554-g', '122-g', '712', '361', '225', '713', '362', '584', '866', '131', '555-g'], shieldPokemon: ['582', '613', '122-g', '712', '361', '225', '713', '362', '584', '866', '131', '875']},
        20: {name: 'Den 20', link: 'https://www.serebii.net/swordshield/maxraidbattles/den20.shtml', gmax: false, swordPokemon: ['037', '850', '757', '607', '554-g', '758', '838', '038', '324', '851', '839', '555-g'], shieldPokemon: ['058', '850', '757', '607', '324', '838', '758', '059', '324', '851', '839', '059']},
        54: {name: 'Den 54', link: 'https://www.serebii.net/swordshield/maxraidbattles/den54.shtml', gmax: false, swordPokemon: ['037', '850', '607', '757', '838', '608', '631', '324', '038', '609', '839', '776'], shieldPokemon: ['058', '850', '607', '757', '838', '631', '608', '324', '059', '609', '839', '758']},
        15: {name: 'Den 15', link: 'https://www.serebii.net/swordshield/maxraidbattles/den15.shtml', gmax: false, swordPokemon: ['837', '524', '557', '688', '838', '525', '558', '689', '095', '839', '526', '464'], shieldPokemon: ['837', '557', '524', '688', '838', '525', '558', '689', '839', '526', '095', '464']},
        39: {name: 'Den 39', link: 'https://www.serebii.net/swordshield/maxraidbattles/den39.shtml', gmax: false, swordPokemon: ['659', '163', '519', '572', '694', '759', '660', '164', '521', '695', '573', '760'], shieldPokemon: ['659', '163', '519', '572', '694', '759', '660', '164', '521', '695', '573', '760']},
        31: {name: 'Den 31', link: 'https://www.serebii.net/swordshield/maxraidbattles/den31.shtml', gmax: false, swordPokemon: ['519', '163', '177', '627', '527', '520', '521', '164', '528', '178', '628', '561'], shieldPokemon: ['519', '163', '177', '629', '527', '520', '521', '164', '528', '178', '630', '561']},
        61: {name: 'Den 61', link: 'https://www.serebii.net/swordshield/maxraidbattles/den61.shtml', gmax: false, swordPokemon: ['177', '163', '821', '278', '012', '822', '164', '279', '178', '701', '823', '225'], shieldPokemon: ['177', '163', '821', '278', '012', '822', '164', '279', '178', '701', '823', '225']},
        29: {name: 'Den 29', link: 'https://www.serebii.net/swordshield/maxraidbattles/den29.shtml', gmax: false, swordPokemon: ['434', '568', '451', '747', '043', '315', '211', '452', '045', '748', '569', '435'], shieldPokemon: ['434', '568', '451', '043', '747', '315', '211', '452', '045', '435', '569', '748']},
        86: {name: 'Den 86', link: 'https://www.serebii.net/swordshield/maxraidbattles/den86.shtml', gmax: true, swordPokemon: ['434', '568', '451', '109', '747', '848', '452', '849', '435', '110-g', '748', '569-gi'], shieldPokemon: ['434', '568', '451', '109', '757', '848', '452', '849', '435', '110-g', '758', '569-gi']},
        7: {name: 'Den 7', link: 'https://www.serebii.net/swordshield/maxraidbattles/den7.shtml', gmax: false, swordPokemon: ['129', '458', '223', '170', '320', '550', '224', '226', '171', '321', '746', '130'], shieldPokemon: ['129', '458', '223', '170', '320', '550', '224', '226', '171', '321', '746', '130']},
        32: {name: 'Den 32', link: 'https://www.serebii.net/swordshield/maxraidbattles/den32.shtml', gmax: false, swordPokemon: ['821', '714', '278', '177', '425', '822', '426', '279', '178', '823', '701', '845'], shieldPokemon: ['821', '714', '278', '177', '425', '822', '426', '279', '178', '823', '701', '845']},
        89: {name: 'Den 89', link: 'https://www.serebii.net/swordshield/maxraidbattles/den89.shtml', gmax: true, swordPokemon: ['177', '163', '821', '278', '012', '822', '164', '279', '178', '701', '561', '823-gi'], shieldPokemon: ['177', '163', '821', '278', '012', '822', '164', '279', '178', '701', '561', '823-gi']},
        24: {name: 'Den 24', link: 'https://www.serebii.net/swordshield/maxraidbattles/den24.shtml', gmax: false, swordPokemon: ['172', '309', '595', '170', '737', '025', '025', '310', '171', '596', '738', '026'], shieldPokemon: ['172', '309', '595', '170', '737', '025', '025', '310', '171', '596', '738', '026']},
        78: {name: 'Den 78', link: 'https://www.serebii.net/swordshield/maxraidbattles/den78.shtml', gmax: true, swordPokemon: ['129', '846', '833', '098', '771', '550', '211', '099', '746', '130', '423-e', '834-gi'], shieldPokemon: ['129', '846', '833', '098', '771', '550', '211', '099', '746', '130', '423-e', '834-gi']},
        23: {name: 'Den 23', link: 'https://www.serebii.net/swordshield/maxraidbattles/den23.shtml', gmax: false, swordPokemon: ['361', '872', '554-g', '215', '122-g', '459', '460', '362', '866', '873', '478', '555-g'], shieldPokemon: ['361', '872', '225', '215', '122-g', '459', '460', '362', '866', '873', '478', '875']},
        18: {name: 'Den 18', link: 'https://www.serebii.net/swordshield/maxraidbattles/den18.shtml', gmax: false, swordPokemon: ['037', '850', '757', '607', '554-g', '758', '608', '038', '324', '851', '631', '555-g'], shieldPokemon: ['058', '850', '757', '607', '631', '608', '758', '059', '324', '631', '851', '059']},
        71: {name: 'Den 71', link: 'https://www.serebii.net/swordshield/maxraidbattles/den71.shtml', gmax: false, swordPokemon: ['037', '850', '607', '037', '838', '608', '631', '324', '059', '038', '609', '136'], shieldPokemon: ['058', '850', '607', '058', '838', '631', '608', '324', '038', '059', '609', '136']},
        30: {name: 'Den 30', link: 'https://www.serebii.net/swordshield/maxraidbattles/den30.shtml', gmax: false, swordPokemon: ['848', '092', '451', '043', '044', '093', '109', '211', '045', '315', '849', '110-g'], shieldPokemon: ['848', '092', '451', '043', '044', '093', '109', '211', '045', '315', '849', '110-g']},
        60: {name: 'Den 60', link: 'https://www.serebii.net/swordshield/maxraidbattles/den60.shtml', gmax: false, swordPokemon: ['434', '568', '451', '109', '747', '848', '569', '452', '849', '435', '110-g', '748'], shieldPokemon: ['434', '568', '451', '109', '757', '848', '569', '452', '849', '435', '110-g', '758']},
        43: {name: 'Den 43', link: 'https://www.serebii.net/swordshield/maxraidbattles/den43.shtml', gmax: false, swordPokemon: ['092', '562-g', '854', '355', '093', '710', '356', '867', '855', '711', '477', '094'], shieldPokemon: ['092', '562-g', '854', '355', '093', '222-g', '356', '302', '867', '864', '477', '094']},
        42: {name: 'Den 42', link: 'https://www.serebii.net/swordshield/maxraidbattles/den42.shtml', gmax: false, swordPokemon: ['422-e', '098', '341', '833', '688', '771', '099', '342', '689', '423-e', '593', '834'], shieldPokemon: ['422-e', '098', '341', '833', '688', '771', '099', '342', '689', '423-e', '593', '834']},
        67: {name: 'Den 67', link: 'https://www.serebii.net/swordshield/maxraidbattles/den67.shtml', gmax: false, swordPokemon: ['458', '341', '846', '833', '747', '550', '342', '748', '771', '226', '131', '134'], shieldPokemon: ['458', '341', '846', '833', '747', '550', '342', '748', '771', '226', '131', '134']},
        25: {name: 'Den 25', link: 'https://www.serebii.net/swordshield/maxraidbattles/den25.shtml', gmax: false, swordPokemon: ['835', '694', '848', '170', '025', '171', '836', '695', '849', '871', '777', '877'], shieldPokemon: ['835', '694', '848', '170', '025', '171', '836', '695', '849', '871', '777', '877']},
        72: {name: 'Den 72', link: 'https://www.serebii.net/swordshield/maxraidbattles/den72.shtml', gmax: false, swordPokemon: ['835', '848', '025', '694', '170', '171', '836', '849', '695', '738', '025', '135'], shieldPokemon: ['835', '848', '025', '694', '170', '171', '836', '849', '695', '738', '025', '135']},
        69: {name: 'Den 69', link: 'https://www.serebii.net/swordshield/maxraidbattles/den69.shtml', gmax: false, swordPokemon: ['827', '263-g', '686', '624', '510', '264-g', '828', '675', '625', '687', '862', '197'], shieldPokemon: ['827', '263-g', '686', '624', '510', '264-g', '828', '675', '625', '687', '862', '197']},
        70: {name: 'Den 70', link: 'https://www.serebii.net/swordshield/maxraidbattles/den70.shtml', gmax: false, swordPokemon: ['420', '761', '829', '546', '762', '597', '421', '598', '830', '763', '547', '470'], shieldPokemon: ['420', '761', '829', '546', '762', '597', '421', '598', '830', '763', '547', '470']},
        84: {name: 'Den 84', link: 'https://www.serebii.net/swordshield/maxraidbattles/den84.shtml', gmax: true, swordPokemon: ['447', '436', '624', '599', '095', '632', '600', '437', '625', '208', '601', '884-gi'], shieldPokemon: ['447', '436', '624', '599', '095', '600', '632', '437', '625', '208', '601', '884-gi']},
        12: {name: 'Den 12', link: 'https://www.serebii.net/swordshield/maxraidbattles/den12.shtml', gmax: false, swordPokemon: ['599', '436', '597', '624', '599', '436', '208', '598', '437', '625', '303', '777'], shieldPokemon: ['599', '436', '597', '624', '599', '436', '208', '598', '437', '625', '208', '777']},
        45: {name: 'Den 45', link: 'https://www.serebii.net/swordshield/maxraidbattles/den45.shtml', gmax: false, swordPokemon: ['447', '436', '624', '599', '095', '632', '600', '437', '625', '208', '601', '448'], shieldPokemon: ['447', '436', '624', '599', '095', '600', '632', '437', '625', '208', '601', '448']},
        51: {name: 'Den 51', link: 'https://www.serebii.net/swordshield/maxraidbattles/den51.shtml', gmax: false, swordPokemon: ['557', '438', '837', '688', '838', '185', '689', '095', '558', '839', '208', '874'], shieldPokemon: ['557', '438', '837', '524', '838', '246', '247', '095', '558', '839', '208', '248']},
        83: {name: 'Den 83', link: 'https://www.serebii.net/swordshield/maxraidbattles/den83.shtml', gmax: true, swordPokemon: ['557', '438', '837', '688', '838', '185', '689', '095', '558', '208', '874', '839-gi'], shieldPokemon: ['582', '613', '122-g', '712', '361', '225', '713', '362', '584', '866', '875', '131-gi']},
        14: {name: 'Den 14', link: 'https://www.serebii.net/swordshield/maxraidbattles/den14.shtml', gmax: false, swordPokemon: ['439', '360', '177', '343', '436', '122-g', '561', '178', '876', '344', '866', '202'], shieldPokemon: ['439', '360', '177', '343', '436', '122-g', '561', '178', '876-f', '344', '866', '202']},
        68: {name: 'Den 68', link: 'https://www.serebii.net/swordshield/maxraidbattles/den68.shtml', gmax: false, swordPokemon: ['686', '436', '122-g', '527', '856', '857', '437', '528', '687', '866', '858', '196'], shieldPokemon: ['686', '436', '122-g', '527', '856', '857', '437', '528', '687', '866', '858', '196']},
        19: {name: 'Den 19', link: 'https://www.serebii.net/swordshield/maxraidbattles/den19.shtml', gmax: false, swordPokemon: ['037', '757', '607', '037', '757', '758', '608', '038', '324', '758', '609', '776'], shieldPokemon: ['058', '757', '607', '058', '757', '608', '758', '059', '758', '324', '609', '059']},
        53: {name: 'Den 53', link: 'https://www.serebii.net/swordshield/maxraidbattles/den53.shtml', gmax: false, swordPokemon: ['037', '850', '607', '004', '005', '038', '631', '324', '038', '758', '851', '006'], shieldPokemon: ['058', '850', '607', '004', '005', '631', '631', '324', '758', '059', '851', '006']},
        33: {name: 'Den 33', link: 'https://www.serebii.net/swordshield/maxraidbattles/den33.shtml', gmax: false, swordPokemon: ['173', '175', '742', '684', '035', '755', '176', '036', '743', '756', '685', '468'], shieldPokemon: ['173', '175', '742', '682', '035', '755', '176', '036', '743', '756', '683', '468']},
        62: {name: 'Den 62', link: 'https://www.serebii.net/swordshield/maxraidbattles/den62.shtml', gmax: false, swordPokemon: ['175', '755', '859', '280', '176', '756', '860', '303', '282', '468', '861', '778'], shieldPokemon: ['175', '755', '859', '280', '176', '756', '860', '078-g', '282', '468', '861', '778']},
        57: {name: 'Den 57', link: 'https://www.serebii.net/swordshield/maxraidbattles/den57.shtml', gmax: false, swordPokemon: ['172', '309', '848', '694', '595', '025', '025', '479-m', '479-s', '479-w', '479-f', '479-h'], shieldPokemon: ['172', '309', '848', '694', '595', '025', '025', '479-m', '479-s', '479-w', '479-f', '479-h']},
        73: {name: 'Den 73', link: 'https://www.serebii.net/swordshield/maxraidbattles/den73.shtml', gmax: false, swordPokemon: ['582', '872', '122-g', '712', '361', '583', '713', '873', '584', '866', '478', '471'], shieldPokemon: ['582', '872', '122-g', '712', '361', '583', '713', '873', '584', '866', '478', '471']},
        56: {name: 'Den 56', link: 'https://www.serebii.net/swordshield/maxraidbattles/den56.shtml', gmax: false, swordPokemon: ['835', '848', '025', '595', '170', '171', '836', '849', '871', '596', '777', '877'], shieldPokemon: ['835', '848', '025', '595', '170', '171', '836', '849', '871', '596', '777', '877']},
        77: {name: 'Den 77', link: 'https://www.serebii.net/swordshield/maxraidbattles/den77.shtml', gmax: true, swordPokemon: ['037', '850', '607', '004', '005', '038', '631', '324', '038', '758', '851', '006-gi'], shieldPokemon: ['058', '850', '607', '004', '005', '631', '631', '324', '758', '059', '851', '006-gi']},
        74: {name: 'Den 74', link: 'https://www.serebii.net/swordshield/maxraidbattles/den74.shtml', gmax: false, swordPokemon: ['175', '684', '859', '280', '176', '860', '685', '868', '282', '861', '468', '700'], shieldPokemon: ['175', '682', '859', '280', '176', '860', '683', '868', '282', '861', '468', '700']},
        50: {name: 'Den 50', link: 'https://www.serebii.net/swordshield/maxraidbattles/den50.shtml', gmax: false, swordPokemon: ['686', '280', '122-g', '527', '856', '857', '281', '528', '858', '866', '687', '282'], shieldPokemon: ['686', '280', '122-g', '527', '856', '857', '281', '528', '858', '866', '687', '282']},
        41: {name: 'Den 41', link: 'https://www.serebii.net/swordshield/maxraidbattles/den41.shtml', gmax: false, swordPokemon: ['535', '090', '170', '747', '536', '846', '091', '171', '746', '537', '847', '748'], shieldPokemon: ['535', '090', '170', '536', '747', '846', '748', '091', '171', '746', '537', '847']},
        76: {name: 'Den 76', link: 'https://www.serebii.net/swordshield/maxraidbattles/den76.shtml', gmax: false, swordPokemon: ['458', '223', '320', '688', '098', '771', '099', '550', '211', '224', '321', '226'], shieldPokemon: ['458', '223', '320', '688', '098', '771', '099', '550', '211', '224', '321', '226']},
        3: {name: 'Den 3', link: 'https://www.serebii.net/swordshield/maxraidbattles/den3.shtml', gmax: false, swordPokemon: ['438', '524', '688', '557', '111', '525', '689', '112', '185', '558', '526', '213'], shieldPokemon: ['438', '688', '524', '557', '111', '525', '689', '112', '185', '526', '558', '213']},
        90: {name: 'Den 90', link: 'https://www.serebii.net/swordshield/maxraidbattles/den90.shtml', gmax: true, swordPokemon: ['767', '824', '588', '751', '616', '557', '825', '826', '752', '768', '589', '012-gi'], shieldPokemon: ['767', '824', '616', '751', '588', '557', '825', '826', '752', '768', '617', '012-gi']},
        37: {name: 'Den 37', link: 'https://www.serebii.net/swordshield/maxraidbattles/den37.shtml', gmax: false, swordPokemon: ['714', '328', '610', '714', '782', '329', '783', '611', '612', '330', '776', '784'], shieldPokemon: ['714', '610', '328', '714', '704', '329', '611', '705', '330', '612', '780', '706']},
        1: {name: 'Den 1', link: 'https://www.serebii.net/swordshield/maxraidbattles/den1.shtml', gmax: false, swordPokemon: ['236', '066', '532', '559', '067', '533', '106', '107', '560', '534', '068', '237'], shieldPokemon: ['236', '066', '532', '453', '533', '067', '107', '106', '454', '237', '068', '534']},
        91: {name: 'Den 91', link: 'https://www.serebii.net/swordshield/maxraidbattles/den91.shtml', gmax: true, swordPokemon: ['341', '098', '846', '833', '747', '550', '342', '748', '771', '130', '131', '099-gi'], shieldPokemon: ['341', '098', '846', '833', '747', '550', '342', '748', '771', '130', '131', '099-gi']},
        85: {name: 'Den 85', link: 'https://www.serebii.net/swordshield/maxraidbattles/den85.shtml', gmax: true, swordPokemon: ['052-g', '436', '624', '597', '679', '437', '863', '598', '625', '618-g', '884', '879-gi'], shieldPokemon: ['052-g', '436', '624', '597', '679', '437', '863', '598', '625', '618-g', '884', '879-gi']},
        66: {name: 'Den 66', link: 'https://www.serebii.net/swordshield/maxraidbattles/den66.shtml', gmax: false, swordPokemon: ['132', '132', '132', '132', '132', '132', '132', '132', '132', '132', '132', '132'], shieldPokemon: ['132', '132', '132', '132', '132', '132', '132', '132', '132', '132', '132', '132']},
        2: {name: 'Den 2', link: 'https://www.serebii.net/swordshield/maxraidbattles/den2.shtml', gmax: false, swordPokemon: ['280', '517', '677', '574', '605', '281', '678', '575', '518', '576', '338', '282'], shieldPokemon: ['280', '517', '677', '577', '605', '281', '678-f', '578', '518', '579', '337', '282']},
        35: {name: 'Den 35', link: 'https://www.serebii.net/swordshield/maxraidbattles/den35.shtml', gmax: false, swordPokemon: ['509', '434', '215', '686', '624', '510', '435', '461', '687', '625', '342', '275'], shieldPokemon: ['509', '434', '215', '686', '624', '510', '435', '461', '687', '625', '342', '302']},
        22: {name: 'Den 22', link: 'https://www.serebii.net/swordshield/maxraidbattles/den22.shtml', gmax: false, swordPokemon: ['220', '613', '872', '215', '122-g', '221', '091', '614', '866', '473', '873', '461'], shieldPokemon: ['220', '613', '872', '215', '122-g', '221', '091', '614', '866', '473', '873', '461']},
        81: {name: 'Den 81', link: 'https://www.serebii.net/swordshield/maxraidbattles/den81.shtml', gmax: true, swordPokemon: ['447', '066', '759', '083-g', '760', '067', '870', '701', '448', '475', '865', '068-gi'], shieldPokemon: ['679', '562-g', '854', '092', '680', '222-g', '093', '302', '855', '864', '867', '094-gi']},
        6: {name: 'Den 6', link: 'https://www.serebii.net/swordshield/maxraidbattles/den6.shtml', gmax: false, swordPokemon: ['092', '355', '425', '708', '592', '710', '093', '356', '426', '709', '711', '593'], shieldPokemon: ['092', '355', '425', '708', '592', '710', '093', '356', '426', '709', '711', '593']},
        80: {name: 'Den 80', link: 'https://www.serebii.net/swordshield/maxraidbattles/den80.shtml', gmax: true, swordPokemon: ['037', '850', '607', '757', '838', '608', '631', '324', '038', '609', '839', '851-gi'], shieldPokemon: ['058', '850', '607', '757', '838', '608', '631', '324', '059', '609', '839', '851-gi']},
        47: {name: 'Den 47', link: 'https://www.serebii.net/swordshield/maxraidbattles/den47.shtml', gmax: false, swordPokemon: ['679', '562-g', '854', '425', '680', '710', '426', '711', '855', '711', '867', '681'], shieldPokemon: ['679', '562-g', '854', '425', '680', '222-g', '426', '302', '855', '864', '867', '681']},
      },
      allPokemon: [{id: '001', name: 'Bulbasaur'}, {id: '002', name: 'Ivysaur'}, {id: '003', name: 'Venusaur'}, {id: '004', name: 'Charmander'}, {id: '005', name: 'Charmeleon'}, {id: '006', name: 'Charizard'}, {id: '007', name: 'Squirtle'}, {id: '008', name: 'Wartortle'}, {id: '009', name: 'Blastoise'}, {id: '010', name: 'Caterpie'}, {id: '011', name: 'Metapod'}, {id: '012', name: 'Butterfree'}, {id: '013', name: 'Weedle'}, {id: '014', name: 'Kakuna'}, {id: '015', name: 'Beedrill'}, {id: '016', name: 'Pidgey'}, {id: '017', name: 'Pidgeotto'}, {id: '018', name: 'Pidgeot'}, {id: '019', name: 'Rattata'}, {id: '020', name: 'Raticate'}, {id: '021', name: 'Spearow'}, {id: '022', name: 'Fearow'}, {id: '023', name: 'Ekans'}, {id: '024', name: 'Arbok'}, {id: '025', name: 'Pikachu'}, {id: '026', name: 'Raichu'}, {id: '027', name: 'Sandshrew'}, {id: '028', name: 'Sandslash'}, {id: '029', name: 'Nidoran\u2640'}, {id: '030', name: 'Nidorina'}, {id: '031', name: 'Nidoqueen'}, {id: '032', name: 'Nidoran\u2642'}, {id: '033', name: 'Nidorino'}, {id: '034', name: 'Nidoking'}, {id: '035', name: 'Clefairy'}, {id: '036', name: 'Clefable'}, {id: '037', name: 'Vulpix'}, {id: '038', name: 'Ninetales'}, {id: '039', name: 'Jigglypuff'}, {id: '040', name: 'Wigglytuff'}, {id: '041', name: 'Zubat'}, {id: '042', name: 'Golbat'}, {id: '043', name: 'Oddish'}, {id: '044', name: 'Gloom'}, {id: '045', name: 'Vileplume'}, {id: '046', name: 'Paras'}, {id: '047', name: 'Parasect'}, {id: '048', name: 'Venonat'}, {id: '049', name: 'Venomoth'}, {id: '050', name: 'Diglett'}, {id: '051', name: 'Dugtrio'}, {id: '052', name: 'Meowth'}, {id: '053', name: 'Persian'}, {id: '054', name: 'Psyduck'}, {id: '055', name: 'Golduck'}, {id: '056', name: 'Mankey'}, {id: '057', name: 'Primeape'}, {id: '058', name: 'Growlithe'}, {id: '059', name: 'Arcanine'}, {id: '060', name: 'Poliwag'}, {id: '061', name: 'Poliwhirl'}, {id: '062', name: 'Poliwrath'}, {id: '063', name: 'Abra'}, {id: '064', name: 'Kadabra'}, {id: '065', name: 'Alakazam'}, {id: '066', name: 'Machop'}, {id: '067', name: 'Machoke'}, {id: '068', name: 'Machamp'}, {id: '069', name: 'Bellsprout'}, {id: '070', name: 'Weepinbell'}, {id: '071', name: 'Victreebel'}, {id: '072', name: 'Tentacool'}, {id: '073', name: 'Tentacruel'}, {id: '074', name: 'Geodude'}, {id: '075', name: 'Graveler'}, {id: '076', name: 'Golem'}, {id: '077', name: 'Ponyta'}, {id: '078', name: 'Rapidash'}, {id: '079', name: 'Slowpoke'}, {id: '080', name: 'Slowbro'}, {id: '081', name: 'Magnemite'}, {id: '082', name: 'Magneton'}, {id: '083', name: "Farfetch'd"}, {id: '084', name: 'Doduo'}, {id: '085', name: 'Dodrio'}, {id: '086', name: 'Seel'}, {id: '087', name: 'Dewgong'}, {id: '088', name: 'Grimer'}, {id: '089', name: 'Muk'}, {id: '090', name: 'Shellder'}, {id: '091', name: 'Cloyster'}, {id: '092', name: 'Gastly'}, {id: '093', name: 'Haunter'}, {id: '094', name: 'Gengar'}, {id: '095', name: 'Onix'}, {id: '096', name: 'Drowzee'}, {id: '097', name: 'Hypno'}, {id: '098', name: 'Krabby'}, {id: '099', name: 'Kingler'}, {id: '100', name: 'Voltorb'}, {id: '101', name: 'Electrode'}, {id: '102', name: 'Exeggcute'}, {id: '103', name: 'Exeggutor'}, {id: '104', name: 'Cubone'}, {id: '105', name: 'Marowak'}, {id: '106', name: 'Hitmonlee'}, {id: '107', name: 'Hitmonchan'}, {id: '108', name: 'Lickitung'}, {id: '109', name: 'Koffing'}, {id: '110', name: 'Weezing'}, {id: '111', name: 'Rhyhorn'}, {id: '112', name: 'Rhydon'}, {id: '113', name: 'Chansey'}, {id: '114', name: 'Tangela'}, {id: '115', name: 'Kangaskhan'}, {id: '116', name: 'Horsea'}, {id: '117', name: 'Seadra'}, {id: '118', name: 'Goldeen'}, {id: '119', name: 'Seaking'}, {id: '120', name: 'Staryu'}, {id: '121', name: 'Starmie'}, {id: '122', name: 'Mr. Mime'}, {id: '123', name: 'Scyther'}, {id: '124', name: 'Jynx'}, {id: '125', name: 'Electabuzz'}, {id: '126', name: 'Magmar'}, {id: '127', name: 'Pinsir'}, {id: '128', name: 'Tauros'}, {id: '129', name: 'Magikarp'}, {id: '130', name: 'Gyarados'}, {id: '131', name: 'Lapras'}, {id: '132', name: 'Ditto'}, {id: '133', name: 'Eevee'}, {id: '134', name: 'Vaporeon'}, {id: '135', name: 'Jolteon'}, {id: '136', name: 'Flareon'}, {id: '137', name: 'Porygon'}, {id: '138', name: 'Omanyte'}, {id: '139', name: 'Omastar'}, {id: '140', name: 'Kabuto'}, {id: '141', name: 'Kabutops'}, {id: '142', name: 'Aerodactyl'}, {id: '143', name: 'Snorlax'}, {id: '144', name: 'Articuno'}, {id: '145', name: 'Zapdos'}, {id: '146', name: 'Moltres'}, {id: '147', name: 'Dratini'}, {id: '148', name: 'Dragonair'}, {id: '149', name: 'Dragonite'}, {id: '150', name: 'Mewtwo'}, {id: '151', name: 'Mew'}, {id: '152', name: 'Chikorita'}, {id: '153', name: 'Bayleef'}, {id: '154', name: 'Meganium'}, {id: '155', name: 'Cyndaquil'}, {id: '156', name: 'Quilava'}, {id: '157', name: 'Typhlosion'}, {id: '158', name: 'Totodile'}, {id: '159', name: 'Croconaw'}, {id: '160', name: 'Feraligatr'}, {id: '161', name: 'Sentret'}, {id: '162', name: 'Furret'}, {id: '163', name: 'Hoothoot'}, {id: '164', name: 'Noctowl'}, {id: '165', name: 'Ledyba'}, {id: '166', name: 'Ledian'}, {id: '167', name: 'Spinarak'}, {id: '168', name: 'Ariados'}, {id: '169', name: 'Crobat'}, {id: '170', name: 'Chinchou'}, {id: '171', name: 'Lanturn'}, {id: '172', name: 'Pichu'}, {id: '173', name: 'Cleffa'}, {id: '174', name: 'Igglybuff'}, {id: '175', name: 'Togepi'}, {id: '176', name: 'Togetic'}, {id: '177', name: 'Natu'}, {id: '178', name: 'Xatu'}, {id: '179', name: 'Mareep'}, {id: '180', name: 'Flaaffy'}, {id: '181', name: 'Ampharos'}, {id: '182', name: 'Bellossom'}, {id: '183', name: 'Marill'}, {id: '184', name: 'Azumarill'}, {id: '185', name: 'Sudowoodo'}, {id: '186', name: 'Politoed'}, {id: '187', name: 'Hoppip'}, {id: '188', name: 'Skiploom'}, {id: '189', name: 'Jumpluff'}, {id: '190', name: 'Aipom'}, {id: '191', name: 'Sunkern'}, {id: '192', name: 'Sunflora'}, {id: '193', name: 'Yanma'}, {id: '194', name: 'Wooper'}, {id: '195', name: 'Quagsire'}, {id: '196', name: 'Espeon'}, {id: '197', name: 'Umbreon'}, {id: '198', name: 'Murkrow'}, {id: '199', name: 'Slowking'}, {id: '200', name: 'Misdreavus'}, {id: '201', name: 'Unown'}, {id: '202', name: 'Wobbuffet'}, {id: '203', name: 'Girafarig'}, {id: '204', name: 'Pineco'}, {id: '205', name: 'Forretress'}, {id: '206', name: 'Dunsparce'}, {id: '207', name: 'Gligar'}, {id: '208', name: 'Steelix'}, {id: '209', name: 'Snubbull'}, {id: '210', name: 'Granbull'}, {id: '211', name: 'Qwilfish'}, {id: '212', name: 'Scizor'}, {id: '213', name: 'Shuckle'}, {id: '214', name: 'Heracross'}, {id: '215', name: 'Sneasel'}, {id: '216', name: 'Teddiursa'}, {id: '217', name: 'Ursaring'}, {id: '218', name: 'Slugma'}, {id: '219', name: 'Magcargo'}, {id: '220', name: 'Swinub'}, {id: '221', name: 'Piloswine'}, {id: '222', name: 'Corsola'}, {id: '223', name: 'Remoraid'}, {id: '224', name: 'Octillery'}, {id: '225', name: 'Delibird'}, {id: '226', name: 'Mantine'}, {id: '227', name: 'Skarmory'}, {id: '228', name: 'Houndour'}, {id: '229', name: 'Houndoom'}, {id: '230', name: 'Kingdra'}, {id: '231', name: 'Phanpy'}, {id: '232', name: 'Donphan'}, {id: '233', name: 'Porygon2'}, {id: '234', name: 'Stantler'}, {id: '235', name: 'Smeargle'}, {id: '236', name: 'Tyrogue'}, {id: '237', name: 'Hitmontop'}, {id: '238', name: 'Smoochum'}, {id: '239', name: 'Elekid'}, {id: '240', name: 'Magby'}, {id: '241', name: 'Miltank'}, {id: '242', name: 'Blissey'}, {id: '243', name: 'Raikou'}, {id: '244', name: 'Entei'}, {id: '245', name: 'Suicune'}, {id: '246', name: 'Larvitar'}, {id: '247', name: 'Pupitar'}, {id: '248', name: 'Tyranitar'}, {id: '249', name: 'Lugia'}, {id: '250', name: 'Ho-Oh'}, {id: '251', name: 'Celebi'}, {id: '252', name: 'Treecko'}, {id: '253', name: 'Grovyle'}, {id: '254', name: 'Sceptile'}, {id: '255', name: 'Torchic'}, {id: '256', name: 'Combusken'}, {id: '257', name: 'Blaziken'}, {id: '258', name: 'Mudkip'}, {id: '259', name: 'Marshtomp'}, {id: '260', name: 'Swampert'}, {id: '261', name: 'Poochyena'}, {id: '262', name: 'Mightyena'}, {id: '263', name: 'Zigzagoon'}, {id: '264', name: 'Linoone'}, {id: '265', name: 'Wurmple'}, {id: '266', name: 'Silcoon'}, {id: '267', name: 'Beautifly'}, {id: '268', name: 'Cascoon'}, {id: '269', name: 'Dustox'}, {id: '270', name: 'Lotad'}, {id: '271', name: 'Lombre'}, {id: '272', name: 'Ludicolo'}, {id: '273', name: 'Seedot'}, {id: '274', name: 'Nuzleaf'}, {id: '275', name: 'Shiftry'}, {id: '276', name: 'Taillow'}, {id: '277', name: 'Swellow'}, {id: '278', name: 'Wingull'}, {id: '279', name: 'Pelipper'}, {id: '280', name: 'Ralts'}, {id: '281', name: 'Kirlia'}, {id: '282', name: 'Gardevoir'}, {id: '283', name: 'Surskit'}, {id: '284', name: 'Masquerain'}, {id: '285', name: 'Shroomish'}, {id: '286', name: 'Breloom'}, {id: '287', name: 'Slakoth'}, {id: '288', name: 'Vigoroth'}, {id: '289', name: 'Slaking'}, {id: '290', name: 'Nincada'}, {id: '291', name: 'Ninjask'}, {id: '292', name: 'Shedinja'}, {id: '293', name: 'Whismur'}, {id: '294', name: 'Loudred'}, {id: '295', name: 'Exploud'}, {id: '296', name: 'Makuhita'}, {id: '297', name: 'Hariyama'}, {id: '298', name: 'Azurill'}, {id: '299', name: 'Nosepass'}, {id: '300', name: 'Skitty'}, {id: '301', name: 'Delcatty'}, {id: '302', name: 'Sableye'}, {id: '303', name: 'Mawile'}, {id: '304', name: 'Aron'}, {id: '305', name: 'Lairon'}, {id: '306', name: 'Aggron'}, {id: '307', name: 'Meditite'}, {id: '308', name: 'Medicham'}, {id: '309', name: 'Electrike'}, {id: '310', name: 'Manectric'}, {id: '311', name: 'Plusle'}, {id: '312', name: 'Minun'}, {id: '313', name: 'Volbeat'}, {id: '314', name: 'Illumise'}, {id: '315', name: 'Roselia'}, {id: '316', name: 'Gulpin'}, {id: '317', name: 'Swalot'}, {id: '318', name: 'Carvanha'}, {id: '319', name: 'Sharpedo'}, {id: '320', name: 'Wailmer'}, {id: '321', name: 'Wailord'}, {id: '322', name: 'Numel'}, {id: '323', name: 'Camerupt'}, {id: '324', name: 'Torkoal'}, {id: '325', name: 'Spoink'},
      {id: '326', name: 'Grumpig'}, {id: '327', name: 'Spinda'}, {id: '328', name: 'Trapinch'}, {id: '329', name: 'Vibrava'}, {id: '330', name: 'Flygon'}, {id: '331', name: 'Cacnea'}, {id: '332', name: 'Cacturne'}, {id: '333', name: 'Swablu'}, {id: '334', name: 'Altaria'}, {id: '335', name: 'Zangoose'}, {id: '336', name: 'Seviper'}, {id: '337', name: 'Lunatone'}, {id: '338', name: 'Solrock'}, {id: '339', name: 'Barboach'}, {id: '340', name: 'Whiscash'}, {id: '341', name: 'Corphish'}, {id: '342', name: 'Crawdaunt'}, {id: '343', name: 'Baltoy'}, {id: '344', name: 'Claydol'}, {id: '345', name: 'Lileep'}, {id: '346', name: 'Cradily'}, {id: '347', name: 'Anorith'}, {id: '348', name: 'Armaldo'}, {id: '349', name: 'Feebas'}, {id: '350', name: 'Milotic'}, {id: '351', name: 'Castform'}, {id: '352', name: 'Kecleon'}, {id: '353', name: 'Shuppet'}, {id: '354', name: 'Banette'}, {id: '355', name: 'Duskull'}, {id: '356', name: 'Dusclops'}, {id: '357', name: 'Tropius'}, {id: '358', name: 'Chimecho'}, {id: '359', name: 'Absol'}, {id: '360', name: 'Wynaut'}, {id: '361', name: 'Snorunt'}, {id: '362', name: 'Glalie'}, {id: '363', name: 'Spheal'}, {id: '364', name: 'Sealeo'}, {id: '365', name: 'Walrein'}, {id: '366', name: 'Clamperl'}, {id: '367', name: 'Huntail'}, {id: '368', name: 'Gorebyss'}, {id: '369', name: 'Relicanth'}, {id: '370', name: 'Luvdisc'}, {id: '371', name: 'Bagon'}, {id: '372', name: 'Shelgon'}, {id: '373', name: 'Salamence'}, {id: '374', name: 'Beldum'}, {id: '375', name: 'Metang'}, {id: '376', name: 'Metagross'}, {id: '377', name: 'Regirock'}, {id: '378', name: 'Regice'}, {id: '379', name: 'Registeel'}, {id: '380', name: 'Latias'}, {id: '381', name: 'Latios'}, {id: '382', name: 'Kyogre'}, {id: '383', name: 'Groudon'}, {id: '384', name: 'Rayquaza'}, {id: '385', name: 'Jirachi'}, {id: '386', name: 'Deoxys'}, {id: '387', name: 'Turtwig'}, {id: '388', name: 'Grotle'}, {id: '389', name: 'Torterra'}, {id: '390', name: 'Chimchar'}, {id: '391', name: 'Monferno'}, {id: '392', name: 'Infernape'}, {id: '393', name: 'Piplup'}, {id: '394', name: 'Prinplup'}, {id: '395', name: 'Empoleon'}, {id: '396', name: 'Starly'}, {id: '397', name: 'Staravia'}, {id: '398', name: 'Staraptor'}, {id: '399', name: 'Bidoof'}, {id: '400', name: 'Bibarel'}, {id: '401', name: 'Kricketot'}, {id: '402', name: 'Kricketune'}, {id: '403', name: 'Shinx'}, {id: '404', name: 'Luxio'}, {id: '405', name: 'Luxray'}, {id: '406', name: 'Budew'}, {id: '407', name: 'Roserade'}, {id: '408', name: 'Cranidos'}, {id: '409', name: 'Rampardos'}, {id: '410', name: 'Shieldon'}, {id: '411', name: 'Bastiodon'}, {id: '412', name: 'Burmy'}, {id: '413', name: 'Wormadam'}, {id: '414', name: 'Mothim'}, {id: '415', name: 'Combee'}, {id: '416', name: 'Vespiquen'}, {id: '417', name: 'Pachirisu'}, {id: '418', name: 'Buizel'}, {id: '419', name: 'Floatzel'}, {id: '420', name: 'Cherubi'}, {id: '421', name: 'Cherrim'}, {id: '422', name: 'Shellos'}, {id: '423', name: 'Gastrodon'}, {id: '424', name: 'Ambipom'}, {id: '425', name: 'Drifloon'}, {id: '426', name: 'Drifblim'}, {id: '427', name: 'Buneary'}, {id: '428', name: 'Lopunny'}, {id: '429', name: 'Mismagius'}, {id: '430', name: 'Honchkrow'}, {id: '431', name: 'Glameow'}, {id: '432', name: 'Purugly'}, {id: '433', name: 'Chingling'}, {id: '434', name: 'Stunky'}, {id: '435', name: 'Skuntank'}, {id: '436', name: 'Bronzor'}, {id: '437', name: 'Bronzong'}, {id: '438', name: 'Bonsly'}, {id: '439', name: 'Mime Jr.'}, {id: '440', name: 'Happiny'}, {id: '441', name: 'Chatot'}, {id: '442', name: 'Spiritomb'}, {id: '443', name: 'Gible'}, {id: '444', name: 'Gabite'}, {id: '445', name: 'Garchomp'}, {id: '446', name: 'Munchlax'}, {id: '447', name: 'Riolu'}, {id: '448', name: 'Lucario'}, {id: '449', name: 'Hippopotas'}, {id: '450', name: 'Hippowdon'}, {id: '451', name: 'Skorupi'}, {id: '452', name: 'Drapion'}, {id: '453', name: 'Croagunk'}, {id: '454', name: 'Toxicroak'}, {id: '455', name: 'Carnivine'}, {id: '456', name: 'Finneon'}, {id: '457', name: 'Lumineon'}, {id: '458', name: 'Mantyke'}, {id: '459', name: 'Snover'}, {id: '460', name: 'Abomasnow'}, {id: '461', name: 'Weavile'}, {id: '462', name: 'Magnezone'}, {id: '463', name: 'Lickilicky'}, {id: '464', name: 'Rhyperior'}, {id: '465', name: 'Tangrowth'}, {id: '466', name: 'Electivire'}, {id: '467', name: 'Magmortar'}, {id: '468', name: 'Togekiss'}, {id: '469', name: 'Yanmega'}, {id: '470', name: 'Leafeon'}, {id: '471', name: 'Glaceon'}, {id: '472', name: 'Gliscor'}, {id: '473', name: 'Mamoswine'}, {id: '474', name: 'Porygon-Z'}, {id: '475', name: 'Gallade'}, {id: '476', name: 'Probopass'}, {id: '477', name: 'Dusknoir'}, {id: '478', name: 'Froslass'}, {id: '479', name: 'Rotom'}, {id: '480', name: 'Uxie'}, {id: '481', name: 'Mesprit'}, {id: '482', name: 'Azelf'}, {id: '483', name: 'Dialga'}, {id: '484', name: 'Palkia'}, {id: '485', name: 'Heatran'}, {id: '486', name: 'Regigigas'}, {id: '487', name: 'Giratina'}, {id: '488', name: 'Cresselia'}, {id: '489', name: 'Phione'}, {id: '490', name: 'Manaphy'}, {id: '491', name: 'Darkrai'}, {id: '492', name: 'Shaymin'}, {id: '493', name: 'Arceus'}, {id: '494', name: 'Victini'}, {id: '495', name: 'Snivy'}, {id: '496', name: 'Servine'}, {id: '497', name: 'Serperior'}, {id: '498', name: 'Tepig'}, {id: '499', name: 'Pignite'}, {id: '500', name: 'Emboar'}, {id: '501', name: 'Oshawott'}, {id: '502', name: 'Dewott'}, {id: '503', name: 'Samurott'}, {id: '504', name: 'Patrat'}, {id: '505', name: 'Watchog'}, {id: '506', name: 'Lillipup'}, {id: '507', name: 'Herdier'}, {id: '508', name: 'Stoutland'}, {id: '509', name: 'Purrloin'}, {id: '510', name: 'Liepard'}, {id: '511', name: 'Pansage'}, {id: '512', name: 'Simisage'}, {id: '513', name: 'Pansear'}, {id: '514', name: 'Simisear'}, {id: '515', name: 'Panpour'}, {id: '516', name: 'Simipour'}, {id: '517', name: 'Munna'}, {id: '518', name: 'Musharna'}, {id: '519', name: 'Pidove'}, {id: '520', name: 'Tranquill'}, {id: '521', name: 'Unfezant'}, {id: '522', name: 'Blitzle'}, {id: '523', name: 'Zebstrika'}, {id: '524', name: 'Roggenrola'}, {id: '525', name: 'Boldore'}, {id: '526', name: 'Gigalith'}, {id: '527', name: 'Woobat'}, {id: '528', name: 'Swoobat'}, {id: '529', name: 'Drilbur'}, {id: '530', name: 'Excadrill'}, {id: '531', name: 'Audino'}, {id: '532', name: 'Timburr'}, {id: '533', name: 'Gurdurr'}, {id: '534', name: 'Conkeldurr'}, {id: '535', name: 'Tympole'}, {id: '536', name: 'Palpitoad'}, {id: '537', name: 'Seismitoad'}, {id: '538', name: 'Throh'}, {id: '539', name: 'Sawk'}, {id: '540', name: 'Sewaddle'}, {id: '541', name: 'Swadloon'}, {id: '542', name: 'Leavanny'}, {id: '543', name: 'Venipede'}, {id: '544', name: 'Whirlipede'}, {id: '545', name: 'Scolipede'}, {id: '546', name: 'Cottonee'}, {id: '547', name: 'Whimsicott'}, {id: '548', name: 'Petilil'}, {id: '549', name: 'Lilligant'}, {id: '550', name: 'Basculin'}, {id: '551', name: 'Sandile'}, {id: '552', name: 'Krokorok'}, {id: '553', name: 'Krookodile'}, {id: '554', name: 'Darumaka'}, {id: '555', name: 'Darmanitan'}, {id: '556', name: 'Maractus'}, {id: '557', name: 'Dwebble'}, {id: '558', name: 'Crustle'}, {id: '559', name: 'Scraggy'}, {id: '560', name: 'Scrafty'}, {id: '561', name: 'Sigilyph'}, {id: '562', name: 'Yamask'}, {id: '563', name: 'Cofagrigus'}, {id: '564', name: 'Tirtouga'}, {id: '565', name: 'Carracosta'}, {id: '566', name: 'Archen'}, {id: '567', name: 'Archeops'}, {id: '568', name: 'Trubbish'}, {id: '569', name: 'Garbodor'}, {id: '570', name: 'Zorua'}, {id: '571', name: 'Zoroark'}, {id: '572', name: 'Minccino'}, {id: '573', name: 'Cinccino'}, {id: '574', name: 'Gothita'}, {id: '575', name: 'Gothorita'}, {id: '576', name: 'Gothitelle'}, {id: '577', name: 'Solosis'}, {id: '578', name: 'Duosion'}, {id: '579', name: 'Reuniclus'}, {id: '580', name: 'Ducklett'}, {id: '581', name: 'Swanna'}, {id: '582', name: 'Vanillite'}, {id: '583', name: 'Vanillish'}, {id: '584', name: 'Vanilluxe'}, {id: '585', name: 'Deerling'}, {id: '586', name: 'Sawsbuck'}, {id: '587', name: 'Emolga'}, {id: '588', name: 'Karrablast'}, {id: '589', name: 'Escavalier'}, {id: '590', name: 'Foongus'}, {id: '591', name: 'Amoonguss'}, {id: '592', name: 'Frillish'}, {id: '593', name: 'Jellicent'}, {id: '594', name: 'Alomomola'}, {id: '595', name: 'Joltik'}, {id: '596', name: 'Galvantula'}, {id: '597', name: 'Ferroseed'}, {id: '598', name: 'Ferrothorn'}, {id: '599', name: 'Klink'}, {id: '600', name: 'Klang'}, {id: '601', name: 'Klinklang'}, {id: '602', name: 'Tynamo'}, {id: '603', name: 'Eelektrik'}, {id: '604', name: 'Eelektross'}, {id: '605', name: 'Elgyem'}, {id: '606', name: 'Beheeyem'}, {id: '607', name: 'Litwick'}, {id: '608', name: 'Lampent'}, {id: '609', name: 'Chandelure'}, {id: '610', name: 'Axew'}, {id: '611', name: 'Fraxure'}, {id: '612', name: 'Haxorus'}, {id: '613', name: 'Cubchoo'}, {id: '614', name: 'Beartic'}, {id: '615', name: 'Cryogonal'}, {id: '616', name: 'Shelmet'}, {id: '617', name: 'Accelgor'}, {id: '618', name: 'Stunfisk'}, {id: '619', name: 'Mienfoo'}, {id: '620', name: 'Mienshao'}, {id: '621', name: 'Druddigon'}, {id: '622', name: 'Golett'}, {id: '623', name: 'Golurk'}, {id: '624', name: 'Pawniard'}, {id: '625', name: 'Bisharp'}, {id: '626', name: 'Bouffalant'}, {id: '627', name: 'Rufflet'}, {id: '628', name: 'Braviary'}, {id: '629', name: 'Vullaby'}, {id: '630', name: 'Mandibuzz'}, {id: '631', name: 'Heatmor'}, {id: '632', name: 'Durant'}, {id: '633', name: 'Deino'}, {id: '634', name: 'Zweilous'}, {id: '635', name: 'Hydreigon'}, {id: '636', name: 'Larvesta'}, {id: '637', name: 'Volcarona'}, {id: '638', name: 'Cobalion'}, {id: '639', name: 'Terrakion'}, {id: '640', name: 'Virizion'}, {id: '641', name: 'Tornadus'}, {id: '642', name: 'Thundurus'}, {id: '643', name: 'Reshiram'}, {id: '644', name: 'Zekrom'}, {id: '645', name: 'Landorus'}, {id: '646', name: 'Kyurem'}, {id: '647', name: 'Keldeo'}, {id: '648', name: 'Meloetta'}, {id: '649', name: 'Genesect'},
      {id: '650', name: 'Chespin'}, {id: '651', name: 'Quilladin'}, {id: '652', name: 'Chesnaught'}, {id: '653', name: 'Fennekin'}, {id: '654', name: 'Braixen'}, {id: '655', name: 'Delphox'}, {id: '656', name: 'Froakie'}, {id: '657', name: 'Frogadier'}, {id: '658', name: 'Greninja'}, {id: '659', name: 'Bunnelby'}, {id: '660', name: 'Diggersby'}, {id: '661', name: 'Fletchling'}, {id: '662', name: 'Fletchinder'}, {id: '663', name: 'Talonflame'}, {id: '664', name: 'Scatterbug'}, {id: '665', name: 'Spewpa'}, {id: '666', name: 'Vivillon'}, {id: '667', name: 'Litleo'}, {id: '668', name: 'Pyroar'}, {id: '669', name: 'Flab\xe9b\xe9'}, {id: '670', name: 'Floette'}, {id: '671', name: 'Florges'}, {id: '672', name: 'Skiddo'}, {id: '673', name: 'Gogoat'}, {id: '674', name: 'Pancham'}, {id: '675', name: 'Pangoro'}, {id: '676', name: 'Furfrou'}, {id: '677', name: 'Espurr'}, {id: '678', name: 'Meowstic'}, {id: '679', name: 'Honedge'}, {id: '680', name: 'Doublade'}, {id: '681', name: 'Aegislash'}, {id: '682', name: 'Spritzee'}, {id: '683', name: 'Aromatisse'}, {id: '684', name: 'Swirlix'}, {id: '685', name: 'Slurpuff'}, {id: '686', name: 'Inkay'}, {id: '687', name: 'Malamar'}, {id: '688', name: 'Binacle'}, {id: '689', name: 'Barbaracle'}, {id: '690', name: 'Skrelp'}, {id: '691', name: 'Dragalge'}, {id: '692', name: 'Clauncher'}, {id: '693', name: 'Clawitzer'}, {id: '694', name: 'Helioptile'}, {id: '695', name: 'Heliolisk'}, {id: '696', name: 'Tyrunt'}, {id: '697', name: 'Tyrantrum'}, {id: '698', name: 'Amaura'}, {id: '699', name: 'Aurorus'}, {id: '700', name: 'Sylveon'}, {id: '701', name: 'Hawlucha'}, {id: '702', name: 'Dedenne'}, {id: '703', name: 'Carbink'}, {id: '704', name: 'Goomy'}, {id: '705', name: 'Sliggoo'}, {id: '706', name: 'Goodra'}, {id: '707', name: 'Klefki'}, {id: '708', name: 'Phantump'}, {id: '709', name: 'Trevenant'}, {id: '710', name: 'Pumpkaboo'}, {id: '711', name: 'Gourgeist'}, {id: '712', name: 'Bergmite'}, {id: '713', name: 'Avalugg'}, {id: '714', name: 'Noibat'}, {id: '715', name: 'Noivern'}, {id: '716', name: 'Xerneas'}, {id: '717', name: 'Yveltal'}, {id: '718', name: 'Zygarde'}, {id: '719', name: 'Diancie'}, {id: '720', name: 'Hoopa'}, {id: '721', name: 'Volcanion'}, {id: '722', name: 'Rowlet'}, {id: '723', name: 'Dartrix'}, {id: '724', name: 'Decidueye'}, {id: '725', name: 'Litten'}, {id: '726', name: 'Torracat'}, {id: '727', name: 'Incineroar'}, {id: '728', name: 'Popplio'}, {id: '729', name: 'Brionne'}, {id: '730', name: 'Primarina'}, {id: '731', name: 'Pikipek'}, {id: '732', name: 'Trumbeak'}, {id: '733', name: 'Toucannon'}, {id: '734', name: 'Yungoos'}, {id: '735', name: 'Gumshoos'}, {id: '736', name: 'Grubbin'}, {id: '737', name: 'Charjabug'}, {id: '738', name: 'Vikavolt'}, {id: '739', name: 'Crabrawler'}, {id: '740', name: 'Crabominable'}, {id: '741', name: 'Oricorio'}, {id: '742', name: 'Cutiefly'}, {id: '743', name: 'Ribombee'}, {id: '744', name: 'Rockruff'}, {id: '745', name: 'Lycanroc'}, {id: '746', name: 'Wishiwashi'}, {id: '747', name: 'Mareanie'}, {id: '748', name: 'Toxapex'}, {id: '749', name: 'Mudbray'}, {id: '750', name: 'Mudsdale'}, {id: '751', name: 'Dewpider'}, {id: '752', name: 'Araquanid'}, {id: '753', name: 'Fomantis'}, {id: '754', name: 'Lurantis'}, {id: '755', name: 'Morelull'}, {id: '756', name: 'Shiinotic'}, {id: '757', name: 'Salandit'}, {id: '758', name: 'Salazzle'}, {id: '759', name: 'Stufful'}, {id: '760', name: 'Bewear'}, {id: '761', name: 'Bounsweet'}, {id: '762', name: 'Steenee'}, {id: '763', name: 'Tsareena'}, {id: '764', name: 'Comfey'}, {id: '765', name: 'Oranguru'}, {id: '766', name: 'Passimian'}, {id: '767', name: 'Wimpod'}, {id: '768', name: 'Golisopod'}, {id: '769', name: 'Sandygast'}, {id: '770', name: 'Palossand'}, {id: '771', name: 'Pyukumuku'}, {id: '772', name: 'Type: Null'}, {id: '773', name: 'Silvally'}, {id: '774', name: 'Minior'}, {id: '775', name: 'Komala'}, {id: '776', name: 'Turtonator'}, {id: '777', name: 'Togedemaru'}, {id: '778', name: 'Mimikyu'}, {id: '779', name: 'Bruxish'}, {id: '780', name: 'Drampa'}, {id: '781', name: 'Dhelmise'}, {id: '782', name: 'Jangmo-o'}, {id: '783', name: 'Hakamo-o'}, {id: '784', name: 'Kommo-o'}, {id: '785', name: 'Tapu Koko'}, {id: '786', name: 'Tapu Lele'}, {id: '787', name: 'Tapu Bulu'}, {id: '788', name: 'Tapu Fini'}, {id: '789', name: 'Cosmog'}, {id: '790', name: 'Cosmoem'}, {id: '791', name: 'Solgaleo'}, {id: '792', name: 'Lunala'}, {id: '793', name: 'Nihilego'}, {id: '794', name: 'Buzzwole'}, {id: '795', name: 'Pheromosa'}, {id: '796', name: 'Xurkitree'}, {id: '797', name: 'Celesteela'}, {id: '798', name: 'Kartana'}, {id: '799', name: 'Guzzlord'}, {id: '800', name: 'Necrozma'}, {id: '801', name: 'Magearna'}, {id: '802', name: 'Marshadow'}, {id: '803', name: 'Poipole'}, {id: '804', name: 'Naganadel'}, {id: '805', name: 'Stakataka'}, {id: '806', name: 'Blacephalon'}, {id: '807', name: 'Zeraora'}, {id: '808', name: 'Meltan'}, {id: '809', name: 'Melmetal'}, {id: '810', name: 'Grookey'}, {id: '811', name: 'Thwackey'}, {id: '812', name: 'Rillaboom'}, {id: '813', name: 'Scorbunny'}, {id: '814', name: 'Raboot'}, {id: '815', name: 'Cinderace'}, {id: '816', name: 'Sobble'}, {id: '817', name: 'Drizzile'}, {id: '818', name: 'Inteleon'}, {id: '819', name: 'Skwovet'}, {id: '820', name: 'Greedent'}, {id: '821', name: 'Rookidee'}, {id: '822', name: 'Corvisquire'}, {id: '823', name: 'Corviknight'}, {id: '824', name: 'Blipbug'}, {id: '825', name: 'Dottler'}, {id: '826', name: 'Orbeetle'}, {id: '827', name: 'Nickit'}, {id: '828', name: 'Thievul'}, {id: '829', name: 'Gossifleur'}, {id: '830', name: 'Eldegoss'}, {id: '831', name: 'Wooloo'}, {id: '832', name: 'Dubwool'}, {id: '833', name: 'Chewtle'}, {id: '834', name: 'Drednaw'}, {id: '835', name: 'Yamper'}, {id: '836', name: 'Boltund'}, {id: '837', name: 'Rolycoly'}, {id: '838', name: 'Carkol'}, {id: '839', name: 'Coalossal'}, {id: '840', name: 'Applin'}, {id: '841', name: 'Flapple'}, {id: '842', name: 'Appletun'}, {id: '843', name: 'Silicobra'}, {id: '844', name: 'Sandaconda'}, {id: '845', name: 'Cramorant'}, {id: '846', name: 'Arrokuda'}, {id: '847', name: 'Barraskewda'}, {id: '848', name: 'Toxel'}, {id: '849', name: 'Toxtricity'}, {id: '850', name: 'Sizzlipede'}, {id: '851', name: 'Centiskorch'}, {id: '852', name: 'Clobbopus'}, {id: '853', name: 'Grapploct'}, {id: '854', name: 'Sinistea'}, {id: '855', name: 'Polteageist'}, {id: '856', name: 'Hatenna'}, {id: '857', name: 'Hattrem'}, {id: '858', name: 'Hatterene'}, {id: '859', name: 'Impidimp'}, {id: '860', name: 'Morgrem'}, {id: '861', name: 'Grimmsnarl'}, {id: '862', name: 'Obstagoon'}, {id: '863', name: 'Perrserker'}, {id: '864', name: 'Cursola'}, {id: '865', name: "Sirfetch'd"}, {id: '866', name: 'Mr. Rime'}, {id: '867', name: 'Runerigus'}, {id: '868', name: 'Milcery'}, {id: '869', name: 'Alcremie'}, {id: '870', name: 'Falinks'}, {id: '871', name: 'Pincurchin'}, {id: '872', name: 'Snom'}, {id: '873', name: 'Frosmoth'}, {id: '874', name: 'Stonjourner'}, {id: '875', name: 'Eiscue'}, {id: '876', name: 'Indeedee'}, {id: '877', name: 'Morpeko'}, {id: '878', name: 'Cufant'}, {id: '879', name: 'Copperajah'}, {id: '880', name: 'Dracozolt'}, {id: '881', name: 'Arctozolt'}, {id: '882', name: 'Dracovish'}, {id: '883', name: 'Arctovish'}, {id: '884', name: 'Duraludon'}, {id: '885', name: 'Dreepy'}, {id: '886', name: 'Drakloak'}, {id: '887', name: 'Dragapult'}, {id: '888', name: 'Zacian'}, {id: '889', name: 'Zamazenta'}, {id: '890', name: 'Eternatus'},
      {id: '562-g', name: 'Galarian Yamask'}, {id: '618-g', name: 'Galarian Stunfisk'}, {id: '423-e', name: 'Gastrodon East'}, {id: '077-g', name: 'Galarian Ponyta'}, {id: '876-f', name: 'Female Indeedee'}, {id: '078-g', name: 'Galarian Rapidash'}, {id: '858-gi', name: 'Gigantamax Hatterene'}, {id: '422-e', name: 'Shellos East'}, {id: '263-g', name: 'Galarian Zigzagoon'}, {id: '264-g', name: 'Galarian Linoone'}, {id: '826-gi', name: 'Gigantamax Orbeetle'}, {id: '869-gi', name: 'Gigantamax Alcremie'}, {id: '841-gi', name: 'Gigantamax Flapple'}, {id: '842-gi', name: 'Gigantamax Appletun'}, {id: '083-g', 'name': "Galarian Farfetch'd"}, {'id': '861-gi', name: 'Gigantamax Grimmsnarl'}, {id: '844-gi', name: 'Gigantamax Sandaconda'}, {id: '052-g', name: 'Galarian Meowth'}, {id: '554-g', name: 'Galarian Darumaka'}, {id: '122-g', name: 'Galarian Mr. Mime'}, {id: '555-g', name: 'Galarian Darmanitan'}, {id: '110-g', name: 'Galarian Weezing'}, {id: '569-gi', name: 'Gigantamax Garbodor'}, {id: '823-gi', name: 'Gigantamax Corviknight'}, {id: '834-gi', name: 'Gigantamax Drednaw'}, {id: '222-g', name: 'Galarian Corsola'}, {id: '884-gi', name: 'Gigantamax Duraludon'}, {id: '839-gi', name: 'Gigantamax Coalossal'}, {id: '131-gi', name: 'Gigantamax Lapras'}, {id: '479-m', name: 'Mow Rotom'}, {id: '479-s', name: 'Fan Rotom'}, {id: '479-w', name: 'Wash Rotom'}, {id: '479-f', name: 'Frost Rotom'}, {id: '479-h', name: 'Heat Rotom'}, {id: '006-gi', name: 'Gigantamax Charizard'}, {id: '012-gi', name: 'Gigantamax Butterfree'}, {id: '099-gi', name: 'Gigantamax Kingler'}, {id: '879-gi', name: 'Gigantamax Copperajah'}, {id: '678-f', name: 'Female Meowstic'}, {id: '068-gi', name: 'Gigantamax Machamp'}, {id: '094-gi', name: 'Gigantamax Gengar'}, {id: '851-gi', name: 'Gigantamax Centiskorch'}]
    }
  },
  methods: {
    handleDrag({target, transform}) {
      target.style.transform = transform
    },
    handlePinchScale({target, delta}) {
      this.currentScale *= delta[0]
      this.$refs.wildAreaMap.style.transform = `scale(${this.currentScale})` + this.resetScale
    },
    remove (item) {
      console.log(this.searchIDs)
      const index = this.searchIDs.indexOf(item.id)
      if (index >= 0) this.searchIDs.splice(index, 1)
    },
    reset() {
      this.currentScale = 1.0
      this.$refs.moveableTarget.$el.style.transform = `translate(0px, 0px)` + this.resetTranslate
      this.$refs.wildAreaMap.style.transform = `scale(${this.currentScale})` + this.resetScale
    },
    scaleDown() {
      // minScale = 0.5
      if (this.currentScale > 0.5) {
        this.currentScale -= 0.5
      } else if (this.currentScale > 0.25) {
        this.currentScale = 0.25
      }
      this.$refs.wildAreaMap.style.transform = `scale(${this.currentScale})` + this.resetScale
    },
    scaleUp() {
      // maxScale = 3.0
      if (this.currentScale < 0.5) {
        this.currentScale = 0.5
      } else if (this.currentScale < 3.0) {
        this.currentScale += 0.5
      }
      this.$refs.wildAreaMap.style.transform = `scale(${this.currentScale})` + this.resetScale
    },
    closeSearchMenu() {
      this.$refs.searchMenu.isMenuActive = false
      this.$refs.denLocationElement.forEach(el => el.clearHover())
    }
  },
  mounted() {
    if (screen.width <= 768) {
      this.resetScale = `scale(${screen.width / 1500})`
      this.resetTranslate = `translate(-20px, ${screen.height / 8}px)`
    }
    this.reset()
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #b1cf4b;
  padding-bottom: 500px;
}
#searchBar {
  position: fixed;
  top: 20px; left: 100vw; margin-left: -30vw;
  width: 25vw;
  z-index: 99;
}
#controls {
  position: fixed;
  top: 100vh; margin-top: -15vh;
  left: 100vw; margin-left: -10vw;
  z-index: 99;
  width: 150px;
  background: #ffffff;
}
#footer {
  position: fixed;
  bottom: 0;
}
@media only screen and (max-width: 768px) {
  /* For mobile phones */
  #controls {
    margin-top: -15vh;
    margin-left: -90vw;
    width: 80vw;
  }
  #searchBar {
    width: 100vw;
    top: 30px;
    left: unset; margin-left: unset;
  }

  #footer {
    top: 0; width: 100vw; height: 30px;
    bottom: unset;
    overflow: visible;
  }
}
.cardBtn {
  padding: 10px;
  border: #000;
}

#wild-area-map {
  position: relative;
  transform-origin: top left;
  top: 15px;
  left: 10px;
}

.moveable-control,.moveable-line {
  display: none;
}
</style>
