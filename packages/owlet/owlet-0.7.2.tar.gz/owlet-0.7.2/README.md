<div align="center">
  <img src="https://raw.githubusercontent.com/HFM3/owlet/master/images/owlet_horiz.png" width="60%"><br>
</div>

---
![PyPI](https://img.shields.io/pypi/v/owlet?label=PyPi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/owlet?label=Python)
![PyPI - License](https://img.shields.io/pypi/l/owlet?label=License)

# A Geospatial Python Package for Field Researchers

## Owlet and EGF: Developed for Field Researchers
Owlet is a Python library for interacting with and mapping EGF files.

EGF, or Exact Geometry Format, is a file structure designed specifically for recording geo-data without traditional GIS software. An EGF file contains all of the necessary components required to define geospatial features— without overcomplicating it.

## EGF File Example

### Overview
An EGF file is comprised of three sections:

1. **A Feature Type Declaration** (point, line, polygon)
2. **Attribute Headers**
3. **Features**: attributes & coordinate sets


#### Example EFG file containing two placemarks:
```
PT



Park Name, City, Pond, Fountain



Post office Square, Boston, FALSE, TRUE
42.356243, -71.055631, 2



Boston Common, Boston, TRUE, TRUE
42.355465, -71.066412, 10

```

In an EGF file, each section / feature is separated by three blank lines and the file ends with a single blank line.

An EGF file is a '.txt' file renamed to '.egf'

[Full EGF Documentation](https://github.com/HFM3/owlet/blob/master/docs/egf.md)


### Installing Owlet
To install owlet, type one of the following commands into the terminal or command line

###### Windows
```python
>>> py -m pip install  owlet
```
###### MacOS / Linux
```python
>>> pip3 install owlet
```
<!---
##### Install specific version
```shell
pip install owlet==0.0.1
```

##### Upgrade to latest version
```shell
pip install --upgrade owlet
```
-->

## Using Owlet
To begin, save the EGF file example above to your computer as **BostonParks.egf** using a text editor such as Notepad.

Once the EGF file is saved, create a new Python file and import Owlet.

When writing a new Python file, begin by importing Owlet.
```Python
import owlet

```
### Reading an EGF file
To read an EGF file, begin by saving the path of the EGF file to a variable in your python script.

Then pass the variable that hold the EGF file's path to the **read_egf()** function. Since the **read_egf()** function is a part of the Owlet Python package, the function is called by typing **owlet.** before the function name - e.g. **owlet.read_egf()**

Below, the EGF file is loaded and saved to a variable named **my_shape**.

```python
in_file = "path/to/file/BostonParks.egf"

my_shape = owlet.read_egf(in_file)

```

If the file path is short, it may be easier to pass the path directly in to the function like in the example below. For longer paths, it is neater to save the path to a variable.

```python
my_shape = owlet.read_egf("folder/BostonParks.egf")

```

### Visualizing an EGF file

To visualize **my_shape** call the **visualize()** function and pass it **my_shape**.

```python
owlet.visualize(my_shape)
```
Upon **visualize()** being executed, the computer's default web browser will open and provide a preview of **my_shape** using the webpage [geojson.io](http://geojson.io)

**Both points from the EGF file are displayed on the map after running _owlet.visualize(my_shape)_**

![EGF Point Visualization](https://raw.githubusercontent.com/HFM3/owlet/master/images/readme/pt_preview.png)

**EGF Files also support linestrings for mapping paths**

![EGF Linestring Visualization](https://raw.githubusercontent.com/HFM3/owlet/master/images/readme/ls_preview.png)

**Polygons are also supported by EGF**

![EGF Polygon Visualization](https://raw.githubusercontent.com/HFM3/owlet/master/images/readme/poly_preview.png)

## Converting an EGF File to Other Formats
To interact with the data from an EGF file outside of Owlet, the data can be exported to a different format. Owlet offers a few different export options.

### GeoJSON
To use the EGF data with other GIS software packages, Owlet provides a GeoJSON export option.

To export data in GeoJSON format, first save the export file path to a variable. (Notice that the new file's name and file extension are included in the path.)

Then call the function **write_geojson()** and pass it the path of the file to be created as well as the variable that holds the EGF geometry.

```python
out_file = "folder/MyShape.json"

owlet.write_geojson(out_file, my_shape)
```
Upon **write_geojson()** being executed, a _.json_ file will be created at the location specified by the path defined by the **out_file** variable. The new GeoJSON file can be loaded, viewed, and manipulated by many common GIS programs.

#### Reading an EGF file and Writing it to a GeoJson File - Complete Script
```python
import owlet

in_file = "path/to/file/BostonParks.egf"
out_file = "folder/MyShape.json"

my_shape = owlet.read_egf(in_file)

owlet.write_geojson(out_file, my_shape)
```

### CSV
To view/manipulate an EGF file in as a table, the **write_csv()** function can be used in the same way as the **write_geojson()** function.

To export data in CSV format, first save the export file path to a variable. (Notice that the new file's name and file extension are included in the path.)

Then call the function **write_csv()** and pass it the path of the file to be created as well as the variable that holds the EGF geometry.

```python
out_file = "folder/MyShape.csv"

owlet.write_csv(out_file, my_shape)
```

**The resulting CSV file will match the table below:**

|Park Name         |City  |Pond |Fountain|GEOMETRY_PT                  |
|------------------|------|-----|--------|-----------------------------|
|Post office Square|Boston|FALSE|TRUE    |[-71.055631, 42.356243, 2.0] |
|Boston Common     |Boston|TRUE |TRUE    |[-71.066412, 42.355465, 10.0]|

When saved as a CSV file and opened with an appropriate program, the data can be filtered, new attributes can be added, and existing attributes can be edited.

For example, a **State** attribute could be added to each record of the table.

|Park Name         |City  |State|Pond |Fountain|GEOMETRY_PT                  |
|------------------|------|-----|-----|--------|-----------------------------|
|Post office Square|Boston|MA   |FALSE|TRUE    |[-71.055631, 42.356243, 2.0] |
|Boston Common     |Boston|MA   |TRUE |TRUE    |[-71.066412, 42.355465, 10.0]|

As long as the **GEOMETRY_PT** column is not manipulated, the CSV file can be loaded back in to Owlet.


**Loading CSV in to Owlet**
```python
in_file = "path/to/file/MyShape.csv"

my_shape = owlet.read_csv(in_file)

```

To see that the changes made to the table have been reflected in Owlet, use the **print()** function.
```python
print(my_shape)
```

 Which will print out:
```
'PT' GCA object containing 2 feature(s) with the following attributes: ['Park Name', 'City', 'State', 'Pond', 'Fountain']
```
The above line informs us that **my_shape** is a **PT** (Point) file that contains **2 features** that each have **Park Name, City, State, Pond,** and **Fountain** as attributes. We can see that the **State** attribute was added and loaded correctly. _"GCA object" refers to the internal format that Owlet uses to store geometry._

#### Reading an EGF file and Writing it to a CSV File - Complete Script
```python
import owlet

in_file = "path/to/file/BostonParks.egf"
out_file = "folder/MyShape.csv"

my_shape = owlet.read_egf(in_file)

owlet.write_csv(out_file, my_shape)
```


### Google Earth KML
Owlet can also write KML files for use with Google Earth. Owlet leverages the KML format's "ExtendedData" feature which makes Owlet's KMLs import cleanly into QGIS.

The **write_kml()** function takes multiple arguments:
1. Path of file to write
2. EGF to write _(the variable that an EGF file is saved to)_
3. Title of the attribute column that contains the attributes that the features should be named with
4. Name of folder within KML file that will contain the features of the EGF file
5. Folder description (optional)
6. Altitude mode (optional)

Optional arguments do not need to be defined in order for a KML to be produced.

Owlet accepts three types of altitude modes:
- **'ctg'** short for Clamped to Ground. Elevation values are ignored and all features are displayed at ground level.
- **'rtg'** short for Relative to Ground. Elevation values are rendered as "x" meters above the ground below.
- **'abs'** short for Absolute. Elevation values are rendered as "x" meters above mean sea level.

The default altitude mode is **ctg**

**Write a KML file by only providing the required arguments**
```python
out_file = "folder/MyShape.kml"

owlet.write_kml(out_file, my_shape, 'Park Name', 'Parks')
```

**Adding a Folder Description**
```python
out_file = "folder/MyShape.kml"

owlet.write_kml(out_file, my_shape, 'Park Name', 'Parks', 'Parks near Downtown Boston')
```

**Changing the Altitude Mode**
```python
out_file = "folder/MyShape.kml"

owlet.write_kml(out_file, my_shape, 'Park Name', 'Parks', altitude_mode='rtg')
```

**Providing all KML Arguments**
```python
out_file = "folder/MyShape.kml"

owlet.write_kml(out_file, my_shape, 'Park Name', 'Parks', 'Parks near Downtown Boston', 'rtg')
```

#### Reading an EGF file and Writing it to a KML File - Complete Script
```python
import owlet

in_file = "path/to/file/BostonParks.egf"
out_file = "folder/MyShape.kml"

my_shape = owlet.read_egf(in_file)

owlet.write_kml(out_file, my_shape, 'Park Name', 'Parks', 'Parks near Downtown Boston', 'rtg')
```

### EGF
Owlet will also export to EGF.


```python
out_file = "folder/MyShape.egf"

owlet.write_egf(out_file, my_shape)
```

&nbsp;
&nbsp;

Owlet License: [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
