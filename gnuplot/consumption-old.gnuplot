load 'common.gnuplot'

plot 'log.csv' using 1:($4+$9) with lines ls 103 title 'Produktion', '' using 1:46 with lines ls 102 title 'Verbrauch eigen', '' using 1:47 with lines ls 101 title 'Verbrauch Netz'
