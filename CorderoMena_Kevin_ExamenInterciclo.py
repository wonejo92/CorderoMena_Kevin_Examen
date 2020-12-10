from mpi4py import MPI
import numpy as np
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
filas=0;
columnas=0;
vector=0;

inicio=time.time()

def Producto_Matriz_Vector(c, B, Resultado):
    R = list()
    for i in range(Resultado):
        sum = 0
        for j in range(Resultado):
            sum += B[i][j] * c[j]
        R.append(sum)
    print(" Resultado :" ,R)

if rank==0:
    print("Ingrese el tamaño de la matriz;")
    filas = int(input("Ingrese el numero de filas:"))
    columnas = int(input("Ingrese el numero de Columnas:"))
    data=np.random.random((filas,columnas))
    vector = int(input("Ingrese el Tamaño del vector:"))
    req=comm.isend(vector,dest=1,tag=11)
    req = comm.isend(data, dest=2, tag=12)
    req = comm.isend(data, dest=3, tag=13)
    req.wait()

elif rank==1:
    req=comm.irecv(source=0,tag=11)
    data=req.wait()
    C = np.random.random(data)
    req = comm.isend(C, dest=3, tag=15)
    req = comm.isend(C, dest=2, tag=12)
    req.wait()

elif rank==2:
    req=comm.irecv(source=0,tag=12)
    data=req.wait()
    a = np.zeros(len(data))
    req = comm.isend(a, dest=3, tag=14)
    req.wait()

elif rank==3:
    #Recuperacion de la matriz enviada por el proceso Nª0
    req=comm.irecv(source=0,tag=13)
    Matriz=req.wait()
    # Recuperacion del vector enviada por el proceso Nª1
    req=comm.irecv(source=1,tag=15)
    Vector=req.wait()
    # Recuperacion del vector Resultante enviada por el proceso Nª2
    req=comm.irecv(source=2,tag=14)
    VectorResultado=req.wait()

    print("Ejecucion desde el rank 3")
    print()
    print("Mtriz ------> ",Matriz)
    print()
    print("Vector----->",Vector)
    print()
    print("Vector de 0----->", VectorResultado)

    for i in range(len(Matriz)):
        VectorResultado[i] = 0.0;
        for j in range(len(Matriz[i])):
            VectorResultado[i] += Matriz[i][j] * Vector[j]

    print(" Resultado : ", VectorResultado)

    #Invocacion a la funcion Producto de una matriz por un vector pasando los parametros anteriormente obtenidos.
    Producto_Matriz_Vector(Vector,Matriz,len(VectorResultado))

    final = time.time()
    tiempo = (final - inicio)
    print("Tiempo empleado de Programacion con MPi basado en Broadcast es: " + str(tiempo) + " Segundos")








