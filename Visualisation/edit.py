#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 14:42:41 2021

@author: ollie
"""


from rdflib import Graph
import pandas as pd


import os
import json
import numpy as np
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import Levenshtein as lev

import dash_cytoscape as cyto

g = Graph()
#import knowledge graph
g.parse("13-8-inference.ttl", format="ttl")
#import table of all nodes for similarity-scoring
node_lex = pd.read_csv('13-8-nodes.csv')

def sim_score(a, b):
    #function for computing standardised lexical similarity scores
    #put both terms into lowercase to remove case sensitivity
    a = a.lower()
    b = b.lower()
    #set the denominator as the longer term length to avoid values greater than 1
    denom = len(b)
    if len(a) > len(b):
        denom = len(a)
    #calculate the levenshtein distance as a proportion of the longer term length
    c = (lev.distance(a, b) / denom)
    return c



#setting up dash cytoscape
asset_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', 'assets'
)

app = dash.Dash(__name__, assets_folder=asset_path)
server = app.server
cyto.load_extra_layouts()

#import json of precomputed positions for class hierarchy view
with open('onto-positions.json') as f:
    onto_elements = json.loads(f.read())

#import json of precomputed positions for class schema view
with open('map_pos.json') as f:
    map_elements = json.loads(f.read())

#default html styling elements
styles = {
    'json-output': {
        'overflow-y': 'scroll',
        'height': 'calc(0.45*(20vh)',
        'border': 'thin lightgrey solid',
    },
    'tab': {'height': 'calc(20vh-100px)'}
}
#stylesheet for hiding some classes exclusive to Literature Review data
dd_style=[
                {
            'selector': '.Academic',
            'style': {
               'display': 'none'
            }
        }, 
                  
                   {
            'selector': '.Article',
            'style': {
               'display': 'none'
            }
        }, 
                    
            {
                'selector': '.Method',
                'style':{
                    'display': 'none',

                    }
                },
            
        {
            'selector': '.Publication',
            'style': {
                'display': 'none',

            }
        }, 
        ]    

#default stylesheet
all_style = [
                {
                'selector': 'edge',
                'style': {'width':'1',
                          'content': 'data(label)',
                          'text-rotation':'autorotate',
                          'text-opacity': 0.8,
                          'text-background-shape':'rounded-rectangle',
                          'text-background-color':'white',
                          'text-background-opacity':0.7,
                          'font-family':'helvetica',
                          'font-style':'italic',
                          'font-size': 11,
                          'font-weight':'thin',
                          'target-distance-from-node':'5px',
                          'target-endpoint':'outside-to-node-or-label',
                          'line-opacity': '0.7',
                          'curve-style': 'bezier',
                          'control-point-step-size':'100',
                          'control-point-weight':0.2,
                          'target-arrow-shape': 'vee',
                          'arrow-scale': 2,
                          'min-zoomed-font-size':16,
                          }
                },
              
                {
                'selector': 'edge[label="equivalentClass"]',
                'style': {
                        'visibility': 'hidden'
                        }
                },
                
                {
                'selector': 'node[label="Thing"]',
                'style': {
                        'display': 'none'
                        }
                },
                                
                {
                'selector': 'node[label="Nothing"]',
                'style': {
                        'display': 'none'
                        }
                },
                                                
                {
                    'selector': '.Actor',
                    'style': {
                            'width':'20',
                            'height':'20',
                            'background-color': '#fb8072',
                            'border-color':'black',
                            'border-width':'1',
                            'shape':'star',
                            'content': 'data(label)',
                            'text-wrap': 'wrap',
                            'text-max-width': '200px',
                            'text-overflow-wrap': 'whitespace',
                            'text-valign': 'top',
                            'text-background-color': '#FFFFFF',
                            'text-background-shape': 'round-rectangle',
                            'text-background-opacity': '0.7',
                            'font-size': 14,
                            'font-weight':'bold',
                            'font-family':'times-new-roman',
                            'min-zoomed-font-size':16,
                            }   
                },
                
                  {
                      'selector': '.Action',
                      'style': {                
                              'width':'20',
                              'height':'20',
                              'background-color': '#b3de69',
                              'border-color':'black',
                              'border-width':'1',
                              'shape':'triangle',
                              'content': 'data(label)',
                              'text-wrap': 'wrap',
                              'text-max-width': '200px',
                              'text-overflow-wrap': 'whitespace',
                              'text-valign': 'top',
                              'text-background-color': '#FFFFFF',
                              'text-background-shape': 'round-rectangle',
                              'text-background-opacity': '0.7',
                              'font-size': 14,
                              'font-weight':'bold',
                              'font-family':'times-new-roman',
                              'min-zoomed-font-size':16,
                              }
                  }, 
                  
                  {
                      'selector': '.Issue',
                      'style': {
                              'width':'20',
                              'height':'20',
                              'background-color': '#80b1d3',
                              'border-color':'black',
                              'border-width':'1',
                              'shape':'rectangle',
                              'content': 'data(label)',
                              'text-wrap': 'wrap',
                              'text-max-width': '200px',
                              'text-overflow-wrap': 'whitespace',
                              'text-valign': 'top',
                              'text-background-color': '#FFFFFF',
                              'text-background-shape': 'round-rectangle',
                              'text-background-opacity': '0.7',
                              'font-size': 14,
                              'font-weight':'bold',
                              'font-family':'times-new-roman',
                              'min-zoomed-font-size':16,
                              }
                  }, 
                  
                  {
                      'selector': '.Method',
                      'style':{
                              'width':'20',
                              'height':'20',
                              'background-color': '#ffffb3',
                              'border-color':'black',
                              'border-width':'1',
                              'shape':'ellipse',
                              'content': 'data(label)',
                              'text-wrap': 'wrap',
                              'text-max-width': '200px',
                              'text-overflow-wrap': 'whitespace',
                              'text-valign': 'top',
                              'text-background-color': '#FFFFFF',
                              'text-background-shape': 'round-rectangle',
                              'text-background-opacity': '0.7',
                              'font-size': 14,
                              'font-weight':'bold',
                              'font-family':'times-new-roman',
                              'min-zoomed-font-size':16,
                              }
                },
                  
                  {
                      'selector': '.Place',
                      'style': {        
                              'width':'20',
                              'height':'20',
                              'background-color': '#fdb462',
                              'border-color':'black',
                              'border-width':'1',
                              'shape':'vee',
                              'content': 'data(label)',
                              'text-wrap': 'wrap',
                              'text-max-width': '200px',
                              'text-overflow-wrap': 'whitespace',
                              'text-valign': 'top',
                              'text-background-color': '#FFFFFF',
                              'text-background-shape': 'round-rectangle',
                              'text-background-opacity': '0.7',
                              'font-size': 14,
                              'font-weight':'bold',
                              'font-family':'times-new-roman',
                              'min-zoomed-font-size':16,
                              }
                  },
                  
                  {
                      'selector': '.Publication',
                      'style': {        
                              'width':'20',
                              'height':'20',
                              'background-color': '#8dd3c7',
                              'border-color':'black',
                              'border-width':'1',
                              'shape':'diamond',
                              'content': 'data(label)',
                              'text-wrap': 'wrap',
                              'text-max-width': '200px',
                              'text-overflow-wrap': 'whitespace',
                              'text-valign': 'top',
                              'text-background-color': '#FFFFFF',
                              'text-background-shape': 'round-rectangle',
                              'text-background-opacity': '0.7',
                              'font-size': 14,
                              'font-weight':'bold',
                              'font-family':'times-new-roman',
                              'min-zoomed-font-size':16,
                              }
                      }, 
                  
                  {
                      'selector': '.Literal',
                      'style': {        
                              'width':'20',
                              'height':'20',
                              'background-color': '#d9d9d9',
                              'border-color':'black',
                              'border-width':'1',
                              'shape':'concave-hexagon',
                              'content': 'data(label)',
                              'text-wrap': 'ellipsis',
                              'text-max-width': '200px',
                              'text-overflow-wrap': 'whitespace',
                              'text-valign': 'top',
                              'text-background-color': '#FFFFFF',
                              'text-background-shape': 'round-rectangle',
                              'text-background-opacity': '0.2',
                              'font-size': 14,        
                              'font-weight':'bold',
                              'font-family':'times-new-roman',
                              'min-zoomed-font-size':16,
                              }
                  }, 
            
                {
                    'selector': ':selected',
                    'style': {        
                            'width':'20',
                            'height':'20',
                            'background-color': '#bc80bd',
                            'border-color':'black',
                            'border-width':'1',
                            'content': 'data(label)',
                            'text-wrap': 'wrap',
                            'text-max-width': '200px',
                            'text-overflow-wrap': 'whitespace',
                            'text-valign': 'top',
                            'text-background-color': '#FFFFFF',
                            'text-background-shape': 'round-rectangle',
                            'text-background-opacity': '0.7',
                            'font-size': 14,
                            'font-weight':'bold',
                            'font-family':'times-new-roman',
                            }
                },
        ]

#import json of precomputed positions for entire dataset view
with open('positions.json') as f:
    full_data = json.loads(f.read())


#layout for dash app
app.layout = html.Div([
    html.Div(className='eight columns', children=[
        
        
        #the network
          cyto.Cytoscape(
            id='food-pol-net',
            #allow box selection using shift+click & drag
            boxSelectionEnabled= True,
            #initial data = data for all nodes
            elements=full_data,
            #initial layout is precomputed, with spacing factor of 4 for scaling
            layout={
                'name': 'preset','spacingFactor':'4'
            },
            #limit vertical height to allow for tabs
            style={
                'height': '74vh',
                'width': '100%'
            },
            #initially hide Lit Review data
            stylesheet=all_style + dd_style
        ),
        #tabs
        html.Div(className='four columns', children=[
        dcc.Tabs(id='tabs', children=[
            
            #Legend for classes, using colour codes and unicode symbols corresponding to shapes
            dcc.Tab(label='Legend', children=[
                html.Div(style=styles['tab'], children=[
                    html.P(children=['Classes:',
                    html.Div(),
                    html.Button('Actor \u2606', style={'background-color': '#fb8072', 'fontSize': 13}),
                    html.Button('Action \u25B3', style={'background-color': '#b3de69', 'fontSize': 13}),
                    html.Button('Issue \u25A1', style={'background-color': '#80b1d3', 'fontSize': 13}),
                    html.Button('Method \u25EF', style={'background-color': '#ffffb3', 'fontSize': 13}),
                    html.Button('Place V', style={'background-color': '#fdb462', 'fontSize': 13}),
                    html.Button('Publication \u25C7', style={'background-color': '#8dd3c7', 'fontSize': 13}),
                    html.Button('Literal/Descriptive \u29D6', style={'background-color': '#d9d9d9', 'fontSize': 13}),
                    ]),
                    html.P(children=['On Selection:',
                    html.Div(),
                    html.Button('Selected Node/Edge(s)', style={'background-color': '#bc80bd', 'fontSize': 13}),
                    html.Div(),
                    html.Button('Edges To Selected Node', style={'background-color': '#fccde5', 'fontSize': 13}),
                    html.Button('Edges From Selected Node', style={'background-color': '#bebada', 'fontSize': 13}),
                    ])])
                ]),
            
            #tab to provide details on demand, in lieu of tooltip functionality
            dcc.Tab(label='Selected Node Info', children=[
                html.Div(style=styles['tab'], children=[
                    html.P('Selected Node Data'),
                    html.Pre(
                        id='tap-node-data',
                        style=styles['json-output']
                    ),                    
                   
                        ])
                    ]),  
            
            #tab to provide explore, search and domain-specific pathway functionality, with access to precomputed views
            dcc.Tab(label='Navigation', children=[
                html.Div(style=styles['tab'], children=[
                    html.P(children=['Search:',
                    dcc.Input(id='search-box', type='text', placeholder='Search Term e.g. NFPOs'),
                    html.Button("Search", id='search-button')]),
                    
                    html.P(children=['Explore:',
                    html.Button("Focus On Selected Node(s)", id='focus-button'),       
                    html.Button("Expand Selected Node(s)", id='expand-button')]),

                    html.P(children=['Load Interaction Pathways:',
                    html.Button("Show Actor-Action-Issue Paths", id='path-button'),
                    html.Button("Show Actor-Action-Actor Paths", id='aapath-button')]),
                    html.P(children=['Load Overviews',
                    html.Button("Load Entire Dataset", id='full-button'),
                    html.Button("Load Class Hierarchy", id='onto-button'),
                    html.Button("Load Class Schema", id='map-button')]),
                    
                    ])
                ]),
            
            #tab to provide display options, to show or hide nodes/edges
             dcc.Tab(label='Display Options', children=[
                html.Div(style=styles['tab'], children=[

                    
                    html.P('Node Display Options:'),
                    dcc.RadioItems(
                    id='display-radio',
                    options=[{'label': 'Hide Academics, Articles, Methods & Publications', 'value': 'dummy-button'}, 
                             {'label': 'Show All Data', 'value': 'all-button'}], value='dummy-button'),
                    
                    dcc.Checklist(
                        id="nodes-checklist",
                        options=[
                        {"label": "Actor", "value": "Actor"},
                         {"label": "Action", "value": "Action"},
                         {"label": "Issue", "value": "Issue"},
                         {"label": "Place", "value": "Place"},
                         {"label": "Publication", "value": "Publication"},
                         {"label": "Method", "value": "Method"},
                         {"label": "Descriptive Info", "value": "Literal"},

                        ],
                        value=['Actor', 'Action', 'Issue'],),
                   
                    html.P('Hidden Edges:'),
                    dcc.Checklist(
                        id="edges-checklist",
                        options=[
                        {"label": "actionImpacts", "value": "actionImpacts"},
                        {"label": "activeIn", "value": "activeIn"},
                        {"label": "concernsPlace", "value": "concernsPlace"},
                        {"label": "interactWith", "value": "interactWith"},
                        {"label": "issueIn", "value": "issueIn"},
                        {"label": "locatedIn", "value": "locatedIn"},
                        {"label": "publishedIn", "value": "publishedIn"},
                        {"label": "relatesTo", "value": "relatesTo"},
                        {"label": "takeAction", "value": "takeAction"},
                        {"label": "usesMethod", "value": "usesMethod"},
                        {"label": "workingOn", "value": "workingOn"},
                        {"label": "wrote", "value": "wrote"},
                        {"label": "subClassOf", "value": "subClassOf"},
                        {"label": "type", "value": "type"},
                        
                        ],
                        value=[],
                        labelStyle={"display": "inline-block"},
                    )                
                    ])
                ]),
             
             #tab to provide create/manage functionality through adding/deleting data from view
             dcc.Tab(label='Editing Toolkit', children=[
                html.Div(style=styles['tab'], children=[
                    
                    html.P(children=['Add Node:', dcc.Input(id='node-name', type='text', placeholder='Name (e.g. Trussell Trust)'),
                    dcc.Input(id='node-class', type='text', placeholder='Classes (e.g. Actor, Charity, Group)'),
                    html.Button("Add Node", id='node-button')]),

                    html.P(children=['Connect Selected Nodes:', dcc.Input(id='edge-name', type='text', placeholder='Edge Label (e.g. worksFor)'), html.Button("Connect Nodes", id='edge-button')]),                 
           
                    html.P(children=['Remove Selected Node(s)/Edge(s):',html.Button("Remove Selected", id='remove-button')]),
                    
                    ])
                ]),
             
            
        ]),
    ]),
        
       
  
    
    
])
])

#dash callback to provide interactive functionality
@app.callback((Output('food-pol-net', 'elements'),
                Output('food-pol-net', 'layout'),
                Output('food-pol-net', 'stylesheet')),
              [Input('food-pol-net', 'tapNode'),
               Input('food-pol-net', 'selectedEdgeData'),
               Input('full-button', 'n_clicks'),
               Input('node-name', 'value'),
                Input('node-class', 'value'),
                Input('node-button', 'n_clicks'),
                Input('edge-name', 'value'),
                Input('edge-button', 'n_clicks'),
                Input('onto-button', 'n_clicks'),
                Input('path-button', 'n_clicks'),
                Input('map-button', 'n_clicks'),
                Input('aapath-button', 'n_clicks'),
                Input('display-radio', 'value'),
                Input("nodes-checklist", "value"),
                Input("edges-checklist", "value"),
                Input('search-button', 'n_clicks'),
                Input('remove-button', 'n_clicks'),
                Input('expand-button', 'n_clicks'),
                Input('focus-button', 'n_clicks'),
                ],
              [State('food-pol-net', 'elements'),
                State('food-pol-net', 'layout'),
                State('food-pol-net', 'stylesheet'),
                State('search-box', 'value'),
                State('food-pol-net', 'selectedNodeData'),
                State('food-pol-net', 'selectedEdgeData'),
                ]
              )
def function(tapnode, tapedge, full_button, nname, nclass, ngen, ename, egen, onto_button, path_button, map_button, aa_path, display, nodes, edges, search_button, remove_button, expand_button, focus, elements, layout, stylesheet, search_term, data_n, data_e):
    #repeat of earlier stylesheets needed within callback function
    dd_style=[
                {
            'selector': '.Academic',
            'style': {
               'display': 'none'
            }
        }, 
                  
                   {
            'selector': '.Article',
            'style': {
               'display': 'none'
            }
        }, 
                    
            {
                'selector': '.Method',
                'style':{
                    'display': 'none',

                    }
                },
            
        {
            'selector': '.Publication',
            'style': {
                'display': 'none',

            }
        }, 
        ]    

    all_style = [
                {
                'selector': 'edge',
                'style': {'width':'1',
                          'content': 'data(label)',
                          'text-rotation':'autorotate',
                          'text-opacity': 0.8,
                          'text-background-shape':'rounded-rectangle',
                          'text-background-color':'white',
                          'text-background-opacity':0.7,
                          'font-family':'helvetica',
                          'font-style':'italic',
                          'font-size': 11,
                          'font-weight':'thin',
                          'target-distance-from-node':'5px',
                          'target-endpoint':'outside-to-node-or-label',
                          'line-opacity': '0.7',
                          'curve-style': 'bezier',
                          'control-point-step-size':'100',
                          'control-point-weight':0.2,
                          'target-arrow-shape': 'vee',
                          'arrow-scale': 2,
                          'min-zoomed-font-size':16,
                          }
                },
              
                {
                'selector': 'edge[label="equivalentClass"]',
                'style': {
                        'visibility': 'hidden'
                        }
                },
                
                {
                'selector': 'node[label="Thing"]',
                'style': {
                        'display': 'none'
                        }
                },
                                
                {
                'selector': 'node[label="Nothing"]',
                'style': {
                        'display': 'none'
                        }
                },
                                                
                {
                    'selector': '.Actor',
                    'style': {
                            'width':'20',
                            'height':'20',
                            'background-color': '#fb8072',
                            'border-color':'black',
                            'border-width':'1',
                            'shape':'star',
                            'content': 'data(label)',
                            'text-wrap': 'wrap',
                            'text-max-width': '200px',
                            'text-overflow-wrap': 'whitespace',
                            'text-valign': 'top',
                            'text-background-color': '#FFFFFF',
                            'text-background-shape': 'round-rectangle',
                            'text-background-opacity': '0.7',
                            'font-size': 14,
                            'font-weight':'bold',
                            'font-family':'times-new-roman',
                            'min-zoomed-font-size':16,
                            }   
                },
                
                  {
                      'selector': '.Action',
                      'style': {                
                              'width':'20',
                              'height':'20',
                              'background-color': '#b3de69',
                              'border-color':'black',
                              'border-width':'1',
                              'shape':'triangle',
                              'content': 'data(label)',
                              'text-wrap': 'wrap',
                              'text-max-width': '200px',
                              'text-overflow-wrap': 'whitespace',
                              'text-valign': 'top',
                              'text-background-color': '#FFFFFF',
                              'text-background-shape': 'round-rectangle',
                              'text-background-opacity': '0.7',
                              'font-size': 14,
                              'font-weight':'bold',
                              'font-family':'times-new-roman',
                              'min-zoomed-font-size':16,
                              }
                  }, 
                  
                  {
                      'selector': '.Issue',
                      'style': {
                              'width':'20',
                              'height':'20',
                              'background-color': '#80b1d3',
                              'border-color':'black',
                              'border-width':'1',
                              'shape':'rectangle',
                              'content': 'data(label)',
                              'text-wrap': 'wrap',
                              'text-max-width': '200px',
                              'text-overflow-wrap': 'whitespace',
                              'text-valign': 'top',
                              'text-background-color': '#FFFFFF',
                              'text-background-shape': 'round-rectangle',
                              'text-background-opacity': '0.7',
                              'font-size': 14,
                              'font-weight':'bold',
                              'font-family':'times-new-roman',
                              'min-zoomed-font-size':16,
                              }
                  }, 
                  
                  {
                      'selector': '.Method',
                      'style':{
                              'width':'20',
                              'height':'20',
                              'background-color': '#ffffb3',
                              'border-color':'black',
                              'border-width':'1',
                              'shape':'ellipse',
                              'content': 'data(label)',
                              'text-wrap': 'wrap',
                              'text-max-width': '200px',
                              'text-overflow-wrap': 'whitespace',
                              'text-valign': 'top',
                              'text-background-color': '#FFFFFF',
                              'text-background-shape': 'round-rectangle',
                              'text-background-opacity': '0.7',
                              'font-size': 14,
                              'font-weight':'bold',
                              'font-family':'times-new-roman',
                              'min-zoomed-font-size':16,
                              }
                },
                  
                  {
                      'selector': '.Place',
                      'style': {        
                              'width':'20',
                              'height':'20',
                              'background-color': '#fdb462',
                              'border-color':'black',
                              'border-width':'1',
                              'shape':'vee',
                              'content': 'data(label)',
                              'text-wrap': 'wrap',
                              'text-max-width': '200px',
                              'text-overflow-wrap': 'whitespace',
                              'text-valign': 'top',
                              'text-background-color': '#FFFFFF',
                              'text-background-shape': 'round-rectangle',
                              'text-background-opacity': '0.7',
                              'font-size': 14,
                              'font-weight':'bold',
                              'font-family':'times-new-roman',
                              'min-zoomed-font-size':16,
                              }
                  },
                  
                  {
                      'selector': '.Publication',
                      'style': {        
                              'width':'20',
                              'height':'20',
                              'background-color': '#8dd3c7',
                              'border-color':'black',
                              'border-width':'1',
                              'shape':'diamond',
                              'content': 'data(label)',
                              'text-wrap': 'wrap',
                              'text-max-width': '200px',
                              'text-overflow-wrap': 'whitespace',
                              'text-valign': 'top',
                              'text-background-color': '#FFFFFF',
                              'text-background-shape': 'round-rectangle',
                              'text-background-opacity': '0.7',
                              'font-size': 14,
                              'font-weight':'bold',
                              'font-family':'times-new-roman',
                              'min-zoomed-font-size':16,
                              }
                      }, 
                  
                  {
                      'selector': '.Literal',
                      'style': {        
                              'width':'20',
                              'height':'20',
                              'background-color': '#d9d9d9',
                              'border-color':'black',
                              'border-width':'1',
                              'shape':'concave-hexagon',
                              'content': 'data(label)',
                              'text-wrap': 'ellipsis',
                              'text-max-width': '200px',
                              'text-overflow-wrap': 'whitespace',
                              'text-valign': 'top',
                              'text-background-color': '#FFFFFF',
                              'text-background-shape': 'round-rectangle',
                              'text-background-opacity': '0.2',
                              'font-size': 14,        
                              'font-weight':'bold',
                              'font-family':'times-new-roman',
                              'min-zoomed-font-size':16,
                              }
                  }, 
            
                {
                    'selector': ':selected',
                    'style': {        
                            'width':'20',
                            'height':'20',
                            'background-color': '#bc80bd',
                            'border-color':'black',
                            'border-width':'1',
                            'content': 'data(label)',
                            'text-wrap': 'wrap',
                            'text-max-width': '200px',
                            'text-overflow-wrap': 'whitespace',
                            'text-valign': 'top',
                            'text-background-color': '#FFFFFF',
                            'text-background-shape': 'round-rectangle',
                            'text-background-opacity': '0.7',
                            'font-size': 14,
                            'font-weight':'bold',
                            'font-family':'times-new-roman',
                            }
                },
        ]
    #retrieve the context for the triggered state
    ctx = dash.callback_context
    #determine which button was pushed
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    #list of all node superclasses
    nodes_list = ['Actor', 'Action', 'Issue', 'Place', 'Publication', 'Method', 'Literal']
   
    #if the 'load entire dataset' button is pushed, load & display that dataset with precomputed positions
    if (button_id == 'full-button'):
        elements = full_data
        return (elements, {'name': 'preset', 'spacingFactor':'4'},  stylesheet)
    
    #if the 'load class hierarchy' button is pushed, load & display that dataset with precomputed positions
    if (button_id == 'onto-button'):
        elements = onto_elements
        return (elements, {'name': 'preset'},  stylesheet)

    #if the 'load class schema' button is pushed, load & display that dataset with precomputed positions
    if (button_id == 'map-button'):
        elements = map_elements
        return (elements, {'name': 'preset'},  stylesheet)          
    
    #if the 'actor-action-issue' path button is pushed:
    if (button_id == 'path-button'):
        #run a SPARQL query to retrieve all entities and interactions linked using the relevant top-level object properties
        qres = g.query(
        """
        SELECT ?actor1 ?gen ?action ?rel ?issue 
        WHERE{
        
       ?action fp:relatesTo ?issue .
       ?action ?rel ?issue .

       ?actor1 fp:takeAction ?action .
       ?actor1 ?gen ?action .
        }
        """ )
        
        #build a dataframe of the output to enable vectorised application of relevant string methods
        df = pd.DataFrame(columns=['source','interaction','target'])
        for row in qres:
               df= df.append({'source': row.action, 'interaction': row.rel, 'target': row.issue}, ignore_index=True)
               df= df.append({'source': row.actor1, 'interaction': row.gen, 'target': row.action}, ignore_index=True)
            
        df_out = df.drop_duplicates()
        df_out = df_out[~(df_out['interaction'].str.contains('rdf'))]
        df_out = df_out[~(df_out['interaction'].str.contains('owl'))]
        df_out = df_out.replace('http://wrenand.co.uk/fpn/', '', regex=True)
        df_out = df_out.drop_duplicates()
        df_out.replace("", float("NaN"), inplace=True)
        df_out.dropna(how='any', inplace=True)
        data = df_out
        
        #produce a table of all the new nodes
        new_node_table = pd.concat([data['source'], data['target']], axis=0)
        new_node_table = new_node_table.drop_duplicates() 
        node_types = pd.DataFrame(columns=['node', 'class'])
        
        #run a new SPARQL query for EACH node to retrieve a list of all of its classes
        for node in new_node_table:
            node = str(node).replace(' ', '_')
            qres = g.query(
                """
                SELECT  ?node_class 
                WHERE{
              <http://wrenand.co.uk/fpn/%s> rdf:type ?node_class . 
            } 
                """ % node)
            #create an empty list of types, fill it with all non-axiomatic types returned by the query above, if there are no returned types it is a Literal.
            type_list = list()
            for row in qres:
                    if 'owl' not in str(row.node_class):
                        type_list.append(row.node_class.replace('http://wrenand.co.uk/fpn/', ''))
            if len(type_list) == 0:
                    type_list.append('Literal')
            node_types = node_types.append({'node' : node, 'class' : type_list}, ignore_index=True)
        
        #putting new data into format for visualisation
        type_dict = {}
        for index,row in node_types.iterrows():
            type_dict[row[0]] = row[1]
            
        new_nodes = list()
        for node in new_node_table:
            new_nodes.append({'data': {'id': str(node), 'label': str(node).replace('_', ' ')}, 'classes': type_dict[str(node).replace(' ', '_')]})
    
        new_edges = [
            {'data': {'source': row[0], 'target': row[2], 'label': row[1]}}
            for index, row in data.iterrows()
        ]
        new_elements = new_nodes + new_edges
        #returning these elements, with a compound-spring layout, with current stylesheet.    
        return (new_elements, {'name': 'cose-bilkent', 'spacingFactor':'3'}, stylesheet)
        
    #if the 'actor-action-issue' path button is pushed:
    if (button_id == 'aapath-button'):
        #run a SPARQL query to retrieve all entities and interactions linked using the relevant top-level object properties
        qres = g.query(
        """
        SELECT ?actor1 ?gen ?action ?imp ?actor2 
        WHERE{
       ?actor1 fp:takeAction ?action .
        ?actor1 ?gen ?action .
       ?action fp:actionImpacts ?actor2 .
       ?action ?imp ?actor2 .
       

        }
        """ )

        #build a dataframe of the output to enable vectorised application of relevant string methods
        df = pd.DataFrame(columns=['source','interaction','target'])
        for row in qres:
               df= df.append({'source': row.action, 'interaction': row.imp, 'target': row.actor2}, ignore_index=True)
               df= df.append({'source': row.actor1, 'interaction': row.gen, 'target': row.action}, ignore_index=True)
            
        df_out = df.drop_duplicates()
        df_out = df_out[~(df_out['interaction'].str.contains('rdf'))]
        df_out = df_out[~(df_out['interaction'].str.contains('owl'))]
        df_out = df_out.replace('http://wrenand.co.uk/fpn/', '', regex=True)
        df_out = df_out.drop_duplicates()
        df_out.replace("", float("NaN"), inplace=True)
        df_out.dropna(how='any', inplace=True)
        data = df_out
        
        #produce a table of all the new nodes
        new_node_table = pd.concat([data['source'], data['target']], axis=0)
        new_node_table = new_node_table.drop_duplicates() 
        node_types = pd.DataFrame(columns=['node', 'class'])
       
        #run a new SPARQL query for EACH node to retrieve a list of all of its classes
        for node in new_node_table:
            node = str(node).replace(' ', '_')
            qres = g.query(
                """
                SELECT  ?node_class 
                WHERE{
              <http://wrenand.co.uk/fpn/%s> rdf:type ?node_class . 
            } 
                """ % node)
            
            #create an empty list of types, fill it with all non-axiomatic types returned by the query above, if there are no returned types it is a Literal.
            type_list = list()
    
            for row in qres:
                    if 'owl' not in str(row.node_class):
                        type_list.append(row.node_class.replace('http://wrenand.co.uk/fpn/', ''))
            if len(type_list) == 0:
                    type_list.append('Literal')
            node_types = node_types.append({'node' : node, 'class' : type_list}, ignore_index=True)
        
        #putting new data into format for visualisation
        type_dict = {}
        for index,row in node_types.iterrows():
            type_dict[row[0]] = row[1]
            
        new_nodes = list()
        for node in new_node_table:
            new_nodes.append({'data': {'id': str(node), 'label': str(node).replace('_', ' ')}, 'classes': type_dict[str(node).replace(' ', '_')]})
    
        new_edges = [
            {'data': {'source': row[0], 'target': row[2], 'label': row[1]}}
            for index, row in data.iterrows()
        ]
        new_elements = new_nodes + new_edges
        layout = {'name': 'dagre', 'spacingFactor':'5'}

        #returning these elements, with a Dagre layout, with current stylesheet.    
        return (new_elements, layout, stylesheet)
    
    #if the search button has been triggered and a term to search has been entered 
    if (button_id == 'search-button') and search_term:
        
        #compute the similarity scores of this search term against all nodes, and store them in the similarity dataframe
        node_lex['scores'] = np.vectorize(sim_score)(node_lex['node'], search_term)
        #the most similar term is the one with the lowest score (fewest changes as a proportion of length)
        max_sim = node_lex['node'][node_lex['scores'].idxmin()]
        #redefining the search term as the most similar term that exists within the data
        search_term = max_sim
        #preparing term for sparql search
        search_term = search_term.replace(' ', '_')\
        #SPARQL query retrieving all outgoing edges & their connected nodes
        qres = g.query(
        """
        SELECT ?p ?o
        WHERE{
        <http://wrenand.co.uk/fpn/%s> ?p ?o . 


        }
        """ % search_term)
        #        #SPARQL query retrieving all incoming edges & their connected nodes
        bqres = g.query(
            """
            SELECT ?s ?p 
            WHERE{
            ?s ?p <http://wrenand.co.uk/fpn/%s> . 

    
        }
        """ % search_term)
        
        #serialising results into dataframe for further use
        df = pd.DataFrame(columns=['source', 'interaction', 'target'])
        for row in qres:
            df = df.append(
                {'source': search_term, 'interaction': row.p, 'target': row.o}, ignore_index=True)
        for row in bqres:
            df = df.append({'source': row.s, 'interaction': row.p,
                            'target': search_term}, ignore_index=True)
        df_out = df.drop_duplicates()
        df_out = df_out[~(df_out['interaction'].str.contains('rdf'))]
        df_out = df_out[~(df_out['interaction'].str.contains('owl'))]
        df_out = df_out.replace('http://wrenand.co.uk/fpn/', '', regex=True)
        df_out = df_out.drop_duplicates()
        df_out.replace("", float("NaN"), inplace=True)
        df_out.dropna(how='any', inplace=True)
        data = df_out
        
        #preparing table of all new nodes
        new_node_table = pd.concat([data['source'], data['target']], axis=0)
        new_node_table = new_node_table.drop_duplicates()
        #if no nodes have been returned (i.e. the search term has no connections), return the search term
        if new_node_table.empty:
            new_node_table = [search_term]

        #produce a table of class lists for all current nodes        
        node_types = pd.DataFrame(columns=['node', 'class'])
        for node in new_node_table:
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
                    if 'owl' not in str(row.node_class):
                        type_list.append(row.node_class.replace('http://wrenand.co.uk/fpn/', ''))
            if len(type_list) == 0:
                    type_list.append('Literal')
            node_types = node_types.append({'node' : node, 'class' : type_list}, ignore_index=True)
        #format data for visualisation
        type_dict = {}
        for index,row in node_types.iterrows():
            type_dict[row[0]] = row[1]
        new_nodes = list()
        for node in new_node_table:
            new_nodes.append({'data': {'id': str(node), 'label': str(node).replace('_', ' ')}, 'classes': type_dict[str(node).replace(' ', '_')]})
        new_edges = [
            {'data': {'source': row[0], 'target': row[2], 'label': row[1]}}
            for index, row in data.iterrows()
        ]
        new_elements = new_nodes + new_edges
       
        #show all nodes, unless dummy-data-only toggle selected
        stylesheet = all_style
        if (display == 'dummy-button'):
           stylesheet = stylesheet + dd_style
       
        #From the list of all node superclasses, if that hasn't been selected on the nodes checklist to view - don't display it or any connected edges.
        for node in nodes_list:
            if node not in nodes:
                stylesheet.append({
                'selector': '.%s' % node,
                'style': {
                    'display': 'none'
                }})
        
        #From the checklist of edge labels, if it has been selected to hide, don't display it
        for edge in edges:
            stylesheet.append({
            'selector': 'edge[label="%s"]' % edge,
            'style': {
                'display': 'none'
            }}) 
        
        #display the search term, even if it would be hidden by the display options otherwise
        stylesheet = stylesheet + [{
                'selector': 'node[id="%s"]' % search_term,
                'style': {
                    'display': 'element'
                }}]
        #if there are fewer than 200 options, display in a dagre layout, otherwise use compound-spring
        if len(new_elements) < 200:
                layout = {'name': 'dagre', 'spacingFactor':'5'}
        else:
                layout = {'name': 'cose-bilkent', 'spacingFactor':'3'}
        return (new_elements, layout, stylesheet)
    
    #if the delete button has been pressed, there is data currently displayed, and both node(s) and edge(s) are selected
    if (button_id =='remove-button') and elements and data_n and data_e:
            #produce a list of all nodes and list of all edges that have been selected
            nodes_to_remove = {ele_data['id'] for ele_data in data_n}
            edges_to_remove = {ele_data['id'] for ele_data in data_e}
            #produce a list of all of the currently displayed data that has not been selected for removal
            intermediate_elements = [ele for ele in elements if ele['data']['id'] not in nodes_to_remove]
            new_elements = [ele for ele in intermediate_elements if ele['data']['id'] not in edges_to_remove]
            #if there are fewer than 200 nodes, display in a dagre layout, otherwise use compound-spring
            if len(new_elements) < 200:
                layout = {'name': 'dagre', 'spacingFactor':'5'}
            else:
                layout = {'name': 'cose-bilkent', 'spacingFactor':'3'}
            return (new_elements, layout, stylesheet)
        
    #if the delete button has been pressed, if there is data currently displayed, and only node(s) selected
    if (button_id =='remove-button') and elements and data_n:
           # produce a list of all currently displayed nodes not selected for removal
            nodes_to_remove = {ele_data['id'] for ele_data in data_n}
            new_elements = [ele for ele in elements if ele['data']['id'] not in nodes_to_remove]
            #if there are fewer than 200 nodes, display in a dagre layout, otherwise use compound-spring
            if len(new_elements) < 200:
                layout = {'name': 'dagre', 'spacingFactor':'5'}
            else:
                layout = {'name': 'cose-bilkent', 'spacingFactor':'3'}
            return (new_elements, layout, stylesheet)

    #if the delete button has been pressed, if there is data currently displayed, and only edge(s) selected
    if (button_id =='remove-button') and elements and data_e:
            edges_to_remove = {ele_data['id'] for ele_data in data_e}
            new_elements = [ele for ele in elements if ele['data']['id'] not in edges_to_remove]
            if len(new_elements) < 200:
                layout = {'name': 'dagre', 'spacingFactor':'5'}
            else:
                layout = {'name': 'cose-bilkent', 'spacingFactor':'3'}
            return (new_elements, layout, stylesheet)
    
    #if the expand button has been pressed, there is data displayed and node(s) selected
    if (button_id =='expand-button') and elements and data_n:
        df = pd.DataFrame(columns=['source', 'interaction', 'target'])
        #insert the current data into the dataframe for results to avoid duplicating currently displayed data later
        for ele in elements:
            if 'source' in ele['data']:
                df = df.append({'source':ele['data']['source'], 'interaction': ele['data']['label'], 'target':ele['data']['target']}, ignore_index=True)
        
        #run two SPARQL queries for each selected node, to retrieve all outgoing and incoming edges and their connected nodes
        #Lexical similarity not needed here because a node is selected, so exact match guaranteed.
        node_to_expand = {ele_data['id'] for ele_data in data_n}
        for node in node_to_expand:
            search_term = node
            qres = g.query(
            """
            SELECT ?p ?o
            WHERE{
            <http://wrenand.co.uk/fpn/%s> ?p ?o . 
            }"""% search_term)
            
            bqres = g.query(
                """
            SELECT ?s ?p
            WHERE{
          ?s ?p <http://wrenand.co.uk/fpn/%s> .
          } 

    
            """ % search_term)
            #also retrieve class membership triples
            class_qres = g.query(
            """
            SELECT ?s
            WHERE{
            ?s a <http://wrenand.co.uk/fpn/%s> .
            }
            """ % search_term)
            
            #if each of these queries returns results, add them to the dataframe
            if len(qres) > 0:
                for row in qres:
                    df = df.append(
                        {'source': search_term, 'interaction': row.p, 'target': row.o}, ignore_index=True)
            if len(bqres) > 0:
                for row in bqres:
                    df = df.append({'source': row.s, 'interaction': row.p,
                                'target': search_term}, ignore_index=True)
            if len(class_qres) > 0:
                for row in class_qres:
                    df = df.append({'source': row.s, 'interaction': 'Type',
                                'target': search_term}, ignore_index=True)
            
            #remove namespaces
            df_out = df.replace('http://wrenand.co.uk/fpn/', '', regex=True)
            df_out = df_out.replace('http://www.w3.org/2002/07/owl#', '', regex=True)
            df_out = df_out.replace('http://www.w3.org/1999/02/22-rdf-syntax-ns#', '', regex=True)
            df_out = df_out.replace('http://www.w3.org/2000/01/rdf-schema#', '', regex=True)
            df_out = df_out.replace('http://www.w3.org/2001/XMLSchema#', '', regex=True)
            #remove reflexive edges
            df_out = df_out[(df_out['source'] != df_out['target'])]
            #remove triples that state that something is a class
            df_out = df_out[df_out['target'] != 'Class']
            #remove all duplicated data (including data that was already in view before pressing expand)
            df_out = df_out.drop_duplicates()
            df_out.replace("", float("NaN"), inplace=True)
            df_out.dropna(how='any', inplace=True)
            data = df_out
            
            #produce a table of all new nodes (which includes the old nodes), list of their classes, and format for visualisation
            new_node_table = pd.concat([data['source'], data['target']], axis=0)
            new_node_table = new_node_table.drop_duplicates()
            node_types = pd.DataFrame(columns=['node', 'class'])
            for node in new_node_table:
                node = str(node).replace(' ', '_')
                qres = g.query(
                    """
                    SELECT  ?node_class 
                    WHERE{
                  <http://wrenand.co.uk/fpn/%s> rdf:type ?node_class . 
                } 
                    """ % node)
                class_qres = g.query(
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
                for row in class_qres:
                    if 'owl' not in str(row.node_class):
                        type_list.append(row.node_class.replace('http://wrenand.co.uk/fpn/', ''))
                if len(type_list) == 0:
                    type_list.append('Literal')
                node_types = node_types.append({'node' : node, 'class' : type_list}, ignore_index=True)
            type_dict = {}
            for index,row in node_types.iterrows():
                type_dict[row[0]] = row[1]

            new_nodes = list()
            for node in new_node_table:
                new_nodes.append({'data': {'id': str(node), 'label': str(node).replace('_', ' ')}, 'classes': type_dict[str(node).replace(' ', '_')]})
            new_edges = [
                {'data': {'source': row[0], 'target': row[2], 'label': row[1]}}
                for index, row in data.iterrows()
            ]
            
            elements = new_nodes + new_edges
            #recalculate the layout based on the number of nodes now displayed
            if len(elements) < 200:
                layout = {'name': 'dagre', 'spacingFactor':'5'}
            else:
                layout = {'name': 'cose-bilkent', 'spacingFactor':'3'}
        return (elements, layout, stylesheet)
    
    #if the focus button is pressed and node(s) are selected
    if (button_id =='focus-button') and data_n:
        df = pd.DataFrame(columns=['source', 'interaction', 'target'])
        
        #run 3 SPARQL queries on each selected node to retrieve all connected nodes.
        #Lexical similarity not needed here because a node is selected, so exact match guaranteed.
        node_to_focus = {ele_data['id'] for ele_data in data_n}
        for node in node_to_focus:
            search_term = node
            qres = g.query(
            """
            SELECT ?p ?o
            WHERE{
            <http://wrenand.co.uk/fpn/%s> ?p ?o . 
            }"""% search_term)
            
            bqres = g.query(
                """
            SELECT ?s ?p
            WHERE{
          ?s ?p <http://wrenand.co.uk/fpn/%s> .
          } 

    
            """ % search_term)
            
            class_qres = g.query(
            """
            SELECT ?s
            WHERE{
            ?s a <http://wrenand.co.uk/fpn/%s> .
            }
            """ % search_term)
            
        
            if len(qres) > 0:
                for row in qres:
                    df = df.append(
                        {'source': search_term, 'interaction': row.p, 'target': row.o}, ignore_index=True)
            if len(bqres) > 0:
                for row in bqres:
                    df = df.append({'source': row.s, 'interaction': row.p,
                                'target': search_term}, ignore_index=True)
            if len(class_qres) > 0:
                for row in class_qres:
                    df = df.append({'source': row.s, 'interaction': 'Type',
                                'target': search_term}, ignore_index=True)
            

            df_out = df.replace('http://wrenand.co.uk/fpn/', '', regex=True)
            df_out = df_out.replace('http://www.w3.org/2002/07/owl#', '', regex=True)
            df_out = df_out.replace('http://www.w3.org/1999/02/22-rdf-syntax-ns#', '', regex=True)
            df_out = df_out.replace('http://www.w3.org/2000/01/rdf-schema#', '', regex=True)
            df_out = df_out.replace('http://www.w3.org/2001/XMLSchema#', '', regex=True)
            df_out = df_out[(df_out['source'] != df_out['target'])]
            df_out = df_out[df_out['target'] != 'Class']
            df_out = df_out.drop_duplicates()
            df_out.replace("", float("NaN"), inplace=True)
            df_out.dropna(how='any', inplace=True)
            data = df_out
            
            #retrieve classes for each new node to display
            new_node_table = pd.concat([data['source'], data['target']], axis=0)
            new_node_table = new_node_table.drop_duplicates()
            node_types = pd.DataFrame(columns=['node', 'class'])
            for node in new_node_table:
                node = str(node).replace(' ', '_')
                qres = g.query(
                    """
                    SELECT  ?node_class 
                    WHERE{
                  <http://wrenand.co.uk/fpn/%s> rdf:type ?node_class . 
                } 
                    """ % node)
                class_qres = g.query(
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
                for row in class_qres:
                    if 'owl' not in str(row.node_class):
                        type_list.append(row.node_class.replace('http://wrenand.co.uk/fpn/', ''))
                if len(type_list) == 0:
                    type_list.append('Literal')
                node_types = node_types.append({'node' : node, 'class' : type_list}, ignore_index=True)
           #format data for visualisation
            type_dict = {}
            for index,row in node_types.iterrows():
                type_dict[row[0]] = row[1]
                
            new_nodes = list()
            for node in new_node_table:
                new_nodes.append({'data': {'id': str(node), 'label': str(node).replace('_', ' ')}, 'classes': type_dict[str(node).replace(' ', '_')]})
    
            new_edges = [
                {'data': {'source': row[0], 'target': row[2], 'label': row[1]}}
                for index, row in data.iterrows()
            ]
            
            elements = new_nodes + new_edges
            #recompute layout based on number of nodes now displayed
            if len(elements) < 200:
                layout = {'name': 'dagre', 'spacingFactor':'5'}
            else:
                layout = {'name': 'cose-bilkent', 'spacingFactor':'3'}
        return (elements, layout, stylesheet)
    
    #if the node display options are changed
    if (button_id == 'nodes-checklist'):
        #set initial stylesheet based on which dataset toggle is currently selected
        stylesheet = all_style
        if (display == 'dummy-button'):
            stylesheet = dd_style + stylesheet
        #hide any edges that are currently selected to be hidden
        for edge in edges:
            stylesheet.append({
            'selector': 'edge[label="%s"]' % edge,
            'style': {
                'display': 'none'
            }})
        #display all of the nodes that are selected to show
        for node in nodes_list:
            if node not in nodes:
                stylesheet.append({
                'selector': '.%s' % node,
                'style': {
                    'display': 'none'
                }})
        return(elements, layout, stylesheet)
    
    #if the edge display options are changed:
    if (button_id == 'edges-checklist'):
        #set initial stylesheet based on which dataset toggle is currently selected
        stylesheet = all_style
        if (display == 'dummy-button'):
           stylesheet = stylesheet + dd_style
       #display all of the nodes that are selected to show
        for node in nodes_list:
            if node not in nodes:
                stylesheet.append({
                'selector': '.%s' % node,
                'style': {
                    'display': 'none'
                }})
        #hide any edges that are currently selected to be hidden
        for edge in edges:
            stylesheet.append({
            'selector': 'edge[label="%s"]' % edge,
            'style': {
                'display': 'none'
            }})
        
        return (elements, layout, stylesheet)
    
    #if the create node button is pushed, and there is a name and class(es) entered
    if (button_id == 'node-button') and nname and nclass:
        #create a new node id with a random integer to allow for duplication
        new_id = nname.replace(' ', '_') + str(np.random.randint(1000, 9999))
        #use the typed name as the node label
        new_label = nname
        #produce a list of the new node's classes, and format data for display
        new_classes = nclass.split(', ')
        new_node = {'data': {'id': new_id, 'label': new_label}, 'classes': new_classes}
        #append this new node to the currently displayed data
        elements += [new_node]
        return (elements, layout, stylesheet)
    
    #if the create edge button is pushed, and exactly two nodes are selected, and a label entered
    if (button_id == 'edge-button') and len(data_n)==2 and ename:
        #set the source and target to the first and second nodes selected chronologically, with the label as entered
        source = data_n[0]['id']
        target = data_n[1]['id']
        label = ename
        #format this for visualisation and append to currently displayed data
        new_edge = [
                {'data': {'source': source, 'target': target, 'label': label}}]
        elements += new_edge
        return (elements, layout, stylesheet)

    #if the display option is set to hide Lit review data, hide it & anything else selected as hidden
    if (display == 'dummy-button'):
        stylesheet = all_style + dd_style
        for node  in nodes_list:
            if node not in nodes:
                stylesheet.append({
                'selector': '.%s' % node,
                'style': {
                    'display': 'none'
                }})    
        for edge in edges:
                stylesheet.append({
                'selector': 'edge[label="%s"]' % edge,
                'style': {
                    'display': 'none'
                }})

    #if the display option is set to show all, hide only nodes and edges selected to be hidden
    if (display == 'all-button'):    
        stylesheet = all_style
        for node in nodes_list:
            if node not in nodes:
                stylesheet.append({
                'selector': '.%s' % node,
                'style': {
                    'display': 'none'
                }})
        for edge in edges:
                stylesheet.append({
                'selector': 'edge[label="%s"]' % edge,
                'style': {
                    'display': 'none'
                }})
                
    #if a node is tapped
    if tapnode:
        #maintain current styling options
        stylesheet = all_style
        if (display == 'dummy-button'):
            stylesheet += dd_style
        for node in nodes_list:
            if node not in nodes:
                stylesheet.append({
                'selector': '.%s' % node,
                'style': {
                    'display': 'none'
                }})
        for edge in edges:
                stylesheet.append({
                'selector': 'edge[label="%s"]' % edge,
                'style': {
                    'display': 'none'
                }})
        #for each of the edges connected to the tapped node
        for edge in tapnode['edgesData']:
            #if the edge starts at the selected node, style it
            if edge['source'] == tapnode['data']['id']: 
                stylesheet.append({"selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {"line-color": '#bebada',
                          'target-arrow-color':'#bebada',
                          'width':'3'}})
            #if the edge ends at the selected node, style it
            if edge['target'] == tapnode['data']['id']: 
                stylesheet.append({"selector": 'edge[id= "{}"]'.format(edge['id']),
                "style": {"line-color": '#fccde5',
                          'target-arrow-color':'#fccde5',
                          'width':'3'}})
    
    #if edge(s) are selected, highlight them
    if data_e:
        for edge in data_e:
                stylesheet.append({"selector": 'edge[id= "{}"]'.format(edge['id']), "style": {"line-color": '#bc80bd',
                          'target-arrow-color':'#bc80bd',
                          'width':'3'}})
        return (elements, layout, stylesheet)
    
    return (elements, layout, stylesheet)



#if a node is selected, display that node's label and classes in the 'Selected Node Info" tab
@app.callback(Output('tap-node-data', 'children'),
              Input('food-pol-net', 'tapNode'))
def display_tap_node(data):
    if data:
        name = data['data']['label']
        node_classes = data['classes'].replace(' ', ', ')
        return 'Selected Node:\n' + name + '\nClasses:\n' + node_classes
    return 'nothing selected'




if __name__ == '__main__':
    app.run_server(debug=False)