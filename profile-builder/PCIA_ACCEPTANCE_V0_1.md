# Profile Builder 0.1.0 — acceptation PCIA

## Cible

Répertoire d'essai :

`/home/utilisateur/ULISDOQ/`

Aucune installation système, aucun déploiement de service et aucun accès réseau ne sont requis.

## Préflight

```bash
cd /home/utilisateur/ULISDOQ
python3 --version
sha256sum ulisdoq-profile-builder-0.1.0.tar.gz
```

SHA-256 attendu de l'archive distribuée dans la conversation :

`f82e610db48b8d894f702485ec0e7f9fc89599fd385105f19c1b75441fa7a66f`

## Exécution

```bash
tar -xzf ulisdoq-profile-builder-0.1.0.tar.gz
cd ulisdoq-profile-builder-0.1.0

./bin/profile-builder info
./bin/profile-builder selftest

./bin/profile-builder plan \
  --characterization examples/ged03/characterization.json \
  --need examples/ged03/requested_need.json \
  --output /tmp/ged03-plan.json

sha256sum /tmp/ged03-plan.json
cat /tmp/ged03-plan.json
```

## Gate

Attendu :

- `ged03_replay=PASS`
- `unknown_fail_closed=PASS`
- `overall=PASS`
- plan GED-03 stable ;
- aucun package Python externe ;
- aucune mutation système.

Après ce gate seulement, GED-04 peut être présenté comme entrée nouvelle au Builder.

Ne pas modifier le planner pour faire réussir GED-04 : `CAPABILITY_GAP` est une sortie valide.
