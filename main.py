from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Line, RoundedRectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# NOT: Window.clearcolor ayarını buradan kaldırdık, build() içine aldık.
# Bu sayede Android "Window daha hazır değil" hatası vermeyecek.

# --- ÖZEL SINIFLAR (GÜVENLİ HALE GETİRİLDİ) ---

class SafeRoundedButton(Button):
    def __init__(self, **kwargs):
        super(SafeRoundedButton, self).__init__(**kwargs)
        self.background_normal = '' 
        self.background_color = (0, 0, 0, 0)
        self.btn_color = kwargs.get('bg_color', get_color_from_hex('#66BB6A'))
        self.radius = kwargs.get('radius', [15,])
        
        # KRİTİK DÜZELTME: Çizimi hemen yapma, ekran hazır olana kadar bekle
        self.bind(pos=self.update_canvas, size=self.update_canvas, state=self.update_canvas)
        Clock.schedule_once(self.update_canvas, 0)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            current_color = self.btn_color
            if self.state == 'down':
                current_color = [c * 0.8 for c in self.btn_color]
            
            Color(rgba=current_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)

class SafeCircleButton(Button):
    def __init__(self, **kwargs):
        super(SafeCircleButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.btn_color = kwargs.get('bg_color', get_color_from_hex('#66BB6A'))
        
        self.bind(pos=self.update_canvas, size=self.update_canvas, state=self.update_canvas)
        Clock.schedule_once(self.update_canvas, 0)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            current_color = self.btn_color
            if self.state == 'down':
                current_color = [c * 0.8 for c in self.btn_color]
            
            Color(rgba=current_color)
            radius = min(self.width, self.height) / 2
            # Çap 0 ise çizim yapma (Hata önleyici)
            if radius > 0:
                RoundedRectangle(pos=self.pos, size=self.size, radius=[radius,])

class SafeTimerLabel(Label):
    def __init__(self, **kwargs):
        super(SafeTimerLabel, self).__init__(**kwargs)
        self.font_size = '50sp'
        self.bold = True
        self.color = get_color_from_hex('#1B5E20')
        
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        Clock.schedule_once(self.update_canvas, 0)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=get_color_from_hex('#E8F5E9'))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[10,])
            Color(rgba=get_color_from_hex('#66BB6A'))
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 10), width=2)

# --- ANA UYGULAMA ---

class ForestFocusApp(App):
    def build(self):
        # KRİTİK: Rengi burada ayarlıyoruz
        Window.clearcolor = get_color_from_hex('#FFFDE7')
        
        self.title = "Forest Timer"
        self.is_running = False
        self.is_paused = False
        self.elapsed_seconds = 0
        
        root = FloatLayout()
        
        # 1. BAŞLAT BUTONU
        self.main_btn = SafeCircleButton(
            text="Başlat", 
            font_size='28sp', 
            bold=True,
            color=get_color_from_hex('#FFFFFF'),
            bg_color=get_color_from_hex('#66BB6A'),
            size_hint=(None, None), 
            size=(220, 220),
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )
        self.main_btn.bind(on_press=self.toggle_timer)
        root.add_widget(self.main_btn)
        
        # 2. SAYAÇ KUTUSU
        self.time_label = SafeTimerLabel(
            text="00:00", 
            size_hint=(None, None), 
            size=(240, 90),
            pos_hint={'center_x': 0.5, 'center_y': 0.40}
        )
        root.add_widget(self.time_label)

        # 3. KONTROL BUTONLARI
        btn_layout = BoxLayout(
            orientation='horizontal', 
            spacing=25, 
            size_hint=(None, None), 
            width=280, 
            height=60,
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        
        self.pause_btn = SafeRoundedButton(
            text="Duraklat", 
            font_size='18sp', 
            bold=True,
            color=get_color_from_hex('#FFFFFF'),
            bg_color=get_color_from_hex('#FFA726')
        )
        self.pause_btn.bind(on_press=self.toggle_pause)
        self.pause_btn.disabled = True
        self.pause_btn.opacity = 0.5
        
        self.reset_btn = SafeRoundedButton(
            text="Sıfırla", 
            font_size='18sp', 
            bold=True,
            color=get_color_from_hex('#FFFFFF'),
            bg_color=get_color_from_hex('#8D6E63')
        )
        self.reset_btn.bind(on_press=self.reset_timer)
        self.reset_btn.disabled = True
        self.reset_btn.opacity = 0.5
        
        btn_layout.add_widget(self.pause_btn)
        btn_layout.add_widget(self.reset_btn)
        root.add_widget(btn_layout)
        
        return root

    def toggle_timer(self, instance):
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            
            self.main_btn.text = "Bitir"
            self.main_btn.btn_color = get_color_from_hex('#EF5350')
            self.main_btn.update_canvas()
            
            self.pause_btn.disabled = False
            self.pause_btn.opacity = 1
            self.pause_btn.text = "Duraklat"
            
            self.reset_btn.disabled = True
            self.reset_btn.opacity = 0.5
            
            Clock.schedule_interval(self.update_time, 1)
        else:
            self.stop_timer()

    def toggle_pause(self, instance):
        if self.is_paused:
            self.is_paused = False
            self.pause_btn.text = "Duraklat"
            self.pause_btn.btn_color = get_color_from_hex('#FFA726')
            self.pause_btn.update_canvas()
            Clock.schedule_interval(self.update_time, 1)
        else:
            self.is_paused = True
            self.pause_btn.text = "Devam Et"
            self.pause_btn.btn_color = get_color_from_hex('#66BB6A')
            self.pause_btn.update_canvas()
            Clock.unschedule(self.update_time)
            self.reset_btn.disabled = False
            self.reset_btn.opacity = 1

    def stop_timer(self):
        self.is_running = False
        self.is_paused = False
        Clock.unschedule(self.update_time)
        
        self.main_btn.text = "Başlat"
        self.main_btn.btn_color = get_color_from_hex('#66BB6A')
        self.main_btn.update_canvas()
        
        self.pause_btn.disabled = True
        self.pause_btn.opacity = 0.5
        self.pause_btn.text = "Duraklat"
        
        self.reset_btn.disabled = False
        self.reset_btn.opacity = 1

    def reset_timer(self, instance):
        self.stop_timer()
        self.elapsed_seconds = 0
        self.update_display()
        self.reset_btn.disabled = True
        self.reset_btn.opacity = 0.5

    def update_time(self, dt):
        self.elapsed_seconds += 1
        self.update_display()

    def update_display(self):
        m, s = divmod(self.elapsed_seconds, 60)
        h, m = divmod(m, 60)
        
        if h > 0:
            self.time_label.text = f'{h:02}:{m:02}:{s:02}'
        else:
            self.time_label.text = f'{m:02}:{s:02}'

if __name__ == '__main__':
    ForestFocusApp().run()
