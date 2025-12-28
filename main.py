from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform

# Android'de kütüphaneleri yükle
if platform == 'android':
    from jnius import autoclass
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Context = autoclass('android.content.Context')
    NotificationManager = autoclass('android.app.NotificationManager')

class FocusApp(App):
    def build(self):
        self.timer_running = False
        self.seconds = 1500 
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.label = Label(text="25:00", font_size='50sp')
        layout.add_widget(self.label)
        
        self.start_btn = Button(text="Odaklanmayı Başlat", on_press=self.toggle_timer, background_color=(0, 1, 0, 1))
        layout.add_widget(self.start_btn)
        return layout

    def toggle_timer(self, instance):
        if not self.timer_running:
            self.timer_running = True
            self.start_btn.text = "Bitir"
            self.start_btn.background_color = (1, 0, 0, 1)
            Clock.schedule_interval(self.update_timer, 1)
            self.set_dnd(True)
        else:
            self.timer_running = False
            self.start_btn.text = "Başlat"
            self.start_btn.background_color = (0, 1, 0, 1)
            Clock.unschedule(self.update_timer)
            self.seconds = 1500
            self.update_label()
            self.set_dnd(False)

    def update_timer(self, dt):
        if self.seconds > 0:
            self.seconds -= 1
            self.update_label()
        else:
            self.toggle_timer(None)

    def update_label(self):
        mins, secs = divmod(self.seconds, 60)
        self.label.text = f'{mins:02}:{secs:02}'

    def set_dnd(self, enable):
        if platform == 'android':
            activity = PythonActivity.mActivity
            nm = activity.getSystemService(Context.NOTIFICATION_SERVICE)
            if not nm.isNotificationPolicyAccessGranted():
                intent = autoclass('android.content.Intent')("android.settings.NOTIFICATION_POLICY_ACCESS_SETTINGS")
                activity.startActivity(intent)
                return
            if enable:
                nm.setInterruptionFilter(NotificationManager.INTERRUPTION_FILTER_NONE)
            else:
                nm.setInterruptionFilter(NotificationManager.INTERRUPTION_FILTER_ALL)

if __name__ == '__main__':
    FocusApp().run()
