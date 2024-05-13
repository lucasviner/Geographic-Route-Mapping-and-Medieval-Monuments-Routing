Ha de contenir: 
1) Obtenir les rutes dels senderistes en una regió geogràfica.
2) Inferir un mapa (un graf) a partir de les rutes.
3) Obtenir les coordenades de monuments medievals.
4) Trobar rutes òptimes per arribar a monuments medievals en el graf inferit.
5) Visualitzar els mapes resultants en 2D i 3D.

El més díficil es montar el graf i simplificar-ho.
Fer servir les llibreries!!


Passos per construir el mapa
1) Tenim els diferents punts, que son senders.
2) Agrupem aquests en clusters, on seran representats per un centroide.
3) Creem un graf, on els vertexs son els centroides i les arestes si hi ha un sender entre dos d'aquests
4) Simplifiquem el graf
5) Associem els monuments als centroides més propers.

Coses a fer:
1) Acabar segments:
  - cook data
  - Modificar per posar-ho com tothom
2) Monuments queda
3) Graphmaker
  - simplificar
  - Numpy
  - modificacions arestes(jordi foto)
4) Viewer
5) Routes
6) Main
