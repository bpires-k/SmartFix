# IMPORTAÇÕES DE MODULOS NECESSÁRIOS E DEFINIÇÃO DE VARIÁVEIS GLOBAIS
import datetime
import os
import sqlite3

# --- CRIAÇÃO AUTOMÁTICA DO FICHEIRO DE LOGS ---
if not os.path.exists("log_erros.txt"):
    with open("log_erros.txt", "w", encoding="utf-8") as l:
        data_inicio = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        l.write(f"[{data_inicio}] SISTEMA: Ficheiro de logs criado e sistema iniciado.\n")

basedados = "BDSmartFix2.db"
dt = datetime.datetime.now()

def registar_log(mensagem):
    try:
        with open("log_erros.txt", "a", encoding="utf-8") as ficheiro:
            data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ficheiro.write(f"[{data_atual}] ERRO: {mensagem}\n")
    except Exception as erro:
        print(f"Não foi possível gravar o log: {erro}")
       
# VALIDAÇÕES DE INPUTS
# Função que valida o NIF, devendo ser composto por 9 dígitos.
'''
def ler_nif():
    while True:
        nif = input("Introduza o NIF: ")
        if len(nif) == 9:
            try:
                int(nif) # Erro se o input tiver letras
                return nif
            except ValueError:
                print("-> NIF inválido! Deve conter exatamente 9 dígitos numéricos.")
                registar_log(f"Tentativa de introdução de NIF inválido: {nif}")
        break
'''
#funcao redundante, nao é usada no codigo

# --- GESTÃO DE CLIENTES ---
# Inserir clientes na base de dados (Registando o NIF como chave primária)
 
def registar_cliente():
    print("\n--- REGISTAR NOVO CLIENTE ---")
   
    # 1. Validação do NIF
    nif_str = input("Introduza o NIF (9 dígitos): ")
    try:
        if len(nif_str) != 9:
            raise ValueError("O NIF deve ter exatamente 9 dígitos.")
        nif = int(nif_str)
    except ValueError as e:
        print(f"-> Erro no NIF: {e}")
        registar_log(f"Registo Cliente - NIF inválido ({nif_str}): {e}") 
        return
#nao é usada a funcao ler_nif
    nome = input("Nome completo: ")

    # 2. Validação da Data de Nascimento
    data_nascimento = input("Data de nascimento (DD-MM-AAAA): ")
    partes_data = data_nascimento.split('-')
   
    if (len(partes_data) != 3 or
        len(partes_data[0]) != 2 or not partes_data[0].isdigit() or
        len(partes_data[1]) != 2 or not partes_data[1].isdigit() or
        len(partes_data[2]) != 4 or not partes_data[2].isdigit()):
        print("-> Erro: Formato de data inválido. Utilize o formato DD-MM-AAAA.")
        registar_log(f"Registo Cliente - Data inválida (NIF {nif}): {data_nascimento}") 
        return
#brute force no if
    sexo = input("Sexo (M/F): ").upper()

    # Validação do Telemóvel
    tel_str = input("Nº de telemóvel de contacto: ")
    try:
        telemovel = int(tel_str)
    except ValueError:
        print("-> Erro: O número de telemóvel deve conter apenas dígitos.")
        registar_log(f"Registo Cliente - Telemóvel inválido (NIF {nif}): {tel_str}") 
        return
#sem validaçao de 9 digitos
    # 3. Validação básica do Email
    email = input("email: ")
    if "@" not in email or "." not in email.split("@")[-1]:
        print("-> Erro: Formato de email inválido.")
        registar_log(f"Registo Cliente - Email inválido (NIF {nif}): {email}") 
#validação estranha do email
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
        
# Consulta de Clientes na BD 
def consultar_clientes():
    print("\n--- LISTA DE CLIENTES REGISTADOS ---")
   
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
   
def alterar_cliente():
    print("\n--- ALTERAR DADOS DE CLIENTE ---")
   
    nif_str = input("Introduza o NIF do cliente cujos dados pretende atualizar (9 dígitos): ")
    try:
        if len(nif_str) != 9:
            print("-> Erro: O NIF deve ter exatamente 9 dígitos.")
            registar_log(f"Alterar Cliente - Tamanho NIF inválido: {nif_str}") 
            return
        nif = int(nif_str)
        #nao foi usado o ler_nif
    except ValueError:
        print("-> Erro: O NIF deve conter apenas números.")
        registar_log(f"Alterar Cliente - NIF numérico inválido: {nif_str}") 
        return

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
       
        novo_nome = input("Novo nome completo: ")
        nova_data = input("Nova data de nascimento (DD-MM-AAAA): ")
        novo_sexo = input("Novo sexo (M/F): ").upper()
       
        tel_str = input("Novo nº de telemóvel: ")
        try:
            novo_telemovel = int(tel_str)
        except ValueError:
            print("-> Erro: O número de telemóvel deve conter apenas dígitos.")
            registar_log(f"Alterar Cliente - Novo telemóvel inválido (NIF {nif}): {tel_str}") 
            conexao.close()
            return
           #redundante ter novas validações, melhor fazer funçoes para cada dado
        novo_email = input("Novo email: ")

        cursor.execute("""
            UPDATE Cliente
            SET Nome = ?, "Data Nascimento" = ?, Sexo = ?, "Nr Telemovel" = ?, email = ?
            WHERE NIF = ?
        """, (novo_nome, nova_data, novo_sexo, novo_telemovel, novo_email, nif))
       
        conexao.commit()
        conexao.close()
        print("-> Dados do cliente alterados com sucesso na base de dados!")
       
    except Exception as e:
        print(f"-> Erro ao atualizar a base de dados: {e}")
        registar_log(f"Alterar Cliente - Erro BD (NIF {nif}): {e}") 
       
##### Registo de telemoveis #####      
       
def registar_telemovel():
    print("\n--- REGISTAR NOVO TELEMÓVEL ---")
   
    try:
        marca = input("Marca: ").strip()
        modelo = input("Modelo: ").strip()
        ram = input("RAM: ").strip()
        disco = input("Disco: ").strip()
       #nao tem exemplos como no alterar_telemovel
        estado_str = input("ID do Estado do telemóvel (1-novo, 2-semi-novo, 3-usado): ").strip()
        try:
            estado_id = int(estado_str)
        except ValueError:
            print("-> Erro: O ID do estado deve ser um número inteiro.")
            registar_log(f"Registo Telemóvel - Estado ID não numérico: {estado_str}") 
            return

        conexao = sqlite3.connect(basedados)
        cursor = conexao.cursor()
       
        cursor.execute("SELECT * FROM Estado WHERE ID = ?", (estado_id,))
        if not cursor.fetchone():
            print(f"-> Aviso: O ID de estado {estado_id} não existe na tabela 'Estado'.")
            registar_log(f"Registo Telemóvel - Estado ID inexistente na BD: {estado_id}") 
            conexao.close()
            return

        cursor.execute("""
            INSERT INTO Telemovel (Marca, Modelo, RAM, Disco, Estado)
            VALUES (?, ?, ?, ?, ?)
        """, (marca, modelo, ram, disco, estado_id))
       
        conexao.commit()
        conexao.close()
        print("-> Telemóvel registado com sucesso na base de dados!")
       
    except sqlite3.OperationalError as e:
        print(f"\n-> Erro na Base de Dados: {e}")
        registar_log(f"Registo Telemóvel - Erro Operacional BD: {e}") 
    except Exception as e:
        print(f"\n-> Erro inesperado: {e}")
        registar_log(f"Registo Telemóvel - Erro Inesperado: {e}") 
        
# Consultar lista de telemoveis registados na BD
def consultar_telemoveis():
    print("\n--- LISTA DE TELEMÓVEIS ---")
   
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

# Alterar dados de telemovel na BD
def alterar_telemovel():
    print("\n--- ALTERAR DADOS DE TELEMÓVEL ---")
   
    id_str = input("Introduza o ID do telemóvel que pretende alterar: ")
    try:
        id_telemovel = int(id_str)
    except ValueError:
        print("-> Erro: O ID deve ser um número inteiro válido.")
        registar_log(f"Alterar Telemóvel - ID inválido: {id_str}") 
        return

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
       
        nova_marca = input("Nova marca: ").strip()
        novo_modelo = input("Novo modelo: ").strip()
        nova_ram = input("Nova RAM (ex: 8GB): ").strip()
        novo_disco = input("Novo disco (ex: 256GB): ").strip()
        novo_estado = input("Novo estado: ").strip()
#redundante fazer novos registos
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
        
# Criar Pedido de reparação       
def criar_pedido():   
    print("\n--- CRIAR/AGENDAR PEDIDO DE REPARAÇÃO ---")

    conexao = None
    try:
        nif_str = input("Introduza o NIF do cliente: ").strip()
        if len(nif_str) != 9 or not nif_str.isdigit():
            print("-> Erro: O NIF deve conter exatamente 9 dígitos.")
            registar_log(f"Criar Pedido - NIF inválido: {nif_str}") 
            return
        #nao foi usada a funcao ler_nif
        nif = int(nif_str)
        conexao = sqlite3.connect(basedados)
        cursor = conexao.cursor()
        cursor.execute("SELECT 1 FROM Cliente WHERE NIF = ?", (nif,))
        if not cursor.fetchone():
            print("-> Não existe nenhum cliente registado com esse NIF.")
            registar_log(f"Criar Pedido - Cliente não encontrado (NIF {nif})") 
            return
        
        id_telemovel_str = input("Introduza o ID do telemóvel a reparar: ").strip()
        try:
            id_telemovel = int(id_telemovel_str)
        except ValueError:
            print("-> Erro: O ID do telemóvel deve ser um número inteiro.")
            registar_log(f"Criar Pedido - ID Telemóvel não numérico: {id_telemovel_str}") 
            return
        cursor.execute("SELECT * FROM Telemovel WHERE ID = ?", (id_telemovel,))
        if not cursor.fetchone():
            print("-> Não existe nenhum telemóvel registado com esse ID.")
            registar_log(f"Criar Pedido - Telemóvel não encontrado (ID {id_telemovel})") 
            return
        
        obs = input("Descrição da reparação: ").strip()
        
        dt_inicio = input("Data agendada (DD-MM-AAAA): ").strip()
        dt_prevista_fim = input("Data prevista de término (DD-MM-AAAA): ").strip()
        dt_fim = input("Data de término (DD-MM-AAAA) [opcional]: ").strip() or None
        try:
            data_inicio = datetime.datetime.strptime(dt_inicio, "%d-%m-%Y")
            data_prevista_fim = datetime.datetime.strptime(dt_prevista_fim, "%d-%m-%Y")
            if dt_fim:
                datetime.datetime.strptime(dt_fim, "%d-%m-%Y")
            valor_pecas = float(input("Valor das peças (€): ").strip().replace(",", "."))
            if valor_pecas < 0:
                raise ValueError
        except ValueError:
            print("-> Erro: Introduza datas válidas e um valor de peças não negativo.")
            registar_log(f"Criar Pedido - Formato de datas/valor de peças inválido") 
            return
        #podia existir uma funcao para validacao de datas
        if dt_fim==None:
            duracao = (data_prevista_fim - data_inicio).days
        else:
            duracao = (datetime.datetime.strptime(dt_fim, "%d-%m-%Y") - data_inicio).days
        if duracao < 1:
            print("-> Erro: A data prevista de término deve ser posterior à data agendada.")
            registar_log(f"Criar Pedido - Duração de reparação inferior a 1 dia ({duracao} dias)") 
            return

        valor_reparacao = valor_pecas + (20 * duracao)
        if dt_fim!= None:
            estado_servico = "Concluida"
        else:
            estado_servico = "Agendada"
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
            
# Consultar lista de reparações
def consultar_reparações():
    print("\n--- LISTA DE REPARAÇÕES ---")
    filtro=input("Quais as reparações que deseja consultar? (1-Todas, 2-Agendadas, 3-Em Curso, 4-Concluída): ").strip()

    try:
        conexao = sqlite3.connect(basedados)
        cursor = conexao.cursor()
        if filtro == "1":
            cursor.execute("SELECT * FROM Reparacao")
        elif filtro == "2":
            cursor.execute("SELECT * FROM Reparacao WHERE EstadoServico = 'Agendada'")
        elif filtro == "3":
            cursor.execute("SELECT * FROM Reparacao WHERE EstadoServico = 'Em Curso'")
        elif filtro == "4":
            cursor.execute("SELECT * FROM Reparacao WHERE EstadoServico IN ('Concluida', 'Concluída')")
        else:
            print("-> Opção de filtro inválida.")
            registar_log(f"Consulta Reparações - Filtro inválido introduzido: {filtro}") 
            conexao.close()
            return
            #se nao meter filtro nao existe uma opcao default
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
    
# Alterar estado da reparação
def alterar_estado_rep():
    print("\n--- ALTERAR ESTADO DE REPARAÇÃO ---")
   
    id_str = input("Introduza o ID da reparação que pretende actualizar: ")
    try:
        id_reparacao = int(id_str)
    except ValueError:
        print("-> Erro: O ID deve ser um número inteiro válido.")
        registar_log(f"Alterar Estado Reparação - ID não numérico: {id_str}") 
        return

    try:
        conexao = sqlite3.connect(basedados)
        cursor = conexao.cursor()
       
        cursor.execute("SELECT * FROM Reparacao WHERE IDReparacao = ?", (id_reparacao,))
        reparacao_existente = cursor.fetchone()
       
        if not reparacao_existente:
            print(f"-> Erro: Não existe nenhuma reparação registada com o ID {id_reparacao}.")
            registar_log(f"Alterar Estado Reparação - ID inexistente na BD: {id_reparacao}") 
            conexao.close()
            return
       
        print(f"\nReparação encontrada -> | ID: {reparacao_existente[0]} | Estado: {reparacao_existente[9]}")
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
            registar_log(f"Alterar Estado Reparação - Opção inválida (ID {id_reparacao}): {novo_estado}") 
            conexao.close()
            return

        cursor.execute("""
            UPDATE Reparacao
            SET EstadoServico = ?
            WHERE IDReparacao = ?
        """, (novo_estado, id_reparacao))
       
        conexao.commit()
        conexao.close()
        print("-> Estado da reparação alterado com sucesso na base de dados!")
       
    except Exception as e:
        print(f"-> Erro ao atualizar o estado da reparação: {e}")
        registar_log(f"Alterar Estado Reparação - Erro BD (ID {id_reparacao}): {e}") 
        
# Alterar Registo de Reparação
def alterar_reparacoes():
    print("\n--- ALTERAR REGISTO DE REPARAÇÃO ---")
   
    id_str = input("Introduza o ID da reparação que pretende atualizar: ")
    try:
        id_reparacao = int(id_str)
    except ValueError:
        print("-> Erro: O ID deve ser um número inteiro válido.")
        registar_log(f"Alterar Registo Reparação - ID não numérico: {id_str}") 
        return

    try:
        conexao = sqlite3.connect(basedados)
        cursor = conexao.cursor()
       
        cursor.execute("SELECT * FROM Reparacao WHERE IDReparacao = ?", (id_reparacao,))
        reparacao_existente = cursor.fetchone()
       
        if not reparacao_existente:
            print(f"-> Não existe nenhuma reparação registada com o ID {id_reparacao}.")
            registar_log(f"Alterar Registo Reparação - ID inexistente na BD: {id_reparacao}") 
            conexao.close()
            return
       
        print(f"\nReparação encontrada (ID: {reparacao_existente[0]})")
        print("Introduza os novos dados:")
       
        nova_obs = input("Introduza as novas observações: ").strip()
        nova_dtInicio = input("Nova data de início (DD-MM-AAAA): ").strip().replace('/', '-')
        nova_dtPrevFim = input("Nova data prevista de fim (DD-MM-AAAA): ").strip().replace('/', '-')
        nova_dtFim = input("Nova data de fim (DD-MM-AAAA) [opcional]: ").strip().replace('/', '-') or None
        
        try:
            data_inicio = datetime.datetime.strptime(nova_dtInicio, "%d-%m-%Y")
            data_prevista_fim = datetime.datetime.strptime(nova_dtPrevFim, "%d-%m-%Y")
            if nova_dtFim:
                datetime.datetime.strptime(nova_dtFim, "%d-%m-%Y")
                
            novo_valorPecas = float(input("Novo valor das peças (€): ").strip().replace(",", "."))
            if novo_valorPecas < 0:
                raise ValueError
        except ValueError:
            print("-> Erro: Introduza datas válidas e um valor de peças não negativo.")
            registar_log(f"Alterar Registo Reparação - Datas/valor peças inválidos (ID {id_reparacao})") 
            conexao.close()
            return

        if nova_dtFim is None:
            duracao = (data_prevista_fim - data_inicio).days
            estado_servico = "Agendada"
        else:
            duracao = (datetime.datetime.strptime(nova_dtFim, "%d-%m-%Y") - data_inicio).days
            estado_servico = "Concluida"

        if duracao < 1:
            print("-> Erro: A data prevista/fim de término deve ser posterior à data de início.")
            registar_log(f"Alterar Registo Reparação - Duração inferior a 1 dia (ID {id_reparacao})") 
            conexao.close()
            return

        novo_valor_reparacao = novo_valorPecas + (20 * duracao)

        cursor.execute("""
            UPDATE Reparacao
            SET Obs = ?, DtInicio = ?, DtPrevistaFim = ?, DtFim = ?, ValorPecas = ?, ValorReparacao = ?, EstadoServico = ?
            WHERE IDReparacao = ?
        """, (nova_obs, nova_dtInicio, nova_dtPrevFim, nova_dtFim, novo_valorPecas, novo_valor_reparacao, estado_servico, id_reparacao))
       
        conexao.commit()
        conexao.close()
        print("-> Dados da reparação alterados com sucesso na base de dados!")
       
    except Exception as e:
        print(f"-> Erro ao atualizar a base de dados: {e}")
        registar_log(f"Alterar Registo Reparação - Erro BD (ID {id_reparacao}): {e}") 
#redundante, deveria haver funcoes para registo individuais para nao se escrever o codigo 2 vezes
##################################################### MENU PRINCIPAL DO SISTEMA #####################################################1
 
def menu():
    while True:
        print("\n" + "=" * 45)
        print("     SMARTFIX - SISTEMA DE GESTÃO E REPARAÇÕES     ")
        print("=" * 45)
       
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