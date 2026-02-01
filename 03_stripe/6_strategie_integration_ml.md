# 6. Stratégie d'intégration de l'apprentissage automatique

# **Contexte & objectif**

L'architecture de données repose sur un modèle de détection de fraude qui doit prendre des décisions en temps réel : autoriser ou bloquer une transaction. Ce modèle n'existe pas isolément. Il s'intègre directement dans le pipeline de données, depuis l'extraction des caractéristiques jusqu'à l'écriture de la décision finale.

Cette stratégie décrit comment le modèle est alimenté, déployé, surveillé, et comment ses sorties sont intégrées dans les stores NoSQL pour garantir une décision rapide, fiable, et traçable.

# Architecture du pipeline ML

Le pipeline ML s'articule autour de cinq étapes distinctes, chacune avec un rôle précis dans le système.

### **Extraction des caractéristiques**

Les données brutes sont transformées en features exploitables par le modèle.

### **Entraînement**

Le modèle est entraîné sur les données historiques stockées dans Snowflake et Cassandra.

### **Validation**

Le modèle est évalué sur ses métriques avant toute mise en production.

### **Déploiement**

Le modèle validé est poussé en production via MLflow Registry.

### **Inférence & décision**

Le modèle score une transaction en temps réel et émet une décision qui est écrite dans MongoDB et PostgreSQL.

# Extraction des features

## Sources de données pour l'extraction

| Source | Données utilisées | Rôle dans l'extraction |
| --- | --- | --- |
| PostgreSQL | Données brutes de transaction | Source primaire : montant, merchant, géolocalisation, timestamp |
| Cassandra | Données historiques | Patterns temporels : comportement passé du client sur 30/90/365 jours |
| MongoDB  | Features précédemment calculées | Reutilisation des features récentes pour éviter les recalculs |

## Comment les features sont extraites

### **1. Collecte**

Lorsqu'une transaction arrive dans PostgreSQL, le CDC la pousse vers Kafka. Spark consomme cette transaction depuis Kafka.

### **2. Enrichissement**

Spark joint la transaction brute avec les données historiques stockées dans Cassandra. Par exemple : le comportement habituel du client, ses transactions récentes, la moyenne de ses montants habituels.

### **3. Calcul des features**

À partir de ces données jointes, Spark calcule les caractéristiques nécessaires au modèle.

Les features calculées sont de trois types :

**Features comportementales** 

Elles décrivent le comportement historique du client.

- Nombre de transactions sur les 24 dernières heures
- Montant moyen des 30 derniers jours
- Nombre de merchants distincts utilisés sur les 7 derniers jours
- Taux de transactions internationales sur les 90 derniers jours

**Features contextuelles**

Elles décrivent le contexte de la transaction en cours.

- Écart entre le montant actuel et la moyenne historique du client
- Heure de la transaction par rapport aux horaires habituels
- Géolocalisation par rapport à la dernière transaction
- Type de merchant comparé aux merchants habituels

**Features d'alerte**

Elles signalent des comportements à risque.

- Nombre de tentatives échouées dans les dernières minutes
- Changement récent des informations du compte
- Première utilisation d'un nouveau dispositif de paiement
- Vitesse de déplacement géographique impossible entre deux transactions

### **4. Stockage**

Les features calculées sont écrites dans MongoDB, collection `ml_features`. Elles restent disponibles pour une utilisation immédiate par le modèle en inférence, et pour un usage futur en entraînement.

## Cohérence des features entre entraînement et inférence

C'est un problème classique en production ML. Si les features utilisées pendant l'entraînement ne sont pas identiques à celles utilisées en inférence, le modèle ne fonctionne pas comme prévu.

Dans cette architecture, la cohérence est garantie par un seul point de vérité : **MongoDB (`ml_features`)**. Les mêmes features sont utilisées pour entraîner le modèle et pour lui alimenter les données en temps réel. Spark applique la même logique de calcul dans les deux cas.

# Entraînement du modèle

## Données d'entraînement

| Source | Volume | Rôle |
| --- | --- | --- |
| Snowflake | Données historiques complètes | Dataset principal d'entraînement |
| Cassandra | Données temporelles granulaires | Patterns comportementaux long terme |
| MongoDB | Scores et décisions passées | Labels pour l'entraînement supervisé |

## Processus d'entraînement

### **Sélection des données**

Un dataset est extrait depuis Snowflake avec une fenêtre temporelle définie. Les labels (BLOCKED/APPROVED) proviennent des décisions passées stockées dans MongoDB.

### **Découpage**

Le dataset est découpé en trois ensembles : entraînement (70%), validation (20%), test (10%). Le découpage est fait par fenêtre temporelle, pas aléatoirement, pour éviter la fuite de données entre les périodes.

### **Entraînement**

Le modèle est entraîné sur l'ensemble entraînement, avec validation croisée sur l'ensemble validation.

### **Évaluation**

Le modèle est évalué sur l'ensemble test avec les métriques suivantes :

| Métrique | Seuil accepté | Pourquoi |
| --- | --- | --- |
| Précision | > 95% | Éviter les faux positifs — ne pas bloquer des transactions légitimes |
| Rappel | > 90% | Capter le maximum de fraude réelle |
| F1-Score | > 92% | Équilibre entre précision et rappel |
| AUC-ROC | > 0.97% | Performance globale du modèle sur tous les seuils |

### **Tracking**

Chaque run d'entraînement est enregistré dans MLflow avec les hyperparamètres utilisés, les métriques obtenues, et le dataset utilisé. Rien n'est perdu, tout est reproductible.

# Validation avant déploiement

## Critères de validation

| Critère | Description | Seuil |
| --- | --- | --- |
| Performance sur test set | Le modèle doit atteindre les seuils définis ci-dessus | Toutes les métriques au-dessus des seuils |
| Comparaison avec le modèle actuel | Le nouveau modèle doit surpasser le modèle en production | Amélioration d'au moins 2% sur le F1-Score |
| Test de stabilité | Le modèle doit se comporté de manière stable sur des données récentes | Pas de dérive > 5% sur les 7 derniers jours |
| Test de biais | Le modèle ne doit pas discriminer un groupe de clients de manière injuste | Taux de blocage équitable entre segments |

## Processus de validation

### **Évaluation automatique**

MLflow compare automatiquement les métriques du nouveau modèle avec celles du modèle en production.

### **Revue manuelle**

Si les métriques sont satisfaites, l'équipe ML revoit les résultats, les erreurs notables, et les comportements sur les cas limites.

### **Approbation**

Si la revue est positive, le modèle est approuvé dans MLflow Registry et prêt à être déployé.

# Déploiement du modèle

## Comment le déploiement se fait

### 1. Promotion

Le modèle validé est promu dans MLflow Registry au statut "Production". La version précédente reste accessible pour un rollback.

### 2. Déploiement progressif

Le nouveau modèle n'est pas déployé d'un coup sur 100% du trafic. Il commence sur 10% des transactions, puis 25%, puis 50%, puis 100%. À chaque palier, les métriques sont surveillées.

### 3. Monitoring post-deploiement

Pendant les 48 premières heures, le modèle est surveillé en temps réel avec des seuils plus stricts que d'habitude.

## Rollback

Si à n'importe quel moment le modèle se comporte de manière anormale, un rollback vers la version précédente est déclenché.

| Scénario de rollback | Délai de réponse |
| --- | --- |
| Taux de faux positifs > 5% | Immédiat — rollback automatique |
| Dérive de performance > 10% | < 15 minutes — rollback après confirmation |
| Comportement anormal détecté manuellement | < 1 heure — rollback après évaluation |

# Inférence en temps réel

## Flux d'inférence

### 1. Réception

Une transaction arrive dans le pipeline via Kafka.

### 2. Récupération des features

Les features nécessaires sont récupérées depuis MongoDB (`ml_features`). Cette étape doit être rapide — MongoDB garantit un accès à faible latence.

### 3. Scoring

Le modèle en production reçoit les features et calcule un score de fraude entre 0 et 1.

### 4. Décision

Sur la base du score, une décision est émise :

| Score | Décision | Action |
| --- | --- | --- |
| 0 à 0.3 | APPROVED | Transaction autorisée |
| 0.3 à 0.7 | REVIEW | Transaction envoyée pour revue manuelle |
| 0.7 à 1 | BLOCKED | Transaction bloquée immédiatement |

### 5. Écriture des sorties

Trois écritures sont effectuées simultanément :

- Le score → MongoDB (`fraud_score`)
- Les features utilisées → MongoDB (`ml_features`)
- La décision → PostgreSQL (BLOCKED / APPROVED / REVIEW)

## **Contraintes de latence**

| Étape | Latence maximale autorisée |
| --- | --- |
| Récupération des features depuis MongoDB | < 5ms |
| Calcul du score par le modèle | < 10ms |
| Écriture de la décision dans PostgreSQL | < 20ms |
| Latence totale du pipeline d'inférence | < 100ms |

# Surveillance des performances

## Métriques surveillées en production

| Métrique | Seuil d'alerte | Niveau |
| --- | --- | --- |
| Taux de faux positifs | > 5% | Critique — rollback automatique |
| Taux de faux négatifs | > 10% | Élevé — investigation immédiate |
| Dérive de performance (F1-Score) | > 10% par rapport à la baseline | Élevé — évaluation + rollback si confirmé |
| Latence d'inférence | > 100ms | Moyen — investigation |
| Volume de scores émis | Écart > 2x la moyenne sur 7 jours | Moyen — vérification |
| Distribution des scores | Changement significatif de la distribution | Élevé — signe de dérive de données |

## Dérive des données (Data Drift)

Un modèle peut être parfait lors de son entraînement et se dégrader en production parce que les données changent. C'est ce qu'on appelle la dérive.

Dans cette architecture, deux types de dérive sont surveillés :

### **Dérive des features**

Les caractéristiques en entrée du modèle changent par rapport à celles utilisées pendant l'entraînement. Par exemple, le montant moyen des transactions augmente soudainement.

### **Dérive des labels**

Le comportement de la fraude lui-même change. Nouveaux patterns, nouvelles techniques d'attaque.

MLflow monitor ces deux types de dérive en continu. Si une dérive significative est détectée, une alerte est levée et un re-entraînement du modèle est déclenché.

## Re-entraînement

| Scénario | Fréquence de re-entraînement |
| --- | --- |
| Dérive détectée par le monitoring | Immédiat — re-entraînement déclenché automatiquement |
| Pas de dérive mais évolution du volume | Mensuel |
| Mise à jour régulière planifiée | Tous les 3 mois |

## Traçabilité complète

Chaque décision émise par le modèle en production est traçable de bout en bout :

- **Quelles features** ont été utilisées → MongoDB (`ml_features`)
- **Quel score** a été émis → MongoDB (`fraud_score`)
- **Quelle décision** a été prise → PostgreSQL
- **Quel modèle** a pris cette décision → MLflow (version, date de déploiement)
- **Pourquoi** cette décision → les features et le score permettent de reconstruire le raisonnement

Cette traçabilité est essentielle en cas de contestation d'une décision par un client, ou en cas de contrôle réglementaire.

# Résumé

| Store | Collection | Rôle dans le pipeline ML | Accès |
| --- | --- | --- | --- |
| MongoDB | `ml_features` | Stocke les features calculées par Spark, utilisées en inférence et en entraînement | Écriture par Spark, lecture par le pipeline ML |
| MongoDB | `fraud_score` | Stocke les scores émis par le modèle en production | Écriture par le pipeline ML, lecture par le service de décision |
| Cassandra | Données historiques | Fournit les patterns temporels pour l'extraction de features | Écriture par Kafka, lecture par Spark |