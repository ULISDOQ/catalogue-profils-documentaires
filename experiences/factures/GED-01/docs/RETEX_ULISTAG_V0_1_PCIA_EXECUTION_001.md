# RETEX — ULISTAG v0.1 sur source réelle PCIA

**Référence : GED01_ULISTAG_V0_1_PCIA_EXECUTION_001**  
**Statut : PASS_CANDIDATE — NON QUALIFIÉ**  
**Autorité : Jean**  
**Méthode : CLAU_METHODE_V2_BETA_5**  
**Source d'exécution : CLAU/GED-RÉEL**

## Résultat

Le candidat ULISTAG v0.1 a été exécuté sur PCIA contre la facture SFR privée ayant servi à la conception.

```text
MATCH_RESULT=MATCH_CANDIDATE
PAGE_COUNT_OBSERVED=2
NODE_RATIO=1.0
EDGE_RATIO=1.0
MISSING_OR_FAILED_NODES=NONE
FAILED_EDGES=NONE

EXTRACTION_RESULT=EXTRACTED_UNVERIFIED
invoice_number=EXTRACTED
date=EXTRACTED
amount=EXTRACTED
```

Aucune valeur privée n'a été retournée à ULISDOQ.

## Environnement

```text
PYTHON=3.12.3
PDFPLUMBER=0.11.10
SOURCE_MUTATED=NO
REFERENCE_INTEGRITY=PASS
QUALIFICATION=NONE
```

Les références ULISDOQ ont été utilisées via des commits individuels épinglés.

## Intégrité du passage

```text
NAVETTE_PUBLICATION_COMMIT=
0d2a51f40457e4d8bcb086c789841b3012f2bd84

NAVETTE_RETURN_COMMIT=
a0078780497ac0424aa95848b6f317f4c33d52b5

NAVETTE_CLEANUP=COMPLETE
```

## Interprétation

Ce résultat démontre uniquement que :

- le candidat ULISTAG v0.1 reconnaît la **source ayant participé à sa conception** ;
- les dix ancres et les huit relations du graphe candidat satisfont le règlement v0.1 sur cette source ;
- le profil structurel associé parvient à extraire les trois champs attendus au niveau technique ;
- le chemin local `document → empreinte → candidat → profil → extraction` est exécutable sur PCIA.

Ce résultat **ne démontre pas** :

- que les valeurs extraites sont correctes ;
- que le candidat reconnaît un autre document du même modèle ;
- qu'il tolère correctement des variantes ;
- qu'il rejette correctement les modèles voisins ;
- qu'il est qualifié ;
- qu'un taux de reconnaissance peut être généralisé.

Le statut reste donc :

```text
PASS_CANDIDATE
QUALIFICATION=NONE
```

## Conséquence sur la roadmap

La première épreuve réelle R5 est passée. Elle ne remplace pas les étapes de discrimination et de généralisation.

La prochaine étape est :

```text
A synthétique — même structure, valeurs A
B synthétique — même structure, valeurs B
N négatif     — structure différente

→ fabriquer les observations selon le même règlement
→ vérifier A≈B
→ vérifier séparation de N
→ contrôler que les valeurs variables n'affectent pas l'identité
→ documenter précisément la signification de node_ratio et edge_ratio
```

Cette étape doit être réalisée sans utiliser la facture privée comme objet publié.

Ensuite seulement viendra un petit corpus indépendant pour commencer à mesurer faux rapprochements et faux rejets.
