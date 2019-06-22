# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior  
from kivy.uix.image import Image 
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty
from kivy.core.audio import SoundLoader
from kivy.uix.popup import Popup

import threading
import time
import random

lock = threading.Lock()

Config.read("config.ini")
Builder.load_file('kv_files/fabrica.kv')
Builder.load_file('kv_files/loja.kv')
Builder.load_file('kv_files/configuracao.kv')
Builder.load_file('kv_files/aminoacido.kv')


######################## ###BEGIN## ######################## 
######################## FABRICA.PY ########################

class Informativo(Popup):
	info_src = StringProperty()



class Close_Fabrica(Popup):
	pass

class Fabrica (Popup):
		
	
	def definir_aminoacido(self, codon):
		if (codon in ["UUC", "UUU"]):
			return "fen"
		elif (codon in ["UUA", "UUG", "CUU", "CUC", "CUA", "CUG"]):
			return "leu"
		elif (codon in ["AUU", "AUC", "AUA"]):
			return "ile"
		elif (codon in ["AUG"]): #códon de iniciação
			return "met"
		elif (codon in ["GUU", "GUC", "GUA", "GUG"]):
			return "val"
		elif (codon in ["UCU", "UCC", "UCA", "UCG", "AGU", "AGC"]):
			return "ser"
		elif (codon in ["CCU", "CCC", "CCA", "CCG"]):
			return "pro"
		elif (codon in ["ACU", "ACC", "ACA", "ACG"]):
			return "tre"
		elif (codon in ["GCU", "GCC", "GCA", "GCG"]):
			return "ala"
		elif (codon in ["UAU", "UAC"]):
			return "tir"
		elif (codon in ["UAA", "UAG", "UGA"]):
			return "stop"
		elif (codon in ["CAU", "CAC"]):
			return "his"
		elif (codon in ["CAA", "CAG"]):
			return "gln"
		elif (codon in ["AAU", "AAC"]):
			return "asn"
		elif (codon in ["AAA", "AAG"]):
			return "lis"
		elif (codon in ["GAU", "GAC"]):
			return "asp"
		elif (codon in ["GAA", "GAG"]):
			return "glu"
		elif (codon in ["UGU", "UGC"]):
			return "cis"
		elif (codon == "UGG"):
			return "trp"
		elif (codon in ["CGU", "CGC", "CGA", "CGG", "AGA", "AGG"]):
			return "arg" 
		elif (codon in ["GGU", "GGC", "GGA", "GGG"]):
			return "gli"
			
	
	def define_color(self, letra):
		if (letra=='A'):
			return [1, .4784313725490196, .4198078431372449, 1]
		elif (letra=='G'):
			return [1, .7294117647058824, .0088888888888889, 1]
		elif (letra=='C'):
			return [ .7882352941176471, .8745098039215686, .3490196078431373, 1]
		else: #letrsa==u
			return [.5098039215686275, .7411764705882353, 1, 1]
	
	def load_fabrica(self):
		
		qtd = self.config.get("codon")['v']
		
		self.ids.grid_fabrica.qtd_codons = qtd
		nucleotideos = ['A', 'U', 'C', 'G']
		
		primeiro = random.choice(nucleotideos) 
		segundo = random.choice(nucleotideos) 
		terceiro = random.choice(nucleotideos)  
		
		self.ids.p.text = primeiro
		self.ids.p.background_color = self.define_color(primeiro)
		self.ids.s.text = segundo
		self.ids.s.background_color = self.define_color(segundo)
		self.ids.t.text = terceiro
		self.ids.t.background_color = self.define_color(terceiro)
		
		self.ids.resp_p.text = ''
		self.ids.resp_s.text = ''
		self.ids.resp_t.text = ''
	
	def conferir_resposta(self):
		if (App.get_running_app().root.config.get("son")['v'] == 1):
			App.get_running_app().root.sound_button.play()
		dic_nucleotideos = {'A': 'U', 'G': 'C', 'U': 'A', 'C': 'G'}
		
		resp_p = self.ids.resp_p.text.upper().strip()
		resp_s = self.ids.resp_s.text.upper().strip()
		resp_t = self.ids.resp_t.text.upper().strip()
		
		if(dic_nucleotideos[self.ids.p.text] == resp_p and dic_nucleotideos[self.ids.s.text] == resp_s and dic_nucleotideos[self.ids.t.text] == resp_t):
			codon = resp_p + resp_s + resp_t
			aminoacido = self.definir_aminoacido(codon)
			
			qtd_codon = self.config.get("codon")['v']-1
			self.config.put("codon",v = qtd_codon)
			
			if (aminoacido == 'stop'):
				self.pops.info_src = "Image/stop.png"
				
			else:
				estabilidade = self.config.get("estabilidade")['v']
				if (estabilidade < 100):
					
					self.config.put("estabilidade",v = estabilidade+5)
					App.get_running_app().root.ids.pb.value = estabilidade+5
					
				qtd_aa = self.aminoacidos.get(aminoacido)['qtd']+1
				name_ = self.aminoacidos.get(aminoacido)['name']
				App.get_running_app().root.children[0].children[3].children[self.dic_aa[aminoacido]].aa_qtd = qtd_aa
				
				
				if (self.aminoacidos.get(aminoacido)['status'] == 0):
					
					
					App.get_running_app().root.children[0].children[3].children[self.dic_aa[aminoacido]].img_src = "Image/Monstros/"+aminoacido+".png"
					App.get_running_app().root.children[0].children[3].children[self.dic_aa[aminoacido]].aa_name = name_
					App.get_running_app().root.children[0].children[3].children[self.dic_aa[aminoacido]].create_thread()
					
					
				self.pops.info_src = "Image/Parabens/"+aminoacido+".png"
				
				self.aminoacidos.put(aminoacido, name = name_, status = 1, qtd = qtd_aa, moedas = self.aminoacidos.get(aminoacido)['moedas'], price = self.aminoacidos.get(aminoacido)['price'])
			
			if (qtd_codon == 0):
					self.dismiss()
					pops= Informativo()
					pops.info_src = "Image/attention.png"
					pops.open()
			else:
				self.load_fabrica()
		else:
			self.pops.info_src = "Image/OPS1.png"
			
			self.ids.resp_p.text = ''
			self.ids.resp_s.text = ''
			self.ids.resp_t.text = ''
			estabilidade = self.config.get("estabilidade")['v']
			self.config.put("estabilidade",v = estabilidade-15)
			App.get_running_app().root.ids.pb.value = estabilidade-15
			
			if (App.get_running_app().root.ids.pb.value < 15):
				self.dismiss()
				self.pops_close.open()
				App.get_running_app().root.call_load()
			
		self.pops.open()
	
	def __init__(self, **kwargs):
		super(Fabrica, self).__init__(**kwargs)
		self.dic_aa = {"val": 19, "leu": 18, "trp": 17, "pro":16, "ile":15, "met":14, "fen":13, "ala":12, "tre":11, "gli":10, "asn":9, "gln":8, "cis":7, "ser":6, "tir":5, "arg":4, "his":3, "lis":2, "glu":1, "asp":0}
		self.aminoacidos = App.get_running_app().root.storage_aminoacidos
		self.config = App.get_running_app().root.config
		self.pops= Informativo()
		self.pops_close = Close_Fabrica()
		self.load_fabrica()


######################## ####END### ######################## 
######################## FABRICA.PY ########################


######################## #BEGIN# ######################## 
######################## LOJA.PY ########################

class Informativo_aminoacido(Popup):
	info_src = StringProperty()

class ImageButton(ButtonBehavior, Image):  
	pass
	

class Item (GridLayout):
	
	def upgrade_aminoacido(self, aminoacido):
		moedas = self.config.get("moeda")['v']
		price_ = self.aminoacidos.get(aminoacido)['price']

		if (moedas >= price_):
			name_ = self.aminoacidos.get(aminoacido)['name']
			moedas_ = int(self.aminoacidos.get(aminoacido)['moedas']+3)
			qtd_ = self.aminoacidos.get(aminoacido)['qtd']

			self.config.put("moeda", v = moedas-price_)
			App.get_running_app().root.ids.conj_moedas.qtd-=price_
		
			self.aminoacidos.put(aminoacido, name = name_, status = 1, qtd = qtd_, moedas = moedas_, price = price_*2)
		
			App.get_running_app().root.children[0].children[3].children[self.dic_aa[aminoacido]].moedas_s = moedas_
			App.get_running_app().root.children[0].children[3].children[self.dic_aa[aminoacido]].aa_price = price_
		
			self.ids.item_button.text = str(price_*2)+'\nUPGRADE'
			self.ids.item_button.value = price_*2
			self.ids.item_desc.text = name_+'\n'+str(qtd_)+' Exemplares\n'+str(moedas_)+' Moedas/s' 
		else:
			self.pops_nao_possui.info_src = "Image/nao_possui.png"
			self.pops_nao_possui.open()
		

	
	def buy_codon(self):
		moedas = self.config.get("moeda")['v']
		preco = self.config.get("preco_codon")['v']
		if (moedas >= preco):
			lock.acquire()
			moedas = self.config.get("moeda")['v']
			self.config.put("moeda", v = moedas-preco)
			lock.release()
			
			App.get_running_app().root.ids.conj_moedas.qtd-=preco
			codons = self.config.get("codon")['v'] + 1
			preco = int (preco*1.12)
			self.config.put("codon", v = codons)
			self.config.put("preco_codon", v = preco)
			self.ids.item_desc.text = 'Codon\n'+str(codons)+' Exemplares\n'
			self.ids.item_button.text = str(preco)+'\nBUY'
		else:
			self.pops_nao_possui.info_src = "Image/nao_possui.png"
			self.pops_nao_possui.open()
		
	def press_button(self, referencia):
		
		if (App.get_running_app().root.config.get("son")['v'] == 1):
			App.get_running_app().root.sound_button.play()
		
		if (referencia == 'codon'):
			self.buy_codon()
		else:
			self.upgrade_aminoacido(referencia)
	
	def open_informativo(self):
		self.pops.info_src = "Image/Monstros/painel/"+self.ids.item_button.referencia+".png"
		self.pops.open()
	
	def __init__(self, text='', image_path='', value=0, button_txt='', referencia='', **kwargs):
		super(Item, self).__init__(**kwargs)
		self.dic_aa = {"val": 19, "leu": 18, "trp": 17, "pro":16, "ile":15, "met":14, "fen":13, "ala":12, "tre":11, "gli":10, "asn":9, "gln":8, "cis":7, "ser":6, "tir":5, "arg":4, "his":3, "lis":2, "glu":1, "asp":0}
		self.ids.item_desc.text = text
		self.ids.item_image.source = image_path
		self.ids.item_button.text = button_txt
		self.ids.item_button.value = value
		self.ids.item_button.referencia = referencia
		self.config = App.get_running_app().root.config
		self.aminoacidos = App.get_running_app().root.storage_aminoacidos
		self.pops= Informativo_aminoacido()
		self.pops_nao_possui = Informativo()
		

class Loja (Popup):
	
	
	
	def load_loja(self):
		aminoacidos = App.get_running_app().root.storage_aminoacidos
		aa = ["val", "leu", "trp", "pro", "ile", "met", "fen", "ala", "tre", "gli", "asn", "gln", "cis", "ser", "tir", "arg", "his", "lis", "glu", "asp"] 
		
		path = 'Image/dna-icon.png'
		name = "Codon"
		qtd = self.config.get("codon")['v']
		price = int(self.config.get("preco_codon")['v'])
		desc = name+'\n'+str(qtd)+' Exemplares\n'
		button_text = str(price)+'\nBUY'
		self.ids['loja'].add_widget(Item(text = desc, image_path=path, value=price, button_txt=button_text, referencia='codon'))
		
		for a in aa:
			if (aminoacidos.get(a)['status'] == 1):
				path ='Image/info/'+a+'.png'
				name = aminoacidos.get(a)['name']
				qtd = aminoacidos.get(a)['qtd']
				moedas = aminoacidos.get(a)['moedas']
				price = aminoacidos.get(a)['price']
				desc = name+'\n'+str(qtd)+' Exemplares\n'+str(moedas)+' Energia/s'
				button_text = str(price)+'\nUPGRADE'
				self.ids['loja'].add_widget(Item(text = desc, image_path=path, value=price, button_txt=button_text, referencia=a))
		
	
	def __init__(self, **kwargs):
		super(Loja, self).__init__(**kwargs)
		self.config = App.get_running_app().root.config
		self.load_loja()


######################## ##END# ######################## 
######################## LOJA.PY ########################

######################## #####BEGIN##### ######################## 
######################## CONFIGURACAO.PY ########################

class Configuracao (Popup):
	
	def if_active_music(self, state):
		if state:
			self.config.put("musica", v = 1)
			App.get_running_app().root.sound.play()
		else:
			self.config.put("musica", v = 0)
			App.get_running_app().root.sound.stop()
	
	def if_active_son(self, state):
		if state:
			self.config.put("son", v = 1)
			
		else:
			self.config.put("son", v = 0)
	def open_tutorial(self):
		tutorial = Tutorial()
		tutorial.open()
			
	
	def __init__(self, **kwargs):
		super(Configuracao, self).__init__(**kwargs)
		self.config = App.get_running_app().root.config
		
		if (self.config.get("musica")['v'] == 1):
			self.ids.music_box.active = True
		else:
			self.ids.music_box.active = False
		
		if (self.config.get("son")['v'] == 1):
			self.ids.son_box.active = True
		else:
			self.ids.son_box.active = False


######################## ######END###### ######################## 
######################## CONFIGURACAO.PY ######################## 


######################## ####BEGIN#### ######################## 
######################## AMINOACIDO.PY ######################## 

class Tutorial (Popup):	
	back = StringProperty()
	
	def change(self):
		if (self.back == 'Image/Tutorial/01.png'):
			self.back = 'Image/Tutorial/02.png'
		elif (self.back == 'Image/Tutorial/02.png'):
			self.back = 'Image/Tutorial/03.png'
		elif (self.back == 'Image/Tutorial/03.png'):
			self.back = 'Image/Tutorial/04.png'
		elif (self.back == 'Image/Tutorial/04.png'):
			self.back = 'Image/Tutorial/05.png'
		elif (self.back == 'Image/Tutorial/05.png'):
			self.back = 'Image/Tutorial/06.png'
		elif (self.back == 'Image/Tutorial/06.png'):
			self.back = 'Image/Tutorial/07.png'
		elif (self.back == 'Image/Tutorial/07.png'):
			self.back = 'Image/Tutorial/08.png'
		elif (self.back == 'Image/Tutorial/08.png'):
			self.back = 'Image/Tutorial/09.png'
		elif (self.back == 'Image/Tutorial/09.png'):
			self.back = 'Image/Tutorial/10.png'
		elif (self.back == 'Image/Tutorial/10.png'):
			self.back = 'Image/Tutorial/11.png'
		elif (self.back == 'Image/Tutorial/11.png'):
			self.back = 'Image/Tutorial/12.png'
		elif (self.back == 'Image/Tutorial/12.png'):
			self.back = 'Image/Tutorial/13.png'
		else:
			self.dismiss()

	
	def __init__(self, **kwargs):
		super(Tutorial, self).__init__(**kwargs)
		self.back = 'Image/Tutorial/01.png'

class ImageButton(ButtonBehavior, Image):  
	pass

class Aminoacido(RelativeLayout):
	img_src = StringProperty()
	aa_name = StringProperty()
	moedas_s = NumericProperty
	aa_qtd = NumericProperty
	aa_price = NumericProperty
	
	def create_thread(self):
		t = threading.Thread(target=self.call_animate_coin)
		t.daemon = True
		t.start()
	
	
	def call_animate_coin(self):
		time.sleep(random.uniform(0, 2))
		Clock.unschedule(self.animate_coin)
		Clock.schedule_interval(self.animate_coin, 2)
	
	def animate_coin(self, dt):
		pos_x = self.ids.image.x
		pos_y = self.ids.image.y
		
		size= self.ids.label_animate.font_size
		
		moedas = self.moedas_s * self.aa_qtd
		self.ids.label_animate.text = '+'+str(moedas)
		


		self.ids.label_animate.pos=(pos_x, pos_y)
		self.ids.label_animate.color= [0,0,0,1]
		def hide_label(self,w): w.color= [0,0,0,0]
		animation = Animation(pos=(pos_x+5, pos_y+50), duration=0.25)
		animation += Animation(pos=(pos_x-10, pos_y+100), duration=0.25)
		animation += Animation(pos=(pos_x+10, pos_y+150), duration=0.25)
		animation += Animation(pos=(pos_x-10, pos_y+200), duration=0.25)
		animation.bind(on_complete=hide_label)
		
		amino_animation = Animation(pos_hint= {'center_x': 0.5, 'center_y': 0.5}, duration=0.2)
		amino_animation += Animation(pos_hint= {'center_x': 0.5, 'center_y': 0.6}, duration=0.4)
		amino_animation += Animation(pos_hint= {'center_x': 0.5, 'center_y': 0.5}, duration=0.4)
		
		animation.start(self.ids.label_animate)
		amino_animation.start(self.ids.image)

		lock.acquire()
		App.get_running_app().root.ids.conj_moedas.qtd+=moedas
		total = App.get_running_app().root.ids.conj_moedas.qtd
		App.get_running_app().root.config.put('moeda',v = total)
		lock.release()

	

	
	def animate(self, pos_x, pos_y):
		if (self.aa_name != "???"):

			if (App.get_running_app().root.config.get("son")['v'] == 1):
				App.get_running_app().root.sound_button.play()

			if (self.img_src == 'Image/Monstros/'+self.id+'.png'):
				self.img_src = 'Image/Monstros/estrutura/'+self.id+'.png'
			else:
				self.img_src = 'Image/Monstros/'+self.id+'.png'

			moedas = self.moedas_s * self.aa_qtd
			text_ = "+"+str(moedas)
			self.animat = Label(pos=(pos_x, pos_y-100), color= [0,0,0,1], text=text_)
			self.add_widget(self.animat)

			animation = Animation(pos=(pos_x, pos_y+100), duration=1)
			animation.bind(on_complete=(lambda x, y: self.remove_widget(y)))

			lock.acquire()
			App.get_running_app().root.ids.conj_moedas.qtd+=moedas
			total = App.get_running_app().root.ids.conj_moedas.qtd
			App.get_running_app().root.config.put('moeda',v = total)
			lock.release()
			
			animation.start(self.animat)


	def __init__(self, text='', image_path='', moedas=0, price=0, n=0, id_='', **kwargs):
		super(Aminoacido, self).__init__(**kwargs)
		self.aa_name = text
		self.img_src = image_path
		self.ids.label_animate.color= [0,0,0,0]
		self.moedas_s = moedas
		self.aa_price= price
		self.aa_qtd= n
		self.id= id_
		if (text != '???'):
			self.create_thread()

class BoardAminoacido(RelativeLayout):
	
	def call_load(self):
		t_load_estabilidade = threading.Thread(target=self.load_estabilidade)
		t_load_estabilidade.daemon = True
		t_load_estabilidade.start()
	
	def load_estabilidade(self):
		v_ = self.ids.pb.value
		self.config.put("carregando",v = 1)
		for i in range(100-v_):
			time.sleep(2)
			v_+=1
			self.ids.pb.value = v_
			self.config.put("estabilidade",v = v_)
		self.config.put("carregando",v = 0)
	
	def open_loja(self):
		self.config.put("first", v = 0)
		pops=Loja()
		pops.open()
	
	def open_configuracao(self):
		self.config.put("first", v = 0)
		pops=Configuracao()
		pops.open()
	
	def open_fabrica(self):
		self.config.put("first", v = 0)

		if (self.config.get("carregando")['v'] == 1):
			pops=Close_Fabrica()
			pops.open()
		else:
			if (self.config.get("codon")['v'] == 0):
				pops=Informativo()
				pops.texto = "Seus codons acabaram. Va ate a loja e compre alguns."
				pops.info_src = "Image/attention.png"
				pops.open()
			else:
				pops=Fabrica()
				pops.open()
			
	
	def load_aa(self):
		aa = ["val", "leu", "trp", "pro", "ile", "met", "fen", "ala", "tre", "gli", "asn", "gln", "cis", "ser", "tir", "arg", "his", "lis", "glu", "asp"] 
		
		for a in aa:
			if (self.storage_aminoacidos.get(a)['status'] == 0):
				path = 'Image/unknown/'+a+'.png'
				name = '???'
			else:
				path = 'Image/Monstros/'+a+'.png'
				name = self.storage_aminoacidos.get(a)['name']
			
			n = self.storage_aminoacidos.get(a)['qtd']
			moedas = self.storage_aminoacidos.get(a)['moedas']
			price = self.storage_aminoacidos.get(a)['price']
			
			x = self.ids['grid'].size[0]/4
			y = self.ids['grid'].size[1]/5
			
			amino = Aminoacido(text = name, image_path=path, moedas=moedas, price=price, id=a)
			
			self.ids['grid'].add_widget(Aminoacido(text = name, image_path=path, moedas=moedas, price=price, n=n, id_=a))
	
	def __init__(self, **kwargs):
		super(BoardAminoacido, self).__init__(**kwargs)
		
		
		self.config = JsonStore('BD/configuracao.json')
		self.storage_aminoacidos = JsonStore('BD/aminoacidos.json')
		self.ids.conj_moedas.qtd = self.config.get('moeda')['v']
		self.ids.pb.value = self.config.get("estabilidade")['v']
		
		if (self.config.get("carregando")['v'] == 1):
			self.call_load()
			
		self.load_aa()
		
		self.sound_button = SoundLoader.load('Music/click-01.wav')
		self.sound = SoundLoader.load('Music/Monkey-Island-Band_Looping.wav')
		self.sound.loop = True
		self.sound.volume = 0.8
		if (self.config.get("musica")['v'] == 1):
			self.sound.play()

######################## #####END##### ######################## 
######################## AMINOACIDO.PY ######################## 



game = BoardAminoacido()

class AminoacidoApp(App):

	def on_start(self):
		self.config = JsonStore('BD/configuracao.json')
		if (self.config.get("first")['v'] == 1):
			tutorial = Tutorial()
			tutorial.open()
		

	def build(self):
		return game

if __name__ == '__main__':
	AminoacidoApp().run()