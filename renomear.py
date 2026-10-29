import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def selecionar_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        entry_pasta.delete(0, tk.END)
        entry_pasta.insert(0, pasta)

def renomear_com_lista():
    pasta = entry_pasta.get()
    
    if not pasta:
        messagebox.showerror("Erro", "Por favor, selecione uma pasta.")
        return

    # Pega o texto da caixa e divide linha por linha (removendo linhas vazias)
    texto_titulos = txt_lista.get("1.0", tk.END).strip()
    if not texto_titulos:
        messagebox.showerror("Erro", "Por favor, insira a lista com os nomes dos episódios.")
        return
    
    titulos = [linha.strip() for linha in texto_titulos.split("\n") if linha.strip()]

    extensoes_video = ('.mp4', '.mkv', '.avi', '.mov', '.wmv')

    try:
        arquivos = sorted(os.listdir(pasta))
        contador = 1

        for arquivo in arquivos:
            caminho_antigo = os.path.join(pasta, arquivo)
            
            if os.path.isdir(caminho_antigo) or not arquivo.lower().endswith(extensoes_video):
                continue
                
            _, extensao = os.path.splitext(arquivo)
            
            # Verifica se existe um nome correspondente na lista que você digitou (ajustando o índice para começar em 0)
            indice_lista = contador - 1
            if indice_lista < len(titulos):
                nome_episodio = titulos[indice_lista]
                
                # Remove caracteres proibidos pelo Windows (< > : " / \ | ? *)
                nome_episodio_limpo = re.sub(r'[<>:"/\\|?*]', '', nome_episodio)
                
                novo_nome = f"Soul Eater - {contador:02d} - {nome_episodio_limpo}{extensao}"
            else:
                # Se os arquivos acabarem sendo mais numerosos que a lista
                novo_nome = f"Soul Eater - {contador:02d}{extensao}"
                
            caminho_novo = os.path.join(pasta, novo_nome)
            
            os.rename(caminho_antigo, caminho_novo)
            contador += 1
            
        messagebox.showinfo("Sucesso", f"Total de {contador - 1} episódios renomeados com sucesso!")
        
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Configuração da Janela Principal
janela = tk.Tk()
janela.title("Organizador por Lista Personalizada")
janela.geometry("500x550")
janela.resizable(False, False)

# Seleção de Pasta
label_pasta = tk.Label(janela, text="Pasta dos Episódios:")
label_pasta.pack(pady=(10, 2))

entry_pasta = tk.Entry(janela, width=60)
entry_pasta.pack(padx=10)

btn_procurar = tk.Button(janela, text="Escolher Pasta", command=selecionar_pasta)
btn_procurar.pack(pady=5)

# Caixa de Texto Estilo Lista (com barra de rolagem)
label_lista = tk.Label(janela, text="Cole os nomes dos episódios (um por linha):")
label_lista.pack(pady=(10, 2))

txt_lista = scrolledtext.ScrolledText(janela, width=55, height=18)
txt_lista.pack(padx=10, pady=5)

# Botão de Execução
btn_executar = tk.Button(janela, text="Renomear com a Lista", command=renomear_com_lista, bg="#2b8a3e", fg="white", font=("Arial", 10, "bold"))
btn_executar.pack(pady=15)

janela.mainloop()
