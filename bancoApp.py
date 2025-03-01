from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class ContaBancaria: 
    def __init__(self, saldo, titular):
        self.saldo = round(float(saldo), 2)
        self.titular = titular

    def valueDepo(self, event=None):       
        saldoCor = "black" 
        try:      
            valor = round(float(valor_entry.get()), 2)
            if valor > 0:
                if valor < abs(self.saldo) and self.saldo < 0:
                    self.saldo += valor
                    saldo_label.config(text="Dinheiro depositadoELSE\nSaldo atualizado.")
                    saldoCor = "red"
                else:
                    self.saldo += round(valor, 2)
                    saldoCor = "green"
                    saldo_label.config(text="Dinheiro depositadoIF\nSaldo atualizado.")
                    saldo_fixPos.config(text=f"R${self.saldo:.2f}")
            else:
                saldo_label.config(text="Digite um valor positivo!")
        except ValueError:
            saldo_label.config(text="Digite um valor válido!")
            return
        
        valor_entry.delete(0, END)
        saldo_fixPos.config(text=f"R${self.saldo:.2f}", fg=saldoCor) 
    
    def valueWith(self, event=None):
        try:
            valor = float(valor_entry.get())
            if 0 < valor < self.saldo:
                self.saldo -= round(valor, 2)
                saldo_label.config(text="Dinheiro retirado\nSaldo atualizado.")
                saldoCor = "green"              
            elif valor <= 0:
                saldo_label.config(text="Digite um valor positivo!")
            else:
                self.saldo -= round(valor, 2)
                saldo_label.config(text="Dinheiro retiradoELSE\nSaldo atualizado.")
                saldoCor = "red"          
        except ValueError:
            saldo_label.config(text="Digite um valor válido!")
            return
        
        valor_entry.delete(0, END)               
        saldo_fixPos.config(text=f"R${self.saldo:.2f}", fg=saldoCor) 
                                                  

# Alinhar janela no meio
def centerAlign(event=None):
        
    screenWid = tela.winfo_screenwidth()
    screenHigh = tela.winfo_screenheight()

    telaWid = int(screenWid * 0.9)
    telaHigh = int(screenHigh * 0.6) 
    posX = (screenWid - telaWid) // 2
    posY = (screenHigh - telaHigh) // 2
    tela.geometry(f"{telaWid}x{telaHigh}+{posX}+{posY}")
        

# Atualizar Layout após rotação

def atualizar_layout():
    novo_wid = tela.winfo_screenwidth()
    novo_high = tela.winfo_screenheight()

    global screenWid, screenHigh
    if novo_wid != screenWid or novo_high != screenHigh:
        screenWid, screenHigh = novo_wid, novo_high
        centerAlign()

    tela.after(500, atualizar_layout)    

   
# Função: Botão de Cédulas
         
def Counter():
        # Configurar a janela
        global telaM
    
        if telaM is not None and telaM.winfo_exists():
            telaM.lift()
            return
    
        telaM = Toplevel(tela)    
        telaM.title("Quantidade de Cédulas")
        telaM.attributes("-topmost", True)
        centerAlign()
        
       # Calculo de notas
        valorNov = round(conta.saldo, 2)
        notas = [ ]
        division = [ ]
        tipos = [200, 100, 50, 20, 10, 5, 2, 1, 0.50, 0.25, 0.10, 0.01]
        i = 0
        
        while i != 12:
            n = tipos[i]
            
            nota = int(round(valorNov, 2)/n)
            valorNov = round(valorNov, 2) - (nota*n) 
            
            notas.append(nota)
            division.append(nota*n)
            i += 1
        listNot = []     
        listQuant = [] 
        for n in range(0, 12):       
              if notas[n] != 0:
                  listNot.append(tipos[n])
                  listQuant.append(notas[n])
                  
        
        # Label de notas        
        totalNots = list(zip(listNot, listQuant))   
        textoFeito = "\n".join([f"R${nota}: {quant}x" for nota, quant in totalNots])         
        notasLabel = Label(telaM, text=textoFeito, font=("Segoe UI Emoji", 12), relief = "solid", bd=10)
        notasLabel.place(x=0, y=0)
        labelWid = notasLabel.winfo_reqwidth()
        labelHigh = notasLabel.winfo_reqheight()
              
        mWid = int(labelWid)
        mHigh = int(labelHigh) 
        mX = int(((screenWid - mWid) // 2) * 1.5)
        mY = int(((screenHigh - mHigh) // 2) * 0.02) 
        telaM.geometry(f"{mWid}x{mHigh}+{mX}+{mY}")    
            


conta = ContaBancaria(0, "Êsio")

tela = Tk()
telaM = None
screenWid, screenHigh = tela.winfo_screenwidth(), tela.winfo_screenheight()

tela.overrideredirect(True)
tela.configure(bg="#414e6e")
tela.title("Controle Financeiro")

centerAlign()
atualizar_layout()

# Saldo
saldo_fixPos = Label(tela, text=f"R${conta.saldo:.2f}", font=("Courier New", 14, "bold"),
                     justify="right", bg="#474963", fg="black", relief="ridge", bd=10)
saldo_fixPos.place(x=0, y=0)


# Entrada
valor_entry = Entry(tela, width=9, font=("Heveltica", 13), fg="#4d4d4d", 
                    relief="ridge", bd=10)
valor_entry.place(relx=0.5, rely=0.25, anchor="center")
saldo_fixPos.lift()
entryWid = valor_entry.winfo_reqwidth()

# Botão Depositar
depoButton = Button(tela, text="Depositar", font=("Arial", 10), relief="raised", bd=12, width=9,  command=conta.valueDepo)
depoButton.place(relx=0.5, rely=0.37, anchor="center")

# Botão Retirar
retirarButton = Button(tela, text="Retirar", font=("Arial", 10), relief="raised", bd=12, width=9,  command=conta.valueWith)
retirarButton.place(relx=0.5, rely=0.5, anchor="center")

# Botão de Cédulas
moneyOrig = Image.open("/storage/emulated/0/Pictures/Eraser/dinheiro.png")
moneyResize = moneyOrig.resize((100, 100))
moneyImg = ImageTk.PhotoImage(moneyResize)

moneyCount = Button(tela, image=moneyImg, command=Counter, width=97, height=98, justify="center", relief="ridge", bd=10, bg="#bbbcc7", padx=20, pady=10)
moneyCount.place(x=entryWid-(moneyCount.winfo_reqwidth()) + 18, rely=0.25, anchor="e")

# Label de informações
saldo_label = Label(tela, text=f"Digite um valor:", relief="sunken", bd=10)
saldo_label.place(rely=0.10, relx=0.5, anchor="n")

# Iniciar o loop da interface gráfica
tela.mainloop()
