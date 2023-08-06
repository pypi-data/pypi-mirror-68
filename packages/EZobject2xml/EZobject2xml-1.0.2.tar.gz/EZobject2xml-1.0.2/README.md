# EZobject2xml
Save and load easily any python object data into/from a xml file.

This module has only one object _xmltool_ with 2 functions.

#### For saving an object into a xml file, you just have to code (python):
```python
from EZobject2xml.xmltoolMod import *
myXmltool = xmltool()
myXmltool.saveObject2xml(myObject,myFilename)
```
where:
>_myObject_ is the object to save

>_myFileName_ if the xml file

#### And for loading:
```python
myXmltool.loadObjectFromXml(myObject,myFilename)
```

#### Not wanna save a data of your object ?:
Just add "__" at the end of the name of the data and "saveObject2xml" function won't save this data.

#### Wanna save a single value data such as integer, float, string, set, tuple, list or dict ?:
You just have to use SingleType class object:
```python
from EZobject2xml.xmltoolMod import *
myxmltool = xmltool()
myvalue_object = SingleType(myvalue)
myxmltool.saveObject2xml(myvalue_object,'myvalue.xml')
```
For loading:
```python
myxmltool.loadObjectFromXml(myvalue_object,'myvalue.xml')
myvalue = myvalue_object.value
```
where:
>_myvalue_ is any basic data type as int, float, str, set, tuple, list or dict

#### Exception:
If objects have to be dynamically initialized during the data reading process
(i.e. if your object has a list of an undefined number of other objects), 
we have to create them first before reading their saved data.
In order to do that, we give a list of object class that we could use to create a new instance of these objects.

This list of class objects is a initDataList object and we pass it as:
```python
myInitDataList = initDataList()
myInitDataList.addInitData(mySubObject1Class,(a tuple containing the parameters to initialize this SubObject))
myInitDataList.addInitData(mySubObject2Class,(a tuple containing the parameters to initialize this SubObject))
...

myXmltool = xmltool()
myXmltool.loadObjectFromXml(myObject,myFilename,myInitDataList)
```
where:
>_mySubObject1Class_ is the class of an object which can be contained in myObject

>_myObject_ is the object to save

>_myFileName_ if the xml file

As seen, myInitDataList is optional and only needed when your object has a list of an undefined number of other objects.

The [test file](https://github.com/JoshuaWar/EZobject2xml/tree/master/tests "test file") has a concrete example.

Please see the python help() function to see more technical information about these functions.

To install the package :
```python
-m pip install EZobject2xml
```