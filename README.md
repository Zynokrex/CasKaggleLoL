# Pràctica Kaggle APC UAB 2022-23
### Biel González Garriga
### Dataset: [League of Legends SOLO-Q Ranked Games](https://www.kaggle.com/datasets/bobbyscience/league-of-legends-soloq-ranked-games)

## Resum
El dataset conté dades del videojoc League of Legends, el dataset complet està format per valors numèrics.

![desktop-wallpaper-summoner-s-rift-league-of-legends-maps](Images/desktop-wallpaper-summoner-s-rift-league-of-legends-maps.jpg)

Més específicament conté les dades de l'equip blau, el que està a baix del mapa. Aquestes dades són sèries temporals de diferents partides. Originalment, hi ha 59 features i unes 25000 files. Podem agrupar les features en:

* `gameId`: Ens dona l'id de la partida a la qual pertanyen les dades d'aquella fila.
* `frame`: Ens diu a quin frame de la partida han estat preses les dades, comença sempre en el minut deu i augmenta de dos en dos.
* `hasWon`: Ens diu si l'equip blau guanya o no la partida.
* Relacionades amb diferencies: Ens informen de l'avantatge o desavantatge d'or, experiència i nivell de l'equip blau.
* Relacionades amb estructures: Ens informen de les estructures perdudes i destruïdes, torres i inhibidors.
* Relacionades amb objectius: Ens informen dels objectius aconseguits i perduts, dracs, heralds, barons.
* Relacionades amb visió: Ens informen dels wards posats, destruïts i perduts per l'equip blau.
* `Deaths`,`Kills`,`Assists`: Ens informen de les morts, assassinats i assistències de l'equip blau.

## Objectiu

Amb aquest dataset intentarem predir sota unes condicions finals si un equip guanyarà o no la partida. I quines són les features que resulten més importants pels models que entrenem.

## Experiments

Durant aquesta pràctica s'ha vist no només sobre models complets sinó també models d'una sola feature per veure si també podiem obtenir un bon rendiment d'aquests. A part de crear nous atributs per visualitzar millor les dades.

## Preporcessat

El dataset estava net i no tenia nuls, per tant, l'únic preprocessat ha sigut la creació de 35 nous atributs d'aspectes rellevants per entendre millor la partida i accions dels jugadors durant aquesta. Alguns exemples serien les animes dels dracs, la quantitat de dracs aconseguits, estructures destruïdes i similars.
Es va contemplar i fer atributs que continuessin quartils, variàncies, mitjanes i desviacions per tenir informació del progrés de la partida, però al final es va descartar pel que es comentarà a les conclusions*.

## Model
| Model | Hiperparametres** | Model.score | ROC AUC | F1 | Accuracy | Precision | Temps |
| -- | -- | -- | -- | -- | -- | -- | -- |
| Logistic Regression | default | 0,975 | 0,997 | 0,976 | 0,976 | 0,976 | 0 0,17s |
| Perceptron | default  | 0,874 | 0,957 | 0,868 | 0,868 | 0,868 | 0,868 | 0,236s |
| Ada Boosting | default  | 0,984 | 0,997 | 0,986 | 0,986 | 0,986 | 6,164s |
| Gradient Boosting | default  | 0,985 | 0,999 | 0,983 | 0,983 | 0,983 | 6,329s |
| Random Forest | default  | 0,985 | 0,999 | 0,985 | 0,985 | 0,985 | 1,720 |
| Multi Layer Perceptron | default  | 0,974 | 0,980 | 0,958 | 0,958 | 0,958 | 1,388s |

## Requisits
* Numpy
* Pandas
* Matplotlib
* Seaborn
* pandas_profiling
* Sklearn
* IPython

## Demo

Per fer qualsevol prova primer s'ha d'executar el jupyter de models. A partir d'allà els models entrenats estan guardats en un diccionari anomenat 'models' i es poden buscar pel seu respectiu nom. Dins del propi notebook s'ha facilitat tot perquè estigui tot net i dins de funcions més o menys intuïtives per l'usuari en l'àmbit de models i creació de gràfics.

## Conclusions

Els millors models han sigut la regressió logística i el random forest, el primer triga menys que el segon i dona molt bons resultats, guanya per molt poc pel que fa a metriques el random forest, però és una diferència minúscula. I les features més importants per a tots els models són `goldDiff` i `expDiff`. Com es pot veure les mètriques de tots els models.

*La creació de noves columnes que ens donessin informació de com ha procedit la partida no ha sigut necessaria ja que els models donen molt bones prediccions sense la necessitat d'aquesta informacio. Per tant crear-les només ralentitzaria l'entrenament dels models a canvi d'una millora poc notable.

**Semblant a la creació de noves columnes, l'esforç i temps que significava fer la busqueda d'hiperparàmetres no compensa ja que els models donen molt bons resultats sense la necessitat d'aquesta cerca.

## Idees per a treballar en un futur

Amb un model més complex es podria intentar predir d'un frame al següent de la partida com avançaran molts dels atributs, una mena de simulació de parts de partides sota unes condicions, però això és molt complex. Una altra idea seria treballar encara en més profunditat la part de l'EDA i extreure encara més informació de com s'hauria de jugar una partida per poder tenir les màximes probabilitats de guanyar. També per millorar la capacitat de l'usuari de poder interactuar amb els models es pot fer un dashboard.

## Llicencia

El projecte ha sigut desenvolupat per Biel González Garriga
