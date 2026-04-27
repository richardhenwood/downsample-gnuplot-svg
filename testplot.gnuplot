#
# Lattice test for random numbers;
# If you can see any patterns in this plot, the random number generator
# is not very good.
#
# Copyright (c) 1991, Jos van der Woude, jvdwoude@hut.nl

# History:
#	-  6. 6. 2006 ds: added univariate and multivariate normal example
#	- 10. 5. 2006 ds: added univariate and multivariate normal example
#	-  ?. ?  1991 jvdw: 1st version

set terminal svg size 600,400 dynamic enhanced font 'arial,10' mousing name "hypertext_1" butt dashlength 1.0  
set output 'testplot.svg'

unset key
set xrange [0: 1]
set yrange [0: 1]
set zrange [0: 1]
set title "Lattice test for random numbers"
set xlabel "rand(n) ->"      rotate parallel
set ylabel "rand(n + 1) ->"  rotate parallel offset 0,-1
set zlabel "rand(n + 2) ->"  rotate parallel offset 0,-1
set format x "%3.2f"
set format y "%3.2f"
set format z "%3.2f"
set tics

# Adjust this value to increase the data points (and output SVG file)
set sample 100000

set style function dots
set parametric
set label at 0.5,0.5 "text in the middle" hypertext point pt 1
plot rand(0), rand(0)
