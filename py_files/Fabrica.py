from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
import random
from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App
from kivy.properties import StringProperty


Builder.load_file('kv_files/fabrica.kv')

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
		
		resp_p = self.ids.resp_p.text.upper()
		resp_s = self.ids.resp_s.text.upper()
		resp_t = self.ids.resp_t.text.upper()
		
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
