import pyodbc

class BancoDeDados:
    def __init__(self, servidor, banco):
        self.servidor = servidor
        self.banco = banco

    def conectar(self):
        try:
            self.conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={self.servidor};DATABASE={self.banco}')
            print("Conexão com o banco de dados estabelecida.")
        except pyodbc.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def desconectar(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
            print("Conexão com o banco de dados encerrada.")

banco_de_dados = BancoDeDados(servidor="FTPSPNBAL43", banco="INVENTARIO_PERIFERICOS")
banco_de_dados.conectar()
