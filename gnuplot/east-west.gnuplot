load 'common.gnuplot'

plot 'log.csv' using 1:4 with lines ls 103, '' using 1:9 with lines ls 104
