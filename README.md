# Atelier : Implémenter une Architecture Lambda simplifiée avec Spark et Kafka

## Réalisé par
👩‍💻 Hajar Elfallaki-Idrissi

---

## 📌 Table des matières
- Introduction
- Objectifs pédagogiques
- Rappel théorique : Architecture Lambda
- Pré-requis techniques
- Structure du projet
- Dataset utilisé
- Mise en place de l’environnement (Docker)
- Batch Layer – Traitement des données historiques
- Speed Layer – Traitement en temps réel
- Serving Layer – Fusion Batch + Streaming
- Captures d’écran
- Questions et réponses
- Conclusion

---

## Introduction
Cet atelier a pour objectif de guider les étudiants dans la mise en place d’une architecture Lambda simplifiée afin de comprendre les principes fondamentaux du traitement de données Big Data, à la fois en mode batch et en mode streaming grâce à Spark et Kafka.

---

## Objectifs pédagogiques
À la fin de cet atelier, les étudiants seront capables de :
- Expliquer les couches : Batch Layer, Speed Layer, Serving Layer
- Implémenter un traitement batch avec Spark
- Implémenter un traitement streaming avec Spark Structured Streaming
- Utiliser Kafka comme source temps réel
- Fusionner les résultats batch & streaming
- Comprendre les limites de l'architecture Lambda

---

## Rappel théorique : Architecture Lambda

### 1) Batch Layer
- Traite toutes les données historiques
- Produit des résultats précis (batch views)
- Exemple : Spark Batch ou Hadoop MapReduce

### 2) Speed Layer (Streaming Layer)
- Traite les nouvelles données en temps réel
- Produit des résultats rapides mais approximatifs
- Exemple : Kafka + Spark Structured Streaming ou Flink

### 3) Serving Layer
- Combine les résultats de Batch & Speed Layer
- Fournit une vue finale aux applications clientes

---

## Pré-requis techniques
- Bases sur Spark (DataFrames, spark-submit)
- Bases sur Kafka (topics, producteurs)
- Docker et Docker Compose installés

---

## Structure du projet
