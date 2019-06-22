from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.app import App
from kivy.storage.jsonstore import JsonStore

Builder.load_file('kv_files/configuracao.kv')

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
