#!/bin/bash

### berries (from https://www.serebii.net/itemdex/list/berry.shtml):
# e = document.getElementsByClassName('fooinfo')
# for (let i =0;i<e.length; i++) {
#   if (i%2 == 0) x.push(e[i].textContent.replace(/\s/g, '').toLowerCase())
# }
declare -a arr=("aguavberry" "apicotberry" "aspearberry" "babiriberry" "belueberry" "blukberry" "chartiberry" "cheriberry" "chestoberry" "chilanberry" "chopleberry" "cobaberry" "colburberry" "cornnberry" "custapberry" "durinberry" "enigmaberry" "figyberry" "ganlonberry" "goldennanabberry" "goldenpinapberry" "goldenrazzberry" "grepaberry" "habanberry" "hondewberry" "iapapaberry" "jabocaberry" "kasibberry" "kebiaberry" "keeberry" "kelpsyberry" "lansatberry" "leppaberry" "liechiberry" "lumberry" "magoberry" "magostberry" "marangaberry" "micleberry" "nanabberry" "nomelberry" "occaberry" "oranberry" "pamtreberry" "passhoberry" "payapaberry" "pechaberry" "persimberry" "petayaberry" "pinapberry" "pomegberry" "qualotberry" "rabutaberry" "rawstberry" "razzberry" "rindoberry" "roseliberry" "rowapberry" "salacberry" "shucaberry" "silvernanabberry" "silverpinapberry" "silverrazzberry" "sitrusberry" "spelonberry" "starfberry" "tamatoberry" "tangaberry" "wacanberry" "watmelberry" "wepearberry" "wikiberry" "yacheberry")
for i in "${arr[@]}"
do
  wget "serebii.net/itemdex/sprites/$i.png" 2> /dev/null
  echo "serebii.net/itemdex/sprites/$i.png"
done


for i in $(seq -f "%03g" 1 890)
do
  wget "serebii.net/pokedex-swsh/icon/$i.png" 2> /dev/null
  echo "serebii.net/pokedex-swsh/icon/$i.png"
done

### special Pokemon:
declare -a arr=("215" "605" "176" "749" "776" "575" "886" "271" "710" "842-gi" "532" "012" "226" "044" "879" "675" "281" "270" "635" "459" "678-f" "171" "170" "614" "613" "436" "143" "477" "576" "743" "835" "864" "836" "761" "134" "709" "195" "632" "423-e" "556" "439" "083-g" "035" "025" "865" "845" "841-gi" "095" "407" "870" "562-g" "859" "099" "468" "747" "708" "453" "094-gi" "050" "631" "338" "839-gi" "421" "610" "533" "420" "526" "573" "247" "342" "099-gi" "715" "595" "045" "535" "849" "278" "077-g" "479-h" "555-g" "038" "837" "458" "682" "275" "674" "067" "695" "839" "700" "782" "659" "557" "058" "092" "601" "752" "629" "324" "762" "479-w" "416" "320" "884-gi" "446" "519" "310" "037" "627" "538" "759" "554-g" "350" "819" "132" "246" "757" "763" "546" "068" "248" "784" "122-g" "211" "470" "517" "222-g" "694" "824" "309" "771" "873" "780" "426" "854" "622" "094" "612" "616" "527" "588" "012-gi" "876-f" "766" "415" "860" "175" "343" "851" "711" "448" "598" "093" "852" "851-gi" "273" "831" "750" "714" "529" "777" "164" "213" "051" "558" "686" "778" "302" "885" "460" "321" "220" "855" "135" "263-g" "434" "783" "584" "315" "136" "825" "768" "208" "844" "005" "683" "876" "569-gi" "866" "237" "349" "736" "599" "438" "858" "090" "572" "178" "678" "751" "578" "356" "756" "537" "834-gi" "052-g" "479-f" "853" "844-gi" "422-e" "026" "559" "568" "596" "437" "475" "826" "036" "066" "264-g" "874" "574" "830" "628" "560" "593" "828" "435" "834" "861" "861-gi" "225" "182" "872" "280" "838" "679" "196" "131-gi" "509" "589" "473" "677" "011" "577" "712" "832" "843" "129" "194" "862" "887" "600" "528" "701" "746" "078-g" "871" "291" "846" "561" "858-gi" "705" "826-gi" "450" "611" "177" "521" "856" "328" "840" "867" "068-gi" "884" "634" "850" "344" "221" "530" "569" "478" "163" "738" "006-gi" "742" "362" "133" "112" "329" "464" "111" "758" "290" "539" "510" "848" "869" "767" "110-g" "006" "185" "272" "292" "869-gi" "681" "583" "223" "625" "748" "518" "822" "833" "685" "339" "688" "043" "623" "449" "340" "461" "524" "689" "355" "550" "536" "341" "823-gi" "091" "447" "547" "765" "330" "173" "579" "842" "680" "279" "684" "406" "131" "660" "704" "823" "592" "609" "755" "109" "525" "098" "633" "608" "868" "827" "520" "829" "471" "863" "781" "624" "202" "425" "879-gi" "361" "172" "452" "737" "630" "010" "224" "004" "106" "857" "617" "197" "337" "597" "841" "107" "821" "582" "282" "360" "760" "877" "303" "878" "236" "059" "847" "274" "479-s" "130" "820" "875" "479-m" "451" "687" "618-g" "713" "706" "534" "454" "607")
for i in "${arr[@]}"
do
  wget "serebii.net/pokedex-swsh/icon/$i.png" 2> /dev/null
  echo "serebii.net/pokedex-swsh/icon/$i.png"
done
