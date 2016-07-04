psql postgres -c"select ba from tieba order by 关注 desc limit $1;" -F, -At | sed -e 's/吧$//'
