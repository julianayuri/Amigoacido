from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior  
from kivy.uix.image import Image 
from kivy.properties import StringProperty

Builder.load_file('kv_files/loja.kv')

class Informativo_aminoacido(Popup):
	info_src = StringProperty()

class ImageButton(ButtonBehavior, Image):  
	pass
	

class Item (GridLayout):
	
	def upgrade_aminoacido(self, aminoacido):
		name_ = self.aminoacidos.get(aminoacido)['name']
		price_ = self.aminoacidos.get(aminoacido)['price']*2
		moedas_ = int(self.aminoacidos.get(aminoacido)['moedas']+3)
		qtd_ = self.aminoacidos.get(aminoacido)['qtd']
		
		self.aminoacidos.put(aminoacido, name = name_, status = 1, qtd = qtd_, moedas = moedas_, price = price_)
		
		App.get_running_app().root.children[0].children[3].children[self.dic_aa[aminoacido]].moedas_s = moedas_
		App.get_running_app().root.children[0].children[3].children[self.dic_aa[aminoacido]].aa_price = price_
		#App.get_running_app().root.children[0].children[3].clear_widgets()
		#App.get_running_app().root.load_aa()
		
		self.ids.item_button.text = str(price_)+'\nUPGRADE'
		self.ids.item_button.value = price_
		self.ids.item_desc.text = name_+'\n'+str(qtd_)+' Exemplares\n'+str(moedas_)+' Moedas/s' 
		

	
	def buy_codon(self):
		moedas = self.config.get("moeda")['v']
		if (moedas >= 500):
			self.config.put("moeda", v = moedas-500)
			codons = self.config.get("codon")['v'] + 1
			self.config.put("codon", v = codons)
			self.ids.item_desc.text = "Codon\n"+str(codons)+' Exemplares\n'
		else:
			print("você não possui moedas para comprar")
		
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
		

class Loja (Popup):
	
	
	
	def load_loja(self):
		aminoacidos = App.get_running_app().root.storage_aminoacidos
		aa = ["val", "leu", "trp", "pro", "ile", "met", "fen", "ala", "tre", "gli", "asn", "gln", "cis", "ser", "tir", "arg", "his", "lis", "glu", "asp"] 
		
		path = 'image/dna-icon.png'
		name = "Codon"
		qtd = self.config.get("codon")['v']
		price = 500
		desc = name+'\n'+str(qtd)+' Exemplares\n'
		button_text = str(price)+'\nBUY'
		self.ids['loja'].add_widget(Item(text = desc, image_path=path, value=price, button_txt=button_text, referencia='codon'))
		
		for a in aa:
			if (aminoacidos.get(a)['status'] == 1):
				path ='image/Monstros/'+a+'.png'
				name = aminoacidos.get(a)['name']
				qtd = aminoacidos.get(a)['qtd']
				moedas = aminoacidos.get(a)['moedas']
				price = aminoacidos.get(a)['price']
				desc = name+'\n'+str(qtd)+' Exemplares\n'+str(moedas)+' Moedas/s'
				button_text = str(price)+'\nUPGRADE'
				self.ids['loja'].add_widget(Item(text = desc, image_path=path, value=price, button_txt=button_text, referencia=a))
		
	
	def __init__(self, **kwargs):
		super(Loja, self).__init__(**kwargs)
		self.config = App.get_running_app().root.config
		self.load_loja()
