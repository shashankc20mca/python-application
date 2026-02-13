from flask import Flask, render_template_string
import os
import socket
import datetime
import platform
import time as pytime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>DevOps Kubernetes Demo By shashank c</title>
  <style>
    :root{
      --bg1:#0b1220;
      --bg2:#0f2a3d;
      --card:#0e1a2b;
      --card2:#0b1626;
      --text:#eaf2ff;
      --muted:#a9bbd6;
      --accent:#58d7ff;
      --accent2:#8b5cf6;
      --good:#22c55e;
      --warn:#f59e0b;
      --shadow: 0 16px 40px rgba(0,0,0,.45);
      --border: 1px solid rgba(255,255,255,.10);
    }

    *{ box-sizing:border-box; }
    body{
      margin:0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      color:var(--text);
      background:
        radial-gradient(1200px 600px at 20% 10%, rgba(88,215,255,.20), transparent 55%),
        radial-gradient(900px 500px at 80% 20%, rgba(139,92,246,.20), transparent 55%),
        linear-gradient(135deg, var(--bg1), var(--bg2));
      min-height:100vh;
      overflow-x:hidden;
    }

    .wrap{ max-width:1100px; margin:0 auto; padding:40px 18px 60px; }

    .topbar{
      display:flex; align-items:center; justify-content:space-between;
      gap:12px; margin-bottom:22px;
    }
    .brand{
      display:flex; align-items:center; gap:12px;
    }
    .logo{
      width:44px; height:44px; border-radius:14px;
      background: linear-gradient(135deg, rgba(88,215,255,.95), rgba(139,92,246,.95));
      box-shadow: 0 12px 26px rgba(88,215,255,.18);
      display:grid; place-items:center;
      font-weight:800; color:#07111c;
      letter-spacing:.5px;
    }
    .title h1{ margin:0; font-size:18px; letter-spacing:.2px; }
    .title p{ margin:2px 0 0; color:var(--muted); font-size:13px; }

    .actions{ display:flex; gap:10px; flex-wrap:wrap; justify-content:flex-end; }
    .btn{
      border:var(--border);
      background: rgba(255,255,255,.06);
      color:var(--text);
      padding:10px 14px;
      border-radius:12px;
      cursor:pointer;
      font-weight:600;
      transition: .2s ease;
      display:flex; align-items:center; gap:8px;
      backdrop-filter: blur(8px);
    }
    .btn:hover{ transform: translateY(-1px); background: rgba(255,255,255,.10); }
    .btn.primary{
      border: none;
      background: linear-gradient(135deg, rgba(88,215,255,.95), rgba(139,92,246,.95));
      color:#07111c;
      box-shadow: 0 14px 30px rgba(139,92,246,.16);
    }

    .hero{
      border:var(--border);
      background: linear-gradient(135deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
      border-radius:22px;
      box-shadow: var(--shadow);
      padding:26px 22px;
      position:relative;
      overflow:hidden;
      margin-bottom:18px;
    }
    .hero:before{
      content:"";
      position:absolute; inset:-2px;
      background:
        radial-gradient(700px 220px at 20% 20%, rgba(88,215,255,.18), transparent 60%),
        radial-gradient(700px 240px at 80% 30%, rgba(139,92,246,.18), transparent 60%);
      pointer-events:none;
      filter: blur(6px);
    }
    .hero-inner{ position:relative; display:flex; gap:18px; flex-wrap:wrap; align-items:flex-start; justify-content:space-between; }
    .hero-left{ min-width:260px; flex:1; }
    .hero-left h2{ margin:0 0 8px; font-size:26px; }
    .hero-left p{ margin:0; color:var(--muted); line-height:1.45; }

    .chips{ display:flex; flex-wrap:wrap; gap:8px; margin-top:14px; }
    .chip{
      border:var(--border);
      background: rgba(0,0,0,.18);
      color: var(--text);
      padding:8px 10px;
      border-radius:999px;
      font-size:13px;
      display:flex; align-items:center; gap:8px;
    }
    .dot{
      width:10px; height:10px; border-radius:999px;
      background: var(--accent);
      box-shadow: 0 0 0 4px rgba(88,215,255,.15);
    }
    .dot.purple{ background: var(--accent2); box-shadow: 0 0 0 4px rgba(139,92,246,.15); }
    .dot.green{ background: var(--good); box-shadow: 0 0 0 4px rgba(34,197,94,.15); }
    .dot.orange{ background: var(--warn); box-shadow: 0 0 0 4px rgba(245,158,11,.15); }

    .status-card{
      min-width:280px;
      border:var(--border);
      background: rgba(0,0,0,.25);
      border-radius:18px;
      padding:16px 16px;
      flex:0 0 auto;
      backdrop-filter: blur(10px);
    }
    .kpi{ display:flex; justify-content:space-between; gap:14px; }
    .kpi .label{ color:var(--muted); font-size:12px; }
    .kpi .value{ font-size:16px; font-weight:800; margin-top:2px; }
    .badge{
      display:inline-flex; align-items:center; gap:8px;
      border-radius:999px;
      padding:8px 10px;
      background: rgba(34,197,94,.14);
      border: 1px solid rgba(34,197,94,.35);
      font-weight:700;
    }
    .pulse{
      width:10px; height:10px; border-radius:999px; background:var(--good);
      box-shadow: 0 0 0 0 rgba(34,197,94,.55);
      animation: pulse 1.6s infinite;
    }
    @keyframes pulse{
      0%{ box-shadow: 0 0 0 0 rgba(34,197,94,.45); }
      70%{ box-shadow: 0 0 0 10px rgba(34,197,94,0); }
      100%{ box-shadow: 0 0 0 0 rgba(34,197,94,0); }
    }

    .grid{
      display:grid;
      grid-template-columns: 1.2fr .8fr;
      gap:18px;
      margin-top:18px;
    }
    @media (max-width: 900px){
      .grid{ grid-template-columns: 1fr; }
    }

    .panel{
      border:var(--border);
      background: linear-gradient(135deg, rgba(255,255,255,.05), rgba(255,255,255,.02));
      border-radius:20px;
      box-shadow: var(--shadow);
      padding:18px;
      position:relative;
      overflow:hidden;
    }
    .panel h3{ margin:0 0 10px; font-size:16px; }
    .panel p{ margin:0; color:var(--muted); font-size:13px; line-height:1.5; }

    .kv{
      display:grid;
      grid-template-columns: 1fr 1fr;
      gap:12px;
      margin-top:12px;
    }
    @media (max-width: 520px){
      .kv{ grid-template-columns: 1fr; }
    }
    .kv .item{
      background: rgba(0,0,0,.22);
      border:var(--border);
      border-radius:14px;
      padding:12px 12px;
    }
    .kv .k{ color:var(--muted); font-size:12px; }
    .kv .v{ margin-top:4px; font-weight:800; font-size:14px; word-break:break-word; }

    .pipeline{
      display:flex; flex-direction:column; gap:10px; margin-top:12px;
    }
    .step{
      display:flex; align-items:center; gap:10px;
      padding:10px 12px;
      border-radius:14px;
      border:var(--border);
      background: rgba(0,0,0,.22);
    }
    .step .icon{
      width:34px; height:34px; border-radius:12px;
      display:grid; place-items:center;
      font-weight:900;
      background: rgba(88,215,255,.12);
      border: 1px solid rgba(88,215,255,.30);
      color: var(--accent);
      flex:0 0 auto;
    }
    .step .txt{ display:flex; flex-direction:column; }
    .step .txt b{ font-size:13px; }
    .step .txt span{ color:var(--muted); font-size:12px; margin-top:2px; }

    .foot{
      margin-top:18px;
      color: var(--muted);
      text-align:center;
      font-size:12px;
      opacity:.9;
    }
    a{ color: var(--accent); text-decoration:none; }
    a:hover{ text-decoration:underline; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="topbar">
      <div class="brand">
        <div class="logo">⚙️</div>
        <div class="title">
          <h1>DevOps Kubernetes Demo by shashank chandrashekar</h1>
          <p>Observability-ready UI • clean status • tech stack overview</p>
        </div>
      </div>

      <div class="actions">
        <button class="btn" onclick="window.location.href='/health'">🩺 Health</button>
        <button class="btn" onclick="copyInfo()">📋 Copy Pod Info</button>
        <button class="btn primary" onclick="window.location.reload()">🔄 Refresh</button>
      </div>
    </div>

    <div class="hero">
      <div class="hero-inner">
        <div class="hero-left">
          <h2>🚀 Running on Kubernetes by SHASHANK</h2>
          <p>
            This service is deployed as a containerized Flask app.
            It shows runtime metadata and highlights the DevOps stack used to build, ship, and operate workloads.
          </p>

          <div class="chips">
            <div class="chip"><span class="dot green"></span> CI/CD</div>
            <div class="chip"><span class="dot"></span> Kubernetes / EKS</div>
            <div class="chip"><span class="dot purple"></span> Docker</div>
            <div class="chip"><span class="dot orange"></span> Monitoring</div>
            <div class="chip"><span class="dot"></span> GitOps</div>
          </div>
        </div>

        <div class="status-card">
          <div class="kpi">
            <div>
              <div class="label">Service Status</div>
              <div class="value">
                <span class="badge"><span class="pulse"></span> Healthy</span>
              </div>
            </div>
            <div style="text-align:right;">
              <div class="label">Server Time</div>
              <div class="value" id="liveClock">{{ time }}</div>
            </div>
          </div>
          <div style="margin-top:12px; color:var(--muted); font-size:12px;">
            Tip: route this through Gateway API / Ingress and scale replicas to see Pod Name change on refresh.
          </div>
        </div>
      </div>
    </div>

    <div class="grid">
      <div class="panel">
        <h3>📦 Runtime & Pod Details</h3>
        <p>Useful for debugging deployments, scaling, and verifying which pod served the request.</p>

        <div class="kv" id="podInfo">
          <div class="item">
            <div class="k">Pod / Hostname</div>
            <div class="v">{{ hostname }}</div>
          </div>
          <div class="item">
            <div class="k">Namespace</div>
            <div class="v">{{ namespace }}</div>
          </div>
          <div class="item">
            <div class="k">Node</div>
            <div class="v">{{ node_name }}</div>
          </div>
          <div class="item">
            <div class="k">Cluster / Platform</div>
            <div class="v">{{ platform }}</div>
          </div>
          <div class="item">
            <div class="k">App Version</div>
            <div class="v">{{ app_version }}</div>
          </div>
          <div class="item">
            <div class="k">Uptime</div>
            <div class="v">{{ uptime }}</div>
          </div>
        </div>
      </div>

      <div class="panel">
        <h3>🛠️ DevOps Tech Stack</h3>
        <p>A quick overview of the delivery pipeline and platform components.</p>

        <div class="pipeline">
          <div class="step">
            <div class="icon">1</div>
            <div class="txt"><b>Source Control</b><span>GitHub / GitLab</span></div>
          </div>
          <div class="step">
            <div class="icon">2</div>
            <div class="txt"><b>CI Pipeline</b><span>Jenkins / GitHub Actions</span></div>
          </div>
          <div class="step">
            <div class="icon">3</div>
            <div class="txt"><b>Build & Registry</b><span>Docker + ECR / DockerHub</span></div>
          </div>
          <div class="step">
            <div class="icon">4</div>
            <div class="txt"><b>Deploy</b><span>Helm / Kustomize / Argo CD</span></div>
          </div>
          <div class="step">
            <div class="icon">5</div>
            <div class="txt"><b>Operate</b><span>Prometheus • Grafana • Loki • Alerts</span></div>
          </div>
        </div>

        <div style="margin-top:14px; font-size:12px; color:var(--muted);">
          Footer Text: <b>{{ footer }}</b>
        </div>
      </div>
    </div>

    <div class="foot">
      {{ footer }} • <a href="/health">/health</a>
    </div>
  </div>

  <script>
    // Live clock (client-side) + copy pod info helper
    function tickClock(){
      const el = document.getElementById("liveClock");
      if(!el) return;
      const now = new Date();
      const pad = (n)=> String(n).padStart(2,'0');
      const s = now.getFullYear()+"-"+pad(now.getMonth()+1)+"-"+pad(now.getDate())+" "
              + pad(now.getHours())+":"+pad(now.getMinutes())+":"+pad(now.getSeconds());
      el.textContent = s;
    }
    setInterval(tickClock, 1000);

    function copyInfo(){
      const pod = "{{ hostname }}";
      const ns  = "{{ namespace }}";
      const node = "{{ node_name }}";
      const ver = "{{ app_version }}";
      const txt = `pod=${pod}\\nnamespace=${ns}\\nnode=${node}\\nversion=${ver}`;
      navigator.clipboard.writeText(txt).then(()=>{
        alert("Pod info copied to clipboard ✅");
      }).catch(()=>{
        alert("Couldn't copy (browser blocked).");
      });
    }
  </script>
</body>
</html>
"""

APP_START = pytime.time()

@app.route("/")
def home():
    hostname = socket.gethostname()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Common k8s downward API env vars (set these in your Deployment)
    namespace = os.getenv("POD_NAMESPACE", os.getenv("KUBERNETES_NAMESPACE", "default"))
    node_name = os.getenv("NODE_NAME", "unknown")
    app_version = os.getenv("APP_VERSION", "v1.0.0")

    uptime_seconds = int(pytime.time() - APP_START)
    uptime = str(datetime.timedelta(seconds=uptime_seconds))

    footer = os.getenv("FOOTER_TEXT", "Running on EKS Fargate with Gateway API")

    return render_template_string(
        HTML_TEMPLATE,
        hostname=hostname,
        time=current_time,
        namespace=namespace,
        node_name=node_name,
        platform=f"{platform.system()} {platform.release()}",
        app_version=app_version,
        uptime=uptime,
        footer=footer
    )

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
