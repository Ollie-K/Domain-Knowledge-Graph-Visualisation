#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 10:51:49 2021

@author: ollie
"""
# Load back with memory-mapping = read-only, shared across processes.
from gensim.models import KeyedVectors
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from rdflib import Graph

g = Graph()
g.parse("13-8-inference.ttl", format="ttl")
    
wv = KeyedVectors.load("fp_3.embeddings", mmap='r') #loading vectors

vec_dict = {} #initialising an empty dictionary
for key in wv.wv.vocab:  # loop through vocabulary
   vec_dict[key] = wv[key] #fill add the corresponding vector to the dictionary of vocab keys

vec_df = pd.DataFrame(vec_dict) #transform dictionary into dataframe
vec_df = vec_df.transpose() #use vocab as index rather than columns
vec_df['uris'] = vec_df.index.to_series()
vec_uris=vec_df[vec_df['uris'].str.contains('wrenand')]
print(vec_uris.head()) #preview of dataframe

#retrieving node classes
vec_types = pd.DataFrame(columns=['node', 'class'])
for uri in vec_uris['uris']:
        uri = str(uri).replace(' ', '_')
        qres = g.query(
            """
            SELECT  ?node_class 
            WHERE{
          <%s> rdf:type ?node_class . 
          FILTER ( ?node_class = fp:Actor || ?node_class = fp:Action|| ?node_class = fp:Issue|| ?node_class = fp:Method|| ?node_class = fp:Place|| ?node_class = fp:Publication)
        } 
            """ % uri)        
        for row in qres:
            if 'owl' not in str(row.node_class):
                superclass = row.node_class.replace('http://wrenand.co.uk/fpn/', '')
        if len(qres) == 0:
              superclass = 'Literal/Property'
        vec_types = vec_types.append({'node' : uri, 'class' : superclass}, ignore_index=True)
type_dict = {}
for index,row in vec_types.iterrows():
        type_dict[row[0]] = row[1]
vec_uris['classes'] = vec_uris['uris'].map(type_dict)
print(vec_uris.iloc[:,:-2].head())
x = vec_uris.iloc[:,:-2]
pca = PCA(n_components=2) #2 components for pca
principalComponents = pca.fit_transform(x) #transforming into 2 components
vec_uris[['principal component 1', 'principal component 2']] = principalComponents
               #creating dataframe
colours = {'Actor':'#fb8072', 'Action': '#b3de69', 'Issue':'#0909ed', 'Method':'#ffff29', 'Place':'#fdb462', 'Publication':'#8dd3c7'}
vec_uris['colour'] =vec_uris['classes'].map(colours)
print(vec_uris.head())
fig, ax = plt.subplots(figsize=(7,7))
ax.set_facecolor('white')
ax.grid(b=None)
for i in colours.keys(): #for each of the 6 clusters
    sub = vec_uris[vec_uris['classes'] == i] #select a subset of the data with that cluster label
    plt.scatter(x=sub['principal component 1'], y=sub['principal component 2'], 
            c=sub['colour'], s=10, marker='o', label = '%s'% i, edgecolors='black', linewidth=0.5, alpha = 0.8) #plotting labelled data
ax.legend(markerscale=2, ncol=2, loc='upper left', facecolor='white', framealpha=0.5, fontsize='medium')
plt.show() #showing it