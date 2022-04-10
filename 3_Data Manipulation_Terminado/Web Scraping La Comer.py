# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 11:53:58 2021

@author: Maste
"""

import requests

response = requests.get("https://www.lacomer.com.mx/lacomer-api/api/v1/public/articulopasillo/articulospasillord?filtroSeleccionado=0&idPromocion=0&marca=&noPagina=1&numResultados=20&orden=-1&padreId=961&parmInt=1&pasId=949&pasiPort=0&precio=&succId=287")

response.text


