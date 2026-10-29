# Profile Builder — cycle de vie d'un profil candidat

**Référence :** PROFILE-BUILDER-CANDIDATE-LIFECYCLE-001
**Statut :** documentation normative candidate

## 1. Pourquoi plusieurs zones ?

Un profil documentaire peut être fabriqué à partir de documents réels et privés, puis devenir une contribution publique, puis éventuellement devenir un profil officiellement disponible dans ULISDOQ.

Ces trois états ne doivent jamais être confondus.

```text
PRIVATE WORKSPACE
      ↓
PUBLICATION / PRIVACY GATE
      ↓
QUARANTINE — CANDIDATE PENDING REVIEW
      ↓
PROJECT REVIEW
      ↓
PROMULGATION
      ↓
OPEN PROFILE STORE
```

## 2. Zone privée

La zone privée contient ce qui est nécessaire à la fabrication mais ne doit pas être publié automatiquement :

- documents sources réels ;
- valeurs observées ;
- sorties OCR brutes ;
- ground truth local ;
- logs locaux ;
- chemins locaux ;
- données personnelles ou confidentielles.

Le Profile Builder travaille ici sous autorité explicite du contributeur.

## 3. Gate de sortie privée

Le passage vers un objet publiable exige :

- export par allowlist ;
- absence de source brute ;
- absence de valeur observée ;
- absence de chemin local ;
- fixtures synthétiques uniquement ;
- scan de motifs à risque ;
- test canari de non-fuite ;
- revue humaine.

Un gate automatique réussi ne constitue pas une autorisation humaine de publication.

## 4. Quarantaine publique

Un profil qui a franchi la frontière privée n'est pas encore un profil ULISDOQ disponible.

Il entre dans une zone de quarantaine :

```text
CANDIDATE_SUBMITTED
PENDING_PROJECT_REVIEW
```

Cette zone peut être publique et examinable, mais elle est explicitement séparée de la zone des profils promulgués.

Le candidat peut y être :

- commenté ;
- testé ;
- challengé ;
- corrigé ;
- requalifié ;
- rejeté.

## 5. Revue contradictoire

La revue doit pouvoir questionner :

- la reconnaissance du type documentaire ;
- la robustesse de l'extraction ;
- les champs et leurs significations ;
- les règles de validation ;
- les dépendances ;
- les limites annoncées ;
- les preuves ;
- la confidentialité ;
- la reproductibilité ;
- la réutilisabilité.

Une anomalie ne doit pas être formulée comme une impression libre. Elle doit être reliée à une preuve.

## 6. Autorité et responsabilité

Le logiciel produit des résultats, des preuves et des gates.

Un reviewer — humain ou assisté — instruit les anomalies.

L'autorité de projet décide :

```text
ACCEPTED
CORRECTIONS_REQUIRED
REJECTED
```

Seul `ACCEPTED` peut conduire à la promulgation.

## 7. Promulgation

La promulgation est un acte distinct :

```text
PENDING_PROJECT_REVIEW
→ ACCEPTED
→ PUBLISHED
```

Le silo ouvert de consommation ULISDOQ ne contient que les profils `PUBLISHED`.

Un candidat présent sur Git n'est donc pas automatiquement disponible à l'usage.

## 8. Invariants

```text
PUBLIC_CANDIDATE != PUBLISHED_PROFILE
PRIVACY_PASS != QUALITY_PASS
AUTOMATIC_GATE_PASS != HUMAN_AUTHORIZATION
REVIEW_RESULT != PROMULGATION
```