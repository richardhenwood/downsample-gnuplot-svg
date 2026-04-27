import shutil
import sys
import copy
import base64

from lxml import etree
import pyvips
#import cairosvg

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://w3.org"
NS_MAP = {None: SVG_NS, 'xlink': XLINK_NS}

inputsvgfile = sys.argv[1]
outputsvgfile = sys.argv[2]

root = etree.parse(inputsvgfile)

keepids = ['coord_text', 'hypertextbox', 'hypertext', 'hyperimage']
keeptags = ['coord_text', 'hypertextbox', 'hypertext', 'hyperimage']

def getparents(elem):
    #for parent in elem.getparent():
    parent = elem.getparent()
    if elem is parent:
        return
    if parent is None:
        return
    yield parent
    yield from getparents(parent)

def followXrefs(elem):
    if '{http://www.w3.org/1999/xlink}href' in elem.attrib:
        xrefid = elem.attrib['{http://www.w3.org/1999/xlink}href']
        for xref in root.xpath(f'//*[@id="{xrefid[1:]}"]'):
            yield xref
            yield from followXrefs(xref)
    return

# crawl across the tree, marking any elements that 
# provide interaction with 'HACK'.
# We will keep these elements as svg and all non-interactive
# elements we will convert to to a png.
root.getroot().set('HACK','keep')
for elem in root.xpath(".//*[@onmousemove]"):
    elem.set('HACK', 'keep')
    for child in elem.iterchildren():
        if child.tag == '{http://www.w3.org/2000/svg}use':
            child.set('HACK', 'keep')
    for parent in getparents(elem):
        try:
            parent.set('HACK', 'keep')
        except TypeError as ex:
            pass
# keep all script tags
for elem in root.xpath("//*[local-name()='script']"):
    try:
        elem.set('HACK', 'keep')
    except TypeError as ex:
        pass
# keep all special ids:
for specialid in keepids:
    for elem in root.xpath(f"//*[@id='{specialid}']"):
        try:
            elem.set('HACK', 'keep')
        except TypeError as ex:
            pass
# keep all text elements:
for elem in root.xpath("//*[local-name()='text']"):
    try:
        elem.set('HACK', 'text')
    except TypeError as ex:
        pass
    for descendent in elem.iterdescendants():
        try:
            descendent.set('HACK', 'text')
        except TypeError as ex:
            pass
    for parent in getparents(elem):
        try:
            parent.set('HACK', 'text')
        except TypeError as ex:
            pass
        

# look through the elements we want to keep and
# check to see if they have an cross references.
# mark these with HACK as well.
for elem in root.iter():
    if elem.get('HACK'):
        for xrefelem in followXrefs(elem):
            xrefelem.set('HACK', 'keep')
            #xrefelem.set('opacity', '0')
            for parent in getparents(xrefelem):
                try:
                    parent.set('HACK', 'keep')
                except TypeError as ex:
                    pass

# make a copy of the tree. 
onlygraphics = copy.deepcopy(root)
# with the 'root' copy we delete all the elements that are missing a 'HACK' attribute.
to_delete = []
for elem in root.iter():
    if elem.get('HACK'):
        continue
    to_delete.append(elem)
    
for elem in to_delete:    
    try:
        elem.getparent().remove(elem)
    except TypeError as ex:
        pass

# the other copy of the tree we use to make a lossy graphics background
# we need to delete the text elements:
to_delete = []
for elem in onlygraphics.iter():
    if elem.get('HACK') == 'text':
        to_delete.append(elem)
for elem in to_delete:    
    try:
        elem.getparent().remove(elem)
    except TypeError as ex:
        pass


# write the background png:
svg_string_data = etree.tostring(onlygraphics, encoding="utf-8") 

image = pyvips.Image.svgload_buffer(svg_string_data)
background = image.write_to_buffer(".png")

#cairosvg falls over with args SVGs
#background = cairosvg.svg2png(bytestring=byte_data)
background64 = base64.b64encode(background)
data_uri = f"data:image/png;base64,{background64.decode()}"

_, _, width, height = root.getroot().attrib['viewBox'].split()
imageelem = etree.Element(
    "{http://www.w3.org/2000/svg}image", {
    "x": "0",
    "y": "0",
    "width": width,
    "height": height,
    "stroke-width": "0",
    "{http://www.w3.org/1999/xlink}href": f"{data_uri}"  # Path to your image
})
# add the image early in the drawing commands so it is below everything
root.xpath("//*[@id='gnuplot_canvas']")[0].insert(0, imageelem)

# before we write out or svg overlay, make it all transparent so we can see the 
# png beneath
for elem in root.iter():
    if elem.get('HACK'):
        for xrefelem in followXrefs(elem):
            xrefelem.set('opacity', '0')
            for parent in getparents(xrefelem):
                try:
                    parent.set('HACK', 'keep')
                except TypeError as ex:
                    pass
root.write(outputsvgfile, pretty_print=True, xml_declaration=True, encoding="UTF-8")