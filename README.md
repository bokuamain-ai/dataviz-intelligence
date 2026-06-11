# 🎓 Système de Gestion des Étudiants (Student Manager)

![C++](https://img.shields.io/badge/C%2B%2B-17-blue.svg)
![Qt](https://img.shields.io/badge/Qt-GUI-green.svg)
![IMS](https://img.shields.io/badge/Groupe-1%C3%A8re_année_IMS-yellow.svg)

## 📌 Informations sur le Projet
- **Auteurs** : Hammouchi Niama & Ihardane Hammouchi
- **Groupe** : 1ère année IMS
- **Année Universitaire** : 2025/2026
- **Date de Rendu** : 15-05-2026

## 📖 Description
Un système complet et robuste de gestion des étudiants développé en **C++ Orienté Objet**. 
Ce projet intègre les concepts avancés du C++ : Héritage, Polymorphisme, STL, Gestion des Exceptions personnalisées, Persistance des données et une Interface Graphique Interactive développée avec le framework **Qt**.

## ✨ Fonctionnalités Principales
- **Navigation et CRUD** : Ajout, modification et suppression rapide d'étudiants.
- **Polymorphisme** : Gestion de 3 types de profils spécifiques :
  - `Licence` (Undergraduate)
  - `Master` (Graduate)
  - `Doctorat` (PhD)
- **Logique Métier** : Calcul automatique des bourses en fonction du niveau et des résultats.
- **Analyse et Recherche** : Tri personnalisé par GPA ou par nom, et recherche dynamique en temps réel.
- **Persistance** : Sauvegarde et rechargement des données depuis des fichiers textes (`data/students.txt`).
- **Robustesse** : Gestion complète des exceptions (entrées invalides, étudiants introuvables, erreurs de fichiers).
- **Fiabilité** : Tests unitaires approfondis intégrés (20/20 tests réussis).

## 🗂 Structure du Projet

```text
StudentManager/
├── src/
│   ├── models/          # Classes métiers (Student, Undergraduate, Graduate, PhD)
│   ├── services/        # Logique métier et contrôleur (StudentManager)
│   ├── exceptions/      # Classes d'exceptions personnalisées
│   ├── persistence/     # Lecture/écriture dans les fichiers de données
│   └── gui/             # Composants de l'interface graphique (MainWindow, etc.)
├── data/
│   └── students.txt     # Données persistantes des étudiants
├── tests/
│   └── test_main.cpp    # Suites de tests unitaires automatiques
├── StudentManager.pro   # Fichier de configuration du projet Qt
└── README.md
```

## 🚀 Compilation et Exécution

### 1. Interface Graphique (Qt)
Pour compiler et lancer l'application graphique, utilisez les commandes suivantes depuis la racine du projet dans un environnement équipé de Qt et MinGW :

```bash
# Générer le Makefile avec qmake
qmake StudentManager.pro

# Compiler le projet
mingw32-make

# Exécuter l'application
release\StudentManager.exe
```

### 2. Tests Unitaires
Pour valider le fonctionnement de la logique métier sans l'interface client, compilez et lancez les tests manuellement avec `g++` :

```bash
# Compiler les tests
C:\mingw64\bin\g++ -std=c++17 -static tests/test_main.cpp src/models/*.cpp src/services/StudentManager.cpp src/persistence/PersistenceManager.cpp -o tests/test_main.exe

# Exécuter les tests
tests\test_main.exe
```

## 🔗 Liens Utiles
- 🎥 **Vidéo de démonstration** : [Regarder sur Google Drive](https://drive.google.com/file/d/1_Wu4_REoT6HQ0Y9L9Z5I8xHCvL4F1egA/view?usp=drivesdk)
- 💻 **Dépôt GitHub** : [Accéder au code source](https://github.com/bokuamain-ai/miniprojet-cpp-Hammouchi-Ihardane)
- 📄 **Rapport PDF** : [Consulter le rapport](https://drive.google.com/file/d/1YUrdYXwi-AQAOFH-o0EC5sTaIo9SFpD9/view?usp=drivesdk)
