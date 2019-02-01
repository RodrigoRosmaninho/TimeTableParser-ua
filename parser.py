from pyquery import PyQuery as pq
from lxml import etree
import sys

class Subject:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __eq__(self, other):
        return self.name == other.name

class Lecture:
    def __init__(self, day, start, finish):
        self.day = day
        self.start = start
        self.finish = finish

class Class:
    def __init__(self, subject, comp, descr, include):
        self.subject = subject
        self.comp = comp
        self.descr = descr
        self.include = include
        self.lectures = []

    def isEqual(self, c):
        return c.subject == self.subject and c.comp == self.comp and c.descr == self.descr

    def getInclude(self):
        if(self.include):
            return "true"
        else:
            return "false"

classes = []

fout = open('timetable.sttx', 'w')
root = etree.Element("timetable")

dayOfWeek = {
    "Segunda" : "Monday",
    "Terça"   : "Tuesday",
    "Quarta"  : "Wednesday",
    "Quinta"  : "Thursday",
    "Sexta"   : "Friday",
    "Sábado"  : "Saturday"
}


def findClass(list, c):
    for item in list:
        if c.isEqual(item):
            return item
    list.append(c)
    return c

def getTime(time):
    time = time.split(":")
    return (int(time[0]) * 60) + int(time[1])

def parseSubject(subject):
    if "-" not in subject:
        return subject

    split = subject.split("-")
    numerals = split[len(split) - 1]
    if "I" in numerals or "V" in numerals:
        value = 0
        for char in numerals:
            if char == "I":
                value += 1
            elif char == "V":
                value += 5
        return subject[:subject.rfind("-")] + str(value)

    elif numerals.isdigit():
        return subject[:subject.rfind("-")] + numerals

    else:
        return subject

def handleEvent(index, node):
    global classes
    n = pq(node)

    title = node.attrib['title'].split(" ")
    color = node.attrib['bgcolor'].split("#")[1]
    day = dayOfWeek[title[0]]
    start = getTime(title[1].split("-")[0])
    finish = getTime(title[1].split("-")[1])
    subject = parseSubject(n.find("span").text().split(" ")[0])
    location = n.find("sala").text()[1:]
    info = n.find("c").text().split("  ")
    descr = info[0]
    comp = info[1][1:-1]

    if comp in descr:
        descr = descr[len(comp):]

    newClass = Class(Subject(subject, color), comp, descr, not comp == "OT")
    newLecture = Lecture(day, start, finish)

    # Determine if Class already exists
    newClass = findClass(classes, newClass)
    newClass.lectures.append(newLecture)

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

def getSubjects():
    subjects = []
    for c in classes:
        if not c.subject in subjects:
            subjects.append(c.subject)
    return subjects


def main():
    f = pq(url=sys.argv[1])
    f("#gvHorario").find(".event").each(handleEvent)

    for s in getSubjects():
        newSubject = etree.SubElement(root, "subject")
        newSubject.text = s.name

    for c in classes:
        saveClass(c)

    colormode = etree.SubElement(root, "colormode")
    colormode.text = "RELATIVE"

    allcolors = etree.SubElement(root, "allcolors")
    saveColor(allcolors, "000000", "000000", "000000", "000000")

    for s in getSubjects():
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

    print("Export Successful!")

if __name__ == "__main__":
    main()