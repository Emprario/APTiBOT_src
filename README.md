# APTiBOT
Source code for Aptibot a discord bot
---
## Fonctionnalités
- [x] Choisir sa classe (byREACT)
- [x] Accepter les cgu (byREACT)
- [x] Chosir ses salons (byREACT)
- [ ] Nouveutés - Changelog
- [ ] CGPU Mandatory (et aboressence des rôles)
- [ ] Obligatoire de choisir une classe & sinon efrei externe
- [ ] Réagir à une liste de mot clef (memer)
- [ ] Renforcer la sécurité
- [ ] Edt
- [ ] Météo
- [ ] Actu de l'école (fetch from myefrei.fr)
- [ ] ? Connexion avec my efrei

## API references
* python3.11.x - discord.py : https://discordpy.readthedocs.io/en/stable/api.html

## Description technique d'attribution des rôles
Quand un utilisateur réagit à un émojie, le bot va obtenir un status de ces rôles sous forme d'un objet `User_pystatus` composé de l'état des trois stages de roles (cf [main.py](main.py)). En fonction de ce dernier la fonction `update_status` va update ses rôles (rajouter rôle, enlever rôle, enlever (update) réaction) avec des fonctions de micro-actions: 