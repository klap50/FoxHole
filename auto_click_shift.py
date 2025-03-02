import time
import threading
from pynput.keyboard import Controller as KeyboardController, Key, Listener
from pynput.mouse import Controller as MouseController, Button

# Inicializar controladores
keyboard = KeyboardController()
mouse = MouseController()

# Número de repeticiones
total_clicks = 27

# Variables de control
activar_autoclick = False  # Estado del AutoClick
mantener_click = False  # Estado de mantener el clic apretado
keys_pressed = set()  # Teclas presionadas

# Bloqueo para controlar la ejecución del script
running = True  

def autoclick():
    """Ejecuta la secuencia de clicks mientras activar_autoclick sea True"""
    global activar_autoclick
    while running:
        if activar_autoclick:
            print("\n🔄 AutoClick Iniciado...")

            for i in range(total_clicks):
                if not activar_autoclick or not running:  # Permitir detener en cualquier momento
                    break

                # 1️⃣ Presionar Shift
                keyboard.press(Key.shift)
                time.sleep(0.009)  # Esperar 2 milisegundos

                # 2️⃣ Hacer clic
                mouse.click(Button.left)
                keyboard.release(Key.shift)  # 3️⃣ Soltar Shift inmediatamente
                print(f"✅ Clic {i + 1} de {total_clicks}")

                if i < total_clicks - 1:
                    time.sleep(3)  # Esperar 5 segundos entre clics

            activar_autoclick = False  # Desactivar al terminar la secuencia
            print("⛔ AutoClick finalizado. Presiona CTRL + A para reiniciarlo.")

        time.sleep(0.5)  # Pequeña pausa antes de volver a verificar

def mantener_clic():
    """Mantiene presionado el clic izquierdo mientras mantener_click sea True"""
    global mantener_click
    estado_anterior = None  # Para evitar spam en la terminal

    while running:
        if mantener_click and estado_anterior != "MANTENIDO":
            mouse.press(Button.left)  # Mantener presionado el clic
            print("🟢 Manteniendo el clic izquierdo PRESIONADO")
            estado_anterior = "MANTENIDO"

        elif not mantener_click and estado_anterior != "LIBERADO":
            mouse.release(Button.left)  # Soltar el clic
            print("🔴 Clic izquierdo LIBERADO")
            estado_anterior = "LIBERADO"

        time.sleep(0.5)

def on_press(key):
    """Detecta combinaciones de teclas para activar funciones"""
    global activar_autoclick, mantener_click, running

    try:
        if key == Key.ctrl_l:
            keys_pressed.add("ctrl")
        elif hasattr(key, 'char'):
            if key.char == "a":
                keys_pressed.add("a")
            elif key.char == "p":
                keys_pressed.add("p")

        # 🔄 CTRL + A → Activar/Desactivar AutoClick
        if "ctrl" in keys_pressed and "a" in keys_pressed:
            activar_autoclick = not activar_autoclick  # Alternar estado
            print("✅ AutoClick ACTIVADO" if activar_autoclick else "⛔ AutoClick DETENIDO")
            keys_pressed.clear()

        # 🖱 CTRL + P → Mantener/Soltar clic izquierdo
        if "ctrl" in keys_pressed and "p" in keys_pressed:
            mantener_click = not mantener_click  # Alternar estado
            print("🖱 Clic Izquierdo: MANTENIDO" if mantener_click else "🖱 Clic Izquierdo: LIBERADO")
            keys_pressed.clear()

    except AttributeError:
        pass

def on_release(key):
    """Detectar cuando se suelta una tecla"""
    try:
        if key == Key.ctrl_l:
            keys_pressed.discard("ctrl")
        elif hasattr(key, 'char') and key.char in ["a", "p"]:
            keys_pressed.discard(key.char)
    except AttributeError:
        pass

# Iniciar los hilos en segundo plano
thread_autoclick = threading.Thread(target=autoclick, daemon=True)
thread_clic_sostenido = threading.Thread(target=mantener_clic, daemon=True)

thread_autoclick.start()
thread_clic_sostenido.start()

print("\n🟢 Script en ejecución. Controles:")
print("  🎯 CTRL + A → Iniciar/Detener AutoClick (27 clics)")
print("  🖱 CTRL + P → Mantener/Soltar Clic Izquierdo")
print("  ❌ CTRL + C → Cerrar script")

try:
    # Escuchar eventos del teclado (bloqueante)
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
except KeyboardInterrupt:
    print("\n🔴 Cerrando script...")
    running = False  # Detener todos los hilos
    exit(0)
