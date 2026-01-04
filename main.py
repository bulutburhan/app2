from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Line
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# FOREST TEMASI: Arka plan "Krem/Bej" rengi
Window.clearcolor = get_color_from_hex('#FFFDE7')

class ForestRing(FloatLayout):
    def __init__(self, **kwargs):
        super(ForestRing, self).__init__(**kwargs)
        self.thickness = 25 
        self.circle_color = get_color_from_hex('#2E7D32') # Koyu Orman Yeşili
        self.bg_color = get_color_from_hex('#C8E6C9')     # Açık Yeşil İz
        self.angle_end = 0
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def set_seconds(self, seconds):
        # Saniye kolu mantığı: Her dakika bir tur atar
        current_second = seconds % 60
        percentage = current_second / 60.0
        self.angle_end = percentage * 360
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # 1. Arkadaki İz (Açık Yeşil)
            Color(rgba=self.bg_color)
            Line(circle=(self.center_x, self.center_y, 110), width=self.thickness)
            
            # 2. Dolan Halka (Orman Yeşili)
            Color(rgba=self.circle_color)
            Line(circle=(self.center_x, self.center_y, 110, 0, self.angle_end), 
                 width=self.thickness, cap='round')

class ForestFocusApp(App):
    def build(self):
        self.title = "Forest Focus"
        self.is_running = False
        self.elapsed_seconds = 0
        
        # Ana Taşıyıcı
        root = FloatLayout()
        
        # 1. MOTİVASYON SÖZÜ
        self.quote_label = Label(text="Toprağa bir tohum ek.", font_size='20sp', bold=True, 
                      color=get_color_from_hex('#558B2F'), # Zeytin Yeşili
                      pos_hint={'center_x': 0.5, 'top': 0.90}, size_hint=(None, None))
        root.add_widget(self.quote_label)

        # 2. YEŞİL HALKA
        self.ring = ForestRing(size_hint=(None, None), size=(300, 300),
                                pos_hint={'center_x': 0.5, 'center_y': 0.6})
        root.add_widget(self.ring)
        
        # 3. SÜRE (Halkanın içinde)
        self.time_label = Label(text="00:00", font_size='60sp', bold=True,
                                color=get_color_from_hex('#1B5E20'), # Çok Koyu Yeşil
                                pos_hint={'center_x': 0.5, 'center_y': 0.6})
        root.add_widget(self.time_label)

        # 4. BUTONLAR
        btn_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(0.85, None), height=75,
                               pos_hint={'center_x': 0.5, 'y': 0.1})
        
        # SIFIRLA BUTONU (Vazgeç)
        self.reset_btn = Button(text="Vazgeç", font_size='18sp', bold=True,
                                background_normal='', 
                                background_color=get_color_from_hex('#A1887F'), # Açık Kahve
                                color=get_color_from_hex('#FFFFFF'))
        self.reset_btn.bind(on_press=self.reset_timer)
        
        # BAŞLAT BUTONU (Dik)
        self.main_btn = Button(text="Dik", font_size='22sp', bold=True,
                               background_normal='', 
                               background_color=get_color_from_hex('#66BB6A'), # Canlı Yeşil
                               color=get_color_from_hex('#FFFFFF'))
        self.main_btn.bind(on_press=self.toggle_timer)
        
        btn_layout.add_widget(self.reset_btn)
        btn_layout.add_widget(self.main_btn)
        
        root.add_widget(btn_layout)
        
        return root

    def toggle_timer(self, instance):
        if not self.is_running:
            # BAŞLAT
            self.is_running = True
            self.main_btn.text = "Duraklat"
            self.main_btn.background_color = get_color_from_hex('#FFA726') # Turuncu
            
            self.reset_btn.disabled = True
            self.reset_btn.opacity = 0.6
            self.quote_label.text = "Ağacın büyüyor..."
            
            Clock.schedule_interval(self.update_time, 1)
        else:
            # DURAKLAT
            self.is_running = False
            self.main_btn.text = "Devam Et"
            self.main_btn.background_color = get_color_from_hex('#66BB6A') # Yeşil
            
            self.reset_btn.disabled = False
            self.reset_btn.opacity = 1
            self.quote_label.text = "Dinleniyorsun."
            
            Clock.unschedule(self.update_time)

    def reset_timer(self, instance):
        # SIFIRLA
        self.is_running = False
        Clock.unschedule(self.update_time)
        self.elapsed_seconds = 0
        
        self.update_display()
        
        self.main_btn.text = "Dik"
        self.main_btn.background_color = get_color_from_hex('#66BB6A')
        self.quote_label.text = "Toprağa bir tohum ek."
        
        self.ring.set_seconds(0)

    def update_time(self, dt):
        self.elapsed_seconds += 1
        self.update_display()

    def update_display(self):
        m, s = divmod(self.elapsed_seconds, 60)
        h, m = divmod(m, 60)
        
        if h > 0:
            self.time_label.text = f'{h:02}:{m:02}:{s:02}'
            self.time_label.font_size = '45sp'
        else:
            self.time_label.text = f'{m:02}:{s:02}'
            self.time_label.font_size = '60sp'
        
        self.ring.set_seconds(self.elapsed_seconds)

if __name__ == '__main__':
    ForestFocusApp().run()
