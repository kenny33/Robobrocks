# Robobrocks

Intégration Home Assistant (custom component) pour une boîte à colis connectée en Bluetooth Low Energy.

## Origine et attribution

Ce projet est un fork de l'intégration **ha-boks**, écrite par **thib3113**
(dépôt d'origine `github.com/thib3113/ha-boks`, aujourd'hui retiré de GitHub).
Tout le code fonctionnel vient de ce projet. Ce fork change seulement le nom du projet
et corrige la compatibilité avec les versions récentes de Home Assistant.

## Licence

Distribué sous licence **GNU General Public License v3.0** (voir [LICENSE](LICENSE)).

Code d'origine © thib3113. Modifications du fork © 2026 David Legros.

Ce programme est un logiciel libre : vous pouvez le redistribuer et/ou le modifier selon
les termes de la GNU GPL telle que publiée par la Free Software Foundation, version 3.
Il est distribué SANS AUCUNE GARANTIE, sans même la garantie implicite de qualité
marchande ou d'adéquation à un usage particulier.

## Compatibilité matérielle

Fonctionne avec les boîtes à colis de la marque Boks (modèle « Boks ONE », PCB 3.0 et 4.0).
Robobrocks est un projet indépendant, sans lien avec ce fabricant.

## Fonctionnalités

- Serrure (`lock`) : ouverture de la porte avec le code maître.
- Capteurs : batterie, température de la batterie, nombre de codes, nombre de journaux,
  dernier événement, état de maintenance, diagnostics batterie.
- Bouton de synchronisation des journaux, entité `event` pour l'historique, liste
  de colis (`todo`). Un colis ajouté sans code reçoit un code à usage unique ; quand le
  colis est rayé (code utilisé) ou coché à la main, ce code est supprimé de la boîte.
  Les codes saisis à la main et les codes permanents ne sont jamais supprimés.
- Registre des codes permanents (voir ci-dessous).
- Services `robobrocks.*` : gestion des codes (maître, usage unique, multi-usage),
  badges NFC, configuration, synchronisation des journaux, génération de code PIN,
  paquets de mise à jour du firmware.

Version minimale de Home Assistant : **2026.8.0**.

## Codes permanents

La boîte range ses codes permanents dans des emplacements numérotés (slots). Elle sait dire
combien elle en contient, mais pas lesquels. Robobrocks tient donc un **registre** des slots
dans Home Assistant : numéro, code et libellé.

**Paramètres → Appareils et services → Robobrocks → Configurer → Codes permanents** :

- **Créer / modifier un slot** : choisir un slot dans la liste (chaque slot est affiché
  « libre » ou avec son libellé et son code). Le formulaire est prérempli pour un slot
  enregistré. Laisser le code vide pour en générer un au hasard. Décocher « Écrire sur la
  boîte » pour seulement enregistrer un code déjà présent dans la boîte : à faire une fois pour
  chaque code créé avant Robobrocks. Si seul le libellé change, rien n'est envoyé.
- **Supprimer un code** : dans la boîte et dans le registre, ou dans le registre seulement.
- **Réécrire tous les codes sur la boîte** : après une réinitialisation de la boîte.
- **Nettoyer une plage de slots** : vide les slots de X à Y (100 au maximum), dans la boîte et
  le registre, ou dans le registre seulement. Un écran de confirmation liste les codes
  enregistrés concernés et demande de cocher « Je confirme ». Il signale aussi si le code
  d'ouverture utilisé par HA est dans la plage. Le nettoyage de la boîte se fait en
  arrière-plan : le capteur de maintenance montre la progression, puis une notification
  s'affiche à la fin.

L'écran affiche aussi le nombre de codes permanents que déclare la boîte, pour repérer un écart,
et la date de dernière utilisation de chaque slot.

Quand les journaux de la boîte montrent qu'un code du registre a été utilisé, Robobrocks émet
l'événement `robobrocks_permanent_code_used` avec `slot`, `code`, `label`, `timestamp` (heure
d'utilisation d'après la boîte), `device_id` et `config_entry_id`. Comme pour les colis,
l'événement arrive au relevé des journaux, donc avec jusqu'à 10 minutes de retard. Exemple :

```yaml
triggers:
  - trigger: event
    event_type: robobrocks_permanent_code_used
    event_data:
      label: Amazon
actions:
  - action: notify.notify
    data:
      message: "📦 Colis Amazon déposé ({{ trigger.event.data.timestamp[11:16] }})"
```

Le registre est stocké dans `/config/.storage/robobrocks_permanent_codes_<adresse>` et inclus
dans les sauvegardes. Comme il est lié à l'adresse Bluetooth de la boîte, il est retrouvé
même si l'intégration est supprimée puis ajoutée à nouveau. Un code du registre n'est jamais
supprimé par la liste de colis.

## Installation (HACS)

1. HACS → menu ⋮ → **Dépôts personnalisés** → ajouter `https://github.com/kenny33/Robobrocks`,
   catégorie **Intégration**.
2. Installer **Robobrocks**, puis redémarrer Home Assistant.
3. **Paramètres → Appareils et services → Ajouter une intégration → Robobrocks**.
   L'appareil est aussi proposé automatiquement s'il est détecté en Bluetooth.

## Migration depuis l'ancienne intégration (domaine `boks`)

Home Assistant ne sait pas déplacer une intégration d'un domaine à un autre. La migration
se fait à la main : on supprime l'ancienne intégration, puis on ajoute Robobrocks.

### Avant de commencer

1. **Note tes identifiants.** Le config flow redemandera l'adresse Bluetooth, le
   **code maître** et la **clé de configuration** (ou la clé maître). Si tu ne les as plus,
   ils se trouvent dans `/config/.storage/core.config_entries`, dans l'entrée
   `"domain": "boks"` (champs `address`, `master_code`, `config_key` / `master_key`).
2. **Note le nom de l'appareil** affiché dans HA (ex. `E3E787AF111`). Si tu réutilises
   exactement le même nom, les `entity_id` resteront identiques.
3. Fais une sauvegarde Home Assistant.

### Procédure

1. **Paramètres → Appareils et services** → ancienne intégration `boks` → **Supprimer**.
   Cette étape doit venir *avant* l'ajout de Robobrocks : sinon les nouvelles entités
   prennent un suffixe `_2`.
2. Supprime le dossier `/config/custom_components/boks/` (ou supprime le dépôt dans HACS).
3. Installe Robobrocks (voir ci-dessus) et redémarre.
4. Ajoute l'intégration Robobrocks et saisis les mêmes identifiants. Garde le **même nom**
   d'appareil.
5. Mets à jour tes automatisations, scripts et dashboards (voir ci-dessous).

### Ce qui change pour toi

| Élément | Après migration | Action |
|---|---|---|
| `unique_id` des entités | Même texte (basé sur l'adresse Bluetooth), mais rattaché à la plateforme `robobrocks` : ce sont de nouvelles entrées dans le registre | Aucune |
| `entity_id` (ex. `lock.e3e787af111_…`) | **Identiques**, à condition de supprimer l'ancienne intégration d'abord et de garder le même nom d'appareil | Vérifier ; renommer si un `_2` apparaît |
| Historique et statistiques | Conservés : ils sont indexés par `entity_id` | Aucune si les `entity_id` sont identiques |
| Dashboards | Fonctionnent s'ils utilisent des `entity_id` | Aucune dans ce cas |
| `device_id` | **Nouveau** | Refaire les déclencheurs, conditions et actions de type « appareil » |
| Services | `boks.*` → `robobrocks.*` (ex. `boks.open_door` → `robobrocks.open_door`) | Modifier scripts et automatisations |
| Événements | `boks_log_entry`, `boks_parcel_completed`, `boks_logs_retrieved` → `robobrocks_…` | Modifier les déclencheurs d'événement |
| Liste de colis (`todo`) | Les colis en attente ne sont **pas** repris (stockage lié à l'ancienne entrée) | Les noter avant et les ressaisir |
| Paquets firmware locaux | `/config/www/boks/` n'est plus utilisé, Robobrocks utilise `/config/www/robobrocks/` | Supprimer l'ancien dossier si tu veux |
| Zones, étiquettes, noms personnalisés de l'appareil | Non repris | Les réattribuer |

### Pourquoi pas de migration automatique

Le code de l'ancien domaine n'existe plus, et Home Assistant ne fournit pas de mécanisme
pour transférer une entrée de configuration d'un domaine à un autre. Une migration automatique
demanderait d'écrire du code spécifique (lecture de l'ancienne entrée, transfert des entités
et de l'appareil). Ce code serait difficile à tester sur une seule installation, et une
erreur pourrait laisser le registre dans un état incohérent. La procédure ci-dessus est
plus simple et réversible grâce à la sauvegarde.
