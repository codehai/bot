ls dat -rt | head -$1 | sed -e 's/^/dat\//' | xargs zpaq vc/usr/share/doc/zpaq/examples/max.cfg dat"$1".a.zpaq
