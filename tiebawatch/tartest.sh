ls dat -rt | head -$1 | sed -e 's/^/dat\//' | xargs tar cf dat"$1".tar
