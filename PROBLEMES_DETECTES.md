**Formatage** :
    - Ligne trop longue (main.py)

**Sécurité** : 
    - Pas de sécurisation des endpoints
    - des api_key et des secrests éxposés... (main.py)
    - valeur par défaut non sécurisé dans les getenv

**Imports**

    - app/database.py : sys (unused) typing.Generator (unused)

    - app/main.py : os (unused) ,sys (unused) ,json (unused), typing.Dict (unused), typing.Any (unused)

    - app/models/item.py : typing.Optional (unused)

    - app/routes/items.py : typing.List (unused), datetime (unused), app.schemas.item.ItemCreate (unused)

    - app/schemas/item.py : typing.Optional (unused)

Total : 12 imports inutilisés

**Types (Typing)**

La root create ressembalait à rien. Il y a des any de partout c'est la merde.

**Documentation**

Des docstrings semblent manquer dans :

Les routes (app/routes/items.py)

Les services (app/services/*)

Les modèles (app/models/*)

**Code mort**

Plusieurs imports inutilisés (listés plus haut)