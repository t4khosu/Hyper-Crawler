# Hyper Crawler

Have you ever wondered, what kind of websites a specific domain references most often?
Especially in a political context it can be useful to find out what soruces a site primarely relies on.
Therefore I implemented my own crawler and visualization tool: **Hyper Crawler**

## Tools and Requirements
* Python >= 3.6.4
* [requirements.txt](requirements.txt) (installation: `pip install -r requirements.txt`)

## Concept
This algorithm intreprets any given site as a node of a big tree. Each node can have many connections to different child sites (edges). Since references to higher nodes are not important, references to already seen sites get ignored. The following image contains a simple tree with root HP:

![alt text](res/tree.png "Tree Structure for homepages")

* HP: Homepage
* (m, n): m = depth, n = position in layer
* \[z\]: time step visited --> breadth-first search, BFS

Ausgehend von der Wurzel, werden alle Verlinkungen [U_1, ..., U_N] auf Seite *A* gesucht. Verlinkungen zeichnen sich durch <a>-Tags aus. 
Referenzen auf die Domäne von *A* und fremde Adressen werden getrennt voneinander gespeichert: A_{selbst}, A_{fremd}.  Anschließend werden Selbstreferenzen in A_{selbst} mit Breitensuche nach neuen Verlinkungen durchsucht.<br>
Für große Webseiten sollte die Suchtiefe nicht zu groß gewählt werden, da manche Seiten mehrere tausende Eigenverlinkungen aufweißen können.

## Ergebnisse
Eine .log- und eine .anl-Datei (analyze). Der Log dient dem Zwischenspeichern aller Ergebnisse, um die Folgen fataler Fehler zu minimieren. In der Analyse-Datei werden Fremddomänen voneinander getrennt und aufsteigend nach Menge der Verlinkungen sortiert. Beispiel: https://naralva.org.<br>

### [naralva.log](results/logs/naralva.log) [naralva.anl](results/naralva.anl)


Ergbenisse der .anl-Datei lassen sich als Graph visualisieren:
![alt text](res/naralva[1_bis_-1].png "Fremdverlinkungen von naralva.org aus")<br>
* Größerer Knoten =  mehr Verlinkungen
* Verlinkungen werden in Sets gespeichert, d.h. Duplikate fallen weg. Dadurch wird immer nur die Menge __unterschiedlicher__ Referenzen betrachtet.
