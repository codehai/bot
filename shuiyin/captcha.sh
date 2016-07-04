#!/bin/bash
#counter=0
function rnd2() {
	if [ -z "$RANDOM" ] ; then
	SEED=`tr -cd 0-9 </dev/urandom | head -c 8`
	else
	SEED=$RANDOM
	fi
	RND_NUM=`echo $SEED $1 $2|awk '{srand($1);printf "%d",rand()*10000%($3-$2)+$2}'`
	echo $RND_NUM
}
let i=0;
for it in $1*.jpg;
{ 
	x=`gm identify -verbose $it | grep Geometry | head -1 | cut -f 2 -d ':'|cut -f 1 -d 'x'|cut -f 2 -d ' '`;
	y=`gm identify -verbose $it | grep Geometry | head -1 | cut -f 2 -d ':'|cut -f 2 -d 'x'|cut -f 1 -d '+'`;
	xmax=`expr $x \* 5 / 20`;
	ymax=`expr $y \* 8 / 20 `;
	fontx=$( rnd2 -$xmax  $xmax);
	fonty=$( rnd2 -$ymax $ymax);
	fontsize=$( rnd2 20 30);
	R=$( rnd2 0 255);
	G=$( rnd2 0 255);
	B=$( rnd2 0 255);
	rot=` echo $( rnd2 -30 30)  | bc  -l`;
	gm convert  $it   -encoding Unicode -font cu.ttf  -pointsize $fontsize -fill "rgb($R,$G,$B)" \
		-draw  "translate "$fontx","$fonty" rotate "$rot" gravity center text 0,0 \"任大包，一个神奇的公众号\"" $2$(echo $it | sed 's/.*\///')
	echo "{path:$it;xmax:$xmax;ymax:$ymax;fontsize:$fontsize;RGB:\"$R,$G,$B\";fontx:$fontx;fonty:$fonty}" >> shuiyin.json
}
