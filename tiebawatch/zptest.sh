ls dat -rt | head -$1 | sed -e 's/^/dat\//' | xargs zp c3 dat"$1".b.zpaq
