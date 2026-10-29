# ULISDOQ — Unification des briques techniques documentaires

**Référence : UNIFICATION-TECH-001**  
**Statut : architecture conceptuelle ; registre de capacités non encore opérationnel**

## Rôle

ULISDOQ est un **unificateur libre** : il référence, met en correspondance, versionne et qualifie les ressources documentaires et les capacités techniques. Il ne présuppose **aucun moteur unique** et n'exécute pas obligatoirement lui-même les traitements.

Le référentiel sépare :
- **Famille / format / TAG** : ce qu'est le document et comment le reconnaître.
- **Profil documentaire** : quelles données et règles sont attendues.
- **Capacité requise** : lecture PDF, OCR, reconnaissance, extraction de facture, lecture de formulaire, validation, etc.
- **Brique technique** : logiciel externe fournissant une ou plusieurs capacités avec version, licence, interfaces et limites.
- **Adaptateur** : correspondance entre contrat canonique ULISDOQ et interface concrète de la brique.
- **Preuve** : résultats de tests et périmètre dans lequel la combinaison profil/brique est qualifiée.

```text
Document local → TAG / format → profil documentaire
                                     │
                                     ▼
                             capacités requises
                                     │
                              registre ULISDOQ
                                     │
                        ┌────────────┼────────────┐
                        ▼            ▼            ▼
                    brique A     brique B     brique N
                        │            │            │
                        └────────────┼────────────┘
                                     ▼
                         adaptateur + exécution locale
                                     │
                                     ▼
                           résultat normalisé + contrôles
```

## Contrat candidat d'une fiche de brique

`component_id` opaque, nom et source officielle (dans la fiche technique uniquement), versions compatibles, licence, fonctions exposées, formats acceptés, dépendances, interface, contraintes de confidentialité, adaptateurs disponibles, preuves de tests, statut et date de revue.

Une brique peut être référencée sans être qualifiée. Un profil peut admettre plusieurs briques compatibles. La qualification porte sur un **couple profil / brique / version / environnement**, et non sur la seule réputation du logiciel.

## Première brique expérimentale

Le moteur **invoice2data** est utilisé dans **GED-01**, comme **une brique parmi N** pour l'extraction de factures. Son utilisation ne définit ni l'architecture globale, ni les autres familles documentaires, ni le choix du moteur pour le formulaire 2044 de GED-02. L'intégration expérimentale est non qualifiée à ce stade.

## Gouvernance des références

Réemployer les outils existants, citer leurs sources et respecter leurs licences ; ne pas supposer de partenariat ou de validation officielle. Les documents privés sont traités localement. La sélection et les mises à jour de briques sont explicites et versionnées ; l'absence de compatibilité ou de preuve donne lieu à un refus ou à une qualification à conduire.

## État de réalisation

Architecture documentée ; pas de registre exécutable de N briques, pas de sélection automatique, pas de qualification transversale prouvée.
