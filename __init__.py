# -*- coding: utf-8 -*-
"""
/***************************************************************************
 shpBuddy
                                 A QGIS plugin
 Quickly create shapefiles for breeding experiments
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-08-27
        copyright            : (C) 2024 by Nathaniel Burner
        email                : nburner@uga.edu
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load shpBuddy class from file shpBuddy.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .shp_buddy import shpBuddy
    return shpBuddy(iface)
