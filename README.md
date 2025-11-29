Atelier : Implémenter une Architecture Lambda simplifiée avec Spark et Kafka
Réalisé par

👩‍💻 Hajar Elfallaki-Idrissi

📌 Table des matières

Introduction

Objectifs pédagogiques

Rappel théorique : Architecture Lambda

Pré-requis techniques

Structure du projet

Dataset utilisé

Mise en place de l’environnement (Docker)

Batch Layer – Traitement des données historiques

Speed Layer – Traitement en temps réel

Serving Layer – Fusion Batch + Streaming

Captures d’écran

Questions et réponses

Conclusion

Introduction

Cet atelier a pour objectif de guider les étudiants dans la mise en place d’une architecture Lambda simplifiée afin de comprendre les principes fondamentaux du traitement de données Big Data, à la fois en mode batch et en mode streaming grâce à Spark et Kafka.

Objectifs pédagogiques

À la fin de cet atelier, les étudiants seront capables de :

Expliquer les couches : Batch Layer, Speed Layer, Serving Layer

Implémenter un traitement batch avec Spark

Implémenter un traitement streaming avec Spark Structured Streaming

Utiliser Kafka comme source temps réel

Fusionner les résultats batch & streaming

Comprendre les limites de l'architecture Lambda

Rappel théorique : Architecture Lambda
1) Batch Layer

Traite toutes les données historiques

Produit des résultats précis (batch views)

Exemple : Spark Batch ou Hadoop MapReduce

2) Speed Layer (Streaming Layer)

Traite les nouvelles données en temps réel

Produit des résultats rapides mais approximatifs

Exemple : Kafka + Spark Structured Streaming ou Flink

3) Serving Layer

Combine les résultats de Batch & Speed Layer

Fournit une vue finale aux applications clientes

Pré-requis techniques

Bases sur Spark (DataFrames, spark-submit)

Bases sur Kafka (topics, producteurs)

Docker et Docker Compose installés

Structure du projet
atelier-lambda/
│ docker-compose.yml
│
└───app/
    │ batch_job.py
    │ streaming_job.py
    │ serving_layer.py
    │
    └───datasets/
           transactions.json

Dataset utilisé

app/datasets/transactions.json

{"customer": "Ali", "amount": 120}
{"customer": "Sara", "amount": 90}
{"customer": "Ali", "amount": 200}
{"customer": "Mounir", "amount": 150}
{"customer": "Sara", "amount": 50}

Mise en place de l’environnement (Docker)

Démarrer la stack :

docker compose up -d


Vérifier :

docker ps

Batch Layer – Traitement des données historiques

Script : app/batch_job.py

Exécution :

docker exec -it spark spark-submit /app/batch_job.py


Objectif pédagogique : comprendre le rôle de la Batch Layer et produire une vue agrégée des données historiques.

Speed Layer – Traitement en temps réel
1. Création du topic Kafka
docker exec -it kafka kafka-topics.sh \
--create --topic real-time-orders \
--bootstrap-server kafka:9092

2. Producteur Kafka
docker exec -it kafka kafka-console-producer.sh \
--topic real-time-orders \
--bootstrap-server kafka:9092


Exemples de messages JSON :

{"customer":"Ali","amount":80}
{"customer":"Mounir","amount":200}
{"customer":"Sara","amount":40}

3. Lancer le streaming :
docker exec -it spark spark-submit /app/streaming_job.py


Objectif pédagogique : visualiser les agrégations en temps réel et comprendre la Speed Layer.

Serving Layer – Fusion Batch + Streaming

Script : app/serving_layer.py

Exécution :

docker exec -it spark python /app/serving_layer.py


Objectif : combiner les résultats batch et streaming pour produire la Serving View finale.

Captures d’écran

📸 Capture 1 — Conteneurs Docker actifs

(Insérer ici la capture d’écran de docker ps)

📸 Capture 2 — Résultat du batch job

(Insérer ici la capture d’écran de l’agrégation batch)

📸 Capture 3 — Producteur Kafka avec messages JSON

(Insérer ici la capture d’écran)

📸 Capture 4 — Spark Streaming en temps réel

(Insérer ici la capture d’écran du streaming)

📸 Capture 5 — Résultat final serving_view.json

(Insérer ici la capture d’écran du JSON final)

Questions et réponses

1. Rôle de chaque couche

Batch Layer : traite tout l’historique, résultats exacts

Speed Layer : traite en temps réel, résultats approximatifs

Serving Layer : combine batch + streaming, fournit vue finale

2. Modifier batch_job.py pour clients avec somme > 200

GroupBy customer, somme amount, filter total_amount > 200

3. Modifier streaming_job.py pour transactions amount >= 100

Lire le flux Kafka, filter amount >= 100

4. Adapter serving_layer.py pour écrire serving_view.json

Fusionner batch + streaming, write JSON mode overwrite

5. Limites de l’architecture Lambda

Double code entre batch et streaming

Complexité de maintenance

Risque d’incohérence

Infrastructure lourde

Scalabilité difficile

6. Motivation de l’architecture Kappa

Supprime Batch Layer

Pipeline streaming unique

Moins de maintenance, moins de coûts

Traitement unifié historique + temps réel

Conclusion

Cet atelier permet de comprendre et expérimenter l’architecture Lambda en utilisant Spark et Kafka, tout en visualisant la différence entre traitement batch et streaming, et la fusion des résultats dans une Serving Layer. Il met en évidence les avantages et limites de l’architecture Lambda, et prépare à des architectures plus modernes comme Kappa.
