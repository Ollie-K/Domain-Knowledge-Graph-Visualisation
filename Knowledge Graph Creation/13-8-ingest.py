#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 08:24:19 2021

@author: ollie
"""
from rdflib import Graph
from rdflib import URIRef, Literal
from rdflib import Namespace
import pandas as pd
from datetime import datetime
import re
import owlrl
import json


def createDummyGraph():
    
    #Empty graph
    g = Graph()
    print('Initialised empty graph')
    #read in the data
    dummy = pd.read_csv('dd-final.csv', header=0)
    dummy = dummy.iloc[1:,:]


    #Creating Namespaces 
    fp = Namespace("http://wrenand.co.uk/fpn/")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    owl = Namespace("http://www.w3.org/2002/07/owl#")
    
    #Prefixes
    g.bind("fp", fp) 
    g.bind("rdf", rdf) 
    g.bind("rdfs", rdfs)
    g.bind("owl", owl)
    
    for index, row in dummy.iterrows():
        #creating nodes & assigning types based on column locations
          if pd.notnull(row[0]):
                actor_1 = URIRef("http://wrenand.co.uk/fpn/{}".format(row[0].strip().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
                g.add((actor_1, rdf.type, fp.Actor))
                g.add((actor_1, rdf.type, owl.NamedIndividual))
          if pd.notnull(row[1]):
              actor_1_type = URIRef("http://wrenand.co.uk/fpn/{}".format(row[1].strip().replace(' ', '_').replace('`', '').replace('\n', '_')))
              g.add((actor_1_type, rdfs.subClassOf, fp.Actor))
          if pd.notnull(row[2]):
              takeAction = URIRef("http://wrenand.co.uk/fpn/{}".format(row[2].strip().lower().replace(' ', '_').replace('`', '').replace('\n', '_').replace('ion', 'e').replace('ed', "")))
              g.add((takeAction, rdfs.subPropertyOf, fp.takeAction))
          if pd.notnull(row[3]):
              action = URIRef("http://wrenand.co.uk/fpn/{}".format(row[3].strip().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
              g.add((action, rdf.type, fp.Action))
          if pd.notnull(row[4]):
              action_type = URIRef("http://wrenand.co.uk/fpn/{}".format(row[4].strip().replace(' ', '_').replace('`', '').replace('\n', '_')))
              g.add((action_type, rdfs.subClassOf, fp.Action))
          if pd.notnull(row[5]):
              actor_1_loc = URIRef("http://wrenand.co.uk/fpn/{}".format(row[5].strip().replace(' ', '_').replace('`', '').replace('\n', '_')))
              g.add((actor_1_loc, rdf.type, fp.Place))
              g.add((actor_1_loc, rdf.type, owl.NamedIndividual))
          if pd.notnull(row[6]):
              #Dealing with inconsistent date formats
              action_date_str = str(row[6])
              action_date_trim = action_date_str.strip().replace(' ', '-').replace('\n', '_').replace('/', '-').replace('January', '01').replace('February', '02').replace('March', '03').replace('April', '04').replace('May', '05').replace('June', '06').replace('July', '07').replace('August', '08').replace('September', '09').replace('October', '10').replace('November', '11').replace('December', '12').replace('Jan', '01').replace('Feb', '02').replace('Mar', '03').replace('Apr', '04').replace('May', '05').replace('Jun', '06').replace('Jul', '07').replace('Aug', '08').replace('Sep', '09').replace('Oct', '10').replace('Nov', '11').replace('Dec', '12')
              if len(action_date_trim) == 4:
                  action_date_trim = "01-01-" + action_date_trim
                  action_date = datetime.strptime(action_date_trim, '%d-%m-%Y')
              if len(action_date_trim) == 10:
                  action_date = datetime.strptime(action_date_trim, '%d-%m-%Y')
              if len(action_date_trim) == 9:
                  action_day = action_date_trim.split('-')[0]
                  action_month = action_date_trim.split('-')[1]
                  action_year = action_date_trim.split('-')[2]
                  if len(action_day) == 1:
                      action_day = '0' + action_day
                  if len(action_month) == 1:
                      action_month = '0' + action_month
                  action_date_trim = action_day + '-' + action_month + '-'+ action_year
                  action_date = datetime.strptime(action_date_trim, '%d-%m-%Y')
              if len(action_date_trim) == 8:
                  action_date = datetime.strptime(action_date_trim, '%d-%m-%y')
          if pd.notnull(row[7]):
              actionImpacts = URIRef("http://wrenand.co.uk/fpn/{}".format(row[7].strip().lower().replace(' ', '_').replace('`', '').replace('\n', '_')))
              g.add((actionImpacts, rdfs.subPropertyOf, fp.actionImpacts))
          if pd.notnull(row[8]):
                actor_2 = URIRef("http://wrenand.co.uk/fpn/{}".format(row[8].strip().replace(' ', '_').replace('`', '').replace('\n', '_')))
                g.add((actor_2, rdf.type, fp.Actor))
                g.add((actor_2, rdf.type, owl.NamedIndividual))
          if pd.notnull(row[9]):
              actor_2_type = URIRef("http://wrenand.co.uk/fpn/{}".format(row[9].strip().replace(' ', '_').replace('`', '').replace('\n', '_')))
              g.add((actor_2_type, rdfs.subClassOf, fp.Actor))
          if pd.notnull(row[10]):
              issue = URIRef("http://wrenand.co.uk/fpn/{}".format(row[10].strip().lower().replace(' ', '_').replace('`', '').replace('\n', '_')))
              g.add((issue, rdf.type, fp.Issue))
              g.add((issue, rdf.type, owl.NamedIndividual))
          if pd.notnull(row[11]):
              descriptor = str(row[11]).strip().replace('\n', ' ').replace('\r', '')
          if pd.notnull(row[12]):
              reference = URIRef(row[12].replace(' ', '').strip().replace('\n', '').replace('\r', ''))
             
          #creating edges
         
          if pd.notnull(row[0]) and pd.notnull(row[1]):
              g.add((actor_1, rdf.type, actor_1_type))
         
          if pd.notnull(row[0]) and pd.notnull(row[2]) and pd.notnull(row[3]):
              g.add((actor_1, takeAction, action)) 
         
          if pd.notnull(row[3]) and pd.notnull(row[4]):
              g.add((action, rdf.type, action_type)) 
         
          if pd.notnull(row[0]) and pd.notnull(row[5]):
              g.add((actor_1, fp.locatedIn, actor_1_loc))
         
          if pd.notnull(row[3]) and pd.notnull(row[6]):
               g.add((action, fp.date, Literal(action_date)))
         
          if pd.notnull(row[3]) and pd.notnull(row[7]) and pd.notnull(row[8]):
              g.add((action, actionImpacts, actor_2))    
         
          if pd.notnull(row[8]) and pd.notnull(row[9]):
              g.add((actor_2, rdf.type, actor_2_type))
         
          if pd.notnull(row[3]) and pd.notnull(row[10]):
              g.add((action, fp.relatesTo, issue))
         
          if pd.notnull(row[0]) and pd.notnull(row[10]):
              g.add((actor_1, fp.workingOn, issue))
         
          if pd.notnull(row[8]) and pd.notnull(row[10]):
              g.add((actor_2, fp.activeIn, issue))
         
          if pd.notnull(row[3]) and pd.notnull(row[10]):
              g.add((action, fp.relatesTo, issue))
         
          if pd.notnull(row[3]) and pd.notnull(row[11]):
              g.add((action, fp.significance, Literal(descriptor)))
         
          if pd.notnull(row[3]) and pd.notnull(row[12]):
              g.add((action, fp.source, reference))
    print("Created '" + str(len(g)) + "' triples.")       
    #saving knowledge graph
    g.serialize(destination='13-8.ttl', format='ttl') 

    
def createDummyLitGraph():
    
    #Empty graph
    g = Graph()
    #read in dummy data graph
    g.parse("13-8.ttl", format="ttl")
    print("Loaded '" + str(len(g)) + "' triples.")
    #read in the  csv
    litrev = pd.read_csv('Lit Review Data.csv', header=1)
    

    #Creating Namespaces 
    fp = Namespace("http://wrenand.co.uk/fpn/")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    owl = Namespace("http://www.w3.org/2002/07/owl#")
    
    #Prefixes
    g.bind("fp", fp) 
    g.bind("rdf", rdf) 
    g.bind("rdfs", rdfs)
    g.bind("owl", owl)
    
    for index, row in litrev.iterrows():
        #creating nodes using columnar matching as before
          if pd.notnull(row[3]):
              article = URIRef("http://wrenand.co.uk/fpn/{}".format(row[3].strip().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
              g.add((article, rdf.type, fp.Article))
              g.add((article, rdf.type, owl.NamedIndividual))
          if pd.notnull(row[4]): #dealing with inconsistent author formats
              if ';' in row[4]:
                  for author in row[4].replace(' and ', '; ').split("; "):
                      author = re.sub(r'[0-9]+', '', author)
                      author_node = URIRef("http://wrenand.co.uk/fpn/{}".format(author.strip().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
                      g.add((author_node, rdf.type, fp.Academic))
                      g.add((author_node, rdf.type, owl.NamedIndividual))
              elif '.,' in row[4]:
                  for author in row[4].replace(' and ', '., ').split("., "):
                      author = re.sub(r'[0-9]+', '', author) + '.'
                      author_node = URIRef("http://wrenand.co.uk/fpn/{}".format(author.strip().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
                      g.add((author_node, rdf.type, fp.Academic))
                      g.add((author_node, rdf.type, owl.NamedIndividual))
              else:
                for author in row[4].replace(' and ', ', ').split(", "):
                    author = author.replace(',', '')  
                    author = re.sub(r'[0-9]+', '', author).lstrip()
                    author_node = URIRef("http://wrenand.co.uk/fpn/{}".format(author.strip().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
                    g.add((author_node, rdf.type, fp.Academic))
                    g.add((author_node, rdf.type, owl.NamedIndividual))
          if pd.notnull(row[6]):
              pub_date = datetime.strptime(str(row[6]), '%Y')
          if pd.notnull(row[7]):
              publication = URIRef("http://wrenand.co.uk/fpn/{}".format(row[7].strip().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
              g.add((publication, rdf.type, fp.Publication))
              g.add((publication, rdf.type, owl.NamedIndividual))
          if pd.notnull(row[8]):
              impact_factor = float(row[8])
          if pd.notnull(row[10]):
              citations = int(row[10])
          if pd.notnull(row[11]):
              pub_type = URIRef("http://wrenand.co.uk/fpn/{}".format(row[11].strip().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
              g.add((pub_type, rdfs.subClassOf, fp.Publication))
          if pd.notnull(row[13]):
              if row[13].lower() == 'yes':
                  peer_rev = True
              else:
                  peer_rev = False
          if pd.notnull(row[18]):
              method1 = URIRef("http://wrenand.co.uk/fpn/{}".format(row[18].strip().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
              g.add((method1, rdf.type, fp.Method))
          if pd.notnull(row[19]):
              method2 = URIRef("http://wrenand.co.uk/fpn/{}".format(row[19].strip().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
              g.add((method2, rdf.type, fp.Method))
          if pd.notnull(row[20]):
              method3 = URIRef("http://wrenand.co.uk/fpn/{}".format(row[20].strip().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
              g.add((method3, rdf.type, fp.Method))
          if pd.notnull(row[21]):
              method4 = URIRef("http://wrenand.co.uk/fpn/{}".format(row[21].strip().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
              g.add((method4, rdf.type, fp.Method))
          if pd.notnull(row[22]):
              method5 = URIRef("http://wrenand.co.uk/fpn/{}".format(row[22].strip().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
              g.add((method5, rdf.type, fp.Method))
          if (pd.notnull(row[23]) and len(row[23]) > 1):
              for place in row[23].split(","):
                  place_node = URIRef("http://wrenand.co.uk/fpn/{}".format(row[23].strip().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
                  g.add((place_node, rdf.type, fp.Place))
                  g.add((place_node, rdf.type, owl.NamedIndividual))
          if (pd.notnull(row[24]) and len(row[24]) > 1):
              if row[24] == 'Education':
                  issue = URIRef("http://wrenand.co.uk/fpn/{}_on_food_waste".format(row[24].strip().lower().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
              else:
                  issue = URIRef("http://wrenand.co.uk/fpn/{}_food_waste".format(row[24].strip().lower().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
              g.add((issue, rdf.type, fp.Issue))  
              g.add((issue, rdf.type, owl.NamedIndividual))
         
          #creating edges   
          if pd.notnull(row[3]) and pd.notnull(row[4]):
              if ';' in row[4]:
                  for author in row[4].replace(' and ', '; ').split("; "):
                      author = re.sub(r'[0-9]+', '', author)
                      author_node = URIRef("http://wrenand.co.uk/fpn/{}".format(author.strip().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
                      g.add((author_node, fp.wrote, article))
              elif '.,' in row[4]:
                  for author in row[4].replace(' and ', '., ').split("., "):
                      author = re.sub(r'[0-9]+', '', author) + '.'
                      author_node = URIRef("http://wrenand.co.uk/fpn/{}".format(author.strip().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
                      g.add((author_node, rdf.type, fp.Academic))
                      g.add((author_node, rdf.type, owl.NamedIndividual))
              else:
                  for author in row[4].replace(' and ', ', ').split(", "):
                      author = author.replace(',', '')  
                      author = re.sub(r'[0-9]+', '', author).lstrip()
                      author_node = URIRef("http://wrenand.co.uk/fpn/{}".format(author.strip().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
                      g.add((author_node, fp.wrote, article))
         
          if pd.notnull(row[3]) and pd.notnull(row[6]):
              g.add((article, fp.date, Literal(pub_date)))
             
          if pd.notnull(row[3]) and pd.notnull(row[7]):
              g.add((article, fp.publishedIn, publication))
       
          if pd.notnull(row[7]) and pd.notnull(row[8]):
              g.add((publication, fp.impactFactor, Literal(impact_factor)))    
         
          if pd.notnull(row[3]) and pd.notnull(row[10]):
              g.add((article, fp.citations, Literal(citations)))          
         
          if pd.notnull(row[7]) and pd.notnull(row[11]):
              g.add((publication, rdf.type, pub_type))
             
          if pd.notnull(row[3]) and pd.notnull(row[13]):
              g.add((article, fp.peerReviewed, Literal(peer_rev)))
             
          if pd.notnull(row[3]) and pd.notnull(row[18]):
              g.add((article, fp.usesMethod, method1))
             
          if pd.notnull(row[3]) and pd.notnull(row[19]):
              g.add((article, fp.usesMethod, method2))
             
          if pd.notnull(row[3]) and pd.notnull(row[20]):
              g.add((article, fp.usesMethod, method3))
             
          if pd.notnull(row[3]) and pd.notnull(row[21]):
              g.add((article, fp.usesMethod, method4))
             
          if pd.notnull(row[3]) and pd.notnull(row[22]):
              g.add((article, fp.usesMethod, method5))
             
          if pd.notnull(row[3]) and pd.notnull(row[23]) and len(row[23]) > 1:
              for place in row[23].split(","):
                  place_node = URIRef("http://wrenand.co.uk/fpn/{}".format(row[23].strip().replace(' ', '_').replace('`', '').replace('\n', '_').replace('\r', '')))
                  g.add((article, fp.concernsPlace, place_node)) 
         
          if pd.notnull(row[3]) and pd.notnull(row[24])and len(row[24]) > 1:
              g.add((article, fp.relatesTo, issue))
    print("Graph now consists of '" + str(len(g)) + "' triples.")             
    g.serialize(destination='13-8-lit.ttl', format='ttl')  
    #saving expanded knowledge graph


def OWLRLInference():
    
    g = Graph()
    #import current triples
    g.parse("13-8-lit.ttl", format="ttl")    
    
    print("Loaded '" + str(len(g)) + "' triples.")
    #import ontology
    g.load("onto-13-8.owl",  format="xml")
    
   
    
    #Performs RDFS reasoning
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, axiomatic_triples=False, datatype_axioms=False).expand(g)
    
    
    print("After inference rules: '" + str(len(g)) + "' triples.")
    

    print("\nSaving extended graph")
    #exporting to rdf as this can be read by protege but ttl cannot (needed to check for unsatisfiabilities)
    g.serialize(destination='13-8-inference.rdf', format='xml')
    g.serialize(destination='13-8-inference.ttl', format='ttl')

def elementExtraction():
    g = Graph()
    g.parse("13-8-inference.ttl", format="ttl")
    #loading knowledge graph
    print("Extracting Data")
    
    
    print('Extracting Elements')
    #SPARQL query to extract all triples
    qres = g.query(
            """
            SELECT *
            WHERE{
           ?s ?p ?o . 
    
            } 
            """ )
    df = pd.DataFrame(columns=['source', 'interaction', 'target'])
    #serializing output into dataframe
    for row in qres:
            df = df.append(
                {'source': row.s, 'interaction': row.p, 'target': row.o}, ignore_index=True)
    
    print(df.shape)
    #drop repeated triples
    df_out = df.drop_duplicates()
    print(df_out.shape)
    #drop axiomatic & class membership triples
    df_out = df_out[~(df_out['interaction'].str.contains('rdf'))]
    print(df_out.shape)
    #drop other axiomatic & class membership triples
    df_out = df_out[~(df_out['interaction'].str.contains('owl'))]
    print(df_out.shape)
    #remove namespace to improve human readability
    df_out = df_out.replace('http://wrenand.co.uk/fpn/', '', regex=True)
    print(df_out.shape)
    #remove any further duplicated triples, remove any blanks
    df_out = df_out.drop_duplicates()
    df_out.replace("", float("NaN"), inplace=True)
    df_out.dropna(how='any', inplace=True)
    data = df_out
    #making a single column of all entities
    node_table = pd.concat([data['source'], data['target']], axis=0)
    print(node_table.shape)
    #removing any duplicated nodes
    node_table = node_table.drop_duplicates()
    print(node_table.shape)
    
    
    node_types = pd.DataFrame(columns=['node', 'class'])
    #running a new SPARQL query for each node to extract a list of its types
    for node in node_table:
        node = str(node).replace(' ', '_')
        qres = g.query(
            """
            SELECT  ?node_class 
            WHERE{
          <http://wrenand.co.uk/fpn/%s> rdf:type ?node_class . 
        } 
            """ % node)
        type_list = list()
        
        for row in qres:
            #ignore axiomatic types
            if 'owl' not in str(row.node_class):
                  type_list.append(row.node_class.replace('http://wrenand.co.uk/fpn/', ''))
        #if no type information has been retrieved for a node, it is a Literal
        if len(type_list) == 0:
              type_list.append('Literal')
        node_types = node_types.append({'node' : node, 'class' : type_list}, ignore_index=True)
    #produce a dictionary with nodes as keys and the type list as values
    type_dict = {}
    for index,row in node_types.iterrows():
        type_dict[row[0]] = row[1]
    
    #Produce node data in visualisation-friendly format to dump into a json
    nodes = list()
    for node in node_table:
        nodes.append({'data': {'id': str(node), 'label': str(node).replace('_', ' ')}, 'classes': type_dict[str(node).replace(' ', '_')]})
        
    #and do the same for edge data
    edges = [
        {'data': {'source': row[0], 'target': row[2], 'label': row[1]}}
        for index, row in data.iterrows()
    ]
    #combine the two, and save as a json
    default_elements = nodes + edges
    with open('13-8_elements_file.json', 'w', encoding ='utf8') as json_file:
        json.dump(default_elements, json_file)
    #Now extracting a new table of all nodes (as before) to use for lexical-similarity search    
    print('Extracting Elements')
    qres = g.query(
            """
            SELECT ?s ?o
            WHERE{
            ?s ?p ?o . 
    
            } 
            """ )
    df = pd.DataFrame(columns=['source', 'target'])
    for row in qres:
            df = df.append(
                {'source': row.s, 'target': row.o}, ignore_index=True)
    
    print(df.shape)
    df_out = df.drop_duplicates()
    print(df_out.shape)
    df_out = df_out.replace('http://wrenand.co.uk/fpn/', '', regex=True)
    print(df_out.shape)
    df_out = df_out.drop_duplicates()
    df_out.replace("", float("NaN"), inplace=True)
    df_out.dropna(how='any', inplace=True)
    data = df_out
    
    node_table = pd.concat([data['source'], data['target']], axis=0)
    print(node_table.head())
    node_table = node_table.drop_duplicates()
    #create a table for dissimilarity scores, initially all zero, and save as csv
    node_lex = pd.DataFrame(columns=['node', 'score'])
    node_lex['node'] = node_table
    node_lex['score'] = 0
    node_lex.to_csv('13-8-nodes.csv', index=False)
    print(node_lex.shape)
    
def extractOnto():
    g = Graph()
    print("Extracting Data")

    g.parse("13-8-inference.ttl", format="ttl")
    
    
    #SPARQL query to extract all classes
    print('Extracting Elements')
    qres = g.query(
            """
            SELECT *
            WHERE{
           ?s a owl:Class .
           ?s ?p ?o . 
           ?o a owl:Class .
           
            } 
            """ )
    df = pd.DataFrame(columns=['source', 'interaction', 'target'])
    for row in qres:
            df = df.append(
                {'source': row.s, 'interaction': row.p, 'target': row.o}, ignore_index=True)
    
    print(df.shape)
    df_out = df.drop_duplicates()
    print(df_out.shape)
    #removing all namespaces (there are more here to deal with)
    df_out = df_out.replace('http://wrenand.co.uk/fpn/', '', regex=True)
    df_out = df_out.replace('http://www.w3.org/2002/07/owl#', '', regex=True)
    df_out = df_out.replace('http://www.w3.org/1999/02/22-rdf-syntax-ns#', '', regex=True)
    df_out = df_out.replace('http://www.w3.org/2000/01/rdf-schema#', '', regex=True)
    df_out = df_out.replace('http://www.w3.org/2001/XMLSchema#', '', regex=True)
    print(df_out.shape)
    #remove reflexive class triples as these are unhelpful for humans
    df_out = df_out[(df_out['source'] != df_out['target'])]
    #remove disjointedness triples: counterintuitive to visualise
    df_out = df_out[(df_out['interaction'] != 'disjointWith')]
    print(df_out.shape) 
    print(df_out)
    df_out = df_out.drop_duplicates()
    df_out.replace("", float("NaN"), inplace=True)
    df_out.dropna(how='any', inplace=True)
    data = df_out
    
    node_table = pd.concat([data['source'], data['target']], axis=0)
    print(node_table.shape)
    node_table = node_table.drop_duplicates()
    print(node_table.shape)
    
    #as before, retrieve all classes for these nodes and serialise into a json
    node_types = pd.DataFrame(columns=['node', 'class'])
    for node in node_table:
        node = str(node).replace(' ', '_')
        qres = g.query(
            """
            SELECT  ?node_class 
            WHERE{
          <http://wrenand.co.uk/fpn/%s> rdfs:subClassOf ?node_class . 
        } 
            """ % node)
        type_list = list()
        
        for row in qres:
            if 'owl' not in str(row.node_class):
                  type_list.append(row.node_class.replace('http://wrenand.co.uk/fpn/', ''))
        if len(type_list) == 0:
              type_list.append('Literal')
        node_types = node_types.append({'node' : node, 'class' : type_list}, ignore_index=True)
    type_dict = {}
    for index,row in node_types.iterrows():
        type_dict[row[0]] = row[1]
    
    
    nodes = list()
    for node in node_table:
        nodes.append({'data': {'id': str(node), 'label': str(node).replace('_', ' ')}, 'classes': type_dict[str(node).replace(' ', '_')]})
        
    
    edges = [
        {'data': {'source': row[0], 'target': row[2], 'label': row[1]}}
        for index, row in data.iterrows()
    ]
    default_elements = nodes + edges
    with open('onto_elements.json', 'w', encoding ='utf8') as json_file:
        json.dump(default_elements, json_file)

def extractMap():
    g = Graph()
    g.parse("13-8-inference.ttl", format="ttl")
    
    print("Extracting Data")
    
    #Query to extract all classes as before
    print('Extracting Elements')
    qres = g.query(
            """
            SELECT *
            WHERE{
           ?s a owl:Class .
           ?s ?p ?o . 
           ?o a owl:Class .
           
            } 
            """ )
    df = pd.DataFrame(columns=['source', 'interaction', 'target'])
    for row in qres:
            df = df.append(
                {'source': row.s, 'interaction': row.p, 'target': row.o}, ignore_index=True)
    print(df.shape)
    #query to extract all object properties that have defined domain and range
    metaqres = g.query(
        """
            SELECT *
            WHERE{
           ?p a owl:ObjectProperty .
           ?p rdfs:domain ?dom . 
           ?p rdfs:range ?ran .
           
            } 
            """ )
    for row in metaqres:
            df = df.append(
                {'source': row.dom, 'interaction': row.p, 'target': row.ran}, ignore_index=True)
    #creating triples to enable visualisation of the top-level interactions.
    #These have not been extracted becasue they do not have a defined domain and/or range.
    df = df.append({'source': 'Actor', 'interaction': 'takeAction', 'target': 'Action'}, ignore_index=True)
    df = df.append({'source': 'Action', 'interaction': 'actionImpacts', 'target': 'Actor'}, ignore_index=True)
    df = df.append({'source': 'Actor', 'interaction': 'locatedIn', 'target': 'Place'}, ignore_index=True)
    df = df.append({'source': 'Article', 'interaction': 'usesMethod', 'target': 'Method'}, ignore_index=True)
    df = df.append({'source': 'Article', 'interaction': 'citations', 'target': 'Citations'}, ignore_index=True)
    df = df.append({'source': 'Action', 'interaction': 'significance', 'target': 'Description'}, ignore_index=True)
    df = df.append({'source': 'Action', 'interaction': 'source', 'target': 'URL'}, ignore_index=True)
    df = df.append({'source': 'Journal', 'interaction': 'impactFactor', 'target': 'impactFactor'}, ignore_index=True)
    df = df.append({'source': 'Journal', 'interaction': 'peerReviewed', 'target': 'Y/N'}, ignore_index=True)
    df = df.append({'source': 'Action', 'interaction': 'date', 'target': 'Date'}, ignore_index=True)
     
    
    #as before, creating a node table, using this to extract classes, and dumping into a json. 
    print(df.shape)
    df_out = df.drop_duplicates()
    print(df_out.shape)
    df_out = df_out.replace('http://wrenand.co.uk/fpn/', '', regex=True)
    df_out = df_out.replace('http://www.w3.org/2002/07/owl#', '', regex=True)
    df_out = df_out.replace('http://www.w3.org/1999/02/22-rdf-syntax-ns#', '', regex=True)
    df_out = df_out.replace('http://www.w3.org/2000/01/rdf-schema#', '', regex=True)
    df_out = df_out.replace('http://www.w3.org/2001/XMLSchema#', '', regex=True)
    print(df_out.shape)
    df_out = df_out[(df_out['source'] != df_out['target'])]
    df_out = df_out.append({'source': 'Actor', 'interaction': 'interactWith', 'target': 'Actor'}, ignore_index=True)
    df_out = df_out[(df_out['interaction'] != 'disjointWith')]
    print(df_out.shape) 
    print(df_out)
    df_out = df_out.drop_duplicates()
    df_out.replace("", float("NaN"), inplace=True)
    df_out.dropna(how='any', inplace=True)
    data = df_out
    
    node_table = pd.concat([data['source'], data['target']], axis=0)
    print(node_table.shape)
    node_table = node_table.drop_duplicates()
    print(node_table.shape)
    
    
    node_types = pd.DataFrame(columns=['node', 'class'])
    for node in node_table:
        node = str(node).replace(' ', '_')
        qres = g.query(
            """
            SELECT  ?node_class 
            WHERE{
          <http://wrenand.co.uk/fpn/%s> rdfs:subClassOf ?node_class . 
        } 
            """ % node)
        type_list = list()
        
        for row in qres:
            if 'owl' not in str(row.node_class):
                  type_list.append(row.node_class.replace('http://wrenand.co.uk/fpn/', ''))
        if len(type_list) == 0:
              type_list.append('Literal')
        node_types = node_types.append({'node' : node, 'class' : type_list}, ignore_index=True)
    type_dict = {}
    for index,row in node_types.iterrows():
        type_dict[row[0]] = row[1]
    
    
    nodes = list()
    for node in node_table:
        nodes.append({'data': {'id': str(node), 'label': str(node).replace('_', ' ')}, 'classes': type_dict[str(node).replace(' ', '_')]})
        
    
    edges = [
        {'data': {'source': row[0], 'target': row[2], 'label': row[1]}}
        for index, row in data.iterrows()
    ]
    default_elements = nodes + edges
    with open('map_elements.json', 'w', encoding ='utf8') as json_file:
        json.dump(default_elements, json_file)
                   
createDummyGraph()
createDummyLitGraph()         
OWLRLInference()   
elementExtraction()  
extractOnto()
extractMap()