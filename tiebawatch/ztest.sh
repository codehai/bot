ls dat -rt | head -$1 | sed -e 's/^/dat\//' | xargs tar czf dat"$1".tgz
