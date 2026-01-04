from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty
from kivy.core.window import Window

# Manuel Renk Tanımları (Import hatası riskini sıfıra indirmek için)
# Bu renkler senin beğendiğin Forest renklerinin Python karşılığıdır.
COLOR_CREAM = (1.0, 0.99, 0.90, 1.0)      # Arkaplan
COLOR_GREEN = (0.4, 0.73, 0.41, 1.0)      # Başlat Butonu
COLOR_RED = (0.93, 0.32, 0.31, 1.0)       # Bitir Butonu
COLOR_ORANGE = (1.0, 0.65, 0.15, 1.0)     # Duraklat
COLOR_BROWN = (0.55, 0.43, 0.39, 1.0)     # Sıfırla / Vazgeç
COLOR_TEXT = (0.10, 0.37, 0.12, 1.0)      # Koyu Yeşil Yazı
COLOR_BOX_BG = (0.91, 0.96, 0.91, 1.0)    # Sayaç Kutusu Zemin

KV_CODE = """
<MainScreen>:
    # 1. ARKA PLAN (Krem Rengi)
    canvas.before:
        Color:
            rgba: 1.0, 0.99, 0.90, 1.0 
        Rectangle:
            pos: self.pos
            size: self.size

    # 2. ORTADAKİ BÜYÜK YUVARLAK BUTON
    Button:
        id: main_btn
        text: "Başlat"
        font_size: '32sp'
        bold: True
        color: 1, 1, 1, 1
        size_hint: None, None
        size: 220, 220
        pos_hint: {'center_x': 0.5, 'center_y': 0.65}
        background_normal: ''
        background_color: 0,0,0,0  # Standart arka planı kapat
        on_press: root.toggle_timer()
        
        canvas.before:
            Color:
                rgba: self.btn_color if self.state == 'normal' else (self.btn_color[0]*0.8, self.btn_color[1]*0.8, self.btn_color[2]*0.8, 1)
            # Ellipse: En güvenli yuvarlak çizme yöntemidir. Çökmez.
            Ellipse:
                pos: self.pos
                size: self.size

    # 3. SAYAÇ KUTUSU
    Label:
        id: time_label
        text: root.time_text
        font_size: '55sp'
        bold: True
        color: 0.10, 0.37, 0.12, 1.0
        size_hint: None, None
        size: 260, 100
        pos_hint: {'center_x': 0.5, 'center_y': 0.40}
        
        canvas.before:
            Color:
                rgba: 0.91, 0.96, 0.91, 1.0
            Rectangle:
                pos: self.pos
                size: self.size
            Color:
                rgba: 0.4, 0.73, 0.41, 1.0
            Line:
                rectangle: (self.x, self.y, self.width, self.height)
                width: 2

    # 4. ALT BUTONLAR (Kare/Dikdörtgen)
    BoxLayout:
        orientation: 'horizontal'
        spacing: 30
        size_hint: None, None
        width: 300
        height: 70
        pos_hint: {'center_x': 0.5, 'center_y': 0.20}

        # Duraklat Butonu
        Button:
            id: pause_btn
            text: "Duraklat"
            font_size: '20sp'
            bold: True
            background_normal: ''
            background_color: 0,0,0,0
            disabled: True
            opacity: 0.5
            on_press: root.toggle_pause()
            
            canvas.before:
                Color:
                    rgba: (1.0, 0.65, 0.15, 1.0) if self.state == 'normal' else (0.8, 0.5, 0.1, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size

        # Sıfırla Butonu
        Button:
            id: reset_btn
            text: "Sıfırla"
            font_size: '20sp'
            bold: True
            background_normal: ''
            background_color: 0,0,0,0
            disabled: True
            opacity: 0.5
            on_press: root.reset_timer()
            
            canvas.before:
                Color:
                    rgba: (0.55, 0.43, 0.39, 1.0) if self.state == 'normal' else (0.4, 0.3, 0.3, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size
"""

from kivy.uix.floatlayout import FloatLayout

class MainScreen(FloatLayout):
    time_text = StringProperty("00:00")
    
    # Butonun dinamik rengi (Kivy Property olarak tanımladık, hata vermez)
    btn_color = ListProperty(COLOR_GREEN)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_running = False
        self.is_paused = False
        self.elapsed_seconds = 0

    def toggle_timer(self):
        if not self.is_running:
            # BAŞLAT
            self.is_running = True
            self.is_paused = False
            
            # Görsel Güncellemeler
            self.ids.main_btn.text = "Bitir"
            self.btn_color = COLOR_RED # Kırmızıya geç
            
            self.ids.pause_btn.disabled = False
            self.ids.pause_btn.opacity = 1
            self.ids.pause_btn.text = "Duraklat"
            
            self.ids.reset_btn.disabled = True
            self.ids.reset_btn.opacity = 0.5
            
            Clock.schedule_interval(self.update_time, 1)
        else:
            # BİTİR (DURDUR)
            self.stop_timer()

    def toggle_pause(self):
        if self.is_paused:
            # DEVAM ET
            self.is_paused = False
            self.ids.pause_btn.text = "Duraklat"
            Clock.schedule_interval(self.update_time, 1)
        else:
            # DURAKLAT
            self.is_paused = True
            self.ids.pause_btn.text = "Devam Et"
            Clock.unschedule(self.update_time)
            
            self.ids.reset_btn.disabled = False
            self.ids.reset_btn.opacity = 1

    def stop_timer(self):
        self.is_running = False
        self.is_paused = False
        Clock.unschedule(self.update_time)
        
        self.ids.main_btn.text = "Başlat"
        self.btn_color = COLOR_GREEN # Yeşile dön
        
        self.ids.pause_btn.disabled = True
        self.ids.pause_btn.opacity = 0.5
        self.ids.pause_btn.text = "Duraklat"
        
        self.ids.reset_btn.disabled = False
        self.ids.reset_btn.opacity = 1

    def reset_timer(self):
        self.stop_timer()
        self.elapsed_seconds = 0
        self.update_display()
        
        self.ids.reset_btn.disabled = True
        self.ids.reset_btn.opacity = 0.5

    def update_time(self, dt):
        self.elapsed_seconds += 1
        self.update_display()

    def update_display(self):
        m, s = divmod(self.elapsed_seconds, 60)
        h, m = divmod(m, 60)
        if h > 0:
            self.time_text = f'{h:02}:{m:02}:{s:02}'
        else:
            self.time_text = f'{m:02}:{s:02}'

class ForestApp(App):
    def build(self):
        return Builder.load_string(KV_CODE)

if __name__ == '__main__':
    ForestApp().run()
