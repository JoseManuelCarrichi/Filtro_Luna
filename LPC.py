import matplotlib.pyplot as plt
from scipy import signal
import librosa
import numpy as np
import soundfile as sf

# Abrir archivo de coeficientes
win = np.loadtxt("coeficientesAsimetric245.txt")
#win = signal.windows.hamming(N)
# Cargar el audio
audio, sample_rate = sf.read('Audios\EnciendeLaLuz.wav')
print(audio[0])
# Aplicar el filtro al audio
filtered_audio = signal.lfilter(win,1,audio)

# Guardar el audio filtrado en un nuevo archivo
sf.write('Output_Audio\Filtered_audio.wav', filtered_audio, sample_rate)

frame_length = 100  # Longitud de la ventana
frame_overlap = 50  # Superposición entre ventanas (ajusta según tus necesidades)

num_frames = int(np.floor((len(filtered_audio) - frame_length) / frame_overlap) + 1)
print(f"Total de frames: {num_frames}")

lpc_coeffs_per_frame = []
sum_lpc_per_frame = []

for i in range(num_frames):
    start = i * frame_overlap
    end = start + frame_length
    frame = filtered_audio[start:end]

    # Calcula los coeficientes LPC para la ventana actual
    lpc_coeffs = librosa.lpc(frame, order=8)

    # Almacena los coeficientes LPC para la ventana actual (excluyendo el primer coeficiente)
    lpc_coeffs_per_frame.append(lpc_coeffs[1:])
    # Suma los coeficientes de cada frame
    sum_lpc_per_frame.append(np.sum(np.abs(lpc_coeffs[1:])))


#print(lpc_coeffs_per_frame)
print(sum_lpc_per_frame)

# Crear un arreglo de tiempo para la visualización
t = np.arange(0, len(filtered_audio)) / sample_rate

# Visualización de los resultados
plt.figure(figsize=(12,8))
plt.subplot(2,1,1)
plt.bar(range(num_frames),sum_lpc_per_frame)
plt.xlabel("Ventanas")
plt.ylabel("Suma de coeficientes")
plt.tight_layout()

plt.subplot(2,1,2)
plt.plot(t,filtered_audio)
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.tight_layout()
plt.show()

#Identificar voz
# Calcular la media y desviación estándar de las sumas de coeficientes
mean_sum = np.mean(sum_lpc_per_frame)
std_dev_sum = np.std(sum_lpc_per_frame)

# Establecer el umbral dinámico 
threshold_dynamic = mean_sum + std_dev_sum
print(f"Threshold: {threshold_dynamic}")

# Identificar regiones de interés basadas en el umbral dinámico y la concentración de sumas
regions_of_interest_dynamic = []
start_index_dynamic = None
count_below_threshold_dynamic = 0

for i, sum_of_coeffs in enumerate(sum_lpc_per_frame):
    if sum_of_coeffs > threshold_dynamic:
        if start_index_dynamic is None:
            start_index_dynamic = i
        count_below_threshold_dynamic = 0  # Reiniciar el contador
    else:
        count_below_threshold_dynamic += 1

        # Verificar si se cumple la condición de 45 frames consecutivos por debajo del umbral
        if count_below_threshold_dynamic >= 45 and start_index_dynamic is not None:
            # Guardar la región de interés y reiniciar variables
            regions_of_interest_dynamic.append((start_index_dynamic, i))
            start_index_dynamic = None
            count_below_threshold_dynamic = 0
print(regions_of_interest_dynamic)
# Extraer y guardar fragmentos de audio basados en el umbral dinámico
count = 1
concatenated_audio = np.array([])  # Inicializar el array para el audio concatenado
for start_dynamic, end_dynamic in regions_of_interest_dynamic:
    start_dynamic = start_dynamic * frame_overlap
    end_dynamic = end_dynamic * frame_overlap + frame_length
    audio_clip_dynamic = filtered_audio[start_dynamic:end_dynamic]
    #Concatenar las muestras
    concatenated_audio = np.concatenate([concatenated_audio, audio_clip_dynamic])
    # Guardar el fragmento de audio como archivo
    sf.write(f'Output_Audio\Audios{start_dynamic}_{end_dynamic}_{count}.wav', audio_clip_dynamic, sample_rate)
    count += 1
# Guardar el audio concatenado como archivo
sf.write('Output_Audio\Voice_clips.wav', concatenated_audio, sample_rate)

# Visualización de los resultados con matplotlib
plt.figure(figsize=(12, 8))

# ... (subgráficos anteriores)

# Marcado del umbral dinámico y las regiones de interés en el tercer subgráfico
plt.bar(range(num_frames), sum_lpc_per_frame, color='skyblue')
#plt.title('Suma de Coeficientes LPC por ventana')
plt.xlabel('Ventanas')
plt.ylabel('Suma de Coeficientes LPC')
plt.axhline(y=threshold_dynamic, color='green', linestyle='--', label='Umbral Dinámico')

# Marcar las regiones de interés basadas en el umbral dinámico en verde
for start_dynamic, end_dynamic in regions_of_interest_dynamic:
    plt.axvspan(start_dynamic, end_dynamic, color='red', alpha=0.3)
    plt.axvline(x=start_dynamic, color='red', linestyle='-', alpha=0.5)
    plt.axvline(x=end_dynamic, color='red', linestyle='-', alpha=0.5)

plt.legend()

plt.tight_layout()
plt.show()