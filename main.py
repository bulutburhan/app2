from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.graphics import Color, Line, Rectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from plyer import notification
import random

# Arkaplan rengini beyaza yakın gri yapalım
Window.clearcolor = get_color_from_hex('#F2F2F7')

class CircularProgressBar(Label):
    def __init__(self, **kwargs):
        super(CircularProgressBar, self).__init__(**kwargs)
        self.thickness = 25
        self.circle_color = get_color_from_hex('#5856D6') # Indigo rengi
        self.bg_color = get_color_from_hex('#E5E5EA')     # Gri halka
        self.angle_end = 360
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def set_value(self, current, total):
        # Yüzdelik hesapla
        if total > 0:
            percentage = current / total
            self.angle_end = percentage * 360
            self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # 1. Gri Arkaplan Halkası
            Color(rgba=self.bg_color)
            Line(circle=(self.center_x, self.center_y, min(self.width, self.height)/2 - self.thickness), 
                 width=self.thickness)
            
            # 2. İlerleme Halkası (Indigo)
            Color(rgba=self.circle_color)
            Line(circle=(self.center_x, self.center_y, min(self.width, self.height)/2 - self.thickness, 0, self.angle_end), 
                 width=self.thickness, cap='round')

class FocusApp(App):
    def build(self):
        self.title = "Odaklan"
        self.messages = [
            "Güzel elini çenenden çek",
            "Ellerin için daha güzel bir yer seç",
            "El, el, el, el! Odaklan!",
            "Dik dur ve ekrana bak.",
            "Hayallerin seni bekliyor, devam et!"
        ]
        
        self.is_running = False
        self.is_paused = False
        self.total_seconds = 1200 # Varsayılan 20 dk
        self.current_seconds = 1200
        
        # --- ARAYÜZ TASARIMI ---
        main_layout = BoxLayout(orientation='vertical', padding=30, spacing=30)
        
        # 1. Başlık
        title_label = Label(text="Odaklan", font_size='40sp', bold=True, 
                            color=get_color_from_hex('#5856D6'), size_hint=(1, 0.15))
        main_layout.add_widget(title_label)

        # 2. Dairesel Sayaç
        self.progress_ring = CircularProgressBar(size_hint=(None, None), size=(250, 250))
        self.progress_ring.pos_hint = {'center_x': 0.5}
        
        # Sayacın ortasındaki metinler
        center_text_layout = FloatLayout(size_hint=(1, 0.4))
        center_text_layout.add_widget(self.progress_ring)
        
        self.time_label = Label(text="20:00", font_size='50sp', bold=True, 
                                color=get_color_from_hex('#000000'), 
                                pos_hint={'center_x': 0.5, 'center_y': 0.5})
        center_text_layout.add_widget(self.time_label)
        
        self.status_label = Label(text="Hazır", font_size='18sp', 
                                  color=get_color_from_hex('#8E8E93'),
                                  pos_hint={'center_x': 0.5, 'center_y': 0.35})
        center_text_layout.add_widget(self.status_label)
        
        main_layout.add_widget(center_text_layout)

        # 3. Süre Giriş Alanı (Dakika)
        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        input_layout.add_widget(Label(text="Süre (Dk):", color=get_color_from_hex('#000000'), size_hint=(0.4, 1)))
        
        self.input_field = TextInput(text="20", multiline=False, input_filter='float', 
                                     halign='center', font_size='20sp', background_normal='')
        self.input_field.background_color = get_color_from_hex('#FFFFFF')
        self.input_field.foreground_color = get_color_from_hex('#000000')
        input_layout.add_widget(self.input_field)
        
        main_layout.add_widget(input_layout)

        # 4. Butonlar (Başlat, Duraklat, Durdur)
        self.buttons_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.15))
        
        self.start_btn = Button(text="Başlat", background_normal='', background_color=get_color_from_hex('#34C759'), 
                                font_size='20sp', bold=True, on_press=self.start_timer)
        
        self.pause_btn = Button(text="Duraklat", background_normal='', background_color=get_color_from_hex('#FF9500'), 
                                font_size='20sp', bold=True, on_press=self.pause_timer, disabled=True, opacity=0)
        
        self.stop_btn = Button(text="Bitir", background_normal='', background_color=get_color_from_hex('#FF3B30'), 
                               font_size='20sp', bold=True, on_press=self.stop_timer, disabled=True, opacity=0)

        self.buttons_layout.add_widget(self.start_btn)
        self.buttons_layout.add_widget(self.pause_btn)
        self.buttons_layout.add_widget(self.stop_btn)
        
        main_layout.add_widget(self.buttons_layout)
        
        return main_layout

    def start_timer(self, instance):
        if not self.is_running:
            # İlk başlatma veya durdurulduktan sonra başlatma
            try:
                mins = float(self.input_field.text)
                if mins <= 0: mins = 1
            except:
                mins = 20
                
            self.total_seconds = int(mins * 60)
            if not self.is_paused: # Eğer duraklatılmamışsa sıfırdan başla
                self.current_seconds = self.total_seconds
            
            self.is_running = True
            self.is_paused = False
            
            # UI Güncelleme
            self.status_label.text = "Odaklanılıyor..."
            self.input_field.disabled = True
            self.start_btn.disabled = True
            self.start_btn.opacity = 0
            
            self.pause_btn.disabled = False
            self.pause_btn.opacity = 1
            self.pause_btn.text = "Duraklat"
            self.pause_btn.background_color = get_color_from_hex('#FF9500')
            
            self.stop_btn.disabled = False
            self.stop_btn.opacity = 1
            
            Clock.schedule_interval(self.update_time, 1)

    def pause_timer(self, instance):
        if self.is_paused:
            # Devam Et (Resume)
            self.is_paused = False
            self.is_running = True
            self.status_label.text = "Odaklanılıyor..."
            self.pause_btn.text = "Duraklat"
            self.pause_btn.background_color = get_color_from_hex('#FF9500') # Turuncu
            Clock.schedule_interval(self.update_time, 1)
        else:
            # Duraklat (Pause)
            self.is_running = False
            self.is_paused = True
            self.status_label.text = "Duraklatıldı"
            self.pause_btn.text = "Devam Et"
            self.pause_btn.background_color = get_color_from_hex('#34C759') # Yeşil
            Clock.unschedule(self.update_time)

    def stop_timer(self, instance):
        self.is_running = False
        self.is_paused = False
        Clock.unschedule(self.update_time)
        
        # Sıfırla
        self.current_seconds = self.total_seconds
        self.update_display()
        self.status_label.text = "Hazır"
        
        # UI eski haline
        self.input_field.disabled = False
        self.start_btn.disabled = False
        self.start_btn.opacity = 1
        
        self.pause_btn.disabled = True
        self.pause_btn.opacity = 0
        self.stop_btn.disabled = True
        self.stop_btn.opacity = 0
        self.progress_ring.angle_end = 360
        self.progress_ring.update_canvas()

    def update_time(self, dt):
        if self.current_seconds > 0:
            self.current_seconds -= 1
            self.update_display()
        else:
            # Süre bitti! Bildirim gönder ve döngüye gir (Swift kodu mantığı)
            self.send_notification()
            self.current_seconds = self.total_seconds # Başa sar
            self.update_display()

    def update_display(self):
        mins, secs = divmod(self.current_seconds, 60)
        self.time_label.text = f'{mins:02}:{secs:02}'
        # Halkayı güncelle
        self.progress_ring.set_value(self.current_seconds, self.total_seconds)

    def send_notification(self):
        msg = random.choice(self.messages)
        try:
            notification.notify(
                title='Odaklan!',
                message=msg,
                app_name='Odak App',
                ticker='Odaklanma Uyarısı'
            )
        except:
            print(f"Bildirim: {msg}")

if __name__ == '__main__':
    FocusApp().run()
