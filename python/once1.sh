set -ex
#psql -wU tiebabot0 hub -p 27213 -c "copy (select * from hub.active_tieba_login_sessions) to stdout with (format csv,delimiter ' ',escape '\\',FORCE_QUOTE *)" -tAF' ' # | xargs -n1 # | parallel --line-buffer -L3 'set -ex; ip netns exec {1} python open.py http://127.0.0.1:15678 {2} {3}'
psql -wU chatengine0 dev -p 27213 -c "copy (select 's1', cookies,un_ua::json->'ua' from login_cookie) to stdout with (format csv,delimiter ' ',escape '\\',FORCE_QUOTE *)" -tAF' ' | parallel --line-buffer 'set -ex; ip netns exec {1} python open.py http://127.0.0.1:15678 {2} {3} > $(date -In).log'
