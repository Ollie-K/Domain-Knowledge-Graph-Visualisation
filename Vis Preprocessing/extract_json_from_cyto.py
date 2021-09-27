#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 14:30:20 2021

@author: ollie
"""


from rdflib import Graph
import pandas as pd


import os
import json

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html


import dash_cytoscape as cyto

g = Graph()
g.parse("13-8-inference.ttl", format="ttl")


asset_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', 'assets'
)

app = dash.Dash(__name__, assets_folder=asset_path)
server = app.server
cyto.load_extra_layouts()

    
with open('13-8_elements_file.json') as f:
    default_elements = json.loads(f.read())

styles = {
    'json-output': {
        'overflow-y': 'scroll',
        'height': 'calc(0.45*(20vh)',
        'border': 'thin lightgrey solid',
    },
    'tab': {'height': 'calc(20vh-100px)'}
}

app.layout = html.Div([
    html.Div(className='eight columns', children=[
        
         cyto.Cytoscape(
            id='food-pol-net',
            boxSelectionEnabled= True,

            elements=default_elements,
            layout={
                'name': 'cose-bilkent',
            },
            style={
                'height': '80vh',
                'width': '100%'
            },
            stylesheet=[
                {
                'selector': 'edge',
                'style': {
                    
                    'curve-style': 'haystack',
                    'target-arrow-shape': 'vee',
                    'arrow-scale': 2
                }},
                {
            'selector': '.Actor',
            'style': {
                'shape': 'star',
                'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2',
            }
        }, 
                  {
            'selector': '.Action',
            'style': {
                'shape': 'tag',
                'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2',
            }
        }, 
                    {
            'selector': '.Issue',
            'style': {
                'shape': 'barrel',
                'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.2',
            }
        }, 
            {
            'selector': '.Place',
            'style': {
                'shape': 'vee'
            }
        }, 
            {
            'selector': '.Literal',
            'style': {
                'shape': 'square'
            }
        }, 
        ]
        ),
        
        html.Div(className='four columns', children=[
        dcc.Tabs(id='tabs', children=[
            
            dcc.Tab(label='Selected Node Data', children=[
                html.Div(style=styles['tab'], children=[
                    html.Pre(
                        id='tap-node-data',
                        style=styles['json-output']
                    ),                    html.Button("Dump json", id='json-dump'),

                   
                        ])
                    ]),  
            
            
            dcc.Tab(label='Search Panel', children=[
                html.Div(style=styles['tab'], children=[
                    html.P('Search Box:'),
                    dcc.Input(id='search-box', type='text'),
                    dcc.RadioItems(
                    id='degrees-radio',
                    options=[{'label': 'Direct Connections', 'value': '1'}, {'label': 'Secondary Connections', 'value': '2'}, {'label': 'Tertiary Connections', 'value': '3'}], value='1'),
                    html.Button("Trace Influences", id='back-button'),
                    html.Button("Trace Effects", id='fwd-button'),
                    html.Button("Trace Both", id='both-button'),
                    
                    html.Button("Remove Selected Node(s)/Edge(s)", id='remove-button'),      
                    html.Button("Expand Selected Node(s)", id='expand-button'), 
                
                    ])
                ]),

            
        ]),
    ]),
        
       
  
    
    
])
])


@app.callback((Output('food-pol-net', 'elements'),
               Output('food-pol-net', 'layout'),
               Output('food-pol-net', 'stylesheet')),
              [Input('degrees-radio', 'value'),
                Input('fwd-button', 'n_clicks'),
                Input('back-button', 'n_clicks'),
                Input('both-button', 'n_clicks'),
                Input('remove-button', 'n_clicks'),
                Input('expand-button', 'n_clicks')],
              [State('food-pol-net', 'elements'),
               State('food-pol-net', 'layout'),
               State('food-pol-net', 'stylesheet'),
                State('search-box', 'value'),
                State('food-pol-net', 'selectedNodeData'),
                State('food-pol-net', 'selectedEdgeData')]
              )
def search(degrees, fwd_button, back_button, both_button, remove_button, expand_button, elements, layout, stylesheet, search_term, data_n, data_e):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print(button_id)
    
    if (button_id == 'fwd-button') and search_term:
        search_term = search_term.replace(' ', '_')
        if (degrees == '1'):
            qres = g.query(
            """
            SELECT ?p ?o 
            WHERE{
            <http://wrenand.co.uk/fpn/%s> ?p ?o . 
            }
            """ % search_term)
            fdf = pd.DataFrame(columns=['source', 'interaction', 'target'])
            print(fdf.shape)
    
            for row in qres:
                fdf = fdf.append(
                    {'source': search_term, 'interaction': row.p, 'target': row.o}, ignore_index=True)
                
        if (degrees == '2'):
            qres = g.query(
            """
            SELECT ?p ?o ?p1 ?o1 
            WHERE{
            <http://wrenand.co.uk/fpn/%s> ?p ?o . 
            OPTIONAL {?o ?p1 ?o1 .}
            }
            """ % search_term)
            fdf = pd.DataFrame(columns=['source', 'interaction', 'target'])
            print(fdf.shape)
    
            for row in qres:
                fdf = fdf.append(
                    {'source': search_term, 'interaction': row.p, 'target': row.o}, ignore_index=True)
                fdf = fdf.append({'source': row.o, 'interaction': row.p1,
                                'target': row.o1}, ignore_index=True)
                
        if (degrees == '3'):
            qres = g.query(
            """
            SELECT ?p ?o ?p1 ?o1 ?p2 ?o2 
            WHERE{
            <http://wrenand.co.uk/fpn/%s> ?p ?o . 
            OPTIONAL {?o ?p1 ?o1 .}
            OPTIONAL {?o1 ?p2 ?o2 .}
    
            }
            """ % search_term)
            fdf = pd.DataFrame(columns=['source', 'interaction', 'target'])
            print(fdf.shape)
    
            for row in qres:
                fdf = fdf.append(
                    {'source': search_term, 'interaction': row.p, 'target': row.o}, ignore_index=True)
                fdf = fdf.append({'source': row.o, 'interaction': row.p1,
                                'target': row.o1}, ignore_index=True)
                fdf = fdf.append({'source': row.o1, 'interaction': row.p2,
                                'target': row.o2}, ignore_index=True)

        print(fdf.shape)
        df_out = fdf.drop_duplicates()
        print(df_out.shape)
        df_out = df_out[~(df_out['interaction'].str.contains('rdf'))]
        print(df_out.shape)
        df_out = df_out[~(df_out['interaction'].str.contains('owl'))]
        print(df_out.shape)
        df_out = df_out.replace('http://wrenand.co.uk/fpn/', '', regex=True)
        print(df_out.shape)
        df_out = df_out.drop_duplicates()
        df_out.replace("", float("NaN"), inplace=True)
        df_out.dropna(how='any', inplace=True)
        data = df_out
        
        new_node_table = pd.concat([data['source'], data['target']], axis=0)
        print(new_node_table.shape)
        new_node_table = new_node_table.drop_duplicates()
        print(new_node_table.shape)
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
        
        return (new_elements, {'name': 'dagre', 'spacingFactor':'2.5'})
    
    if (button_id == 'back-button') and search_term:
        search_term = search_term.replace(' ', '_')
        if (degrees =='1'):
            bqres = g.query(
            """
            SELECT ?s ?p
            WHERE{
            ?s ?p <http://wrenand.co.uk/fpn/%s> .     
            }
            """ % search_term)
            bdf = pd.DataFrame(columns=['source', 'interaction', 'target'])
            print(bdf.shape)
            for row in bqres:
                bdf = bdf.append({'source': row.s, 'interaction': row.p,
                                'target': search_term}, ignore_index=True)
                
        if (degrees =='2'):
            bqres = g.query(
            """
            SELECT ?s ?p ?p1 ?s1
            WHERE{
            ?s ?p <http://wrenand.co.uk/fpn/%s> . 
            OPTIONAL {?s1 ?p1 ?s .}
    
            }
            """ % search_term)
            bdf = pd.DataFrame(columns=['source', 'interaction', 'target'])
            print(bdf.shape)
            for row in bqres:
                bdf = bdf.append({'source': row.s, 'interaction': row.p,
                                'target': search_term}, ignore_index=True)
                bdf = bdf.append({'source': row.s1, 'interaction': row.p1,
                                'target': row.s}, ignore_index=True)
                
        if (degrees == '3'):
            bqres = g.query(
            """
            SELECT ?s ?p ?p1 ?s1 ?p2 ?s2 
            WHERE{
            ?s ?p <http://wrenand.co.uk/fpn/%s> . 
            OPTIONAL {?s1 ?p1 ?s .}
            OPTIONAL {?s2 ?p2 ?s1 .}
    
            }
            """ % search_term)
            bdf = pd.DataFrame(columns=['source', 'interaction', 'target'])
            print(bdf.shape)
            for row in bqres:
                bdf = bdf.append({'source': row.s, 'interaction': row.p,
                                'target': search_term}, ignore_index=True)
                bdf = bdf.append({'source': row.s1, 'interaction': row.p1,
                                'target': row.s}, ignore_index=True)
                bdf = bdf.append({'source': row.s2, 'interaction': row.p2,
                                'target': row.s1}, ignore_index=True)

        print(bdf.shape)
        df_out = bdf.drop_duplicates()
        print(df_out.shape)
        df_out = df_out[~(df_out['interaction'].str.contains('rdf'))]
        print(df_out.shape)
        df_out = df_out[~(df_out['interaction'].str.contains('owl'))]
        print(df_out.shape)
        df_out = df_out.replace('http://wrenand.co.uk/fpn/', '', regex=True)
        print(df_out.shape)
        df_out = df_out.drop_duplicates()
        df_out.replace("", float("NaN"), inplace=True)
        df_out.dropna(how='any', inplace=True)
        data = df_out
        
        new_node_table = pd.concat([data['source'], data['target']], axis=0)
        print(new_node_table.shape)
        new_node_table = new_node_table.drop_duplicates()
        print(new_node_table.shape)
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
        
        return (new_elements, {'name': 'dagre', 'spacingFactor':'2.5'}, 
                [{
                'selector': 'edge',
                'style': {
                    'source-label': 'data(label)',
                    'source-text-rotation': 'autorotate',
                    'source-text-offset': 200,
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'rectangle',
                    'text-background-opacity': '0.7',
                    'text-background-padding': '7',
                    'curve-style': 'bezier',
                    'control-point-weights': '0 0.1 0.2',
                    'target-arrow-shape': 'vee',
                    'arrow-scale': 2
                }},
                {
                'selector': 'node',
                'style': {'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.7',
                    

                }
            }])
    
    if (button_id == 'both-button') and search_term:
        search_term = search_term.replace(' ', '_')
        if (degrees =='1'):
            qres = g.query(
            """
            SELECT ?p ?o
            WHERE{
            <http://wrenand.co.uk/fpn/%s> ?p ?o . 

    
            }
            """ % search_term)
            bqres = g.query(
                """
                SELECT ?s ?p 
                WHERE{
                ?s ?p <http://wrenand.co.uk/fpn/%s> . 

        
            }
            """ % search_term)
        
            df = pd.DataFrame(columns=['source', 'interaction', 'target'])
            print(df.shape)
    
            for row in qres:
                df = df.append(
                    {'source': search_term, 'interaction': row.p, 'target': row.o}, ignore_index=True)
        
            for row in bqres:
                df = df.append({'source': row.s, 'interaction': row.p,
                                'target': search_term}, ignore_index=True)

                
        if (degrees =='2'):
            qres = g.query(
            """
            SELECT ?p ?o ?p1 ?o1
            WHERE{
            <http://wrenand.co.uk/fpn/%s> ?p ?o . 
            OPTIONAL {?o ?p1 ?o1 .}
    
            }
            """ % search_term)
            
            bqres = g.query(
                """
                SELECT ?s ?p ?p1 ?s1 
                WHERE{
                ?s ?p <http://wrenand.co.uk/fpn/%s> . 
                OPTIONAL {?s1 ?p1 ?s .}

        
            }
            """ % search_term)
        
            df = pd.DataFrame(columns=['source', 'interaction', 'target'])
            print(df.shape)
    
            for row in qres:
                df = df.append(
                    {'source': search_term, 'interaction': row.p, 'target': row.o}, ignore_index=True)
                df = df.append({'source': row.o, 'interaction': row.p1,
                                'target': row.o1}, ignore_index=True)

        
            for row in bqres:
                df = df.append({'source': row.s, 'interaction': row.p,
                                'target': search_term}, ignore_index=True)
                df = df.append({'source': row.s1, 'interaction': row.p1,
                                'target': row.s}, ignore_index=True)

                
        if (degrees =='3'):
            qres = g.query(
            """
            SELECT ?p ?o ?p1 ?o1 ?p2 ?o2 
            WHERE{
            <http://wrenand.co.uk/fpn/%s> ?p ?o . 
            OPTIONAL {?o ?p1 ?o1 .}
            OPTIONAL {?o1 ?p2 ?o2 .}
    
            }
            """ % search_term)
            bqres = g.query(
                """
                SELECT ?s ?p ?p1 ?s1 ?p2 ?s2 
                WHERE{
                ?s ?p <http://wrenand.co.uk/fpn/%s> . 
                OPTIONAL {?s1 ?p1 ?s .}
                OPTIONAL {?s2 ?p2 ?s1 .}
        
            }
            """ % search_term)
        
            df = pd.DataFrame(columns=['source', 'interaction', 'target'])
            print(df.shape)
    
            for row in qres:
                df = df.append(
                    {'source': search_term, 'interaction': row.p, 'target': row.o}, ignore_index=True)
                df = df.append({'source': row.o, 'interaction': row.p1,
                                'target': row.o1}, ignore_index=True)
                df = df.append({'source': row.o1, 'interaction': row.p2,
                                'target': row.o2}, ignore_index=True)
        
            for row in bqres:
                df = df.append({'source': row.s, 'interaction': row.p,
                                'target': search_term}, ignore_index=True)
                df = df.append({'source': row.s1, 'interaction': row.p1,
                                'target': row.s}, ignore_index=True)
                df = df.append({'source': row.s2, 'interaction': row.p2,
                                'target': row.s1}, ignore_index=True)

        print(df.shape)
        df_out = df.drop_duplicates()
        print(df_out.shape)
        df_out = df_out[~(df_out['interaction'].str.contains('rdf'))]
        print(df_out.shape)
        df_out = df_out[~(df_out['interaction'].str.contains('owl'))]
        print(df_out.shape)
        df_out = df_out.replace('http://wrenand.co.uk/fpn/', '', regex=True)
        print(df_out.shape)
        df_out = df_out.drop_duplicates()
        df_out.replace("", float("NaN"), inplace=True)
        df_out.dropna(how='any', inplace=True)
        data = df_out
        
        new_node_table = pd.concat([data['source'], data['target']], axis=0)
        print(new_node_table.shape)
        new_node_table = new_node_table.drop_duplicates()
        print(new_node_table.shape)
        
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
        
        return (new_elements, {'name': 'dagre', 'spacingFactor':'2.5'}, [{
                'selector': 'edge',
                'style': {
                    'source-label': 'data(label)',
                    'source-text-rotation': 'autorotate',
                    'source-text-offset': 200,
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'rectangle',
                    'text-background-opacity': '0.7',
                    'text-background-padding': '7',
                    'curve-style': 'bezier',
                    'control-point-weights': '0 0.1 0.2',
                    'target-arrow-shape': 'vee',
                    'arrow-scale': 2
                }},
                {
                'selector': 'node',
                'style': {'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.7',
                    

                }
            }])
    
    if (button_id =='remove-button') and elements and data_n and data_e:
            nodes_to_remove = {ele_data['id'] for ele_data in data_n}
            edges_to_remove = {ele_data['id'] for ele_data in data_e}
            intermediate_elements = [ele for ele in elements if ele['data']['id'] not in nodes_to_remove]
            new_elements = [ele for ele in intermediate_elements if ele['data']['id'] not in edges_to_remove]
            return (new_elements, {'name': 'dagre', 'spacingFactor':'2.5'}, [{
                'selector': 'edge',
                'style': {
                    'source-label': 'data(label)',
                    'source-text-rotation': 'autorotate',
                    'source-text-offset': 200,
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'rectangle',
                    'text-background-opacity': '0.7',
                    'text-background-padding': '7',
                    'curve-style': 'bezier',
                    'control-point-weights': '0 0.1 0.2',
                    'target-arrow-shape': 'vee',
                    'arrow-scale': 2
                }},
                {
                'selector': 'node',
                'style': {'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.7',
                    

                }
            }])
        
    if (button_id =='remove-button') and elements and data_n:
            nodes_to_remove = {ele_data['id'] for ele_data in data_n}
            new_elements = [ele for ele in elements if ele['data']['id'] not in nodes_to_remove]
            return (new_elements, {'name': 'dagre', 'spacingFactor':'2.5'}, [{
                'selector': 'edge',
                'style': {
                    'source-label': 'data(label)',
                    'source-text-rotation': 'autorotate',
                    'source-text-offset': 200,
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'rectangle',
                    'text-background-opacity': '0.7',
                    'text-background-padding': '7',
                    'curve-style': 'bezier',
                    'control-point-weights': '0 0.1 0.2',
                    'target-arrow-shape': 'vee',
                    'arrow-scale': 2
                }},
                {
                'selector': 'node',
                'style': {'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.7',
                    

                }
            }])
        #from https://github.com/plotly/dash-cytoscape/blob/master/demos/usage-remove-selected-elements.py

    if (button_id =='remove-button') and elements and data_e:
            edges_to_remove = {ele_data['id'] for ele_data in data_e}
            new_elements = [ele for ele in elements if ele['data']['id'] not in edges_to_remove]
            return (new_elements, {'name': 'dagre', 'spacingFactor':'2.5'}, [{
                'selector': 'edge',
                'style': {
                    'source-label': 'data(label)',
                    'source-text-rotation': 'autorotate',
                    'source-text-offset': 200,
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'rectangle',
                    'text-background-opacity': '0.7',
                    'text-background-padding': '7',
                    'curve-style': 'bezier',
                    'control-point-weights': '0 0.1 0.2',
                    'target-arrow-shape': 'vee',
                    'arrow-scale': 2
                }},
                {
                'selector': 'node',
                'style': {'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.7',
                    

                }
            }])
    
    if (button_id =='expand-button') and elements and data_n:
        df = pd.DataFrame(columns=['source', 'interaction', 'target'])
        for ele in elements:
            if 'source' in ele['data']:
                df = df.append({'source':ele['data']['source'], 'interaction': ele['data']['label'], 'target':ele['data']['target']}, ignore_index=True)

        node_to_expand = {ele_data['id'] for ele_data in data_n}
        for node in node_to_expand:
            search_term = node
            qres = g.query(
            """
            SELECT ?s1 ?p1 ?p ?o
            WHERE{
           OPTIONAL { <http://wrenand.co.uk/fpn/%s> ?p ?o . }
            OPTIONAL{ ?s ?p1 <http://wrenand.co.uk/fpn/%s> .} 

    
            }
            """ % (search_term, search_term))
            
        
            if len(qres) > 0:
                for row in qres:
                    df = df.append(
                        {'source': search_term, 'interaction': row.p, 'target': row.o}, ignore_index=True)
                    df = df.append({'source': row.s1, 'interaction': row.p1,
                                'target': search_term}, ignore_index=True)
            
            df_out = df[~(df['interaction'].str.contains('rdf'))]
            
            df_out = df_out[~(df_out['interaction'].str.contains('owl'))]
            df_out = df_out.replace('http://wrenand.co.uk/fpn/', '', regex=True)
            df_out = df_out.drop_duplicates()
            df_out.replace("", float("NaN"), inplace=True)
            df_out.dropna(how='any', inplace=True)
            data = df_out
            
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
                
                
                
            new_nodes = list()
            for node in new_node_table:
                new_nodes.append({'data': {'id': str(node), 'label': str(node).replace('_', ' ')}, 'classes': type_dict[str(node).replace(' ', '_')]})
    
            new_edges = [
                {'data': {'source': row[0], 'target': row[2], 'label': row[1]}}
                for index, row in data.iterrows()
            ]
            
            elements = new_nodes + new_edges
        return (elements, {'name': 'dagre', 'spacingFactor':'2.5'}, [{
                'selector': 'edge',
                'style': {
                    'source-label': 'data(label)',
                    'source-text-rotation': 'autorotate',
                    'source-text-offset': 200,
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'rectangle',
                    'text-background-opacity': '0.7',
                    'text-background-padding': '7',
                    'curve-style': 'bezier',
                    'control-point-weights': '0 0.1 0.2',
                    'target-arrow-shape': 'vee',
                    'arrow-scale': 2
                }},
                {
                'selector': 'node',
                'style': {'content': 'data(label)',
                    'text-wrap': 'ellipsis',
                    'text-max-width': '200px',
                    'text-overflow-wrap': 'whitespace',
                    'text-valign': 'bottom',
                    'text-background-color': '#FFFFFF',
                    'text-background-shape': 'round-rectangle',
                    'text-background-opacity': '0.7',
                    

                }
            }])
            
    return (elements, layout, stylesheet)

@app.callback(Output('tap-node-data', 'children'),
              [Input('food-pol-net', 'selectedNodeData')],
              [Input('food-pol-net', 'selectedEdgeData')])
def display_tap_node(data1, data2):
    if data1 and data2:
        data3 = []
        data = data1 + data2
        print(data1)
        print(data2)
        name = json.dumps(data)
        # name = data['data']['label'] 
        # node_classes = data['classes'].replace(' ', ', ')
        # return 'Selected Node:\n' +  name + '\nClasses:\n' + node_classes
        return(name)
    return 'nothing selected'

if __name__ == '__main__':
    app.run_server(debug=False)