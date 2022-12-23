def run(filepath):
    rawLines = open(filepath).readlines()
    decommentedLines = []
    lineSoFar = ""

    for line in rawLines:
        lineSoFar = ""
        
        for char in line:
            if char == '#':
                break
            lineSoFar += char
        decommentedLines.append(lineSoFar)
    return decommentedLines
