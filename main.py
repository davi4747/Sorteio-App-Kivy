# -*- coding: utf-8 -*-
# Made by Davi Sousa, Twitter: @davi4747, Instagram: @davisousa_80, Github Profile: github.com/davi4747

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.core.window import Window
from random import choice
from datetime import date, datetime
import json

class Gerenciador(ScreenManager):
    pass

class Main_menu(Screen):

    def on_pre_enter(self, *args):
        Window.bind(on_keyboard=self.voltar)

    def voltar(self, window, key, *args):
        if key == 27:
            self.confirmacao()
            return True

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard=self.voltar)

    def confirmacao(self):
        box = BoxLayout(orientation='vertical', spacing=dp(3))
        atencao = Image(source='att.png')
        botoes = BoxLayout(padding=dp(4), spacing=dp(3))
        pop = Popup(title='Você quer mesmo sair?', content=box, size_hint=(None, None), size=(dp(250), dp(180)))
        sim = Botaor(text='SIM', on_release=App.get_running_app().stop)
        nao = Botaor(text='NÃO', on_release=pop.dismiss)
        botoes.add_widget(sim)
        botoes.add_widget(nao)
        box.add_widget(atencao)
        box.add_widget(botoes)
        pop.open()

class Botaor(ButtonBehavior, Label):

    cor1 = ListProperty([0.1, 0.1, 0.1, 1])
    cor2 = ListProperty([0.4, 0.4, 0.4, 1])

    def on_press(self):
        self.cor1, self.cor2 = self.cor2, self.cor1

    def on_release(self):
        self.cor1, self.cor2 = self.cor2, self.cor1

class Nomes(Screen):
    def __init__(self, **kwargs):
        super(Nomes, self).__init__()
        self.titulo = ''
        self.tipo = ''
        arquivo = open('lists.txt', 'r')
        arquivo2 = arquivo.read()
        if arquivo2 == '':
            self.lista_nomes_temp = []
            self.dic_listas = {}
            self.lista_titulos = []
            arquivo.close()
        else:
            self.lista_nomes_temp = []
            self.lista_titulos = []
            dic = json.loads(arquivo2)
            self.dic_listas = dic
            for c in self.dic_listas.keys():
                self.lista_titulos.append(c)
            arquivo.close()

    def on_pre_enter(self, *args):
        Window.bind(on_keyboard=self.voltar)

    def back(self):
        App.get_running_app().root.get_screen('menu_nomes').ids.participantes.text = '0 PARTICIPANTES:'
        self.ids.box_participantes.clear_widgets()
        self.lista_nomes_temp = []
        App.get_running_app().root.current = 'menu_principal'

    def voltar(self, window, key, *args):
        if key == 27:
            self.back()
            return True

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard=self.voltar)

    def confirmar_nome(self):
        if self.ids.text1.text == '':
            pass
        else:
            texto = self.ids.text1.text
            texto = texto.strip()
            self.lista_nomes_temp.append(texto)
            self.ids.box_participantes.add_widget(Participante(texto))
            self.ids.text1.text = ''
            q = len(self.lista_nomes_temp)
            aviso = str(q) + ' PARTICIPANTES:'
            App.get_running_app().root.get_screen('menu_nomes').ids.participantes.text = aviso

    def carregar(self):
        arquivo = open('lists.txt', 'r')
        arquivo2 = arquivo.read()
        if arquivo2 == '' or arquivo2 == '{}':
            box = BoxLayout(orientation='vertical', spacing=dp(4), padding=dp(6))
            pop = Popup(title='Listas Salvas', content=box, size_hint=(None, None), size=(dp(250), dp(180)))
            atencao = Image(source='att.png')
            box2 = BoxLayout(orientation='vertical', spacing=dp(3), padding=dp(5))
            aviso = Label(text='Não há lista salva!')
            box2.add_widget(atencao)
            box2.add_widget(aviso)
            botao = Botaor(text='OK', on_release=pop.dismiss)
            box2.add_widget(botao)
            box.add_widget(box2)
            pop.open()
            arquivo.close()
        else:
            self.ids.box_participantes.clear_widgets()
            App.get_running_app().root.get_screen('menu_nomes').ids.participantes.text = '0 PARTICIPANTES:'
            self.lista_nomes_temp = []
            App.get_running_app().root.current = 'load'
            self.lista_titulos = []
            self.abrirtxt()
            for c in self.lista_titulos:
                App.get_running_app().root.get_screen('load').ids.box_titulos.add_widget(Titulo(c))
            self.lista_titulos = []

    def recolocar(self):
        self.lista_titulos = []
        self.abrirtxt()
        for c in self.dic_listas[self.titulo]:
            self.lista_nomes_temp.append(c)
            self.ids.box_participantes.add_widget(Participante(c))
        self.lista_titulos = []
        App.get_running_app().root.get_screen('load').ids.box_titulos.clear_widgets()
        q = len(self.lista_nomes_temp)
        aviso = str(q) + ' PARTICIPANTES:'
        App.get_running_app().root.get_screen('menu_nomes').ids.participantes.text = aviso
        App.get_running_app().root.current = 'menu_nomes'

    def removert(self, titulo):
        self.lista_titulos = []
        self.abrirtxt()
        del self.dic_listas[titulo]
        self.lista_titulos = []
        dic = json.dumps(self.dic_listas)
        with open('lists.txt', 'w') as f:
            f.write(dic)
            f.close()


    def abrirtxt(self):
        arquivo = open('lists.txt', 'r')
        arquivo2 = arquivo.read()
        dic = json.loads(arquivo2)
        self.dic_listas = dic
        for c in dic.keys():
            self.lista_titulos.append(c)
        arquivo.close()

    def verificar(self):
        if len(self.lista_nomes_temp) <= 1:
            box = BoxLayout(orientation='vertical', spacing=dp(4), padding=dp(6))
            pop = Popup(title='Salvar Lista', content=box, size_hint=(None, None), size=(dp(250), dp(180)))
            atencao = Image(source='att.png')
            box2 = BoxLayout(orientation='vertical', spacing=dp(3), padding=dp(5))
            aviso = Label(text='Adicione ao menos 2 participantes!')
            box2.add_widget(atencao)
            box2.add_widget(aviso)
            botao = Botaor(text='OK', on_release=pop.dismiss)
            box2.add_widget(botao)
            box.add_widget(box2)
            pop.open()
        else:
            App.get_running_app().root.get_screen('edit').lista_temp = self.lista_nomes_temp
            App.get_running_app().root.get_screen('menu_nomes').ids.box_participantes.clear_widgets()
            App.get_running_app().root.get_screen('menu_nomes').ids.participantes.text = '0 PARTICIPANTES:'
            self.lista_nomes_temp = []
            App.get_running_app().root.current = 'edit'

    def salvar(self):
        try:
            self.abrirtxt()
        except:
            pass
        titulo = App.get_running_app().root.get_screen('edit').titulo
        self.lista_titulos = []
        self.titulo = titulo
        self.dic_listas[titulo] = App.get_running_app().root.get_screen('edit').lista_temp
        dic = json.dumps(self.dic_listas)
        with open('lists.txt', 'w') as f:
            f.write(dic)
        App.get_running_app().root.get_screen('edit').titulo = None
        App.get_running_app().root.get_screen('edit').ids.label_titulo.text = '---'
        App.get_running_app().root.current = 'menu_nomes'

class Load(Screen):
    def on_pre_enter(self, *args):
        Window.bind(on_keyboard=self.voltar)

    def back(self):
        self.ids.box_titulos.clear_widgets()
        App.get_running_app().root.current = 'menu_nomes'

    def voltar(self, window, key, *args):
        if key == 27:
            self.back()
            return True

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard=self.voltar)

class Edit(Screen):
    def __init__(self, **kwargs):
        super(Edit, self).__init__()
        self.titulo = ''
        self.lista_temp = None

    def on_pre_enter(self, *args):
        Window.bind(on_keyboard=self.voltar)

    def voltar(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'menu_nomes'
            return True

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard=self.voltar)

class Resultado(Screen):
    def __init__(self, **kwargs):
        super(Resultado, self).__init__()
        self.lista_temp = []
        self.lista_perm = None
        self.quantidade = 0

    def on_pre_enter(self, *args):
        Window.bind(on_keyboard=self.voltar)

    def back(self):
        self.ids.box_resultado.clear_widgets()
        self.lista_temp = []
        App.get_running_app().root.current = 'menu_principal'

    def voltar(self, window, key, *args):
        if key == 27:
            self.back()
            return True

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard=self.voltar)

    def preparar(self):
        if len(App.get_running_app().root.get_screen('menu_nomes').lista_nomes_temp) <= 1:
            box = BoxLayout(orientation='vertical', spacing=dp(4), padding=dp(6))
            pop = Popup(title='CONFIRMAR SORTEIO', content=box, size_hint=(None, None), size=(dp(250), dp(180)))
            atencao = Image(source='att.png')
            box2 = BoxLayout(orientation='vertical', spacing=dp(3), padding=dp(5))
            aviso = Label(text='Adicione ao menos 2 participantes!')
            box2.add_widget(atencao)
            box2.add_widget(aviso)
            botao = Botaor(text='OK', on_release=pop.dismiss)
            box2.add_widget(botao)
            box.add_widget(box2)
            pop.open()
        else:
            App.get_running_app().root.get_screen('menu_nomes').ids.box_participantes.clear_widgets()
            self.lista_perm = App.get_running_app().root.get_screen('menu_nomes').lista_nomes_temp
            App.get_running_app().root.get_screen('menu_nomes').lista_nomes_temp = []
            App.get_running_app().root.current = 'resultado'
            self.sortear()

    def grupos(self):
        if len(App.get_running_app().root.get_screen('menu_nomes').lista_nomes_temp) <= 2:
            box = BoxLayout(orientation='vertical', spacing=dp(4), padding=dp(6))
            pop = Popup(title='CONFIRMAR SORTEIO', content=box, size_hint=(None, None), size=(dp(250), dp(180)))
            atencao = Image(source='att.png')
            box2 = BoxLayout(orientation='vertical', spacing=dp(3), padding=dp(5))
            aviso = Label(text='Adicione ao menos 3 participantes!')
            box2.add_widget(atencao)
            box2.add_widget(aviso)
            botao = Botaor(text='OK', on_release=pop.dismiss)
            box2.add_widget(botao)
            box.add_widget(box2)
            pop.open()
        else:
            App.get_running_app().root.get_screen('menu_nomes').ids.box_participantes.clear_widgets()
            self.lista_perm = App.get_running_app().root.get_screen('menu_nomes').lista_nomes_temp
            App.get_running_app().root.get_screen('menu_nomes').lista_nomes_temp = []
            App.get_running_app().root.current = 'grupo'

    def sortear(self):
        if App.get_running_app().root.get_screen('menu_nomes').tipo == 'individual':
            for c in self.lista_perm:
                self.lista_temp.append(c)
            self.ids.box_resultado.clear_widgets()
            data = str(date.today())
            hor = datetime.today()
            calendario = {'01':'Janeiro', '02':'Fevereiro', '03':'Março', '04':'Abril', '05':'Maio', '06':'Junho', '07':'Julho',
                          '08':'Agosto', '09':'Setembro', '10':'Outubro', '11':'Novembro', '12':'Dezembro'}
            mensagem = 'Realizado em: ' + data[8:] + ' de ' + calendario[data[5:7]] + ' de ' + data[0:4] + ' às ' + \
                       '{:0>2}'.format(str(hor.hour)) + ':' + '{:0>2}'.format(str(hor.minute))
            App.get_running_app().root.get_screen('resultado').ids.label_top.text = mensagem
            cont = 0
            while not len(self.lista_temp) == 0:
                esc = choice(self.lista_temp)
                cont += 1
                colocado = str(cont) + ': ' + esc
                self.ids.box_resultado.add_widget(Sorteado(colocado))
                self.lista_temp.remove(esc)
            self.lista_temp = []
        else:
            self.sortearg()

    def sortearg(self):
        for c in self.lista_perm:
            self.lista_temp.append(c)
        self.ids.box_resultado.clear_widgets()
        data = str(date.today())
        hor = datetime.today()
        calendario = {'01':'Janeiro', '02':'Fevereiro', '03':'Março', '04':'Abril', '05':'Maio', '06':'Junho', '07':'Julho',
                      '08':'Agosto', '09':'Setembro', '10':'Outubro', '11':'Novembro', '12':'Dezembro'}
        mensagem = 'Realizado em: ' + data[8:] + ' de ' + calendario[data[5:7]] + ' de ' + data[0:4] + ' às ' + \
                   '{:0>2}'.format(str(hor.hour)) + ':' + '{:0>2}'.format(str(hor.minute))
        App.get_running_app().root.get_screen('resultado').ids.label_top.text = mensagem
        cont = 0
        while not len(self.lista_temp) == 0:
            if len(self.lista_temp) < int(App.get_running_app().root.get_screen('grupo').quantidade):
                restante = []
                while len(self.lista_temp) != 0:
                    for t in self.lista_temp:
                        restante.append(t)
                        self.lista_temp.remove(t)
                ordem = 'Grupo Restante:'
                self.ids.box_resultado.add_widget(Sorteadog(ordem, restante))
            else:
                esc = []
                for c in range(0, int(App.get_running_app().root.get_screen('grupo').quantidade)):
                    item = choice(self.lista_temp)
                    esc.append(item)
                    self.lista_temp.remove(item)
                cont += 1
                ordem = 'Grupo ' + str(cont) + ':'
                self.ids.box_resultado.add_widget(Sorteadog(ordem, esc))
        App.get_running_app().root.current = 'resultado'
        self.lista_temp = []

class Titulo(BoxLayout):
    def __init__(self, titulo, **kwargs):
        super(Titulo, self).__init__()
        self.ids.labelt.text = titulo

class Sorteado(BoxLayout):
    def __init__(self, texto, **kwargs):
        super(Sorteado, self).__init__()
        self.ids.sorteado.text = texto

class Sorteadog(BoxLayout):
    def __init__(self, ordem, escolhidos, **kwargs):
        super(Sorteadog, self).__init__()
        self.ids.ordem.text = ordem
        for c in escolhidos:
            self.ids.escolhidos.add_widget(Label(text=c, font_size=dp(18), size_hint_y=None, height=dp(28)))

class Participante(BoxLayout):
    def __init__(self, texto, **kwargs):
        super(Participante, self).__init__()
        self.ids.labelp.text = texto

class Numeros(Screen):

    def on_pre_enter(self, *args):
        Window.bind(on_keyboard=self.voltar)

    def voltar(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'menu_principal'
            return True

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard=self.voltar)

    def ok1(self):
        self.ids.number1.text = self.ids.text1.text.strip()
        self.ids.text1.text = ''

    def ok2(self):
        self.ids.number2.text = self.ids.text2.text.strip()
        self.ids.text2.text = ''

    def avisar(self):
        box = BoxLayout(orientation='vertical', spacing=dp(4), padding=dp(6))
        pop = Popup(title='VERIFICAR NÚMEROS', content=box, size_hint=(None, None), size=(dp(250), dp(180)))
        atencao = Image(source='att.png')
        box2 = BoxLayout(orientation='vertical', spacing=dp(3), padding=dp(5))
        aviso = Label(text='Digite apenas números!')
        box2.add_widget(atencao)
        box2.add_widget(aviso)
        botao = Botaor(text='OK', on_release=pop.dismiss)
        box2.add_widget(botao)
        box.add_widget(box2)
        pop.open()

    def sortear(self):
        try:
            numb1 = int(self.ids.number1.text.strip())
            numb2 = int(self.ids.number2.text.strip())
            if numb2 <= numb1:
                box = BoxLayout(orientation='vertical', spacing=dp(4), padding=dp(6))
                pop = Popup(title='VERIFICAR NÚMEROS', content=box, size_hint=(None, None), size=(dp(250), dp(180)))
                atencao = Image(source='att.png')
                box2 = BoxLayout(orientation='vertical', spacing=dp(3), padding=dp(5))
                aviso = Label(text='O segundo deve ser maior!')
                box2.add_widget(atencao)
                box2.add_widget(aviso)
                botao = Botaor(text='OK', on_release=pop.dismiss)
                box2.add_widget(botao)
                box.add_widget(box2)
                pop.open()
            else:
                data = str(date.today())
                hor = datetime.today()
                calendario = {'01': 'Janeiro', '02': 'Fevereiro', '03': 'Março', '04': 'Abril', '05': 'Maio', '06': 'Junho',
                              '07': 'Julho', '08': 'Agosto', '09': 'Setembro', '10': 'Outubro',
                              '11': 'Novembro', '12': 'Dezembro'}
                mensagem = 'Realizado em: ' + data[8:] + ' de ' + calendario[data[5:7]] + ' de ' + data[0:4] + ' às ' + '{:0>2}'.format(str(
                    hor.hour)) + ':' + '{:0>2}'.format(str(hor.minute))
                self.ids.label_aviso.text = mensagem
                resultado = choice(range(numb1, numb2 + 1))
                self.ids.label_resultado.text = str(resultado)
        except:
            self.avisar()

class Sobre(Screen):
    def on_pre_enter(self, *args):
        Window.bind(on_keyboard=self.voltar)

    def voltar(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'menu_principal'
            return True

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard=self.voltar)

class Grupo(Screen):
    def __init__(self, **kwargs):
        super(Grupo, self).__init__()
        self.quantidade = ''

    def on_pre_enter(self, *args):
        Window.bind(on_keyboard=self.voltar)

    def voltar(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'menu_nomes'
            return True

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard=self.voltar)

    def verificar(self):
        try:
            num = int(self.ids.text2.text.strip())
            for c in App.get_running_app().root.get_screen('resultado').lista_perm:
                App.get_running_app().root.get_screen('resultado').lista_temp.append(c)
            if num >= len(App.get_running_app().root.get_screen('resultado').lista_temp):
                box = BoxLayout(orientation='vertical', spacing=dp(4), padding=dp(6))
                pop = Popup(title='VERIFICAR NÚMEROS', content=box, size_hint=(None, None), size=(dp(250), dp(180)))
                atencao = Image(source='att.png')
                box2 = BoxLayout(orientation='vertical', spacing=dp(3), padding=dp(5))
                aviso = Label(text='Digite um número menor que\na quantidade de participantes!')
                box2.add_widget(atencao)
                box2.add_widget(aviso)
                botao = Botaor(text='OK', on_release=pop.dismiss)
                box2.add_widget(botao)
                box.add_widget(box2)
                pop.open()
                App.get_running_app().root.get_screen('resultado').lista_temp = []
            else:
                self.ids.quantidade.text = str(num)
                self.quantidade = str(num)
                self.ids.text2.text = self.ids.quantidade.text
                App.get_running_app().root.get_screen('resultado').lista_temp = []
        except:
            App.get_running_app().root.get_screen('numeros').avisar()

class Sorteio(App):
    def build(self):
        return Gerenciador()

Sorteio().run()
