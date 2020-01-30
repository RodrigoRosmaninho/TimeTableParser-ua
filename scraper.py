import sys

# Try to import pyquery. If the module is not found, print an error and quit program
try:
    from pyquery import PyQuery as pq
except:
    print("\nError. The 'pyquery' module was not found on your system.\nInstall it by running 'pip install pyquery'")
    sys.exit(4)

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
    descr = info[0].split(" ")[-1]
    comp = info[1][1:-1]

    if comp in descr:
        descr = descr[len(comp):]

    # If no descr is specified, hardcode value 1 to avoid NullPointerException on SmartTimeTable
    if len(descr) == 0:
        descr = "1"

    newClass = Class(Subject(subject, color), comp, descr, not comp == "OT")
    newLecture = Lecture(day, start, finish)

    # Determine if Class already exists
    newClass = findClass(classes, newClass)
    newClass.lectures.append(newLecture)


def getClasses(url):
    global classes
    classes = []

    f = pq(url=url)
    f("#gvHorario").find(".event").each(handleEvent)
    return classes
