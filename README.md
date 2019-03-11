# HyperCrawler

Ziel dieses Projekts ist es, ausgehend von einer gegebenen URL *A*, alle Fremdverlinkungen zu finden.<br>
Fremdverlinkungen bezeichnen Webseiten, deren URLs kein Teil der Domäne von *A* sind.

## Requirements
* Python 3.6.4
* [requirements.txt](requirements.txt) (Installation mit `pip install -r requirements.txt`)

# Idee
Algorithmus:<br>
![alt text](res/tree.png "Tree Structure for homepages")<br>
* HP: Homepage
* (m, n): m = Baumtiefe (depth), n = Position in der aktuellen Schicht
* [z]: Ablaufschritte im Algorithmus

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
