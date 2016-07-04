./lsbas.sh 20 | parallel -u -j1 'seq 0 20 99 | parallel -u -j5 -IXXX "./onepage.sh {} XXX dat/ ; "; sleep 1' | pv > /dev/null
