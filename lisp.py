import operator as op

# Define aliases para tipos utilizados no programa
Symbol = str
Number = (int, float)
List = list

def tokenize(chars):
    """
    Converte uma string de código Lisp em uma lista de tokens.

    Substitui os parênteses por espaços para garantir que
    eles sejam tratados separadamente e divide a string em tokens.

    Args:
        chars (str): A string de código Lisp a ser tokenizada.

    Returns:
        list: Lista de tokens obtida a partir da string de entrada.
    """
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(program):
    """
    Converte uma string de código Lisp em uma estrutura de dados (listas e símbolos).

    Chama a função `read_from_tokens` para interpretar os tokens gerados pela função `tokenize`.

    Args:
        program (str): A string de código Lisp a ser interpretada.

    Returns:
        list: A estrutura de dados representando o programa Lisp.
    """
    return read_from_tokens(tokenize(program))

def read_from_tokens(tokens):
    """
    Lê tokens e converte em estruturas de dados Lisp.

    Esta função analisa os tokens para construir a lista de expressões de Lisp.
    Se encontrar um '(', cria uma nova lista. Se encontrar um número ou símbolo,
    retorna o valor correspondente.

    Args:
        tokens (list): A lista de tokens a ser lida.

    Returns:
        object: Uma lista de expressões ou um símbolo/valor (se o token for uma constante).
    
    Raises:
        SyntaxError: Se o programa Lisp não estiver bem formado.
    """
    if len(tokens) == 0:
        raise SyntaxError('Unexpected EOF')  # Erro quando o fim do programa é alcançado inesperadamente
    token = tokens.pop(0)  # Obtém o primeiro token

    if token == '(':
        # Se encontrar '(', inicia uma nova lista
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  # descarta o ')'
        return L
    elif token == ')':
        raise SyntaxError('Unexpected )')  # Erro caso se depare com um ')' inesperado
    else:
        return atom(token)  # Caso contrário, processa o token como um átomo (número ou símbolo)

def atom(token):
    """
    Converte um token em seu tipo correspondente (número ou símbolo).

    Tenta converter o token em um número (inteiro ou flutuante). Caso falhe, retorna o token como um símbolo.

    Args:
        token (str): O token a ser convertido.

    Returns:
        int, float ou Symbol: O valor convertido ou o símbolo.
    """
    try:
        return int(token)  # Tenta converter para inteiro
    except ValueError:
        try:
            return float(token)  # Tenta converter para flutuante
        except ValueError:
            return Symbol(token)  # Caso contrário, é um símbolo

def standard_env():
    """
    Cria e retorna o ambiente padrão, com as operações aritméticas e comparações básicas.

    O ambiente padrão inclui operadores matemáticos e comparações, como +, -, *, /, >, <, etc.

    Returns:
        dict: O ambiente padrão com operadores e funções.
    """
    env = {}
    env.update({
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.truediv,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le,
        '=': op.eq,
    })
    return env

# Cria o ambiente global com as funções e operadores padrão
global_env = standard_env()

def evaluate(x, env=global_env):
    """
    Avalia uma expressão Lisp no ambiente dado.

    A função processa uma expressão Lisp, verificando se é um símbolo, uma lista ou uma expressão especial
    (como `if` ou `define`), e realiza a avaliação recursivamente.

    Args:
        x (object): A expressão Lisp a ser avaliada.
        env (dict): O ambiente onde a avaliação será realizada.

    Returns:
        object: O valor resultante da avaliação da expressão.
    """
    if isinstance(x, Symbol):      
        return env[x]  # Retorna o valor associado ao símbolo no ambiente
    elif not isinstance(x, List):
        return x  # Se não for uma lista, é um valor atômico (número ou símbolo)

    if x[0] == 'if':               
        # Avalia uma expressão condicional (if)
        (_, test, conseq, alt) = x
        exp = conseq if evaluate(test, env) else alt
        return evaluate(exp, env)
    elif x[0] == 'def':         
        # Define uma nova variável ou função no ambiente
        (_, var, exp) = x
        env[var] = evaluate(exp, env)
    else:                          
        # Caso seja uma chamada de função, avalia o operador e os argumentos
        proc = evaluate(x[0], env)
        args = [evaluate(exp, env) for exp in x[1:]]
        return proc(*args)

def repl():
    """
    Função principal do interpretador. Executa um loop onde o usuário pode inserir expressões Lisp.

    O REPL permite ao usuário digitar expressões Lisp e obter resultados imediatamente,
    e pode ser encerrado digitando 'exit' ou 'quit'.
    """
    while True:
        try:
            program = input("Digite sua expressão Lisp: ")
            if program.lower() in ['exit', 'quit']:
                break
            result = evaluate(parse(program))
            print("Resultado:", result)
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == '__main__':
    """
    Função de inicialização do programa. Inicia o REPL e exibe uma mensagem de boas-vindas.
    """
    print("Bem-vindo ao interpretador Lisp")
    print("Digite 'exit' ou 'quit' para sair.")
    repl()

