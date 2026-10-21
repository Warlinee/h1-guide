# Tesseract.js vendored

Le screenshot reader (`ocrRun()` dans `index.html`) fait l'OCR avec Tesseract.js. Ce folder en est une copie vendored, servie par le wiki lui-même : aucun CDN n'est appelé et le screenshot ne quitte pas le browser.

Ce sont exactement les files que tesseract.js 5.1.1 download par défaut sur le CDN jsDelivr, sans aucune modification. Chaque sha256 a été vérifié contre le package npm et contre jsDelivr.

| File | Version | Source | Taille (bytes) | sha256 |
|---|---|---|---|---|
| `tesseract.min.js` | tesseract.js 5.1.1 | https://cdn.jsdelivr.net/npm/tesseract.js@5.1.1/dist/tesseract.min.js | 66 695 | `a8e29918d098b2b06e1012bdaeffb4aec0445c5d5654709023e0bd1f442a80e8` |
| `tesseract.min.js.LICENSE.txt` | tesseract.js 5.1.1 | https://cdn.jsdelivr.net/npm/tesseract.js@5.1.1/dist/tesseract.min.js.LICENSE.txt | 149 | `cdf963ced7d25a0f98901a547647b4d6e2dbe0197fd78c87a059a87b0e542fe2` |
| `worker.min.js` | tesseract.js 5.1.1 | https://cdn.jsdelivr.net/npm/tesseract.js@5.1.1/dist/worker.min.js | 123 724 | `aca1229639fc9907d86f96e825955a2b7c5716d17f3bc3acd71f9c7ab66181fc` |
| `worker.min.js.LICENSE.txt` | tesseract.js 5.1.1 | https://cdn.jsdelivr.net/npm/tesseract.js@5.1.1/dist/worker.min.js.LICENSE.txt | 466 | `45f54171aeaa1d10c0c1a66f374b7bba1f02472b1487fbe892eec04f840002ac` |
| `tesseract-core-simd-lstm.wasm.js` | tesseract.js-core 5.1.1 | https://cdn.jsdelivr.net/npm/tesseract.js-core@5.1.1/tesseract-core-simd-lstm.wasm.js | 3 938 657 | `ce20eda9533cbed1e6c2b4276fbae1e0adc61b6754b5513084be601787b457cf` |
| `tesseract-core-lstm.wasm.js` | tesseract.js-core 5.1.1 | https://cdn.jsdelivr.net/npm/tesseract.js-core@5.1.1/tesseract-core-lstm.wasm.js | 3 938 277 | `8f04aa0cc81e7bde33f80e92fa01a7a665f0b4884d098acf5de9c7104a11dfaa` |
| `fra.traineddata.gz` | @tesseract.js-data/fra 1.0.0, modèle 4.0.0_best_int | https://cdn.jsdelivr.net/npm/@tesseract.js-data/fra@1.0.0/4.0.0_best_int/fra.traineddata.gz | 707 406 | `d611139672b3752c7097e671e4a1d9209dfd37f2aeb081ef6487fba3351e9255` |
| `eng.traineddata.gz` | @tesseract.js-data/eng 1.0.0, modèle 4.0.0_best_int | https://cdn.jsdelivr.net/npm/@tesseract.js-data/eng@1.0.0/4.0.0_best_int/eng.traineddata.gz | 2 952 873 | `45b4cb346724ac1774f1c36f42f182b887bcdb28ebe63e6fff90ac41f3fcff91` |
| `LICENSE-tesseract.js.md` | tesseract.js 5.1.1 | https://cdn.jsdelivr.net/npm/tesseract.js@5.1.1/LICENSE.md | 11 357 | `b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1` |
| `LICENSE-tesseract.js-core.txt` | tesseract.js-core 5.1.1 | https://cdn.jsdelivr.net/npm/tesseract.js-core@5.1.1/LICENSE | 11 358 | `c6596eb7be8581c18be736c846fb9173b69eccf6ef94c5135893ec56bd92ba08` |
| `LICENSE-tessdata.txt` | naptha/tessdata, commit 9c2fee3 | https://raw.githubusercontent.com/naptha/tessdata/9c2fee3df42e6cdc19ebc1e4fb05a5bafa48dab0/LICENSE | 11 357 | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |

## Ce que le browser charge

- `tesseract.min.js` : chargé par la page au premier usage du screenshot reader, pas avant.
- `worker.min.js` : le worker. Il tourne depuis une blob URL, c'est pour ça que `getWorker()` passe des paths absolus.
- Un seul des deux `tesseract-core-*-lstm.wasm.js` : le wasm SIMD si le browser le supporte, sinon l'autre. Avec `oem` 1 (LSTM seul), Tesseract.js ne peut choisir que ces deux-là. Les variantes sans `-lstm` ne servent qu'au moteur « legacy » et ne sont pas vendored.
- `fra.traineddata.gz` et `eng.traineddata.gz` : les traineddata restent en gzip. Le worker reconnaît le gzip à ses deux premiers bytes et le décompresse lui-même. Si un server les envoie avec `Content-Encoding: gzip`, le browser les décompresse avant et le worker les prend tels quels. Ensuite ils sont gardés en cache dans IndexedDB (ce ne sont pas des données du joueur).

Les source maps (`.map`) ne sont pas vendored, elles ne servent qu'aux DevTools.

`.gitattributes` marque `vendor/**` en `-text` : Git ne touche pas aux line endings, les files restent identiques octet pour octet.

## Licences

- tesseract.js et tesseract.js-core : Apache-2.0 (`LICENSE-tesseract.js.md`, `LICENSE-tesseract.js-core.txt`).
- Traineddata : Apache-2.0 (`LICENSE-tessdata.txt`, repo naptha/tessdata, tiré de tesseract-ocr/tessdata_best). Le `package.json` des packages `@tesseract.js-data` indique MIT, mais le repo d'où viennent les files est en Apache-2.0.
- `*.LICENSE.txt` : mentions des petites libs incluses dans les deux `.min.js` (regenerator-runtime, buffer et zlib.js en MIT, ieee754 en BSD-3-Clause), fournies telles quelles avec tesseract.js.

## Mettre à jour

1. Choisis la version de tesseract.js. Dans son `package.json`, la dependency `tesseract.js-core` (`^x.y.z`) donne la version du core que le worker charge par défaut : x.y.z.
2. Download les mêmes files sur jsDelivr (les URL ci-dessus avec les nouvelles versions) et remplace ceux de ce folder, sans les modifier.
3. Recalcule les sha256 (`sha256sum vendor/tesseract/*`) et mets le tableau à jour.
4. Si les traineddata changent : les browsers qui les ont déjà en cache gardent l'ancienne version (clé `./fra.traineddata` dans IndexedDB). Ajoute alors une option `cachePath` à `createWorker` (par exemple le nom de la nouvelle version) pour forcer un nouveau download.
5. Teste avec `python -m http.server` (le screenshot reader ne marche pas en ouvrant le file `index.html` directement) : un screenshot en FR et en EN, la console sans erreur, et dans l'onglet Network des DevTools, aucune request vers un autre site.
