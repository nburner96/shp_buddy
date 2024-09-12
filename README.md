# SHP Buddy
SHP Buddy is a QGIS plugin that provides an quick and intuitive method for generating shapefiles for common plant breeding experiment designs. SHP Buddy lays out plots in a serpentine pattern and can account for fill plots and wheel tracks. Plot sizes are adjustable to exclude things such as adjacent plots and alleyways from the regions of interest. SHP Buddy provides an easy method for integrating field book information such as line names, pedigrees, and trait notes into the final shapefile for convenient identification and viewing. SHP Buddy works out-of-the-box in QGIS and does not require additional package or script installations. 

# Plot Layout and Numbering
Plots are laid out in a serpentine pattern, beginning at the bottom left of the shapefile and working its way across each range before moving up to the next range. Experiments with less than 100 plots will be numbered using the "RPP" format, where R is the rep number, and PP is the 2-digit plot number. Ex: a 3 rep experiment with 20 plots each is numbered 101-120, 201-220, and 301-330. 

Each plot in an experiment with 100 or more plots were rep is given a 4 digit plot number in the "RPPP" format. Ex: a 3 rep experiment with 200 plots each is numbered 1001-1200, 2001-2200, and 3001-3200.

Fill plots, if specified, are place after the last plot in each rep (see tutorial below).

# Tutorial
This example will walk through how to make a shapefile for the following experiment map:

![image](https://github.com/user-attachments/assets/1478a0df-118d-4df4-8e12-af6198452a73)

This experiment consists of 3 reps with 30 plots each. The experiment is 4 plots across and 26 ranges deep. Each rep ends with 2 fill plots and ranges 9 and 18 have a wheel track (and are fill plots). Each plot is 20 x 10 ft, however in this example we will trim 5 and 2.5 ft from each side of the length and width, respectively

SHP Buddy can be accessed from two locations in QGIS: the vector dropdown or the plugin toolbar:

![image](https://github.com/user-attachments/assets/414f63a4-5b6a-4c9c-9506-c162bc813753)

A dialog window will pop up where you can enter test specifications. Most sections are fairly self-explanatory, please see accompanying notes for further clarification:

1. Name of the experiment
2. Plots per rep and number of reps. Plots per rep value should exclude fill plots that are not in wheel tracks (see below)
3. Dimensions of experiment in terms of plots. Rows is the total number of plots across each range, ranges is the total number of ranges (including wheel track ranges)
4. Number of fill plots after each rep. Expressed as a comma separated list. List length must equal Reps value (specify 0 if a rep is not followed by fills).
5. Wheel track ranges. A list of numbers indicating which ranges (starting from the front of the field) are in wheel tracks and are planted with fills. In the example, ranges 9 and 18 are wheel track ranges.


6. Plot tracker. This displays the number of different types of plots specified to help identify the source of potential dimension errors. Specified plots is the total number of experimental and fill plots (including those in wheel tracks). Required plots is the total footprint (in plots) of the experiment as calculated by Rows x Ranges.
7. Total plot dimensions. Includes all rows and alleyways for each plot.
8. Plot buffers. Specifies how much to trim off of each side of the length and width. In the example, we want to only look at the middle two rows (2.5 ft. row spacing) for each plot and exclude alleyways.
9. Plot units. Currently feet and meters are available.

10. Field book upload. Specify a CSV file containing fieldbook information. The only requirement is that the first row is the header. Below is an example of a typical field book:

11. Specify which header corresponds to the Plot ID column.
12. Column selection. This section appears only if a field book file is specified. Select the columns that you want to add to the shapefile.



