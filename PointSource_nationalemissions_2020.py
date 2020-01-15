
# Name Code: Converting CSV files of the point source emission inventory to USEPA Tags on KML files 
# The Python code used in this project was adapted from the original code developed by Manos Marks, of Geo APIs, Team, Authored: December 2007
# Updated: December 2013
# Software required: Windows, Linux, Mac OS
# Program language: Python 2.6.2 version 
# Adapted by Abraham Ortinez-Alvarez  abraham@atmosfera.unam.mx 

The Python code used in this project was tropicalized and adapted from the original code developed by Manos Marks, of Geo APIs, Team
# The project was developed in Python 2.6.2 version 

import geocoding_for_kml
import csv
import xml.dom.minidom
import sys


def extractAddress(row):
  # This extracts an address from a row and returns it as a string. This requires knowing
  # ahead of time what the columns are that hold the address information.
  return '%s,%s,%s' % (row['Industry_Name'],row['Coordinates'],row['Identification'],row['Geographic_Information'],row['Process'],row['Properties'],row['Equipment'],row['Emission'])
                  
                                      

def createPlacemark(kmlDoc, row, order):
  # This creates a  element for a row of data.
  # A row is a dict.
  placemarkElement = kmlDoc.createElement('Placemark')
  station = (row['Industry_Name'])
  nameElement = kmlDoc.createElement('name')
  nameElement.appendChild(kmlDoc.createTextNode(station))
  placemarkElement.appendChild(nameElement)
  
  
  #Coordinates = (row['Coordinates'])
  #coorElement = kmlDoc.createElement('coordinates')
  #coorElement.appendChild(kmlDoc.createTextNode(Coordinates))
  #pointElement.appendChild(coorElement)  
  extElement = kmlDoc.createElement('ExtendedData')
  placemarkElement.appendChild(extElement)
  
  # Loop through the columns and create a  element for every field that has a value.
  for key in order:
    if row[key]:
      dataElement = kmlDoc.createElement('Data')
      dataElement.setAttribute('name', key)
      valueElement = kmlDoc.createElement('value')
      dataElement.appendChild(valueElement)
      valueText = kmlDoc.createTextNode(row[key])
      valueElement.appendChild(valueText)
      extElement.appendChild(dataElement)

    	  
	  
  pointElement = kmlDoc.createElement('Point')
  placemarkElement.appendChild(pointElement)
  #coordinates = geocoding_for_kml.geocode(extractAddress(row))
  Coordinates = (row['Coordinates'])
  coorElement = kmlDoc.createElement('coordinates')
  coorElement.appendChild(kmlDoc.createTextNode(Coordinates))
  pointElement.appendChild(coorElement)
  
  return placemarkElement
   
   

def createKML(csvReader, fileName, order):
  # This constructs the KML document from the CSV file.
  kmlDoc = xml.dom.minidom.Document()
  
  kmlElement = kmlDoc.createElementNS('http://earth.google.com/kml/2.2', 'kml')
  kmlElement.setAttribute('xmlns','http://earth.google.com/kml/2.2')
  kmlElement = kmlDoc.appendChild(kmlElement)
  documentElement = kmlDoc.createElement('Document')
  documentElement = kmlElement.appendChild(documentElement)

  # Skip the header line.
  csvReader.next()
  
  for row in csvReader:
    placemarkElement = createPlacemark(kmlDoc, row, order)
    documentElement.appendChild(placemarkElement)
  kmlFile = open(fileName, 'w')
  kmlFile.write(kmlDoc.toprettyxml('  ', newl = '\n', encoding = 'utf-8'))


def main():
  # This reader opens up 'file.csv', which should be replaced with your own.
  # It creates a KML file called 'file.kml'.
  
  # If an argument was passed to the script, it splits the argument on a comma
  # and uses the resulting list to specify an order for when columns get added.
  # Otherwise, it defaults to the order used in the sample.
  
  if len(sys.argv) >1: order = sys.argv[1].split(',')
  else: order = ['Industry_Name','Coordinates','Identification','Geographic_Information','Process','Properties','Equipment','Emission',]
  csvreader = csv.DictReader(open('C:/Users/Abraham/Desktop/emission_pointsource_emistags.csv'),order)
  kml = createKML(csvreader, 'C:/Users/Abraham/Desktop/datgen_pointsource_emistags.kml',order)
if __name__ == '__main__':
  main()

