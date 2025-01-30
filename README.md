# SHP Buddy
SHP Buddy is a QGIS plugin that provides an quick and intuitive method for generating shapefiles for common plant breeding experiment designs. SHP Buddy lays out plots in a serpentine pattern and can account for fill plots and wheel tracks. Plot sizes are adjustable to exclude things such as adjacent plots and alleyways from the regions of interest. SHP Buddy provides an easy method for integrating field book information such as line names, pedigrees, and trait notes into the final shapefile for convenient identification and viewing. SHP Buddy works out-of-the-box in QGIS and does not require additional package or script installations. 

## Contents
[Plot layout and Numbering](https://github.com/nburner96/shp_buddy?tab=readme-ov-file#plot-layout-and-numbering)

[Installation](https://github.com/nburner96/shp_buddy?tab=readme-ov-file#installation)

[Tutorial](https://github.com/nburner96/shp_buddy?tab=readme-ov-file#tutorial)

[Plot Information](https://github.com/nburner96/shp_buddy?tab=readme-ov-file#plot-information)

[Limitations](https://github.com/nburner96/shp_buddy?tab=readme-ov-file#limitations)

# Plot Layout and Numbering
Plots are laid out in a serpentine pattern, beginning at the bottom left of the shapefile and working its way across each range before moving up to the next range. Experiments with less than 100 plots will be numbered using the "RPP" format, where R is the rep number, and PP is the 2-digit plot number. Ex: a 3 rep experiment with 20 plots each is numbered 101-120, 201-220, and 301-320. 

Each plot in an experiment with 100 or more plots were rep is given a 4 digit plot number in the "RPPP" format. Ex: a 3 rep experiment with 200 plots each is numbered 1001-1200, 2001-2200, and 3001-3200.

Fill plots, if specified, are place after the last plot in each rep (see tutorial below).

# Installation
SHP Buddy can be installed from the plugins repository directly within QGIS. The plugins repository can be accessed through selecting the Plugins dropdown > Manage and Install Plugins. Search for "SHP Buddy" in the All tab to install.

# Tutorial
This example will walk through how to make a shapefile for the following experiment map:

![image](https://github.com/user-attachments/assets/1478a0df-118d-4df4-8e12-af6198452a73)

This experiment consists of 3 reps with 30 plots each. The experiment is 4 plots across and 26 ranges deep. Each rep ends with 2 fill plots and ranges 9 and 18 have a wheel track (and are fill plots). Each plot is 20 x 10 ft, however in this example we will trim 5 and 2.5 ft from each side of the length and width, respectively

SHP Buddy can be accessed from two locations in QGIS: the vector dropdown or the plugin toolbar:

![image](https://github.com/user-attachments/assets/414f63a4-5b6a-4c9c-9506-c162bc813753)

A dialog window will pop up where you can enter test specifications. Most sections are fairly self-explanatory, please see accompanying notes for further clarification:

![image](https://github.com/user-attachments/assets/2f2a57cc-623e-4fe8-85dc-851716bd0fdc)

1. Name of the experiment
2. Plots per rep and number of reps. Plots per rep value should exclude fill plots that are not in wheel tracks (see below)
3. Dimensions of experiment in terms of plots. Rows is the total number of plots across each range, ranges is the total number of ranges (including wheel track ranges)
4. Number of fill plots after each rep. Expressed as a comma separated list. List length must equal Reps value (specify 0 if a rep is not followed by fills).
5. Wheel track ranges. A list of numbers indicating which ranges (starting from the front of the field) are in wheel tracks and are planted with fills. In the example, ranges 9 and 18 are wheel track ranges.
6. Check this box to flip the direction of the plots. If unchecked, the serpentine pattern begins with plots increasing from left to right in the first range.

![image](https://github.com/user-attachments/assets/0b7accd5-e4d5-4057-a331-9110f373b6b4)
![image](https://github.com/user-attachments/assets/d3c399b4-6ff9-4697-8acb-4f5806af0478)

7. Plot tracker. This displays the number of different types of plots specified to help identify the source of potential dimension errors. Specified plots is the total number of experimental and fill plots (including those in wheel tracks). Required plots is the total footprint (in plots) of the experiment as calculated by Rows x Ranges. If there are no errors in the inputs, a preview of the map will appear.

### Unreplicated layout options (sidenote)

![image](https://github.com/user-attachments/assets/e5ce229e-1b4d-480f-adbd-5bdae16fa3c0)

Checking the 'Unreplicated' box will display a slightly different set of inputs for unreplicated designs. The first and last plots are designated with the Start and End plot values. Plot indent is an optional value indicating the number of skipped plots in the first range preceding the first plot for a scenario in which the preceding experiment does not fill the last range. The plot tracker LCD is also modified to show the number of "trailing plots" in the last range. Specified plots is the sum of the experimental plots, indent plots, and wheel track plots (if specified) at the beginning of the layout. This value, plus the number of trailing plots, cannot exceed the total possible plots value determined by the product of rows and columns.

The example shown is a layout that begins at plot 2001 and ends at 8195. This layout begins 25 plots into its first range as it follows another layout. The 'Right to left' box is checked since the plot numbers are increasing from right to left in the first range. A similar example is described in the associated paper (currently pending publication).  

## Tutorial continued

![image](https://github.com/user-attachments/assets/249af6c4-f6e4-4471-b7d5-1c85fb41608b)

8. Total plot dimensions. Includes all rows and alleyways for each plot.
9. Plot buffers. Specifies how much to trim off of each side of the length and width. In the example, we want to only look at the middle two rows (2.5 ft. row spacing) for each plot and exclude alleyways.
10. Plot units. Currently feet and meters are available. The final plot dimensions will be displayed above.

![image](https://github.com/user-attachments/assets/c9295e4b-4292-4f11-b8a8-61d5f021ff37)

![image](https://github.com/user-attachments/assets/edf76165-1360-4ff0-a899-d3869d1ca884)

11. Field book upload. Optionally, specify a CSV file containing fieldbook information. The only requirements are that the first row is the header and that the plot IDs must match the expected numbering system as described above.

The following dropdowns will appear if a field book is uploaded.

![image](https://github.com/user-attachments/assets/12f96052-17a3-4030-a746-dfd6d0f9d7fb)

12. Specify which header corresponds to the Plot ID column.
13. Column selection. This section appears only if a field book file is specified. Select the columns that you want to add to the shapefile. *Note: plot and experiment name (if specified) fields are automatically added to the shapefile, do not select these columns to import from the field book*
    
![image](https://github.com/user-attachments/assets/a15e1556-99d4-4bca-8f0d-bc42c1329f3e)

15. Save shapefile. Optionally, specify the folder and file name of the shapefile. If no name specified, shapefile will be generated as a temporary layer.

**Press OK to generate the shapefile**

![image](https://github.com/user-attachments/assets/f635f89e-77df-4722-9334-2af86867bed7)

The shapefile will be added to the QGIS project.

# Editing

![image](https://github.com/user-attachments/assets/b679ac1b-7afc-4406-bce0-fc59b6bb49d0)

The shapefile can be aligned with the plots in the image by selecting the layer in the Layers panel and pressing the "Toggle Editing". The shapefile can be moved and rotated using the labeled functions. To save changes, press the "Toggle Editing" button again. More information on editing shapefiles can be found in the [QGIS documentation](https://docs.qgis.org/3.34/en/docs/user_manual/working_with_vector/editing_geometry_attributes.html).

# Plot Information

![image](https://github.com/user-attachments/assets/d0e8b081-1a82-4ab0-ad6b-9888278c00bc)
![image](https://github.com/user-attachments/assets/3f75ebc3-120a-4790-bc9d-e0c312603d06)

Right-clicking the shapefile and selecting "Open Attribute Table" will display the field book information associated with each plot.

![image](https://github.com/user-attachments/assets/f2c4cde8-98ce-43a3-8339-6f623e3c78ff)

Lastly, the "Identify Features" tool can be used to display information for plots of interest.

# Limitations
SHP Buddy is a great option for common serpentine breeding experiments. However, there are a number of features that may be of interest to other researchers that are not currently available in the plugin. Below is a list of some of these features, and possible solutions for the time being:
1. Custom plot IDs
   * Add a column that follows the SHP Buddy plot numbering system to the field book CSV. Select this column when importing the field book.
2. Unbalanced designs
   * SHP Buddy currently only generates shapefiles with the same number of plots per rep. One way around this may be to make "dummy" plots in the field book CSV and delete these later.
3. Serpentine pattern by row
   * Some breeding experiments serpentine down rows instead of across ranges. A solution to this could be to ultimately rotate the shapefile 90 degrees, which would require the length and width parameters to be swapped. As far as accounting for wheel tracks in this set up, one could manually select and move the appropriate plots up a range. 

This is by no means an exhaustive list. I hope to get around to most of these in the not too distant future. In the meantime, SHP Buddy is open source so feel free to play around with the code and send a pull request if you come up with something cool.

Please report any issues [here](https://github.com/nburner96/shp_buddy/issues)

