# 🚀 Architecture Lambda avec Spark et Kafka

> Atelier pratique pour implémenter une architecture Lambda simplifiée

**Réalisé par** : 👩‍💻 Hajar Elfallaki-Idrissi

---

## 📋 Table des matières

- [Introduction](#introduction)
- [Objectifs pédagogiques](#objectifs-pédagogiques)
- [Architecture Lambda - Rappel théorique](#architecture-lambda---rappel-théorique)
- [Pré-requis techniques](#pré-requis-techniques)
- [Structure du projet](#structure-du-projet)
- [Dataset utilisé](#dataset-utilisé)
- [Installation et démarrage](#installation-et-démarrage)
- [Batch Layer](#batch-layer--traitement-des-données-historiques)
- [Speed Layer](#speed-layer--traitement-en-temps-réel)
- [Serving Layer](#serving-layer--fusion-batch--streaming)
- [Code source](#code-source)
- [Captures d'écran](#captures-décran)
- [Questions et réponses](#questions-et-réponses)
- [Conclusion](#conclusion)

---

## 🎯 Introduction

Cet atelier guide les étudiants dans la mise en place d'une **architecture Lambda simplifiée** pour comprendre les principes fondamentaux du traitement de données Big Data, à la fois en mode **batch** et en mode **streaming** grâce à **Apache Spark** et **Apache Kafka**.

---

## 📚 Objectifs pédagogiques

À la fin de cet atelier, vous serez capable de :

✅ Expliquer les trois couches de l'architecture Lambda : **Batch Layer**, **Speed Layer**, **Serving Layer**  
✅ Implémenter un traitement batch avec **Spark**  
✅ Implémenter un traitement streaming avec **Spark Structured Streaming**  
✅ Utiliser **Kafka** comme source temps réel  
✅ Fusionner les résultats batch & streaming  
✅ Comprendre les limites de l'architecture Lambda  

---

## 🏗️ Architecture Lambda - Rappel théorique

### 1️⃣ Batch Layer
- **Rôle** : Traite toutes les données historiques
- **Résultat** : Vues batch précises et complètes
- **Technologies** : Spark Batch, Hadoop MapReduce

### 2️⃣ Speed Layer (Streaming Layer)
- **Rôle** : Traite les nouvelles données en temps réel
- **Résultat** : Résultats rapides mais approximatifs
- **Technologies** : Kafka + Spark Structured Streaming, Apache Flink

### 3️⃣ Serving Layer
- **Rôle** : Combine les résultats de Batch & Speed Layer
- **Résultat** : Vue finale unifiée pour les applications clientes

```
┌─────────────────────────────────────────────────────────────┐
│                     ARCHITECTURE LAMBDA                     │
└─────────────────────────────────────────────────────────────┘

  Données historiques          Nouvelles données (temps réel)
         │                              │
         ▼                              ▼
   ┌───────────┐                 ┌──────────────┐
   │  Batch    │                 │    Speed     │
   │  Layer    │                 │    Layer     │
   │  (Spark)  │                 │(Kafka+Spark) │
   └─────┬─────┘                 └──────┬───────┘
         │                              │
         │         ┌──────────────┐     │
         └────────▶│   Serving    │◀────┘
                   │    Layer     │
                   └──────┬───────┘
                          │
                          ▼
                   Applications clientes
```

---

## ⚙️ Pré-requis techniques

- 🐳 **Docker** et **Docker Compose** installés
- 🐍 Connaissances de base en **Python**
- ⚡ Notions sur **Apache Spark** (DataFrames, spark-submit)
- 📨 Notions sur **Apache Kafka** (topics, producteurs)

---

## 📁 Structure du projet

```
atelier-lambda/
│
├── docker-compose.yml          # Configuration Docker (Spark + Kafka + Zookeeper)
│
└── app/
    ├── batch_job.py            # Script Batch Layer
    ├── streaming_job.py        # Script Speed Layer
    ├── serving_layer.py        # Script Serving Layer
    │
    └── datasets/
        └── transactions.json   # Données historiques
```

---

## 📊 Dataset utilisé

**Fichier** : `app/datasets/transactions.json`

```json
{"customer": "Ali", "amount": 120}
{"customer": "Sara", "amount": 90}
{"customer": "Ali", "amount": 200}
{"customer": "Mounir", "amount": 150}
{"customer": "Sara", "amount": 50}
```

---

## 🐳 Installation et démarrage

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd atelier-lambda
```

### 2. Créer le fichier `docker-compose.yml`

```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    container_name: kafka
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  spark:
    image: bitnami/spark:3.5
    container_name: spark
    environment:
      - SPARK_MODE=master
    ports:
      - "8080:8080"
      - "7077:7077"
    volumes:
      - ./app:/app
```

### 3. Démarrer les services

```bash
docker compose up -d
```

### 4. Vérifier que les conteneurs sont actifs

```bash
docker ps
```

Vous devriez voir : `zookeeper`, `kafka`, `spark`

---

## 🗂️ Batch Layer – Traitement des données historiques

### Objectif
Traiter l'ensemble des données historiques et produire une vue agrégée par client.

### Script : `app/batch_job.py`

```python
from pyspark.sql import SparkSession

# Initialiser Spark
spark = SparkSession.builder \
    .appName("BatchLayer") \
    .getOrCreate()

# Lire les données historiques
df = spark.read.json("/app/datasets/transactions.json")

# Agréger par client
batch_view = df.groupBy("customer").sum("amount") \
    .withColumnRenamed("sum(amount)", "total_amount")

# Afficher le résultat
batch_view.show()

# Sauvegarder le résultat
batch_view.write.mode("overwrite").json("/app/output/batch_view")

spark.stop()
```

### Exécution

```bash
docker exec -it spark spark-submit /app/batch_job.py
```

### Résultat attendu

```
+--------+------------+
|customer|total_amount|
+--------+------------+
|Ali     |320         |
|Sara    |140         |
|Mounir  |150         |
+--------+------------+
```

---

## ⚡ Speed Layer – Traitement en temps réel

### Objectif
Traiter les nouvelles transactions en temps réel via Kafka et Spark Streaming.

### 1. Créer le topic Kafka

```bash
docker exec -it kafka kafka-topics.sh \
  --create --topic real-time-orders \
  --bootstrap-server kafka:9092
```

### 2. Script : `app/streaming_job.py`

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum

# Initialiser Spark avec support Kafka
spark = SparkSession.builder \
    .appName("SpeedLayer") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

# Lire le flux Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "real-time-orders") \
    .load()

# Parser les données JSON
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("customer", StringType(), True),
    StructField("amount", IntegerType(), True)
])

parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Agréger en temps réel
streaming_view = parsed_df.groupBy("customer").agg(_sum("amount").alias("total_amount"))

# Afficher les résultats en continu
query = streaming_view.writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()
```

### 3. Lancer le streaming job

```bash
docker exec -it spark spark-submit /app/streaming_job.py
```

### 4. Envoyer des messages au producteur Kafka

```bash
docker exec -it kafka kafka-console-producer.sh \
  --topic real-time-orders \
  --bootstrap-server kafka:9092
```

Saisir les messages suivants :

```json
{"customer":"Ali","amount":80}
{"customer":"Mounir","amount":200}
{"customer":"Sara","amount":40}
```

### Résultat en temps réel

Les agrégations s'affichent en continu dans la console Spark.

---

## 🔄 Serving Layer – Fusion Batch + Streaming

### Objectif
Combiner les résultats du batch et du streaming pour produire une vue finale unifiée.

### Script : `app/serving_layer.py`

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ServingLayer") \
    .getOrCreate()

# Charger la vue batch
batch_view = spark.read.json("/app/output/batch_view")

# Charger la vue streaming (simulée ici via un fichier)
streaming_view = spark.read.json("/app/output/streaming_view")

# Fusionner les deux vues
serving_view = batch_view.union(streaming_view) \
    .groupBy("customer").sum("total_amount") \
    .withColumnRenamed("sum(total_amount)", "final_amount")

# Afficher le résultat
serving_view.show()

# Sauvegarder la vue finale
serving_view.write.mode("overwrite").json("/app/output/serving_view.json")

spark.stop()
```

### Exécution

```bash
docker exec -it spark python /app/serving_layer.py
```

### Résultat final

```
+--------+------------+
|customer|final_amount|
+--------+------------+
|Ali     |400         |
|Sara    |180         |
|Mounir  |350         |
+--------+------------+
```

---

## 📸 Captures d'écran

### 📸 Capture 1 — Conteneurs Docker actifs
*(Insérer ici la capture d'écran de `docker ps`)*

### 📸 Capture 2 — Résultat du batch job
*(Insérer ici la capture d'écran de l'agrégation batch)*

### 📸 Capture 3 — Producteur Kafka avec messages JSON
*(Insérer ici la capture d'écran)*

### 📸 Capture 4 — Spark Streaming en temps réel
*(Insérer ici la capture d'écran du streaming)*

### 📸 Capture 5 — Résultat final `serving_view.json`
*(Insérer ici la capture d'écran du JSON final)*

---

## ❓ Questions et réponses

### 1. Quel est le rôle de chaque couche ?

- **Batch Layer** : Traite tout l'historique, produit des résultats exacts
- **Speed Layer** : Traite en temps réel, résultats rapides mais approximatifs
- **Serving Layer** : Combine batch + streaming, fournit la vue finale

### 2. Comment modifier `batch_job.py` pour ne garder que les clients avec une somme > 200 ?

```python
batch_view = df.groupBy("customer").sum("amount") \
    .withColumnRenamed("sum(amount)", "total_amount") \
    .filter(col("total_amount") > 200)
```

### 3. Comment modifier `streaming_job.py` pour filtrer les transactions >= 100 ?

```python
parsed_df = parsed_df.filter(col("amount") >= 100)
```

### 4. Comment adapter `serving_layer.py` pour écrire `serving_view.json` ?

```python
serving_view.write.mode("overwrite").json("/app/output/serving_view.json")
```

### 5. Quelles sont les limites de l'architecture Lambda ?

❌ **Double code** entre batch et streaming  
❌ **Complexité de maintenance**  
❌ **Risque d'incohérence** entre les deux couches  
❌ **Infrastructure lourde** (gestion de deux pipelines)  
❌ **Scalabilité difficile**  

### 6. Quelle est la motivation de l'architecture Kappa ?

✅ Supprime la Batch Layer  
✅ Pipeline streaming unique  
✅ Moins de maintenance, coûts réduits  
✅ Traitement unifié historique + temps réel  

---

## 🎓 Conclusion

Cet atelier permet de comprendre et expérimenter l'**architecture Lambda** en utilisant **Apache Spark** et **Apache Kafka**, tout en visualisant la différence entre traitement batch et streaming, et la fusion des résultats dans une Serving Layer.

Il met en évidence les **avantages** et **limites** de l'architecture Lambda, et prépare à des architectures plus modernes comme **Kappa**.

---

## 📝 Licence

Ce projet est à usage pédagogique.

---

**Bon courage ! 🚀**
