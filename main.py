import os
# --- PC İÇİN GÖRÜNTÜ AYARI ---
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Line
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# --- TELEFON GÖRÜNÜMÜ ---
Window.size = (400, 750)
Window.clearcolor = get_color_from_hex('#FFFFFF')

class SecondsRing(FloatLayout):
    def __init__(self, **kwargs):
        super(SecondsRing, self).__init__(**kwargs)
        self.thickness = 20
        self.circle_color = get_color_from_hex('#5856D6') # Indigo
        self.bg_color = get_color_from_hex('#F2F2F7')     # Gri İz
        self.angle_end = 0
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def set_seconds(self, seconds):
        # Her 60 saniyede bir tam tur atar (Saniye kolu mantığı)
        current_second = seconds % 60
        percentage = current_second / 60.0
        self.angle_end = percentage * 360
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # Arkadaki sabit gri halka
            Color(rgba=self.bg_color)
            Line(circle=(self.center_x, self.center_y, 120), width=self.thickness)
            
            # Öndeki dolan renkli halka
            Color(rgba=self.circle_color)
            Line(circle=(self.center_x, self.center_y, 120, 0, self.angle_end), 
                 width=self.thickness, cap='round')

class FocusApp(App):
    def build(self):
        self.title = "Kronometre"
        self.is_running = False
        self.elapsed_seconds = 0
        
        # --- ANA EKRAN ---
        root = FloatLayout()
        
        # 1. Başlık
        title = Label(text="Kronometre", font_size='28sp', bold=True, 
                      color=get_color_from_hex('#000000'),
                      pos_hint={'center_x': 0.5, 'top': 0.92}, size_hint=(None, None))
        root.add_widget(title)

        # 2. Halka (Ortada)
        self.ring = SecondsRing(size_hint=(None, None), size=(300, 300),
                                pos_hint={'center_x': 0.5, 'center_y': 0.55})
        root.add_widget(self.ring)
        
        # 3. Süre Yazısı (Halkanın İçinde)
        self.time_label = Label(text="00:00:00", font_size='50sp', bold=True,
                                color=get_color_from_hex('#000000'),
                                pos_hint={'center_x': 0.5, 'center_y': 0.55})
        root.add_widget(self.time_label)

        # 4. Butonlar (Yan Yana)
        btn_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(0.8, None), height=70,
                               pos_hint={'center_x': 0.5, 'y': 0.1})
        
        # Başlat / Duraklat Butonu
        self.main_btn = Button(text="Başlat", font_size='22sp', bold=True,
                               background_normal='', background_color=get_color_from_hex('#34C759'),
                               color=get_color_from_hex('#FFFFFF'))
        self.main_btn.bind(on_press=self.toggle_timer)
        
        # Sıfırla Butonu
        self.reset_btn = Button(text="Sıfırla", font_size='22sp', bold=True,
                                background_normal='', background_color=get_color_from_hex('#8E8E93'),
                                color=get_color_from_hex('#FFFFFF'))
        self.reset_btn.bind(on_press=self.reset_timer)
        
        btn_layout.add_widget(self.reset_btn)
        btn_layout.add_widget(self.main_btn)
        
        root.add_widget(btn_layout)
        
        return root

    def toggle_timer(self, instance):
        if not self.is_running:
            # Başlat
            self.is_running = True
            self.main_btn.text = "Duraklat"
            self.main_btn.background_color = get_color_from_hex('#FF9500') # Turuncu
            self.reset_btn.disabled = True # Çalışırken sıfırlanmasın
            self.reset_btn.opacity = 0.5
            Clock.schedule_interval(self.update_time, 1)
        else:
            # Duraklat
            self.is_running = False
            self.main_btn.text = "Devam Et"
            self.main_btn.background_color = get_color_from_hex('#34C759') # Yeşil
            self.reset_btn.disabled = False
            self.reset_btn.opacity = 1
            Clock.unschedule(self.update_time)

    def reset_timer(self, instance):
        # Sıfırla
        self.is_running = False
        Clock.unschedule(self.update_time)
        self.elapsed_seconds = 0
        
        # Arayüzü Sıfırla
        self.update_display()
        self.main_btn.text = "Başlat"
        self.main_btn.background_color = get_color_from_hex('#34C759')
        
        self.ring.set_seconds(0)

    def update_time(self, dt):
        self.elapsed_seconds += 1
        self.update_display()

    def update_display(self):
        # Saat : Dakika : Saniye formatı
        m, s = divmod(self.elapsed_seconds, 60)
        h, m = divmod(m, 60)
        
        if h > 0:
            self.time_label.text = f'{h:02}:{m:02}:{s:02}'
            self.time_label.font_size = '40sp' # Sığması için küçült
        else:
            self.time_label.text = f'{m:02}:{s:02}'
            self.time_label.font_size = '50sp'
            
        # Halkayı güncelle (Saniye animasyonu)
        self.ring.set_seconds(self.elapsed_seconds)

if __name__ == '__main__':
    FocusApp().run()
