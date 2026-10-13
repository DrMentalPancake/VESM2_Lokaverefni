from nicegui import ui
import paho.mqtt.client as mqtt

PI_IP = "10.201.48.160"
MQTT_BROKER = "test.mosquitto.org" # The public cloud broker your ESP32 uses

# Initialize MQTT Client connection
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

# GRAPHICAL DASHBOARD INTERFACE LAYOUT
with ui.card().classes('w-full max-w-lg mx-auto q-pa-lg items-center shadow-lg my-8 rounded-xl'):
    ui.label('IoT Weather Surveillance Hub').classes('text-xl font-bold text-blue-6')
    ui.label('Live Network Stream & Camera Position Control Interface').classes('text-xs text-gray-500 text-center q-mb-md')
    ui.html(f'<img src="http://{PI_IP}:8000/stream" width="400" height="300" style="border-radius: 8px; border: 2px solid #e2e8f0;"/>')

    # Horizontal Pan Controls
    with ui.column().classes('w-full q-mt-md'):
        pan_label = ui.label('Horizontal (Pan) Angle: 90°').classes('text-sm font-semibold text-gray-7')
        ui.slider(min=0, max=180, value=90, on_change=update_pan).classes('w-full')

    # Vertical Tilt Controls
    with ui.column().classes('w-full q-mt-sm'):
        tilt_label = ui.label('Vertical (Tilt) Angle: 90°').classes('text-sm font-semibold text-gray-7')
        ui.slider(min=0, max=180, value=90, on_change=update_tilt).classes('w-full')

    # Quick alignment reset button
    ui.button('Reset Mount Position (90°)', on_click=lambda: [
        client.publish("weather/servo1", "90"),
        client.publish("weather/servo2", "90")
    ]).classes('q-mt-lg w-full bg-blue-6 text-white font-bold py-2 rounded-lg')

# Start local server frame on Port 8080
ui.run(port=8080, title="IoT Weather Station")

