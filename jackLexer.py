import re
import sys
class Lexer():

    def __init__(self, FileName):
        self.fileName = FileName
        self.tokenRegex = r'\".*?\"|{|}|\(|\)|\[|]|\.|,|;|\+|-|\*|/|&|\||<|>|=|~|[A-Za-z|_]+[\w|_]*|\d+'
        self.commentRegex = r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\''
        self.tokenList = None
        self.keywordList = ['class', 'constructor', 'function', \
        'method', 'field', 'static', 'var', 'int', 'char', \
        'boolean', 'void', 'true', 'false', 'null', 'this', \
        'let', 'do', 'if', 'else', 'while', 'return']

        self.symbolList = ['{','}', '(', ')', '[', ']', '.', \
        ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~', '&lt;', '&gt;', '&amp;']

    def parseFile(self):
        fileString = open(self.fileName, 'r').read()    
        self.getTokens(self.stripComments(fileString))

    def stripComments(self, string):
        for token in re.compile(self.commentRegex, re.DOTALL | re.MULTILINE).findall(string):
            string = string.replace(token,"")
        print string
        return string

    def getTokens(self, string):
        self.tokenList = re.findall(self.tokenRegex, string) #compile(self.tokenRegex)

    def getTokenString(self, token):
        if token in self.keywordList:
            return "<keyword> "+ token + " </keyword>"
        elif token in self.symbolList:
            if token == '<' or token == '&lt;':
                token = '&lt;'
            elif token == '>' or token == '&gt;':
                token = '&gt;'
            elif token == '&' or token == '&amp;':
                token = '&amp;'
            return "<symbol> "+ token + " </symbol>"
        elif token.isdigit():
            return "<integerConstant> "+token+" </integerConstant>"
        elif '"' in token:
            return "<stringConstant> "+token[1:-1]+" </stringConstant>"
            sys.pause()
        else: 
            return "<identifier> "+ token + " </identifier>"

    def printTokens(self):
        if self.tokenList == None:
            return
        print "<tokens>"
        for token in self.tokenList:
            print self.getTokenString(token)
        print "<\\tokens>"

    def hasNextToken(self):
        return self.tokenList

    def getNextToken(self):
        if self.hasNextToken():
            return self.getTokenString(self.tokenList.pop(0))
        else:
            return None

    def pushToken(self, token):
        self.tokenList.insert(0,token)



def main():
    fileName = sys.argv[1]
    lexer = Lexer(fileName)
    lexer.parseFile()
    while lexer.hasNextToken():
        print lexer.getNextToken();


if __name__ == '__main__':
    main()