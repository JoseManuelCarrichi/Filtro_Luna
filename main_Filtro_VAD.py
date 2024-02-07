from EliminarSilencios import VAD
from FiltroPasaBanda import filtrarAudio, graficarTramas, graficarFiltro



#Path del Archivo original
#AudioFile = 'Audios/JM_LunaFugaz_1.wav'
AudioFile = 'Voces DB\Dany_Texto_4_Femenino.wav '
# Filtrar audio
path_Output = filtrarAudio(AudioFile)

# Graficar audios 
#graficarTramas(AudioFile, path_Output)
#graficarFiltro(AudioFile,path_Output)

# Eliminar Silencios y detectar voz
VAD(path_Output)
#VAD(AudioFile) 

