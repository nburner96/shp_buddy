# SHP Buddy
SHP Buddy is a QGIS plugin that provides an quick and intuitive method for generating shapefiles for common plant breeding experiment designs. SHP Buddy lays out plots in a serpentine pattern and can account for fill plots and wheel tracks. Plot sizes are adjustable to exclude things such as adjacent plots and alleyways from the regions of interest. SHP Buddy provides an easy method for integrating field book information such as line names, pedigrees, and trait notes into the final shapefile for convenient identification and viewing. SHP Buddy works out-of-the-box in QGIS and does not require additional package or script installations. 

# Plot Layout and Numbering
Plots are laid out in a serpentine pattern, beginning at the bottom left of the shapefile and working its way across each range before moving up to the next range. Experiments with less than 100 plots will be numbered using the "RPP" format, where R is the rep number, and PP is the 2-digit plot number. Ex: a 3 rep experiment with 20 plots each is numbered 101-120, 201-220, and 301-320. 

Each plot in an experiment with 100 or more plots were rep is given a 4 digit plot number in the "RPPP" format. Ex: a 3 rep experiment with 200 plots each is numbered 1001-1200, 2001-2200, and 3001-3200.

Fill plots, if specified, are place after the last plot in each rep (see tutorial below).

# Tutorial
This example will walk through how to make a shapefile for the following experiment map:

![image](https://github.com/user-attachments/assets/1478a0df-118d-4df4-8e12-af6198452a73)

This experiment consists of 3 reps with 30 plots each. The experiment is 4 plots across and 26 ranges deep. Each rep ends with 2 fill plots and ranges 9 and 18 have a wheel track (and are fill plots). Each plot is 20 x 10 ft, however in this example we will trim 5 and 2.5 ft from each side of the length and width, respectively

SHP Buddy can be accessed from two locations in QGIS: the vector dropdown or the plugin toolbar:

![image](https://github.com/user-attachments/assets/414f63a4-5b6a-4c9c-9506-c162bc813753)

A dialog window will pop up where you can enter test specifications. Most sections are fairly self-explanatory, please see accompanying notes for further clarification:

![image](https://github.com/user-attachments/assets/7898ef5d-8ef0-45b3-aa8c-c55af7517f86)

1. Name of the experiment
2. Plots per rep and number of reps. Plots per rep value should exclude fill plots that are not in wheel tracks (see below)
3. Dimensions of experiment in terms of plots. Rows is the total number of plots across each range, ranges is the total number of ranges (including wheel track ranges)
4. Number of fill plots after each rep. Expressed as a comma separated list. List length must equal Reps value (specify 0 if a rep is not followed by fills).
5. Wheel track ranges. A list of numbers indicating which ranges (starting from the front of the field) are in wheel tracks and are planted with fills. In the example, ranges 9 and 18 are wheel track ranges.

![image](https://github.com/user-attachments/assets/120f5b10-9262-4a2b-be27-be50963733d1)
![image](https://github.com/user-attachments/assets/d3c399b4-6ff9-4697-8acb-4f5806af0478)

6. Plot tracker. This displays the number of different types of plots specified to help identify the source of potential dimension errors. Specified plots is the total number of experimental and fill plots (including those in wheel tracks). Required plots is the total footprint (in plots) of the experiment as calculated by Rows x Ranges. If there are no errors in the inputs, a preview of the map will appear.

![image](https://github.com/user-attachments/assets/106b889a-f29e-4d13-ad32-1e5573c0b95e)

7. Total plot dimensions. Includes all rows and alleyways for each plot.
8. Plot buffers. Specifies how much to trim off of each side of the length and width. In the example, we want to only look at the middle two rows (2.5 ft. row spacing) for each plot and exclude alleyways.
9. Plot units. Currently feet and meters are available. The final plot dimensions will be displayed above.

![image](https://github.com/user-attachments/assets/a3a88e99-485c-48d9-8a81-53ce66127350)

![image](https://github.com/user-attachments/assets/edf76165-1360-4ff0-a899-d3869d1ca884)

10. Field book upload. Optionally, specify a CSV file containing fieldbook information. The only requirement is that the first row is the header and that the plot IDs must match the expected numbering system as described above.

![image](https://github.com/user-attachments/assets/b6a2cfcf-79be-4571-baaf-25718a6313c5)

The following dropdowns will appear if a field book is uploaded.

![image](https://github.com/user-attachments/assets/21e1e515-ed7f-4567-91a8-b789bcd95ad7)

11. Specify which header corresponds to the Plot ID column.
12. Column selection. This section appears only if a field book file is specified. Select the columns that you want to add to the shapefile.

![image](https://github.com/user-attachments/assets/af361d61-35d6-4952-84a4-a4476b7575b3)

13. Save shapefile. Optionally, specify the folder and file name of the shapefile. If no name specified, shapefile will be generated as a temporary layer.

**Press run to generate the shapefile**

![image](https://github.com/user-attachments/assets/d9af1bbf-f349-4d13-b4fe-668fd84ad4d6)

The shapefile will be added to the center of the field of view.

![image](https://github.com/user-attachments/assets/b679ac1b-7afc-4406-bce0-fc59b6bb49d0)

The shapefile can be aligned with the plots in the image by selecting the layer in the Layers panel and pressing the "Toggle Editing". The shapefile can be moved and rotated using the labeled functions. To save changes, press the "Toggle Editing" button again.

![image](https://github.com/user-attachments/assets/d0e8b081-1a82-4ab0-ad6b-9888278c00bc)
![image](https://github.com/user-attachments/assets/c311c5a3-99b3-48e8-b365-77f894a05055)

Right-clicking the shapefile and selecting "Open Attribute Table" will display the field book information associated with each plot.

