# **1. Vue d’ensemble de l’implémentation pilote**

## Objectif du pilote

L’objectif de ce projet pilote est de tester l’efficacité du **cadre de gouvernance des données** développé pour Spotify.

Ce pilote vise à valider la capacité du cadre à :

- améliorer la qualité et la conformité des données,
- structurer la collaboration entre les équipes data et métiers,
- et garantir la sécurité et la traçabilité des informations.
- éliminer les silos des données (entre les équipes)

Il permettra d’identifier les obstacles techniques ou organisationnels avant le déploiement à grande échelle dans toute l’entreprise.

## Périmètre du pilote

Le pilote sera mené au sein du département Marketing , et portera sur les données d’engagement utilisateur et de performance des campagnes (ex. : Spotify Wrapped, données publicitaires, écoute et clics).

Ce choix s’explique par la criticité de ces données dans la stratégie business et leur sensibilité au regard du RGPD.

# 2. Objectifs principaux

Les objectifs du pilote s’alignent sur la stratégie globale de gouvernance des données et la vision du **Center of Excellence (CoE)** mis en place par Spotify :

- **Amélioration de la qualité des données :** renforcer la précision, la cohérence et la complétude des données via un suivi automatisé.
- **Conformité réglementaire (RGPD/CCPA) :** assurer la légalité des traitements et la traçabilité des consentements utilisateurs.
- **Accessibilité et intégration :** améliorer la circulation des données entre les équipes marketing, produit et IT grâce à un catalogue commun.
- **Gestion des risques :** détecter et corriger les failles de sécurité ou de gouvernance afin de réduire les risques opérationnels.
- Gestion d’un plateforme de données et élimination des silos entre les équipes

Le modèle **Center of Excellence (CoE)** est une **évolution naturelle** de ce modèle, mais **non encore atteinte**.

# **3. Équipe pilote et rôles**

| **Membre de l’équipe** | **Rôle** | **Responsabilités principales** |
| --- | --- | --- |
| [Nom à définir] | Lead du projet pilote / 
*Chief Data Officer (CDO)* | **Sponsor du pilote / Lead stratégique** 
Définit les objectifs du pilote, supervise la mise en œuvre du cadre de gouvernance, valide les indicateurs de performance et les résultats. |
| [Nom à définir] | Data Protection Officer (DPO) | **Expert conformité**
Garantit le respect du RGPD, CCPA et PCI-DSS ; supervise les outils de conformité (OneTrust, TrustArc) et les audits. |
| [Nom à définir] | Data Steward (Marketing) | **Responsable opérationnel qualité**
Supervise la qualité et la cohérence des données d’engagement marketing ; coordonne les actions de nettoyage via *Ataccama ONE*. |
| [Nom à définir] | Data Engineer (Marketing) | **Intégration & pipeline**
Met en place les flux de données entre sources marketing et le *Data Catalog* (Collibra) ; veille à la traçabilité et la sécurisation des échanges. |
| [Nom à définir] | Data Analyst / Scientist (Marketing) | **Exploitation analytique**
Analyse les données nettoyées pour mesurer la performance des campagnes et les impacts du pilote sur la qualité et la valeur business. |
| [Nom à définir] | IT Security Manager | **Support sécurité & infrastructure**
Supervise les protocoles de chiffrement et d’accès ; configure le suivi des incidents via *Splunk*. |
| [Nom à définir] | Data Governance Committee | **Instance de supervision**
Valide les processus, assure la cohérence inter-départements et suit la feuille de route du pilote dans le cadre du futur *Center of Excellence*. |
| [Nom à définir] | **Marketing Operations Manager** | **Représentant métier**
Fait le lien entre les besoins marketing et les équipes data ; exprime les cas d’usage et évalue les gains métiers liés à la qualité et à la disponibilité des données. |

# **4. Calendrier et jalons**

| **Milestone** | **Target date** | **Responsible team member** |
| --- | --- | --- |
| **Kick-off Meeting** | Semaine 1 | **Chief Data Officer (CDO)** & **Data Governance Committee** |
| **Data Assessment and Cleansing** | Semaines 2 à 5 | **Data Steward Marketing** & **Data Engineer Marketing** |
| **GDPR/CCPA Compliance Audit** | Semaines 5 à 7 | **Data Protection Officer (DPO)** |
| **Technical Setup and Data Integration** | Semaines 7 à 9 | **Data Engineer Marketing** & **IT Security Manager** |
| **Mid-Project Review and Adjustments** | Semaine 10 | **CDO** & **Data Governance Committee** |
| **Final Review and Pilot Closure** | Semaine 16 | **CDO**, **DPO**, & **Marketing Operations Manager** |

# 5. **Livrables clés**

## I. Data quality report

Le rapport présentera, de manière comparative, la situation **avant** et **après** le pilote selon quatre dimensions clés de la qualité des données.

| **Dimension** | **Description** | **Indicateur de mesure (KPI)** | **Résultat attendu** |
| --- | --- | --- | --- |
| **Complétude (Completeness)** | Pourcentage de champs renseignés dans les datasets marketing. | % de champs complets dans le Data Catalog. | **+15 %** d’amélioration de la complétude des données utilisateur et campagne. |
| **Exactitude (Accuracy)** | Concordance des données collectées avec les valeurs réelles ou de référence. | % d’erreurs détectées via *Ataccama ONE*. | **-20 %** d’erreurs détectées après nettoyage. |
| **Cohérence (Consistency)** | Uniformité des formats et définitions entre systèmes (ex. : devise, date, ID utilisateur). | Taux d’alignement inter-systèmes. | **+25 %** d’harmonisation des formats. |
| **Unicité (Uniqueness)** | Élimination des doublons dans les jeux de données marketing. | Nombre de doublons par 10 000 enregistrements. | **-30 %** de doublons détectés. |

## II. Résumé de la conformité au RGPD et au CCPA

Le rapport de conformité servira à mesurer les **écarts résiduels** entre les pratiques actuelles et les exigences légales, et à confirmer la capacité du cadre de gouvernance à **soutenir la conformité continue** à ces lois.

Voici les axes d’évaluation et indicateur de suivis (KPI)

| **Domaine de conformité** | **Indicateur (KPI)** | **Objectif visé** |
| --- | --- | --- |
| **Gestion du consentement** | % de consentements valides enregistrés dans OneTrust | 100 % des consentements documentés et traçables |
| **Droits des utilisateurs** | Délai moyen de traitement d’une demande (accès/suppression) | < 72h après la demande |
| **Notification des violations** | Délai de notification au DPO / autorité | < 72h après détection |
| **Cartographie des traitements** | Taux de traitements documentés dans le registre | 100 % des traitements critiques marketing |
| **Conservation et suppression** | % de données supprimées après durée légale | 100 % des données concernées |
| **Transferts internationaux** | Présence de clauses contractuelles types (CCT) | Conformité totale pour tous les transferts hors UE/US |

### Les résultats attendus

- Une **cartographie complète** des traitements marketing validée par le DPO.
- La **mise en conformité intégrale** des mécanismes de consentement et de gestion des droits utilisateurs.
- Une **traçabilité automatique** des actions de conformité (via *OneTrust* et *Splunk*).
- Des **rapports d’audit standardisés**, exploitables pour les futures revues de conformité à l’échelle du groupe.

## III. **Plan d’intégration technique**

Ce livrable présentera la manière dont les données marketing ont été intégrées, documentées et rendues accessibles de façon sécurisée et uniforme à l’ensemble du département.

| **Domaine** | **Indicateur** | **Objectif** |
| --- | --- | --- |
| Accessibilité | % de jeux de données documentés dans le catalogue | 100 % des jeux de données marketing clés |
| Intégration | Nombre de sources connectées au catalogue | 100 % des sources identifiées intégrées |
| Traçabilité | % de flux de données monitorés par Splunk | 100 % des flux critiques surveillés |
| Collaboration | Nombre d’utilisateurs actifs sur le Data Catalog | +30 % d’utilisateurs marketing formés et actifs |
| Interopérabilité | Temps moyen d’accès à une donnée inter-système | Réduction de 40 % du temps d’accès |

### **Les résultats attendus**

- **Un catalogue de données marketing complet** (via *Collibra / Alation*), rendant chaque dataset facilement repérable et documenté.
- **Des flux de données automatisés et sécurisés**, connectant les systèmes marketing, analytics et produit.
- **Une visibilité centralisée sur la circulation et l’usage des données**, grâce à la supervision *Splunk*.
- **Une réduction significative des silos organisationnels**, favorisant la collaboration entre les équipes et l’agilité dans les projets marketing.

## IV. Rapport d’évaluation des risques

Ce point vise à identifier, évaluer et documenter les risques liés à la gestion, à la sécurité et à la conformité des données dans le cadre du pilote.

| **Catégorie de risque** | **Indicateur** | **Objectif** |
| --- | --- | --- |
| **Risque de non-conformité** | Nombre d’écarts RGPD/CCPA identifiés | 0 écart critique à la fin du pilote |
| **Risque de sécurité** | Nombre d’incidents de sécurité détectés par Splunk | 0 incident majeur pendant le pilote |
| **Risque opérationnel** | Taux d’erreurs liées à la manipulation ou au transfert de données | Réduction de 25 % par rapport à la baseline |
| **Risque de qualité** | Données impactées par une incohérence ou une perte d’intégrité | Réduction de 30 % après nettoyage |
| **Risque de dépendance outil / process** | % de processus critiques non automatisés ou non documentés | < 10 % |

### **Les résultats attendus**

- Une **cartographie complète des risques data** du département marketing, classés par criticité.
- L’identification de **mesures correctives** immédiates (procédures de sécurité, formation, automatisation).
- La mise en place d’un **registre de suivi des risques** intégré à *OneTrust* et mis à jour trimestriellement.
- Une **réduction significative des risques majeurs** (non-conformité, perte de données, doublons, accès non autorisé).
- Une **culture de gestion proactive des risques**, intégrée dans la gouvernance data et les pratiques métiers.

## V. Commentaires des parties prenantes

Ce point à recueillir et analyser les **retours qualitatifs** des principales parties prenantes (équipes marketing, data, conformité, IT et direction) sur **l’efficacité et la pertinence du cadre de gouvernance des données** déployé lors du pilote.

| **Thème évalué** | **Indicateur de satisfaction** | **Objectif** |
| --- | --- | --- |
| **Qualité perçue des données** | Score moyen de satisfaction sur la fiabilité des données (1–5) | ≥ 4 |
| **Accessibilité et compréhension** | % d’utilisateurs estimant que les données sont plus faciles à trouver / comprendre | ≥ 80 % |
| **Utilisation du Data Catalog** | Taux d’adoption des outils (Collibra / Alation) | ≥ 75 % des utilisateurs formés actifs |
| **Collaboration inter-équipes** | % d’équipes déclarant une meilleure circulation de l’information | ≥ 70 % |
| **Confiance globale dans la gouvernance** | Score de confiance moyen (1–5) | ≥ 4 |

### **Les résultats attendus**

- Une **adhésion majoritaire** des équipes marketing et data à la nouvelle gouvernance.
- Une **amélioration notable de la compréhension et de l’usage des données** au quotidien.
- Des **recommandations concrètes** pour optimiser la clarté du catalogue, la qualité des métadonnées et la formation des utilisateurs.
- Une **base de retours réutilisable** pour la phase de déploiement global (Center of Excellence).

# 6. Gestion des risques

Identifier l’ensemble des risques susceptibles d’affecter la réussite du projet pilote de gouvernance des données et définir pour chacun une stratégie d’atténuation adaptée.

L’analyse des risques s’appuie sur :

- les bonnes pratiques du **DMBOK** et de la **norme ISO 27005** (évaluation de la probabilité × impact),
- les outils de monitoring et de conformité décrits dans le projet pilote,
- les observations faites lors de la phase de diagnostic et des précédents audits internes.

| **Catégorie de risque** | **Description du risque** | **Impact potentiel** | **Probabilité** | **Stratégie d’atténuation** |
| --- | --- | --- | --- | --- |
| **Organisationnel** | Manque de coordination entre les équipes data, marketing et IT. | Retard dans la mise en œuvre, incohérences dans les livrables. | Moyenne | Mettre en place un comité de gouvernance hebdomadaire et un reporting partagé (via Collibra). |
| **Qualité des données** | Données incomplètes ou incohérentes lors de l’intégration initiale. | Biais d’analyse, perte de fiabilité des indicateurs. | Élevée | Mettre en place un audit automatique via *Ataccama ONE* et un plan de nettoyage supervisé par le Data Steward. |
| **Conformité réglementaire** | Non-respect du RGPD ou du CCPA lors des traitements marketing. | Risque d’amende et d’atteinte à la réputation. | Moyenne | Utiliser *OneTrust* pour la cartographie des traitements et le suivi du consentement. Vérification finale par le DPO. |
| **Sécurité des données** | Fuite ou accès non autorisé à des données sensibles. | Risque juridique et perte de confiance des utilisateurs. | Faible à moyenne | Implémenter *Splunk* pour le monitoring temps réel et restreindre les droits d’accès via le CDO. |
| **Technique / Intégration** | Difficulté à connecter certaines sources de données au catalogue. | Retard ou perte de données lors du transfert. | Moyenne | Mobiliser les Data Engineers et documenter chaque flux dans *Collibra*. Tests d’intégration avant production. |
| **Humain / Adoption** | Faible engagement des utilisateurs ou résistance au changement. | Baisse d’efficacité du pilote, non-utilisation des outils. | Moyenne à élevée | Mettre en place une formation ciblée et des sessions de sensibilisation à la gouvernance. |
| **Financier / Ressources** | Sous-estimation du temps ou des ressources nécessaires. | Dépassement budgétaire ou extension de calendrier. | Moyenne | Planifier des marges de temps, prioriser les actions critiques et suivre les coûts mensuellement. |
| **Dépendance outil / fournisseur** | Dysfonctionnement d’un outil clé (Ataccama, Collibra, OneTrust). | Interruption temporaire des contrôles qualité ou conformité. | Faible | Prévoir des solutions de secours (backups, exports manuels) et une assistance technique contractuelle. |
| **Communication / Reporting** | Manque de visibilité sur l’avancement du pilote. | Décisions retardées, perte de confiance du comité. | Moyenne | Mettre en place un tableau de bord Power BI de suivi des KPIs et un reporting bi-hebdomadaire au CDO. |

### **Suivi et réévaluation**

- Les risques seront revus mensuellement par le Data Governance Committee, à l’aide d’un tableau de bord centralisé dans *OneTrust Risk Module*.
- Chaque risque fera l’objet d’une évaluation continue selon les critères :
    - *probabilité d’occurrence*,
    - *impact sur le projet*,
    - *efficacité des mesures d’atténuation*.
- En cas d’incident majeur, une procédure de revue immédiate et plan de mitigation d’urgence sera déclenchée sous la responsabilité du CDO et du DPO.

# 7. Formation et gestion du changement

Assurer une adoption fluide et durable du cadre de gouvernance des données au sein du département marketing, en accompagnant les employés tout au long du projet pilote.

## **I. Sessions de formation**

Des ateliers de formation ciblés seront organisés pour les employés du département marketing afin de leur permettre de maîtriser les nouveaux processus et outils de gouvernance.

Ces formations seront adaptées aux différents profils : managers, analystes, Data Stewards et collaborateurs opérationnels.

### **Objectifs des sessions**

- Comprendre les principes de la gouvernance des données (qualité, conformité, sécurité, traçabilité).
- Se familiariser avec les outils utilisés dans le pilote :
    - *Collibra / Alation* pour le catalogage et la documentation,
    - *Ataccama ONE* pour la qualité,
    - *OneTrust* pour la conformité,
    - *Splunk* pour le suivi des incidents.
- Acquérir les bons réflexes de gestion et de partage responsable des données.

### **Format et fréquence**

- 3 ateliers interactifs (2 h chacun) en petits groupes, animés par les Data Stewards et le CDO.
- Sessions de démonstration en ligne pour les outils techniques.
- Évaluation post-formation (quiz ou test de compréhension) pour mesurer le niveau de maîtrise.

## **II. Ressources d’assistance**

Afin de garantir un soutien continu pendant la phase pilote, plusieurs ressources d’assistance seront mises à disposition :

### **Documentation et guides utilisateurs**

- Guides pratiques sur l’utilisation du Data Catalog, la création de métadonnées, et la gestion des consentements.
- Fiches “bonnes pratiques” sur la sécurité, la confidentialité et la manipulation des données.
- Accès à une **base de connaissances interne (Notion / Confluence)** régulièrement mise à jour par les Data Stewards.

### **Tutoriels et support en ligne**

- Vidéos tutoriels et mini-formations disponibles sur l’intranet (parcours “Data Literacy”).
- Assistance technique via un **canal Slack dédié** ou un **helpdesk interne** pour signaler les problèmes liés aux outils ou aux accès.
- Mise en place d’un **“Data Support Office Hours”** : permanences hebdomadaires avec le Data Governance Committee pour les questions complexes.

## III. **Mécanisme de retour d’information**

Un dispositif structuré de **feedback** sera instauré afin de recueillir les commentaires, suggestions et difficultés rencontrées par les employés pendant le pilote.

### **Moyens mis en place**

- **Questionnaires anonymes** en ligne après chaque formation et à mi-parcours du pilote.
- **Entretiens courts** avec les responsables marketing et les Data Stewards pour collecter les retours qualitatifs.
- **Canal de feedback ouvert** sur Slack ou via un formulaire interne (*“Data Governance Feedback Form”*).

### **Analyse et exploitation des retours**

- Les commentaires seront centralisés dans un **rapport de satisfaction et d’adoption**, analysé par le **Data Governance Committee**.
- Les points récurrents donneront lieu à des **actions correctives** immédiates (mise à jour de guides, sessions de renforcement).
- Une **synthèse des retours utilisateurs** sera intégrée au rapport final du pilote afin de documenter la perception et l’appropriation du cadre.

# 8. Évaluation et enseignements tirés

Ce chapitre vise à évaluer la performance et l’efficacité du projet pilote de gouvernance des données au sein du département marketing.

L’évaluation repose sur les indicateurs clés de performance (KPI) définis lors du lancement du pilote, ainsi que sur les retours d’expérience des utilisateurs et des parties prenantes.

## I. Indicateurs d’évaluation

L’évaluation du pilote s’appuiera sur les KPI définis dans les chapitres précédents , couvrant les domaines de la qualité, de la conformité, de la sécurité et de l’intégration technique. Les résultats mesurés permettront de quantifier les améliorations concrètes et de déterminer si les objectifs du pilote ont été atteints.

| **Domaine** | **Indicateur de performance (KPI)** | **Résultat attendu** | **Méthode de mesure** |
| --- | --- | --- | --- |
| **Qualité des données** | Amélioration du taux de complétude et réduction des doublons | +15 à +30 % selon les dimensions mesurées | Audit automatisé via *Ataccama ONE* |
| **Conformité RGPD / CCPA** | % de consentements valides, rapidité de réponse aux demandes utilisateurs | 100 % de conformité pour les traitements critiques | Suivi via *OneTrust* |
| **Accessibilité et intégration** | % de sources intégrées au Data Catalog, temps moyen d’accès à la donnée | Réduction du temps d’accès de 40 % | Suivi via *Collibra / Power BI* |
| **Sécurité et traçabilité** | Nombre d’incidents de sécurité détectés / évités | 0 incident critique durant le pilote | Monitoring *Splunk* |
| **Adoption des utilisateurs** | Taux d’utilisation des outils et score de satisfaction | > 75 % d’utilisateurs actifs et satisfaits | Questionnaires et rapports d’usage |

### **Analyse des résultats**

- Les résultats obtenus seront **comparés aux valeurs cibles initiales** pour évaluer les progrès réels.
- Un **rapport d’évaluation final** sera produit, incluant graphiques, tendances et écarts d’amélioration.
- Ces données serviront de base pour la **feuille de route d’extension** du cadre de gouvernance.

## II. Enseignements tirés

À l’issue du projet pilote, une **revue de capitalisation** sera menée afin d’identifier les **facteurs de réussite**, les **points de vigilance** et les **axes d’amélioration** pour la suite.

### **Points forts observés**

- Meilleure collaboration entre les équipes marketing et data grâce au Data Catalog.
- Adoption rapide des outils *Ataccama ONE* et *OneTrust* par les Data Stewards.
- Amélioration notable de la qualité et de la fiabilité des jeux de données marketing.

### **Défis rencontrés**

- Difficultés d’intégration initiale de certaines sources hétérogènes.
- Charge de travail sous-estimée pour la documentation des métadonnées.
- Besoin accru de formation continue pour garantir une appropriation durable.

### **Recommandations pour la mise en œuvre à grande échelle**

- Étendre progressivement le cadre à d’autres départements (produit, finance, contenu) selon la maturité de chacun.
- Mettre en place un **Center of Excellence (CoE)** officiel pour piloter la gouvernance à l’échelle de l’entreprise.
- Standardiser les processus de contrôle qualité et de conformité entre tous les départements.
- Renforcer les actions de **formation et de data literacy** pour pérenniser la culture data.

## III. Commentaires des parties prenantes

Les retours qualitatifs des participants seront essentiels pour affiner le cadre avant déploiement global. Des entretiens et questionnaires seront réalisés auprès de l’ensemble des acteurs du pilote.

| **Partie prenante** | **Type de retour attendu** | **Objectif du feedback** |
| --- | --- | --- |
| **Data Stewards** | Retours sur les processus de contrôle qualité et l’usage des outils. | Identifier les points à améliorer dans la standardisation et la documentation. |
| **Data Engineers** | Retours sur la complexité des intégrations techniques. | Simplifier les workflows et améliorer la compatibilité inter-systèmes. |
| **DPO / Conformité** | Retours sur la traçabilité et la gestion des consentements. | Optimiser la conformité et la gestion des audits. |
| **Marketing Managers** | Retours sur la disponibilité et la pertinence des données. | Mesurer la valeur business apportée par la gouvernance. |
| **Comité de gouvernance** | Synthèse globale sur l’efficacité du cadre. | Décider du passage à la phase d’industrialisation. |

### **Utilisation des commentaires**

- Les observations seront **analysées et intégrées** dans un document “*Post-Pilot Improvement Plan*”.
- Un **atelier de restitution** sera organisé pour présenter les enseignements au Comité de gouvernance et définir les priorités du déploiement global.

# 9. Prochaines étapes

Sur la base des résultats positifs et des enseignements du projet pilote, ce chapitre définit les prochaines étapes nécessaires à l’extension du cadre de gouvernance des données à l’ensemble de Spotify.

## I. Plan d’extension

Le succès du pilote au sein du département marketing confirme la pertinence du cadre de gouvernance défini.

La prochaine étape consiste à étendre progressivement la gouvernance des données à d’autres départements stratégiques de Spotify, selon une approche structurée et progressive.

| **Phase** | **Département concerné** | **Objectif principal** | **Période estimée** |
| --- | --- | --- | --- |
| **Phase 1 – Consolidation** | Marketing (phase post-pilote) | Stabiliser les processus, former les utilisateurs restants et valider les premiers indicateurs consolidés. | Mois 1 à 3 |
| **Phase 2 – Extension ciblée** | Produit & Contenu | Harmoniser la gouvernance entre la donnée utilisateur et la donnée de recommandation (algorithmes, playlists, interactions). | Mois 4 à 8 |
| **Phase 3 – Intégration élargie** | Finance, RH, et Opérations | Étendre la gouvernance aux données administratives et de performance interne. | Mois 9 à 15 |
| **Phase 4 – Industrialisation globale** | Tous les départements (modèle CoE) | Centraliser les pratiques dans un **Center of Excellence Data Governance** coordonné par le CDO. | Mois 16 à 24 |

### **Actions clés prévues**

- **Déploiement progressif des outils techniques** (*Collibra, OneTrust, Ataccama, Splunk*) dans chaque département.
- **Formation et sensibilisation** de nouvelles équipes (produit, RH, finance) à la culture et aux standards de gouvernance.
- **Mise en place d’un Data Governance Committee étendu** pour assurer la cohérence inter-départements.
- **Standardisation des politiques et procédures** de qualité, sécurité et conformité à l’échelle de l’entreprise.
- **Création d’indicateurs de maturité par département**, afin de suivre la progression globale vers un modèle “data-driven”.

### **Objectif final**

Transformer la gouvernance actuelle (modèle *proactif, départemental*) en un **modèle “Center of Excellence” fédéré**, garantissant :

- la cohérence globale des pratiques,
- la réutilisabilité des données,
- et la supervision unifiée sous la responsabilité du **Chief Data Officer (CDO)**.

## II. Ajustements du cadre

Les enseignements tirés du pilote et les retours des parties prenantes (DPO, Data Stewards, Marketing, IT) permettront d’ affiner le cadre de gouvernance avant son déploiement complet.

### Axes d’ajustement identifiés

| **Domaine** | **Problématique observée** | **Ajustement proposé** |
| --- | --- | --- |
| **Qualité des données** | Charge de documentation élevée pour les Stewards | Automatiser la génération de métadonnées via *Ataccama ONE* et *Collibra APIs*. |
| **Conformité RGPD / CCPA** | Besoin de traçabilité renforcée sur certains flux publicitaires | Étendre *OneTrust* à la gestion des cookies et des consentements multi-plateformes. |
| **Sécurité & accès** | Gestion manuelle des rôles utilisateurs dans certains outils | Implémenter une gouvernance d’accès unifiée (IAM centralisée). |
| **Formation et adoption** | Besoin de sessions continues pour les nouveaux employés | Mettre en place un parcours de formation “Data Governance Onboarding”. |
| **Suivi de performance** | Indicateurs dispersés par département | Créer un tableau de bord global de gouvernance dans *Power BI* (suivi des KPI qualité, conformité et adoption). |

### **Améliorations structurelles prévues**

- Mise à jour de la **politique interne de gouvernance des données**, intégrant les nouvelles procédures issues du pilote.
- Ajout d’une **charte d’éthique des données** pour encadrer les usages de l’IA et du machine learning.
- Adoption d’un **modèle d’amélioration continue (PDCA)** : planification → exécution → vérification → adaptation.
- Intégration des retours d’utilisateurs et des résultats de la phase pilote dans la documentation du **Data Governance Framework v2.0**.