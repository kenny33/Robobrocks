# Changelog

## [1.4.0] — 2026-11-24 — fork Robobrocks

Fork de l'intégration d'origine de thib3113 (dernière version connue : 1.3.0-pre10).
Aucun changement fonctionnel : le protocole BLE, les commandes et la logique sont identiques.

### Ajouté
- Liste de colis : quand un colis est terminé (rayé automatiquement après usage du code, ou
  coché à la main), son code à usage unique est supprimé de la boîte. Seuls les codes créés
  par l'intégration en usage unique sont concernés : un code saisi à la main (par exemple un
  code permanent) ou le code maître ne sont jamais supprimés. Si le colis est coché avant que
  son code ait été envoyé, l'envoi est simplement annulé. Décocher un colis annule une
  suppression encore en attente.
- Registre des codes permanents dans les options de l'intégration (menu « Codes permanents ») :
  créer ou modifier un slot (choisi dans une liste, formulaire prérempli, avec ou sans
  écriture sur la boîte), supprimer, réécrire tous les codes sur la boîte, nettoyer une plage
  de slots (avec écran de confirmation). Le registre est lié à l'adresse Bluetooth de la boîte. Un code du
  registre n'est jamais supprimé par la liste de colis. Utiliser un code du registre émet
  l'événement `robobrocks_permanent_code_used` (slot, code, libellé, heure) et met à jour la
  date de dernière utilisation du slot. Les options de l'intégration s'ouvrent
  maintenant sur un menu (« Paramètres » / « Codes permanents »).

### Changé
- Nouveau nom de projet et nouveau domaine Home Assistant : `boks` → `robobrocks`.
  Les services, événements, traductions et clés de stockage suivent le nouveau domaine
  (voir la section « Migration » du README).
- Le composant est maintenant dans `custom_components/robobrocks/`.
- Version minimale de Home Assistant : 2026.8.0.

### Corrigé
- `ImportError: cannot import name 'EntityCategory' from 'homeassistant.components.sensor'`
  au chargement (capteur de température de la batterie).
- Les appels à `device_registry.async_get_device` (déprécié, cassé en 2027.8.0) sont remplacés
  par `async_get_device_by_identifier`.
- L'appel à `DeviceEntry.config_entries` (déprécié, cassé en 2027.10.0) est remplacé par
  `config_entry_id`.
- Suppression d'un paquet de mise à jour : l'appel à `hass.components.persistent_notification`,
  qui n'existe plus dans HA, est remplacé par `persistent_notification.async_dismiss`.

- Liste de colis : un colis n'était pas rayé quand l'utilisation de son code arrivait par le
  relevé de fin de session Bluetooth (événement émis sans `config_entry_id` et avec un
  mauvais `device_id`), et le code utilisé était lu au mauvais endroit (`code` au lieu de
  `extra_data.code`) : aucun colis n'était rayé automatiquement. Bugs présents dans le code
  d'origine.

### Retiré
- Icône et logo du projet d'origine.
