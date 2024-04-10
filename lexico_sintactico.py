from flask import Flask, request, jsonify, render_template
import ply.lex as lex
import ply.yacc as yacc

app = Flask(__name__, template_folder='templates')

# Tokens y definiciones del analizador léxico y sintáctico
tokens = (
    'ID', 'LPAREN', 'RPAREN', 'COLON', 'STRING', 'LBRACE', 'RBRACE', 'FUN', 'PRINTLN',
)

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_FUN = r'fun'
t_PRINTLN = r'println'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = 'ID' if t.value not in ('fun', 'println') else t.value.upper()
    return t

def t_STRING(t):
    r'\"[^\"]*\"'
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def p_program(p):
    '''program : FUN ID LPAREN ID COLON STRING RPAREN LBRACE PRINTLN LPAREN STRING RPAREN RBRACE'''
    p[0] = {'function_name': p[2], 'parameter_name': p[4], 'string_value': p[11][1:-1], 'print_string': p[11][1:-1]}

def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()

# Rutas para la aplicación

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse_code():
    code = request.form['code']
    lexer.input(code)
    parsed = parser.parse(lexer=lexer)
    return jsonify(parsed)

@app.route('/hello')
def hello():
    return "¡Hola! Esta es la página de inicio de mi aplicación."

@app.route('/parse_simple', methods=['POST'])
def parse_simple_code():
    code = request.form['code']
    # Tu lógica de análisis de código aquí...
    parsed_code = f"El código analizado es: {code}"
    return jsonify({'parsed_code': parsed_code})

if __name__ == '__main__':
    app.run(debug=True)
