# Contribuer au ROTK Wiki (non officiel)

Wiki communautaire FR/EN (et chinois) d'aide aux joueurs de ROTK (H1Z1). **Il n'est pas affilié à ROTK** et doit le rester visiblement : le bandeau « non officiel » reste, et aucune page ne doit imiter un outil ou une page du staff.

Site en ligne : https://warlinee.github.io/h1-guide/ (GitHub Pages, branche `main`, racine du dépôt). Chaque push sur `main` est en ligne en environ 1 minute.

## Comment travailler

1. Crée une branche (`git checkout -b ma-modif`) : on ne pousse jamais directement sur `main`.
2. Teste en local (voir plus bas).
3. Ouvre une Pull Request vers `main` avec une courte description et une capture. Warline relit avant la mise en ligne.

## Structure

Tout le site tient dans **`index.html`** (HTML, CSS et JS, sans build ni dépendance externe : le lecteur de captures utilise une copie de Tesseract.js rangée dans le dossier `vendor/tesseract/`, pas de CDN). La version chinoise est à part, dans `zh.js`, chargé seulement en chinois :

| Élément | Où |
|---|---|
| Textes de l'interface FR/EN | objet `UI` (`UI.fr`, `UI.en`) |
| Version chinoise (bouton 中文, `?lang=zh`) | `zh.js` : chaque texte anglais avec sa traduction. Dans `index.html` : `ZH_ROOTS` et `zhApply()` (textes), `zhTokens()` (recherche en chinois) |
| Catégories (accès rapide et onglets) | tableau `CATS` (+ icônes `icons/cat-<id>.webp`) |
| Fiches problème / solution | tableau `F` |
| « Avant de demander » | `RULES` |
| Liens utiles | `LINKS` |
| Recherche (sans accents, synonymes, fautes de frappe, classement) | `norm`, `STOP`, `SYN`, `queryTokens`, `nearWord` (fautes de frappe), `scoreRow`, `rankRows` (classement commun à la barre, à la fenêtre de recherche et à Réponses rapides), `searchLines`, `filter()` |
| Liens directs vers une fiche | `#slug` du titre FR, voir `slugOf()` et `openCard()` |
| Aperçus Discord des liens de fiche | pages `c/<slug>.html`, `c/<slug>.en.html` et `c/<slug>.zh.html`, générées par `tools/build_card_pages.py` ; `404.html` renvoie vers la fiche si une page manque |
| Réponses rapides pour le support (`?support`) | champ `m` de chaque fiche + `SUP_GENERAL` : pas de lien depuis la page publique, `noindex` |
| Lecteur de captures (OCR dans le navigateur) | `ocrRun()`, `prepImage()`, `ocrMatch()` + les fichiers de `vendor/tesseract/` : pour les mettre à jour, suis `vendor/tesseract/README.md` |
| Patch notes (bouton dans la barre, `#patch-notes`) | tableau `PATCH_NOTES`, version la plus récente en premier : **ajoute une ligne à chaque changement visible**. `c` facultatif : slug de la fiche concernée, pour le lien « Voir la fiche » |

### Format d'une fiche (`F`)

```js
{c:"launcher", s:"ok", k:["mot-clé","code d'erreur"], v:"nomvideo",
 t:{fr:"Titre FR", en:"EN title"},
 f:{fr:["Étape 1", "Étape 2"], en:["Step 1", "Step 2"]},
 n:{fr:"Note facultative", en:"Optional note"}}
```

- `c` : id de catégorie (`CATS`).
- `s` : statut. `ok` = confirmé chez des joueurs, `lead` = piste, `known` = bug connu sans correctif.
- `k` : mots-clés et codes (servent à la recherche et aux étiquettes).
- `r` : facultatif. Slugs des fiches citées dans le texte (« fiche Windows Defender »), affichées en boutons « Voir aussi » à la fin de la fiche.
- `v` : facultatif. Vidéo `videos/<v>-fr.mp4` / `-en.mp4` + affiche `.jpg`.
- Toujours remplir **FR et EN**.
- Le chinois ne se remplit pas ici : il est dans `zh.js`, tenu par Wazlyy. Quand tu changes le texte anglais d'une fiche, ce texte repasse tout seul en anglais dans la version chinoise en attendant sa traduction : tu n'as rien à faire de plus.

Après avoir ajouté, renommé ou modifié une fiche, régénère les aperçus Discord :

```bash
python tools/build_card_pages.py
```

Il faut Playwright (`pip install playwright`) et Microsoft Edge ou Chromium. Sans ça, le lien de la fiche marche quand même, seul l'aperçu sur Discord reste générique.

Les vidéos sont fabriquées hors du dépôt. Seuls les `.mp4` et `.jpg` finaux sont publiés : les sources (`videos/*.html`, `videos/src/`) restent locales et sont dans `.gitignore`.

## Règles pour un outil de debug (ou tout ajout interactif)

- **100 % côté navigateur.** Un fichier ou un texte collé par le joueur est analysé localement et **n'est jamais envoyé** nulle part : pas de `fetch` vers un serveur, pas d'analytics, pas de webhook.
- Les logs contiennent souvent des **noms de PC, des chemins avec le nom d'utilisateur, des identifiants et parfois des tickets de connexion**. Rien ne doit être stocké (pas de `localStorage` pour ces données), et un éventuel rapport à copier doit **masquer** ces informations avant affichage.
- **Aucune clé, aucun token, aucun secret** dans le dépôt : le site est public.
- Rester **en FR et en EN**, accessible au clavier, lisible sur mobile.
- Ne jamais donner de commande pour contourner l'anticheat, ni de raccourci console.

## Tester avant la PR

```bash
python -m http.server 8765
```

Puis ouvre http://127.0.0.1:8765/ et vérifie :

- la version FR et la version EN (`?lang=fr`, `?lang=en`), et la version chinoise (`?lang=zh`) ;
- un écran de 375 px de large (rien ne déborde sur le côté) ;
- la console sans erreur ;
- quelques recherches (« ecran noir », « pas de son », « crash ») ;
- un lien direct (`#chutes-de-fps-ou-saccades-en-combat`) ;
- le lecteur de captures (colle une capture d'erreur) : il ne marche qu'avec ce serveur local, pas en ouvrant le fichier `index.html` directement.
