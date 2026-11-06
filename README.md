# EBV VTOM en direct

Visualiseur autonome d'une Expression de Besoin VTOM (`.xlsm`) : applications et étapes (jobs) de la
journée, avec l'heure courante.

## Utilisation

1. Ouvrir `index.html` dans un navigateur (double-clic suffit, aucun serveur requis ; la bibliothèque
   SheetJS est chargée depuis cdnjs, donc une connexion réseau est nécessaire au premier affichage).
2. Charger l'EBV (bouton ou glisser-déposer). Le classeur est lu dans le navigateur, rien n'est envoyé.
3. Onglet **Vue du jour** : frise 24 h, applications déjà lancées / en fenêtre / à venir, pas prévues
   aujourd'hui, à confirmer. Un onglet par application est créé automatiquement.
4. Dans un onglet application : plage de lancement, planification, cyclicité, prédécesseurs/successeurs,
   chaîne des étapes (rectangles reliés dans l'ordre prédécesseur → successeur). Cliquer une étape ouvre
   le détail (script, paramètres, utilisateur, machine, liens).

Options : date de référence et heure simulée (pour rejouer une autre journée), inclusion des lignes en
`Suppression`, recherche. Le dernier classeur chargé est mémorisé dans le navigateur (localStorage).

## Version hors ligne (poste sans Internet)

`dist/ebv-vtom-en-direct-hors-ligne.html` est la même application en un seul fichier, avec la
bibliothèque SheetJS et les polices intégrées : elle ne fait aucune requête réseau. C'est ce fichier
qu'il faut transmettre aux postes dont l'accès Internet est bloqué ; un double-clic suffit.

Après toute modification de `index.html`, régénérer le fichier :

```bash
python3 build-offline.py
```

Le script échoue s'il reste une ressource externe dans la page. Les dépendances embarquées sont dans
`vendor/` (origine, empreinte et licences dans `vendor/README.md`).

## Ce qui est lu

- Onglet `APP` : APPLICATION, Commentaire, Prédécesseur/Successeur, Heure début / max lancement,
  Planification, Cyclique, Durée du cycle, GO externe/manuel, environnements, action/version EBV.
- Onglet `JOB` : JOB, APPLICATION, Commentaire, Prédécesseur/Successeur, type de traitement, script,
  paramètres, heure/planification propres (rares).
- Onglet `Histo` : titre, projet.

Les colonnes sont repérées par leur libellé d'en-tête (repli sur la position si le libellé change).

## Limites

- Aucune durée n'étant renseignée dans l'EBV (`Durée Max` vide), une étape ne peut pas être dite
  « terminée » : le statut d'une étape est celui de la fenêtre de lancement de son application.
- Planifications interprétées : tous les jours, tous les `<jour>`, N-ième `<jour>` du mois (dernier
  compris), N-ième semaine du mois, avec plage de mois. Les autres textes sont marqués « à confirmer ».
  Les jours fériés ne sont pas pris en compte.
