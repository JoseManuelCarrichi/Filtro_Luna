import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import firwin, lfilter, windows


# Filtro Pasa banda
Fss = 44100 / 2  # Frecuencia de muestreo y Normalización
N = 100  # Filtro de orden 100
Flow = 300  # Frecuencia de corte baja
Fhigh = 3800  # Frecuencia de corte alta
Low = Flow / Fss
High = Fhigh / Fss
win = np.hamming(N)  # Tipo de ventana
Coef = firwin(N, [Low, High], pass_zero=False) * win  # Filtro pasa banda
plt.figure()
plt.plot(Coef)
plt.title('Coeficientes del filtro')
plt.show()

np.save('CoeficientesFPB.npy', Coef)  # Guardar los coeficientes en un archivo numpy
