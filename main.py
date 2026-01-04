from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.core.window import Window

# KV DİLİ - ARAYÜZ TASARIMI (Bu kısım Android'de asla çökmez)
KV = """
#:import get_color_from_hex kivy.utils.get_color_from_hex

<RoundedButton@Button>:
    background_normal: ''
    background_color: 0,0,0,0
    btn_color: get_color_from_hex('#66BB6A') # Varsayılan Yeşil
    color: 1,1,1,1
    font_size: '18sp'
    bold: True
    canvas.before:
        Color:
            rgba: root.btn_color if self.state == 'normal' else [c*0.8 for c in root.btn_color]
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [15,]

<CircleButton@Button>:
    background_normal: ''
    background_color: 0,0,0,0
    btn_color: get_color_from_hex('#66BB6A')
    color: 1,1,1,1
    font_size: '28sp'
    bold: True
    canvas.before:
        Color:
            rgba: root.btn_color if self.state == 'normal' else [c*0.8 for c in root.btn_color]
        RoundedRectangle:
            pos: self.pos
            size: self.size
            # Eni ve boyu ne olursa olsun tam yuvarlak yapar
            radius: [min(self.width, self.height) / 2,]

FloatLayout:
    # ARKA PLAN RENGİ (Krem/Bej)
    canvas.before:
        Color:
            rgba: get_color_from_hex('#FFFDE7')
        Rectangle:
            pos: self.pos
            size: self.size

    # 1. ORTADAKİ BÜYÜK BUTON
    CircleButton:
        id: main_btn
        text: "Başlat"
        size_hint: None, None
        size: 220, 220
        pos_hint: {'center_x': 0.5, 'center_y': 0.65}
        on_press: app.toggle_timer()

    # 2. SAYAÇ KUTUSU VE METNİ
    Label:
        id: time_label
        text: app.time_text
        font_size: '50sp'
        bold: True
        color: get_color_from_hex('#1B5E20') # Koyu Yeşil
        size_hint: None, None
        size: 240, 90
        pos_hint: {'center_x': 0.5, 'center_y': 0.40}
        
        # Kutunun Çizimi
        canvas.before:
            Color:
                rgba: get_color_from_hex('#E8F5E9') # Açık yeşil zemin
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [10,]
            Color:
                rgba: get_color_from_hex('#66BB6A') # Yeşil Çerçeve
            Line:
                rounded_rectangle: (self.x, self.y, self.width, self.height, 10)
                width: 2

    # 3. ALT KONTROL BUTONLARI (Kapsayıcı)
    BoxLayout:
        orientation: 'horizontal'
        spacing: 25
        size_hint: None, None
        width: 280
        height: 60
        pos_hint: {'center_x': 0.5, 'center_y': 0.20}

        RoundedButton:
            id: pause_btn
            text: "Duraklat"
            btn_color: get_color_from_hex('#FFA726') # Turuncu
            disabled: True
            opacity: 0.5
            on_press: app.toggle_pause()

        RoundedButton:
            id: reset_btn
            text: "Sıfırla"
            btn_color: get_color_from_hex('#8D6E63') # Kahve
            disabled: True
            opacity: 0.5
            on_press: app.reset_timer()
"""

class ForestFocusApp(App):
    time_text = StringProperty("00:00")
    
    def build(self):
        self.is_running = False
        self.is_paused = False
        self.elapsed_seconds = 0
        return Builder.load_string(KV)

    def toggle_timer(self):
        btn = self.root.ids.main_btn
        pause_btn = self.root.ids.pause_btn
        reset_btn = self.root.ids.reset_btn
        
        from kivy.utils import get_color_from_hex
        
        if not self.is_running:
            # BAŞLAT
            self.is_running = True
            self.is_paused = False
            
            btn.text = "Bitir"
            btn.btn_color = get_color_from_hex('#EF5350') # Kırmızı
            
            pause_btn.disabled = False
            pause_btn.opacity = 1
            pause_btn.text = "Duraklat"
            
            reset_btn.disabled = True
            reset_btn.opacity = 0.5
            
            Clock.schedule_interval(self.update_time, 1)
        else:
            # DURDUR
            self.stop_timer()

    def toggle_pause(self):
        pause_btn = self.root.ids.pause_btn
        reset_btn = self.root.ids.reset_btn
        from kivy.utils import get_color_from_hex
        
        if self.is_paused:
            # DEVAM ET
            self.is_paused = False
            pause_btn.text = "Duraklat"
            pause_btn.btn_color = get_color_from_hex('#FFA726')
            Clock.schedule_interval(self.update_time, 1)
        else:
            # DURAKLAT
            self.is_paused = True
            pause_btn.text = "Devam Et"
            pause_btn.btn_color = get_color_from_hex('#66BB6A')
            Clock.unschedule(self.update_time)
            reset_btn.disabled = False
            reset_btn.opacity = 1

    def stop_timer(self):
        self.is_running = False
        self.is_paused = False
        Clock.unschedule(self.update_time)
        
        btn = self.root.ids.main_btn
        pause_btn = self.root.ids.pause_btn
        reset_btn = self.root.ids.reset_btn
        from kivy.utils import get_color_from_hex
        
        btn.text = "Başlat"
        btn.btn_color = get_color_from_hex('#66BB6A')
        
        pause_btn.disabled = True
        pause_btn.opacity = 0.5
        pause_btn.text = "Duraklat"
        
        reset_btn.disabled = False
        reset_btn.opacity = 1

    def reset_timer(self):
        self.stop_timer()
        self.elapsed_seconds = 0
        self.update_display()
        
        reset_btn = self.root.ids.reset_btn
        reset_btn.disabled = True
        reset_btn.opacity = 0.5

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

if __name__ == '__main__':
    ForestFocusApp().run()
