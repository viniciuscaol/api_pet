import psycopg2
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk

# Função para conectar ao banco de dados PostgreSQL
def conectar_bd():
    try:
        conexao = psycopg2.connect(
            host="localhost",
            database="pet_db",
            user="user",
            password="senha123",
            port="5432"
        )
        cursor = conexao.cursor()
        return conexao, cursor
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None, None

# Função para salvar informações de cadastro no banco
def salvar_informacoes(nome, idade, peso):
    conexao, cursor = conectar_bd()
    if conexao is not None:
        try:
            cursor.execute('INSERT INTO pets (nome, idade, peso) VALUES (%s, %s, %s)', (nome, idade, peso))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Informações salvas com sucesso!")
        except Exception as e:
            print("Erro ao salvar no banco de dados:", e)
        finally:
            cursor.close()
            conexao.close()

# Função para buscar pets no banco com filtros
# Função para buscar pets no banco com ou sem filtros
def buscar_pets(filtro, valor):
    conexao, cursor = conectar_bd()
    if conexao is not None:
        try:
            # Se o valor de busca estiver vazio, selecione todos os pets
            if valor == "":
                query = "SELECT * FROM pets"
                cursor.execute(query)
            else:
                query = f"SELECT * FROM pets WHERE {filtro} LIKE %s"
                cursor.execute(query, ('%' + valor + '%',))
            
            resultados = cursor.fetchall()
            return resultados
        except Exception as e:
            print("Erro ao buscar no banco de dados:", e)
            return []
        finally:
            cursor.close()
            conexao.close()


# Função para exibir a interface de cadastro
def exibir_interface_cadastro():
    def cadastrar_pet():
        nome = entry_nome.get()
        try:
            idade = int(entry_idade.get())
            peso = float(entry_peso.get())
            salvar_informacoes(nome, idade, peso)
        except ValueError:
            messagebox.showerror("Erro", "Idade ou peso inválidos.")
    
    janela_cadastro = tk.Toplevel()
    janela_cadastro.title("Cadastro de Pet")

    label_nome = tk.Label(janela_cadastro, text="Nome do pet:")
    label_nome.grid(row=0, column=0, padx=10, pady=5)
    entry_nome = tk.Entry(janela_cadastro)
    entry_nome.grid(row=0, column=1, padx=10, pady=5)

    label_idade = tk.Label(janela_cadastro, text="Idade do pet:")
    label_idade.grid(row=1, column=0, padx=10, pady=5)
    entry_idade = tk.Entry(janela_cadastro)
    entry_idade.grid(row=1, column=1, padx=10, pady=5)

    label_peso = tk.Label(janela_cadastro, text="Peso do pet (kg):")
    label_peso.grid(row=2, column=0, padx=10, pady=5)
    entry_peso = tk.Entry(janela_cadastro)
    entry_peso.grid(row=2, column=1, padx=10, pady=5)

    botao_cadastrar = tk.Button(janela_cadastro, text="Cadastrar", command=cadastrar_pet)
    botao_cadastrar.grid(row=3, column=0, columnspan=2, pady=10)

# Função para exibir a interface de pesquisa
def exibir_interface_pesquisa():
    def realizar_busca():
        filtro = filtro_combobox.get()
        valor = entry_valor.get()
        resultados = buscar_pets(filtro, valor)
        for row in tree.get_children():
            tree.delete(row)
        for resultado in resultados:
            tree.insert("", tk.END, values=resultado)

    janela_pesquisa = tk.Toplevel()
    janela_pesquisa.title("Pesquisar Pet")

    label_filtro = tk.Label(janela_pesquisa, text="Pesquisar por:")
    label_filtro.grid(row=0, column=0, padx=10, pady=5)

    filtros = ["nome", "idade", "peso"]
    filtro_combobox = ttk.Combobox(janela_pesquisa, values=filtros, state="readonly")
    filtro_combobox.grid(row=0, column=1, padx=10, pady=5)
    filtro_combobox.current(0)

    label_valor = tk.Label(janela_pesquisa, text="Valor:")
    label_valor.grid(row=1, column=0, padx=10, pady=5)
    entry_valor = tk.Entry(janela_pesquisa)
    entry_valor.grid(row=1, column=1, padx=10, pady=5)

    botao_buscar = tk.Button(janela_pesquisa, text="Buscar", command=realizar_busca)
    botao_buscar.grid(row=2, column=0, columnspan=2, pady=10)

    tree = ttk.Treeview(janela_pesquisa, columns=("ID", "Nome", "Idade", "Peso"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Idade", text="Idade")
    tree.heading("Peso", text="Peso")
    tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Função principal para exibir a janela inicial com opções
def janela_principal():
    janela = tk.Tk()
    janela.title("Sistema de Pets")

    botao_cadastro = tk.Button(janela, text="Cadastrar Pet", command=exibir_interface_cadastro)
    botao_cadastro.grid(row=0, column=0, padx=20, pady=20)

    botao_pesquisa = tk.Button(janela, text="Pesquisar Pet", command=exibir_interface_pesquisa)
    botao_pesquisa.grid(row=0, column=1, padx=20, pady=20)

    janela.mainloop()

janela_principal()
