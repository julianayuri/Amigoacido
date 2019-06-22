from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior  
from kivy.uix.image import Image 
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from py_files import Configuracao
from py_files import Loja
from py_files import Fabrica
from kivy.animation import Animation
from kivy.uix.label import Label
import threading
from kivy.clock import Clock
from kivy.app import App
from kivy.properties import StringProperty, NumericProperty
import time
import random
from kivy.core.audio import SoundLoader
Builder.load_file('kv_files/aminoacido.kv')



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
		self.ids.label_animate.text = "+"+str(moedas)
		


		self.ids.label_animate.pos=(pos_x, pos_y)
		self.ids.label_animate.color= [0,0,0,1]
		def hide_label(self,w): w.color= [0,0,0,0]; w.font_size = size
		animation = Animation(pos=(pos_x, pos_y+80), duration=1)
		animation &= Animation(font_size = size*1.8)
		animation.bind(on_complete=hide_label)
		
		amino_animation = Animation(pos_hint= {'center_x': 0.5, 'center_y': 0.5}, duration=0.2)
		amino_animation += Animation(pos_hint= {'center_x': 0.5, 'center_y': 0.6}, duration=0.4)
		amino_animation += Animation(pos_hint= {'center_x': 0.5, 'center_y': 0.5}, duration=0.4)
		
		animation.start(self.ids.label_animate)
		amino_animation.start(self.ids.image)

		App.get_running_app().root.ids.conj_moedas.qtd+=moedas
		total = App.get_running_app().root.ids.conj_moedas.qtd
		App.get_running_app().root.config.put('moeda',v = total)
	
	def animate(self, pos_x, pos_y):
		if (self.aa_name != "unknown"):
			if (App.get_running_app().root.config.get("son")['v'] == 1):
				App.get_running_app().root.sound_button.play()
			moedas = self.moedas_s * self.aa_qtd
			text_ = "+"+str(moedas)
			self.animat = Label(pos=(pos_x, pos_y-50), color= [0,0,0,1], text=text_)
			self.add_widget(self.animat)

			animation = Animation(pos=(pos_x, pos_y+20), duration=1)
			animation.bind(on_complete=(lambda x, y: self.remove_widget(y)))
			
			App.get_running_app().root.ids.conj_moedas.qtd+=moedas
			total = App.get_running_app().root.ids.conj_moedas.qtd
			App.get_running_app().root.config.put('moeda',v = total)
			
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
		if (text != 'unknown'):
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
			time.sleep(5)
			v_+=1
			self.ids.pb.value = v_
			self.config.put("estabilidade",v = v_)
		self.config.put("carregando",v = 0)
	
	def open_loja(self):
		pops=Loja.Loja()
		pops.open()
	
	def open_configuracao(self):
		pops=Configuracao.Configuracao()
		pops.open()
	
	def open_fabrica(self):
		if (self.config.get("carregando")['v'] == 1):
			pops=Fabrica.Close_Fabrica()
			pops.open()
		else:
			if (self.config.get("codon")['v'] == 0):
				pops=Fabrica.Informativo()
				pops.texto = "Seus codons acabaram. Va ate a loja e compre alguns."
				pops.info_src = "Image/attention.png"
				pops.open()
			else:
				pops=Fabrica.Fabrica()
				pops.open()
			
	
	def load_aa(self):
		aa = ["val", "leu", "trp", "pro", "ile", "met", "fen", "ala", "tre", "gli", "asn", "gln", "cis", "ser", "tir", "arg", "his", "lis", "glu", "asp"] 
		
		for a in aa:
			if (self.storage_aminoacidos.get(a)['status'] == 0):
				path = "Image/interrogacao.png"
				name = 'unknown'
			else:
				path = 'image/Monstros/'+a+'.png'
				name = self.storage_aminoacidos.get(a)['name']
			
			n = self.storage_aminoacidos.get(a)['qtd']
			moedas = self.storage_aminoacidos.get(a)['moedas']
			price = self.storage_aminoacidos.get(a)['price']
			
			x = self.ids['grid'].size[0]/4
			y = self.ids['grid'].size[1]/5
			
			amino = Aminoacido(text = name, image_path=path, moedas=moedas, price=price, id=a)
			
			self.ids['grid'].add_widget(Aminoacido(text = name, image_path=path, moedas=moedas, price=price, n=n, id_=a))
		print(self.children[0].children[3].children[0].id)
	
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
		self.sound = SoundLoader.load('Music/Misty-Bog_Looping.mp3')
		self.sound.loop = True
		if (self.config.get("musica")['v'] == 1):
			self.sound.play()
		
		
		

