import sys
from checkList import *
def getCFile(file, isTest):
    # f = open('/root/qxahz/stations.txt')
    f = open(file)
    tmp = ''
    line = f.readline()

    # pre-defined variables
    lineNumber = 1
    TabNumber = 0
    previousIndentation = 0

    indentationCheckLine = []
    indentationSpaceWarning = []
    spaceWarning = []
    result = ' ---------- Your Original Code File ----------\n'

    while line:
        tmp = line
        lineWithoutSpaceAndTab = line.replace(' ', '')
        lineWithoutSpaceAndTab = lineWithoutSpaceAndTab.replace('\t', '')
        lineWithoutSpaceAndTab = lineWithoutSpaceAndTab.replace('\n', '')

        if lineWithoutSpaceAndTab[0:2] != '//':
            # check indentation
            tabNumber = checkTabNumber(line)
            standardIndentation = IndentationForLine(line, previousIndentation)
            outputStandardIndentation = standardIndentation

            if standardIndentation != tabNumber:
                if not(len(lineWithoutSpaceAndTab) == 0 and standardIndentation != 0):
                    print('Warning')
                    indentationCheckLine.append(lineNumber)

            print(lineNumber,' ', outputStandardIndentation, ' ', tabNumber, line)
            result += str(lineNumber) + '\t |' + line

            previousIndentation = standardIndentation + predictIndentationChangeNextLine(line, tabNumber)
            if previousIndentation < 0:
                previousIndentation = 0


            # check additional space
            if not checkSpaceIndentation(line):
                indentationSpaceWarning.append(lineNumber)

            # check space missed
            for i in checkSpaceBeforeAndAfterSign(line, lineNumber):
                spaceWarning.append(i)

        # read next line
        lineNumber += 1
        line = f.readline()
    f.close()


    if isTest:
        print(' ---------- Style Check Report ----------')
        if len(indentationCheckLine) == 0 and len(indentationSpaceWarning) == 0:
            print('Indentation check passed.')
        else:
            for i in indentationCheckLine:
                print('[Style Warning] Line ' + str(i + 1) + '. Please check indentation.')
            print()
            for i in range(0, 5):
                if i < len(indentationSpaceWarning):
                    print('[Style Warning] Line ' + str(indentationSpaceWarning[i]) + '. Use space instead of tab for indentation.')
            if len(indentationSpaceWarning) > 5:
                print('With other ' + str(len(indentationSpaceWarning) - 5) + ' lines...')
            print()

        if len(spaceWarning) == 0:
            print('Space check passed.\n\n')
        else:
            for i in range(0, 5):
                if i < len(spaceWarning):
                    print(spaceWarning[i])
            if len(spaceWarning) > 5:
                print('With other ' + str(len(spaceWarning) - 5) + ' places...')
            print()
    else:
        result = result.replace('<', '&lt;')
        result = result.replace('>', '&gt;')
        result = result.replace('>', '&gt;')
        result += '\n ---------- Style Check Report ----------\n'
        if len(indentationCheckLine) == 0 and len(indentationSpaceWarning) == 0:
            result += 'Indentation check passed.\n\n'
        else:
            for i in indentationCheckLine:
                result += '[Style Warning] Line ' + str(i + 1) + '. Please check indentation.\n'
            result += '\n'
            for i in range(0, 5):
                if i < len(indentationSpaceWarning):
                    result += '[Style Warning] Line ' + str(indentationSpaceWarning[i]) + '. Use space instead of tab for indentation.\n'
            if len(indentationSpaceWarning) > 5:
                result += 'With other ' + str(len(indentationSpaceWarning) - 5) + ' lines...\n'
            result += '\n'

        if len(spaceWarning) == 0:
            result += 'Space check passed.\n\n'
        else:
            for i in range(0, 5):
                if i < len(spaceWarning):
                    result += (spaceWarning[i] + '\n')
            if len(spaceWarning) > 5:
                result += 'With other ' + str(len(spaceWarning) - 5) + ' places...\n'
            result += '\n'

        return result

# check tab or blank spaces for indentation check
def checkTabNumber(checkLine):
    tabNumber = 0
    # print(checkLine.find('   '))
    while (checkLine.find('\t') != -1 and checkLine.find('\t') < 2) or (checkLine.find('  ') != -1 and checkLine.find('  ') < 2) or (checkLine.find('    ') != -1 and checkLine.find('    ') < 2) or \
            (checkLine.find('   ') != -1 and checkLine.find('   ') < 2):
        tabNumber += 1
        blankIndex = checkLine.find('    ')
        tabIndex = checkLine.find('\t')
        # print(blankIndex, ' ', tabIndex, ' ', tabNumber)

        if blankIndex < tabIndex and blankIndex != -1:
            checkLine = checkLine[checkLine.find('    ') + len('    '):]
        elif blankIndex == -1:
            if checkLine.find('   ') != -1 and checkLine.find('   ') < 2:
                checkLine = checkLine[checkLine.find('   ') + len('   '):]
            elif checkLine.find('  ') != -1 and checkLine.find('  ') < 2:
                checkLine = checkLine[checkLine.find('  ') + len('  '):]
            else:
                checkLine = checkLine[checkLine.find('\t') + len('\t'):]
        elif blankIndex > tabIndex and tabIndex != -1:
            checkLine = checkLine[checkLine.find('\t') + len('\t'):]
        elif tabIndex == -1:
            checkLine = checkLine[checkLine.find('    ') + len('    '):]
        elif checkLine.find('   ') != -1:
            checkLine = checkLine[checkLine.find('   ') + len('   '):]
        else:
            checkLine = checkLine[checkLine.find('  ') + len('  '):]
        # print(checkLine)

    return tabNumber

# check for indentation for a line
# return the correct indentation number for a line
def IndentationForLine(checkLine, PreviousIndentation):
    Indentation = PreviousIndentation

    # replace all unnecessary space and tab
    checkLine = checkLine.replace(' ', '')
    checkLine = checkLine.replace('\t', '')

    if checkLine.find('}') == 0 and checkLine.find('}') != -1:
        Indentation -= 1

    return Indentation

# check for indentation next line
# return the indentation change for a line without consideration of '{'
def predictIndentationChangeNextLine(checkLine, indentation):
    nextLineIndentationChange = 0

    while checkLine.find('{') != -1 or checkLine.find('}') != -1:
        if checkLine.find('{') < checkLine.find('}') and checkLine.find('{') != -1:
            nextLineIndentationChange += 1
            checkLine = checkLine[checkLine.find('{') + len('{'):]

        elif checkLine.find('{') < checkLine.find('}') and checkLine.find('{') == -1 and checkLine.find('}') > indentation:
            if nextLineIndentationChange > 0:
                nextLineIndentationChange -= 1
            checkLine = checkLine[checkLine.find('}') + len('}'):]

        elif checkLine.find('{') > checkLine.find('}') and checkLine.find('}') > indentation:
            if nextLineIndentationChange > 0:
                nextLineIndentationChange -= 1
            checkLine = checkLine[checkLine.find('}') + len('}'):]

        elif checkLine.find('{') > checkLine.find('}') and checkLine.find('}') == -1:
            nextLineIndentationChange += 1
            checkLine = checkLine[checkLine.find('{') + len('{'):]

        else:
            checkLine = checkLine[checkLine.find('}') + len('}'):]

    return nextLineIndentationChange

# check additional blank
def checkSpaceIndentation(checkLine):
    if checkLine.find('  ') == 0 or checkLine.find('  ') == 1:
        return False
    else:
        return True

# check space before and after certain sign
def checkSpaceBeforeAndAfterSign(checkLine, lineNumber):
    problem = []
    # check both spaces
    for i in bothBlank:
        tmpCheck = checkLine

        quotLenth = 0
        quotOne = 0
        quotTwo = 0

        while tmpCheck.find(i) != -1:

            if quotLenth <= 0:
                quotOne = tmpCheck.find('"')
                if quotOne != -1:
                    quotTwo = (tmpCheck[quotOne + 1:]).find('"') + quotOne + 1
                    if quotTwo != 0:
                        quotLenth = quotTwo - quotOne
                        # print("quot: ", quotTwo, quotOne)
                    else:
                        quotLenth = 0
                else:
                    quotTwo = -1

            print('quotlength: ' + str(quotLenth))
            flag = True
            # cancel report for noBlank signal
            for j in noBlank:
                if tmpCheck.find(i) == tmpCheck.find(j) and tmpCheck.find(i) != -1:
                    flag = False
                if tmpCheck.find(i) == tmpCheck.find(j) + 1 and tmpCheck.find(i) != -1 and j == 'h>':
                    flag = False
                if tmpCheck.find(i) == tmpCheck.find(j) + 4 and tmpCheck.find(i) != -1 and j == 'char*':
                    flag = False
                if tmpCheck.find(i) == tmpCheck.find(j) + 3 and tmpCheck.find(i) != -1 and j == 'int*':
                    flag = False
                if tmpCheck.find(i) == tmpCheck.find(j) + 6 and tmpCheck.find(i) != -1 and j == 'double*':
                    flag = False
                if tmpCheck.find(i) == tmpCheck.find(j) + 4 and tmpCheck.find(i) != -1 and j == 'bool*':
                    flag = False
                if tmpCheck.find(i) == tmpCheck.find(j) + 5 and tmpCheck.find(i) != -1 and j == 'char *':
                    flag = False
                if tmpCheck.find(i) == tmpCheck.find(j) + 4 and tmpCheck.find(i) != -1 and j == 'int *':
                    flag = False
                if tmpCheck.find(i) == tmpCheck.find(j) + 7 and tmpCheck.find(i) != -1 and j == 'double *':
                    flag = False
                if tmpCheck.find(i) == tmpCheck.find(j) + 5 and tmpCheck.find(i) != -1 and j == 'bool *':
                    flag = False
                if tmpCheck.find(i) == tmpCheck.find(j) + 5 and tmpCheck.find(i) != -1 and j == 'char**':
                    flag = False
                if tmpCheck.find(i) == tmpCheck.find(j) + 4 and tmpCheck.find(i) != -1 and j == 'int**':
                    flag = False
                if tmpCheck.find(i) == tmpCheck.find(j) + 7 and tmpCheck.find(i) != -1 and j == 'double**':
                    flag = False
                if tmpCheck.find(i) == tmpCheck.find(j) + 5 and tmpCheck.find(i) != -1 and j == 'bool**':
                    flag = False

            # check bothblank1 for avoiding repeatedly report
            for j in bothBlank1:
                if tmpCheck.find(i) == tmpCheck.find(j) and tmpCheck.find(i) != -1:
                    flag = False
                    # print('test')

            # Dont report blank inside quotation mark
            if not (tmpCheck.find(i) < quotLenth + quotOne and quotLenth > 0):
                if (tmpCheck[tmpCheck.find(i) - 1: tmpCheck.find(i)] != ' ' or tmpCheck[tmpCheck.find(i) + len(i): tmpCheck.find(i) + len(i) + 1] != ' ') and flag and tmpCheck.find(i) != 0:
                    problem.append('[Style Warning] Line ' + str(lineNumber) + '. Missing space before or after sign "' + i + '".')

            tmpCheck = tmpCheck[tmpCheck.find(i) + len(i):]
            # print(i, 'string: ', str(len(tmpCheck[:tmpCheck.find(i)])))
            quotLenth = quotLenth + quotOne - len(tmpCheck[:tmpCheck.find(i)]) - len(i)
            quotOne = quotOne - len(tmpCheck[:tmpCheck.find(i)]) - len(i)
            if quotOne < 0:
                quotOne = 0

    # check both spaces for bothspace1
    for i in bothBlank1:
        tmpCheck = checkLine
        while tmpCheck.find(i) != -1:

            if (tmpCheck[tmpCheck.find(i) - 1: tmpCheck.find(i)] != ' ' or tmpCheck[tmpCheck.find(i) + len(i): tmpCheck.find(i) + len(i) + 1] != ' '):
                problem.append(
                    '[Style Warning] Line ' + str(lineNumber) + '. Missing space before or after sign "' + i + '".')
            tmpCheck = tmpCheck[tmpCheck.find(i) + len(i):]

    return problem

# test purpose
# file = 'Lab2.c'
# getCFile(file, True)