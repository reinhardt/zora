set datafile separator ','
set xdata time
set timefmt "%Y-%m-%dT%H:%M:%S%z"
set format x "%d.%m. %H:%M:%S"

set key autotitle columnhead
set ylabel 'Leistung (W)'
set xlabel 'Zeit'
set xtics rotate

set style line 100 lt 1 lc rgb "grey" lw 0.5 # linestyle for the grid
set grid ls 100 # enable grid with specific linestyle
set style line 101 lw 2 lt rgb "#d63f00"
set style line 102 lw 2 lt rgb "#88bf4d"
set style line 103 lw 2 lt rgb "#4c5773"
set style line 104 lw 2 lt rgb "#509ee3"
set style line 105 lw 2 lt rgb "#ef8c8c"
set style line 114 lw 2 lt rgb "#98d9d9"
set style line 115 lw 2 lt rgb "#f2a86f"
