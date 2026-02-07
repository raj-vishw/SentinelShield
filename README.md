# 🛡️ SentinelShield
Hybrid Intrusion Detection & Web Protection System

## 📌 Overview
SentinelShield is a hybrid Web Application Firewall (WAF) and Intrusion Detection System (IDS) designed to inspect HTTP requests in real time, detect malicious activities, log security events, and visualize them through a live dashboard. The project demonstrates how modern web security systems analyze traffic, correlate detection signals, and assist security analysts in monitoring threats.

## 🚀 Key Features
- HTTP request inspection (path, parameters, body)
- Signature-based attack detection (SQLi, XSS, LFI, etc.)
- Behavior-based detection (burst requests, brute-force patterns)
- Correlation-based risk scoring
- Structured JSON logging
- Real-time auto-refreshing dashboard
- Manual IP banning from dashboard
- Inline WAF gateway (Client → WAF → Backend)

## 🧠 Architecture
Client → SentinelShield WAF → Backend Application  
                        ↓  
                     Logs → Dashboard

## 🧰 Technologies Used
- Python, Flask
- React (Vite)
- Node.js, npm
- JSON logging
- curl / Browser

## 📁 Project Structure
SentinelShield/
├── backend_app.py
├── waf_gateway.py
├── run.sh
├── core/
├── detectors/
├── api/
├── data/
└── sentinelshield-ui/

## ▶️ How to Run
1. Start Application:
Command: ./run.sh

## 🧪 Testing
Normal request:
curl http://127.0.0.1:5000/login

SQL Injection test:
curl "http://127.0.0.1:5000/login?user=admin%27%20OR%201=1"

## 📊 Dashboard
Access at: http://localhost:5173  
Displays live statistics, security events, risk trends, and IP ban controls.

## 🔮 Future Enhancements
- Database-based logging
- Auto IP banning
- Machine learning anomaly detection
- Dashboard authentication

## 🎓 Conclusion
SentinelShield provides hands-on experience with real-time web attack detection, logging, and security monitoring, closely simulating how modern web protection systems operate.
