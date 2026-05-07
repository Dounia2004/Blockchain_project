Voici le workflow complet, propre et sans erreur pour tester l'application de bout en bout ! 

Assure-toi d’utiliser Postman (ou un autre client API) et de bien changer d'utilisateur (via l'authentification) selon l'étape.

### 🏠 Étape 1 : Créer la Propriété (Côté Django)
* **Qui est connecté :** `admin123` (le propriétaire)
* **Endpoint :** `POST http://127.0.0.1:8000/api/properties/`
* **Body (JSON) :**
```json
{
    "title": "Super Appartement",
    "description": "Très beau",
    "property_type": "APARTMENT",
    "address": "123 Rue de la Paix",
    "city": "Paris",
    "postal_code": "75000",
    "country": "France",
    "surface_area": 50.0,
    "rooms": 2,
    "bedrooms": 1,
    "price_per_month": "1000.00",
    "security_deposit": "2000.00"
}
```
👉 **Résultat :** L'API te renvoie un objet. **Copie l'UUID du champ `"id"`** de cette propriété (ex: `1111-2222...`).

---

### 🔗 Étape 2 : Déployer la Propriété sur la Blockchain (Ganache)
* **Qui est connecté :** `admin123` (le propriétaire)
* **Endpoint :** `POST http://127.0.0.1:8000/api/properties/TON_UUID_DE_PROPRIETE/deploy_to_blockchain/`
* **Body (JSON) :**
```json
{
    "tenant_address": "0x_ADRESSE_GANACHE_DE_MOSSAB",
    "duration_months": 12
}
```
👉 **Résultat :** Ça va consommer du Gas sur Ganache. L'API te renvoie :
```json
{
    "contract_address": "0xABC123...",
    "transaction_hash": "0xDEF456..."
}
```
**Copie l'adresse du contrat (`0xABC123...`)**.

---

### 📝 Étape 3 : Créer le Contrat de Location (Côté Django)
Maintenant que le fix de tout à l'heure est en place, l'adresse blockchain sera bien sauvegardée !
* **Qui est connecté :** `admin123` (le propriétaire)
* **Endpoint :** `POST http://127.0.0.1:8000/api/contracts/`
* **Body (JSON) :**
```json
{
    "property": "TON_UUID_DE_PROPRIETE",
    "tenant": 4,  
    "start_date": "2026-06-01",
    "end_date": "2027-06-01",
    "monthly_rent": "1000.00",
    "security_deposit": "2000.00",
    "blockchain_contract_address": "0xABC123_ADRESSE_COPIEE_A_L_ETAPE_2"
}
```
*(Vérifie bien que `tenant: 4` correspond à l'ID de Mossab)*
👉 **Résultat :** Le contrat est créé ! **Copie l'UUID du champ `"id"`** de ce tout nouveau contrat (ex: `3333-4444...`).

---

### ✍️ Étape 4 : Signer et Payer la Caution (Ganache)
C'est au locataire de jouer ! Tu dois te déconnecter de `admin123` et te connecter avec le compte du locataire.
* **Qui est connecté :** `mossab` (le locataire)
* **Endpoint :** `POST http://127.0.0.1:8000/api/contracts/TON_UUID_DE_CONTRAT/sign_on_blockchain/`
* **Body :** Vide `{} ` (pas besoin de paramètres)
👉 **Résultat :** L'API va récupérer la clé privée de `mossab`, l'adresse du smart contract attachée à ce contrat Django, et payer la caution de *2000 ETH (Wei)* sur Ganache. Tu recevras un `transaction_hash`. Le statut du contrat passe en "ACTIVE".

---

### 💸 Étape 5 : Payer le Loyer Mensuel (Ganache)
* **Qui est connecté :** `mossab` (le locataire)
* **Endpoint :** `POST http://127.0.0.1:8000/api/contracts/TON_UUID_DE_CONTRAT/pay_rent_blockchain/`
* **Body :** Vide `{}`
👉 **Résultat :** *1000 ETH (Wei)* sont transférés du portefeuille de Mossab vers l'adresse de Admin123 sur Ganache.

**Et voilà ! Ton cycle Immobilier × Blockchain fonctionne de A à Z !**