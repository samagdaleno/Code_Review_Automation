import re
import os
import fnmatch
    
count = 0
fileName = ""
exclusionList = ["App.xaml.cs",
                "Resources.Designer.cs", 
                "ImportQntFile.feature.cs",
                "RoleCreation.feature.cs", 
                "AssemblyInfo.cs", 
                ".NETFramework,Version=v4.8.AssemblyAttributes.cs", 
                "NUnit.AssemblyHooks.cs"]

def getFilePathsFromDirectory(directoryPath):
    global fileName
    for path, currentDirectory, files in os.walk(directoryPath):
        for file in fnmatch.filter(files, '*.cs'):
            #print(os.path.join(path, file))
            fileName = file
            exclusionBool = ".g." in fileName or ".AssemblyInfo." in fileName
            if((fileName not in exclusionList) and (not exclusionBool)):
                readFileLineByLine(os.path.join(path, file))

def readFileLineByLine(filePath):
    global count
    count = 0 
    file = open(filePath, encoding='utf-8-sig')
    FileLines = file.readlines()

    #print("Reading: {}".format(filePath))
    commentBlock = []
    commentBlockStart = False
    previousLine = ""
    for line in FileLines:
        count += 1
        trimmedLine = line.strip()
        checkForVarDeclaration(trimmedLine, "private")
        checkForVarDeclaration(trimmedLine, "public")
        #checkForMethodDeclaration(trimmedLine)

        #Check for comment block         
        if(trimmedLine.startswith('//')):
            if(not previousLine.startswith('//')):
                commentBlockStart = True
                commentBlock.append(trimmedLine)
            
            elif (commentBlockStart):
                commentBlock.append(trimmedLine)

        elif(commentBlockStart):
            #sent comentBlock to method
            checkCommentBlock(commentBlock)
            commentBlockStart = False
            commentBlock = []

        previousLine = trimmedLine


def checkForVarDeclaration(line, accessModifier):

    if(re.match(r'^'+accessModifier+'\s[\w\S]+\s\w+;$', line)):
        checkCorrectVarSintax(line, 2, accessModifier)

    elif(re.match(r'^'+accessModifier+'\s[\w\S]+\s\w+\s=\s[\w\d\S]+;$', line)):
        checkCorrectVarSintax(line, 2, accessModifier)

    # elif(re.match(r'^private\s[\w\S]+\s[\w\S]+\s=>\s[\w\d\S]+;$', line)):  # Not clear
    #      checkCorrectPrivateSintax(line, 4)

    elif(re.match(r'^'+accessModifier+'\s\w+\s[\w\S]+\s\w+;$', line)):
        checkCorrectVarSintax(line, 3, accessModifier)

    elif(re.match(r'^'+accessModifier+'\s\w+\s[\w\S]+\s\w+\s=\s[\w\d\S]+;$', line)):
        checkCorrectVarSintax(line, 3, accessModifier)

def checkForMethodDeclaration(line):
    if(re.match(r'\b(public|private|internal|protected)\s*(static|virtual|abstract)?\s*[a-zA-Z]*\s[a-zA-Z]+\s*\((([a-zA-Z\[\]\<\>]*\s*[a-zA-Z]*\s*)[,]?\s*)+\)', line)):
        print(re.match(r'\b(public|private|internal|protected)\s*(static|virtual|abstract)?\s*[a-zA-Z]*\s[a-zA-Z]+\s*\((([a-zA-Z\[\]\<\>]*\s*[a-zA-Z]*\s*)[,]?\s*)+\)', line).groups())
        print(line)
        print('------------------------------------')



def checkCorrectVarSintax(line, namePosition, accessModifier):
    global fileName
    wordArr = line.split()
    if ((accessModifier == "private") and (not wordArr[namePosition].startswith("_"))):
        print('------------------------------------')
        print("Private naming convention not followed!")
        print("On file: {}".format(fileName))
        print("Line {}: {}".format(count, line.strip()))

    elif ((accessModifier == "public") and (not wordArr[namePosition][0].isupper())):
        print('------------------------------------')
        print("Public naming convention not followed!")
        print("On file: {}".format(fileName))
        print("Line {}: {}".format(count, line.strip()))
        print('------------------------------------')



def checkCommentBlock(commentList):
    global fileName
    printBlock = True
    for line in commentList:
        if (("TODO:" in line) or ("<" in line)) :
            printBlock = False
            break
    # if(printBlock):
    #     print(commentList)

def main():
    print("Checking for correct naming conventions...")

if __name__ == "__main__":
    main()
    print("")
    getFilePathsFromDirectory("YOUR REPO PATH")
    #readFileLineByLine("Test.cs")
    print("finished.")