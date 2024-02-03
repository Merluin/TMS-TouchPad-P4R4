from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.button import Button

class ppTMSApp(App):
  def build(self):
  # Main layout
  main_layout = BoxLayout(orientation='horizontal', padding=10)

# Left side layout for sliders and buttons
left_layout = BoxLayout(orientation='vertical', size_hint_x=None, width=300)

# Sliders and their labels
for text in ["IPI", "Rep", "ITI"]:
  slider_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
slider = Slider(min=0, max=100, value=40)  # Example values
slider.id = text.lower()  # Assign an id to each slider
slider.bind(value=self.on_slider_value)
label = Label(text=text, size_hint_x=None, width=100)
value_label = Label(text=str(slider.value))
slider_layout.add_widget(label)
slider_layout.add_widget(slider)
slider_layout.add_widget(value_label)
left_layout.add_widget(slider_layout)

# Buttons TS, CS, Bio
for text in ["TS", "CS", "Bio"]:
  btn = Button(text=text, size_hint_y=None, height=50)
left_layout.add_widget(btn)

# Add the left layout to the main layout
main_layout.add_widget(left_layout)

# Right side layout for ppTMS, START, PAUSE, STOP
right_layout = BoxLayout(orientation='vertical', padding=10)

# ppTMS label and percentage
pptms_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
pptms_label = Label(text="ppTMS", size_hint_x=None, width=100)
pptms_value = Label(text="0%")
pptms_layout.add_widget(pptms_label)
pptms_layout.add_widget(pptms_value)
right_layout.add_widget(pptms_layout)

# START, PAUSE, STOP buttons
for text in ["START", "PAUSE", "STOP"]:
  btn = Button(text=text, size_hint_y=None, height=100)
right_layout.add_widget(btn)

# Add the right layout to the main layout
main_layout.add_widget(right_layout)

return main_layout

def on_slider_value(self, instance, value):
  instance.parent.children[0].text = f"{int(value)}"  # Update the label with the slider value

if __name__ == '__main__':
  ppTMSApp().run()
