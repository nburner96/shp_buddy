# -*- coding: utf-8 -*-
"""
/***************************************************************************
 shpBuddy
                                 A QGIS plugin
 Quickly create shapefiles for breeding experiments
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-08-27
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Nathaniel Burner
        email                : nburner@uga.edu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon, QFont, QColor
from qgis.PyQt.QtWidgets import QAction, QDialogButtonBox, QTableWidgetItem
from qgis.core import QgsVectorLayer, QgsProject, QgsGeometry, QgsFeature, QgsField, QgsFields, QgsRectangle, QgsPointXY, Qgis, QgsVectorFileWriter
from qgis.PyQt.QtCore import QVariant
import numpy as np
import pandas as pd
import csv

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .shp_buddy_dialog import shpBuddyDialog
import os.path


class shpBuddy:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'shpBuddy_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&SHP Buddy')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('shpBuddy', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/shp_buddy/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Create breeding plots'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&SHP Buddy'),
                action)
            self.iface.removeToolBarIcon(action)

    def enable_run_button(self):
        plots = self.dlg.plotSpin.value()
        rows = self.dlg.rowSpin.value()
        ranges = self.dlg.rangeSpin.value()
        reps = self.dlg.repSpin.value()
        fills = [int(x) for x in self.dlg.fillsEdit.text().split(',') if x.strip().isdigit()]
        wheel_track = [int(x) for x in self.dlg.wheelEdit.text().split(',') if x.strip().isdigit()]

        self.dlg.maxLCD.display(rows*ranges)
        self.dlg.exptLCD.display(plots*reps)
        self.dlg.fillLCD.display(sum(fills))
        self.dlg.wheelLCD.display(len(wheel_track)*rows)
        self.dlg.specLCD.display(plots*reps + sum(fills) + len(wheel_track)*rows)

        self.dlg.exptLCD.setStyleSheet("color: black;")
        self.dlg.fillLCD.setStyleSheet("color: black;")
        self.dlg.wheelLCD.setStyleSheet("color: black;")
        self.dlg.specLCD.setStyleSheet("color: blue")
        self.dlg.maxLCD.setStyleSheet("color: blue;")

        warning_text =""

        if len(fills) != reps:
            warning_text = warning_text + "Fill list length should equal number of reps.\n"
        if any(x > ranges or x < 1 for x in wheel_track):
            warning_text = warning_text + "At least one wheel track range is outside range limit.\n"
        if plots * reps + sum(fills) + len(wheel_track)*rows != rows*ranges:
            warning_text = warning_text + f"Specified plots does not equal total possible plots."


        self.dlg.warnLbl.setText(warning_text)
        self.dlg.warnLbl.setStyleSheet("color: red;")

        if warning_text == "":
            self.dlg.runBtn.button(QDialogButtonBox.Ok).setEnabled(True)
            self.field_preview()
        else:
            self.dlg.runBtn.button(QDialogButtonBox.Ok).setEnabled(False)
            self.dlg.fieldTbl.setVisible(False)
            self.dlg.fieldTbl.clear()
            self.dlg.fieldTbl.setRowCount(0)
            self.dlg.fieldTbl.setColumnCount(0)

    def set_max_buffer(self):
        width = self.dlg.widSpin.value()  # width in feet
        length = self.dlg.lenSpin.value()  # length in feet

        self.dlg.wbuffSpin.setRange(0,width/2 - 0.001)
        self.dlg.lbuffSpin.setRange(0,length/2 - 0.001)

    def reset_values(self):
        self.dlg.exptEdit.clear()
        self.dlg.plotSpin.setValue(1)
        self.dlg.repSpin.setValue(1)
        self.dlg.rowSpin.setValue(1)
        self.dlg.rangeSpin.setValue(1)
        self.dlg.fillsEdit.clear()
        self.dlg.wheelEdit.clear()
        self.dlg.lenSpin.setValue(1)
        self.dlg.widSpin.setValue(1)
        self.dlg.lbuffSpin.setValue(0)
        self.dlg.wbuffSpin.setValue(0)
        self.dlg.unitCmboBox.setCurrentIndex(0)
        self.dlg.fieldTbl.clear()
        self.dlg.fieldTbl.setVisible(False)

        self.dlg.fieldTbl.setRowCount(0)
        self.dlg.fieldTbl.setColumnCount(0)

        # Add field book related things below
        self.dlg.fbFile.setFilePath("")
        self.dlg.plotCmboBox.clear()
        self.dlg.colsCmboBox.clear()
        self.dlg.outFile.setFilePath("")

        self.enable_run_button()

    def field_preview(self):
        rows = self.dlg.rowSpin.value()
        ranges = self.dlg.rangeSpin.value()
        reps = self.dlg.repSpin.value()
        plots = self.dlg.plotSpin.value()
        fills = [int(x) for x in self.dlg.fillsEdit.text().split(',') if x.strip().isdigit()]
        wheel_track = [int(x) for x in self.dlg.wheelEdit.text().split(',') if x.strip().isdigit()]

        wheel_track = [x - 1 for x in wheel_track]

        # Make matrix of plots
        vec = []

        for rep in range(1, reps + 1):
            if plots < 100:
                vec.extend(list(range(rep * 100 + 1, rep * 100 + plots + 1)) + [None] * fills[rep - 1])
            else:
                vec.extend(list(range(rep * 1000 + 1, rep * 1000 + plots + 1)) + [None] * fills[rep - 1])

        # Split the vector into groups of `rows`
        groups = [vec[i:i + rows] for i in range(0, len(vec), rows)]

        # Reverse every other group
        for i in range(len(groups)):
            if i % 2 == 1:
                groups[i] = groups[i][::-1]

        # Combine groups into a matrix
        mat = np.array([item for group in groups for item in group]).reshape(-1, rows)

        # Create a new matrix with ranges x rows
        new_mat = np.full((ranges, rows), np.nan)

        if wheel_track:
            # Insert the matrix `mat` into `new_mat` excluding the wheel_track rows
            mask = np.ones(ranges, dtype=bool)
            mask[wheel_track] = False
            new_mat[mask, :] = mat
        else:
            # No wheel_track specified, insert `mat` directly into `new_mat`
            new_mat[:mat.shape[0], :] = mat

        # Reverse the order of the rows
        new_mat = np.flipud(new_mat)

        # Display new_mat in fieldTbl
        self.dlg.fieldTbl.setRowCount(new_mat.shape[0])
        self.dlg.fieldTbl.setColumnCount(new_mat.shape[1])

        for i in range(new_mat.shape[0]):
            for j in range(new_mat.shape[1]):
                value = new_mat[i, j]
                if np.isnan(value):
                    item = QTableWidgetItem("Fill")
                    item.setForeground(QColor("red"))
                    if j == 0 or j == new_mat.shape[1] - 1:
                        font = QFont()
                        font.setBold(True)
                        item.setFont(font)
                else:
                    item = QTableWidgetItem(str(int(value)))
                    if j == 0 or j == new_mat.shape[1] - 1:
                        font = QFont()
                        font.setBold(True)
                        item.setFont(font)
                    else:
                        item.setForeground(QColor("gray"))

                item.setTextAlignment(Qt.AlignCenter)
                self.dlg.fieldTbl.setItem(i, j, item)

        # Set the row headers to start from 1
        self.dlg.fieldTbl.setVerticalHeaderLabels([str(i + 1) for i in reversed(range(new_mat.shape[0]))])

        # Resize cells to fit content
        self.dlg.fieldTbl.resizeColumnsToContents()
        self.dlg.fieldTbl.resizeRowsToContents()

        # Calculate table dimensions
        max_rows = min(new_mat.shape[0], 20)
        max_cols = min(new_mat.shape[1], 20)

        # Calculate max column width and make all columns uniform with that
        max_column_width = max(self.dlg.fieldTbl.columnWidth(i) for i in range(max_cols))
        for i in range(self.dlg.fieldTbl.columnCount()):
            self.dlg.fieldTbl.setColumnWidth(i, max_column_width)

        # Row height should be standard in nearly all cases
        row_height = self.dlg.fieldTbl.rowHeight(0)

        # Content dimensions
        content_width = max_cols * max_column_width
        content_height = max_rows * row_height

        # Set the table size to fit the content
        table_width = content_width + self.dlg.fieldTbl.verticalHeader().width()
        table_height = content_height + self.dlg.fieldTbl.horizontalHeader().height()

        # Check if the vertical scrollbar is visible
        if new_mat.shape[0] > max_rows:
            self.dlg.fieldTbl.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            table_width += self.dlg.fieldTbl.verticalScrollBar().width()
        else:
            self.dlg.fieldTbl.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        if new_mat.shape[1] > max_cols:
            self.dlg.fieldTbl.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            table_height += self.dlg.fieldTbl.horizontalScrollBar().height()
        else:
            self.dlg.fieldTbl.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.dlg.fieldTbl.setFixedSize(table_width, table_height)

        # Set the vertical scroll bar to be at the bottom by default
        self.dlg.fieldTbl.scrollToBottom()

        self.dlg.fieldTbl.setVisible(True)

    def plot_size(self):
        width = self.dlg.widSpin.value()  # width in feet
        length = self.dlg.lenSpin.value()  # length in feet
        lenBuff = self.dlg.lbuffSpin.value()
        widBuff = self.dlg.wbuffSpin.value()

        units = self.dlg.unitCmboBox.currentText()

        final_length = length - lenBuff*2
        final_width = width - widBuff*2

        # Round to 3 decimal places and truncate trailing zeroes
        final_length = f"{final_length:.3f}".rstrip('0').rstrip('.')
        final_width = f"{final_width:.3f}".rstrip('0').rstrip('.')

        # Units abbreviation
        if units == "feet":
            abb = "ft."
        else:
            abb = "m"

        self.dlg.dimLbl.setText(f"Plot size: {final_length} x {final_width} {abb}")
        self.dlg.dimLbl.setStyleSheet("color: blue;")

    def csv_headers(self):
        csv_file_path = self.dlg.fbFile.filePath()

        # Clear the existing items in the combo boxes
        self.dlg.plotCmboBox.clear()
        self.dlg.colsCmboBox.clear()

        # Ensure a valid CSV file is selected
        if not csv_file_path or not os.path.exists(csv_file_path):
            self.dlg.plotCmboBox.setVisible(False)
            self.dlg.colsCmboBox.setVisible(False)
            self.dlg.label_17.setVisible(False)
            self.dlg.label_18.setVisible(False)
            return

        # Read the CSV headers
        try:
            with open(csv_file_path, 'r') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)  # Read the first row for headers

                # Populate plotCmboBox with headers
                self.dlg.plotCmboBox.addItems(headers)

                # Populate colsCmboBox with checkable items
                for header in headers:
                    self.dlg.colsCmboBox.addItem(header)

                self.dlg.plotCmboBox.setVisible(True)
                self.dlg.colsCmboBox.setVisible(True)
                self.dlg.label_17.setVisible(True)
                self.dlg.label_18.setVisible(True)

        except Exception as e:
            self.iface.messageBar().pushMessage("Error", f"Error reading CSV file: {e}",
                                                level=Qgis.Critical)
            self.dlg.plotCmboBox.setVisible(False)
            self.dlg.colsCmboBox.setVisible(False)
            self.dlg.label_17.setVisible(False)
            self.dlg.label_18.setVisible(False)

    def save_shapefile(self, layer):
        file_path = self.dlg.outFile.filePath()

        if not file_path:
            self.iface.messageBar().pushMessage("Error", f"Error: No file path provided for saving the shapefile.",
                                                level=Qgis.Critical)
            return

        # Define the format and options for the shapefile
        error = QgsVectorFileWriter.writeAsVectorFormat(layer, file_path, "UTF-8", layer.crs(), "ESRI Shapefile")

        if error[0] != QgsVectorFileWriter.NoError:
            self.iface.messageBar().pushMessage("Error", f"Error saving shapefile: {error[1]}",
                                                level=Qgis.Critical)
        else:
            return



    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = shpBuddyDialog()

            # reset and cancel buttons enabled
            self.dlg.runBtn.button(QDialogButtonBox.Ok).setEnabled(False)
            self.dlg.runBtn.button(QDialogButtonBox.Reset).setEnabled(True)
            self.dlg.runBtn.button(QDialogButtonBox.Cancel).setEnabled(True)

            # Set Defaults
            self.dlg.warnLbl.setText("")
            self.enable_run_button()
            self.dlg.plotCmboBox.setVisible(False)
            self.dlg.colsCmboBox.setVisible(False)
            self.dlg.label_17.setVisible(False)
            self.dlg.label_18.setVisible(False)


            # Connect signals
            self.dlg.fillsEdit.textEdited.connect(self.enable_run_button)
            self.dlg.wheelEdit.textEdited.connect(self.enable_run_button)
            self.dlg.plotSpin.valueChanged.connect(self.enable_run_button)
            self.dlg.repSpin.valueChanged.connect(self.enable_run_button)
            self.dlg.rowSpin.valueChanged.connect(self.enable_run_button)
            self.dlg.rangeSpin.valueChanged.connect(self.enable_run_button)

            self.dlg.runBtn.button(QDialogButtonBox.Reset).clicked.connect(self.reset_values)

            # Update dimensions label
            self.plot_size()

            self.dlg.lenSpin.valueChanged.connect(self.plot_size)
            self.dlg.widSpin.valueChanged.connect(self.plot_size)
            self.dlg.lbuffSpin.valueChanged.connect(self.plot_size)
            self.dlg.wbuffSpin.valueChanged.connect(self.plot_size)
            self.dlg.unitCmboBox.currentIndexChanged.connect(self.plot_size)

            # CSV file connect
            self.dlg.fbFile.fileChanged.connect(self.csv_headers)

            # Update max buffer values
            self.dlg.widSpin.valueChanged.connect(self.set_max_buffer)
            self.dlg.lenSpin.valueChanged.connect(self.set_max_buffer)


        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()

        # See if OK was pressed
        if result:
            # Get the project CRS
            project = QgsProject.instance()
            crs = project.crs()

            # Define units (either meters or feet)
            units = self.dlg.unitCmboBox.currentText()

            # Define dimensions and spacing
            expt = self.dlg.exptEdit.text()
            width = self.dlg.widSpin.value()  # width in feet
            length = self.dlg.lenSpin.value()  # length in feet
            rows = self.dlg.rowSpin.value()
            ranges = self.dlg.rangeSpin.value()
            reps = self.dlg.repSpin.value()
            plots = self.dlg.plotSpin.value()
            fills = [int(x) for x in self.dlg.fillsEdit.text().split(',') if x.strip().isdigit()]
            wheel_track = [int(x) for x in self.dlg.wheelEdit.text().split(',') if x.strip().isdigit()]

            # Optional buffer
            lenBuff = self.dlg.lbuffSpin.value()
            widBuff = self.dlg.wbuffSpin.value()

            wheel_track = [x - 1 for x in wheel_track]

            if units == 'feet':
                width = width / 3.28084
                length = length / 3.28084


            # Get the extent of the current map canvas
            canvas = self.iface.mapCanvas()
            extent = canvas.extent()

            # Calculate the center coordinates of the current extent
            center_x = extent.xMinimum() + (extent.width() / 2)
            center_y = extent.yMinimum() + (extent.height() / 2)

            # Define the starting point for the grid to appear in the center of the screen
            start_x = center_x - ((rows * width) / 2)
            start_y = center_y - ((ranges * length) / 2)

            # Create a new memory layer for the plots
            if expt:
                layer = QgsVectorLayer("Polygon?crs={}".format(crs.authid()), expt, "memory")
            else:
                layer = QgsVectorLayer("Polygon?crs={}".format(crs.authid()), "Plots", "memory")
            pr = layer.dataProvider()

            # Define fields
            fields = QgsFields()
            if expt:
                fields.append(QgsField("Expt", QVariant.String))

            fields.append(QgsField("Plot", QVariant.String))

            # Add fields for CSV attributes
            csv_file_path = self.dlg.fbFile.filePath()
            if csv_file_path and os.path.exists(csv_file_path):
                selected_cols = self.dlg.colsCmboBox.checkedItems()
                for col in selected_cols:
                    if col not in fields.names():
                        fields.append(QgsField(col, QVariant.String))

            # Add fields to the layer
            pr.addAttributes(fields)
            layer.updateFields()

            # Load CSV data
            csv_data = {}
            if csv_file_path and os.path.exists(csv_file_path):
                try:
                    with open(csv_file_path, 'r') as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            plot_number = row.get(self.dlg.plotCmboBox.currentText())
                            if plot_number:
                                csv_data[plot_number] = {col: row[col] for col in selected_cols if col in row}
                except Exception as e:
                    self.iface.messageBar().pushMessage("Error", f"Error reading CSV data: {e}",
                                                        level=Qgis.Critical)

            # Create features for the plots
            features = []

            # Make matrix of plots

            vec = []

            for rep in range(1, reps + 1):
                if plots < 100:
                    vec.extend(list(range(rep * 100 + 1, rep * 100 + plots + 1)) + [None] * fills[rep - 1])
                else:
                    vec.extend(list(range(rep * 1000 + 1, rep * 1000 + plots + 1)) + [None] * fills[rep - 1])

            # Split the vector into groups of `rows`
            groups = [vec[i:i + rows] for i in range(0, len(vec), rows)]

            # Reverse every other group
            for i in range(len(groups)):
                if i % 2 == 1:
                    groups[i] = groups[i][::-1]

            # Combine groups into a matrix
            mat = np.array([item for group in groups for item in group]).reshape(-1, rows)

            # Create a new matrix with ranges x rows
            new_mat = np.full((ranges, rows), np.nan)

            if wheel_track:
                # Insert the matrix `mat` into `new_mat` excluding the wheel_track rows
                mask = np.ones(ranges, dtype=bool)
                mask[wheel_track] = False
                new_mat[mask, :] = mat
            else:
                # No wheel_track specified, insert `mat` directly into `new_mat`
                new_mat[:mat.shape[0], :] = mat

            # Loop through rows and columns to create plot polygons
            for row in range(ranges):
                for col in range(rows):

                    plot_number = new_mat[row, col]

                    if np.isnan(plot_number):
                        continue

                    # Calculate plot coordinates
                    x_min = start_x + col * width + lenBuff
                    x_max = x_min + width - lenBuff
                    y_min = start_y + row * length + widBuff
                    y_max = y_min + length - widBuff

                    # Create plot geometry
                    plot_polygon = QgsGeometry.fromRect(QgsRectangle(x_min, y_min, x_max, y_max))

                    # Rotate the geometry around the center of the grid
                    plot_polygon.rotate(-canvas.rotation(), QgsPointXY(center_x, center_y))

                    # Create feature and set attributes
                    feature = QgsFeature()
                    feature.setGeometry(plot_polygon)

                    attributes = [plot_number]
                    if expt:
                        attributes.insert(0, expt)

                    # Append CSV attributes
                    if csv_file_path and os.path.exists(csv_file_path):
                        if str(int(plot_number)) in csv_data:
                            csv_attributes = [csv_data[str(int(plot_number))].get(col, '') for col in selected_cols]
                            attributes.extend(csv_attributes)
                        else:
                            attributes.extend([''] * len(selected_cols))

                    feature.setAttributes(attributes)
                    features.append(feature)

            # Add features to the layer
            pr.addFeatures(features)

            # Save and add shapefile
            saved_file_path = self.dlg.outFile.filePath()

            if saved_file_path:
                self.save_shapefile(layer)
                if expt:
                    saved_layer = QgsVectorLayer(saved_file_path, expt, "ogr")
                else:
                    saved_layer = QgsVectorLayer(saved_file_path, "Plots", "ogr")

                if not saved_layer.isValid():
                    self.iface.messageBar().pushMessage("Error", "Error loading saved shapefile.",
                                                        level=Qgis.Critical)
                else:
                    project.addMapLayer(saved_layer)
            else:
                # Add as temporary layer
                project.addMapLayer(layer)

            if expt:
                self.iface.messageBar().pushMessage("Success", f"{expt} shapefile generated.", level=Qgis.Success)
            else:
                self.iface.messageBar().pushMessage("Success", f"Plot shapefile generated.", level=Qgis.Success)

