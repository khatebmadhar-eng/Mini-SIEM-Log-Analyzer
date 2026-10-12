# 🛡️ Mini SIEM & Log Analyzer

An advanced, lightweight **Security Information and Event Management (SIEM)** and log analysis tool built with **Flask** and styled with a high-end, custom **Cyber SOC Dark/Neon UI**. Designed specifically to simulate, detect, and respond to real-world security threats in real-time.

---

## 🚀 Key Features

* **Automated Log Parsing & Analysis:** Automatically ingests and parses system/web server logs to flag anomalies.
* **Real-Time Threat Detection:** Detects high-priority security incidents including:
  * Brute-Force Attack attempts.
  * Unauthorized access and suspicious IP traffic.
* **Cyber SOC Dashboard:** A fully custom, dark-mode/neon visual interface featuring real-time tickers, security metrics, and live alert feeds.
* **Incident Response Protocols:** Built-in simulation tools to trigger mock attacks and test automated mitigation responses.
* **Interactive Simulators:** Test incident response workflows directly from the browser interface.

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML5, CSS3 (Custom Cyber SOC Theme), JavaScript
* **Version Control:** Git & GitHub

---

## 📂 Project Structure

```text
Mini-SIEM-Log-Analyzer/
│
├── app2.py              # Main Flask application logic & routing
├── pp2.py               # Log parsing and threat detection engine
├── templates/           # HTML templates (SOC Dashboard, Alert panels)
├── static/              # CSS stylesheets & custom neon SOC assets
└── README.md            # Project documentation
