import xml.etree.ElementTree as e
a = e.parse('bookmarks.xbel')
r = a.getroot()
print('<html><body>')
for c in r:
  try:
    print('<a href=\"' + c.attrib['href'] + '\" > X'  + '</a>  <br>')
  except:
    pass
  finally:
    pass
print('</body></html>')
