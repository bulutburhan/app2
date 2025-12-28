from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform

# Android kütüphanelerine erişim için hazırlık
if platform == 'android':
    from jnius import autoclass
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Context = autoclass('android.content.Context')
    NotificationManager = autoclass('android.app.NotificationManager')

class FocusApp(App):
    def build(self):
        self.timer_running = False
        self.seconds = 1500  # 25 Dakika (Pomodoro)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        self.label = Label(text="25:00", font_size='50sp')
        layout.add_widget(self.label)
        
        self.start_btn = Button(text="Odaklanmayı Başlat", on_press=self.toggle_timer, background_color=(0, 1, 0, 1))
        layout.add_widget(self.start_btn)
        
        return layout

    def toggle_timer(self, instance):
        if not self.timer_running:
            # Başlatılıyor
            self.timer_running = True
            self.start_btn.text = "Bitir / Mola Ver"
            self.start_btn.background_color = (1, 0, 0, 1)
            Clock.schedule_interval(self.update_timer, 1)
            self.set_dnd(True) # DND Modunu Aç
        else:
            # Durduruluyor
            self.timer_running = False
            self.start_btn.text = "Odaklanmayı Başlat"
            self.start_btn.background_color = (0, 1, 0, 1)
            Clock.unschedule(self.update_timer)
            self.seconds = 1500 # Sayacı sıfırla
            self.update_label()
            self.set_dnd(False) # DND Modunu Kapat

    def update_timer(self, dt):
        if self.seconds > 0:
            self.seconds -= 1
            self.update_label()
        else:
            # Süre bittiğinde otomatik durdur
            self.toggle_timer(None)

    def update_label(self):
        mins, secs = divmod(self.seconds, 60)
        self.label.text = f'{mins:02}:{secs:02}'

    def set_dnd(self, enable):
        """
        Rahatsız Etmeyin modunu açıp kapatan fonksiyon
        """
        if platform == 'android':
            activity = PythonActivity.mActivity
            nm = activity.getSystemService(Context.NOTIFICATION_SERVICE)
            
            # İzin kontrolü
            if not nm.isNotificationPolicyAccessGranted():
                # Kullanıcıyı izin sayfasına yönlendir
                intent = autoclass('android.content.Intent')(
                    "android.settings.NOTIFICATION_POLICY_ACCESS_SETTINGS"
                )
                activity.startActivity(intent)
                return

            if enable:
                # DND Aç (INTERRUPTION_FILTER_NONE = Tam Sessizlik)
                nm.setInterruptionFilter(NotificationManager.INTERRUPTION_FILTER_NONE)
            else:
                # DND Kapat (INTERRUPTION_FILTER_ALL = Her şeye izin ver)
                nm.setInterruptionFilter(NotificationManager.INTERRUPTION_FILTER_ALL)
        else:
            # PC testi için
            status = "AÇILDI" if enable else "KAPATILDI"
            print(f"Sistem: Rahatsız Etmeyin Modu {status}")

if __name__ == '__main__':
    FocusApp().run()