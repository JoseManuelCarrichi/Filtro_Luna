import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import soundfile as sf

# Filtro Digital FIR
N = 4000  # Orden del filtro
fm = 44100  # Frecuencia de Muestreo 16KHz
fc = 4000  # Frecuencia de Corte 4KHz
fN = fc / fm # Frecuencia Normalizada

# Generar la respuesta al impulso del filtro (función sinc)
h = np.zeros(N)
for k in range(1, N+1):
    h[k-1] = 2 * fN * np.sinc(2 * (k - round(N/2)) * fN)

# Aplicar la ventana Hamming a la respuesta al impulso
win = np.hamming(N)
filHam = h * win

# Cargar el audio
audio, sample_rate = sf.read('Audios\Rodrigo.wav')  

# Aplicar el filtro al audio
filtered_audio = signal.convolve(audio, filHam, mode = 'same')

# Guardar el audio filtrado en un nuevo archivo
sf.write('audio_filtrado.wav', filtered_audio, sample_rate)

# GRAFICAR
# Crear un arreglo de tiempo para la visualización
t = np.arange(0, len(audio)) / sample_rate

# Graficar el audio original
plt.figure(figsize=(12, 6))
plt.subplot(4, 1, 1)
plt.plot(t, audio, label='Audio Original')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid()
plt.legend()

# Graficar el audio filtrado
plt.subplot(4, 1, 2)
plt.plot(t, filtered_audio, label='Audio Filtrado', color='orange')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid()
plt.legend()


# Valor absoluto - Normalizado de la señal
audio_abs = np.abs(filtered_audio)

plt.subplot(4, 1, 3)
plt.plot(t, audio_abs, label='Normalizado', color='green')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid()
plt.legend()


#plt.tight_layout()
#plt.show()

# Deteccion de voz
# umbral para la detección de voz humana
umbral = 0.04  

# Detección de voz humana
voz_humana = audio_abs > umbral

# Graficar la detección de voz humana
plt.subplot(4,1,4)
plt.plot(t, audio_abs, label='Normalizado', color='green')
plt.fill_between(t, 0, 0.4, where=voz_humana, alpha=0.5, color='red', label='Voz Humana Detectada')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()