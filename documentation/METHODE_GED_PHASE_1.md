# Méthode GED-N — Phase 1

**Référence : ULISTAG-PHASE1-GED-METHOD-001**  
**Statut : méthode expérimentale de production répétable**

## But

Construire rapidement des cas GED-N comparables afin d'explorer environ 70 types, formats et fournisseurs documentaires.

La phase 1 vise la **production d'expérience et l'accumulation de matière empirique**. Elle ne vise pas à produire, pour chaque cas, un TAG définitif ni à qualifier complètement ULISTAG.

## Chaîne minimale

```text
1. APPROVISIONNER
   quelques positifs représentatifs
   + si possible un négatif proche

2. CARACTÉRISER
   format physique / pages / texte / image / layout
   sans chercher à tout comprendre

3. CHERCHER LE RÉEMPLOI
   méthode ULISTAG existante
   matcher existant
   primitives existantes

4. CONSTRUIRE UN TAG CANDIDAT MINIMAL
   suffisamment discriminant pour le cas
   pas nécessairement optimal

5. ÉPROUVER
   positifs → doivent converger
   négatif proche → doit être rejeté
   produire des mesures explicables

6. LIER
   TAG candidat
   → profil documentaire candidat
   → méthode d'extraction éventuelle

7. CAPITALISER
   résultat
   limites
   méthode utilisée
   nouveauté éventuelle
   dette observée

8. PASSER AU GED SUIVANT
```

## Critère de réussite de phase 1

> Disposer d'une méthode suffisamment fiable et explicable pour reconnaître le type documentaire dans le corpus expérimental et produire, si utile, un profil candidat réutilisable.

Ce critère ne signifie pas que le TAG est optimal, qualifié pour la production ou généralisable hors du corpus observé.

## Contrat minimal d'un GED-N

Chaque cas conserve au minimum :

- identifiant GED ;
- besoin documentaire ;
- caractérisation technique ;
- corpus positif disponible ;
- négatif proche si disponible ;
- méthode tentée ou réutilisée ;
- paramètres candidats ;
- résultats minimisés ;
- limites observées ;
- dette éventuelle ;
- décision : réemploi / nouveau candidat / unsupported / no-further-value-now.

## Produit collectif de la phase 1

Les ~70 cas doivent permettre de constituer une matrice empirique :

```text
cas
× primitives utiles
× matcher employé
× coût
× robustesse observée
× faux rapprochements
× faux rejets
× limites
× famille documentaire
```

Cette matière devient l'entrée de la phase 2, consacrée à l'amélioration des méthodes ULISTAG, à leur regroupement, aux variantes indépendantes et à la qualification plus poussée.

## Règle de sobriété

La méthode doit réduire le coût du GED suivant. Une complexité qui n'améliore ni la discrimination du cas ni la réutilisabilité est différée.
