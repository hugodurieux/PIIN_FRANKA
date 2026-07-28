# Évaluation Critique Exhaustive : Pipeline « URDF vers robot commandé »

Ce document rassemble l'intégralité des retours, critiques et axes d'amélioration concernant la première version du rapport de recherche. Il est structuré par ordre de criticité, des failles scientifiques majeures aux détails formels.

## 1. Failles Logiques et Fondamentaux Scientifiques

*   **Le diagnostic de l'axe "figé" (Section 5.4) :** L'hypothèse incriminant le solveur de cinématique inverse (IK) de MoveIt2 (KDL) pour un blocage *en cours d'exécution* est dynamiquement incohérente. Un solveur IK génère une trajectoire de points de consigne avant l'exécution. Si un axe se fige pendant le suivi avec une erreur persistante et une commande PD active (de -4 à -11 Nm), le problème se situe au niveau de l'exécution, de l'asservissement ou de la physique du moteur, pas de la planification géométrique.
*   **L'abandon non justifié du formalisme Port-Hamiltonien :** La méthode s'oriente vers un MLP sous lagrangien augmenté classique en omettant de justifier pourquoi l'approche par systèmes Port-Hamiltoniens sur groupes de Lie n'a pas été retenue pour constituer les piliers de l'architecture. Ce formalisme garantit pourtant la passivité de manière intrinsèque, ce qui est supérieur à un forçage par pénalisation duale.
*   **La preuve de stabilité en boucle fermée (Section 3.5.2) :** Le calcul des gains PD s'appuie sur un théorème exigeant une erreur *strictement bornée* (au sens du pire cas). En remplaçant la borne maximale absolue (pouvant atteindre 65 Nm) par un quantile à 99,9 %, la garantie mathématique de stabilité au sens de Lyapunov est purement et simplement annulée pour devenir une simple espérance statistique.
*   **Un sous-échantillonnage spatial extrême (Section 3.4) :** Tirer seulement 10 configurations centrales via une séquence de Sobol dans un espace à 7 degrés de liberté laisse des vides immenses dans l'espace articulaire. Ce sous-échantillonnage n'est pas identifié dans les limites du rapport.
*   **Une contribution revendiquée mais non validée (Section 1.3) :** Le protocole de réduction de l'écart simulation-réalité est présenté comme l'une des quatre contributions majeures, pour être ensuite admis comme "non validé expérimentalement". Un protocole non testé reste une perspective, pas une contribution.

## 2. Faiblesses Méthodologiques et Argumentatives

*   **L'incohérence physique du modèle de frottement (Section 3.3.3) :** Le vecteur d'état passé au module de frottement contient la position spatiale (sin/cos de $q$). Physiquement, le frottement dépend de la vitesse et de la charge, mais ne devrait pas dépendre de la position, sauf modélisation d'un défaut d'usinage localisé.
*   **Le biais d'optimisation non corrigé (Section 5.3) :** L'erreur quadratique moyenne (MSE) de la fonction de perte n'est pas pondérée. Les axes porteurs ayant une limite de couple de 87 Nm et le poignet de 12 Nm, le réseau est mathématiquement incité à ignorer l'erreur du poignet. Constater ce défaut "a posteriori" sans avoir intégré de matrice de pondération diagonale dans la perte affaiblit la rigueur de l'apprentissage.
*   **La fragilité du Lagrangien Augmenté (Section 3.3.2) :** Le poids de pénalisation quadratique est fixé arbitrairement à $\rho = 1$. Aucune étude de sensibilité ou mise à jour adaptative n'est proposée, alors que l'instabilité de la montée duale est souvent liée à un mauvais calibrage de ce paramètre.
*   **Le "Sim-to-Sim gap" (Section 3.5.3) :** L'utilisation d'Isaac Sim pour générer les données d'entraînement et de MuJoCo pour la commande temps réel crée un écart de domaine injustifié qu'il faut expliquer.
*   **L'origine du "bruit capteur" (Section 3.6) :** L'argument justifiant l'affinage pour éviter de surapprendre le "bruit capteur" est caduc, puisque les données proviennent d'un simulateur qui ne génère pas nativement ce type de bruit matériel.
*   **Le choix de l'activation Mish (Section 3.3.1) :** Si le rejet de ReLU est très bien argumenté (nécessité d'une dérivée continue), le choix spécifique de Mish par rapport à d'autres fonctions lisses (GELU, Tanh) n'est pas justifié.
*   **Titre trompeur :** Le titre omet de préciser que l'intégralité des travaux a été réalisée en simulation.

## 3. Manques Formels et Structurels

*   **Absence de résumé (Abstract) :** Il manque un résumé (français/anglais) condensant le contexte, le verrou, la méthode et les résultats.
*   **Contexte institutionnel :** L'introduction plonge trop vite dans la technique. Il est nécessaire d'encadrer le stage en mentionnant le laboratoire d'accueil à Melbourne, ainsi que la finalité plus large liée à l'interaction humain-agent.
*   **Absence de spécifications matérielles :** Les détails d'architecture réseau sont présents, mais la configuration matérielle (CPU/GPU) et les temps d'entraînement sont absents, ce qui nuit à la reproductibilité.
*   **Gestion de la bibliographie :** L'utilisation de l'environnement manuel `thebibliography` est inadaptée pour un document de ce niveau. Une transition vers BibTeX/Biber s'impose.

## 4. Typographie et Purisme LaTeX

*   **Redondance avec `babel-french` :** Les espaces insécables forcés (`~;`, `~:`) sont inutiles et risqués, car `babel` gère déjà automatiquement la typographie française pour les ponctuations doubles.
*   **Absence de `siunitx` :** Les grandeurs physiques (Hz, Nm, rad) sont écrites en dur. L'utilisation du package `siunitx` est indispensable pour standardiser les unités et les espacements.
*   **Bidouillage de la macro `\parag` :** La redéfinition de commande pour forcer un comportement visuel en ignorant `tocdepth` est une mauvaise pratique LaTeX.
*   **Indices textuels en mode mathématique :** Les abréviations physiques en indice (comme $g_{\text{couple}}$) doivent utiliser `\mathrm{}` plutôt que `\text{}` pour garantir la robustesse typographique, indépendamment de la police du texte environnant.
