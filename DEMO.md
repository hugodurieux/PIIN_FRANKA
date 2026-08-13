# Démo Franka Panda — mode d'emploi

**État au 2026-08-13.** Ce fichier est autosuffisant : il n'y a rien à chercher
ailleurs pour lancer la démo devant quelqu'un.

Ce qui est montré : le bras planifie, descend, saisit un cube de 4 cm et le
soulève, piloté au couple à 1 kHz par un contrôleur couple-calculé + PD dont le
modèle de dynamique est extrait automatiquement de l'URDF.

---

## 0. Avant de commencer

- **Quatre terminaux**, tous frais. Chaque bloc ci-dessous précise lequel.
- Chaque commande est **sur une seule ligne**, à copier telle quelle. Ne les
  recompose pas à la main : des commandes longues collées dans un terminal ont
  déjà été tronquées silencieusement dans ce projet (un `checkpoint_path` perdu
  a invalidé une run entière sans le moindre message d'erreur).
- Compter **~2 minutes** entre le lancement et la première prise.
- Position du cube : `x=0.55, y=0, z=0.02`. C'est la seule configuration avec un
  taux de réussite mesuré (3/3, dispersion 1.0 mm).

---

## 1. La séquence

### Terminal 1 — simulateur

```
bash ~/projects/pinn_franka/ros2_ws/rebuild_and_relaunch_sim.sh
```

Tue les processus restants, vérifie qu'ils sont partis, reconstruit, puis lance.
**Attendre `OK: build succeeded` et que la fenêtre MuJoCo soit ouverte** avant de
passer au terminal 2.

### Terminal 2 — contrôleur

```
bash ~/projects/pinn_franka/ros2_ws/launch_pinn_demo.sh
```

Doit afficher `gain_safety_margin_override = 4.0`.
S'il affiche `No checkpoint_path set`, **arrêter** : le contrôleur publierait des
couples nuls et le bras s'effondrerait.

### Terminal 3 — mode effort

```
bash ~/projects/pinn_franka/ros2_ws/switch_to_effort.sh
```

Doit sortir avec le code 0. **Cette étape n'est pas optionnelle sur un sim
frais.** Sans elle, chaque couple publié est jeté en silence, tous les voyants
restent au vert, et le bras reste immobile au repos avec `joint7` à `-0.78529`.
C'est la signature exacte du bug qui a coûté une semaine à ce projet.

### Terminal 3 — la prise

```
source /opt/ros/jazzy/setup.bash && source ~/projects/pinn_franka/ros2_ws/install/setup.bash && source ~/projects/pinn_franka/ros2_ws/set_pinn_env.sh && python3 ~/projects/pinn_franka/stage4/test_grasp_pick.py 2>&1 | tee ~/projects/pinn_franka/stage4/test_grasp_pick_run49.log
```

Incrémenter `run49` à chaque exécution (48 est la dernière archivée).

---

## 2. Ce qu'on doit voir

| Étape | Attendu |
|---|---|
| 5 sous-étapes de pré-approche | `converged` sur chacune |
| Approche 1/2 puis 2/2 | `converged` |
| Erreur de prise finale | **~7 mm** (tolérance 20 mm) |
| Largeur de pince finale | **~0.040** |
| Levée de 0.150 m | `converged` |
| Verdict | `SUCCESS` |

**La largeur de pince est le meilleur instrument de mesure de la démo :**
`~0.040` = cube tenu à plat ; `~0.020` = cube lâché pendant la levée ;
`~0.053` = pince en diagonale sur les coins ; `~0.034` = pince refermée dans le
vide, trop haut. Un test qui annonce `SUCCESS` avec une largeur à 0.020 ment —
c'est déjà arrivé (run32) et c'est pour ça que la vérification post-levée existe.

---

## 3. Entre deux prises

### Terminal 3

```
bash ~/projects/pinn_franka/ros2_ws/reset_world_home.sh
```

Puis relancer la commande de prise en incrémentant le numéro de run.

**Ne jamais appeler le service `ResetWorld` directement.** Il réinitialise
silencieusement les articulations sur le PID de position interne du plugin, ce
qui fait jeter tous les couples sans qu'aucune couche ne le signale. Le script
ci-dessus réassère le mode effort automatiquement ; c'est toute sa raison
d'être.

---

## 4. Si ça casse — triage

Le point décisif : **distinguer un échec de planification d'un échec de suivi.**
Seul le second met en cause le contrôleur ou le modèle.

| Symptôme | Cause | Quoi faire |
|---|---|---|
| `planning failed, error_code=99999` après ~5 s | MoveIt n'a jamais produit de trajectoire — échantillonneur IK épuisé | Relancer ; si ça persiste, refaire le terminal 1 |
| Même message après ~1.8 ms | But en collision — scène de planification polluée | `reset_world_home.sh`, puis relancer |
| `still converging` 10 s, erreur **plate**, bras au repos | Couples jetés : mode effort perdu | Refaire le terminal 3 (`switch_to_effort.sh`) |
| `still converging`, erreur qui décroît trop lentement | Vraie limite de suivi | Le seul cas qui concerne le stage 1/3 |
| Le bras s'effondre | Le nœud du terminal 2 est mort | Relancer le terminal 2 |

**Avant toute hypothèse, lire le log du composant qui a échoué.** `move_group`
nomme ses échecs de planification explicitement. Dans ce projet, deux
corrections ont été faites contre des causes devinées alors que le vrai message
était déjà dans le log.

---

## 5. Arrêt

Ctrl-C dans le terminal 3, puis le 2, puis le 1.

**Attention, défaut connu : Ctrl-C sur le contrôleur fait tomber le bras.** Le
mode effort n'est sûr que tant que le nœud publie ; dès qu'il s'arrête, la
compensation de gravité disparaît. Sans conséquence en simulation, mais ne pas
le présenter comme un arrêt propre — sur un vrai robot c'est le rôle des freins.

---

## 6. Ce qu'on peut dire, et ce qu'il ne faut pas dire

**Le pipeline :** un fichier URDF en entrée, un robot contrôlable en sortie.
Quatre étages — apprentissage de dynamique (PINN), planification MoveIt2,
contrôle en couple, préhension. Les quatre fonctionnent bout en bout.

**Ce qui tourne réellement dans cette démo :** `tau = RNEA(q, q̇, q̈) + PD`.
Le résidu appris est **désactivé**, délibérément.

**Pourquoi — et c'est un résultat, pas un aveu.** Le résidu a été entraîné sur
Isaac Sim et la démo tourne sous MuJoCo. Mesuré, toutes choses égales par
ailleurs :

| | biais joint5 | erreur bride |
|---|---|---|
| résidu activé | −0.0337 rad | 14.3 mm |
| résidu désactivé | −0.0015 rad | 7.5 mm |

Le modèle appris **dégrade** le suivi d'un facteur 22 quand on le sort de son
domaine d'entraînement. Le confondant sur les gains pousse dans l'autre sens
(un Kp plus faible augmenterait `e_ss = tau/Kp`), donc le résultat y survit.

C'est un résultat de transfert de domaine, **pas** une réfutation de l'approche
grey-box. Ne pas le formuler comme « le PINN ne marche pas ».

**Autre chiffre honnête, si la question vient.** Sur une partition par
trajectoire (et non par échantillon), le modèle gris ne se sépare pas de RNEA
seul : 1.244 contre 1.185 Nm, avec une dispersion de 0.94 à 1.55 sur les
graines. La cause est identifiée — la meilleure perte de validation tombe dès
l'époque 1 et remonte ensuite, donc le checkpoint retenu est à peine entraîné,
faute de trajectoires distinctes (30 seulement). Ce qui a été confirmé au
passage : la boîte noire, elle, s'effondre à 4.48 Nm — ses 28 % d'avance
antérieurs venaient entièrement de la fuite temporelle.

**Ce qu'il reste à faire, si on demande.** `generate_mujoco_dataset.py` collecte
des données dans le domaine de déploiement via `mj_inverse` (quelques minutes,
sans Isaac). Réentraîner dessus, puis refaire exactement la comparaison
ci-dessus avec `launch_pinn_controller_ablation.sh` comme témoin. La barre à
battre est déjà mesurée : **7.5 mm**.

---

## 7. Aide-mémoire

| Besoin | Commande |
|---|---|
| Démo (résidu désactivé) | `bash ~/projects/pinn_franka/ros2_ws/launch_pinn_demo.sh` |
| Comparer avec le résidu activé | `bash ~/projects/pinn_franka/ros2_ws/launch_pinn_controller_boosted.sh 4.0` |
| Refaire l'ablation (témoin) | `bash ~/projects/pinn_franka/ros2_ws/launch_pinn_controller_ablation.sh` |
| Récupérer le mode effort | `bash ~/projects/pinn_franka/ros2_ws/force_effort_mode.sh` |
| Tout reconstruire et relancer | `bash ~/projects/pinn_franka/ros2_ws/rebuild_and_relaunch_sim.sh` |
