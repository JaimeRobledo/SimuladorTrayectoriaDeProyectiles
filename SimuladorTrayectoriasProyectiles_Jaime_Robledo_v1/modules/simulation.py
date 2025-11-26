import matplotlib.pyplot as plt
import numpy as np
from . import ammo
municion_dict = ammo.municion_dict
import math


def densidad_atomsfera(y):
    p0 = 1.225  # Densidad del aire a nivel del mar en kg/m^3
    p_actual = p0 * ((np.e) ** (-y / 8500))
    return p_actual

def f(u,m,g,cd,areaFrontal,p):
    x, y, vx, vy = u
    v_total=np.sqrt((vx**2)+(vy**2))

    # Fuerza de drag
    if v_total > 1e-12:
        fuerzaResistenciaAire=(0.5*p*cd*areaFrontal)*(v_total**2)
        ax=((-fuerzaResistenciaAire)/(m))*((vx)/(v_total))
        ay=-g-(((fuerzaResistenciaAire)/(m))*((vy)/(v_total)))
    else:
        ax = 0
        ay = -g

    # Retorna derivadas
    return np.array([vx, vy, ax, ay], float)

def calcular_resistencia_aire(v0x,v0y,g,y0,m,cd,p,delta_t,d):
    lista_x = []
    lista_y = []
    t=0
    #posicion
    x=0
    y=y0
    #Velocidad
    vx=v0x
    vy=v0y
    #area frontal del proyectil
    areaFrontal = math.pi * (d/2)**2

    while(y>=0):
        p=densidad_atomsfera(y)

        u=np.array([x,y,vx,vy])

        k1=f(u,m,g,cd,areaFrontal,p)

        u2=u+((delta_t/2)*k1)

        k2=f(u2,m,g,cd,areaFrontal,p)

        u3=u+((delta_t/2)*k2)

        k3=f(u3,m,g,cd,areaFrontal,p)

        u4=u+(delta_t*k3)

        k4=f(u4,m,g,cd,areaFrontal,p)


        #actulizar posiciones
        u_next= u+((delta_t/6)*((k1)+(2*k2)+(2*k3)+(k4)))
        x,y,vx,vy=u_next
        t+=delta_t

        if(y!=0):
            lista_x.append(x)
            lista_y.append(y)
        


    return lista_x,lista_y,vx,vy,t
    

def ComponentesVelocidad(v0,theta):
    v0x=v0*np.cos(theta)
    v0y=v0*np.sin(theta)
    return v0x,v0y

def tiempoVuelo(v0y,g,y0):
    if(y0==0):
        t=(2*v0y)/(g)
    else:
        t=(-v0y-np.sqrt(v0y**2-4*(-0.5*g)*y0))/(2*(-0.5*g))
    return t

def AlcanceMax(x):
    xMax=max(x)
    return xMax

def AlturaMax(y):
    yMax= max(y)
    return yMax

def energia_cinetica(m,v):
    Ec=0.5*m*(v**2)
    return Ec

def graficar(v0=400,angulo=10,m=0.2,cd=0.47,d=0.05,y0=0,municion="Default", municion_dict=None, plot=True):
    g=9.81
    p=1.225
    delta_t=0.01
    theta=np.radians(angulo)

    if municion != "Default" and municion in municion_dict:
        datos = municion_dict[municion]
        v0 = datos["v0"]
        m  = datos["m"]
        cd = datos["Cd"]
        d  = datos["d"]


    v0x,v0y = ComponentesVelocidad(v0,theta)

    #----Parabola con resitencia de aire----
    x_vals, y_vals, vx, vy, t = calcular_resistencia_aire(v0x,v0y,g,y0,m,cd,p,delta_t,d)
    xMax = AlcanceMax(x_vals)
    yMax = AlturaMax(y_vals)
    x_vals = np.array(x_vals)
    y_vals = np.array(y_vals)

    #----Parabola Perfecta----
    x_vals_perfecto, y_vals_perfecto, vx_perfecto, vy_perfecto, t_perfecto = calcular_resistencia_aire(v0x,v0y,g,y0,m,0,p,delta_t,d)
    xMax_perfecto = max(x_vals_perfecto)
    yMax_perfecto = max(y_vals_perfecto)
    x_vals_perfecto = np.array(x_vals_perfecto)
    y_vals_perfecto = np.array(y_vals_perfecto)

    #redondear valores muy cercanos a cero
    x_vals = np.round(x_vals, decimals=10)
    y_vals = np.round(y_vals, decimals=10)
    x_vals_perfecto = np.round(x_vals_perfecto, decimals=10)
    y_vals_perfecto = np.round(y_vals_perfecto, decimals=10)


    energia_inicial=energia_cinetica(m,v0)
    energia_final_real=energia_cinetica(m,vx)
    energia_final_perfecta=energia_cinetica(m,vx_perfecto)

    plt.figure(figsize=(18,16))

    #----Parabola con resitencia de aire----

    plt.plot(x_vals/1000, y_vals/1000, 'b-', label='Con resistencia de aire')
    plt.xlabel("Distancia (km)")
    plt.ylabel("Altura (km)")
    plt.title("Trayectoria del proyectil")
    plt.grid(True)
    #Marcar altura maxima
    idx = np.argmax(y_vals)
    yMax = y_vals[idx]
    x_at_yMax = x_vals[idx]
    plt.plot((x_at_yMax)/1000, yMax/1000, 'ro')
    #marcar alcance maximo
    plt.plot(xMax/1000, 0, 'ro')

    #----Parabola Perfecta----

    plt.plot(x_vals_perfecto/1000, y_vals_perfecto/1000, 'g--', label='Sin resistencia de aire')
    #Marcar altura maxima
    idx = np.argmax(y_vals_perfecto)
    yMax_perfecto = y_vals_perfecto[idx]
    x_at_yMax = x_vals_perfecto[idx]
    plt.plot((x_at_yMax)/1000, yMax_perfecto/1000, 'ro')
    #marcar alcance maximo
    plt.plot(xMax_perfecto/1000, 0, 'ro')

    plt.legend()
    if plot:
        # código de matplotlib
        plt.show()
    else:
        return x_vals, y_vals, vx, vy, t, x_vals_perfecto, y_vals_perfecto, t_perfecto, energia_inicial, energia_final_real, energia_final_perfecta

    


