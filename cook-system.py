from msilib.schema import Class
import os
from tkinter import font
from typing import List
import Banco
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import date
import time

tv=ttk.Treeview
SystemMenu=Tk()
SystemMenu.title('Cook System')
SystemMenu.geometry('350x300')

def data():
    hoje = date.today()
    data = hoje.strftime('%d/%m/%Y')
    return data
    
lHora=Label(SystemMenu, text=update_clock(), bg='#dde')
lHora.place(x=120, y=5, width=100, height=30)

def PedidoLogin():
    lg=Tk()
    lg.title('ADMIN')
    lg.geometry('250x200')
    lg.configure(background='#dde')
    lg.bind("<Escape>", lambda x: lg.destroy())
    
    def logar():
        vLogin=Login.get()
        vSenha=Senha.get()
        try:
            Banco.cursor.execute("SELECT * FROM funcionarios WHERE nome='"+vLogin+"' AND codigo='"+vSenha+"'")
            if Banco.cursor.fetchone() is not None:
                Banco.cursor.execute("SELECT * FROM funcionarios WHERE nome='"+vLogin+"' AND codigo='"+vSenha+"'")
                Banco.cursor.fetchone()
                messagebox.showinfo(title='SUCESSO', message='Login realizado com sucesso!')
                lg.destroy()

                def Pedido():
                    lP=Tk()
                    lP.title('FAÇA SEU PEDIDO')
                    lP.geometry('600x720')
                    lP.configure(background='#dde')
                    lP.bind("<Escape>", lambda x: lP.destroy())



                    def popular():
                            tvEstoque.delete(*tvEstoque.get_children())
                            vquery="SELECT * FROM produtos order by nome"
                            prods=Banco.dql(vquery)
                            for i in prods:
                                tvEstoque.insert("", "end", values=i)

                    def carrinho():
                        try:
                            linhaSelecionada=tvEstoque.selection()[0]
                            vCodigo=tvEstoque.item(linhaSelecionada, 'values')[0]
                            vNome=tvEstoque.item(linhaSelecionada, 'values')[1]
                            vItens = bQuantidade.get()
                            vValor = tvEstoque.item(linhaSelecionada, 'values')[3]
                            tvCarrinho.insert("", "end", values=(vCodigo, vNome, vItens, vValor))
                        except:
                            messagebox.showerror(title='ERRO 101', message='Não foi possível adicionar ao carrinho')

                    def remover():
                        try:
                            linhaSelecionada=tvCarrinho.selection()[0]
                            tvCarrinho.delete(linhaSelecionada)
                        except:
                            messagebox.showerror(title='ERRO 103', message='Não foi possível remover')

                    def vender():
                        try:
                            for i in tvCarrinho.get_children():
                                vCodigo=tvCarrinho.item(i, 'values')[0]
                                vQuantidade=tvCarrinho.item(i, 'values')[2]
                                Banco.cursor.execute("UPDATE produtos SET quantidade = quantidade-'"+vQuantidade+"' WHERE codigo='"+vCodigo+"'")
                                Banco.cursor.execute("CREATE TABLE IF NOT EXISTS pedidos (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, setor TEXT, data TEXT, cod TEXT, itens TEXT, qnt TEXT)")
                            vData=data()
                            Banco.cursor.execute("INSERT INTO pedidos (setor, data, cod, itens, qnt) values ('"+vData+"', '"+tvCarrinho.item(i, 'values')[0]+"','"+tvCarrinho.item(i, 'values')[1]+"', '"+tvCarrinho.item(i, 'values')[2]+"')")
                            messagebox.showinfo(title='SUCESSO', message='Pedido realizado com sucesso!')
                            Banco.banco.commit()
                            tvCarrinho.delete(*tvCarrinho.get_children())
                        except:
                            messagebox.showerror(title='ERRO 106', message='Não foi possível fazer o pedido')


                    tvEstoque=ttk.Treeview(lP, columns=('Codigo', 'Nome', 'Quantidade', 'Valor'), show='headings')
                    tvEstoque.column('Codigo', minwidth=0,width=25)
                    tvEstoque.column('Nome', minwidth=0,width=100)
                    tvEstoque.column('Quantidade', minwidth=0,width=25)
                    tvEstoque.column('Valor', minwidth=0,width=25)
                    tvEstoque.heading('Codigo', text='Código')
                    tvEstoque.heading('Nome', text='Produto')
                    tvEstoque.heading('Quantidade', text='Quantidade')
                    tvEstoque.heading('Valor', text='Valor')
                    tvEstoque.pack()
                    popular()
                    tvEstoque.place(x=0, y=370, width=600, height=150)

                    tvCarrinho=ttk.Treeview(lP, columns=('Codigo', 'Nome', 'Quantidade', 'Valor'), show='headings')
                    tvCarrinho.column('Codigo', minwidth=0,width=25)
                    tvCarrinho.column('Nome', minwidth=0,width=100)
                    tvCarrinho.column('Quantidade', minwidth=0,width=25)
                    tvCarrinho.column('Valor', minwidth=0,width=25)
                    tvCarrinho.heading('Codigo', text='Código')
                    tvCarrinho.heading('Nome', text='Produto')
                    tvCarrinho.heading('Quantidade', text='Quantidade')
                    tvCarrinho.heading('Valor', text='Valor')
                    tvCarrinho.pack()
                    tvCarrinho.place(x=0, y=520, width=600, height=100)

                    bAtualizar=Button(lP, text='Att (F1)', width=8, command=hora)
                    bAtualizar.place(x=100, y=100, width=100, height=50)

                    bQuantidade=Entry(lP)
                    bQuantidade.insert(0, '1')
                    bQuantidade.place(x=20, y=625, width=60, height=50)

                    bRemover=Button(lP, text='Remover (F2)', width=8, command=remover)
                    lP.bind("<F2>", lambda x: remover())
                    bRemover.place(x=220, y=625, width=100, height=50)

                    bCarrinho=Button(lP, text='Adicionar (F1)', width=8, command=lambda:[carrinho(),data()])
                    lP.bind("<F1>", lambda x:[carrinho(),data()])
                    bCarrinho.place(x=100, y=625, width=100, height=50)

                    bVender=Button(lP, text='Finalizar (F8)', width=8, command=lambda:[vender(),popular()])
                    lP.bind("<F8>", lambda x:[vender(),popular()])
                    bVender.place(x=440, y=625, width=100, height=50)
                Pedido()

            else:
                messagebox.showinfo(title='ERRO', message='Login ou senha incorretos!')
        except:
            print('Erro ao logar')

    vLogin=StringVar()
    vSenha=StringVar()
    lbLogin=Label(lg, text='Login:', bg='#dde')
    lbLogin.place(x=50, y=10)
    Login=Entry(lg, textvariable=vLogin)
    Login.place(x=50, y=30, width=150)
    lbSenha=Label(lg, text='Senha:', bg='#dde')
    lbSenha.place(x=50, y=60)
    Senha=Entry(lg, textvariable=vSenha, show='*')
    Senha.place(x=50, y=80, width=150)
    bLogar=Button(lg, text='Logar', command=logar)
    lg.bind("<Return>", lambda x: logar())
    bLogar.place(x=50, y=110, width=150)
    lg.mainloop()

bPedidos=Button(SystemMenu, text='Pedir (F1)', width=8, command=PedidoLogin)
bPedidos.place(x=15, y=5, width=100, height=30)

SystemMenu.mainloop()
