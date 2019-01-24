'''
Created on 17 Aug 2016

@author: Marwa
'''
import os
import sys
import xml.etree.ElementTree as ET
"""TODO: Add detailed comments for class, elements and all methods
   """
class Parseur():
    TagXMLRoot = None
    
    def __init__(self, XMLPath=''):
        self.LoadTagsXML(XMLPath)

    def LoadTagsXML(self, XMLPath=''):
        if XMLPath=='': XMLPath = os.path.join(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__), "Tag_list.xml")
        self.XMLTree = ET.parse(XMLPath)
        self.TagXMLRoot = self.XMLTree.getroot()

    def liste_tag_by_section(self, section_id):
        list=[]
        for section in self.TagXMLRoot.findall('SECTION'):
                id = section.get('id')
                if int(id) == section_id:
                    for tag in section.findall('tag'):
                            id = tag.find('tagid').text
                            list.append(id)
        list.sort()       
        return list

    def get_tag_list(self):
        list=[]
        for section in self.TagXMLRoot.findall('SECTION'):
            for tag in section.findall('tag'):
                 id = tag.find('tagid').text
                 list.append(id)
        list.sort()
        return list
    
    def get_information(self, ch):
        list=[]
        for section in self.TagXMLRoot.findall('SECTION'):
            for tag in section.findall('tag'):
                id = tag.find('tagid').text
                if ch == id :
                    Length = tag.find('Length').text
                    Format = tag.find('Format').text
                    Flag = tag.find('Flag').text
                    description = tag.find('description').text
                    Name = tag.find('Name').text
                    list = [id, Name ,Format ,Length,description, Flag]
                    break        
        return list

    def get_items(self, ch):
        list=[]
        for section in self.TagXMLRoot.findall('SECTION'):
            for tag in section.findall('tag'):
                id = tag.find('tagid').text
                if ch == id :
                    for item in tag.findall('item'):
                        description = item.get('information')
                        index = int(item.get('index'))
                        list.append (index)
                        list.append(description)      
        return list
    
    def is_decodable(self,ch):
        for section in self.TagXMLRoot.findall('SECTION'):
            for tag in section.findall('tag'):
                id = tag.find('tagid').text
                if ch == id :
                    Flag = tag.find('Flag').text
                    self.test=int(Flag)
                    break
        return self.test      

