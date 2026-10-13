from nicegui import ui
import paho.mqtt.client as mqtt


MQTT_BROKER = "test.mosquitto.org"


client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)
client.loop_start()


def update_pan(e):
    angle = str(int(e.value))
    client.publish("weather/servo1", angle)
    pan_label.set_text(f"Horizontal (Pan) Angle: {angle}°")

def update_tilt(e):
    angle = str(int(e.value))
    client.publish("weather/servo2", angle)
    tilt_label.set_text(f"Vertical (Tilt) Angle: {angle}°")


with ui.card().classes('w-96 mx-auto q-pa-lg items-center shadow-md my-8'):
    ui.label('Pan-Tilt Camera Controller').classes('text-xl font-bold text-blue-6')
    ui.label('Drag the sliders below to point your weather camera station.').classes('text-xs text-gray-500 text-center q-mb-md')

    pan_label = ui.label('Horizontal (Pan) Angle: 90°').classes('text-sm font-semibold self-start')
    ui.slider(min=0, max=180, value=90, on_change=update_pan).classes('w-full q-mb-md')

    tilt_label = ui.label('Vertical (Tilt) Angle: 90°').classes('text-sm font-semibold self-start')
    ui.slider(min=0, max=180, value=90, on_change=update_tilt).classes('w-full')

    ui.button('Center Mount (90°)', on_click=lambda: [
        client.publish("weather/servo1", "90"),
        client.publish("weather/servo2", "90")
    ]).classes('q-mt-lg w-full bg-blue-6 text-white')

ui.run(port=8080, title="Servo Control Hub")
