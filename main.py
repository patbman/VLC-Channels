import re
import csv
import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import xml.etree.cElementTree as ET



def getChannels(homerunIP,name):
    #homerunIP = 'http://10.0.0.12'
    browser = webdriver.Chrome()
    #browser = webdriver.Chrome('chromedriver.exe')
    count = 0
    Channels={}
    browser.get('http://'+homerunIP+'/lineup.html')
    time.sleep(3)
    soup = bs(browser.page_source, 'lxml')
    browser.close()
    for i in soup.find("table", {"id": "channelTable"}):
        channelNumber = re.search('^\d+',i.text)[0]
        channelName = re.search('[^\d]+',i.text)[0]
        Channels[count]=[channelNumber,channelName]
        count+=1

    makePlaylist(Channels,name)
def makePlaylist(Channels,name):

    data = ET.Element('playlist')
    items = ET.SubElement(data, 'title')
    trackList = ET.SubElement(items, 'trackList')
    data.set("xmlns","http://xspf.org/ns/0/")
    data.set("xmlns:vlc","http://www.videolan.org/vlc/playlist/ns/0/")
    data.set("version","1")
    items.text = 'Playlist'



    for x , y in Channels.items():
        Track = ET.SubElement(trackList, 'track')

        Location = ET.SubElement(Track, 'location')
        Location.text = 'http://10.0.0.12:5004/auto/v' + y[0]

        itemTitle = ET.SubElement(Track, 'title')
        itemTitle.text = y[1]

        Extension = ET.SubElement(Track, 'extension')
        Extension.set('application', 'http://www.videolan.org/vlc/playlist/0')

        Vid = ET.SubElement(Extension, 'vlc:id')
        Vid.text = str(x)

        Vop1 = ET.SubElement(Extension, 'vlc:option')
        Vop1.text = 'network-caching=1000'

        Vop2 = ET.SubElement(Extension, 'vlc:option')
        Vop2.text = 'file-caching=300'

    Ext2 = ET.SubElement(trackList, 'extension')
    Ext2.set('application','http://www.videolan.org/vlc/playlist/0')

    for x in Channels.keys():
        Vlit = ET.SubElement(Ext2, 'vlc:item')
        Vlit.set('tid',str(x))



    tree=ET.ElementTree(data)
    tree.write(name+".xspf")

getChannels(homerunIP=input('insert IP of HDhomerun: '),name=input('insert channel playlist name: '))