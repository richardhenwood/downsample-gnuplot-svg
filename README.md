# Downsample a Gnuplot SVG figure

Do you have a multi-MB gnuplot SVG you would like to share? Use this tool to drastically reduce the file size.

## About Gnuplot

[Gnuplot](http://www.gnuplot.info/) is a high performance scientific graphing utility. It has been in continuous development since 1986 and is in my opinion the best available tool for visualizing many datasets.

## SVG Output and File Size

Gnuplot supports many types of output. I have recently become interested in SVG because it renders in most browsers and it includes Hypertext support. I use hypertext support to allow my users to explore more about the data I'm sharing.
Gnuplot performs particularly well with high volumes of data. It can comfortably handle millions of observations. However, when millions of data points are rendered into an SVG, the resulting file can be inconveniently large. I can use PNG output, but the power of hypertext is lost.

## Lossy SVG Compression

The lossy SVG compression I have implemented in this repository works as follows:
 1. start with an SVG file produced by Gnuplot
 1. create a new SVG file that just has the hypertext and text values in it.
 1. render the origional svg file into a PNG file.
 1. add the PNG rendering into the SVG file with the hypertext as a background.

This is lossy compression because the PNG rendering rasterizes the vector information in the figure. Rasterizing converts vector (line) information to pixel information. If you zoom into a figure after lossy compression you will see the pixels of the PNG.

## Notes

 * Compression is effective if you have a high ratio of points to text and hyperlinks.
 * libvips has been chosen for the rasterizing. It took ~70 minutes to rasterize a 77MB SVG file on my old laptop.
 * I initially used cariosvg but it fell-over rasterizing a 77MB SVG file.

## Todo
 * Add the ability to change rasterizing resolution.
 * Profile the code to understand where it spends most of it's time.
 * Improve performance of the rasterizing step.
