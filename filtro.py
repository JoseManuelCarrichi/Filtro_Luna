import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Filtro Digital... Feb/2022
N = 100  # Orden del filtro
fm = 16000 # Frecuencia de muestreo 16 KHz
fc = 4000  # Frecuencia de Corte 4 KHz
fN = fc / fm

# Generar la respuesta al impulso del filtro (función sinc)
h = np.zeros(N)
for k in range(1, N+1):
    h[k-1] = 2 * fN * np.sinc(2 * (k - round(N/2)) * fN)

# Aplicar la ventana Hamming a la respuesta al impulso
#win = np.hamming(N)
win = signal.windows.hamming(N)
np.savetxt("coeficientesFiltro.txt", win, delimiter=",")
filHam = h * win
print(type(win))

# Calcular la respuesta en frecuencia del filtro
frequencies, response = signal.freqz(filHam, worN=8000, fs=fm)
frequencies2, response2 = signal.freqz(h, worN=8000, fs=fm)

# Obtener la respuesta de magnitud en decibeles
magnitude = 20 * np.log10(np.abs(response))
magnitude2 = 20 * np.log10(np.abs(response2))

# Visualizar la respuesta de magnitud del filtro
plt.figure()
plt.plot(frequencies, magnitude, label='Hamming')
plt.plot(frequencies2, magnitude2, label='Señal cuadrada')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud (dB)')
plt.grid()
plt.legend()
plt.show()