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

* HP: homepage
* (m, n): m = depth, n = position in layer
* \[z\]: time step visited --> breadth-first search, BFS

A root can be any user defined domain `d`. At first all hyperrefs defined by \<a\>...\</a\> from `d`'s homepage are collected.
If a found site contains the same domain `d`, the algorithm will run again for this site. If not, the site's URL gets stored.
However, if the site was already checked, it won't be checked again.

Since some domains contain thousands of references, the depth of this tree can be specified.


## Result
Eine .log- und eine .anl-Datei (analyze). Der Log dient dem Zwischenspeichern aller Ergebnisse, um die Folgen fataler Fehler zu minimieren. In der Analyse-Datei werden Fremddomänen voneinander getrennt und aufsteigend nach Menge der Verlinkungen sortiert. Beispiel: https://naralva.org.<br>

### [naralva.log](results/logs/naralva.log) [naralva.anl](results/naralva.anl)


Ergbenisse der .anl-Datei lassen sich als Graph visualisieren:
![alt text](res/naralva[1_bis_-1].png "Fremdverlinkungen von naralva.org aus")<br>
* Größerer Knoten =  mehr Verlinkungen
* Verlinkungen werden in Sets gespeichert, d.h. Duplikate fallen weg. Dadurch wird immer nur die Menge __unterschiedlicher__ Referenzen betrachtet.
