# 5. Sécurité & conformité

# **Pourquoi la sécurité est particulièrement critique chez Stripe**

Stripe ne traite pas des données ordinaires. Chaque transaction qui passe par la plateforme embarque des informations financières sensibles : des données de carte, des comportements de paiement, des informations personnelles des utilisateurs.

Dans ce contexte, une faille n'est jamais anodine. Elle expose directement les clients, elle met la plateforme en violation de réglementations aussi strictes que le **PCI-DSS** ou le **RGPD**, et elle peut détruire la confiance que les utilisateurs ont accordé à Stripe. Pour une plateforme de paiement, cette confiance est tout.

La sécurité n'est donc pas un élément parmi d'autres dans cette architecture. Elle est la condition sur laquelle repose la viabilité du système entier.

# Les risques identifiés

## **Risque de fuite de données**

Les données financières circulent à travers plusieurs composants : PostgreSQL, Kafka, Snowflake, MongoDB, Cassandra. Chaque point de transit est un point potentiel d'exposition. Si une de ces couches n'est pas correctement protégée, les données sensibles peuvent être accessibles à des acteurs non autorisés.

## **Risque d'accès non autorisé**

L'architecture comporte de nombreux services qui communiquent entre eux. Un service qui a besoin de lire un score de fraude n'a aucune raison d'accéder aux données brutes du client ou aux features du modèle. Si ces périmètres ne sont pas bien définis, le risque de surfiltration interne devient réel — un composant compromis peut en exposer d'autres.

## **Risque de décision erronée du modèle**

Le modèle ML émet des décisions en production : bloquer ou autoriser une transaction. Si ce modèle n'est pas correctement suivi, validé, ou si une version défaillante est déployée sans contrôle, les conséquences sont directes : des transactions légitimes bloquées, ou de la fraude laissée passer.

# Stratégies de sécurité

## **Le chiffrement**

Le chiffrement est le processus qui transforme une donnée lisible en une donnée incompréhensible pour quiconque ne possède pas la clé de déchiffrement. C'est la même logique qu'un coffre-fort : les données sont à l'intérieur, mais sans la bonne clé, personne ne peut y accéder.

### **Chiffrement au repos**

C'est la protection des données **stockées**.

Les données sont chiffrées au moment de l'écriture et déchiffrées au moment de la lecture, de manière transparente pour l'application. Le service qui lit la donnée ne sait même pas qu'elle était chiffrée. C'est géré en dehors de la couche applicative.

L’algorithme standard utilise pour chiffré les données est l’AES-256. C'est ce que utilisent la grande majorité des systèmes en production aujourd'hui. Il est considéré comme inviolable avec les moyens actuels.

Les clés de chiffrement ne sont jamais stockées au même endroit que les données. Elles sont gérées par un système dédié — un **KMS (Key Management System)** comme AWS KMS, Google Cloud KMS, ou HashiCorp Vault. Le KMS contrôle qui peut utiliser quelle clé, et garde un historique complet des usages.

### **Chiffrement en transit**

C'est la protection des données **en mouvement**.

Le protocole **TLS (Transport Layer Security)** chiffre la communication entre deux points. Concrètement, avant même qu'une donnée soit envoyée, les deux composants établissent un tunnel chiffré. Tout ce qui circule dans ce tunnel est invisible pour quiconque l'intercepte en route.

TLS doit être obligatoire sur toutes les communications, sans exception. Une seule liaison non chiffrée suffit pour créer un point de faille. Dans une architecture comme celle de Stripe, ça veut dire chaque connexion entre chaque brique du pipeline.

### **Rotation des clés**

Une clé de chiffrement ne doit jamais être utilisée indéfiniment. Si une clé est compromise elle expose toutes les données qui ont été chiffrées avec elle. La rotation régulière limite cette exposition.

Le KMS génère automatiquement une nouvelle clé selon un calendrier défini — tous les 90 jours, tous les 6 mois, selon la politique de sécurité. Les données chiffrées avec l'ancienne clé sont progressivement re-chiffrées avec la nouvelle. L'ancienne clé est ensuite désactivée.

## **Contrôle d'accès RBAC**

RBAC (Role-Based Access Control) est un système de contrôle d'accès qui définit les permissions non pas par utilisateur ou par service individuellement, mais par rôle. On crée des rôles, on leur attribue des permissions, puis on associe chaque utilisateur ou service à un rôle.

Une seule logique, s'assurer que chaque composant du système ne voit que ce qu'il a besoin de voir.
Dans l'architecture de Stripe, des dizaines de services coexistent. Un service qui calcule un score de fraude n'a aucune raison d'accéder aux données personnelles d'un client. Un service de reporting n'a aucune raison de modifier une transaction. Sans RBAC, chaque composant pourrait potentiellement accéder à tout — et c'est exactement le type de situation qui transforme une faille mineure en incident majeur.

### Comment ça fonctionne en pratique ?

**Définition des rôles**

On identifie les grandes fonctions du système : lecture des scores, écriture des décisions, accès au reporting, administration. Chaque fonction devient un rôle.

**Attribution des permissions**

Chaque rôle est associé à un ensemble de permissions précises : lire, écrire, supprimer, sur quel composant, sur quelle table ou collection.

**Association des services**

Chaque service ou utilisateur est associé à un ou plusieurs rôles. Il ne peut faire que ce que ses rôles autorisent.

**Principe de moindre privilège**

C'est le principe fondateur du RBAC. Chaque entité reçoit uniquement les permissions minimales nécessaires à son fonctionnement. Jamais plus.

Dans le contexte de Stripe, ça veut dire par exemple qu'un service autorisé à lire `fraud_score` dans MongoDB ne peut pas lire `ml_features`, ne peut pas écrire dans PostgreSQL, et ne peut pas accéder à Snowflake. Les périmètres sont hermétiques.

## **Audit & Traçabilité**

L'audit est le mécanisme qui enregistre chaque action sensible effectuée sur le système. La traçabilité est la capacité à suivre le chemin d'une donnée depuis sa source jusqu'à sa destination.

Dans un système normal, on n'a pas besoin de savoir en détail qui a fait quoi. Mais dans un système qui traite des données financières, chaque action peut avoir des conséquences réglementaires et légales.

### Comment ça fonctionne en pratique ?

**L'audit trail**

Chaque opération sensible est loguée : qui a accédé à quoi, quand, depuis quelle adresse, avec quel résultat. Ces logs sont stockés séparément des données de production, pour éviter qu'ils soient falsifiés en cas d'incident.

**La traçabilité du lignage**

Dans l'architecture de Stripe, chaque donnée a un chemin tracé : elle part de PostgreSQL, passe par Kafka, est transformée par Spark, et arrive dans MongoDB ou Snowflake. Le lignage permet de savoir à tout moment où se trouve une donnée, d'où elle provient, et quelles transformations elle a subi.

## Protection des données banquaires (**PCI-DSS)**

PCI-DSS (Payment Card Industry Data Security Standard) est la norme de sécurité internationale applicable à toute entité qui traite, stocke, ou transmet des données de carte bancaire.

Elle existe pour une raison simple : les données de carte bancaire sont l'une des catégories de données les plus convoitées par les acteurs malveillants. PCI-DSS impose un niveau de protection minimum pour limiter ce risque à l'échelle industrielle.

### Ce qu'elle impose en pratique ?

La norme est découpée en 12 exigences principales. Les plus critiques dans le contexte de Stripe sont :

**Chiffrement des données de carte**

Aucune donnée de carte ne peut circuler en clair dans le système que ce soit au repos ou en transit.

**Segmentation réseau**

Les systèmes qui traitent les données de carte doivent être isolés du reste du réseau. Un compromis sur un composant périphérique ne doit pas permettre d'atteindre les données sensibles.

**Contrôle d'accès strict**

Seules les personnes et les systèmes nécessaires peuvent accéder aux données de carte. Le principe de moindre privilège est une exigence fondamentale.

**Audit continu**

Chaque accès aux données de carte doit être loguée et monitoré.

**Tests réguliers**

Des tests de pénétration et des scans de vulnérabilités sont obligatoires à intervalles réguliers pour vérifier la solidité du système.

## Segmentation réseau

La segmentation réseau est le fait de découper le réseau en zones isolées, où chaque zone ne peut communiquer qu'avec les zones autorisées.

Dans une architecture sans segmentation, si un composant est compromis, l'attaquant peut potentiellement se déplacer latéralement vers tous les autres composants du système. Avec de la segmentation, chaque composant est dans sa propre zone. Une compromise reste cantonnée.

### Comment ça fonctionne en pratique ?

**Zones de protection**

Les composants sont regroupés selon leur niveau de sensibilité. Les données de carte bancaire sont dans une zone hautement protégée. Le reporting est dans une zone moins restrictive. Les deux zones ne communiquent pas directement.

**Firewalls entre les zones**

Chaque communication entre deux zones passe par un firewall qui vérifie si cette communication est autorisée. Si ce n'est pas le cas, elle est bloquée.

**Dans le contexte de l'architecture**

PostgreSQL ,qui contient les données transactionnelles sensibles, ne doit être accessible que par les services qui en ont besoin (CDC, boucle de retour). Snowflake, Kafka, les stores NoSQL , chacun dans sa propre zone, avec des chemins de communication explicitement définis.

## **Monitoring en temps réel des anomalies d'accès**

C'est le système qui surveille en permanence les comportements d'accès sur l'architecture, et qui alerte immédiatement dès qu'un comportement inhabituel est détecté.

### Comment ça fonctionne en pratique ?

**Établissement d'un comportement normal**

Le système apprend d'abord ce qui est "normal" : quel service accède à quoi, à quelle fréquence, depuis où. Cette baseline devient la référence.

**Détection des écarts**

Dès qu'un comportement s'écarte de cette baseline, une alerte est levée. Par exemple :

- Un service qui soudainement accède à une collection hors de son périmètre
- Un volume de requêtes inhabituellement élevé sur une table sensible
- Un accès depuis une adresse IP inconnue
- Une tentative d'accès en dehors des horaires habituels

**Alertes et réponse**

Les anomalies détectées sont classées par niveau de sévérité. Les alertes critiques déclenchent une réponse immédiate — isolation du composant concerné, revocation des accès, notification de l'équipe de sécurité.

# Les normes de conformité

## La conformité RPGD

Le RGPD (Règlement Général sur la Protection des Données) est le cadre réglementaire européen qui régit la collecte, le stockage, et l'utilisation des données personnelles.
Il s'applique à toute entreprise qui traite des données de personnes situées en Europe — peu importe où l'entreprise est basée.

Il protège les individus. Il leur garantit qu'ils savent comment leurs données sont utilisées, et leur donne des droits sur ces données.

### Ce qu'il impose en pratique ?

**Droit à l'oubli**

Un utilisateur peut demander la suppression de ses données personnelles. Le système doit être capable de les identifier et de les supprimer sans casser l'architecture — ce qui impose une bonne traçabilité du lignage.

**Minimisation des données**

On ne collecte que ce qui est strictement nécessaire. Pas de données superflues stockées "au cas où".

**Consentement explicite**

L'utilisateur doit avoir donné son accord avant que ses données ne soient utilisées à des fins spécifiques.

**Traçabilité des traitements**

On doit être capable de montrer comment les données sont utilisées, par quels composants, et pourquoi. C'est directement lié au lignage présent dans l'architecture.

**Notification en cas de fuite**

Si une fuite de données personnelles est détectée, les personnes concernées et les autorités compétentes doivent être informées dans un délai défini.

## SOC 2

SOC 2 (Service Organization Controls 2) est un standard d'assurance qualité qui évalue la sécurité, la disponibilité, et la confidentialité d'un système de traitement des données.

Ce n'est pas une réglementation imposée par la loi. C'est une certification qu'une entreprise demande volontairement pour prouver à ses clients que son système est digne de confiance.

Stripe traite les données de ses clients (entreprises, plateformes e-commerce, applications). Ces clients ont besoin d'être sûrs que leur argent et leurs données sont entre de bonnes mains.
SOC 2 répond à cette question de manière objective. Ce n'est pas Stripe qui dit "nous sommes sécurisés", c'est un auditeur externe qui le vérifie et qui le certifie.

### Ce qu'elle évalue en pratique ?

La certification SOC 2 évalue cinq principes fondamentaux :

**Sécurité**

Le système est protégé contre les accès non autorisés. Chiffrement, contrôle d'accès, monitoring, tout est vérifié.

**Disponibilité**

Le système fonctionne de manière fiable. Les temps de pannes sont définis et respectés.

**Confidentialité**

Les données confidentielles sont protégées selon les engagements pris avec les clients.

**Intégrité du traitement**

Les données sont traitées de manière complète, précise, et dans les délais définis.

**Vie privée**

Les données personnelles sont collectées, utilisées, et conservées conformément à la politique de vie privée.

# Plan détaillé

### PostgreSQL (OLTP — Source de vérité)

C'est le composant le plus critique de l'architecture. Il contient les données transactionnelles brutes et reçoit les décisions finales via la boucle de retour.

**Chiffrement au repos** — AES-256 activé sur l'ensemble des tables. Les données de carte et les décisions BLOCKED/APPROVED sont chiffrées dès l'écriture.

**Chiffrement en transit** — TLS obligatoire sur toutes les connexions entrantes et sortantes. Aucune connexion non chiffrée n'est acceptée.

**Contrôle d'accès** — Deux rôles uniquement : lecture par le CDC, écriture par la boucle de retour (décision ML). Aucun autre service n'a accès.

**Segmentation réseau** — Placé dans une zone hautement isolée. Aucune communication directe avec Snowflake, Looker, ou les stores NoSQL.

**Audit** — Chaque requête en lecture et en écriture est loguée avec timestamp, source, et résultat.

**Rotation des clés** — Tous les 90 jours via le KMS.

### Apache Kafka (Streaming)

Point de transit central. Toutes les données de PostgreSQL y passent avant d'être consommées.

**Chiffrement au repos** — Les messages stockés dans les partitions sont chiffrés avec AES-256.

**Chiffrement en transit** — TLS obligatoire entre le producteur (CDC) et les consommateurs (Spark, MongoDB, Cassandra).

**Contrôle d'accès** — Le CDC a le droit de produire. Spark, MongoDB, et Cassandra ont le droit de consommer sur des topics spécifiques uniquement. Aucun accès croisé entre topics.

**Segmentation réseau** — Zone isolée. Ne communique qu'avec le CDC en entrée, et Spark/NoSQL en sortie.

**Monitoring** — Alerte si le volume de messages par partition dépasse 2x le volume moyen sur les 7 derniers jours.

### Apache Spark (Transformation)

Consomme les données depuis Kafka, les transforme, et les pousse vers Snowflake et les stores NoSQL.

**Chiffrement en transit** — TLS obligatoire sur toutes les connexions vers Kafka, Snowflake, MongoDB, et Cassandra.

**Contrôle d'accès** — Rôle "transformation uniquement". Lecture sur Kafka, écriture sur Snowflake et NoSQL. Aucun accès en lecture sur PostgreSQL ou sur les données brutes non transformées.

**Segmentation réseau** — Zone de traitement isolée. Ne communique jamais directement avec PostgreSQL ou Looker.

**Audit** — Chaque job de transformation est loguée avec les données en entrée, en sortie, et la durée d'exécution.

### Apache Airflow (Orchestration)

Contrôle l'exécution de tous les workflows de transformation.

**Contrôle d'accès** — Rôle "orchestration uniquement". Déclenche les jobs Spark, ne lit jamais les données directement.

**Audit** — Chaque workflow déclenché est loguée avec statut, durée, et résultat. En cas d'échec, une alerte est levée automatiquement.

**Monitoring** — Alerte si un workflow prend plus de 2x le temps moyen habituel, ou si un job échoue deux fois consécutivement.

### Snowflake (OLAP — Datawarehouse)

Stocke les données transformées pour l'analyse et le ML.

**Chiffrement au repos** — AES-256 sur toutes les tables. Les données personnelles et financières sont identifiées et taguées via la classification automatique.

**Chiffrement en transit** — TLS obligatoire sur toutes les connexions entrantes (Spark) et sortantes (Looker, ML).

**Contrôle d'accès** — Trois rôles distincts : écriture par Spark uniquement, lecture par Looker sur les tables de reporting, lecture par le pipeline ML sur les tables features. Aucun accès croisé entre ces trois périmètres.

**Segmentation réseau** — Zone analytique isolée. Ne communique jamais avec PostgreSQL directement.

**Audit** — Chaque requête est loguée avec l'identité du service appelant, les tables accessées, et le volume de données retourné.

**Rotation des clés** — Tous les 90 jours via le KMS.

### MongoDB (NoSQL — Scores & Features)

Stocke les scores de fraude et les features du modèle. Accès à faible latence pour la boucle de retour.

**Chiffrement au repos** — AES-256 activé indépendamment sur chaque collection.

**Chiffrement en transit** — TLS obligatoire sur toutes les connexions.

**Contrôle d'accès par collection** — Aucun service n'a accès aux deux collections simultanément

**Segmentation réseau** — Zone NoSQL isolée. Ne communique qu'avec Spark en entrée et le service de décision en sortie.

**Monitoring** — Alerte si un service accède à une collection hors de son périmètre défini, ou si le volume de requêtes dépasse 3x la moyenne habituelle.

**Rotation des clés** — Tous les 90 jours, indépendamment par collection.

### Cassandra (NoSQL — Données historiques)

Stocke les données historiques volumineuses pour les patterns temporels.

**Chiffrement au repos** — AES-256 activé sur l'ensemble des keyspaces.

**Chiffrement en transit** — TLS obligatoire entre Kafka et Cassandra.

**Contrôle d'accès** — Rôle "écriture historique" pour Kafka, rôle "lecture historique" pour Spark. Aucun autre accès autorisé.

**Segmentation réseau** — Même zone que MongoDB, mais sans communication directe entre les deux stores.

**Rotation des clés** — Tous les 90 jours via le KMS.

### Looker (Reporting & Dashboards)

Point d'exposition vers les utilisateurs internes. Ne doit jamais avoir accès aux données brutes sensibles.

**Chiffrement en transit** — TLS obligatoire entre Looker et Snowflake, et entre Looker et les utilisateurs finaux.

**Contrôle d'accès** — Lecture uniquement sur les tables de reporting dans Snowflake. Aucun accès sur PostgreSQL, Kafka, ou les stores NoSQL.

**Segmentation réseau** — Zone reporting isolée. Accès sortant vers les utilisateurs uniquement via HTTPS.

**Audit** — Chaque dashboard consulté est loguée avec l'identité de l'utilisateur et les données affichées.

### Pipeline Machine Learning

Génère les scores de fraude et les décisions en production.

**Chiffrement en transit** — TLS obligatoire entre le pipeline ML, Snowflake, et MongoDB.

**Contrôle d'accès** — Lecture sur les tables features dans Snowflake.

**Validation avant déploiement** — Aucun modèle n'est déployé en production sans validation préalable sur ses métriques de performance via MLflow.

**Monitoring** — Alerte si le taux de faux positifs dépasse 5%, ou si la performance du modèle dérive de plus de 10% par rapport à la baseline établie lors du déploiement.

### MLflow (Suivi des modèles)

Contrôle le cycle de vie de tous les modèles en production.

**Contrôle d'accès** — Seule l'équipe ML a le droit de valider et de déployer un modèle. Le monitoring est en lecture pour l'équipe de sécurité.

**Versioning** — Chaque modèle est versionné avant déploiement. Un rollback vers une version précédente validée est possible en quelques minutes.

**Audit** — Chaque déploiement, rollback, et changement de configuration est loguée avec l'identité de la personne responsable.

### Plan de réponse à incident

| Niveau d'alerte | Exemple | Réponse | Délai |
| --- | --- | --- | --- |
| Critique | Accès non autorisé sur PostgreSQL | Isolation immédiate du composant, revocation des accès, notification équipe sécurité | < 5 minutes |
| Élevé | Anomalie de volume sur Kafka | Alerte équipe sécurité, investigation, isolation si confirmé | < 15 minutes |
| Moyen | Dérive de performance du modèle ML | Alerte équipe ML, évaluation, rollback si nécessaire | < 1 heure |
| Faible | Tentative d'accès bloquée par RBAC | Log enregistré, revue quotidienne | 24 heures |

### Fréquences de maintenance sécurité

| Action | Fréquence |
| --- | --- |
| Rotation des clés de chiffrement | Tous les 90 jours |
| Tests de pénétration | Tous les 3 mois |
| Scans de vulnérabilités | Hebdomadaire |
| Revue des permissions RBAC | Mensuelle |
| Audit des logs | Quotidien |
| Validation des modèles ML | À chaque déploiement |

# Conclusion

La sécurité n'est pas une couche qu'on ajoute à une architecture une fois qu'elle est construite. C'est une décision de conception qui se prend dès le début, et qui influence chaque choix technologique qui suit.Dans le cas de cette architecture, chaque brique a été choisie non seulement pour sa performance, mais pour sa capacité à s'intégrer dans un environnement sécurisé. 

Le chiffrement, le contrôle d'accès, l'audit, la segmentation, le monitoring, aucun de ces éléments n'est isolé. Ils fonctionnent ensemble, en layers, pour créer un système où chaque niveau de protection renforce les suivants.

## Exemples concrets d'application

### Une transaction frauduleuse arrive via Stripe.

Elle est persistée dans PostgreSQL, chiffrée au repos immédiatement. Le CDC la détecte et la pousse vers Kafka via une connexion TLS chiffrée en transit. Kafka la stocke dans une partition isolée par segmentation réseau. Spark la consomme, la transforme, et l'envoie vers le modèle ML. Le modèle émet un score élevé de fraude. La décision **BLOCKED** est écrite dans PostgreSQL. L'application la lit et bloque la transaction. À aucun moment, la donnée n'a circulé en clair. À aucun moment, un composant non autorisé n'a pu y accéder.

### **Un service tente d'accéder à une collection hors de son périmètre.**

Un service autorisé à lire `fraud_score` dans MongoDB essaie d'accéder à `ml_features`. Le RBAC bloque la requête immédiatement. Le monitoring en temps réel détecte l'anomalie en quelques secondes et lève une alerte. L'équipe de sécurité est notifiée. Le service concerné est isolé pour investigation. La tentative n'a jamais pu aboutir.

### **Une clé de chiffrement approche de sa date de rotation.**

Le KMS génère automatiquement une nouvelle clé. Les données stockées dans PostgreSQL, MongoDB, et Cassandra sont progressivement re-chiffrées avec la nouvelle clé. L'ancienne clé est désactivée une fois le processus terminé. Aucun service n'est interrompu. Aucune intervention manuelle n'est nécessaire. La protection reste intacte en permanence.

### **Une tentative d'intrusion survient sur un composant périphérique.**

Un attaquant comprime un service de reporting connecté à Snowflake. La segmentation réseau empêche tout mouvement latéral vers PostgreSQL, Kafka, ou les stores NoSQL. Le monitoring détecte immédiatement un comportement anormal — des requêtes inhabituelle depuis le service compromis. Le composant est isolé automatiquement. Les données sensibles n'ont jamais été exposées.