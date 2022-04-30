load 'common.gnuplot'

plot 'log.csv' using 1:($4+$9) with lines ls 101 title 'Produktion', '' using 1:(-$14) with lines ls 102 title 'Batterie Ladung/Entladung'
