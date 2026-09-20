# Brief — relecture qualité d’un chapitre

Fichier à donner à un agent pour refaire **la même passe** que Bordeaux
(`cards/c13-bordeaux.yaml`) sur un autre chapitre, par exemple Bourgogne :

```
Lis import/STUDY_CARD_QUALITY.md et applique-le à cards/c15-burgundy.yaml.
Mets à jour import/quality-review.yaml. Ne commit pas tant que je n’ai pas
demandé. make check à la fin.
```

Ce n’est **pas** un fact-check. Une bonne réponse factuelle peut quand même
échouer. On ne touche pas `import/progress.yaml`.

Source de vérité de **cette** passe. Le reste (`CONTENT_GUIDELINES.md`,
`AGENTS.md`, `import/AGENT_PLAYBOOK.md`) y renvoie. Le suivi carte par carte
est [quality-review.yaml](quality-review.yaml).

## Cinq barres

| Barre | Question | Échec typique |
| --- | --- | --- |
| **ISOLATION** | La carte se tient toute seule ? | « cette variation », « ce mélange », « those sites » |
| **CREDIBILITY** | Un WSET 3 hésite-t-il vraiment ? | Carmenère vs Merlot ; Alpes ; Chablis en Bordeaux |
| **LENGTH** | Un coup d’œil à la longueur donne-t-il la réponse ? | Clé de 20 mots, trois leurres de 4 mots |
| **WHY** | L’explication apporte-t-elle autre chose ? | Recopiage de la bonne réponse en gras |
| **SENSE** | Le français veut-il dire quelque chose ? | Calque, mot qui ne se dit pas en vin |

Réécrire **`en:` et `fr:` ensemble**. Même nombre de choix, **même index**
de la bonne réponse. Ne pas renommer les `id`.

## 1. Isolation

Chaque carte est tirée au sort dans Anki. Aucun « cette / ce / that / those /
ces » qui renvoie à la carte d’avant.

- Mauvais : *Comment les châteaux ambitieux atténuent-ils cette variation de millésime ?*
- Bon : *Comment les châteaux ambitieux réduisent-ils l’écart de qualité d’un millésime bordelais à l’autre ?*
- Mauvais : *Pourquoi ce mélange de cépages fonctionne-t-il vraiment ?*
- Bon : *Pourquoi un assemblage Merlot–Cabernet fonctionne-t-il vraiment à Bordeaux ?*

Nommer le sujet dans la question (cépage, AOC, rive, millésime).

## 2. Crédibilité des leurres

Les fausses réponses doivent être **pickables** : même classe, même cadre.

- Cépage vs cépage, AOC vs AOC, étape vs étape, climat vs climat.
- Dans le cadre de la question. Climat bordelais → maritime frais /
  continental / méditerranéen — pas mousson tropicale ni hiver polaire.
- Les leurres les plus plantés ou les plus cités à l’examen doivent être
  là quand c’est le sujet (Merlot **et** Cabernet Sauvignon **et**
  Cabernet Franc pour « quel noir occupe le plus d’hectares » — pas
  Carmenère / Petit Verdot à la place du Cabernet Sauvignon).
- Échec si trois leurres sont des blagues : Alpes, permafrost, irrigation
  à l’eau de mer, pomme comme cépage légal, Chablis / Champagne / Tokaj
  comme adresse du chapitre, Cognac, « tout jeter à l’égout ».
- Échec si le candidat n’a pas besoin de connaître le fait pour éliminer.

## 3. Longueur des choix

La bonne réponse ne doit pas sauter aux yeux parce qu’elle est plus longue
ou la seule phrase détaillée.

- Raccourcir la clé, mettre le détail dans le Why.
- Ou allonger les leurres **de la même classe** — pas du remplissage vide.
- Merlot vs Cabernet Sauvignon : OK (noms). Une clé de 20 mots à côté de
  trois stubs : pas OK.

## 4. Why (explication)

Ne **pas** recoller la bonne réponse. L’étudiant vient de la lire.

- Soit un fait **en plus** : mécanisme, exemple nommé, exception.
- Soit un Why **court**. Un Why long n’existe que pour enseigner ce que
  le choix n’a pas déjà dit.
- Jamais « option B » / « la réponse B ».
- Un nom de cépage ou d’AOC peut apparaître s’il sert un **fait nouveau**
  (« Le Merlot couvre plus de la moitié du vignoble »). Pas si le Why
  est juste le mot-clé relâché.

## 5. Sens français

Lire stem, choix et Why **comme du français**, pas comme une traduction.

- Si un locuteur dit « ça ne veut rien dire », recaster. Un calque mot
  à mot qui « matche » l’anglais échoue quand même.
- Tutoiement interdit. Registre vin : *cépages*, *élevage*, *assemblage*,
  *pourriture noble* — pas *variétés de raisins* sauf si c’est le point.
- La Why répond à la question **française**, pas à un autre stem.

### Mots et calques à ne pas répéter

Venus de la passe Bordeaux ; les chercher dans **tout** le chapitre.

| À éviter | Dire plutôt |
| --- | --- |
| *assaisonner* / *assaisonnement* (un cépage) | *cépage d’appoint*, *entrer en appoint* |
| *seasoning* (EN, même idée) | supporting grape / stay in the background |
| *un taux de graves* | *beaucoup de graves*, *les graves*, *sol graveleux* |
| *sols de graves* | *les graves*, *un sol de graves*, *terroir de graves* |
| *graves* minuscule vs *Graves* | cailloux / sol vs l’AOC |
| *quotidien* pour un vin « de tous les jours » | *de tous les jours*, *courant* |
| *millésime lent* | *millésime tardif* |
| *s’il verse à la vendange* | *s’il pleut fort à la vendange* |
| *mélange de cépages* (le vin) | *assemblage* |
| *Il l’allonge* (sujet perdu) | recaster la phrase entière |

Ne pas inventer d’AOC ni tordre un nom pour coller à l’anglais.

## Comment travailler

1. Un seul fichier `cards/cNN-….yaml`. Lots ≤ 40 cartes si un critic tourne.
2. Lire **toutes** les cartes du chapitre, pas un échantillon.
3. Corriger EN et FR ensemble. Index de la bonne réponse inchangé.
4. Mettre à jour [quality-review.yaml](quality-review.yaml) (pas
   `progress.yaml`) : `credibility` / `sense` / `length` / `why` /
   `isolation` si utile, `status: agent-fixed` ou `agent-pass`,
   `human: pending`.
5. `make check`.
6. Ne pas committer `.apkg`. Ne pas committer tant que l’humain n’a pas
   demandé.

## Rubric critic (coller)

```
Tu es critic qualité (lecture seule). N’édite pas. Ne commit pas.
Ce n’est PAS un fact-check. Relis fr: et les choix en: alignés.

1. ISOLATION — la carte est-elle autonome ? (pas cette / that / ce)
2. CREDIBILITY — leurres pickables, même classe, même cadre.
   Échec blague / impossible même si le fait est vrai.
3. LENGTH — la clé n’est pas visiblement la plus longue.
4. WHY — pas de recopiage de la clé. Fait en plus ou Why court.
5. SENSE — le français veut-il dire quelque chose ? Calques, mots
   qui ne se disent pas en vin : voir import/STUDY_CARD_QUALITY.md.

Retour EXACT :
ACCEPT_ALL=yes|no
REVISE: id — ISOLATION|CREDIBILITY|LENGTH|WHY|SENSE — une ligne
```
