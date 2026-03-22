# Politique de Gouvernance des Données

## 1. Introduction

Chez Spotify, la donnée alimente les algorithmes, améliore l'expérience des utilisateurs et constitue un actif stratégique à l'échelle mondiale. Dans ce contexte, la gouvernance des données doit garantir **fiabilité, conformité et éthique** de leur utilisation.

Ce document définit les principes, les exigences de conformité et les rôles encadrant la gestion des données chez Spotify. Il s'applique à l'ensemble des employés, partenaires et systèmes manipulant des données personnelles, opérationnelles ou analytiques.

## 2. Principes de gouvernance des données

*Source : Governance Principles Guide — aligné sur les 10 dimensions du DMBOK*

La gouvernance des données chez Spotify repose sur dix dimensions fondamentales issues du référentiel DMBOK, chacune traduite en engagement opérationnel :

| **Dimension DMBOK** | **Principe (définition DMBOK)** | **Engagement Spotify** | **Mise en œuvre** |
| --- | --- | --- | --- |
| **Data Governance** | Disponibilité, utilisabilité, intégrité et sécurité des données | Gouvernance dirigée par le CDO, soutenu par les Data Stewards, le DPO et le Comité de Gouvernance, pour garantir qualité, conformité et sécurité des données | Responsabilité, transparence et amélioration continue — aligné sur le Governance Principles Guide |
| **Data Architecture** | Cadre, règles et modèles structurant la collecte, le stockage et l'utilisation des données | Infrastructure moderne et scalable, encore partiellement intégrée entre départements — objectif : vision unifiée et fiable du patrimoine data | Modèles de données cohérents — cadre centralisé piloté par la gouvernance — principes de sécurité et de minimisation |
| **Data Development** | Création, test et maintenance des bases de données et pipelines de données | Équipes techniques collaborant avec les Data Stewards pour concevoir et maintenir des pipelines fiables, dans une logique de proactivité et de conformité | Principes de data quality et d'ethical use — cohérence et qualité garanties à chaque étape de développement |
| **Database Operations** | Gestion et maintenance quotidiennes des bases de données | Contrôle constant de la performance, de la sécurité et de la conformité, sous supervision du Data Governance Committee | Sécurité opérationnelle — gestion du cycle de vie des données — accountability et amélioration continue |
| **Data Security** | Protection contre les accès non autorisés, la corruption et les violations | Sécurité encadrée par le DPO avec politiques d'accès, d'encryption et de réponse aux incidents — conformité PCI-DSS et RGPD | Protection, transparence et minimisation — confidentialité et intégrité du patrimoine informationnel garanties |
| **Reference & Master Data Management** | Source unique et fiable pour les données de référence critiques | Référentiel centralisé pour harmoniser les données clés entre départements — Data Stewards garants de la cohérence des "golden records" | Élimination des doublons et incohérences — qualité, traçabilité et responsabilité des données |
| **Data Warehousing & BI** | Centralisation des données et analyse pour la prise de décision | Entrepôts de données alimentant tableaux de bord et personnalisation des expériences utilisateurs — l'une des maturités les plus fortes de Spotify | Data quality, utilisation éthique et amélioration continue — usage responsable et stratégique de la donnée |
| **Document & Content Management** | Création, organisation, stockage et récupération des documents et contenus numériques | Politiques claires d'accès, de stockage et de sécurité documentaire sous supervision du DPO et du Comité de Gouvernance — conformité RGPD et CCPA | Transparence et traçabilité — processus de conformité continue aux cadres réglementaires |
| **Metadata Management** | Données sur les données — contexte, origine, format et traçabilité | Traçabilité complète des actifs informationnels guidée par les principes d'accountability et de data quality | Documentation des sources, formats et propriétaires de données — favorise compréhension, gouvernance et réutilisation à l'échelle |
| **Data Quality** | Exactitude, exhaustivité, cohérence, unicité et actualité des données | Audits réguliers et indicateurs de qualité supervisés par le CDO et les Data Stewards — décisions fondées sur des données fiables et conformes aux standards internationaux | Exactitude et cohérence garanties — conformité aux standards internes et réglementaires |

## 3. Conformité réglementaire

*Source : Compliance Checklist*

Spotify adopte une approche **privacy-by-design** et **privacy-by-default** pour l'ensemble de ses traitements.

### RGPD (Europe)

| **Exigence** | **Mise en œuvre** |
| --- | --- |
| Consentement explicite | Requis pour le profilage, la publicité ciblée et les données sensibles |
| Droits des utilisateurs | Accès, rectification, suppression, portabilité, opposition — traitement sous 30 jours |
| Notification des violations | Détection et notification aux autorités sous 72h |
| Transferts internationaux | Clauses contractuelles types (SCC) — audits des fournisseurs tiers |
| DPO | Nommé, indépendant fonctionnellement, rattaché au Board (RGPD art. 38) |

### CCPA (Californie)

| **Exigence** | **Mise en œuvre** |
| --- | --- |
| Droit d'opt-out | Les utilisateurs californiens peuvent s'opposer à la vente de leurs données |
| Transparence | Publication annuelle des catégories de données collectées et de leur usage |
| Non-discrimination | Aucune dégradation de service pour les utilisateurs exerçant leurs droits |

> PCI-DSS s'applique aux flux de paiement Premium (Stripe, PayPal, Apple Pay) : tokenisation obligatoire, audit annuel QSA, cartographie des flux de données de paiement.
> 

## 4. Rôles et responsabilités

*Source : Data Governance Role Template*

La gouvernance des données repose sur quatre rôles clés qui fonctionnent en synergie :

| **Rôle** | **Responsabilité principale** | **Rattachement** |
| --- | --- | --- |
| **Chief Data Officer (CDO)** | *"Lead the data governance strategy and oversee data management across Spotify"* — définit les politiques et s'assure de leur alignement avec les objectifs métier | CEO |
| **Data Protection Officer (DPO)** | *"Ensure compliance with data protection regulations such as GDPR and CCPA"* — point de contact avec les autorités — indépendant fonctionnellement | Board / CEO |
| **Data Stewards** | *"Ensure data accuracy, consistency, and reliability"* — appliquent les politiques de gouvernance au niveau opérationnel par domaine métier | CDO |
| **Data Governance Committee** | *"Guide the data governance framework and ensure alignment across the organization"* — valide les politiques, arbitre les conflits inter-départements | Board |

Ces rôles fonctionnent en synergie : le CDO dirige la stratégie, le DPO agit comme autorité indépendante sur la conformité, les Data Stewards assurent la qualité opérationnelle, et le Comité de Gouvernance oriente et valide l'ensemble.

## 5. Processus de gouvernance

Le cadre opérationnel comprend :

- **Revues trimestrielles** de conformité et de qualité pilotées par le Data Governance Committee.
- **Audits internes annuels** évaluant l'efficacité des politiques (qualité, sécurité, conformité).
- **Gestion du cycle de vie des données** : de la collecte à la suppression sécurisée, selon les durées de rétention définies par type de données.
- **Procédures d'alerte et de correction** : tout incident affectant des données sensibles est notifié au DPO sous 4 heures.
- **Révision annuelle** du présent document, validée par le Comité de Gouvernance. Période de transition de 30 jours pour toute mise à jour majeure.

# 6. Schéma organisationnel

J’ai produit deux livrables complémentaires. Le premier répond strictement au périmètre demandé : les 4 rôles définis dans le Roles Template. Le second représente la vision organisationnelle cible que le framework de gouvernance doit permettre d'atteindre à horizon 18 mois, alignée sur le modèle Center of Excellence recommandé dans les ressources.

## Schéma Simple (As-Is)

![schema_simple.png](img/organigrame_simple.jpg)

# Ce vers quoi Spotify doit tendre (To-Be)

![schema_complet.jpg](img/Organigramme_complet.jpg)