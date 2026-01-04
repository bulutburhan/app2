from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# KV DİLİ: Arayüz çizim kuralları burada tanımlanır.
# Kivy bu kuralları okur ve ekran hazır olduğunda güvenle çizer.
KV_CODE = """
#:import get_color_from_hex kivy.utils.get_color_from_hex

# Yuvarlak Köşeli Kare Buton Tanımı (Duraklat/Sıfırla için)
<RoundedButton@Button>:
    background_normal: ''
    background_color: 0,0,0,0
    btn_color: get_color_from_hex('#66BB6A') # Varsayılan renk
    font_size: '18sp'
    bold: True
    color: 1, 1, 1, 1
    canvas.before:
        Color:
            # Tıklanınca rengi koyulaştır (Opaklığı değiştirerek)
            rgba: self.btn_color if self.state == 'normal' else [c * 0.8 for c in self.btn_color]
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [15,]

# Tam Yuvarlak Buton Tanımı (Başlat için)
<CircleButton@Button>:
    background_normal: ''
    background_color: 0,0,0,0
    btn_color: get_color_from_hex('#66BB6A')
    font_size: '28sp'
    bold: True
    color: 1, 1, 1, 1
    canvas.before:
        Color:
            rgba: self.btn_color if self.state == 'normal' else [c * 0.8 for c in self.btn_color]
        RoundedRectangle:
            pos: self.pos
            size: self.size
            # Genişlik ve yüksekliğin en küçüğüne göre tam daire yap
            radius: [min(self.width, self.height) / 2.0,]

FloatLayout:
    # Arka Plan Rengi
    canvas.before:
        Color:
            rgba: get_color_from_hex('#FFFDE7') # Krem Rengi
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
        color: get_color_from_hex('#1B5E20') # Koyu Yeşil Yazı
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

    # 3. ALT BUTONLAR (Yan Yana)
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
    # Ekranda değişen metni Kivy'ye bildiriyoruz
    time_text = StringProperty("00:00")
    
    def build(self):
        self.is_running = False
        self.is_paused = False
        self.elapsed_seconds = 0
        # KV kodunu güvenli bir şekilde yükle
        return Builder.load_string(KV_CODE)

    def toggle_timer(self):
        # KV dosyasındaki elemanlara erişim
        btn = self.root.ids.main_btn
        pause_btn = self.root.ids.pause_btn
        reset_btn = self.root.ids.reset_btn
        
        if not self.is_running:
            # BAŞLATMA MANTIĞI
            self.is_running = True
            self.is_paused = False
            
            btn.text = "Bitir"
            btn.btn_color = get_color_from_hex('#EF5350') # Kırmızıya dön
            
            pause_btn.disabled = False
            pause_btn.opacity = 1
            pause_btn.text = "Duraklat"
            
            reset_btn.disabled = True
            reset_btn.opacity = 0.5
            
            Clock.schedule_interval(self.update_time, 1)
        else:
            # DURDURMA MANTIĞI
            self.stop_timer()

    def toggle_pause(self):
        pause_btn = self.root.ids.pause_btn
        reset_btn = self.root.ids.reset_btn
        
        if self.is_paused:
            # DEVAM ET
            self.is_paused = False
            pause_btn.text = "Duraklat"
            pause_btn.btn_color = get_color_from_hex('#FFA726') # Turuncu
            Clock.schedule_interval(self.update_time, 1)
        else:
            # DURAKLAT
            self.is_paused = True
            pause_btn.text = "Devam Et"
            pause_btn.btn_color = get_color_from_hex('#66BB6A') # Yeşil
            Clock.unschedule(self.update_time)
            
            # Duraklatınca sıfırlamaya izin ver
            reset_btn.disabled = False
            reset_btn.opacity = 1

    def stop_timer(self):
        self.is_running = False
        self.is_paused = False
        Clock.unschedule(self.update_time)
        
        btn = self.root.ids.main_btn
        pause_btn = self.root.ids.pause_btn
        reset_btn = self.root.ids.reset_btn
        
        btn.text = "Başlat"
        btn.btn_color = get_color_from_hex('#66BB6A') # Yeşile dön
        
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
