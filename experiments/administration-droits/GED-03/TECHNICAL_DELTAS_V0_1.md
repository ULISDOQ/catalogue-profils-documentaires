# GED-03 — Deltas techniques identifiés avant exécution

**Référence : GED03-TECHNICAL-DELTAS-001**  
**Statut : préparation uniquement**

## Aucun delta lourd attendu

Le cas ne requiert a priori ni OCR, ni rendu PDF, ni OpenCV, ni PyMuPDF, ni invoice2data, ni modèle appris.

## Delta D1 — adaptateur EML normalisé

**État : MISSING / SMALL**

Il manque un adaptateur ULISDOQ qui transforme un objet Python `email.message.EmailMessage` en contrat GED-03 normalisé.

Fonctions minimales :

- lecture locale ;
- parsing MIME ;
- décodage des en-têtes ;
- adresses structurées ;
- sélection du corps texte ;
- inventaire des pièces jointes sans exécution ;
- exposition des défauts de parsing ;
- JSON conforme au schéma ;
- SHA-256 et traceabilité.

Estimation : petit composant Python, sans dépendance externe initiale.

## Delta D2 — validation de conteneur

**État : MISSING / SMALL**

L'extension `.eml` ne suffit pas. Il faut définir le minimum structurel permettant de distinguer :

- message valide ;
- simple texte renommé ;
- MIME malformé ;
- message tronqué.

Ne pas inventer un détecteur complexe avant d'observer ce que fournit la bibliothèque standard, notamment ses défauts de parsing.

## Delta D3 — registre de profil

**État : ADAPTATION**

Si GED-03 produit un profil candidat, le registre actuel devra accepter un mode de reconnaissance `CONTAINER_NATIVE` ne dépendant pas d'un `format_tag_id` ULISTAG visuel.

Cette évolution doit rester générique et ne pas coder `.eml` dans le registre.

## Delta D4 — mesure GED-core

**État : CONTRACT_ONLY**

Il manque encore un objet commun permettant de mesurer le coût de fabrication d'un GED-N. GED-03 peut en fournir la première instance, mais il est prématuré d'automatiser l'orchestrateur.

## Dépendances

```text
NEW_EXTERNAL_PYTHON_DEPENDENCY_EXPECTED=0
SYSTEM_PACKAGE_EXPECTED=0
PCIA_DEPLOYMENT_REQUIRED_FOR_PREPARATION=NO
```
