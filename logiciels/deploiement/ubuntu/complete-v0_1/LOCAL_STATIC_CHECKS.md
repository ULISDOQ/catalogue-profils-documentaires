# ULISDOQ Complete Ubuntu v0.1 — Contrôles statiques locaux

**Objet :** retour `ULISDOQ_COMPLETE_UBUNTU_PROFILE_TARGETED_REVIEW_001`.

Contrôles exécutés localement après correction, sans exécution PCIA et sans installation système :

```text
python3 -m py_compile verify_complete.py
RESULT=PASS

bash -n ulisdoq-deploy.sh
RESULT=PASS
```

Versions de contenu contrôlées :

- `ulisdoq-deploy.sh` : correction delta/rattachement/rollback, commit `32f2b798562e0992b6ad8ca918c7e3c79e59773c`.
- `verify_complete.py` : correction syntaxique + probes fonctionnelles, puis correction représentation montant, commit final `98eac408e92174314348baf831a2048e96ffd3f7`.

Ces contrôles prouvent uniquement la validité syntaxique Python/Bash du delta retourné. Ils ne remplacent pas :

- l'installation sur Ubuntu ;
- la résolution réelle des dépendances ;
- les probes fonctionnelles sur PCIA ;
- la qualification runtime du profil complet.

Aucune mutation PCIA n'a été réalisée pour ces contrôles.
