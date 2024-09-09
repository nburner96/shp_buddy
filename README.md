# SHP Buddy
SHP Buddy is a QGIS plugin that provides an quick and intuitive method for generating shapefiles for common plant breeding experiment designs. SHP Buddy lays out plots in a serpentine pattern and can account for fill plots and wheel tracks. Plot sizes are adjustable to exclude things such as adjacent plots and alleyways from the regions of interest. SHP Buddy provides an easy method for integrating field book information such as line names, pedigrees, and trait notes into the final shapefile for convenient identification and viewing. SHP Buddy works out-of-the-box in QGIS and does not require additional package or script installations. 

# Tutorial
This example will walk through how to make a shapefile for the following experiment map:

![image](https://github.com/user-attachments/assets/1478a0df-118d-4df4-8e12-af6198452a73)

This experiment consists of 3 reps with 30 plots each. The experiment is 4 plots across and 26 ranges deep. Each rep ends with 2 fill plots and wheel track plots are present in ranges 9 and 18. Each plot is 20 x 10 ft, however in this example we will trim 5 and 2.5 ft from each side of the length and width, respectively, for a final plot size of 10 x 5 ft.

SHP Buddy can be accessed from two locations in QGIS: the vector dropdown or the plugin toolbar:

![image](https://github.com/user-attachments/assets/414f63a4-5b6a-4c9c-9506-c162bc813753)

