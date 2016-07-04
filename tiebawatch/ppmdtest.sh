ls dat -rt | head -$1 | sed -e 's/^/dat\//' | xargs ppmd e -m256 -o16 -r0 -fdat"$1".r0.ppm
