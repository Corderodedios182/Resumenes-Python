# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 10:46:20 2022

@author: indra
"""

from pyspark import SparkContext, SparkConf
import pandas as pd

conf = SparkConf().setAppName("tmp").setMaster("local")
sc = SparkContext(conf=conf)

distFile = pd.read_csv("Datos/trainsched.txt").fillna(0)

#Crear un RDD
rddFile = sc.textFile("Datos/trainsched.txt")

rdd = sc.parallelize(distFile.loc[:,"diff_min"])
rdd.collect()
rdd.count()

rddtwo = rdd.map(lambda x: x)
rddtwo.collect()


