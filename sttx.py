import sys

# Try to import pyquery. If the module is not found, print an error and quit program
try:
    from lxml import etree
except:
    print("\nError. The 'lxml' module was not found on your system.\nInstall it by running 'pip install lxml'")
    sys.exit(5)

root = etree.Element("timetable")

def saveLecture(elem, l):
    newLecture = etree.SubElement(elem, 'lecture')

    day = etree.SubElement(newLecture, "day")
    day.text = l.day

    start = etree.SubElement(newLecture, "start")
    start.text = str(l.start)

    finish = etree.SubElement(newLecture, "finish")
    finish.text = str(l.finish)


def saveClass(c):
    newClass = etree.SubElement(root, 'class')
    newClass.set("subject", c.subject.name)

    comp = etree.SubElement(newClass, "comp")
    comp.text = c.comp

    descr = etree.SubElement(newClass, "descr")
    descr.text = c.descr

    include = etree.SubElement(newClass, "include")
    include.text = c.getInclude()

    for l in c.lectures:
        saveLecture(newClass, l)


def saveColor(elem, t, tp, p, ot):
    color_t = etree.SubElement(elem, 't')
    color_t.text = str(int(t, 16) - 1)

    color_tp = etree.SubElement(elem, 'tp')
    color_tp.text = str(int(tp, 16) - 1)

    color_p = etree.SubElement(elem, 'p')
    color_p.text = str(int(p, 16) - 1)

    color_ot = etree.SubElement(elem, 'ot')
    color_ot.text = str(int(ot, 16) - 1)

def getSubjects(classes):
    subjects = []
    for c in classes:
        if not c.subject in subjects:
            subjects.append(c.subject)
    return subjects


def export(name, classes):

    if ".sttx" not in name:
        name = name + ".sttx"

    fout = open(name, 'w')

    for s in getSubjects(classes):
        newSubject = etree.SubElement(root, "subject")
        newSubject.text = s.name

    for c in classes:
        saveClass(c)

    colormode = etree.SubElement(root, "colormode")
    colormode.text = "RELATIVE"

    allcolors = etree.SubElement(root, "allcolors")
    saveColor(allcolors, "000000", "000000", "000000", "000000")

    for s in getSubjects(classes):
        newColor = etree.SubElement(root, "colormapping")
        subject = etree.SubElement(newColor, "subject")
        subject.text = s.name
        saveColor(newColor, s.color, s.color, s.color, "000000")

    overlapping = etree.SubElement(root, "overlapping")

    mode = etree.SubElement(overlapping, "mode")
    mode.text = "NONE"

    count = etree.SubElement(overlapping, "count")
    count.text = "null"

    time = etree.SubElement(overlapping, "time")
    time.text = "null"

    fout.write(etree.tostring(root, xml_declaration=True, encoding="utf-8", pretty_print=True).decode('utf-8'))
    fout.close()

if __name__ == "__main__":
    main()