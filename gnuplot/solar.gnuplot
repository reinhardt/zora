set datafile separator '\t'
set xdata time
set timefmt "%s"
set format x "%d.%m. %H:%M:%S"

set key autotitle columnhead
set ylabel 'Leistung (W)'
set xlabel 'Zeit'
set xtics rotate

set style line 100 lt 1 lc rgb "grey" lw 0.5 # linestyle for the grid
set grid ls 100 # enable grid with specific linestyle
set style line 101 lw 3 lt rgb "#d63f00"
set style line 102 lw 3 lt rgb "#26dfd0"

plot 'log.csv' using 1:4 with lines, '' using 1:9 with lines
plot 'log.csv' using 1:($4+$9) with lines ls 101 title 'Produktion', '' using 1:(-$14) with lines ls 102 title 'Batterie Ladung/Entladung'
