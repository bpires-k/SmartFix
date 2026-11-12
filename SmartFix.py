# IMPORTAÇÕES DE MODULOS NECESSÁRIOS E DEFINIÇÃO DE VARIÁVEIS GLOBAIS
import datetime
import os
import sqlite3
import platform

#colocar keyboard a funcionar para fazer funcao de carregar no enter para voltar ao menu
# --- CRIAÇÃO AUTOMÁTICA DO FICHEIRO DE LOGS ---
if not os.path.exists("log_erros.txt"):
    with open("log_erros.txt", "w", encoding="utf-8") as l:
        data_inicio = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        l.write(f"[{data_inicio}] SISTEMA: Ficheiro de logs criado e sistema iniciado.\n")

basedados = "BDSmartFix2.db"
dt = datetime.datetime.now()

def limpar_cmd(): 
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# FUNÇÕES AUXILIARES
# Função para aguardar que o utilizador pressione a tecla 'q' para voltar ao menu inicial
def ispressed():
    print("\nPressione q e Enter para voltar ao Menu Inicial")
    while True:
        tecla = input().strip().lower()
        if tecla == "q":
            break
# Função para registar logs de erros em ficheiro
def registar_log(mensagem):
    try:
        with open("log_erros.txt", "a", encoding="utf-8") as ficheiro:
            data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ficheiro.write(f"[{data_atual}] ERRO: {mensagem}\n")
    except Exception as erro:
        print(f"Não foi possível gravar o log: {erro}")
# Função para cancelar o processo de registo        
def cancelar_processo(tipo_registo, pk):
    if pk == '-':
        print("Cancelado com Sucesso")
        registar_log(f"{tipo_registo} - Processo cancelado")
        return True

# VALIDAÇÕES DE INPUTS
#validacao do NIF, devendo ser composto por 9 dígitos.
def validar_nif(tipo_registo):
    while True:
        nif = input("Introduza o NIF (- para cancelar): ")
        if cancelar_processo(tipo_registo, nif):
            return None
        try:
            if len(nif) != 9:
                raise ValueError("O NIF deve ter exatamente 9 dígitos.")
            nif = int(nif)
            return nif
        except ValueError as e:
            print(f"-> Erro no NIF: {e}")
            registar_log(f"{tipo_registo} - NIF inválido ({nif}): {e}") 

#validacao de string só com letras
def validar_str(tipo_str, tipo_registo, pk):
    while True:
        str = input(f"Indique {tipo_str} (- para cancelar): ")
        if cancelar_processo(tipo_registo, str):
            return None
        if cancelar_processo(tipo_registo, str):
            menu()
        if str.replace(" ", "").isalpha():
            return str
        else:
            print("-> Erro: Nome inválido, utilizar apenas caracteres alfabéticos e espaços")
            registar_log(f"{tipo_registo} - texto inválido (chave primária: {pk}: {str})")

#validacao data introduzida no formato pretendido
def validar_data(tipo_data, tipo_registo, pk):
    while True:
        i = 0
        data = input(f"Introduza {tipo_data} (DD-MM-AAAA) (- para cancelar): ")
        if cancelar_processo(tipo_registo, data):
            return None
        partes_data = data.split('-')
        if (len(partes_data) == 3):
            while i < 3:
                if partes_data[i].isdigit():
                    i += 1
                else:
                    print("-> Erro: Data inválida, dígitos não numéricos. Utilize o formato DD-MM-AAAA com digitos numéricos.")
                    registar_log(f"Registo {tipo_registo} - Data inválida (chave primária {pk}): {data}")
                    break
            if len(partes_data[0]) == 2 and len(partes_data[1]) == 2 and len(partes_data[2]) == 4:
                return data
            else:
                print("-> Erro: Data inválida, formato com valores errados. Utilize o formato DD-MM-AAAA com digitos numéricos.")
                registar_log(f"{tipo_registo} - Data inválida (chave primária {pk}): {data}")
        else:
            print("-> Erro: Data inválida. Utilize o formato DD-MM-AAAA com digitos numéricos.")
            registar_log(f"{tipo_registo} - Data inválida (chave primária {pk}): {data}")

def validar_data_fim(tipo_data, tipo_registo, pk):
    while True:
        i = 0
        data = input(f"Introduza {tipo_data} (DD-MM-AAAA) (enter para ignorar, - para cancelar): ")
        if data == "":
            return data
        if cancelar_processo(tipo_registo, data):
            return "-"
        partes_data = data.split('-')
        if (len(partes_data) == 3):
            while i < 3:
                if partes_data[i].isdigit():
                    i += 1
                else:
                    print("-> Erro: Data inválida, dígitos não numéricos. Utilize o formato DD-MM-AAAA com digitos numéricos.")
                    registar_log(f"Registo {tipo_registo} - Data inválida (chave primária {pk}): {data}")
                    break
            if len(partes_data[0]) == 2 and len(partes_data[1]) == 2 and len(partes_data[2]) == 4:
                data = datetime.datetime.strptime(data, "%d-%m-%Y")
                return data
            else:
                print("-> Erro: Data inválida, formato com valores errados. Utilize o formato DD-MM-AAAA com digitos numéricos.")
                registar_log(f"{tipo_registo} - Data inválida (chave primária {pk}): {data}")
        else:
            print("-> Erro: Data inválida. Utilize o formato DD-MM-AAAA com digitos numéricos.")
            registar_log(f"{tipo_registo} - Data inválida (chave primária {pk}): {data}")
            
#validacao o input do sexo 
def validar_sexo(tipo_registo, pk):
    while True:
        sexo = input("Introduza o sexo (M/F) (- para cancelar): ").upper()
        if cancelar_processo(tipo_registo, sexo):
            return None
        if sexo != "M" and sexo != "F":
            print("-> Erro: Sexo inválido, apenas utilize M ou F")
            registar_log(f"{tipo_registo} - Sexo inválido (NIF {pk}: {sexo})")
        else:
            return sexo

#validacao o input de telemovel
def validar_tlm(tipo_registo, pk):
    while True:
        tlm = input ("Introduza o número de telemóvel (- para cancelar): ")
        if cancelar_processo(tipo_registo, tlm):
            return None
        try:
            if len(tlm) != 9:
                raise ValueError("-> Erro: Número de Telemóvel inválido, o número de telemóvel deve ter exatamente 9 dígitos númericos.")
            tlm = int(tlm)
            return tlm
        except ValueError as e:
            print(e)
            registar_log(f"{tipo_registo} - Telemóvel inválido (NIF {pk}: {tlm})")

#validaçao do input do email
def validar_email(tipo_registo, pk):
    while True:
        email = input("Introduza o email (- para cancelar): ")
        if cancelar_processo(tipo_registo, email):
            return None
        if "@" not in email or "." not in email.split("@")[-1]:
            print("-> Erro: Formato de email inválido.")
            registar_log(f"{tipo_registo} - Email inválido (NIF {pk}): {email}")
        else:
            return(email)
        
#validacao de string com letras e numeros        
def validar_printable(tipo_printable, tipo_registo, pk):
    while True:
        printable = input(f"Introduza {tipo_printable} (- para cancelar): ")
        if cancelar_processo(tipo_registo, printable):
            return None
        if printable.isprintable() and printable != "":
            return printable
        else:
            print("-> Erro: Nome inválido, utilizar apenas caracteres alfabéticos e espaços")
            registar_log(f"{tipo_registo} - texto inválido (chave primária: {pk}: {printable})")

#validacao estado do tlm com inputs expecificos
def validar_estado_tlm(tipo_registo, pk):
    while True:
        estado_str = input("ID do Estado do telemóvel (1-novo, 2-semi-novo, 3-usado, - para cancelar): ")
        if cancelar_processo(tipo_registo, estado_str):
            return None
        if estado_str == "1" or estado_str == "2" or estado_str == "3" :
            return int(estado_str)
        else:
            print("-> Erro: O ID do estado deve ser um número entre 1 e 3.")
            registar_log(f" {tipo_registo} - Estado ID não numérico: {pk}: {estado_str}") 

#validacao do id indicado
def validar_id(tipo_registo):
    while True:
        id = input("Introduza o ID que pretende aceder (- para cancelar): ")
        if cancelar_processo(tipo_registo, id):
            return None
        try:
            return(int(id))
        except ValueError:
            print("-> Erro: O ID deve ser um número inteiro válido.")
            registar_log(f"{tipo_registo} - ID inválido: {id}")

#calculo da duracao da reparacao
def calcular_duracao_reparacao(dt_inicio, dt_p_fim, dt_fim, tipo_registo):
    if (dt_fim == ""):
        dt_fim = dt_p_fim
    duracao = (dt_fim - dt_inicio).days + 1
    if duracao < 1:
        print("-> Erro: A data prevista de término deve ser posterior à data agendada.")
        registar_log(f"{tipo_registo} - Duração de reparação inferior a 1 dia ({duracao} dias)") 
        return
    else:
        return duracao
#validacao de preco das pecas
def validar_valor_pecas(tipo_registo):
    while True:
        texto = input("Introduza o valor das peças (€) (- para cancelar): ").strip().replace(",", ".")
        if cancelar_processo(tipo_registo, texto):
            return None
        try:
            valor_pecas = round(float(texto), 2)
            if valor_pecas < 0:
                raise ValueError
            return (float(valor_pecas))
        except ValueError:
            print("-> Erro: Valor das peças inválido, indique um valor decimal de 2 casas decimais")
            registar_log(f"{tipo_registo} - valor inválido ({texto})") 

# --- GESTÃO DE CLIENTES ---
# Inserir clientes na base de dados (Registando o NIF como chave primária)
 
def registar_cliente():
    print("\n--- REGISTAR NOVO CLIENTE ---")
    #validação de dados
    nif = validar_nif("Registar novo cliente")
    if not nif:
        return
    nome = validar_str("o nome completo", "Registar novo cliente", nif)
    if not nome:
        return
    data_nascimento = validar_data("a data de nascimento", "Registar novo cliente", nif)
    if not data_nascimento:
        return
    sexo = validar_sexo("Registar novo cliente", nif)
    if not sexo:
        return
    telemovel = validar_tlm("Registar novo cliente", nif)
    if not telemovel:
        return
    email = validar_email("Registar novo cliente", nif)
    if not email:
        return

    conexao = None

    # Ligação à base de dados e inserção do cliente
    try:
        conexao = sqlite3.connect(basedados)
        cursor = conexao.cursor()
       
        cursor.execute("""
            INSERT INTO Cliente (NIF, Nome, "Data Nascimento", Sexo, "Nr Telemovel", email)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nif, nome, data_nascimento, sexo, telemovel, email))
       
        conexao.commit()
        conexao.close()
        print("-> Cliente registado com sucesso na base de dados!")
    except Exception as e:
        print(f"-> Erro ao gravar na base de dados: {e}") 
        registar_log(f"Registo Cliente - Erro BD (NIF {nif}): {e}")
    finally:
            if conexao is not None:
                conexao.close()
            ispressed()
        
# Consulta de Clientes na BD 
def consultar_clientes():
    print("\n--- LISTA DE CLIENTES REGISTADOS ---")
    conexao = None
    try:
        conexao = sqlite3.connect(basedados)
        cursor = conexao.cursor()
       
        cursor.execute("SELECT * FROM Cliente")
        clientes = cursor.fetchall()
        conexao.close()

        if not clientes:
            print("-> Não existem clientes registados no sistema.")
            return []
       
        for x , y in enumerate(clientes, 1):
            nif = y[0]
            nome = y[1]
            telemovel = y[4]
            email = y[5]
            print(f"{x}. Nome: {nome} | NIF: {nif} | Telemóvel: {telemovel} | Email: {email}")
           
        return clientes
    except Exception as e:
        print(f"-> Erro ao consultar a base de dados: {e}")
        registar_log(f"Consulta Clientes - Erro BD: {e}")
        return []
    finally:
        if conexao is not None:
            conexao.close()
        ispressed()

def alterar_cliente():
    print("\n--- ALTERAR DADOS DE CLIENTE ---")
    # validacao de dados
    nif = validar_nif("Alterar dados cliente")
    if not nif:
        return
    conexao = None
    try:
        conexao = sqlite3.connect(basedados)
        cursor = conexao.cursor()
       
        cursor.execute("SELECT * FROM Cliente WHERE NIF = ?", (nif,))
        cliente_existente = cursor.fetchone()
       
        if not cliente_existente:
            print("-> Não existe nenhum cliente registado com esse NIF.")
            registar_log(f"Alterar Cliente - NIF não encontrado na BD: {nif}") 
            conexao.close()
            return
       
        print(f"\nCliente encontrado: {cliente_existente[1]}")
        print("Introduza os novos dados:")
       
        novo_nome = validar_str("o nome completo", "Alterar dados cliente", nif)
        if not novo_nome:
            return
        nova_data_nascimento = validar_data("a data de nascimento", "Alterar dados cliente", nif)
        if not nova_data_nascimento:
            return
        novo_sexo = validar_sexo("Alterar dados cliente", nif)
        if not novo_sexo:
            return
        novo_telemovel = validar_tlm("Alterar dados cliente", nif)
        if not novo_telemovel:
            return
        novo_email = validar_email("Alterar dados cliente", nif)
        if not novo_email:
            return
# Ligação à base de dados e atualização dos dados do cliente
        cursor.execute("""
            UPDATE Cliente
            SET Nome = ?, "Data Nascimento" = ?, Sexo = ?, "Nr Telemovel" = ?, email = ?
            WHERE NIF = ?
        """, (novo_nome, nova_data_nascimento, novo_sexo, novo_telemovel, novo_email, nif))
       
        conexao.commit()
        conexao.close()
        print("-> Dados do cliente alterados com sucesso na base de dados!")   
    except Exception as e:
        print(f"-> Erro ao atualizar a base de dados: {e}")
        registar_log(f"Alterar Cliente - Erro BD (NIF {nif}): {e}")
    finally:
            if conexao is not None:
                conexao.close()
            ispressed()
       
##### Registo de telemoveis #####
def registar_telemovel():
    print("\n--- REGISTAR NOVO TELEMÓVEL ---")
    # validacao de dados
    conexao = None
    try:
        marca = validar_str("a marca do telemóvel", "Registar novo telemóvel", "sem pk")
        if not marca:
            return
        modelo = validar_printable("o modelo do telemóvel", "Registar novo telemóvel", "sem pk")
        if not modelo:
            return
        ram = validar_printable("a memória RAM do telemóvel (ex: 8, 16GB, 4)", "Registar novo telemóvel", "sem pk")
        if not ram:
            return
        disco = validar_printable("o armazenamento total do telemóvel (ex: 256GB, 1TB)", "Registar novo telemóvel", "sem pk")
        if not disco:
            return
        estado = validar_estado_tlm("Registar novo telemóvel", "sem pk")
        if not estado:
            return

        conexao = sqlite3.connect(basedados)
        cursor = conexao.cursor()
       # verificar se o estado existe na tabela Estado
        cursor.execute("SELECT * FROM Estado WHERE ID = ?", (estado,))
        if not cursor.fetchone():
            print(f"-> Aviso: O ID de estado {estado} não existe na tabela 'Estado'.")
            registar_log(f"Registo Telemóvel - Estado ID inexistente na BD: {estado}") 
            conexao.close()
            return
# Ligação à base de dados e inserção do telemóvel
        cursor.execute("""
            INSERT INTO Telemovel (Marca, Modelo, RAM, Disco, Estado)
            VALUES (?, ?, ?, ?, ?)
        """, (marca, modelo, ram, disco, estado))
       
        conexao.commit()
        conexao.close()
        print("-> Telemóvel registado com sucesso na base de dados!")   
    except sqlite3.OperationalError as e:
        print(f"\n-> Erro na Base de Dados: {e}")
        registar_log(f"Registo Telemóvel - Erro Operacional BD: {e}")
        conexao.close()
    except Exception as e:
        print(f"\n-> Erro inesperado: {e}")
        registar_log(f"Registo Telemóvel - Erro Inesperado: {e}")
    finally:
        if conexao is not None:
            conexao.close()
        ispressed()
        
# Consultar lista de telemoveis registados na BD
def consultar_telemoveis():
    print("\n--- LISTA DE TELEMÓVEIS ---")
    # validacao de dados
    conexao = None
    try:
        conexao = sqlite3.connect(basedados)
        cursor = conexao.cursor()
       
        cursor.execute("SELECT * FROM Telemovel")
        telemoveis = cursor.fetchall()
        conexao.close()

        if not telemoveis:
            print("-> Não existem telemóveis registados no sistema.")
            return
       
        for t in telemoveis:
            print(f"ID: {t[0]} | Marca: {t[1]} | Modelo: {t[2]} | RAM: {t[3]} | Disco: {t[4]} | Estado ID: {t[5]}")        
    except Exception as e:
        print(f"-> Erro ao consultar telemóveis: {e}")
        registar_log(f"Consulta Telemóveis - Erro BD: {e}")
    finally:
        if conexao is not None:
            conexao.close()
        ispressed()

# Alterar dados de telemovel na BD
def alterar_telemovel():
    print("\n--- ALTERAR DADOS DE TELEMÓVEL ---")
    #continuar aqui, definir funcao para ir buscar id de telemoveis
    id_telemovel = validar_id("Alterar Dados de Telemóvel")
    if not id_telemovel:
        return
    conexao = None
    try:
        conexao = sqlite3.connect(basedados)
        cursor = conexao.cursor()
       
        cursor.execute("SELECT * FROM Telemovel WHERE ID = ?", (id_telemovel,))
        telemovel_existente = cursor.fetchone()

        if not telemovel_existente:
            print(f"-> Erro: Não existe nenhum telemóvel registado com o ID {id_telemovel}.")
            registar_log(f"Alterar Telemóvel - ID inexistente na BD: {id_telemovel}") 
            conexao.close()
            return
       
        print(f"\nTelemóvel encontrado -> Marca: {telemovel_existente[1]} | Modelo: {telemovel_existente[2]}")
        print("Introduza os novos dados:")
       
        nova_marca = validar_str("a marca do telemóvel", "Alterar dados de telemóvel", id)
        if not nova_marca:
            return
        novo_modelo = validar_printable("o modelo do telemóvel", "Alterar dados de telemóvel", id)
        if not novo_modelo:
            return
        nova_ram = validar_printable("a memória RAM do telemóvel (ex: 8, 16GB, 4)", "Alterar dados de telemóvel", id)
        if not nova_ram:
            return
        novo_disco = validar_printable("o armazenamento total do telemóvel (ex: 256GB, 1TB)", "Alterar dados de telemóvel", id)
        if not novo_disco:
            return
        novo_estado = validar_estado_tlm("Alterar dados de telemóvel", id)
        if not novo_estado:
            return
        # Ligação à base de dados e atualização dos dados do telemóvel
        cursor.execute("""
            UPDATE Telemovel
            SET Marca = ?, Modelo = ?, RAM = ?, Disco = ?, Estado = ?
            WHERE ID = ?
        """, (nova_marca, novo_modelo, nova_ram, novo_disco, novo_estado, id_telemovel))
       
        conexao.commit()
        conexao.close()
        print("-> Dados do telemóvel alterados com sucesso na base de dados!")  
    except Exception as e:
        print(f"-> Erro ao atualizar o telemóvel: {e}")
        registar_log(f"Alterar Telemóvel - Erro BD (ID {id_telemovel}): {e}")
    finally:
            if conexao is not None:
                conexao.close()
            ispressed() 
        
# Criar Pedido de reparação       
def criar_pedido():   
    print("\n--- CRIAR/AGENDAR PEDIDO DE REPARAÇÃO ---")
    tipo_registo = "Criar pedido de reparação"
    # validacao de dados
    conexao = None
    try:
        nif = validar_nif(tipo_registo)
        if not nif:
            return
        conexao = sqlite3.connect(basedados)
        cursor = conexao.cursor()
        cursor.execute("SELECT 1 FROM Cliente WHERE NIF = ?", (nif,))
        if not cursor.fetchone():
            print("-> Não existe nenhum cliente registado com esse NIF.")
            registar_log(f"Criar Pedido - Cliente não encontrado (NIF {nif})") 
            return
        id_telemovel = validar_id(tipo_registo)
        if not id_telemovel:
            return
        cursor.execute("SELECT * FROM Telemovel WHERE ID = ?", (id_telemovel,))
        if not cursor.fetchone():
            print("-> Não existe nenhum telemóvel registado com esse ID.")
            registar_log(f"Criar Pedido - Telemóvel não encontrado (ID {id_telemovel})") 
            return
        obs = validar_printable("as observações da reparação", tipo_registo, id)
        if not obs:
            return
        dt_inicio = validar_data("a data de inicio", tipo_registo, id)
        if not dt_inicio:
            return
        dt_prevista_fim = validar_data("a data prevista de fim", tipo_registo, id)
        if not dt_prevista_fim:
                return
        dt_fim = validar_data_fim("a data de fim", tipo_registo, id)
        if dt_fim == '-':
                return
        valor_pecas = validar_valor_pecas("o valor das peças")
        if not valor_pecas:
                return
        duracao = calcular_duracao_reparacao(dt_inicio, dt_prevista_fim, dt_fim, tipo_registo)
        if not duracao:
                return
        if duracao == None:
            raise Exception("Duração inferior a 1 dia")
        valor_reparacao = valor_pecas + (20 * duracao)
        if not valor_reparacao:
                return
        # Determinar o estado do serviço com base na data de fim
        if dt_fim != "":
            estado_servico = "Concluída"
        else:
            estado_servico = "Agendada"

        # Ligação à base de dados e inserção do pedido de reparação
        cursor.execute(
            """INSERT INTO Reparacao
               (NIF, IDTelemovel, Obs, DtInicio, DtPrevistaFim, DtFim,
                ValorPecas, ValorReparacao, EstadoServico)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (nif, id_telemovel, obs, dt_inicio, dt_prevista_fim, dt_fim,
             valor_pecas, valor_reparacao, estado_servico)
        )
        conexao.commit()
        print("\n-> Pedido de reparação criado com sucesso!")
    except Exception as e:
        print(f"-> Erro ao criar pedido de reparação: {e}")
        registar_log(f"Criar Pedido - Erro Geral/BD: {e}") 
    finally:
        if conexao is not None:
            conexao.close()
        ispressed()
            
# Consultar lista de reparações
def consultar_reparações():
    print("\n--- LISTA DE REPARAÇÕES ---")
    # Input do filtro de reparações a consultar
    filtro = input("Quais as reparações que deseja consultar? (1-Todas (default), 2-Agendadas, 3-Em Curso, 4-Concluída): ").strip()
    conexao = None
    try:
        conexao = sqlite3.connect(basedados)
        cursor = conexao.cursor()
        if filtro == "1" or filtro == "":
            cursor.execute("SELECT * FROM Reparacao")
        elif filtro == "2":
            cursor.execute("SELECT * FROM Reparacao WHERE EstadoServico = 'Agendada'")
        elif filtro == "3":
            cursor.execute("SELECT * FROM Reparacao WHERE EstadoServico = 'Em Curso'")
        elif filtro == "4":
            cursor.execute("SELECT * FROM Reparacao WHERE EstadoServico IN ('Concluída')")
        else:
            print("-> Opção de filtro inválida.")
            registar_log(f"Consulta Reparações - Filtro inválido introduzido: {filtro}") 
            conexao.close()
            return
        reparacoes = cursor.fetchall()
        conexao.close()
        if not reparacoes:
            print("-> Não existem reparações registadas no sistema.")
            return
        for r in reparacoes:
            print(f"| Estado: {r[9]} | ID: {r[0]} | NIF: {r[1]} | ID Tel.: {r[2]} | Observações: {r[3]} | Data Início: {r[4]} | Data Prevista Fim: {r[5]} | Data Fim: {r[6]} | Valor Peças: {r[7]}€ | Valor Reparação: {r[8]}€ |") 
    except Exception as e:
        print(f"-> Erro ao consultar reparações: {e}")
        registar_log(f"Consulta Reparações - Erro BD: {e}")
    finally:
        ispressed()
        if conexao is not None:
            conexao.close()
        ispressed() 
    
# Alterar estado da reparação
def alterar_estado_rep():
    tipo_registo = "Alterar estado de reparação"
    print("\n--- ALTERAR ESTADO DE REPARAÇÃO ---")
    # validacao de dados
    id = validar_id(tipo_registo)
    if not id:
        return
    conexao = None
    try:
        conexao = sqlite3.connect(basedados)
        cursor = conexao.cursor()
       
        cursor.execute("SELECT * FROM Reparacao WHERE IDReparacao = ?", (id,))
        reparacao_existente = cursor.fetchone()
       
        if not reparacao_existente:
            print(f"-> Erro: Não existe nenhuma reparação registada com o ID {id}.")
            registar_log(f"Alterar Estado Reparação - ID inexistente na BD: {id}") 
            conexao.close()
            return
        print(f"\nReparação encontrada -> | ID: {reparacao_existente[0]} | Estado: {reparacao_existente[9]}")
        if reparacao_existente[9] == "Em Curso":
            print("Não é possível alterar reparações em curso")
            registar_log(F"{tipo_registo} - Erro tentativa de alteração de reparação em curso (ID {id})")
        print("Introduza o novo estado:")
       
        novo_estado = input("Novo estado da reparação (1 - Agendada, 2 - Em Curso, 3 - Concluída): ").strip()
        if novo_estado == "1":
            novo_estado = "Agendada"
        elif novo_estado == "2":
            novo_estado = "Em Curso"
        elif novo_estado == "3":
            novo_estado = "Concluída"
        else:
            print("-> Erro: Opção de estado inválida.")
            registar_log(f"Alterar Estado Reparação - Opção inválida (ID {id}): {novo_estado}") 
            conexao.close()
            return
        # Ligação à base de dados e atualização do estado da reparação
        cursor.execute("""
            UPDATE Reparacao
            SET EstadoServico = ?
            WHERE IDReparacao = ?
        """, (novo_estado, id))
        conexao.commit()
        conexao.close()
        print("-> Estado da reparação alterado com sucesso na base de dados!")
    except Exception as e:
        print(f"-> Erro ao atualizar o estado da reparação: {e}")
        registar_log(f"Alterar Estado Reparação - Erro BD (ID {id}): {e}") 
    finally:
            if conexao is not None:
                conexao.close()
            ispressed()
# Alterar Registo de Reparação
def alterar_reparacoes():
    print("\n--- ALTERAR REGISTO DE REPARAÇÃO ---")
    tipo_registo = "Alterar reparação"
    # validacao de dados
    id = validar_id(tipo_registo)
    if not id:
        return
    conexao = None
    try:
        conexao = sqlite3.connect(basedados)
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Reparacao WHERE IDReparacao = ?", (id,))
        reparacao_existente = cursor.fetchone()
        if not reparacao_existente:
            print(f"-> Não existe nenhuma reparação registada com o ID {id}.")
            registar_log(f"Alterar Registo Reparação - ID inexistente na BD: {id}") 
            conexao.close()
            return
        print(f"\nReparação encontrada (ID: {reparacao_existente[0]})")
        print("Introduza os novos dados:")
        nova_obs = validar_printable("as observações da reparação", tipo_registo, id)
        if not nova_obs:
            return
        nova_dt_inicio = validar_data("a data de inicio", tipo_registo, id)
        if not nova_dt_inicio:
            return
        nova_dt_prev_fim = validar_data("a data prevista de fim", tipo_registo, id)
        if not nova_dt_prev_fim:
            return
        nova_dt_fim = validar_data("a data de fim", tipo_registo, id) or None
        if not nova_dt_fim:
            return
        duracao = calcular_duracao_reparacao(nova_dt_inicio, nova_dt_prev_fim, nova_dt_fim, tipo_registo)
        if not duracao:
            return
        if duracao == None:
            raise Exception("Duração inferior a 1 dia")
        novo_valor_pecas = validar_valor_pecas("o valor das peças")
        if not novo_valor_pecas:
            return
        novo_valor_reparacao = novo_valor_pecas + (20 * duracao)
        if nova_dt_fim != None:
            estado_servico = "Concluída"
        else:
            estado_servico = "Agendada"
        # Ligação à base de dados e atualização do registo da reparação
        cursor.execute("""
            UPDATE Reparacao
            SET Obs = ?, DtInicio = ?, DtPrevistaFim = ?, DtFim = ?, ValorPecas = ?, ValorReparacao = ?, EstadoServico = ?
            WHERE IDReparacao = ?
        """, (nova_obs, nova_dt_inicio, nova_dt_prev_fim, nova_dt_fim, novo_valor_pecas, novo_valor_reparacao, estado_servico, id))
        conexao.commit()
        conexao.close()
        print("-> Dados da reparação alterados com sucesso na base de dados!")
    except Exception as e:
        print(f"-> Erro ao atualizar a base de dados: {e}")
        registar_log(f"Alterar Registo Reparação - Erro BD (ID {id}): {e}")
    finally:
            if conexao is not None:
                conexao.close()
            ispressed()  
##################################################### MENU PRINCIPAL DO SISTEMA #####################################################

def menu():
    while True:
        limpar_cmd()
        print("\n" + "=" * 51)
        print("     SMARTFIX - SISTEMA DE GESTÃO E REPARAÇÕES     ")
        print("=" * 51)
        print("\n--- GESTÃO DE CLIENTES ---")
        print(" 1. Registar Novo Cliente")
        print(" 2. Consultar Clientes Registados")
        print(" 3. Alterar Dados de Cliente")
        print("\n--- GESTÃO DE TELEMÓVEIS ---")
        print(" 4. Registar Novo Telemóvel")
        print(" 5. Consultar Lista de Telemóveis")
        print(" 6. Alterar Dados de Telemóvel")
        print("\n--- GESTÃO DE REPARAÇÕES ---")
        print(" 7. Criar/Agendar Pedido de Reparação")
        print(" 8. Consultar Reparações (Todas / Por Estado)")
        print(" 9. Atualizar Estado de Reparação (Agendada / Em Curso / Concluída)")
        print("10. Alterar Registo de Reparação")
        print("\n *0. Sair do Sistema*")
        opcao = input("\nEscolha uma opção (0 a 10): ")
        limpar_cmd()
       
        # Processamento das opções
 
        if opcao == "1":
            registar_cliente()
        elif opcao == "2":
            consultar_clientes()
        elif opcao == "3":
            alterar_cliente()
        elif opcao == "4":
            registar_telemovel()
        elif opcao == "5":
            consultar_telemoveis()
        elif opcao == "6":
            alterar_telemovel()
        elif opcao == "7":  
            criar_pedido()
        elif opcao == "8":
            consultar_reparações()
        elif opcao == "9":    
            alterar_estado_rep()
        elif opcao == "10":
            alterar_reparacoes()
        elif opcao == "0":
            print("\nA sair do sistema SmartFix. Até breve!")
            break
        else:
            print("-> Opção inválida ou funcionalidade ainda não implementada.")
menu()
