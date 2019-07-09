import xml.etree.ElementTree as ET

DATAPATH = "abbott-smith.tei_lemma.xml"

NAMESPACE = "{http://www.crosswire.org/2013/TEIOSIS/namespace}"
toText = lambda y: list(map(lambda x: x.text, y))
 
def processSense(s):
    stext = s.text
    print(stext)
    glosses = toText(s.findall(".//" + NAMESPACE  + 'gloss'))
    if glosses == []:
        return  [stext]
    return glosses

flatten = lambda l: [item for sublist in l for item in sublist]
removeNone = lambda x: list(filter(lambda y: y, x))

def processEntry(entry):
    orth = entry.get('lemma')
    if not (orth):
        return None
    else:
        print(orth)
    senses = entry.findall(NAMESPACE +'sense')
    gls = removeNone(map(lambda x: removeNone(processSense(x)), senses))
    filtered = []
    print(list(gls))
    gloform =  " | ".join(flatten(gls))
#    if gloform == '':
#        gloform = "?"
    return orth + "\t" + gloform 

def processFile(fpath):
    doc = ET.parse(fpath)
    root = doc.getroot()
    entries =  root.findall('.//' + NAMESPACE + "entry")
    out = list(filter(lambda x: x, map(lambda x: processEntry(x),entries )))
    print( fpath + " " + str(len(out)))
    with open('gloss-dict.tab', 'w', encoding="utf-8") as f:
        f.write('\n'.join(out).strip())


processFile(DATAPATH)

print("done")
