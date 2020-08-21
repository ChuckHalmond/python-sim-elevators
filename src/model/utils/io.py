import sys

line = 20 * '-'

def progressBar(value, endvalue, bar_length = 40):

    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\rProgress : [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()

def appendToStreamLineStartingWith(stream, mapping):
    starts = mapping.keys()
    linesStartingWith = {}
    
    stream.seek(0)
    for line in stream:
        for start in starts:
            if line.startswith(start):
                linesStartingWith[start] = line.rstrip('\n')
    stream.seek(0)

    content = stream.read()
    for start in starts:
        lineStartingWith = linesStartingWith[start]
        if (lineStartingWith != None):
            content = content.replace(lineStartingWith, lineStartingWith + mapping[start])

    stream.seek(0)
    stream.truncate()
    stream.write(content)