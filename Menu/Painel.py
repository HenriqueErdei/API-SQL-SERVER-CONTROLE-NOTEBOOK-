import pyodbc
import random
import string

# Função para conectar ao banco de dados
def conectar_bd():
    dados_conexao = (
        "Driver={SQL Server};"
        "Server=FTPSPNBAL43;"
        "Database=INVENTARIO_PERIFERICOS;"
    )
    return pyodbc.connect(dados_conexao)

# Função para registrar um usuário
def cadastrar_usuario():
    conexao = conectar_bd()
    cursor = conexao.cursor()

    print("Cadastro de Usuário:")
    Usuario = input("Qual é o nome do usuário? ")
    Setor = input("Qual é o setor? ")
    Modelo = input("Qual é o modelo? ")
    data_entrada = input("Qual é a data de entrada? (formato: YYYY-MM-DD) ")

    # Gerar código único
    Codigo = gerar_codigo_unico(cursor)

    # Preencher no DB
    comando = """INSERT INTO NOTEBOOK(Usuario, Setor, Modelo, Codigo, data_entrada)
    VALUES (?, ?, ?, ?, ?)"""
    cursor.execute(comando, (Usuario, Setor, Modelo, Codigo, data_entrada))
    conexao.commit()

    # Mensagem de sucesso
    print("Usuário cadastrado no sistema com sucesso!")
    print("Código do usuário:", Codigo)

    conexao.close()

# Função para visualizar usuário por código
def visualizar_por_codigo():
    conexao = conectar_bd()
    cursor = conexao.cursor()

    print("Visualização de Usuário por Código:")
    codigo = input("Digite o código da máquina: ")
    comando = "SELECT * FROM NOTEBOOK WHERE Codigo = ?"
    cursor.execute(comando, (codigo,))
    resultado = cursor.fetchone()
    if resultado:
        print("Usuário encontrado:")
        print("Nome do usuário:", resultado.Usuario)
        print("Setor:", resultado.Setor)
        print("Modelo:", resultado.Modelo)
        print("Código:", resultado.Codigo)
        print("Data de Entrada:", resultado.data_entrada)
    else:
        print("Nenhum usuário encontrado para o código informado.")

    conexao.close()

# Função para visualizar usuário por nome
def visualizar_por_nome():
    conexao = conectar_bd()
    cursor = conexao.cursor()

    print("Visualização de Usuário por Nome:")
    nome = input("Digite o nome do usuário: ")
    comando = "SELECT * FROM NOTEBOOK WHERE Usuario = ?"
    cursor.execute(comando, (nome,))
    resultado = cursor.fetchall()
    if resultado:
        print("Usuários encontrados:")
        for usuario in resultado:
            print("Nome do usuário:", usuario.Usuario)
            print("Setor:", usuario.Setor)
            print("Modelo:", usuario.Modelo)
            print("Código:", usuario.Codigo)
            print("Data de Entrada:", usuario.data_entrada)
    else:
        print("Nenhum usuário encontrado para o nome informado.")

    conexao.close()

# Função para retornar máquina
def retornar_maquina():
    conexao = conectar_bd()
    cursor = conexao.cursor()

    print("Retorno de Máquina:")
    Codigo = input("Qual é o código do Usuario? ")

    # Consultar o banco de dados
    comando_consulta = f"SELECT * FROM NOTEBOOK WHERE Codigo = ?"
    cursor.execute(comando_consulta, (Codigo,))
    resultado = cursor.fetchone()

    # Verificar se a máquina existe no banco de dados
    if resultado:
        data_devolucao = input("Qual é a data de devolução? (formato: YYYY-MM-DD) ")

        # Preencher no DB
        comando = f"""UPDATE NOTEBOOK SET data_devolucao = ? WHERE Codigo = ?"""
        cursor.execute(comando, (data_devolucao, Codigo))
        conexao.commit()
        
        # Mensagem de sucesso
        print("Devolução registrada com sucesso no sistema!")
    else:
        # Mensagem de erro
        print("Erro: Usuario não encontrado no banco de dados.")

    conexao.close()

# Função para gerar código de 6 dígitos único
def gerar_codigo_unico(cursor):
    while True:
        codigo = ''.join(random.choices(string.digits, k=6))
        comando = "SELECT COUNT(*) FROM NOTEBOOK WHERE Codigo = ?"
        cursor.execute(comando, (codigo,))
        if cursor.fetchone()[0] == 0:
            return codigo

# Função principal
def menu_principal():
    print("Menu Principal:")
    print("1. Cadastrar Usuário")
    print("2. Visualizar Usuário por Código")
    print("3. Visualizar Usuário por Nome")
    print("4. Devolução Notebook")
    print("5. Sair")

def main():
    while True:
        menu_principal()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            visualizar_por_codigo()
        elif opcao == "3":
            visualizar_por_nome()
        elif opcao == "4":
            retornar_maquina()
        elif opcao == "5":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida. Por favor, escolha uma das opções listadas.")

if __name__ == "__main__":
    main()
