**Questions à documenter** :

1. **Qu'est-ce que la CI (Continuous Integration) ?**
    - La CI est une pratique consistant à intégrer fréquemment du code dans un dépôt partagé avec tests automatisés.

    - Elle résout les conflits d’intégration tardifs et détecte rapidement les régressions.

    - Principes clés : intégrations fréquentes, tests automatisés, builds reproductibles.

    - Exemples d’outils : GitHub Actions, GitLab CI, Jenkins.

2. **Qu'est-ce que le CD (Continuous Deployment/Delivery) ?**
   - Le CD automatise la mise à disposition du code jusqu'aux environnements de test ou de production.
   - Delivery = déploiement automatisé jusqu'à la pré-prod ; Deployment = déploiement automatique en prod.
   - Bénéfices : livraisons rapides et fiables ; Risques : déployer des bugs plus rapidement si les tests sont insuffisants.

3. **Pourquoi CI/CD est important ?**
   - Qualité du code : détecte tôt les erreurs, renforce la stabilité grâce aux tests automatisés.
   - Vitesse de développement : réduit les temps de build, release et feedback.
   - Collaboration : facilite le travail parallèle et réduit les conflits entre développeurs.

4. **Qu’est-ce que uv ?**

    - Gestionnaire ultra-rapide pour Python (install, run, build) basé sur Rust.

    - Différences avec pip/poetry/pipenv : Plus rapide, unifié (install + venv + lock), sans dépendance Python, CLI moderne.

    - Avantages Vitesse extrême, gestion simple des environnements et lockfile, compatible pyproject, reproductible.

    - Fonctionnement avec pyproject.toml,uv lit et écrit les dépendances directement dans pyproject.toml.

    - Structure par Sections [project], [tool.uv], [project.optional-dependencies], etc.

    - Gestion des dépendances : uv add, uv remove, uv lock; gère prod/dev/optional via sections séparées.

    - Build backend : Peut utiliser uv comme backend ([build-system]) ou un backend existant (setuptools, hatch, poetry-core).

    - Utiliser uv dans GitHub Actions, Installation uses: astral-sh/setup-uv@v1,

    - Cache Utilise automatiquement le cache basé sur le lockfile.

    - Commandes
        run: `uv sync`,
        run: `uv run pytest`

5. **Versionnage sémantique (SemVer)**

    - Format : MAJOR.MINOR.PATCH.

    - MAJOR : changements incompatibles (breaking).

    - MINOR : nouvelles fonctionnalités compatibles.

    - PATCH : corrections sans impact fonctionnel.

6. **Conventional Commits**

    - Format : type(scope): description.

    - Types : feat, fix, docs, refactor, test, chore, etc.

    - Impact : feat → bump MINOR, fix → PATCH, BREAKING CHANGE → MAJOR.

7. **python-semantic-release**

    - Analyse les commits selon Conventional Commits et décide du bump auto.

    - Config dans pyproject.toml ([tool.semantic_release]).

    - Génère automatiquement un CHANGELOG basé sur les commits.

    - Crée et publie la release GitHub + tag Git + version PyPI si configuré.

8. **Comment MkDocs génère de la documentation ?**
    - MkDocs prend des fichiers Markdown, applique un thème, et génère un site statique HTML organisé selon mkdocs.yml.

    - Comment déployer sur GitHub Pages ? On active GitHub Pages et on pousse le dossier site/ généré, ou on utilise mkdocs gh-deploy pour automatiser le déploiement.

    - Qu'est-ce que mkdocstrings ? C’est un plugin MkDocs qui génère automatiquement la documentation du code à partir des docstrings de vos modules.