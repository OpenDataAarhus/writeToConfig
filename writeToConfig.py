__author__ = 'aztst40'
import argparse

def getLine(textFile,curPos):
    sLine=textFile.rfind("\n",0,curPos)
    eLine=textFile.find("\n",curPos)+1
    return textFile[sLine+1:eLine-1]

def search(textFile,sub,start,comment):
    curPos=0
    while curPos>-1:
        curPos=textFile.find(sub,start)
        line=getLine(textFile,curPos)
        comPos=line.find(comment)
        subPos=line.find(sub)
        if (comPos>subPos) or comPos==-1 or sub.find(comment)>-1:
            return curPos
        else:
            start=curPos+1
    return curPos

def getOption(textFile,section,option):
    o=0
    sectionStart=search(textFile,section,0,"#")
    start=sectionStart
    while o>-1:
        o=search(textFile,option,start,"#")
        line=getLine(textFile,o)
        elm=line.find("=") #erLigMed
        opt=line[:elm+1].replace(' ','')
        if opt==option + "=":
            return line[elm+1:]
        else:
            start=o+len(line)+1
    return None

def getOptionLine(textFile,section,option):
    o=0
    sectionStart=search(textFile,section,0,"#")
    start=sectionStart
    while o>-1:
        o=search(textFile,option,start,"#")
        line=getLine(textFile,o)
        elm=line.find("=") #erLigMed
        opt=line[:elm+1].replace(' ','')
        if opt==option + "=":
            return line
        else:
            start=o+len(line)+1
    return None

def getOptionPos(textFile,section,option):
    o=0
    sectionStart=search(textFile,section,0,"#")
    start=sectionStart
    while o>-1:
        o=search(textFile,option,start,"#")
        line=getLine(textFile,o)
        elm=line.find("=") #erLigMed
        opt=line[:elm+1].replace(' ','')
        if opt==option + "=":
            return o
        else:
            start=o+len(line)+1
    return o

def setOption(textFile,section,option,value,add):
    optionPos=getOptionPos(textFile,section,option)
    if add==False:
        elm=textFile.find("=",optionPos)
    else:
        elm=textFile.find("\n",optionPos)-1
    eol=textFile.find("\n",elm)
    start=textFile[:elm+1]
    end=textFile[eol:]
    print "value=" + value
    textFile=start + value + end
    return textFile

def commentOutLine(textFile,section,option,value,add):
    optionPos=getOptionPos(textFile,section,option)
    start=textFile[:optionPos]
    end=textFile[optionPos:]
    textFile=start + "#" + end
    return textFile

def addOption(textFile,section,option,at,value):
    sectionPos=search(textFile,section,0,"#")
    if at!="":
        sectionPos=textFile.find(at,sectionPos)
    eol=textFile.find("\n",sectionPos)
    start=textFile[:eol+1]
    end=textFile[eol:]
    return start + option + '=' + value + end

def readTextFile(fileName):
    with open(fileName, "r") as file:
        textFile=file.read()
        file.close()
    return textFile

def addSetProperty(fileName,section,option,value,aeof,acaa):
    textFile=readTextFile(fileName)
    if section is None:
        section=''
    oValue=getOption(textFile,section,option)

    if oValue is not None:
        if acaa==True:
            line=getOptionLine(textFile,section,option)
            textFile=commentOutLine(textFile,section,option,value,aeof)
            if aeof==True:
                textFile=addOption(textFile,section,option,line,oValue + value)
            else:
                textFile=addOption(textFile,section,option,line,value)
            print "textFile=" + textFile
        else:
            textFile=setOption(textFile,section,option,value,aeof)
    else:
        textFile=addOption(textFile,section,option,"",value)
    writeTextFile(fileName,textFile)

def writeTextFile(fileName,textFile):
    text_file = open(fileName, "w")
    text_file.write(textFile)
    text_file.close()

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-f','--filename', help='Configuration file.', required=True)
parser.add_argument('-s','--section', help='Section.', required=False)
parser.add_argument('-o','--option', help='Option.', required=True)
parser.add_argument('-v','--value', help='Value.', required=True)
parser.add_argument('-al','--addline', help='Add to end of line.', required=False,nargs='?',const=False)
parser.add_argument('-a','--add', help='Comment and Add.', required=False,nargs='?',const=False)
parser.add_argument('-strip','--strip', help='Strip spaces.', required=False,nargs='?',const=False)
args = vars(parser.parse_args())

if args['addline'] is None:
    aeol=False
else:
    aeol=True
print "args[add]=" + str(args['add'])
if args['add'] is None:
    acaa=False
else:
    acaa=True
addSetProperty(args['filename'],args['section'],args['option'],args['value'],aeol,acaa)

#-f jetty -o JETTY_HOST -s #JETTY_HOST -v "127.0.0.1" -a true
#-f jetty -o JETTY_PORT -s #JETTY_PORT -v "8983" -a true
#-f jetty -o NO_START -v "0" -a true
#-f jetty -o JAVA_HOME -s #JAVA_HOME -v "/usr/lib/jvm/java-6-openjdk-amd64/" -a true

