import multiprocessing
import os
import time

def proceso_hijo():
    print(f"Proceso Hijo: {os.getpid()}\nProceso Padre: {os.getppid()}")
    time.sleep(2)
    print("Finalizó el proceso hijo")
def main():
    p1 = multiprocessing.Process(target=proceso_hijo)
    p2 = multiprocessing.Process(target=proceso_hijo)
    p3 = multiprocessing.Process(target=proceso_hijo)
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
    print("Finalizó el proceso padre")
if __name__ == "__main__":
    main()