import os
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def check_file_exist():
    fp = open("database_index.xml", "w")