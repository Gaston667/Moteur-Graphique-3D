# Moteur-Graphique-3D

## Description

Ce projet est un moteur graphique 3D développé en Python dans le but de comprendre le fonctionnement interne du rendu 3D et des moteurs graphiques.

L’objectif principal n’est pas d’utiliser une bibliothèque graphique avancée comme OpenGL ou Unity, mais de recréer les bases d’un moteur 3D à partir de zéro afin d’apprendre les concepts fondamentaux de l’infographie et du rendu temps réel.

Le moteur fonctionne actuellement dans le terminal et permet déjà de :

- gérer une caméra 3D avec déplacements et rotations ;
- projeter des objets 3D sur un plan 2D ;
- afficher des triangles et des meshes ;
- charger des modèles `.obj` ;
- manipuler des vecteurs et des calculs mathématiques liés à la 3D.

---

## Concepts travaillés

Ce projet permet de travailler plusieurs notions importantes :

- coordonnées et vecteurs 3D ;
- transformations géométriques ;
- rotations (`pitch`, `yaw`, `roll`) ;
- projection perspective ;
- rasterisation ;
- gestion des inputs clavier ;
- architecture d’un moteur graphique ;
- chargement de modèles 3D.

---

## Objectifs du projet

L’objectif à long terme est d’ajouter progressivement :

- la rasterisation complète des triangles ;
- le remplissage des polygones ;
- le Z-buffer ;
- les textures ;
- la lumière et le shading ;
- une interface graphique plus avancée ;
- un véritable pipeline de rendu 3D.
