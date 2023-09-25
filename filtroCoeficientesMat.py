import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import soundfile as sf

# Filtro Digital FIR
N = 160  # Orden del filtro
fm = 44100  # Frecuencia de Muestreo 
fc = 4000  # Frecuencia de Corte 4KHz
fN = fc / fm # Frecuencia Normalizada

# Abrir archivo de coeficientes
win = np.loadtxt("coeficientesAsimetric245.txt")
#win = signal.windows.hamming(N)
# Cargar el audio
audio, sample_rate = sf.read('Audios\Rodrigo.wav') 

# Graficar coeficientes
plt.figure(1,figsize=(12, 6))
plt.subplot(1,1,1)
plt.plot(win)
plt.tight_layout()
plt.show()

# Calcular la respuesta en frecuencia del filtro
frequencies, response = signal.freqz(win, worN=8000, fs=fm)
# Obtener la respuesta de magnitud en decibeles
magnitude = 20 * np.log10(np.abs(response))
# Visualizar la respuesta de magnitud del filtro
plt.figure()
plt.plot(frequencies, magnitude)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud (dB)')
plt.grid()
plt.show()

# Aplicar el filtro al audio
# filtered_audio = signal.convolve(audio, win, mode = 'same',)
filtered_audio = signal.lfilter(win,1,audio) 

# Guardar el audio filtrado en un nuevo archivo
sf.write('audio_filtrado_coeficientes.wav', filtered_audio, sample_rate)

# GRAFICAR
# Crear un arreglo de tiempo para la visualización
t = np.arange(0, len(filtered_audio)) / sample_rate


# Graficar el audio filtrado
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 2)
plt.plot(t, filtered_audio, label='Audio Filtrado', color='orange')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid()
plt.legend()

# Graficar el audio original
plt.subplot(2, 1, 1)
plt.plot(t, audio, label='Audio Original')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid()
plt.legend()

# Mostrar graficas
plt.tight_layout()
plt.show()