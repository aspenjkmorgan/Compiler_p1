import sys
from Tokenizer2 import Tokenizer

class CompileEngine:
    def __init__(self, T):
        self.T = T  # T is Tokenizer instance
    
    def printXMLToken(self):
        toke = self.T.token()
        type = self.T.tokenType()
        print('<' + type + '> ' + toke + ' </' + type + '>')


    def checkToken(self, tokens):
        if self.T.token() in tokens:
            self.printXMLToken()
            self.T.advance()
        else:
            sys.exit('Error in grammar.')
            

    def checkType(self, expected_types):
       if self.T.tokenType() in expected_types:
           self.printXMLToken()
           self.T.advance()
       else:
          sys.exit('Error in grammar.') 

####################################################################
    def compileClass(self):
        """
        Compiles <class> :=
            'class' <class-name> '{' <class-var-dec>* <subroutine-dec>* '}'

        The tokenizer is expected to be positionsed at the beginning of the
        file.
        """
        print("<class>")
        self.checkToken(('class',))
       
        self.checkType(('identifier',))
        
        self.checkToken(('{',))
        
        while(self.T.token() in ('static', 'field')):
            self.compileClassVarDec()
        
        while(self.T.token() in ('constructor', 'function', 'method')):
            self.compileSubroutine()
        
        self.checkToken(('}',))
        print("</class>")


    def compileClassVarDec(self):
        """
        Compiles <class-var-dec> :=
            ('static' | 'field') <type> <var-name> (',' <var-name>)* ';'
        """
        print("<classVarDec>")
        self.checkToken(('static', 'field'))
        
        if self.T.token() in ('int', 'char', 'boolean'):
            self.checkToken(('int', 'char', 'boolean'))
        else:
            self.checkType(('identifier',))
        
        self.checkType(('identifier',))
        
        while self.T.token() == ',':
            self.checkToken((',',))
            self.checkType(('identifier',))
        
        self.checkToken((';',))
        print("</classVarDec>")


    def compileSubroutine(self):
        """
        Compiles <subroutine-dec> :=
            ('constructor' | 'function' | 'method') ('void' | <type>)
            <subroutine-name> '(' <parameter-list> ')' <subroutine-body>

        ENTRY: Tokenizer positioned on the initial keyword.
        EXIT:  Tokenizer positioned after <subroutine-body>.
        """
        print("<subroutineDec>")
        self.checkToken(('constructor', 'function', 'method'))
        
        if self.T.token() in (('void', 'char', 'int', 'boolean')):
            self.checkToken(('void', 'char', 'int', 'boolean'))
        else:
            self.checkType(('identifier',))

        self.checkType('identifier')

        self.checkToken(('(',))

        self.compileParameterList()

        self.checkToken((')',))
        
        self.compileSubroutineBody()
        print("</subroutineDec>")


    def compileParameterList(self):
        """
        Compiles <parameter-list> :=
            ( <type> <var-name> (',' <type> <var-name>)* )?

        ENTRY: Tokenizer positioned on the initial keyword.
        EXIT:  Tokenizer positioned after <subroutine-body>.
        """
        keys = ('this', 'true', 'false', 'null')

        print("<parameterList>")
        if self.T.token() in ('int', 'boolean', 'char'):
            self.checkToken(('int', 'boolean', 'char'))
            self.checkType(('identifier',))
        elif self.T.token() not in (')'):
            self.checkType(('identifier',))
            self.checkType(('identifier',))
        
        while self.T.token() == ',':
            self.checkToken((',',))
            if self.T.token() in ('int', 'boolean', 'char'):
                self.checkToken(('int', 'boolean', 'char'))
            else:
                self.checkType(('identifier',))
            
            self.checkType(('identifier',))
        
        print("</parameterList>")


    def compileSubroutineBody(self):
        """
        Compiles <subroutine-body> :=
            '{' <var-dec>* <statements> '}'
        """
        print("<subroutineBody>")
        self.checkToken(('{'))
        
        while self.T.token() == 'var':
            self.compileVarDec()
        
        self.compileStatements()
        
        self.checkToken(('}',))
        print("</subroutineBody>")


    def compileVarDec(self):
        """
        Compiles <var-dec> :=
            'var' <type> <var-name> (',' <var-name>)* ';'
        """
        print("<varDec>")
        self.checkToken(('var',))
       
        if self.T.token() in ('int', 'char', 'boolean'):
            self.checkToken(('int', 'char', 'boolean'))
        else:
            self.checkType(('identifier',))
        
        self.checkType(('identifier',))
        
        while self.T.token() == ',':
            self.checkToken((',',))
            self.checkType(('identifier',))
        
        self.checkToken((';',))
        print("</varDec>")


    def compileStatements(self):
        """
        Compiles <statements> := (<let-statement> | <if-statement> |
            <while-statement> | <do-statement> | <return-statement>)*
        """
        print("<statements>")
        while self.T.token() in ('let', 'if', 'while', 'do', 'return'):
            toke = self.T.token()
            if toke == 'let':
                self.compileLet()
            elif toke == 'if':
                self.compileIf()
            elif toke == 'while':
                self.compileWhile()
            elif toke == 'do':
                self.compileDo()
            else:
                self.compileReturn()
        print("</statements>")


    def compileLet(self):
        """
        Compiles <let-statement> :=
            'let' <var-name> ('[' <expression> ']')? '=' <expression> ';'
        """
        print("<letStatement>")
        self.checkToken(('let',))
        
        self.checkType(('identifier',))
        
        if self.T.token() == '[':
            self.checkToken(('[',))
            self.compileExpression()
            self.checkToken((']',))

        self.checkToken(('=',))
        
        self.compileExpression()
        
        self.checkToken((';',))
        print("</letStatement>")


    def compileIf(self):
        """
        Compiles <if-statement> :=
            'if' '(' <expression> ')' '{' <statements> '}' ( 'else'
            '{' <statements> '}' )?
        """
        print("<ifStatement>")
        self.checkToken(('if',)) 
        
        self.checkToken(('(',))
        self.compileExpression()
        self.checkToken((')',))
        
        self.checkToken(('{',))
        self.compileStatements() 
        self.checkToken(('}',))

        if self.T.token() == 'else':
            self.checkToken(('else',))
            self.checkToken(('{',))
            self.compileStatements()
            self.checkToken(('}'))
        print("</ifStatement>")


    def compileWhile(self):
        """
        Compiles <while-statement> :=
        'while' '(' <expression> ')' '{' <statements> '}'
        """
        print("<whileStatement>")
        self.checkToken(('while',))
        
        self.checkToken(('(',))
        self.compileExpression()
        self.checkToken((')',))
        
        self.checkToken(('{',))
        self.compileStatements()
        self.checkToken(('}',))
        print("</whileStatement>")


    def compileDo(self):
        """
        Compiles <do-statement> := 'do' <subroutine-call> ';'

        <subroutine-call> := (<subroutine-name> '(' <expression-list> ')') |
            ((<class-name> | <var-name>) '.' <subroutine-name> '('
            <expression-list> ')')

        <*-name> := <identifier>
        """
        print("<doStatement>")
        self.checkToken(('do',))
        self.compileSubroutineCall()
        self.checkToken((';',))
        print("</doStatement>")


    def compileReturn(self):
        """
        Compiles <return-statement> :=
            'return' <expression>? ';'
        """
        print("<returnStatement>")
        self.checkToken(('return',))
        
        if self.T.token() not in ((';',)):
            self.compileExpression()
        
        self.checkToken((';',))
        print("</returnStatement>")

    def compileSubroutineCall(self):
        """
        subroutineName'('expressionList')' |
        (className|varName)'.'subroutineName'('expressionList')'
        """
        self.checkType(('identifier',))

        if self.T.token() == '.':
            self.checkToken(('.',))
            self.checkType(('identifier',))
        
        self.checkToken(('(',))
        self.compileExpressionList()
        self.checkToken((')',))



# The following are not LL(1) and are not part of the initial assignment
    def compileExpression(self):
        """
        Compiles <expression> :=
            <term> (op <term>)*
        """
        print("<expression>")
        self.compileTerm()
        while self.T.token() in ('+', '-', '*', '/', '%', '&amp;', '|', '&lt;', '&gt;', '='):
            self.checkToken(('+', '-', '*', '/', '%', '&amp;', '|', '&lt;', '&gt;', '='))
            self.compileTerm()
        print("</expression>")

    def compileExpressionList(self):
        """
        Compiles <expression-list> :=
            (<expression> (',' <expression>)* )?
        """
 
        print("<expressionList>")
        while self.T.token() != ')':
            if self.T.token() == ',':
                self.checkToken(',')
            else:
                self.compileExpression()
        print("</expressionList>")

    def compileTerm(self):
        """
        Compiles a <term> :=
            <int-const> | <string-const> | <keyword-const> | <var-name> |
            (<var-name> '[' <expression> ']') | <subroutine-call> |
            ( '(' <expression> ')' ) | (<unary-op> <term>)
        """
        print("<term>")
        # self.printXMLToken()
        # self.T.advance()

        cType = self.T.tokenType()
        cToken = self.T.token()

        if cType == 'integerConstant':
            self.checkType(('integerConstant',))
        
        elif cType == 'stringConstant':
            self.checkType(('stringConstant',))

        elif cToken in ('true', 'false', 'null', 'this'):
            self.checkToken(('true', 'false', 'null', 'this'))

        elif cToken in ('~', '-'):
            self.checkToken(('~', '-'))
            self.compileTerm()

        elif cToken in ('(',):
            self.checkToken(('(',))
            self.compileExpression()
            self.checkToken((')',))

        else:
            if self.T.getNext() == '[':
                self.checkType(('identifier',))
                self.checkToken('[')
                self.compileExpression()
                self.checkToken((']',))

            elif self.T.getNext() not in ('(', '.'):
                self.checkType(('identifier',))

            else:
                self.compileSubroutineCall()
                
        print("</term>")

def main():
    input = sys.argv[1]
    file = open(input, 'r') 
    test = CompileEngine(Tokenizer(file))

    # write to .xml file
    sys.stdout = open(input.split('.')[0] + '.xml', 'wt')
    test.compileClass()
    

if __name__ == "__main__":
    main()