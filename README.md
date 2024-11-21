Pour l'instant:
- parse.py extrait les nouveaux morceaux depuis les playlists de streaming et les place dans l'excel de la librairie locale
- remove.py supprime les musiques avec le junk tag

Prochains dev:
- download.py passe sur toutes les musiques de la librairie qui n'ont pas de fichiers associés et propose d'associer le nouveau fichier téléchargé
- tags_sync.py:
1. télecharge les artworks des musiques
2. Met à jour Artiste + Titre dans le CSV en fonction des métadonnées du fichier audio (modifié via Rekordbox)
3. Met à jour le nom du fichier audio en fonction du combo Artiste + Titre dans l'excel