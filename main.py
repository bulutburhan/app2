from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

# Renk Sabitleri
COLOR_CREAM = (1.0, 0.99, 0.90, 1.0)
COLOR_GREEN = (0.4, 0.73, 0.41, 1.0)
COLOR_RED = (0.93, 0.32, 0.31, 1.0)
COLOR_ORANGE = (1.0, 0.65, 0.15, 1.0)
COLOR_BROWN = (0.55, 0.43, 0.39, 1.0)

KV_CODE = """
<MainScreen>:
    # ARKA PLAN
    canvas.before:
        Color:
            rgba: 1.0, 0.99, 0.90, 1.0
        Rectangle:
            pos: self.pos
            size: self.size

    # 1. ORTADAKİ BÜYÜK YUVARLAK BUTON
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
        background_color: 0,0,0,0
        on_press: root.toggle_timer()
        
        canvas.before:
            # Rengi root (MainScreen) üzerinden alıyoruz
            Color:
                rgba: root.main_btn_color
            Ellipse:
                pos: self.pos
                size: self.size

    # 2. SAYAÇ KUTUSU
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

    # 3. ALT BUTONLAR
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
                    rgba: root.pause_btn_color
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
                    rgba: 0.55, 0.43, 0.39, 1.0
                Rectangle:
                    pos: self.pos
                    size: self.size
"""

class MainScreen(FloatLayout):
    time_text = StringProperty("00:00")
    
    # Renkleri burada tanımlıyoruz ki KV dosyası çökmesin
    main_btn_color = ListProperty(COLOR_GREEN)
    pause_btn_color = ListProperty(COLOR_ORANGE)

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
            
            self.ids.main_btn.text = "Bitir"
            self.main_btn_color = COLOR_RED # Kırmızıya dön
            
            self.ids.pause_btn.disabled = False
            self.ids.pause_btn.opacity = 1
            self.ids.pause_btn.text = "Duraklat"
            self.pause_btn_color = COLOR_ORANGE
            
            self.ids.reset_btn.disabled = True
            self.ids.reset_btn.opacity = 0.5
            
            Clock.schedule_interval(self.update_time, 1)
        else:
            # BİTİR
            self.stop_timer()

    def toggle_pause(self):
        if self.is_paused:
            # DEVAM ET
            self.is_paused = False
            self.ids.pause_btn.text = "Duraklat"
            self.pause_btn_color = COLOR_ORANGE
            Clock.schedule_interval(self.update_time, 1)
        else:
            # DURAKLAT
            self.is_paused = True
            self.ids.pause_btn.text = "Devam Et"
            self.pause_btn_color = COLOR_GREEN
            Clock.unschedule(self.update_time)
            
            self.ids.reset_btn.disabled = False
            self.ids.reset_btn.opacity = 1

    def stop_timer(self):
        self.is_running = False
        self.is_paused = False
        Clock.unschedule(self.update_time)
        
        self.ids.main_btn.text = "Başlat"
        self.main_btn_color = COLOR_GREEN
        
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
        # Tasarımı yükle
        Builder.load_string(KV_CODE)
        # VE EN ÖNEMLİSİ: Ana ekranı döndür (Siyah ekranı çözen kısım burası)
        return MainScreen()

if __name__ == '__main__':
    ForestApp().run()
