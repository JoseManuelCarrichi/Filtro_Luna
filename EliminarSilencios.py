import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

# Lectura del audio
Audio, sample_rate = sf.read('Audios/Vian_EnciendeLaLuz.wav') 

#tam = len(Audio)
yn = Audio**2 # Calcular la energía de la señal
yne = np.log(yn) # Pasar a escala logarítmica
yneAux = np.copy(yne)
yneAux[np.isneginf(yne)] = np.nan # Busca valores en -inf y los asigna como Not as Number
minimo = np.nanmin(yneAux) # Busca el valor mínimo en la señal
yne[np.isneginf(yne)] = minimo # En aquellos puntos donde asigno NAN, coloca el mínimo

del yneAux, minimo # Elimina las variables
aux = np.max(yne)
aux1 = np.min(yne) + 17
YnenNoise = yne[np.where(yne <= aux1)[0]]


plt.figure()
plt.plot(YnenNoise)
plt.show()

hyne, _ = np.histogram(YnenNoise, bins=10) #Obtiene el histograma de la señal

Ind1, Ind2, Ind3 = np.argsort(hyne)[-3:]
hyne[Ind1] = 0
hyne[Ind2] = 0
hyne[Ind3] = 0


#Graficar el histograma
plt.figure()
plt.bar(range(len(hyne)),hyne)
plt.title('Hitograma modificado')
plt.show()

# Encontrar los valores de los índices maximos
Q = ((-((10 - Ind1) + 0.5) + aux1)+ (-((10 - Ind2) + 0.5) + aux1)+ (-((10 - Ind3) + 0.5) + aux1)) / 3

audio = Q +aux
#k3 = (Q - (audio*(0.375/3)))+1
k3 = (Q - (audio*(0.375/1.6)))
Humbralk3 = np.zeros(len(Audio))
Humbralk3[yne>=k3] = 1 # Los valores que superan el humbral se colocan en 1

r = np.where(Humbralk3 == 1)[0]
aux = len(r)

for s in range(aux - 1):
    if (r[s + 1] - r[s]) <= 1000:
        Humbralk3[r[s]:r[s + 1] + 1] = 1


# Graficar el humbralk3
plt.figure()
plt.plot(Humbralk3)
plt.show()

AudioClean = Audio[Humbralk3 > 0]

plt.figure()
plt.plot(AudioClean)
plt.show()

plt.figure()
plt.plot(Audio)
plt.plot(Humbralk3)
plt.show()

# Guardar el audio final
sf.write('Output_Audio/Voice_without_silence.wav',AudioClean,sample_rate)