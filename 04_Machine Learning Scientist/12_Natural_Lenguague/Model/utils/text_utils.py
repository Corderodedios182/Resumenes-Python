### Bitácora de futura edición:
# Comentar código #- HECHO
# Dar formato a la PEP8 y PEP484 #- HECHO
# Preparar estilo numpy #- HECHO
# Vectorizar estilo numpy #- HECHO
# Vectorizar estilo numba #- PENDIENTE
# Preparar para paralelización tipo Dask

################################################################################
#
# Nombre del guión         : text_utils.py
# Descripción              : Programa con ProcesadoDeTexto para corregir errores
#                             en texto (procesa texto y entrega un vector 
#                             semántico).
# Autor(es)                : Alfredo Espinoza Pelayo
# Correo(s) Electrónico(s) : c.aespel@ternium.com.mx
# Última Fecha de Edición  : 10/05/2022
#
################################################################################


# Índice:
##  • Módulos a Importar
##  • Clase Principal
###    1. Atributos
###    2. Métodos Privados
####       _actualizar_letras_sustitutas
####       _sustituir_letras_extrañas
####       _quitar_puntuación_y_espacios_extras
####       _vectorizar_token
####       _preprocesar_texto
###    3. Métodos Públicos
####       vectorize



################################################################################
# Módulos a Importar ###########################################################
################################################################################
# region

# Estándar
##  - dataclasses: Con este módulo se crean estructuras de datos arbitrarias
##  - re: Con este módulo se buscan expresiones regulares en textos
##  - string: módulo contiene conjuntos de letras premitidas
##  - typing: módulo usado para proveer indicios de tipificación de variables
##  - warning: módulo usado para ignorar warnings
from dataclasses import dataclass
import re
import string
from typing import List

# De terceros
##  - gensim: Módulo para procesar texto, similitudes, vectorizar
##  - numpy: Con este módulo se manejan arreglos de numpy y métodos de 
##            promediado y suma de vectores p/elemento
##  - unidecode: Módulo con tuplas donde se sustituyen létras generales con su 
##                equivalente del alfabeto inglés
import gensim
import numpy as np
from unidecode import unidecode

# Local
## (vacío)

# endregion



################################################################################
# Clase Principal ##############################################################
################################################################################
# region

@dataclass
class ProcesadorDeTexto:
    """Procesador de texto a vector.
    1. Limpia el texto y actualiza su filtro a como se encuentra caracteres no 
     aceptables en el idioma Español.
    2. Transforma cadenas de caracteres a vectores en espacio vectorial 
     semántico utilizando un modelo de lengüaje arbitrario.

    Variables:
    ----------
    alfabeto_español: set
    alfabeto_español_y_puntuación: set
    letras_substitutas: Dict
    puntuación: set
    
    Métodos Privados:
    -----------------
    _actualizar_letras_sustitutas: function
    _sustituir_letras_extrañas: function
    _quitar_puntuación_y_espacios_extras: function
    _vectorizar_palabra: function
    _process_text: function
    

    Métodos Públicos:
    -----------------
    vectorize: function

    Returns
    -------
    np.ndarray
        _description_
    """

    # Atributos
    # region
    
    ## Letras en el alfabeto alfabeto español permitido
    alfabeto_español = \
        set(string.digits).union(
            set(string.ascii_letters)
        )
    alfabeto_español = \
        alfabeto_español.union(
            set('áéíóúÁÉÍÓÚüÜñÑ')
        )

    ## Puntuación permitida en el alfabeto español
    puntuación = \
        set(
            string.punctuation
        )
    puntuación = \
        puntuación.union(
            set((' ', '°'))
        )

    ## Diccionario vacío de letras substitutas que se incorporarán a como se 
    ##  vayan encontrando letras que no estén en el alfabeto español
    letras_substitutas = dict()

    ## Conjunto auxiliar unión entre el alfabeto español y los símbolos de 
    ##  puntuación aceptables
    alfabeto_español_y_puntuación = \
        alfabeto_español.union(
            puntuación
        )
        
    # endregion
    
    
    # Métodos Privados
    # region
    
    def _actualizar_letras_sustitutas(
        self,
        letras_raras: set,
    ) -> None:
        """Aquí se actualiza el diccionario de sustitución de letras o símbolos 
         raros.

        Parameters
        ----------
        letras_raras : set
            _description_
        """
        
        # Si hay letras raras que no están en el diccionario de sustitución, se 
        #  agregan a este con su respectiva sustitución
        if not letras_raras.issubset(self.letras_substitutas):
            
            letras_raras_nuevas = \
                letras_raras.difference(
                    self.letras_substitutas
                )
            
            nuevas_letras_raras_substitutas = \
                {
                    letra_rara_nueva:
                        unidecode(
                            string=letra_rara_nueva
                        )
                    for letra_rara_nueva
                    in letras_raras_nuevas
                }
            
            # Se computa y actualiza la lista de letras substitutas del 
            #  Procesador
            self.letras_substitutas.update(nuevas_letras_raras_substitutas)

            
    def _sustituir_letras_extrañas(
        self,
        token: str,
    ) -> str:
        """Filtra los símbolos que no pertenecen al idioma Español, ni a la 
         puntuación permitida.
        El filtro de símbolos crece a como este va conociendo nuevos simbolos no
         permitidos, para así no empezar con un filtro innecesariamente amplio
        (evitar cómputo innecesario).
        En la medida de lo necesario, se sustituyen las letras raras por letras
         del idioma Español y crece un diccionario de sustitución para futuras 
         letras raras (como por ejemplo Ç se sustituye por C).

        Parameters
        ----------
        token : str
            _description_

        Returns
        -------
        str
            _description_
        """

        # Si la cadena está vacía, regresar ''
        if token == '':
            return token

        # Hacer una set con todas los diferentes caracteres de la cadena de 
        #  caracteres
        letras = set(token)

        # Si todas los caracteres pertenecen al alfabeto español y puntuaciones 
        #  permitidas, regresar cadena de caracteres
        if letras.issubset(self.alfabeto_español_y_puntuación):
            return token
        
        # Si hay letras que no estén en el alfabeto español ni en el conjunto
        #  de puntuación, hacer limpieza
        else:
            # Se obtienen las letras ausentes en el alfabeto español y conjunto 
            #  de puntuación
            letras_raras = \
                letras.difference(
                    self.alfabeto_español_y_puntuación
                )
            
            self._actualizar_letras_sustitutas(letras_raras)

            for letra_rara in letras_raras:
                token = \
                    np.char.replace(
                        a=token,
                        old=letra_rara,
                        new=self.letras_substitutas[letra_rara],
                    )
            
            return token
        

    @staticmethod
    def _quitar_puntuación_y_espacios_extras(
        token: str,
    ) -> str:
        """Quita todo lo que no sea palabra, tabulaciones y espacios en blanco
         extras.

        Parameters
        ----------
        token : str
            _description_
            
        Returns
        -------
        str
            _description_
        """
        
        # Sustituye lo que no sea palabra o (espacio, tabulación o cambio de 
        #  línea) por un espacio en blanco
        token_nopunt = \
            re.sub(
                pattern=r'[^\w\s]',
                repl=' ',
                string=token,
            )
        
        # Rompe la cadena al encontrar un espacio en blanco
        token_nopunt_separado = token_nopunt.split()
        
        # Se unen las cadenas de la lista en una sóla cadena con un solo espacio 
        #  entre cadenas de caracteres
        token_nopunt_no_extr_espacio = \
            " ".join(
                token_nopunt_separado
            )
        
        return token_nopunt_no_extr_espacio


    @staticmethod
    def _vectorizar_token(
        token: str,
        model_w2v: gensim.models.Word2Vec,
    ) -> np.ndarray:
        
        try:
            vec = \
                model_w2v.wv[token]
        
        except:
            vec = \
                np.zeros(
                    shape=model_w2v.vector_size,
                    dtype=np.float64,
                )

        return vec


    def _preprocesar_texto(
        self,
        texto: str,
    ) -> List[str]:
        """Función principal de preprocesamiento.

        Parameters
        ----------
        texto: str
            _description_

        Returns
        -------
        np.ndarray[np.str_]
            _description_
        """
        
        tokens = texto.split()

        # Lista de tokens con letras minimizadas
        tokens = \
            [
                str.lower(token)
                for token
                in tokens
            ]

        # Lista de tokens con letras minimizadas, sin símbolos raros
        tokens = \
            [
                str(
                    self._sustituir_letras_extrañas(
                        token=token,
                    )
                )
                for token
                in tokens
            ]

        # Lista de tokens con letras minimizadas, sin símbolos raros, sin 
        #  puntuaciones ni espacios extras
        tokens = \
            [
                self._quitar_puntuación_y_espacios_extras(
                    token=token,
                ) 
                for token
                in tokens
            ]

        # Lista de tokens con letras minimizadas, sin símbolos raros, sin 
        #  puntuaciones ni espacios extras, sin tokens vacíos
        tokens = \
            list(
                filter(None, tokens)
            )
            
        return tokens

    # endregion
    

    # Métodos Públicos
    # region
    
    def vectorize(
        self,
        texto: str,
        model_w2v: gensim.models.Word2Vec,
    ) -> np.ndarray:
        """Función principal de vectorización.
        Recibe una cadena de caracteres (str) y entrega un arreglo con elementos
         numéricos flotantes, estos representan el promedio de cada una de las
         representaciones de cada elemento en la lista de cadena de caracteres 
         en el espacio semántico vectorial.
         
        Parameters
        ----------
        texto : str
            _description_
        model_w2v: gensim.models.Word2Vec
            _description_

        Returns
        -------
        np.ndarray
            _description_
        """

        texto_length = len(texto)
        
        if texto_length != 0:
            tokens = \
                self._preprocesar_texto(
                    texto=texto,
                )

            vector = \
                np.mean(
                    np.array(
                        object = \
                            [
                                self._vectorizar_token(
                                    token=token,
                                    model_w2v=model_w2v,
                                )
                                for token
                                in tokens
                            ]
                    ),
                    axis=0,
                )
                
            vector = \
                np.ravel(
                    a=vector
                )
        else:
            vector: np.ndarray = \
                np.zeros(
                    shape=model_w2v.vector_size,
                )
            
        return vector

    # endregion
    
# endregion
