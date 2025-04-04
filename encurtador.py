import tkinter as tk
from tkinter import ttk, messagebox
import requests
import pyperclip  # Para copiar para a área de transferência

def encurtar_tinyurl(url):
    """Função que encurta o URL usando a API do TinyURL"""
    tinyurl_api = f"https://tinyurl.com/api-create.php?url={url}"
    try:
        response = requests.get(tinyurl_api)
        
        if response.status_code == 200:
            return response.text  # Retorna o link encurtado
        else:
            return f"Erro: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Erro na conexão: {str(e)}"

def encurtar_link():
    """Função chamada quando o botão 'Encurtar' é pressionado"""
    url_original = entrada_url.get()
    
    if not url_original:
        messagebox.showerror("Erro", "Por favor, insira um URL válido")
        return
    
    # Verifica se o URL começa com http:// ou https://
    if not (url_original.startswith('http://') or url_original.startswith('https://')):
        url_original = 'https://' + url_original
    
    # Atualiza o status
    status_label.config(text="Encurtando link...")
    root.update()
    
    # Encurta o link
    url_encurtada = encurtar_tinyurl(url_original)
    
    # Exibe o resultado
    resultado_var.set(url_encurtada)
    status_label.config(text="Link encurtado com sucesso!")

def copiar_link():
    """Função para copiar o link encurtado para a área de transferência"""
    link_encurtado = resultado_var.get()
    
    if link_encurtado and not link_encurtado.startswith("Erro"):
        pyperclip.copy(link_encurtado)
        status_label.config(text="Link copiado para a área de transferência!")
    else:
        messagebox.showerror("Erro", "Não há link válido para copiar")

# Criar a janela principal
root = tk.Tk()
root.title("Encurtador de Links")
root.geometry("500x300")
root.resizable(False, False)

# Estilo
style = ttk.Style()
style.configure("TButton", font=("Arial", 10, "bold"), padding=5)
style.configure("TLabel", font=("Arial", 10))
style.configure("Titulo.TLabel", font=("Arial", 14, "bold"))

# Frame principal
frame_principal = ttk.Frame(root, padding=20)
frame_principal.pack(fill="both", expand=True)

# Título
titulo = ttk.Label(frame_principal, text="Encurtador de Links", style="Titulo.TLabel")
titulo.pack(pady=(0, 20))

# Frame para entrada do URL
frame_entrada = ttk.Frame(frame_principal)
frame_entrada.pack(fill="x", pady=5)

ttk.Label(frame_entrada, text="URL:").pack(side="left", padx=(0, 5))
entrada_url = ttk.Entry(frame_entrada, width=50)
entrada_url.pack(side="left", fill="x", expand=True)
entrada_url.focus()

# Botão de encurtar
botao_encurtar = ttk.Button(frame_principal, text="Encurtar", command=encurtar_link)
botao_encurtar.pack(pady=10)

# Frame para resultado
frame_resultado = ttk.Frame(frame_principal)
frame_resultado.pack(fill="x", pady=5)

ttk.Label(frame_resultado, text="Link encurtado:").pack(side="left", padx=(0, 5))
resultado_var = tk.StringVar()
resultado_entry = ttk.Entry(frame_resultado, textvariable=resultado_var, width=50, state="readonly")
resultado_entry.pack(side="left", fill="x", expand=True)

# Botão copiar
botao_copiar = ttk.Button(frame_principal, text="Copiar para Área de Transferência", command=copiar_link)
botao_copiar.pack(pady=10)

# Status
status_label = ttk.Label(frame_principal, text="")
status_label.pack(pady=5)

# Dica informativa
dica = ttk.Label(frame_principal, text="Dica: URLs sem 'http://' serão automaticamente prefixadas com 'https://'", 
                 font=("Arial", 8), foreground="gray")
dica.pack(side="bottom", pady=(20, 0))

# Iniciar o loop principal
root.mainloop()