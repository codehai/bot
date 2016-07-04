a:
	while true; do wget \
		'http://m.tieba.com/mo/m?kw=%E9%AD%94%E5%85%BD%E4%B8%96%E7%95%8C&pn=0' -O "$$(date)-0.html" \
		'http://m.tieba.com/mo/m?kw=%E9%AD%94%E5%85%BD%E4%B8%96%E7%95%8C&pn=20' -O "$$(date)-1.html" \
		'http://m.tieba.com/mo/m?kw=%E9%AD%94%E5%85%BD%E4%B8%96%E7%95%8C&pn=40' -O "$$(date)-2.html"; \
		sleep 5; done
c:
	ls *.html -rt | xargs -d '\n' grep -l 东北90后二次元 -H -A 5 | tee wc
