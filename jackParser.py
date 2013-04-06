
import re
from jackLexer import Lexer

class Parser():
	""" house keeping"""
	def __init__(self, fileName):
		self.lexer = Lexer(fileName)
		self.lexer.parseFile()
		out = fileName.split(".")[0]+".xml"
		self.outFile = open(out, "w")
	
	def closeFile(self):
		self.outFile.close()

	def returnToken(self, token):
		key, name = self.getTokeninfo(token)
		if key == 'stringConstant':
			name = '"' + name + '"'
		self.lexer.pushToken(name)

	def getTokeninfo (self, tokenString):
		""" in format <token> value </token>"""
		regex = r"<(\w+)> (.*?) </\w+>"
		match = re.compile(regex).match(tokenString)
		return match.group(1), match.group(2)

	def write(self, string):
		self.outFile.write(string + "\n")
		print string

	def parse(self):
		self.parseClass()

	"""Parsing Functions"""
	def parseClass(self):
		self.write('<class>')
		token = self.lexer.getNextToken()
		if not self.nextElement(token,'class'):
			print "class not found"
			return
		self.write(token)
		if not self.className():
			print "classNameNotFound"
			return
		token = self.lexer.getNextToken()
		if not self.nextElement(token,'{'):
			print "{ after class Name not found"
			return
		self.write(token)
		if not self.classVarDecStar():
			return 
		if not self.subroutineDecStar():
			return
		token = self.lexer.getNextToken()
		if not self.nextElement(token,'}'):
			print "ending } for class not found"
			return
		self.write(token)
		self.write('</class>')
		self.closeFile()

	def nextElement(self,token, element):
		""" checks to see if next element is correct"""
		if not token: 
			return False
		keyword, ele = self.getTokeninfo(token)
		if(ele == element):
			return True
		return False

	def className(self):
		token = self.lexer.getNextToken()
		if not token:
			return False
		keyword, ele = self.getTokeninfo(token)
		if keyword == 'identifier':
			self.write(token)
			return True
		print "Identifer Not Found"
		return False

	""" Class variable declarations"""
	def classVarDecStar(self):		
		while True:
			token = self.lexer.getNextToken()
			if not self.nextElement(token, 'static') and not self.nextElement(token, 'field'):
				self.returnToken(token)
				return True
			self.write('<classVarDec>')
			self.returnToken(token)
			if not self.classVarDec():
				print "Incorrect Variable Declaration"
				return False
			self.write('</classVarDec>')
		return True

	def classVarDec(self):
		token = self.lexer.getNextToken()
		if not self.nextElement(token,'static') and not self.nextElement(token,'field'):
			print "static or field not found"
			return
		self.write(token)
		token = self.lexer.getNextToken()
		if not self.type(token):
			return "Type in variable declaration not valid"
			return False
		self.write(token)
		if not self.varName():
			return "not a correct var name"
			return False
		while True:
			token = self.lexer.getNextToken()
			if not self.nextElement(token,','):
				self.returnToken(token)
				break;
			self.write(token)
			if not self.varName():
				print "incorrect variable name"
				return False
		token = self.lexer.getNextToken()
		if not self.nextElement(token, ';'):
			print "no ';' after variable decloaration"
			return False
		self.write(token)
		return True

	def type(self, token, extra=None):
		if self.nextElement(token, 'int') or self.nextElement(token, 'char') or self.nextElement(token, 'boolean'):
			return True
		else:
			key, name = self.getTokeninfo(token)
			if key == 'identifier':
				return True
			else:
				if not extra == None:
					if self.nextElement(token, extra):
						return True
		return False

	def varName(self):
		token = self.lexer.getNextToken()
		key, name = self.getTokeninfo(token)
		if not key == 'identifier':
			print "inValid Variable Name"
			return False
		self.write(token)
		return True

	""" SubRoutines """
	def subroutineDecStar(self):
		while True:
			token = self.lexer.getNextToken()
			if not self.nextElement(token, 'constructor') and not self.nextElement(token, 'function') and not self.nextElement(token, 'method'):
				self.returnToken(token)
				return True
			self.returnToken(token)
			self.write('<subroutineDec>')
			if not self.subroutineDec():
				print "Incorrect subroutine Declaration"
				return False
			self.write('</subroutineDec>')
		return True

	def subroutineDec(self):
		token = self.lexer.getNextToken()
		if not self.nextElement(token, 'constructor') and not self.nextElement(token, 'function') and not self.nextElement(token, 'method'):
			print "Not a valid subroutine keyword"
			return False
		self.write(token)
		token = self.lexer.getNextToken()
		if not self.type(token, 'void'):
			print "Not a vilid type for subroutine"
			return False
		self.write(token)
		if not self.varName():
			print "not a vaild subroutine Name"
			return False
		token = self.lexer.getNextToken()
		if not self.nextElement(token, '('):
			print "Missing '(' in function"
			return False
		self.write(token)
		if not self.parameterListStar():
			print "Incorrect paramator List"
			return False
		token = self.lexer.getNextToken()
		if not self.nextElement(token, ')'):
			print "Missing ending ')' for subroutine"
			return False
		self.write(token)
		if not self.subroutineBody():
			print "Body of subroutine is not correct"
			return False
		return True

	def parameterListStar(self):
		self.write('<parameterList>')
		""" one paramter """
		token = self.lexer.getNextToken()
		if self.nextElement(token, ')'):
			""" No parameters"""
			self.returnToken(token)
			self.write('</parameterList>')
			return True
		if not self.type(token):
			self.returnToken(token)
			return True
		self.write(token)
		token = self.lexer.getNextToken()
		key, name = self.getTokeninfo(token)
		if not key == 'identifier':
			print "incorrect identifier"
			return False
		self.write(token)
		""" multiple Parameters"""
		while True:
			token = self.lexer.getNextToken()
			if not self.nextElement(token, ','):
				self.returnToken(token)
				break
			self.returnToken(token)
			self.extraParameters()
		self.write('</parameterList>')
		return True

	def extraParameters(self):
		token = self.lexer.getNextToken()
		if not self.nextElement(token, ','):
			print "no comma"
			return False
		self.write(token)
		token = self.lexer.getNextToken()
		if not self.type(token):
			print "incorrect var Name"
			return False
		self.write(token)
		token = self.lexer.getNextToken()
		key, name = self.getTokeninfo(token)
		if not key == 'identifier':
			print 'incorrect identifier'
			return False
		self.write(token)
		return True

	def subroutineBody(self):
		self.write('<subroutineBody>')
		token = self.lexer.getNextToken()
		if not self.nextElement(token, '{'):
			print "no { before function"
			return False
		self.write(token)
		if not self.varDecStar():
			print "incorrect variable statments"
			return False
		if not self.statements():
			print "incorrect Statemnts"
			return False
		token = self.lexer.getNextToken()
		if not self.nextElement(token, '}'):
			print "Founc on '}' after function"
			return False
		self.write(token)
		self.write('</subroutineBody>')
		return True

	def varDecStar(self):
		while True:
			token = self.lexer.getNextToken()
			if not self.nextElement(token, 'var'):
				self.returnToken(token)
				return True
			self.returnToken(token)
			if not self.varDec():
				print "incorrect declaration of variables"
				return False

	def varDec(self):
		self.write('<varDec>')
		token = self.lexer.getNextToken()
		if not self.nextElement(token, 'var'):
			print "incorrect startig statemnt"
			return False
		self.write(token)
		token = self.lexer.getNextToken()
		if not self.type(token):
			print "incorrect type"
			return False
		self.write(token)
		token = self.lexer.getNextToken()
		key, name = self.getTokeninfo(token)
		if not key == 'identifier':
			print "incorrect Variable Name"
			return False
		self.write(token)
		while True:
			token = self.lexer.getNextToken()
			if not self.nextElement(token, ','):
				self.returnToken(token)
				break
			self.write(token)
			token = self.lexer.getNextToken()
			key, name = self.getTokeninfo(token)
			if not key == 'identifier':
				print "incorrect identifier"
				return False
			self.write(token)

		token = self.lexer.getNextToken()
		if not self.nextElement(token, ';'):
			print "No ';' at the end of variable declaration"
			return False
		self.write(token)
		self.write('</varDec>')
		return True

	""" Statements for the subroutine Body"""
	def statements(self):
		"""
		There are 5 different kinds of statements
		let, if, while, do, and return
		"""
		self.write('<statements>')
		while True:
			token = self.lexer.getNextToken()
			if self.nextElement(token, 'let'):
				self.returnToken(token)
				self.write('<letStatement>')
				if not self.letStatement():
					print "let statement not correct"
					return False
				self.write('</letStatement>')
			elif self.nextElement(token, 'if'):
				self.returnToken(token)
				self.write('<ifStatement>')
				if not self.ifStatement():
					print "if Statement is not Correct"
					return False
				self.write('</ifStatement>')
			elif self.nextElement(token, 'while'):
				self.returnToken(token)
				self.write('<whileStatement>')
				if not self.whileStatement():
					print "while statement not correct"
					return False
				self.write('</whileStatement>')
			elif self.nextElement(token, 'do'):
				self.returnToken(token)
				self.write('<doStatement>')
				if not self.doStatement():
					print "do statement not correct"
					return False
				self.write('</doStatement>')
			elif self.nextElement(token, 'return'):
				self.returnToken(token)
				self.write('<returnStatement>')
				if not self.returnStatement():
					print "return statement not correct"
					return False
				self.write('</returnStatement>')
			else:
				self.returnToken(token)
				""" no more statements"""
				break
		self.write('</statements>')
		return True

	""" Statement Types"""
	def letStatement(self):
		token = self.lexer.getNextToken()
		if not self.nextElement(token, 'let'):
			return False
		self.write(token)
		token = self.lexer.getNextToken()
		key, name = self.getTokeninfo(token)
		if not key == 'identifier':
			print "Variable name not an identifier"
			return False
		self.write(token)

		token = self.lexer.getNextToken()
		if self.nextElement(token, '['):
			self.write(token)
			self.expression()
			token = self.lexer.getNextToken()
			if not self.nextElement(token, ']'):
				print "expected ']'"
				return False
			self.write(token)
		else:
			self.returnToken(token)
		
		token = self.lexer.getNextToken()
		if not self.nextElement(token, '='):
			print "no '=' in statement"
			return False
		self.write(token)

		if not self.expression():
			print "incorrect expression"
			return False

		token = self.lexer.getNextToken()
		if not self.nextElement(token, ';'):
			print "no ';' found"
			return False
		self.write(token)
		return True


	def ifStatement(self):
		token = self.lexer.getNextToken()
		if not self.nextElement(token, 'if'):
			return False
		self.write(token)

		token = self.lexer.getNextToken()
		if not self.nextElement(token, '('):
			print "no '(' Found"
			return False
		self.write(token)

		if not self.expression():
			print "incorrect expression"
			return False

		token = self.lexer.getNextToken()
		if not self.nextElement(token, ')'):
			print "No ')' found"
			return False
		self.write(token)

		token = self.lexer.getNextToken()
		if not self.nextElement(token, '{'):
			print "No '{' found"
			return False
		self.write(token)

		if not self.statements():
			return False

		token = self.lexer.getNextToken()
		if not self.nextElement(token, '}'):
			print "No '}' found"
			return False
		self.write(token)

		token = self.lexer.getNextToken()

		if not self.nextElement(token, 'else'):
			self.returnToken(token)
			return True
		
		self.write(token)

		token = self.lexer.getNextToken()
		if not self.nextElement(token, '{'):
			print "no '{' after else"
			return False
		self.write(token)

		if not self.statements():
			return False

		token = self.getNextToken()
		if not self.nextElement(token, '}'):
			print "ending '}' in else not found"
			return False
		self.write(token)
		return True


	def whileStatement(self):
		token = self.lexer.getNextToken()
		if not self.nextElement(token, 'while'):
			return False
		self.write(token)

		token = self.lexer.getNextToken()
		if not self.nextElement(token, '('):
			print "no ( found in whle statement"
			return False
		self.write(token)

		if not self.expression():
			return False

		token = self.lexer.getNextToken()
		if not self.nextElement(token, ')'):
			print "no ')' in while statement"
			return False
		self.write(token)

		token = self.lexer.getNextToken()
		if not self.nextElement(token, '{'):
			print "no '{' found after while"
			return False
		self.write(token)

		if not self.statements():
			return False

		token = self.lexer.getNextToken()
		if not self.nextElement(token, '}'):
			print "no '}' found at then of while"
			return False
		self.write(token)
		return True

	def doStatement(self):
		token = self.lexer.getNextToken()
		if not self.nextElement(token, 'do'):
			return False
		self.write(token)

		if not self.subroutineCall():
			return False

		token = self.lexer.getNextToken()
		if not self.nextElement(token, ';'):
			print "no ';' found at end of do"
			return False
		self.write(token)
		return True

	def returnStatement(self):
		token = self.lexer.getNextToken()
		if not self.nextElement(token, 'return'):
			return False
		self.write(token)

		token = self.lexer.getNextToken()
		if self.nextElement(token, ';'):
			self.write(token)
			return True
		self.returnToken(token)

		if not self.expression():
			return False

		token = self.lexer.getNextToken()
		if not self.nextElement(token, ';'):
			print "no ';' found at the end of return"
			return False
		self.write(token)
		return True

	def expression(self):
		self.write('<expression>')
		if not self.term():
			print 'no term'
			return False

		while True:
			token = self.lexer.getNextToken()
			if not self.isOp(token):
				self.returnToken(token)
				break
			self.write(token)
			if not self.term():
				print "invalid term"
				return False
		self.write('</expression>')
		return True

	def term(self):
		self.write('<term>')
		token = self.lexer.getNextToken()
		if self.isIntegerConstant(token):
			self.write(token)
		elif self.isStringConstant(token):
			self.write(token)
		elif self.isKeywordConstant(token):
			self.write(token)
		elif self.isUnaryOp(token):
			self.write(token)
			if not self.term():
				return False
		elif self.nextElement(token, '('):
			self.write(token)
			if not self.expression():
				return False
			token = self.lexer.getNextToken()
			if not self.nextElement(token, ')'):
				return False
			self.write(token)
		elif self.isIdentifier(token):
			""" identifier"""
			identifierToken = token
			token = self.lexer.getNextToken()
			if self.nextElement(token, '['):
				self.write(identifierToken)
				self.write(token)
				if not self.expression():
					return False
				token = self.lexer.getNextToken()
				if not self.nextElement(token, ']'):
					return False
				self.write(token)
			elif self.nextElement(token, '.') or self.nextElement(token, '('):
				self.returnToken(token)
				self.returnToken(identifierToken)
				if not self.subroutineCall():
					return False
			else:
				self.returnToken(token)
				self.write(identifierToken) # When only a varName
		else:
			return False
		self.write('</term>')
		return True

	def subroutineCall(self):
		token = self.lexer.getNextToken()
		if not self.isIdentifier(token):
			print "var in subroutine failed"
			return False
		self.write(token)

		token = self.lexer.getNextToken()
		if self.nextElement(token, '('):
			self.write(token)
			if not self.expressionList():
				return False
			token = self.lexer.getNextToken()
			if not self.nextElement(token, ')'):
				print "no ')' found at end of subroutine"
				return False
			self.write(token)
		elif self.nextElement(token, '.'):
			self.write(token)
			token = self.lexer.getNextToken()
			if not self.isIdentifier(token):
				print "incorrect identifier in subroutine"
				return False
			self.write(token)

			token = self.lexer.getNextToken()
			if not self.nextElement(token, '('):
				print "no '('' found in subroutineCall"
				return False
			self.write(token)

			if not self.expressionList():
				print "incorrect expressionList in subroutine"
				return False

			token = self.lexer.getNextToken()
			if not self.nextElement(token, ')'):
				print "no ending '(' found in subroutine"
				return False
			self.write(token)
		return True

	def expressionList(self):
		self.write('<expressionList>')
		token = self.lexer.getNextToken()
		if self.nextElement(token, ')'):
			self.returnToken(token)
		else:
			self.returnToken(token)
			if not self.expression():
				return False

			while True:
				token = self.lexer.getNextToken()
				if not self.nextElement(token, ','):
					self.returnToken(token)
					break
				self.write(token)
				if not self.expression():
					return False
		self.write('</expressionList>')
		return True

	def isOp(self, token):
		opList = ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']
		for op in opList:
			if self.nextElement(token, op):
				return True
		return False

	def isUnaryOp(self, token):
		opList = ['-', '~']
		for op in opList:
			if self.nextElement(token, op):
				return True
		return False
	
	def isKeywordConstant(self, token):
		keyList = ['true', 'false', 'null', 'this']
		for key in keyList:
			if self.nextElement(token, key):
				return True
		return False

	def isIntegerConstant(self, token):
		key, name = self.getTokeninfo(token)
		if key == 'integerConstant':
			return True
		return False

	def isStringConstant(self, token):
		key, name = self.getTokeninfo(token)
		if key == 'stringConstant':
			return True
		return False

	def isIdentifier(self, token):
		key, name = self.getTokeninfo(token)
		if key == 'identifier':
			return True
		return False

def main():
	p = Parser("Test/Square.jack")
	p.parse()

if __name__ == '__main__':
	main()
