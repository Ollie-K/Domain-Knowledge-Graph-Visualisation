# Visualisation Preprocessing

Files necessary to extract node positions from a visualisation for precomputing layout. 

N.B. Extracting all node positions requires a modified version of dash-cytoscape (supplied) that needs to be used in place of the same file in your build. Its location will depend on your system, so search is probably the best way to find it. This modified version is not used in or compatable with the final visualisation, so retain both & replace when done. 

* Run the relevant script, open a web browser and visit the url given in your terminal (likely http://127.0.0.1:8050/). 
* Once visualised, box drag the nodes to select them & copy the string at the bottom into a new json file. These are given in outputs.

## Guide to files:

* outputs - folder containing the resulting node positions for use in the final visualisation 

* 13-8_elements_file.json - json containing all nodes and their classes, and edges.
* 13-8-inference.ttl - the created knowledge graph
* dash_cytoscape_extra.min.js - modified version of dash-Cytoscape to allow for the extraction of multiple selected node positions
* extract_json_from_cyto.py - script to allow for the visualisation & extraction of position for all entities
* extract_map_pos_from_cyto.py - script to allow for the visualisation & extraction of position for class schema
* extract_onto_pos_from_cyto.py - script to allow for the visualisation & extraction of position for class hierarchy
* map_elements.json - json containing all classes, their structure and indicative interactions.
* onto_elements.json - json containing all classes and their structure.