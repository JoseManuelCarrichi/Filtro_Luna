import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import soundfile as sf

# Filtro Digital FIR
N = 100  # Orden del filtro
fm = 44100  # Frecuencia de Muestreo 44.1 KHz
fc = 4000  # Frecuencia de Corte 4KHz
fN = fc / fm # Frecuencia Normalizada

# Generar la respuesta al impulso del filtro (función sinc)
h = np.zeros(N)
for k in range(1, N+1):
    h[k-1] = 2 * fN * np.sinc(2 * (k - round(N/2)) * fN)

# Aplicar la ventana Hamming a la respuesta al impulso
win = np.hamming(N)
filHam = h * win
# Guardar coeficientes en un archivo
np.savetxt("coeficientesFiltro.csv", win, delimiter=",")


# Cargar el audio
audio, sample_rate = sf.read('Audios\EnciendeLaLuz.wav')  

# Aplicar el filtro al audio
filtered_audio = signal.convolve(audio, filHam, mode = 'same')

# Guardar el audio filtrado en un nuevo archivo
sf.write('audio_filtrado_original.wav', filtered_audio, sample_rate)

# GRAFICAR
# Crear un arreglo de tiempo para la visualización
t = np.arange(0, len(audio)) / sample_rate

#filhamm
plt.figure(1,figsize=(12, 6))
plt.subplot(1,1,1)
plt.plot(filHam)
plt.tight_layout()
plt.show()

# Graficar el audio original
plt.figure(2, figsize=(12, 6))
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

# Calcular la media y la desviación estándar
mean_audio_abs = np.mean(audio_abs)
std_audio_abs = np.std(audio_abs)

# Establecer un umbral inicial (por ejemplo, 2 veces la desviación estándar por encima de la media)
threshold = 2 * std_audio_abs + mean_audio_abs
print(f"Threshold: {threshold}")


# Detección de voz humana
voz_humana = audio_abs > threshold
max_amplitude = max(audio_abs)
print(f"Max Amplitude: {max_amplitude}")

plt.subplot(4, 1, 4)
plt.plot(t, audio_abs, label='Normalizado', color='green')
plt.fill_between(t, 0, max_amplitude + 0.05, where=voz_humana, alpha=0.5, color='red', label='Voz Humana Detectada')
plt.axhline(y=threshold, color='blue', linestyle='--', label='Umbral')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid()
plt.legend()

# Detectar segmentos de voz basados en el umbral
segments_with_voice = t[audio_abs > threshold]

# Puedes imprimir los tiempos en los que se detecta voz
print("Tiempos con voz detectada:", segments_with_voice)

plt.tight_layout()
plt.show()