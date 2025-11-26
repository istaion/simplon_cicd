# Comparatif des outils Python

## Linters Python

| Outil | Avantages | Inconvénients | Note /10 | Choix ? |
|-------|-----------|---------------|----------|---------|
| **Ruff** | Ultra rapide, remplace flake8/isort/bandit partiel, config simple | Moins complet sur règles complexes que Pylint | 9/10 | ✅ |
| **Flake8** | Standard historique, énorme écosystème de plugins | Lent comparé à Ruff, règles limitées par défaut | 7/10 | ❌ |
| **Pylint** | Analyse la plus stricte et complète, suggestions refactor | Très lent, souvent trop verbeux | 6/10 | ❌ |

---

## Formatters Python

| Outil | Avantages | Inconvénients | Note /10 | Choix ? |
|-------|-----------|---------------|----------|---------|
| **Ruff format** | Ultra rapide, compatible Black | Encore jeune | 9/10 | ✅ |
| **Black** | Standard de facto, opinionated | Pas de customisation | 8/10 | ✔️ |
| **autopep8** | Personnalisable | Résultats parfois incohérents, moins adopté | 5/10 | ❌ |

---

## Type Checkers

| Outil | Avantages | Inconvénients | Note /10 | Choix ? |
|-------|-----------|---------------|----------|---------|
| **Mypy** | Référence, rigoureux | Plus lent, config complexe | 8/10 | ✔️ |
| **Pyright** | Très rapide, super intégration VS Code, meilleur inference | Moins strict par défaut | 9/10 | ✅ |
| **Pyre** | Très rapide sur grands projets | Moins maintenu et communauté plus petite | 6/10 | ❌ |

---

## Frameworks de Tests

| Outil | Avantages | Inconvénients | Note /10 | Choix ? |
|-------|-----------|---------------|----------|---------|
| **pytest** | Simple, assertions natives, plugins puissants | Peut encourager structure trop libre | 10/10 | ✅ |
| **unittest** | Standard builtin stable | Verbeux, moins flexible | 6/10 | ❌ |

---

## Security Scanners

| Outil | Avantages | Inconvénients | Note /10 | Choix ? |
|-------|-----------|---------------|----------|---------|
| **Bandit** | Analyse statique du code | Scope limité | 7/10 | ✔️ |
| **Safety** | Vérifie vulnérabilités dépendances | Pas d'analyse code | 8/10 | ✔️ |
| **Snyk** | Complet (code + deps + containers) | Payant pour l'avancé | 9/10 | 💰 |
| **Trivy** | Excellent pour images Docker et infra | Moins adapté pur Python | 8/10 | ✔️ |

---

## Recommandations globales

| Catégorie | Choix recommandé |
|-----------|------------------|
| Linter | **Ruff** |
| Formatter | **Ruff format** ou **Black** |
| Type checker | **Pyright** |
| Tests | **pytest** |
| Security | **Safety + Trivy** |
