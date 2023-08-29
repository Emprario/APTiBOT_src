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
Quand un utilisateur réagit à un émoji, si une opération interne n'est pas déjà en cours, il va réagir à la demande de rôle. Le bot va update votre status en considérant la hiérarchie des rôles ( `CGU_ROOT < CLASSE < ROLES (extra)` )