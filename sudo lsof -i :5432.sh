sudo lsof -i :5432
sudo kill -9 279

psql -U postgres -d sparkifydb

brew install libpg-dev




sudo rm /tmp/.s.PGSQL.5432.lock
sudo rm /tmp/.s.PGSQL.5432

pg_ctl -D /usr/local/var/postgres start
alias pgb='pg_ctl -D /usr/local/var/postgres start'
source ~/.bash_profile
pgb

echo 'export PATH="/opt/homebrew/opt/libpq/bin:$PATH"' >> ~/.zshrc
export LDFLAGS="-L/opt/homebrew/opt/libpq/lib"
export CPPFLAGS="-I/opt/homebrew/opt/libpq/include"

brew install libpq