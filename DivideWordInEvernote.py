#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re

def makeBlockToSave(content, title, templBlock):
    newBlock = re.sub('<title>(.*)</title>', '<title>%s</title>' % title,
                      templBlock, flags=re.DOTALL)

    content = re.sub(r'^\<\!\[CDATA\[.*<en-note>', '', content, flags=re.DOTALL)
    content = re.sub(r'<en-note>$', '', content, flags=re.DOTALL)

    # Removing tags which were apparently opened before division and adding tags closed after next division
    filteredContent = ''
    openedTagNames = []
    l = len(content)
    i = 0
    while i < l:
        tagBeginPos = content.find('<', i)
        if tagBeginPos >= 0:
            endPos = content.find('>', i + 1)
            if endPos < 0:
                raise Exception('No closing >')

            # curTag = content[tagBeginPos + 1 : endPos]
            substrBetween = content[i:tagBeginPos]
            filteredContent += substrBetween
            tagSubstr = content[tagBeginPos : endPos + 1]
            i = endPos + 1

            if tagSubstr[-2] == '/':
                filteredContent += tagSubstr
                continue

            curTagName = tagSubstr[1:-1]
            pos = curTagName.find(' ')
            if pos > 0:
                curTagName = curTagName[:pos]

            if tagSubstr[1] == '/':
                # </tag >
                curTagName = curTagName[1:]
                if not openedTagNames:
                    continue
                elif openedTagNames[-1] != curTagName:
                    raise Exception('Unexpected closing tag \'%s\'' % tagSubstr)

                filteredContent += tagSubstr
                del openedTagNames[-1]
                continue

            # <tag >
            openedTagNames.append(curTagName)
            filteredContent += tagSubstr
        else:
            filteredContent += content[i:]
    for tagName in reversed(openedTagNames):
        filteredContent += '</%s>' % tagName

    if filteredContent != content:
        print('Filter result:\n%s\n%s' % (content, filteredContent))

    # repl1 = re.sub('(<content>.*<en-note>).*(</en-note\n*>.*</content>)',
    #        r'\1%s\2' % filteredContent,
    #        newBlock, flags=re.DOTALL)
    #     # First variant. Breaks at Exercises after 'Glary Duplicate Cleaner 5.0' or looses \0
    res = re.search('(<content>.*<en-note>).*(</en-note>.*</content>)',
           newBlock, flags=re.DOTALL)
    # res - e.g. ((88, 15806), (88, 221), (15783, 15806))
    newBlock = newBlock[:res.span(1)[1]] + filteredContent + newBlock[res.span(2)[0]:]
    # assert newBlock == repl1
    return newBlock

def divideEvernoteWordFile(outFilePath, inFilePath):
    with open(inFilePath, 'r', encoding='utf-8') as inFile:
        inText = inFile.read()
        with open(outFilePath, 'w', encoding='utf-8') as outFile:
            # Searching for <note><title>События</title><content>...</note>

            # blocks = re.findall(r'<note>.*?<\/note>', inText, flags=re.DOTALL)
            findIt = re.finditer(r'<note>.*?<\/note>', inText, flags=re.DOTALL)
            templBlock = None
            for blockIt in findIt:
                if templBlock is None:
                    templBlock = blockIt.group(0)
                    templBlock = templBlock.replace('<source-application>evernote.win32</source-application>',
                                            '<source-application>DivideEvernoteWord.py</source-application>')
                    print('Template block: %s' % re.search('<title>(.*)</title>', templBlock).group(1))
                else:
                    blockToDivide = blockIt.group(0)
                    blockToDividePoss = blockIt.span(0)
            print('Main block: %s, %d byte(s)' % (re.search('<title>(.*)</title>', blockToDivide).group(1),
                                                  len(blockToDivide)))
            outFile.write(inText[:blockToDividePoss[0]])

            contentToDivide = re.search('<content>(.*)</content>', blockToDivide, flags=re.DOTALL).group(1)
            # Parsing blocks like <h2 style="text-align: center;"><span style="font-family: &quot;Times New Roman&quot;; color: rgb(1, 1, 1); font-size: 14pt; font-weight: bold;">Селигер</span></h2>
            findIt = re.finditer(r'<h([234])(?:(?: .*?)|)><span .*?>(.*?)</span>', contentToDivide, flags=re.DOTALL)
            curH2Title = ''
            curH3Title = ''
            prevPos = 0
            level = 1
            fullTitle = 'Main'
            results = list(findIt)
            print('%d header(s) found' % len(results))
            for hBlockIt in results:
                curPos = hBlockIt.span(0)[0]
                if not level is None:
                    newBlock = makeBlockToSave(contentToDivide[prevPos:curPos], fullTitle, templBlock)
                    outFile.write('\n\n')
                    outFile.write(newBlock)

                level = hBlockIt.group(1)
                title = hBlockIt.group(2)
                print('h%s %s' % (level, title))
                # title = re.search('<title>(.*)</title>', block).group(1)
                fullTitle = title
                if int(level) == 2:
                    curH2Title = title
                elif int(level) == 3:
                    curH3Title = title
                    if curH2Title.strip('\n\r\t '):
                        fullTitle = '%s / %s' % (curH2Title, title)
                else:
                    if curH3Title.strip('\n\r\t '):
                        fullTitle = '%s / %s' % (curH3Title, title)
                prevPos = curPos

            # newBlock = makeBlockToSave(contentToDivide[prevPos: ], fullTitle, templBlock)
            # outFile.write('\n\n')
            # outFile.write(newBlock)

            outFile.write('\n\n')
            outFile.write(inText[blockToDividePoss[1]:])


    # <en-media hash="66390225c7c231540e967eb6d44acb6a" type="image/jpeg" width="63"/>

if __name__ == '__main__':
    outFilePath = r'E:\Data\Evernote\Divided.enex'
    fileDir = r'E:\Data\Evernote' + '\\'  # r Python strings escape \' and \"
    # divideEvernoteWordFile(outFilePath, fileDir + 'Organizer1.enex')
    # divideEvernoteWordFile(outFilePath, fileDir + 'Startups.enex')
    divideEvernoteWordFile(outFilePath, fileDir + 'Exercises.enex')


