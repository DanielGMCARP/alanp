import threading
import time
import random

bandeja_pedidos = []
numero_pedido = 0
seguir_trabajando = True

espacios_vacios = threading.Semaphore(5)
espacios_llenos = threading.Semaphore(0)
lock_bandeja = threading.Lock()
lock_contador = threading.Lock()

def hacer_pedido():
    global numero_pedido
    with lock_contador:
        numero_pedido += 1
        return f"Pedido-{numero_pedido}"

def obtener_estado_bandeja():
    with lock_bandeja:
        return len(bandeja_pedidos)

def mesero_trabajo(numero_mesero):
    global seguir_trabajando
    while seguir_trabajando:
        try:
            nuevo_pedido = hacer_pedido()
            
            if espacios_vacios.acquire(timeout=1):
                with lock_bandeja:
                    bandeja_pedidos.append(nuevo_pedido)
                
                espacios_llenos.release()
                
                print(f"MESERO {numero_mesero} genero: {nuevo_pedido}")
                print(f"Bandeja: {obtener_estado_bandeja()} pedidos")
                print("-" * 35)
                time.sleep(random.uniform(1.5, 3.5))
            else:
                print(f"MESERO {numero_mesero}: Bandeja llena - no puede agregar")
                
        except:
            break

def cocinero_trabajo(numero_cocinero):
    global seguir_trabajando
    while seguir_trabajando:
        try:
            if espacios_llenos.acquire(timeout=1):
                pedido_a_cocinar = None
                with lock_bandeja:
                    if bandeja_pedidos:
                        pedido_a_cocinar = bandeja_pedidos.pop(0)
                
                if pedido_a_cocinar:
                    espacios_vacios.release()
                    
                    print(f"COCINERO {numero_cocinero} tomo: {pedido_a_cocinar}")
                    print(f"Bandeja: {obtener_estado_bandeja()} pedidos")
                    
                    tiempo_cocinar = random.uniform(2, 5)
                    print(f"COCINERO {numero_cocinero} preparando {pedido_a_cocinar} ({tiempo_cocinar:.1f}s)")
                    time.sleep(tiempo_cocinar)
                    
                    print(f"COCINERO {numero_cocinero} completo: {pedido_a_cocinar}")
                    print("=" * 50)
                else:
                    espacios_llenos.release()
            else:
                if seguir_trabajando:
                    print(f"COCINERO {numero_cocinero}: Bandeja vacia - esperando pedidos")
                
        except:
            break

def main():
    global seguir_trabajando
    
    print("🍽️  RESTAURANTE ALDARDO GUAGLIARDO🐱‍👤🐱‍👤")
    print("🍕 COMIDA LAURA")
    print("=" * 50)
    print("Iniciando sistema")
    print("3 meseros (productores)")
    print("2 cocineros (consumidores)")  
   
    print("=" * 50)
    time.sleep(2)
    
    meseros = []
    cocineros = []
    
    for i in range(3):
        mesero = threading.Thread(target=mesero_trabajo, args=(i+1,))
        mesero.start()
        meseros.append(mesero)
    
    for i in range(2):
        cocinero = threading.Thread(target=cocinero_trabajo, args=(i+1,))
        cocinero.start()
        cocineros.append(cocinero)
    
    try:
        time.sleep(20)
    except KeyboardInterrupt:
        print("\n⚠️  Cerrando restaurante")
    time.sleep(2)
    
    seguir_trabajando = False
    
    for mesero in meseros:
        mesero.join()
    for cocinero in cocineros:
        cocinero.join()
    
    print("\n🏪 RESTAURANTE CERRADO😜😜😜😜")
    time.sleep(2)
    print(f"📊 Total de pedidos procesados: {numero_pedido}")
    time.sleep(1)
    print(f"📋 Pedidos pendientes: {obtener_estado_bandeja()}")

if __name__ == "__main__":
    main()