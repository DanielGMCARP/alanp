import os
import multiprocessing
import time
import random

# Estados del ciclo de vida de un proceso
estados = ["Creación", "Listo", "Ejecutando", "Bloqueado", "Terminado"]
pid = os.getpid
def ciclo_de_vida_proceso(pid):
    print(f"proceso {pid} - Estado: {estados[0]}")
    time.sleep(random.choice(2))  # Simula el tiempo de creació
    print(f"proceso {pid} - Estado: {estados[1]}")
    time.sleep(random.choice(2))  # Simula el tiempo de preparación
    print(f"proceso {pid} - Estado: {estados[2]}")
    time.sleep(random.choice(0.1, 0.5))  # Simula el tiempo de ejecución
    print(f"proceso {pid} - Estado: {estados[3]}")
    time.sleep(random.choice(0.1, 0.5))  # Simula el tiempo de bloqueo
    print(f"proceso {pid} - Estado: {estados[4]}")
def main():
    procesos = []
    for i in range(5):  # Crea 5 procesos
        p = multiprocessing.Process(target=ciclo_de_vida_proceso, args=(i,))
        procesos.append(p)
        p.start()
    for p in procesos:
        p.join()
    print("Todos los procesos han finalizado.")

if __name__ == "__main__":
    main()