# Home Assistant App: MQTT HA to LOGO!

[![GitHub Release](https://img.shields.io/github/v/release/705marc/ha_to_logo?style=for-the-badge)](https://github.com/YOUR_GITHUB_USERNAME/mqtt_ha_to_logo/releases)
[![License](https://img.shields.io/github/license/705marc/ha_to_logo?style=for-the-badge)](LICENSE)
[![Home Assistant App](https://img.shields.io/badge/Home%20Assistant-App-blue?style=for-the-badge&logo=home-assistant)](https://www.home-assistant.io/)

A Home Assistant App to bridge Home Assistant MQTT messages and payload formats to Siemens LOGO! PLC-compatible MQTT structures.

---

## 🚀 Features

- **MQTT Translation:** Intercepts Home Assistant MQTT states (`convertHAtoLOGO/#`) and reformats them for Siemens LOGO! PLCs.
- **Payload Conversion:**
  - **Button / Pulse:** Converts `"Button"` commands into a brief pulse sequence (`[1]` followed by `[0]` after 0.5s).
  - **ON / OFF States:** Maps simple string commands (`"ON"` / `"OFF"`) to binary array values (`[1]` / `[0]`).
- **Zero-Config Integration:** Automatically integrates with the official Home Assistant Mosquitto Broker service.
- **Custom MQTT Support:** Option to connect to external MQTT brokers.

---

## 📦 Installation

### Option 1: Direct Import via My Home Assistant (Recommended)

Click the button below to automatically add this repository to your Home Assistant instance:

[![Open your Home Assistant instance and show the app store with a pre-filled repository url.](https://my.home-assistant.io/badges/addupdate_repository.svg)](https://my.home-assistant.io/redirect/addupdate_repository/?repository_url=https%3A%2F%2Fgithub.com%2F705marc%2Fha_to_logo)

---

### Option 2: Manual Repository Import

1. Copy the URL of this GitHub repository:
   ```text
   https://github.com/YOUR_GITHUB_USERNAME/mqtt_ha_to_logo
   ```
2. In your Home Assistant UI, navigate to **Settings** $\rightarrow$ **Apps** $\rightarrow$ **App Store**.
3. Click the **three dots (⋮)** in the top right corner and select **Repositories**.
4. Paste the URL into the repository field and click **Add**.
5. Scroll down or search for **MQTT HA to LOGO** under the newly added repository section and click **Install**.

---

## ⚙️ Configuration

Example configuration within Home Assistant:

```yaml
mqtt_broker: "auto"
mqtt_port: 1883
mqtt_user: ""
mqtt_password: ""
```

### Options

| Option          | Type    | Default | Description                                                                                                 |
| :-------------- | :------ | :------ | :---------------------------------------------------------------------------------------------------------- |
| `mqtt_broker`   | string  | `auto`  | Set to `auto` to use Home Assistant's built-in Mosquitto broker, or specify your custom broker IP/hostname. |
| `mqtt_port`     | integer | `1883`  | Port used by your MQTT broker.                                                                              |
| `mqtt_user`     | string  | `""`    | MQTT username (leave empty if using `auto` with local Mosquitto).                                           |
| `mqtt_password` | string  | `""`    | MQTT password (leave empty if using `auto` with local Mosquitto).                                           |

---

## 📡 Topic & Payload Structure

### Input Topic

The app listens to:

```text
devices/logo/convertHAtoLOGO/#
```

### Output Topic

The app stripped topic publishes directly to:

```text
devices/logo/#
```

### Processing Logic

1. **Button Action:**
   - **Input Payload:** `{"state": {"Light_1": {"value": "Button"}}}`
   - **Output Sequence:**
     1. `{"state": {"Light_1": {"value": [1]}}}`
     2. _(0.5s delay)_
     3. `{"state": {"Light_1": {"value": [0]}}}`

2. **ON Command:**
   - **Input Payload:** `{"state": {"Light_1": {"value": "ON"}}}`
   - **Output Payload:** `{"state": {"Light_1": {"value": [1]}}}`

3. **OFF Command:**
   - **Input Payload:** `{"state": {"Light_1": {"value": "OFF"}}}`
   - **Output Payload:** `{"state": {"Light_1": {"value": [0]}}}`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
