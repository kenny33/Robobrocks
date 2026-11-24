# Changelog

## [Non publié] — fork Robobrocks

Fork de l'intégration d'origine de thib3113 (dernière version connue : 1.3.0-pre10).
Aucun changement fonctionnel : le protocole BLE, les commandes et la logique sont identiques.

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

### Retiré
- Icône et logo du projet d'origine.
