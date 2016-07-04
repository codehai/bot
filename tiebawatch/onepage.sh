#wget "http://m.tieba.com/mo/m?kw=$1&pn=$2" -O "$3$(date -Ins)-$1-$2.html"
curl "http://m.tieba.com/mo/m?kw=$1&pn=$2" \
	--max-time 2 --retry 0 \
	--connect-timeout 1 \
	-A 'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_2 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5' -s \
	--resolve 180.97.104.40:80:tieba.baidu.com \
	| tee "$3$(date -Ins)-$1-$2.html"


	#--max-time 10 \ --retry 3 \ --retry-delay 1 \ --retry-max-time 3 \
