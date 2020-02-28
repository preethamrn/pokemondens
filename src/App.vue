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
        <v-col cols='12'><v-card class='cardBtn' tile @click='reset'>RECENTER</v-card></v-col>
      </v-row>
    </div>
    <pinch-zoom id='pinchzoom'>
      <div id='wild-area-map'>
        <img alt="Pokemon Wild Area Map" src="./assets/pokemon-wild-area.png" @touchstart='closeSearchMenu'>
        <DenLocation v-for="(den, index) in dens" :key="'den-'+index"
          :position='den.position'
          :commonDen='denPokemon[den.commonID]'
          :rareDen='denPokemon[den.rareID]'
          :gmax='denPokemon[den.rareID] && (denPokemon[den.commonID].gmax || denPokemon[den.rareID].gmax)'
          :screenshotImg='den.img'
          :searchIDs='searchIDs'
          ref='hoverableElement'/>
        <BerryTree v-for="(tree, index) in trees" :key="'berry-'+index"
          :position='tree.position'
          :treeBerries='tree.berries'
          :treePokemon='tree.pokemon'
          :treeInfo='tree.info'
          :screenshotImg='tree.img'
          :searchIDs='searchIDs'
          ref='hoverableElement'/>
      </div>
    </pinch-zoom>
    <v-footer id='footer'>
      <v-icon left>mdi-information</v-icon>
      <span>Credits: <a href='https://www.youtube.com/channel/UC7tKYiFtH_6HCBD4hh7hTWw'>preethamrn</a>, <a href='https://reddit.com/u/malixx92'>/u/Malixx92</a>, <a href='https://www.serebii.net/swordshield/maxraidbattledens.shtml'>Serebii</a></span>
    </v-footer>
  </div>
</template>

<script>
/* eslint-disable no-param-reassign,no-unused-expressions,no-unused-vars,no-console */
import DenLocation from './components/DenLocation.vue'
import BerryTree from './components/BerryTree.vue'
import './components/pinch-zoom'

export default {
  name: 'app',
  components: {
    DenLocation,
    BerryTree,
  },
  data() {
    return {
      // support reset pinch-zoom --x,--y,--scale attributes
      resetScale: 1.0,
      resetTranslate: {
        x: 0,
        y: 0,
      },

      // Pokemon searching
      searchIDs: [],

      // den data (immutable)
      trees: [
        {info: {name: "Axew's Eye", link: "https://www.serebii.net/pokearth/galar/axew'seye.shtml"}, berries: ['salacberry', 'lumberry', 'keeberry', 'marangaberry', 'kebiaberry', 'colburberry'], pokemon: ['819', '420'], img: "https://www.serebii.net/swordshield/berry/axew'seye.jpg", position: {x: 645, y: 1480}},
        {info: {name: 'Bridge Field', link: 'https://www.serebii.net/pokearth/galar/bridgefield.shtml'}, berries: ['kelpsyberry', 'qualotberry', 'sitrusberry', 'passhoberry', 'wikiberry', 'leftovers'], pokemon: ['819', '420'], img: 'https://www.serebii.net/swordshield/berry/bridgefield1.jpg', position: {x: 1000, y: 813}},
        {info: {name: 'Bridge Field', link: 'https://www.serebii.net/pokearth/galar/bridgefield.shtml'}, berries: ['pomegberry', 'tamatoberry', 'sitrusberry', 'occaberry', 'figyberry', 'leftovers'], pokemon: ['819', '420'], img: 'https://www.serebii.net/swordshield/berry/bridgefield2.jpg', position: {x: 960, y: 813}},
        {info: {name: 'Bridge Field', link: 'https://www.serebii.net/pokearth/galar/bridgefield.shtml'}, berries: ['hondewberry', 'grepaberry', 'sitrusberry', 'rindoberry', 'aguavberry', 'leftovers'], pokemon: ['819', '420'], img: 'https://www.serebii.net/swordshield/berry/bridgefield3.jpg', position: {x: 920, y: 813}},
        {info: {name: 'Bridge Field', link: 'https://www.serebii.net/pokearth/galar/bridgefield.shtml'}, berries: ['ganlonberry', 'liechiberry', 'roseliberry', 'babiriberry', 'chopleberry', 'kasibberry', 'leftovers'], pokemon: ['819', '420'], img: 'https://www.serebii.net/swordshield/berry/bridgefield4.jpg', position: {x: 1022, y: 950}},
        {info: {name: 'Dappled Grove', link: 'https://www.serebii.net/pokearth/galar/dappledgrove.shtml'}, berries: ['oranberry', 'chestoberry', 'pechaberry', 'persimberry'], pokemon: ['819', '420'], img: 'https://www.serebii.net/swordshield/berry/dappledgrove1.jpg', position: {x: 193, y: 1697}},
        {info: {name: 'Dappled Grove', link: 'https://www.serebii.net/pokearth/galar/dappledgrove.shtml'}, berries: ['oranberry', 'chestoberry', 'rawstberry', 'pomegberry', 'pechaberry'], pokemon: ['819', '420'], img: 'https://www.serebii.net/swordshield/berry/dappledgrove2.jpg', position: {x: 164, y: 1643}},
        {info: {name: 'Dappled Grove', link: 'https://www.serebii.net/pokearth/galar/dappledgrove.shtml'}, berries: ['chestoberry', 'rawstberry', 'leppaberry', 'chilanberry', 'grepaberry'], pokemon: ['819', '420'], img: 'https://www.serebii.net/swordshield/berry/dappledgrove3.jpg', position: {x: 293, y: 1545}},
        {info: {name: 'Dappled Grove', link: 'https://www.serebii.net/pokearth/galar/dappledgrove.shtml'}, berries: ['pechaberry', 'rawstberry', 'oranberry', 'chilanberry', 'apicotberry'], pokemon: ['819', '420'], img: 'https://www.serebii.net/swordshield/berry/dappledgrove4.jpg', position: {x: 287, y: 1486}},
        {info: {name: "Giant's Cap", link: "https://www.serebii.net/pokearth/galar/giant'scap.shtml"}, berries: ['ganlonberry', 'tamatoberry', 'qualotberry', 'apicotberry', 'lumberry', 'leftovers'], pokemon: ['819', '420'], img: "https://www.serebii.net/swordshield/berry/giant'scap.jpg", position: {x: 688, y: 504}},
        {info: {name: "Giant's Mirror", link: "https://www.serebii.net/pokearth/galar/giant'smirror.shtml"}, berries: ['kelpsyberry', 'hondewberry', 'tamatoberry', 'pomegberry', 'qualotberry', 'grepaberry', 'leftovers'], pokemon: ['819', '420'], img: "https://www.serebii.net/swordshield/berry/giant'smirror.jpg", position: {x: 1306, y: 394}},
        {info: {name: "Giant's Seat", link: "https://www.serebii.net/pokearth/galar/giant'sseat.shtml"}, berries: ['sitrusberry', 'chestoberry', 'aspearberry', 'leppaberry', 'qualotberry', 'ganlonberry'], pokemon: ['819', '420'], img: "https://www.serebii.net/swordshield/berry/giant'sseat.jpg", position: {x: 1175, y: 1678}},
        {info: {name: 'Hammerlocke Hills', link: 'https://www.serebii.net/pokearth/galar/hammerlockehills.shtml'}, berries: ['sitrusberry', 'kelpsyberry', 'hondewberry', 'iapapaberry', 'magoberry', 'leftovers'], pokemon: ['819', '420'], img: 'https://www.serebii.net/swordshield/berry/hammerlockehills1.jpg', position: {x: 980, y: 226}},
        {info: {name: 'Hammerlocke Hills', link: 'https://www.serebii.net/pokearth/galar/hammerlockehills.shtml'}, berries: ['leppaberry', 'pomegberry', 'grepaberry', 'wacanberry', 'petayaberry', 'leftovers'], pokemon: ['819', '420'], img: 'https://www.serebii.net/swordshield/berry/hammerlockehills2.jpg', position: {x: 792, y: 132}},
        {info: {name: 'Lake of Outrage', link: 'https://www.serebii.net/pokearth/galar/lakeofoutrage.shtml'}, berries: ['apicotberry', 'petayaberry', 'habanberry', 'yacheberry', 'chartiberry', 'shucaberry', 'leftovers'], pokemon: ['819', '420'], img: 'https://www.serebii.net/swordshield/berry/lakeofoutrage.jpg', position: {x: 741, y: 143}},
        {info: {name: 'Motostoke Riverbank', link: 'https://www.serebii.net/pokearth/galar/motostokeriverbank.shtml'}, berries: ['sitrusberry', 'leppaberry', 'tangaberry', 'cobaberry', 'salacberry', 'leftovers'], pokemon: ['819', '420'], img: 'https://www.serebii.net/swordshield/berry/motostokeriverbank1.jpg', position: {x: 1055, y: 1204}},
        {info: {name: 'Motostoke Riverbank', link: 'https://www.serebii.net/pokearth/galar/motostokeriverbank.shtml'}, berries: ['pomegberry', 'grepaberry', 'qualotberry', 'kelpsyberry', 'hondewberry', 'tamatoberry', 'leftovers'], pokemon: ['819', '420'], img: 'https://www.serebii.net/swordshield/berry/motostokeriverbank2.jpg', position: {x: 823, y: 1136}},
        {info: {name: 'North Lake Miloch', link: 'https://www.serebii.net/pokearth/galar/northlakemiloch.shtml'}, berries: ['rawstberry', 'persimberry', 'hondewberry', 'aspearberry', 'petayaberry'], pokemon: ['819', '819', '420'], img: 'https://www.serebii.net/swordshield/berry/northlakemiloch.jpg', position: {x: 1123, y: 1272}},
        {info: {name: 'Rolling Fields', link: 'https://www.serebii.net/pokearth/galar/rollingfields.shtml'}, berries: ['oranberry', 'pechaberry', 'cheriberry'], pokemon: ['819', '420'], img: 'https://www.serebii.net/swordshield/berry/rollingfields1.jpg', position: {x: 675, y: 1739}},
        {info: {name: 'Rolling Fields', link: 'https://www.serebii.net/pokearth/galar/rollingfields.shtml'}, berries: ['oranberry', 'persimberry', 'cheriberry', 'kelpsyberry'], pokemon: ['819', '420'], img: 'https://www.serebii.net/swordshield/berry/rollingfields2.jpg', position: {x: 373, y: 1670}},
        {info: {name: 'Watchtower Ruins', link: 'https://www.serebii.net/pokearth/galar/watchtowerruins.shtml'}, berries: ['sitrusberry', 'leppaberry', 'oranberry', 'cheriberry', 'rawstberry', 'liechiberry'], pokemon: ['819', '420'], img: 'https://www.serebii.net/swordshield/berry/watchtowerruins.jpg', position: {x: 305, y: 1357}},
      ],
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
      allPokemon: [{id: '004', name: 'Charmander'}, {id: '005', name: 'Charmeleon'}, {id: '006', name: 'Charizard'}, {id: '006-gi', name: 'Gigantamax Charizard'}, {id: '010', name: 'Caterpie'}, {id: '011', name: 'Metapod'}, {id: '012', name: 'Butterfree'}, {id: '012-gi', name: 'Gigantamax Butterfree'}, {id: '025', name: 'Pikachu'}, {id: '026', name: 'Raichu'}, {id: '035', name: 'Clefairy'}, {id: '036', name: 'Clefable'}, {id: '037', name: 'Vulpix'}, {id: '038', name: 'Ninetales'}, {id: '043', name: 'Oddish'}, {id: '044', name: 'Gloom'}, {id: '045', name: 'Vileplume'}, {id: '050', name: 'Diglett'}, {id: '051', name: 'Dugtrio'}, {id: '052-g', name: 'Galarian Meowth'}, {id: '058', name: 'Growlithe'}, {id: '059', name: 'Arcanine'}, {id: '066', name: 'Machop'}, {id: '067', name: 'Machoke'}, {id: '068', name: 'Machamp'}, {id: '068-gi', name: 'Gigantamax Machamp'}, {id: '077-g', name: 'Galarian Ponyta'}, {id: '078-g', name: 'Galarian Rapidash'}, {id: '083-g', name: "Galarian Farfetch'd"}, {id: '090', name: 'Shellder'}, {id: '091', name: 'Cloyster'}, {id: '092', name: 'Gastly'}, {id: '093', name: 'Haunter'}, {id: '094', name: 'Gengar'}, {id: '094-gi', name: 'Gigantamax Gengar'}, {id: '095', name: 'Onix'}, {id: '098', name: 'Krabby'}, {id: '099', name: 'Kingler'}, {id: '099-gi', name: 'Gigantamax Kingler'}, {id: '106', name: 'Hitmonlee'}, {id: '107', name: 'Hitmonchan'}, {id: '109', name: 'Koffing'}, {id: '110-g', name: 'Galarian Weezing'}, {id: '111', name: 'Rhyhorn'}, {id: '112', name: 'Rhydon'}, {id: '122-g', name: 'Galarian Mr. Mime'}, {id: '129', name: 'Magikarp'}, {id: '130', name: 'Gyarados'}, {id: '131', name: 'Lapras'}, {id: '131-gi', name: 'Gigantamax Lapras'}, {id: '132', name: 'Ditto'}, {id: '133', name: 'Eevee'}, {id: '134', name: 'Vaporeon'}, {id: '135', name: 'Jolteon'}, {id: '136', name: 'Flareon'}, {id: '143', name: 'Snorlax'}, {id: '163', name: 'Hoothoot'}, {id: '164', name: 'Noctowl'}, {id: '170', name: 'Chinchou'}, {id: '171', name: 'Lanturn'}, {id: '172', name: 'Pichu'}, {id: '173', name: 'Cleffa'}, {id: '175', name: 'Togepi'}, {id: '176', name: 'Togetic'}, {id: '177', name: 'Natu'}, {id: '178', name: 'Xatu'}, {id: '182', name: 'Bellossom'}, {id: '185', name: 'Sudowoodo'}, {id: '194', name: 'Wooper'}, {id: '195', name: 'Quagsire'}, {id: '196', name: 'Espeon'}, {id: '197', name: 'Umbreon'}, {id: '202', name: 'Wobbuffet'}, {id: '208', name: 'Steelix'}, {id: '211', name: 'Qwilfish'}, {id: '213', name: 'Shuckle'}, {id: '215', name: 'Sneasel'}, {id: '220', name: 'Swinub'}, {id: '221', name: 'Piloswine'}, {id: '222-g', name: 'Galarian Corsola'}, {id: '223', name: 'Remoraid'}, {id: '224', name: 'Octillery'}, {id: '225', name: 'Delibird'}, {id: '226', name: 'Mantine'}, {id: '236', name: 'Tyrogue'}, {id: '237', name: 'Hitmontop'}, {id: '246', name: 'Larvitar'}, {id: '247', name: 'Pupitar'}, {id: '248', name: 'Tyranitar'}, {id: '263-g', name: 'Galarian Zigzagoon'}, {id: '264-g', name: 'Galarian Linoone'}, {id: '270', name: 'Lotad'}, {id: '271', name: 'Lombre'}, {id: '272', name: 'Ludicolo'}, {id: '273', name: 'Seedot'}, {id: '274', name: 'Nuzleaf'}, {id: '275', name: 'Shiftry'}, {id: '278', name: 'Wingull'}, {id: '279', name: 'Pelipper'}, {id: '280', name: 'Ralts'}, {id: '281', name: 'Kirlia'}, {id: '282', name: 'Gardevoir'}, {id: '290', name: 'Nincada'}, {id: '291', name: 'Ninjask'}, {id: '292', name: 'Shedinja'}, {id: '302', name: 'Sableye'}, {id: '303', name: 'Mawile'}, {id: '309', name: 'Electrike'}, {id: '310', name: 'Manectric'}, {id: '315', name: 'Roselia'}, {id: '320', name: 'Wailmer'}, {id: '321', name: 'Wailord'}, {id: '324', name: 'Torkoal'}, {id: '328', name: 'Trapinch'}, {id: '329', name: 'Vibrava'}, {id: '330', name: 'Flygon'}, {id: '337', name: 'Lunatone'}, {id: '338', name: 'Solrock'}, {id: '339', name: 'Barboach'}, {id: '340', name: 'Whiscash'}, {id: '341', name: 'Corphish'}, {id: '342', name: 'Crawdaunt'}, {id: '343', name: 'Baltoy'}, {id: '344', name: 'Claydol'}, {id: '349', name: 'Feebas'}, {id: '350', name: 'Milotic'}, {id: '355', name: 'Duskull'}, {id: '356', name: 'Dusclops'}, {id: '360', name: 'Wynaut'}, {id: '361', name: 'Snorunt'}, {id: '362', name: 'Glalie'}, {id: '406', name: 'Budew'}, {id: '407', name: 'Roserade'}, {id: '415', name: 'Combee'}, {id: '416', name: 'Vespiquen'}, {id: '420', name: 'Cherubi'}, {id: '421', name: 'Cherrim'}, {id: '422-e', name: 'Shellos East'}, {id: '423-e', name: 'Gastrodon East'}, {id: '425', name: 'Drifloon'}, {id: '426', name: 'Drifblim'}, {id: '434', name: 'Stunky'}, {id: '435', name: 'Skuntank'}, {id: '436', name: 'Bronzor'}, {id: '437', name: 'Bronzong'}, {id: '438', name: 'Bonsly'}, {id: '439', name: 'Mime Jr.'}, {id: '446', name: 'Munchlax'}, {id: '447', name: 'Riolu'}, {id: '448', name: 'Lucario'}, {id: '449', name: 'Hippopotas'}, {id: '450', name: 'Hippowdon'}, {id: '451', name: 'Skorupi'}, {id: '452', name: 'Drapion'}, {id: '453', name: 'Croagunk'}, {id: '454', name: 'Toxicroak'}, {id: '458', name: 'Mantyke'}, {id: '459', name: 'Snover'}, {id: '460', name: 'Abomasnow'}, {id: '461', name: 'Weavile'}, {id: '464', name: 'Rhyperior'}, {id: '468', name: 'Togekiss'}, {id: '470', name: 'Leafeon'}, {id: '471', name: 'Glaceon'}, {id: '473', name: 'Mamoswine'}, {id: '475', name: 'Gallade'}, {id: '477', name: 'Dusknoir'}, {id: '478', name: 'Froslass'}, {id: '479-f', name: 'Frost Rotom'}, {id: '479-h', name: 'Heat Rotom'}, {id: '479-m', name: 'Mow Rotom'}, {id: '479-s', name: 'Fan Rotom'}, {id: '479-w', name: 'Wash Rotom'}, {id: '509', name: 'Purrloin'}, {id: '510', name: 'Liepard'}, {id: '517', name: 'Munna'}, {id: '518', name: 'Musharna'}, {id: '519', name: 'Pidove'}, {id: '520', name: 'Tranquill'}, {id: '521', name: 'Unfezant'}, {id: '524', name: 'Roggenrola'}, {id: '525', name: 'Boldore'}, {id: '526', name: 'Gigalith'}, {id: '527', name: 'Woobat'}, {id: '528', name: 'Swoobat'}, {id: '529', name: 'Drilbur'}, {id: '530', name: 'Excadrill'}, {id: '532', name: 'Timburr'}, {id: '533', name: 'Gurdurr'}, {id: '534', name: 'Conkeldurr'}, {id: '535', name: 'Tympole'}, {id: '536', name: 'Palpitoad'}, {id: '537', name: 'Seismitoad'}, {id: '538', name: 'Throh'}, {id: '539', name: 'Sawk'}, {id: '546', name: 'Cottonee'}, {id: '547', name: 'Whimsicott'}, {id: '550', name: 'Basculin'}, {id: '554-g', name: 'Galarian Darumaka'}, {id: '555-g', name: 'Galarian Darmanitan'}, {id: '556', name: 'Maractus'}, {id: '557', name: 'Dwebble'}, {id: '558', name: 'Crustle'}, {id: '559', name: 'Scraggy'}, {id: '560', name: 'Scrafty'}, {id: '561', name: 'Sigilyph'}, {id: '562-g', name: 'Galarian Yamask'}, {id: '568', name: 'Trubbish'}, {id: '569', name: 'Garbodor'}, {id: '569-gi', name: 'Gigantamax Garbodor'}, {id: '572', name: 'Minccino'}, {id: '573', name: 'Cinccino'}, {id: '574', name: 'Gothita'}, {id: '575', name: 'Gothorita'}, {id: '576', name: 'Gothitelle'}, {id: '577', name: 'Solosis'}, {id: '578', name: 'Duosion'}, {id: '579', name: 'Reuniclus'}, {id: '582', name: 'Vanillite'}, {id: '583', name: 'Vanillish'}, {id: '584', name: 'Vanilluxe'}, {id: '588', name: 'Karrablast'}, {id: '589', name: 'Escavalier'}, {id: '592', name: 'Frillish'}, {id: '593', name: 'Jellicent'}, {id: '595', name: 'Joltik'}, {id: '596', name: 'Galvantula'}, {id: '597', name: 'Ferroseed'}, {id: '598', name: 'Ferrothorn'}, {id: '599', name: 'Klink'}, {id: '600', name: 'Klang'}, {id: '601', name: 'Klinklang'}, {id: '605', name: 'Elgyem'}, {id: '607', name: 'Litwick'}, {id: '608', name: 'Lampent'}, {id: '609', name: 'Chandelure'}, {id: '610', name: 'Axew'}, {id: '611', name: 'Fraxure'}, {id: '612', name: 'Haxorus'}, {id: '613', name: 'Cubchoo'}, {id: '614', name: 'Beartic'}, {id: '616', name: 'Shelmet'}, {id: '617', name: 'Accelgor'}, {id: '618-g', name: 'Galarian Stunfisk'}, {id: '622', name: 'Golett'}, {id: '623', name: 'Golurk'}, {id: '624', name: 'Pawniard'}, {id: '625', name: 'Bisharp'}, {id: '627', name: 'Rufflet'}, {id: '628', name: 'Braviary'}, {id: '629', name: 'Vullaby'}, {id: '630', name: 'Mandibuzz'}, {id: '631', name: 'Heatmor'}, {id: '632', name: 'Durant'}, {id: '633', name: 'Deino'}, {id: '634', name: 'Zweilous'}, {id: '635', name: 'Hydreigon'}, {id: '659', name: 'Bunnelby'}, {id: '660', name: 'Diggersby'}, {id: '674', name: 'Pancham'}, {id: '675', name: 'Pangoro'}, {id: '677', name: 'Espurr'}, {id: '678', name: 'Meowstic'}, {id: '678-f', name: 'Female Meowstic'}, {id: '679', name: 'Honedge'}, {id: '680', name: 'Doublade'}, {id: '681', name: 'Aegislash'}, {id: '682', name: 'Spritzee'}, {id: '683', name: 'Aromatisse'}, {id: '684', name: 'Swirlix'}, {id: '685', name: 'Slurpuff'}, {id: '686', name: 'Inkay'}, {id: '687', name: 'Malamar'}, {id: '688', name: 'Binacle'}, {id: '689', name: 'Barbaracle'}, {id: '694', name: 'Helioptile'}, {id: '695', name: 'Heliolisk'}, {id: '700', name: 'Sylveon'}, {id: '701', name: 'Hawlucha'}, {id: '704', name: 'Goomy'}, {id: '705', name: 'Sliggoo'}, {id: '706', name: 'Goodra'}, {id: '708', name: 'Phantump'}, {id: '709', name: 'Trevenant'}, {id: '710', name: 'Pumpkaboo'}, {id: '711', name: 'Gourgeist'}, {id: '712', name: 'Bergmite'}, {id: '713', name: 'Avalugg'}, {id: '714', name: 'Noibat'}, {id: '715', name: 'Noivern'}, {id: '736', name: 'Grubbin'}, {id: '737', name: 'Charjabug'}, {id: '738', name: 'Vikavolt'}, {id: '742', name: 'Cutiefly'}, {id: '743', name: 'Ribombee'}, {id: '746', name: 'Wishiwashi'}, {id: '747', name: 'Mareanie'}, {id: '748', name: 'Toxapex'}, {id: '749', name: 'Mudbray'}, {id: '750', name: 'Mudsdale'}, {id: '751', name: 'Dewpider'}, {id: '752', name: 'Araquanid'}, {id: '755', name: 'Morelull'}, {id: '756', name: 'Shiinotic'}, {id: '757', name: 'Salandit'}, {id: '758', name: 'Salazzle'}, {id: '759', name: 'Stufful'}, {id: '760', name: 'Bewear'}, {id: '761', name: 'Bounsweet'}, {id: '762', name: 'Steenee'}, {id: '763', name: 'Tsareena'}, {id: '765', name: 'Oranguru'}, {id: '766', name: 'Passimian'}, {id: '767', name: 'Wimpod'},
      {id: '768', name: 'Golisopod'}, {id: '771', name: 'Pyukumuku'}, {id: '776', name: 'Turtonator'}, {id: '777', name: 'Togedemaru'}, {id: '778', name: 'Mimikyu'}, {id: '780', name: 'Drampa'}, {id: '781', name: 'Dhelmise'}, {id: '782', name: 'Jangmo-o'}, {id: '783', name: 'Hakamo-o'}, {id: '784', name: 'Kommo-o'}, {id: '819', name: 'Skwovet'}, {id: '820', name: 'Greedent'}, {id: '821', name: 'Rookidee'}, {id: '822', name: 'Corvisquire'}, {id: '823', name: 'Corviknight'}, {id: '823-gi', name: 'Gigantamax Corviknight'}, {id: '824', name: 'Blipbug'}, {id: '825', name: 'Dottler'}, {id: '826', name: 'Orbeetle'}, {id: '826-gi', name: 'Gigantamax Orbeetle'}, {id: '827', name: 'Nickit'}, {id: '828', name: 'Thievul'}, {id: '829', name: 'Gossifleur'}, {id: '830', name: 'Eldegoss'}, {id: '831', name: 'Wooloo'}, {id: '832', name: 'Dubwool'}, {id: '833', name: 'Chewtle'}, {id: '834', name: 'Drednaw'}, {id: '834-gi', name: 'Gigantamax Drednaw'}, {id: '835', name: 'Yamper'}, {id: '836', name: 'Boltund'}, {id: '837', name: 'Rolycoly'}, {id: '838', name: 'Carkol'}, {id: '839', name: 'Coalossal'}, {id: '839-gi', name: 'Gigantamax Coalossal'}, {id: '840', name: 'Applin'}, {id: '841', name: 'Flapple'}, {id: '841-gi', name: 'Gigantamax Flapple'}, {id: '842', name: 'Appletun'}, {id: '842-gi', name: 'Gigantamax Appletun'}, {id: '843', name: 'Silicobra'}, {id: '844', name: 'Sandaconda'}, {id: '844-gi', name: 'Gigantamax Sandaconda'}, {id: '845', name: 'Cramorant'}, {id: '846', name: 'Arrokuda'}, {id: '847', name: 'Barraskewda'}, {id: '848', name: 'Toxel'}, {id: '849', name: 'Toxtricity'}, {id: '850', name: 'Sizzlipede'}, {id: '851', name: 'Centiskorch'}, {id: '851-gi', name: 'Gigantamax Centiskorch'}, {id: '852', name: 'Clobbopus'}, {id: '853', name: 'Grapploct'}, {id: '854', name: 'Sinistea'}, {id: '855', name: 'Polteageist'}, {id: '856', name: 'Hatenna'}, {id: '857', name: 'Hattrem'}, {id: '858', name: 'Hatterene'}, {id: '858-gi', name: 'Gigantamax Hatterene'}, {id: '859', name: 'Impidimp'}, {id: '860', name: 'Morgrem'}, {id: '861', name: 'Grimmsnarl'}, {id: '861-gi', name: 'Gigantamax Grimmsnarl'}, {id: '862', name: 'Obstagoon'}, {id: '863', name: 'Perrserker'}, {id: '864', name: 'Cursola'}, {id: '865', name: "Sirfetch'd"}, {id: '866', name: 'Mr. Rime'}, {id: '867', name: 'Runerigus'}, {id: '868', name: 'Milcery'}, {id: '869', name: 'Alcremie'}, {id: '869-gi', name: 'Gigantamax Alcremie'}, {id: '870', name: 'Falinks'}, {id: '871', name: 'Pincurchin'}, {id: '872', name: 'Snom'}, {id: '873', name: 'Frosmoth'}, {id: '874', name: 'Stonjourner'}, {id: '875', name: 'Eiscue'}, {id: '876', name: 'Indeedee'}, {id: '876-f', name: 'Female Indeedee'}, {id: '877', name: 'Morpeko'}, {id: '878', name: 'Cufant'}, {id: '879', name: 'Copperajah'}, {id: '879-gi', name: 'Gigantamax Copperajah'}, {id: '884', name: 'Duraludon'}, {id: '884-gi', name: 'Gigantamax Duraludon'}, {id: '885', name: 'Dreepy'}, {id: '886', name: 'Drakloak'}, {id: '887', name: 'Dragapult'},
      {id: 'aguavberry', name: 'Aguav Berry'}, {id: 'apicotberry', name: 'Apicot Berry'}, {id: 'aspearberry', name: 'Aspear Berry'}, {id: 'babiriberry', name: 'Babiri Berry'}, {id: 'chartiberry', name: 'Charti Berry'}, {id: 'cheriberry', name: 'Cheri Berry'}, {id: 'chestoberry', name: 'Chesto Berry'}, {id: 'chilanberry', name: 'Chilan Berry'}, {id: 'chopleberry', name: 'Chople Berry'}, {id: 'cobaberry', name: 'Coba Berry'}, {id: 'colburberry', name: 'Colbur Berry'}, {id: 'figyberry', name: 'Figy Berry'}, {id: 'ganlonberry', name: 'Ganlon Berry'}, {id: 'grepaberry', name: 'Grepa Berry'}, {id: 'habanberry', name: 'Haban Berry'}, {id: 'hondewberry', name: 'Hondew Berry'}, {id: 'iapapaberry', name: 'Iapapa Berry'}, {id: 'kasibberry', name: 'Kasib Berry'}, {id: 'kebiaberry', name: 'Kebia Berry'}, {id: 'keeberry', name: 'Kee Berry'}, {id: 'kelpsyberry', name: 'Kelpsy Berry'}, {id: 'leftovers', name: 'Leftovers'}, {id: 'leppaberry', name: 'Leppa Berry'}, {id: 'liechiberry', name: 'Liechi Berry'}, {id: 'lumberry', name: 'Lum Berry'}, {id: 'magoberry', name: 'Mago Berry'}, {id: 'marangaberry', name: 'Maranga Berry'}, {id: 'occaberry', name: 'Occa Berry'}, {id: 'oranberry', name: 'Oran Berry'}, {id: 'passhoberry', name: 'Passho Berry'}, {id: 'pechaberry', name: 'Pecha Berry'}, {id: 'persimberry', name: 'Persim Berry'}, {id: 'petayaberry', name: 'Petaya Berry'}, {id: 'pomegberry', name: 'Pomeg Berry'}, {id: 'qualotberry', name: 'Qualot Berry'}, {id: 'rawstberry', name: 'Rawst Berry'}, {id: 'rindoberry', name: 'Rindo Berry'}, {id: 'roseliberry', name: 'Roseli Berry'}, {id: 'salacberry', name: 'Salac Berry'}, {id: 'shucaberry', name: 'Shuca Berry'}, {id: 'sitrusberry', name: 'Sitrus Berry'}, {id: 'tamatoberry', name: 'Tamato Berry'}, {id: 'tangaberry', name: 'Tanga Berry'}, {id: 'wacanberry', name: 'Wacan Berry'}, {id: 'wikiberry', name: 'Wiki Berry'}, {id: 'yacheberry', name: 'Yache Berry'}],
    }
  },
  methods: {
    remove (item) {
      const index = this.searchIDs.indexOf(item.id)
      if (index >= 0) this.searchIDs.splice(index, 1)
    },
    reset() {
      const pinchZoom = document.querySelector('#pinchzoom')
      pinchZoom.setTransform({
        scale: this.resetScale,
        x: this.resetTranslate.x,
        y: this.resetTranslate.y,
        // Fire a 'change' event if values are different to current values
        allowChangeEvent: false,
      })
    },
    closeSearchMenu() {
      this.$refs.searchMenu.isMenuActive = false
      this.$refs.hoverableElement.forEach(el => el.clearHover())
    }
  },
  mounted() {
    if (screen.width <= 768) {
      this.resetScale = screen.width / 1500
      this.resetTranslate = {x: -20, y: screen.height / 8}
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
  display:inline-block
}
</style>
