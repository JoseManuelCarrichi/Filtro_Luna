import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Filtro Digital FIR
N = 160  # Orden del filtro
fm = 44100  # Frecuencia de Muestreo 
fc = 4000  # Frecuencia de Corte 4KHz
fN = fc / fm # Frecuencia Normalizada

# Generar la respuesta al impulso del filtro (función sinc)
h = np.zeros(N)
for k in range(1, N+1):
    h[k-1] = 2 * fN * np.sinc(2 * (k - round(N/2)) * fN)

# Aplicar la ventana Hamming a la respuesta al impulso
#win = np.hamming(N)
win = signal.windows.hamming(N)
filHam = h * win

# Filtro con coeficientes propios
# Abrir archivo de coeficientes
newWin = np.loadtxt("coeficientesAsimetric245.txt")
filCoef = h * newWin 

# Graficar coeficientes
plt.figure(1,figsize=(12, 6))
plt.plot(filHam, label = "Hamming")
plt.plot(newWin, label = "Filtro propuesto")
plt.tight_layout()
plt.grid()
plt.legend()
plt.show()


# Calcular la respuesta en frecuencia del filtro
frequencies, response = signal.freqz(filHam, worN=8000, fs=fm)
frequencies2, response2 = signal.freqz(newWin, worN=8000, fs=fm)

# Obtener la respuesta de magnitud en decibeles
magnitude = 20 * np.log10(np.abs(response))
magnitude2 = 20 * np.log10(np.abs(response2))

plt.figure()
plt.plot(frequencies, magnitude, label = "Hamming")
plt.plot(frequencies2, magnitude2, label= "Filtro propesto" )
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud (dB)')
plt.grid()
plt.legend()
plt.show()