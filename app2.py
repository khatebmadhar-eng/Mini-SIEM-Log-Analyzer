from flask import Flask, render_template_string, request
import re

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MINI SIEM // ADVANCED THREAT HUNTING MATRIX</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

        body {
            margin: 0;
            padding: 20px;
            font-family: 'Share Tech Mono', monospace;
            background-color: #010204;
            color: #00ff66;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 50% 20%, rgba(0, 255, 102, 0.12) 0%, rgba(1, 2, 4, 0.98) 85%),
                linear-gradient(rgba(0, 255, 102, 0.025) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 102, 0.025) 1px, transparent 1px);
            background-size: 100% 100%, 25px 25px, 25px 25px;
        }

       
        .ticker-wrap {
            width: 100%;
            background: #001105;
            border-bottom: 1px solid #00ff66;
            border-top: 1px solid #00ff66;
            overflow: hidden;
            white-space: nowrap;
            box-sizing: border-box;
            margin-bottom: 20px;
            padding: 5px 0;
        }
        .ticker {
            display: inline-block;
            animation: ticker 25s linear infinite;
            font-size: 12px;
            color: #00ff66;
        }
        .ticker-item {
            display: inline-block;
            padding: 0 2rem;
        }
        @keyframes ticker {
            0% { transform: translate3d(0, 0, 0); }
            100% { transform: translate3d(-50%, 0, 0); }
        }

        body::after {
            content: " ";
            display: block;
            position: fixed;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.04), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.04));
            z-index: 99999;
            background-size: 100% 3px, 3px 100%;
            pointer-events: none;
        }

        .container {
            background: rgba(3, 10, 6, 0.96);
            padding: 30px;
            border-radius: 6px;
            box-shadow: 0 0 40px rgba(0, 255, 102, 0.3), inset 0 0 20px rgba(0, 255, 102, 0.08);
            width: 95%;
            max-width: 900px;
            border: 1px solid #00ff66;
            position: relative;
        }

        .container::before {
            content: "AI_SOC_CORE // DEFCON_1_ACTIVE";
            position: absolute;
            top: -10px;
            left: 20px;
            background: #010204;
            padding: 0 10px;
            font-size: 11px;
            color: #00ff66;
            letter-spacing: 2px;
        }

        h2 { 
            color: #00ff66; 
            text-align: center; 
            margin-bottom: 5px; 
            text-shadow: 0 0 15px rgba(0,255,102,0.7); 
            letter-spacing: 2px;
            font-size: 28px;
        }
        .subtitle { text-align: center; color: #00aa44; font-size: 12px; margin-bottom: 25px; letter-spacing: 1.5px; }
        
        /* Stats Cards */
        .stats-grid {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: #010603;
            border: 1px solid #004411;
            padding: 12px;
            border-radius: 4px;
            flex: 1;
            text-align: center;
            box-shadow: inset 0 0 10px rgba(0,255,102,0.05);
        }
        .stat-card span { display: block; font-size: 11px; color: #00aa44; text-transform: uppercase; }
        .stat-card strong { font-size: 22px; color: #00ff66; text-shadow: 0 0 8px rgba(0,255,102,0.4); }

        /* Incident Timeline */
        .timeline-box {
            background: #010603;
            border: 1px solid #004411;
            border-radius: 4px;
            padding: 12px 15px;
            margin-bottom: 20px;
        }
        .timeline-title { font-size: 12px; color: #00ff66; font-weight: bold; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
        .timeline-steps {
            display: flex;
            justify-content: space-between;
            position: relative;
            font-size: 11px;
            color: #00aa44;
        }
        .step { text-align: center; z-index: 2; background: #010603; padding: 0 5px; }
        .step.active { color: #ff3333; font-weight: bold; text-shadow: 0 0 8px rgba(255,51,51,0.6); }

        /* Quick Simulator Buttons */
        .quick-actions {
            display: flex;
            gap: 10px;
            margin-bottom: 8px;
        }
        .quick-btn {
            background: #010603;
            color: #00ff66;
            border: 1px solid #00ff66;
            padding: 6px 12px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 11px;
            font-weight: bold;
            font-family: 'Share Tech Mono', monospace;
            transition: 0.2s;
        }
        .quick-btn:hover { background: #00ff66; color: #010204; box-shadow: 0 0 12px #00ff66; }

        textarea { 
            width: 96%; 
            height: 110px; 
            padding: 12px; 
            margin: 5px 0 15px 0; 
            border: 1px solid #004411; 
            border-radius: 4px; 
            background: #000803; 
            color: #00ff66; 
            font-family: 'Share Tech Mono', monospace; 
            font-size: 14px; 
        }
        textarea:focus { outline: none; border-color: #00ff66; box-shadow: 0 0 10px rgba(0,255,102,0.4); }
        
        button.analyze-btn { 
            background: #00aa44; 
            color: #010204; 
            border: none; 
            padding: 12px 25px; 
            border-radius: 4px; 
            cursor: pointer; 
            font-weight: bold; 
            font-size: 15px; 
            width: 100%; 
            letter-spacing: 2px; 
            text-transform: uppercase; 
            font-family: 'Share Tech Mono', monospace;
            transition: 0.2s; 
        }
        button.analyze-btn:hover { background: #00ff66; box-shadow: 0 0 20px rgba(0,255,102,0.8); }

        .alerts { margin-top: 20px; }
        .alert-box { padding: 15px; margin-bottom: 12px; border-radius: 4px; border-left: 5px solid; font-size: 14px; }
        .HIGH { background-color: rgba(255, 0, 0, 0.2); border-color: #ff3333; color: #ff9999; box-shadow: 0 0 15px rgba(255,0,0,0.3); animation: pulse 1.5s infinite; }
        .INFO { background-color: rgba(0, 255, 102, 0.1); border-color: #00ff66; color: #99ffbb; }

        @keyframes pulse {
            0% { opacity: 0.8; }
            50% { opacity: 1; box-shadow: 0 0 25px rgba(255,0,0,0.6); }
            100% { opacity: 0.8; }
        }

        /* AI Analysis Box */
        .ai-box {
            background: #001107;
            border: 1px dashed #00ff66;
            border-radius: 4px;
            padding: 15px;
            margin-top: 20px;
            box-shadow: 0 0 15px rgba(0,255,102,0.15);
        }
        .ai-box h4 { margin: 0 0 8px 0; color: #00ff66; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }
        .ai-box p { margin: 0; color: #aaffcc; font-size: 13px; line-height: 1.5; }

        /* Incident Response Plan Box */
        .ir-plan {
            background: #060101;
            border: 1px solid #ff3333;
            border-radius: 4px;
            padding: 15px;
            margin-top: 15px;
            box-shadow: 0 0 15px rgba(255,51,51,0.2);
        }
        .ir-plan h4 { margin: 0 0 10px 0; color: #ff3333; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }
        .ir-plan ul { margin: 0; padding-left: 18px; color: #ffcccc; font-size: 13px; }
        .ir-plan li { margin-bottom: 5px; }
    </style>
    <script>
        function loadBruteForce() {
            document.getElementById('logInput').value = 
                '192.168.1.105 - - [12/Oct/2026:10:15:22] "POST /login HTTP/1.1" 401 232 Login failed for user admin\\n' +
                '192.168.1.105 - - [12/Oct/2026:10:15:25] "POST /login HTTP/1.1" 401 232 Login failed for user admin\\n' +
                '192.168.1.105 - - [12/Oct/2026:10:15:28] "POST /login HTTP/1.1" 401 232 Login failed for user root';
        }
        function loadCleanTraffic() {
            document.getElementById('logInput').value = 
                '192.168.1.20 - - [12/Oct/2026:12:00:00] "GET /index.html HTTP/1.1" 200 1024\\n' +
                '192.168.1.25 - - [12/Oct/2026:12:01:05] "GET /about HTTP/1.1" 200 512';
        }
    </script>
</head>
<body>

    <!-- Live Threat Feed Ticker -->
    <div class="ticker-wrap">
        <div class="ticker">
            <span class="ticker-item">🚨 [LIVE FEED]: BRUTE FORCE ATTEMPT DETECTED ON PORT 443</span>
            <span class="ticker-item">⚠️ [SOC ADVISORY]: HIGH ANOMALY TRAFFIC DETECTED FROM EXTERNAL SUBNET</span>
            <span class="ticker-item">🛡️ [FIREWALL]: AUTOMATED IP BLACKLISTING ENGAGED</span>
            <span class="ticker-item">⚡ [SYSTEM]: SIEM ENGINE RUNNING AT 100% EFFICIENCY</span>
        </div>
    </div>

    <div class="container">
        <h2>⚡ ADVANCED MINI SIEM & THREAT INTEL ⚡</h2>
        <div class="subtitle">[ SECURE OPERATIONS CENTER // AUTONOMOUS INCIDENT RESPONSE ]</div>

        <!-- Dashboard Stats -->
        <div class="stats-grid">
            <div class="stat-card">
                <span>Total Logs Processed</span>
                <strong>{{ total_logs }}</strong>
            </div>
            <div class="stat-card">
                <span>Critical Threats</span>
                <strong style="color: #ff3333; text-shadow: 0 0 8px rgba(255,51,51,0.6);">{{ high_count }}</strong>
            </div>
            <div class="stat-card">
                <span>Unique Source IPs</span>
                <strong>{{ unique_ips }}</strong>
            </div>
        </div>

        <!-- Incident Timeline -->
        <div class="timeline-box">
            <div class="timeline-title">📊 ANOMALY DETECTION TIMELINE</div>
            <div class="timeline-steps">
                <div class="step {% if high_count > 0 %}active{% endif %}">10:15:22<br>[Probe Initiated]</div>
                <div class="step {% if high_count > 0 %}active{% endif %}">10:15:25<br>[Multiple 401s]</div>
                <div class="step {% if high_count > 0 %}active{% endif %}">10:15:28<br>[Threshold Exceeded]</div>
                <div class="step {% if high_count > 0 %}active{% endif %}">10:15:28<br>[HIGH ALERT TRIGGERED]</div>
            </div>
        </div>

        <form method="POST">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <label style="font-size: 12px; color: #00aa44; letter-spacing: 1px;">LOG INGESTION STREAM:</label>
                <div class="quick-actions">
                    <button type="button" class="quick-btn" onclick="loadBruteForce()">⚡ Sim Brute Force</button>
                    <button type="button" class="quick-btn" onclick="loadCleanTraffic()">🌐 Sim Clean Traffic</button>
                </div>
            </div>
            
            <textarea id="logInput" name="logs">{{ logs }}</textarea>
            <br>
            <button type="submit" class="analyze-btn">Execute AI Threat Analysis</button>
        </form>

        {% if alerts %}
        <div class="alerts">
            <div style="font-size: 12px; color: #00ff66; font-weight: bold; margin-bottom: 8px; letter-spacing: 1px;">SECURITY ALERTS & ANOMALIES:</div>
            {% for alert in alerts %}
                <div class="alert-box {{ alert.level }}">
                    <strong>[{{ alert.level }}]</strong> {{ alert.message }}
                </div>
            {% endfor %}
        </div>

        <!-- AI Threat Intelligence Summary Box -->
        <div class="ai-box">
            <h4>🤖 AI Security Analyst Summary</h4>
            <p>
                {% if high_count > 0 %}
                The behavioral analysis engine has flagged high-frequency authentication failures indicative of automated credential stuffing or brute-force enumeration. Immediate isolation of the source IP is recommended to prevent unauthorized privilege escalation.
                {% else %}
                Traffic stream analyzed successfully. No anomalous patterns, unauthorized access signatures, or brute-force vectors were identified. System operates within normal baseline parameters.
                {% endif %}
            </p>
        </div>

        {% if high_count > 0 %}
        <!-- Recommended Incident Response Plan -->
        <div class="ir-plan">
            <h4>🚨 MANDATORY INCIDENT RESPONSE (IR) PROTOCOL</h4>
            <ul>
                <li><strong>Containment:</strong> Blackhole / Block attacking IP address via Edge Firewall.</li>
                <li><strong>Forensics:</strong> Audit adjacent server timestamps for payload execution or data exfiltration.</li>
                <li><strong>Remediation:</strong> Enforce strict rate-limiting and IP throttling rules on login endpoints.</li>
            </ul>
        </div>
        {% endif %}
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    default_logs = "192.168.1.105 - - [12/Oct/2026:10:15:22] \"POST /login HTTP/1.1\" 401 232 Login failed for user admin\n192.168.1.105 - - [12/Oct/2026:10:15:25] \"POST /login HTTP/1.1\" 401 232 Login failed for user admin\n192.168.1.105 - - [12/Oct/2026:10:15:28] \"POST /login HTTP/1.1\" 401 232 Login failed for user root"
    logs = default_logs
    alerts = []
    total_logs = 3
    high_count = 1
    unique_ips = 1

    if request.method == "POST":
        logs = request.form.get("logs", "")
        ip_attempts = {}
        lines = [line for line in logs.strip().split('\n') if line.strip()]
        total_logs = len(lines)
        
        all_ips = set()
        for line in lines:
            ip_match = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
            if ip_match:
                ip = ip_match.group()
                all_ips.add(ip)
                if "fail" in line.lower() or "unauthorized" in line.lower() or "401" in line:
                    ip_attempts[ip] = ip_attempts.get(ip, 0) + 1

        unique_ips = len(all_ips)
        
        for ip, count in ip_attempts.items():
            if count >= 2:
                alerts.append({
                    "level": "HIGH", 
                    "message": f"Critical Brute Force Vector identified from IP: {ip} ({count} failed authentication attempts)"
                })
            else:
                alerts.append({
                    "level": "INFO", 
                    "message": f"Anomaly notice: Unusual request pattern from IP: {ip}"
                })
                
        high_count = len([a for a in alerts if a["level"] == "HIGH"])
        
        if not alerts and logs.strip():
            alerts.append({"level": "INFO", "message": "System check clean. No malicious intrusion signatures detected."})

    return render_template_string(HTML_TEMPLATE, logs=logs, alerts=alerts, total_logs=total_logs, high_count=high_count, unique_ips=unique_ips)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
