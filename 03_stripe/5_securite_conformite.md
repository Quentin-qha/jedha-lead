# 5. Sécurité & conformité

# Risques identifiés

| Risque | Description |
| --- | --- |
| Fuite de données | Les données financières transitent par 5 composants (PostgreSQL → Kafka → Spark → Snowflake/NoSQL). Chaque point de transit est un point d'exposition potentiel. |
| Accès non autorisé | Des dizaines de services coexistent. Sans périmètres hermétiques, un composant compromis peut en exposer d'autres. |
| Décision erronée du modèle ML | Le modèle émet des décisions en production. Un déploiement non contrôlé peut bloquer des transactions légitimes ou laisser passer de la fraude. |

# Stratégies de sécurité

## Chiffrement

- **Au repos** — AES-256 sur l'ensemble des composants de stockage (PostgreSQL, Kafka, Snowflake, MongoDB, Cassandra). Les clés sont gérées via un KMS externe (AWS KMS ou HashiCorp Vault) — jamais co-localisées avec les données.
- **En transit** — TLS obligatoire sur toutes les connexions sans exception. Une seule liaison non chiffrée suffit à créer un point de faille.
- **Rotation des clés** — Tous les 90 jours via le KMS. Re-chiffrement progressif des données existantes, désactivation automatique de l'ancienne clé.

## Contrôle d'accès RBAC

Principe de moindre privilège appliqué à chaque composant. Un service autorisé à lire `fraud_score` dans MongoDB ne peut pas lire `ml_features`, écrire dans PostgreSQL, ou accéder à Snowflake. Les périmètres sont hermétiques.

| Rôle | Permissions | Composants concernés |
| --- | --- | --- |
| CDC | Lecture PostgreSQL, production Kafka | PostgreSQL → Kafka |
| Spark Transformation | Lecture Kafka, écriture Snowflake + NoSQL | Kafka → Snowflake, MongoDB, Cassandra |
| Pipeline ML | Lecture features Snowflake, écriture scores MongoDB | Snowflake → MongoDB |
| Service décision | Lecture fraud_score MongoDB, écriture décision PostgreSQL | MongoDB → PostgreSQL |
| Looker | Lecture tables reporting Snowflake uniquement | Snowflake |
| Équipe ML | Validation et déploiement MLflow | MLflow Registry |

## Segmentation réseau

Chaque composant est placé dans une zone réseau isolée avec des chemins de communication explicitement définis. Un compromis reste cantonné à sa zone.

| Zone | Composants | Communications autorisées |
| --- | --- | --- |
| Zone transactionnelle | PostgreSQL | CDC (lecture), boucle de retour ML (écriture) |
| Zone streaming | Kafka | CDC (entrée), Spark + NoSQL (sortie) |
| Zone traitement | Spark, Airflow | Kafka (entrée), Snowflake + NoSQL (sortie) |
| Zone analytique | Snowflake | Spark (écriture), Looker + ML (lecture) |
| Zone NoSQL | MongoDB, Cassandra | Spark (écriture), pipeline ML (lecture) |
| Zone reporting | Looker | Snowflake (lecture), utilisateurs HTTPS (sortie) |

## Audit & traçabilité

- **Audit trail** — Chaque opération sensible est loguée : identité du service, timestamp, ressource accédée, résultat. Logs stockés séparément des données de production.
- **Lignage** — Chaque donnée est traçable de sa source (PostgreSQL) à sa destination finale (Snowflake, MongoDB). Permet de répondre à toute question réglementaire sur l'origine et le chemin d'une donnée.

## Monitoring des anomalies

Baseline établie sur les comportements normaux d'accès par service. Alertes levées sur tout écart : accès hors périmètre, volume inhabituellement élevé, IP inconnue.

# Conformité réglementaire

## PCI-DSS

Exigences critiques et leur implémentation dans l'architecture :

| Exigence PCI-DSS | Implémentation |
| --- | --- |
| Chiffrement des données de carte | AES-256 au repos + TLS en transit sur l'ensemble du pipeline |
| Segmentation réseau | Zones isolées par niveau de sensibilité, aucun mouvement latéral possible |
| Contrôle d'accès strict | RBAC avec principe de moindre privilège sur chaque composant |
| Audit continu | Chaque accès aux données sensibles est loguée avec identité et timestamp |
| Tests réguliers | Tests de pénétration trimestriels, scans de vulnérabilités hebdomadaires |

Note : `Payment_Method` stocke uniquement un token et les 4 derniers chiffres de carte — jamais le numéro complet.

## RGPD

| Exigence RGPD | Implémentation |
| --- | --- |
| Droit à l'oubli | Lignage complet permettant d'identifier et supprimer toutes les données d'un utilisateur sans casser l'architecture |
| Minimisation des données | Seules les données nécessaires à chaque composant sont accessibles via RBAC |
| Traçabilité des traitements | Lignage bout-en-bout de PostgreSQL aux stores finaux |
| Explicabilité algorithmique | `Fraud_Assessment.model_name`, `model_version`, `risk_factors` documentent chaque décision ML (exigence d'explicabilité IA) |
| Notification de fuite | Monitoring temps réel avec alertes critiques < 5 minutes |

## CCPA

Le CCPA (California Consumer Privacy Act) s'applique aux utilisateurs Stripe basés en Californie. Les exigences clés sont couvertes par l'architecture existante : droit d'accès aux données personnelles via le lignage, droit de suppression via la traçabilité PII, et opt-out de la vente de données (non applicable — Stripe ne revend pas de données clients).

## SOC 2

SOC 2 évalue la sécurité, disponibilité, confidentialité, intégrité du traitement, et vie privée. L'architecture supporte les cinq principes via le chiffrement, le RBAC, le monitoring, l'audit trail et la segmentation réseau décrits ci-dessus.

# Plan de sécurité par composant

| Composant | Chiffrement repos | Chiffrement transit | RBAC | Segmentation | Audit | Rotation clés |
| --- | --- | --- | --- | --- | --- | --- |
| PostgreSQL | AES-256 | TLS | CDC (lecture), ML (écriture) | Zone transactionnelle isolée | Toutes requêtes loguées | 90 jours |
| Kafka | AES-256 | TLS | CDC (prod), Spark/NoSQL (conso par topic) | Zone streaming isolée | Volume/partition monitoré | 90 jours |
| Spark | — | TLS | Lecture Kafka, écriture Snowflake + NoSQL | Zone traitement isolée | Jobs loguées avec I/O | — |
| Airflow | — | — | Orchestration uniquement, jamais accès données | Zone traitement | Chaque workflow loguée | — |
| Snowflake | AES-256 | TLS | Spark (écriture), Looker + ML (lecture séparés) | Zone analytique isolée | Requêtes loguées avec volume | 90 jours |
| MongoDB | AES-256 par collection | TLS | Accès par collection, jamais croisé | Zone NoSQL | Accès hors périmètre alerté | 90 jours |
| Cassandra | AES-256 | TLS | Kafka (écriture), Spark (lecture) | Zone NoSQL, sans comm MongoDB | — | 90 jours |
| Looker | — | TLS | Lecture reporting Snowflake uniquement | Zone reporting | Dashboard + identité loguées | — |
| MLflow | — | — | Équipe ML (deploy), Sécu (lecture) | — | Déploiements + rollbacks loguées | — |

# Plan de réponse à incident

| Niveau | Exemple | Réponse | Délai |
| --- | --- | --- | --- |
| Critique | Accès non autorisé sur PostgreSQL | Isolation composant, révocation accès, notification sécurité | < 5 min |
| Élevé | Anomalie volume Kafka ou dérive ML > 10% | Alerte sécurité/ML, investigation, isolation si confirmé | < 15 min |
| Moyen | Dérive performance modèle ML | Alerte équipe ML, évaluation, rollback si nécessaire | < 1 heure |
| Faible | Tentative d'accès bloquée par RBAC | Log enregistré, revue quotidienne | 24 heures |

# Fréquences de maintenance

| Action | Fréquence |
| --- | --- |
| Rotation des clés de chiffrement | 90 jours |
| Tests de pénétration | Trimestriel |
| Scans de vulnérabilités | Hebdomadaire |
| Revue des permissions RBAC | Mensuelle |
| Audit des logs | Quotidien |
| Validation des modèles ML | À chaque déploiement |