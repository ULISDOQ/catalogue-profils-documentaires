# GED-02 — Classification locale d'un formulaire 2044

**Statut : candidat documentaire, non qualifié.** Ce cas vérifie que le catalogue peut décrire un document administratif sans dépendre d'un moteur de factures.

Le profil candidat est [profiles/fr_formulaire_2044_candidate.json](profiles/fr_formulaire_2044_candidate.json). Il retient une **famille de déclaration fiscale de revenus fonciers**, un numéro de formulaire déclaré et des indices textuels à vérifier sur un exemplaire officiel daté. Les versions annuelles, annexes et éventuelles variantes doivent être distinguées.

Le TAG peut être préparé localement avec l'[éditeur ULISDOQ](../../client/tag_candidate.py), puis comparé à un catalogue versionné. **Aucun document 2044 réel ni exemplaire officiel vérifié n'est fourni dans cette expérience** ; aucun résultat de reconnaissance n'est revendiqué.

## Critère de preuve

À partir d'un exemplaire local autorisé : relever sa version/millésime, générer un TAG candidat sans valeurs fiscales privées, identifier le profil exact ou retourner UNKNOWN, choisir un moteur compatible avec les formulaires et valider les champs sur un jeu d'essai indépendant. Une extraction de facture ne convient pas à ce cas.
