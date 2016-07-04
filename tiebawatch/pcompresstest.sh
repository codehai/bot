pcompress -a -l 14 $(ls dat -rt | head -$1 | sed -e 's/^/dat\//') dat"$1".pz
