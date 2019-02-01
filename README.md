# TimeTableParser-ua
Python tool for scraping any timetable page on the University of Aveiro's academic portal (PACO) and exporting it to different formats.

Particularly useful for use in software that helps you generate alternative timetables.
Multiple timetables can be joined in one exported file, which helps people who have classes from different curricular years

### Usage:

After cloning this repository, navigate to its directory, and run:
```
python3 parser.py
```

##### Optional arguments:
If they are not specified the script will prompt you for the required values.
                  
| Argument    | Function                                       |
| ----------- | ---------------------------------------------- |
| -h, --help  | Show help message                              |
| -d dest     | Specify destination filename                   |
| -u [urls]   | Specify all timetable urls separated by spaces |
| -f format   | specify desired output format (eg: sttx)       |

#### Requirements:

- Python 3.x
- [pyquery](https://pypi.org/project/pyquery/)
- [lxml](https://pypi.org/project/lxml/)

#### Getting PACO Timetable URLs
1. Go to https://paco.ua.pt/horariosweb/
2. Pick your department and course
3. Click on the link icon on the top of the screen to generate the url
4. Rinse and repeat for all the desired urls
<br>

### Available Formats:
- .sttx
- .json (coming soon)


#### About .sttx:
Format used by [SmartTimeTable](http://code.ua.pt/projects/stt), a java Swing app made by MIECT student Diogo Regateiro that generates all the permutations of possible timetables.
Available for download [here]().
