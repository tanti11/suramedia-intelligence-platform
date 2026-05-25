import streamlit as st
import base64

# 1. Mengatur konfigurasi halaman Streamlit agar memenuhi layar (Wide Mode)
st.set_page_config(
    page_title="SuraMedia Intelligence Platform",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed" # Menyembunyikan sidebar bawaan Streamlit
)

st.markdown("""
    <style>
        /* Menghilangkan padding bawaan container Streamlit */
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
        /* Menghilangkan border default pada iframe */
        iframe {
            border: none;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)


# 2. Menyimpan seluruh kode HTML, CSS Cerah, dan JS Premium ke dalam variabel string
html_code = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SuraMedia Intelligence Platform</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg: #f8fafc;
  --surface: #ffffff;
  --surface2: #f1f5f9;
  --border: #e2e8f0;
  --border-mid: #cbd5e1;
  --blue-500: #1d4ed8;
  --blue-400: #2563eb;
  --blue-300: #3b82f6;
  --blue-200: #60a5fa;
  --blue-50:  #eff6ff;
  --accent:   #0ea5e9;
  --text-main: #0f172a;
  --text-muted: #64748b;
  --text-dim: #94a3b8;
  --green:    #10b981;
  --green-lt: #d1fae5;
  --red:      #ef4444;
  --red-lt:   #fee2e2;
  --amber:    #f59e0b;
  --amber-lt: #fef3c7;
  --sidebar-w: 210px;
  --topbar-h: 48px;
  --radius-sm: 4px;
  --radius:    8px;
  --radius-lg: 10px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow:    0 4px 12px rgba(15,23,42,0.04);
}

body {
  font-family: "Plus Jakarta Sans", sans-serif;
  background: var(--bg);
  color: var(--text-main);
  min-height: 100vh;
  display: flex;
  overflow-x: hidden;
  font-size: 13px;
  line-height: 1.4;
}

/* ──────────────────────────────────────────
   SIDEBAR (LIGHT VERSION)
────────────────────────────────────────── */
.sidebar {
  width: var(--sidebar-w);
  min-height: 100vh;
  background: var(--surface);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0; top: 0;
  z-index: 200;
}

.sidebar-brand {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.brand-title {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 16px;
  font-weight: 800;
  color: var(--blue-500);
  letter-spacing: -0.5px;
}

.sidebar-nav {
  flex: 1;
  padding: 12px 8px;
  overflow-y: auto;
}

.nav-section-label {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--text-dim);
  padding: 0 8px;
  margin-bottom: 4px;
  margin-top: 12px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border-radius: var(--radius);
  cursor: pointer;
  transition: all 0.15s ease;
  color: var(--text-muted);
  font-size: 12.5px;
  font-weight: 500;
  margin-bottom: 1px;
  position: relative;
  user-select: none;
}

.nav-item svg {
  width: 15px; height: 15px;
  flex-shrink: 0;
  stroke-width: 2;
  transition: all 0.15s;
}

.nav-item:hover {
  background: var(--blue-50);
  color: var(--blue-500);
}

.nav-item.active {
  background: var(--blue-50);
  color: var(--blue-400);
  font-weight: 600;
  border: 1px solid rgba(37,99,235,0.15);
}

.nav-badge {
  margin-left: auto;
  font-size: 9px;
  font-weight: 700;
  background: var(--blue-400);
  color: white;
  padding: 1px 5px;
  border-radius: 10px;
}
.nav-badge.new { background: linear-gradient(135deg, var(--accent), var(--blue-300)); }

.sidebar-footer {
  padding: 10px 8px;
  border-top: 1px solid var(--border);
}

.user-card {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  border-radius: var(--radius);
  background: var(--surface2);
}

.user-avatar {
  width: 28px; height: 28px;
  border-radius: 50%;
  background: var(--blue-400);
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 700; color: white;
}

.user-info { min-width: 0; }
.user-name { font-size: 11.5px; font-weight: 700; color: var(--text-main); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-role { font-size: 10px; color: var(--text-muted); }

/* ──────────────────────────────────────────
   MAIN LAYOUT & TOPBAR
────────────────────────────────────────── */
.main {
  margin-left: var(--sidebar-w);
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--bg);
}

.topbar {
  height: var(--topbar-h);
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  position: sticky; top: 0; z-index: 100;
}

.topbar-breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-muted);
}
.topbar-breadcrumb .current { color: var(--text-main); font-weight: 600; }

.topbar-right { display: flex; align-items: center; gap: 4px; }
.topbar-btn {
  width: 28px; height: 28px;
  border-radius: var(--radius-sm);
  background: var(--surface2);
  border: 1px solid var(--border);
  display: flex; align-items: center; justify-content: center;
  color: var(--text-muted); cursor: pointer;
}
.topbar-btn svg { width: 14px; height: 14px; }

.live-pill {
  display: flex; align-items: center; gap: 4px;
  font-size: 11px; font-weight: 600;
  color: var(--green); background: #e6f4ea;
  padding: 3px 8px; border-radius: 12px;
}
.live-dot {
  width: 5px; height: 5px; background: var(--green); border-radius: 50%;
  animation: blink 2s ease-in-out infinite;
}
@keyframes blink { 0%,100% { opacity:1; } 50% { opacity:0.4; } }

/* ──────────────────────────────────────────
   PAGE SECTIONS & CONTENT
────────────────────────────────────────── */
.page-section { display: none; padding: 14px 16px; }
.page-section.active { display: block; }

.page-header {
  display: flex; align-items: flex-end; justify-content: space-between;
  margin-bottom: 12px;
}
.page-title { font-size: 16px; font-weight: 800; color: var(--text-main); letter-spacing: -0.3px; }
.page-subtitle { font-size: 11.5px; color: var(--text-muted); margin-top: 1px; }

.btn {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 6px 12px; border-radius: var(--radius);
  font-size: 11.5px; font-weight: 600; cursor: pointer; border: none;
}
.btn-primary { background: var(--blue-400); color: white; }
.btn-primary:hover { background: var(--blue-500); }
.btn-ghost { background: var(--surface2); border: 1px solid var(--border); color: var(--text-muted); }
.btn svg { width: 13px; height: 13px; }

/* STAT STRIP */
.stat-strip {
  display: flex; gap: 4px; padding: 6px 16px;
  border-bottom: 1px solid var(--border); background: var(--surface);
}
.stat-chip {
  display: flex; align-items: center; gap: 4px; padding: 3px 8px;
  border-radius: 12px; background: var(--surface2); border: 1px solid var(--border);
  font-size: 11px; font-weight: 600;
}
.chip-dot { width: 5px; height: 5px; border-radius: 50%; }
.chip-val { color: var(--text-main); }
.chip-lbl { color: var(--text-muted); font-weight: 400; }

/* ──────────────────────────────────────────
   KPI CARDS
────────────────────────────────────────── */
.kpi-row {
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: 10px; margin-bottom: 12px;
}
.kpi-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius-lg); padding: 12px 14px; box-shadow: var(--shadow-sm);
}
.kpi-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.kpi-icon-wrap { width: 30px; height: 30px; border-radius: var(--radius); display: flex; align-items: center; justify-content: center; }
.kpi-icon-wrap.blue  { background: var(--blue-50); color: var(--blue-400); }
.kpi-icon-wrap.green { background: #e6f4ea; color: var(--green); }
.kpi-icon-wrap.red   { background: #fce8e6; color: var(--red); }
.kpi-icon-wrap.amber { background: #fef3c7; color: var(--amber); }
.kpi-icon-wrap svg { width: 16px; height: 16px; }

.kpi-change { font-size: 11px; font-weight: 700; }
.kpi-change.up { color: var(--green); }
.kpi-change.down { color: var(--red); }

.kpi-value { font-size: 20px; font-weight: 800; color: var(--text-main); line-height: 1; margin-bottom: 2px; }
.kpi-label { font-size: 11px; color: var(--text-muted); font-weight: 500; margin-bottom: 8px; }
.kpi-bar { height: 3px; background: var(--surface2); border-radius: 2px; overflow: hidden; }
.kpi-bar-fill { height: 100%; border-radius: 2px; width: 0%; transition: width 1s ease-in-out; }

/* ──────────────────────────────────────────
   CHARTS & PANELS LAYOUT (COMPACT)
────────────────────────────────────────── */
.charts-row {
  display: grid; grid-template-columns: 1fr 260px;
  gap: 10px; margin-bottom: 12px;
}
.panel {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius-lg); overflow: hidden; display: flex; flex-direction: column;
}
.panel-header {
  padding: 10px 14px; border-bottom: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
}
.panel-title { font-size: 12px; font-weight: 700; color: var(--text-main); }
.panel-subtitle { font-size: 10.5px; color: var(--text-muted); }
.panel-body { padding: 12px 14px; flex: 1; }

.chart-tabs { display: flex; gap: 2px; background: var(--surface2); border-radius: var(--radius-sm); padding: 2px; }
.chart-tab { font-size: 10px; font-weight: 600; color: var(--text-muted); padding: 3px 8px; border-radius: 3px; cursor: pointer; }
.chart-tab.active { background: var(--surface); color: var(--blue-400); box-shadow: var(--shadow-sm); }

.chart-wrap { height: 150px; position: relative; }
.donut-wrap { position: relative; width: 110px; height: 110px; margin: 0 auto 10px; }
.donut-center { position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); text-align: center; }
.donut-center-value { font-size: 16px; font-weight: 800; color: var(--text-main); line-height: 1; }
.donut-center-label { font-size: 9px; color: var(--text-muted); }

.donut-legend { display: flex; flex-direction: column; gap: 4px; }
.donut-legend-item { display: flex; align-items: center; justify-content: space-between; font-size: 11px; }
.donut-legend-left { display: flex; align-items: center; gap: 6px; }
.legend-bar { width: 8px; height: 8px; border-radius: 2px; }
.legend-name { color: var(--text-muted); }
.legend-count { font-weight: 600; color: var(--text-main); }
.legend-pct { color: var(--text-muted); font-size: 10px; width: 32px; text-align: right; }

/* BOTTOM ROW (SOURCES & TABLE) */
.bottom-row { display: grid; grid-template-columns: 240px 1fr; gap: 10px; }

.source-list { display: flex; flex-direction: column; gap: 8px; }
.source-item-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px; }
.source-name { font-size: 11.5px; color: var(--text-main); font-weight: 600; }
.source-total { font-size: 11px; font-weight: 700; color: var(--text-muted); font-family: "JetBrains Mono", monospace; }
.source-bar { height: 5px; background: var(--surface2); border-radius: 3px; overflow: hidden; display: flex; }
.source-seg { height: 100%; }
.source-breakdown { display: flex; gap: 6px; margin-top: 2px; }
.src-mini { font-size: 9.5px; font-weight: 600; }

/* DATA TABLE CONTROLS & STYLE */
.table-controls {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 14px; border-bottom: 1px solid var(--border); gap: 10px;
}
.filter-tabs { display: flex; gap: 2px; }
.filter-tab {
  font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 12px;
  cursor: pointer; color: var(--text-muted);
}
.filter-tab.active { background: var(--blue-50); color: var(--blue-400); font-weight: 700; }

.search-box {
  display: flex; align-items: center; gap: 6px; background: var(--surface2);
  border: 1px solid var(--border); border-radius: var(--radius); padding: 4px 10px;
}
.search-box svg { width: 12px; height: 12px; color: var(--text-muted); }
.search-box input { background: none; border: none; outline: none; font-size: 11.5px; width: 140px; color: var(--text-main); }

.data-table { width: 100%; border-collapse: collapse; }
.data-table thead th {
  padding: 8px 12px; text-align: left; font-size: 10px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted);
  background: var(--surface2); border-bottom: 1px solid var(--border);
}
.data-table tbody tr { border-bottom: 1px solid var(--border); }
.data-table tbody tr:hover { background: var(--blue-50); }
.data-table tbody td { padding: 8px 12px; font-size: 11.5px; color: var(--text-main); vertical-align: middle; }

.td-id { font-family: "JetBrains Mono", monospace; color: var(--text-dim); }
.td-source { font-weight: 700; color: var(--blue-400); }
.td-title { max-width: 320px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-weight: 500; }
.td-score { font-family: "JetBrains Mono", monospace; font-weight: 600; }
.td-score.pos { color: var(--green); }
.td-score.neg { color: var(--red); }
.td-score.net { color: var(--text-muted); }

.badge { display: inline-flex; align-items: center; gap: 3px; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: 700; }
.badge-pos { background: #e6f4ea; color: var(--green); }
.badge-net { background: var(--surface2); color: var(--text-muted); }
.badge-neg { background: #fce8e6; color: var(--red); }
.badge-dot { width: 4px; height: 4px; border-radius: 50%; }
.badge-pos .badge-dot { background: var(--green); }
.badge-net .badge-dot { background: var(--text-muted); }
.badge-neg .badge-dot { background: var(--red); }

.table-footer { display: flex; align-items: center; justify-content: space-between; padding: 8px 14px; border-top: 1px solid var(--border); }
.table-info { font-size: 11px; color: var(--text-muted); }
.pagination { display: flex; gap: 3px; }
.pg {
  width: 24px; height: 24px; border-radius: var(--radius-sm); font-size: 11px; font-weight: 600;
  display: flex; align-items: center; justify-content: center; cursor: pointer;
  border: 1px solid var(--border); color: var(--text-muted); background: transparent;
}
.pg.active { background: var(--blue-400); border-color: var(--blue-400); color: white; }

.td-title-link {
  display: block;
  color: var(--text-main);
  text-decoration: none;
  font-weight: 500;
  font-size: 11.5px;
  line-height: 1.4;
  transition: color 0.15s;
}
.td-title-link:hover { color: var(--blue-400); text-decoration: underline; }
.td-source-inline {
  display: inline-block;
  font-size: 9.5px;
  font-weight: 700;
  color: var(--blue-400);
  background: var(--blue-50);
  border: 1px solid rgba(37,99,235,0.15);
  border-radius: 4px;
  padding: 1px 5px;
  margin-right: 5px;
  vertical-align: middle;
}

/* ── PRINT / EXPORT PDF ── */
@media print {
  body { background: white !important; display: block !important; }
  .sidebar, .topbar, .stat-strip, .table-controls,
  .table-footer, .page-header-right, .btn,
  .feature-pills, .chat-input-area { display: none !important; }
  .main { margin-left: 0 !important; }
  .page-section { display: block !important; padding: 0 !important; }
  .page-section#section-ai-chat { display: none !important; }
  .kpi-row { grid-template-columns: repeat(4,1fr) !important; }
  .charts-row, .bottom-row { grid-template-columns: 1fr !important; }
  .panel { break-inside: avoid; }
  canvas { max-height: 200px !important; }
  .page-title { font-size: 18px; }
  .print-header { display: block !important; }
}
.print-header {
  display: none;
  text-align: center; padding: 12px 0 4px;
  font-size: 20px; font-weight: 800; color: var(--blue-500);
}

/* ──────────────────────────────────────────
   AI CHAT INTERFACE (COMPACT LIGHT)
────────────────────────────────────────── */
.chat-container { display: flex; flex-direction: column; height: calc(100vh - 120px); background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); overflow: hidden; }
.chat-messages { flex: 1; padding: 14px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; background: var(--bg); }
.chat-bubble { max-width: 75%; padding: 8px 12px; border-radius: var(--radius-lg); font-size: 12.5px; line-height: 1.4; position: relative; }
.chat-bubble.user { background: var(--blue-400); color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
.chat-bubble.assistant { background: var(--surface); color: var(--text-main); align-self: flex-start; border-bottom-left-radius: 2px; border: 1px solid var(--border); box-shadow: var(--shadow-sm); }
.chat-input-area { padding: 10px; background: var(--surface); border-top: 1px solid var(--border); display: flex; gap: 8px; align-items: center; }
.chat-input { flex: 1; height: 32px; border: 1px solid var(--border); border-radius: var(--radius); padding: 0 12px; outline: none; font-size: 12px; background: var(--bg); }
.chat-input:focus { border-color: var(--blue-400); background: var(--surface); }

.feature-pills { display: flex; gap: 6px; padding: 6px 14px; background: var(--surface); border-bottom: 1px solid var(--border); overflow-x: auto; }
.feature-pill { padding: 4px 10px; background: var(--blue-50); border: 1px solid rgba(37,99,235,0.1); border-radius: 12px; font-size: 11px; color: var(--blue-400); font-weight: 600; cursor: pointer; white-space: nowrap; }
.feature-pill:hover { background: var(--blue-400); color: white; }

/* ──────────────────────────────────────────
   SETTINGS PANEL STYLE
────────────────────────────────────────── */
.settings-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.form-group { margin-bottom: 12px; }
.form-label { display: block; font-size: 11px; font-weight: 700; color: var(--text-muted); margin-bottom: 4px; text-transform: uppercase; }
.form-input { width: 100%; height: 34px; border: 1px solid var(--border); border-radius: var(--radius); padding: 0 10px; font-size: 12px; font-family: inherit; background: var(--bg); color: var(--text-main); outline: none; }
.form-input:focus { border-color: var(--blue-400); background: var(--surface); }
.sys-info-table { width: 100%; font-size: 12px; border-collapse: collapse; }
.sys-info-table td { padding: 6px 0; border-bottom: 1px solid var(--surface2); }
.sys-info-table td:first-child { font-weight: 600; color: var(--text-muted); width: 40%; }
.sys-info-table td:last-child { font-family: "JetBrains Mono", monospace; color: var(--text-main); text-align: right; }

/* ──────────────────────────────────────────
   FAQ SECTION
────────────────────────────────────────── */
.settings-section-title {
  font-size: 13px; font-weight: 800; color: var(--text-main);
  letter-spacing: -0.3px; margin: 18px 0 10px;
  display: flex; align-items: center; gap: 8px;
}
.settings-section-title svg { width: 15px; height: 15px; color: var(--blue-400); }
.settings-divider { height: 1px; background: var(--border); margin: 18px 0; }

.faq-list { display: flex; flex-direction: column; gap: 6px; }
.faq-item {
  border: 1px solid var(--border); border-radius: var(--radius-lg);
  overflow: hidden; background: var(--surface);
  transition: box-shadow 0.15s;
}
.faq-item:hover { box-shadow: var(--shadow); }
.faq-question {
  display: flex; align-items: center; justify-content: space-between;
  padding: 11px 14px; cursor: pointer; font-size: 12.5px; font-weight: 600;
  color: var(--text-main); user-select: none; gap: 10px;
}
.faq-question:hover { background: var(--blue-50); color: var(--blue-500); }
.faq-icon {
  width: 18px; height: 18px; flex-shrink: 0;
  border-radius: 50%; background: var(--blue-50);
  display: flex; align-items: center; justify-content: center;
  color: var(--blue-400); transition: transform 0.2s, background 0.2s;
}
.faq-icon svg { width: 10px; height: 10px; }
.faq-item.open .faq-icon { transform: rotate(180deg); background: var(--blue-400); color: white; }
.faq-answer {
  display: none; padding: 0 14px 12px;
  font-size: 12px; color: var(--text-muted); line-height: 1.6;
  border-top: 1px solid var(--surface2);
  background: var(--surface);
}
.faq-answer p { margin: 8px 0 0; }
.faq-answer code {
  background: var(--surface2); border: 1px solid var(--border);
  border-radius: 3px; padding: 0 5px; font-family: "JetBrains Mono", monospace;
  font-size: 11px; color: var(--blue-400);
}
.faq-item.open .faq-answer { display: block; }


</style>
</head>
<body>

  <aside class="sidebar">
    <div class="sidebar-brand">
      <div class="brand-title">SURAMEDIA</div>
    </div>
    <div class="sidebar-nav">
      <div class="nav-section-label">Main Menu</div>
      <div class="nav-item active" onclick="switchTab(this, 'section-dashboard')">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
        Dashboard <span class="nav-badge">Live</span>
      </div>
      <div class="nav-item" onclick="switchTab(this, 'section-ai-chat')">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        AI Chat <span class="nav-badge new">New</span>
      </div>
      <div class="nav-section-label">System</div>
      <div class="nav-item" onclick="switchTab(this, 'section-settings')">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1-4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
        Settings
      </div>
    </div>
    <div class="sidebar-footer">
      <div class="user-card">
        <div class="user-avatar">AD</div>
        <div class="user-info">
          <div class="user-name">Administrator</div>
          <div class="user-role">Analyst Level 1</div>
        </div>
      </div>
    </div>
  </aside>

  <div class="main">

    <div class="topbar">
      <div class="topbar-breadcrumb">
        <span>SuraMedia</span>
        <span>›</span>
        <span class="current" id="topbar-page-title">Dashboard</span>
      </div>
      <div class="topbar-right">
        <div class="live-pill"><div class="live-dot"></div>LIVE</div>
      </div>
    </div>

    <div class="stat-strip">
      <div class="stat-chip"><div class="chip-dot" style="background:var(--blue-400)"></div><span class="chip-val">6,305</span><span class="chip-lbl">Positif</span></div>
      <div class="stat-strip"></div>
      <div class="stat-chip"><div class="chip-dot" style="background:var(--text-muted)"></div><span class="chip-val">3,186</span><span class="chip-lbl">Netral</span></div>
      <div class="stat-chip"><div class="chip-dot" style="background:var(--red)"></div><span class="chip-val">3,363</span><span class="chip-lbl">Negatif</span></div>
      <div class="stat-chip" style="margin-left:auto"><div class="chip-dot" style="background:var(--amber)"></div><span class="chip-val">Jan 2025 – Mei 2026</span><span class="chip-lbl">Periode</span></div>
    </div>

    <section id="section-dashboard" class="page-section active">
      <div class="print-header">SuraMedia Intelligence Platform — Laporan Dashboard</div>
      <div class="page-header">
        <div>
          <div class="page-title">Media Intelligence Dashboard</div>
          <div class="page-subtitle">Analisis sentimen berita Kota Surabaya · NLP Pipeline · Dataset 12,854 artikel</div>
        </div>
        <div class="page-header-right">
          <button class="btn btn-ghost" onclick="exportPDF()">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
            Export PDF
          </button>
          <button class="btn btn-primary" onclick="location.reload()">Refresh Data</button>
        </div>
      </div>

      <div class="kpi-row">
        <div class="kpi-card">
          <div class="kpi-header">
            <div class="kpi-icon-wrap blue"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg></div>
            <div class="kpi-change up">▲ 14.2%</div>
          </div>
          <div class="kpi-value">12,854</div>
          <div class="kpi-label">Total Artikel Berita</div>
          <div class="kpi-bar"><div class="kpi-bar-fill" id="kb-total" style="background:var(--blue-400)"></div></div>
        </div>

        <div class="kpi-card">
          <div class="kpi-header">
            <div class="kpi-icon-wrap green"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/></svg></div>
            <div class="kpi-change up">▲ 8.4%</div>
          </div>
          <div class="kpi-value">6,305</div>
          <div class="kpi-label">Sentimen Positif</div>
          <div class="kpi-bar"><div class="kpi-bar-fill" id="kb-pos" style="background:var(--green)"></div></div>
        </div>

        <div class="kpi-card">
          <div class="kpi-header">
            <div class="kpi-icon-wrap blue"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="4" y1="9" x2="20" y2="9"/><line x1="4" y1="15" x2="20" y2="15"/></svg></div>
            <div class="kpi-change" style="color:var(--text-muted)">─ 0.0%</div>
          </div>
          <div class="kpi-value">3,186</div>
          <div class="kpi-label">Sentimen Netral</div>
          <div class="kpi-bar"><div class="kpi-bar-fill" id="kb-net" style="background:var(--text-muted)"></div></div>
        </div>

        <div class="kpi-card">
          <div class="kpi-header">
            <div class="kpi-icon-wrap red"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm12-7h3a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-3"/></svg></div>
            <div class="kpi-change down">▼ 2.1%</div>
          </div>
          <div class="kpi-value">3,363</div>
          <div class="kpi-label">Sentimen Negatif</div>
          <div class="kpi-bar"><div class="kpi-bar-fill" id="kb-neg" style="background:var(--red)"></div></div>
        </div>
      </div>

      <div class="charts-row">
        <div class="panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Tren Volume Isu & Sentimen Historis</div>
              <div class="panel-subtitle">Agregasi bulanan pergerakan opini publik</div>
            </div>
            <div class="chart-tabs">
              <div class="chart-tab active">Semua</div>
            </div>
          </div>
          <div class="panel-body">
            <div class="chart-wrap"><canvas id="lineChart"></canvas></div>
          </div>
        </div>

        <div class="panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Distribusi Sentimen</div>
              <div class="panel-subtitle">Komposisi data keseluruhan</div>
            </div>
          </div>
          <div class="panel-body">
            <div class="donut-wrap">
              <canvas id="donutChart" width="110" height="110"></canvas>
              <div class="donut-center">
                <div class="donut-center-value">12.8K</div>
                <div class="donut-center-label">Artikel</div>
              </div>
            </div>
            <div class="donut-legend">
              <div class="donut-legend-item">
                <div class="donut-legend-left">
                  <div class="legend-bar" style="background:#3b82f6"></div>
                  <div class="legend-name">Positif</div>
                </div>
                <div style="display:flex; gap:8px;">
                  <div class="legend-count">6.3K</div>
                  <div class="legend-pct">49.0%</div>
                </div>
              </div>
              <div class="donut-legend-item">
                <div class="donut-legend-left">
                  <div class="legend-bar" style="background:#64748b"></div>
                  <div class="legend-name">Netral</div>
                </div>
                <div style="display:flex; gap:8px;">
                  <div class="legend-count">3.1K</div>
                  <div class="legend-pct">24.8%</div>
                </div>
              </div>
              <div class="donut-legend-item">
                <div class="donut-legend-left">
                  <div class="legend-bar" style="background:#ef4444"></div>
                  <div class="legend-name">Negatif</div>
                </div>
                <div style="display:flex; gap:8px;">
                  <div class="legend-count">3.3K</div>
                  <div class="legend-pct">26.2%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bottom-row">
        <div class="panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Volume per Sumber Media</div>
              <div class="panel-subtitle">Komposisi sentimen tiap media</div>
            </div>
          </div>
          <div class="panel-body">
            <div class="source-list" id="source-list"></div>
          </div>
        </div>

        <div class="panel">
          <div class="table-controls">
            <div class="filter-tabs">
              <div class="filter-tab active" onclick="filterTable(this,'all')">Semua Berita</div>
              <div class="filter-tab" onclick="filterTable(this,'pos')">Positif</div>
              <div class="filter-tab" onclick="filterTable(this,'net')">Netral</div>
              <div class="filter-tab" onclick="filterTable(this,'neg')">Negatif</div>
            </div>
            <div class="search-box">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
              <input type="text" id="searchInput" placeholder="Cari judul berita atau media...">
            </div>
          </div>
          <div style="overflow-x:auto;">
            <table class="data-table">
              <thead>
                <tr>
                  <th style="width:40px">No</th>
                  <th style="width:100px">Tanggal</th>
                  <th>Judul Artikel Berita</th>
                  <th style="width:120px">Sentimen</th>
                </tr>
              </thead>
              <tbody id="tableBody"></tbody>
            </table>
          </div>
          <div class="table-footer">
            <div class="table-info" id="tableInfo">Menampilkan 0 dari 0 entri</div>
            <div class="pagination" id="tablePagination"></div>
          </div>
        </div>
      </div>
    </section>

    <section id="section-ai-chat" class="page-section">
      <div class="page-header">
        <div>
          <div class="page-title">SuraMedia AI Assistant</div>
          <div class="page-subtitle">Tanya jawab pintar berbasis data crawling real-time teks berita Surabaya</div>
        </div>
      </div>
      
      <div class="chat-container">
        <div class="feature-pills">
          <div class="feature-pill" data-prompt="Bagaimana tren isu infrastruktur di Surabaya akhir-akhir ini berdasarkan data yang ada?">Tren Infrastruktur</div>
          <div class="feature-pill" data-prompt="Topik apa yang paling banyak mendapat sentimen negatif dari berita-berita terbaru?">Topik Sentimen Negatif</div>
          <div class="feature-pill" data-prompt="Buatkan analisis perbandingan eksposur berita antara Detik.com, Jawapos, dan Antara Surabaya.">Detik vs Jawapos vs Antara</div>
        </div>
        <div class="chat-messages" id="chatBox">
          <div class="chat-bubble assistant">👋 Halo Admin! Saya SuraMedia AI. Silakan tanyakan analisis tren, ringkasan sentimen, atau peta persepsi publik dari artikel berita yang telah berhasil ditarik oleh sistem.</div>
        </div>
        <div class="chat-input-area">
          <input type="text" class="chat-input" id="chatInput" placeholder="Ketik pesan Anda ke SuraMedia AI...">
          <button class="btn btn-primary" id="btnSendChat" style="height:32px;">Kirim</button>
        </div>
      </div>
    </section>

    <section id="section-settings" class="page-section">
      <div class="page-header">
        <div>
          <div class="page-title">System Settings</div>
          <div class="page-subtitle">Konfigurasi API Key, Manajemen Data Pipeline, dan Status Platform</div>
        </div>
        <div class="page-header-right">
          <button class="btn btn-primary" onclick="saveSettings()">Simpan Konfigurasi</button>
        </div>
      </div>

      <div class="settings-grid">
        <div class="panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Integrasi API LLM</div>
              <div class="panel-subtitle">Konfigurasi kredensial untuk layanan SuraMedia AI</div>
            </div>
          </div>
          <div class="panel-body">
            <div class="form-group">
              <label class="form-label">Groq API Key</label>
              <input type="password" class="form-input" id="settingApiKey" placeholder="gsk_...">
            </div>
            <div class="form-group">
              <label class="form-label">Model Engine</label>
              <input type="text" class="form-input" value="llama-3.1-8b-instant" readonly style="background:var(--surface2); color:var(--text-muted); cursor:not-allowed;">
            </div>
          </div>
        </div>

        <div class="panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Informasi Sistem</div>
              <div class="panel-subtitle">Status dan spesifikasi runtime platform saat ini</div>
            </div>
          </div>
          <div class="panel-body">
            <table class="sys-info-table">
              <tr>
                <td>Status Gateway</td>
                <td style="color:var(--green); font-weight:700;">CONNECTED</td>
              </tr>
              <tr>
                <td>Pipeline Crawler</td>
                <td style="color:var(--blue-400); font-weight:700;">IDLE (SCHEDULER ACTIVE)</td>
              </tr>
              <tr>
                <td>Database Engine</td>
                <td>SQLite3 v3.45</td>
              </tr>
              <tr>
                <td>Framework Core</td>
                <td>Streamlit Wide-Frame Context</td>
              </tr>
            </table>
          </div>
        </div>
      </div>

      <!-- DIVIDER -->
      <div class="settings-divider"></div>

      <!-- FAQ SECTION -->
      <div class="settings-section-title">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        Frequently Asked Questions
      </div>

      <div class="faq-list">

        <div class="faq-item" onclick="toggleFaq(this)">
          <div class="faq-question">
            Bagaimana cara memperbarui Groq API Key saya?
            <div class="faq-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></div>
          </div>
          <div class="faq-answer">
            <p>Masukkan API Key baru pada kolom <code>Groq API Key</code> di panel <strong>Integrasi API LLM</strong> di atas, lalu klik tombol <strong>Simpan Konfigurasi</strong>. API Key yang baru akan langsung aktif untuk sesi AI Chat tanpa perlu me-reload halaman.</p>
            <p>API Key dapat diperoleh secara gratis di <code>console.groq.com</code> — daftarkan akun Groq Anda dan buat key baru di menu API Keys.</p>
          </div>
        </div>

        <div class="faq-item" onclick="toggleFaq(this)">
          <div class="faq-question">
            Apa itu Pipeline Crawler dan kapan data diperbarui?
            <div class="faq-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></div>
          </div>
          <div class="faq-answer">
            <p>Pipeline Crawler adalah komponen otomatis yang bertugas mengambil (scraping) artikel berita terbaru dari tiga sumber media: <strong>Detik.com</strong>, <strong>Jawapos</strong>, dan <strong>Antara Surabaya</strong> secara terjadwal.</p>
            <p>Status <code>IDLE (SCHEDULER ACTIVE)</code> berarti sistem standby dan akan aktif secara otomatis sesuai jadwal yang telah dikonfigurasi di backend. Dataset saat ini mencakup periode <strong>Januari 2025 – Mei 2026</strong> dengan total <strong>12.854 artikel</strong>.</p>
          </div>
        </div>

        <div class="faq-item" onclick="toggleFaq(this)">
          <div class="faq-question">
            Bagaimana cara kerja klasifikasi sentimen NLP di platform ini?
            <div class="faq-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></div>
          </div>
          <div class="faq-answer">
            <p>Setiap artikel yang berhasil di-crawl diproses melalui pipeline NLP (Natural Language Processing) berbasis model transformer. Sistem mengklasifikasikan sentimen ke dalam tiga kategori:</p>
            <p><strong>Positif</strong> — pemberitaan yang mengandung nada optimistis, apresiasi, atau keberhasilan program kota.</p>
            <p><strong>Netral</strong> — pemberitaan informatif tanpa kecenderungan emosi tertentu.</p>
            <p><strong>Negatif</strong> — pemberitaan yang mengandung keluhan, kritik, atau peristiwa yang merugikan warga.</p>
          </div>
        </div>

        <div class="faq-item" onclick="toggleFaq(this)">
          <div class="faq-question">
            Mengapa AI Chat menampilkan peringatan "API Key tidak valid"?
            <div class="faq-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></div>
          </div>
          <div class="faq-answer">
            <p>Pesan ⚠️ <em>API Key Groq belum diatur atau tidak valid</em> muncul jika:</p>
            <p>• API Key dikosongkan atau belum diperbarui sejak pengaturan awal.</p>
            <p>• API Key telah kadaluarsa atau dicabut dari akun Groq Anda.</p>
            <p>• Terjadi gangguan koneksi ke server <code>api.groq.com</code>.</p>
            <p>Pastikan key diawali dengan <code>gsk_</code> dan paste ulang dengan benar tanpa spasi di awal/akhir.</p>
          </div>
        </div>

        <div class="faq-item" onclick="toggleFaq(this)">
          <div class="faq-question">
            Bagaimana cara mengekspor laporan dashboard ke PDF?
            <div class="faq-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></div>
          </div>
          <div class="faq-answer">
            <p>Buka halaman <strong>Dashboard</strong> dan klik tombol <strong>Export PDF</strong> di pojok kanan atas. Sistem akan membuka dialog print browser secara otomatis — pilih <strong>"Save as PDF"</strong> sebagai tujuan cetak.</p>
            <p>Layout laporan telah dioptimasi khusus untuk format cetak: sidebar, toolbar, dan elemen interaktif akan disembunyikan secara otomatis agar tampilan PDF bersih dan profesional.</p>
          </div>
        </div>

        <div class="faq-item" onclick="toggleFaq(this)">
          <div class="faq-question">
            Apakah data berita yang ditampilkan bersifat real-time?
            <div class="faq-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></div>
          </div>
          <div class="faq-answer">
            <p>Indikator <strong>LIVE</strong> di topbar menunjukkan bahwa koneksi platform ke database aktif dan siap menerima data terbaru dari scheduler. Namun, pembaruan data berita tergantung pada frekuensi crawling yang dikonfigurasi di backend (umumnya setiap beberapa jam sekali).</p>
            <p>Untuk memuat ulang data terbaru secara manual, klik tombol <strong>Refresh Data</strong> yang tersedia di halaman Dashboard.</p>
          </div>
        </div>

      </div>


    </section>

  <script>
    // DATASET TREND BULANAN
    const TREND = [
      {b:"2025-01",p:380,nt:210,ng:190}, {b:"2025-02",p:410,nt:195,ng:220},
      {b:"2025-03",p:490,nt:240,ng:180}, {b:"2025-04",p:430,nt:220,ng:290},
      {b:"2025-05",p:520,nt:260,ng:210}, {b:"2025-06",p:580,nt:230,ng:195},
      {b:"2025-07",p:495,nt:215,ng:310}, {b:"2025-08",p:610,nt:270,ng:240},
      {b:"2025-09",p:540,nt:290,ng:225}, {b:"2025-10",p:670,nt:245,ng:190},
      {b:"2025-11",p:590,nt:230,ng:260}, {b:"2025-12",p:640,nt:285,ng:230},
      {b:"2026-01",p:710,nt:310,ng:280}, {b:"2026-02",p:680,nt:290,ng:340},
      {b:"2026-03",p:790,nt:340,ng:310}, {b:"2026-04",p:820,nt:360,ng:295},
      {b:"2026-05",p:854,nt:386,ng:363}
    ];

    const SOURCES = [
      {n:"Detik.com",p:4200,nt:1650,ng:1400},
      {n:"Jawapos",p:3680,nt:1820,ng:1450},
      {n:"Antara Surabaya",p:2850,nt:1100,ng:704}
    ];

    // DATASET BERITA INDIVIDUAL — DI-EXTEND HINGGA 30 DATA UNTUK SETIAP SENTIMEN (TOTAL 90 ROWS)
    const ROWS = [
      // === DATA POSITIF (30 ITEMS) ===
      {tgl:"22 Mei 2026", s:"Detik.com", j:"Pemkot Surabaya Resmikan Terowongan TIJD Joyoboyo Guna Urai Kemacetan", st:"pos", url:"https://www.detik.com/jatim"},
      {tgl:"22 Mei 2026", s:"Jawapos", j:"Genangan Air di Kawasan Mayjen Sungkono Mulai Surut Pasca Pembersihan Saluran", st:"pos", url:"https://www.jawapos.com"},
      {tgl:"20 Mei 2026", s:"Antara Surabaya", j:"Triwulan I 2026, Nilai Investasi Asing Masuk Surabaya Meroket Tajam", st:"pos", url:"https://jatim.antaranews.com"},
      {tgl:"19 Mei 2026", s:"Detik.com", j:"Kunjungan Wisatawan ke Kota Tua Surabaya Alami Kenaikan Signifikan", st:"pos", url:"https://www.detik.com/jatim"},
      {tgl:"19 Mei 2026", s:"Jawapos", j:"Pemkot Surabaya Targetkan Zero Kemiskinan Ekstrem pada Akhir 2026", st:"pos", url:"https://www.jawapos.com"},
      {tgl:"18 Mei 2026", s:"Antara Surabaya", j:"Proyek Revitalisasi Taman Bungkul Surabaya Dimulai, Warga Sambut Antusias", st:"pos", url:"https://jatim.antaranews.com"},
      {tgl:"17 Mei 2026", s:"Jawapos", j:"Surabaya Raih Penghargaan Kota Smart City Terbaik Nasional 2026", st:"pos", url:"https://www.jawapos.com"},
      {tgl:"15 Mei 2026", s:"Detik.com", j:"Penyaluran Beasiswa Pemuda Tangguh Surabaya Tahap II Resmi Dibuka", st:"pos", url:"https://www.detik.com/jatim"},
      {tgl:"14 Mei 2026", s:"Antara Surabaya", j:"Pemerintah Kota Pastikan Stok Bahan Pangan Harian Aman Hingga Idul Adha", st:"pos", url:"https://jatim.antaranews.com"},
      {tgl:"12 Mei 2026", s:"Jawapos", j:"RSUD Soewandhie Tambah Fasilitas Kamar Operasi Canggih Tanpa Antrean", st:"pos", url:"https://www.jawapos.com"},
      {tgl:"10 Mei 2026", s:"Detik.com", j:"Gelaran Surabaya Great Expo 2026 Targetkan Transaksi Hingga Miliaran Rupiah", st:"pos", url:"https://www.detik.com/jatim"},
      {tgl:"09 Mei 2026", s:"Jawapos", j:"Transformasi Digital Kelurahan Surabaya Percepat Pengurusan KTP Dalam 10 Menit", st:"pos", url:"https://www.jawapos.com"},
      {tgl:"08 Mei 2026", s:"Antara Surabaya", j:"Pasar Turi Baru Gelar Promo Besar, Kunjungan Pembeli Naik Tiga Lipat", st:"pos", url:"https://jatim.antaranews.com"},
      {tgl:"06 Mei 2026", s:"Detik.com", j:"Sukses Reduksi Stunting, Kader Surabaya Hebat Dapat Apresiasi Khusus Wali Kota", st:"pos", url:"https://www.detik.com/jatim"},
      {tgl:"05 Mei 2026", s:"Jawapos", j:"Taman Hiburan Pantai Kenjeran Bersolek Guna Sambut Wisatawan Akhir Pekan", st:"pos", url:"https://www.jawapos.com"},
      {tgl:"03 Mei 2026", s:"Antara Surabaya", j:"Layanan Pintu Air Petekan Optimal Hambat Intrusi Air Laut ke Pemukiman", st:"pos", url:"https://jatim.antaranews.com"},
      {tgl:"02 Mei 2026", s:"Detik.com", j:"Gedung Balai Pemuda Jadi Pusat Ekosistem Kreatif Anak Muda Kreatif Surabaya", st:"pos", url:"https://www.detik.com/jatim"},
      {tgl:"01 Mei 2026", s:"Jawapos", j:"Pemkot Sediakan Bus Listrik Tambahan Rute Terminal Purabaya - ITS", st:"pos", url:"https://www.jawapos.com"},
      {tgl:"29 Apr 2026", s:"Antara Surabaya", j:"Pembangunan Box Culvert Lidah Kulon Rampung Lebih Cepat Dari Estimasi", st:"pos", url:"https://jatim.antaranews.com"},
      {tgl:"27 Apr 2026", s:"Detik.com", j:"Pemberdayaan UMKM Jahit Dolly Mampu Suplai Kebutuhan Seragam Nasional", st:"pos", url:"https://www.detik.com/jatim"},
      {tgl:"25 Apr 2026", s:"Jawapos", j:"Ratusan Taman Aktif Surabaya Terawat Asri Menjadi Destinasi Piknik Gratis", st:"pos", url:"https://www.jawapos.com"},
      {tgl:"23 Apr 2026", s:"Antara Surabaya", j:"Penerapan Kawasan Tanpa Rokok (KTR) di Kantor Pemerintahan Banjir Dukungan", st:"pos", url:"https://jatim.antaranews.com"},
      {tgl:"21 Apr 2026", s:"Detik.com", j:"Karnaval Budaya Hari Jadi Kota Surabaya (HJKS) Bakal Diikuti Delegasi Asing", st:"pos", url:"https://www.detik.com/jatim"},
      {tgl:"20 Apr 2026", s:"Jawapos", j:"Pemasangan Jaringan Penerangan Jalan Umum Baru Terangi Wilayah Surabaya Barat", st:"pos", url:"https://www.jawapos.com"},
      {tgl:"18 Apr 2026", s:"Antara Surabaya", j:"Satpol PP Humanis Gencarkan Edukasi Kamtibmas Tanpa Tindakan Kekerasan", st:"pos", url:"https://jatim.antaranews.com"},
      {tgl:"16 Apr 2026", s:"Detik.com", j:"Peluncuran Aplikasi WargaKu v3 Bikin Aduan Langsung Direspon OPD Terkait", st:"pos", url:"https://www.detik.com/jatim"},
      {tgl:"14 Apr 2026", s:"Jawapos", j:"Pemanfaatan Aset Lahan Tidur untuk Urban Farming Hasilkan Tonan Sayur Paroki", st:"pos", url:"https://www.jawapos.com"},
      {tgl:"12 Apr 2026", s:"Antara Surabaya", j:"Pemeriksaan Kesehatan Gratis Keliling Jangkau Lansia di Kawasan Prorakyat", st:"pos", url:"https://jatim.antaranews.com"},
      {tgl:"10 Apr 2026", s:"Detik.com", j:"Kondisi Sungai Kalimas Bersih, Komunitas Dayung Gelar Latihan Rutin", st:"pos", url:"https://www.detik.com/jatim"},
      {tgl:"08 Apr 2026", s:"Jawapos", j:"E-Subandono Sukses Integrasikan Pendataan Bansos Agar Tepat Sasaran", st:"pos", url:"https://www.jawapos.com"},

      // === DATA NEGATIF (30 ITEMS) ===
      {tgl:"21 Mei 2026", s:"Antara Surabaya", j:"Keluhan Warga Terkait Keterlambatan Pasokan Air Bersih PDAM di Rungkut", st:"neg", url:"https://jatim.antaranews.com"},
      {tgl:"20 Mei 2026", s:"Jawapos", j:"Kemacetan Parah Landa Jalan Ahmad Yani Akibat Truk Mogok di Jam Kerja", st:"neg", url:"https://www.jawapos.com"},
      {tgl:"18 Mei 2026", s:"Detik.com", j:"Banjir Rob Kembali Genangi Kawasan Pelabuhan Tanjung Perak Surabaya", st:"neg", url:"https://www.detik.com/jatim"},
      {tgl:"17 Mei 2026", s:"Antara Surabaya", j:"Tarif Angkutan Umum Kota Surabaya Naik, Penumpang Keluhkan Kebijakan", st:"neg", url:"https://jatim.antaranews.com"},
      {tgl:"15 Mei 2026", s:"Jawapos", j:"Pedagang Pasar Gubeng Keluhkan Kebocoran Atap Saat Diguyur Hujan Deras", st:"neg", url:"https://www.jawapos.com"},
      {tgl:"13 Mei 2026", s:"Detik.com", j:"Tumpukan Sampah Liar di Pinggir Jalan Benowo Timbulkan Bau Menyengat", st:"neg", url:"https://www.detik.com/jatim"},
      {tgl:"11 Mei 2026", s:"Antara Surabaya", j:"Warga Kenjeran Protes Proyek Galian Saluran Air Hambat Akses Masuk Toko", st:"neg", url:"https://jatim.antaranews.com"},
      {tgl:"09 Mei 2026", s:"Jawapos", j:"Lampu Merah Perempatan Kertajaya Mati, Lalu Lintas Semrawut Tanpa Petugas", st:"neg", url:"https://www.jawapos.com"},
      {tgl:"07 Mei 2026", s:"Detik.com", j:"Aksi Balap Liar Motor Resahkan Pengguna Jalan di Koridor Dharmahusada", st:"neg", url:"https://www.detik.com/jatim"},
      {tgl:"05 Mei 2026", s:"Antara Surabaya", j:"Harga Cabai Rawit di Pasar Wonokromo Melonjak Drastis Jelang Tengah Tahun", st:"neg", url:"https://jatim.antaranews.com"},
      {tgl:"04 Mei 2026", s:"Jawapos", j:"Plafon Selasar Fasilitas Umum Mulyorejo Ambrol, Korban Jiwa Nihil", st:"neg", url:"https://www.jawapos.com"},
      {tgl:"02 Mei 2026", s:"Detik.com", j:"Antrean Truk Kontainer Mengular di Kaliosman Picu Kepadatan Jalur Logistik", st:"neg", url:"https://www.detik.com/jatim"},
      {tgl:"30 Apr 2026", s:"Antara Surabaya", j:"Sistem Pembayaran Cashless Suroboyo Bus Sempat Error, Penumpang Terlantar", st:"neg", url:"https://jatim.antaranews.com"},
      {tgl:"28 Apr 2026", s:"Jawapos", j:"Jalan Berlubang di Sepanjang Jalur Kalianak Kembali Memakan Korban Pemotor", st:"neg", url:"https://www.jawapos.com"},
      {tgl:"26 Apr 2026", s:"Detik.com", j:"Pipa Distribusi Utama PDAM Bocor di Karangpilang, Pasokan Wilayah Selatan Macet", st:"neg", url:"https://www.detik.com/jatim"},
      {tgl:"24 Apr 2026", s:"Antara Surabaya", j:"Warga Mengeluh Sulit Dapatkan Blanko KTP-el Fisik di Beberapa Kecamatan", st:"neg", url:"https://jatim.antaranews.com"},
      {tgl:"22 Apr 2026", s:"Jawapos", j:"Parkir Liar Menjamur di Sekitar Kebun Binatang Surabaya Picu Tarif Nuthuk", st:"neg", url:"https://www.jawapos.com"},
      {tgl:"19 Apr 2026", s:"Detik.com", j:"Kondisi Halte Bus Eksisting di Sukolilo Terbengkalai dan Penuh Coretan Vandalisme", st:"neg", url:"https://www.detik.com/jatim"},
      {tgl:"17 Apr 2026", s:"Antara Surabaya", j:"Nelayan Bulak Sambat Penurunan Hasil Tangkapan Akibat Cuaca Buruk Ekstrem", st:"neg", url:"https://jatim.antaranews.com"},
      {tgl:"15 Apr 2026", s:"Jawapos", j:"Angkutan Feeder Wirawiri Tabrak Pembatas Jalan di Gunung Anyar Akibat Supir Mengantuk", st:"neg", url:"https://www.jawapos.com"},
      {tgl:"13 Apr 2026", s:"Detik.com", j:"Marak Pencurian Kabel Pembumian Fasilitas Penerangan Jalan di Area Surabaya Timur", st:"neg", url:"https://www.detik.com/jatim"},
      {tgl:"11 Apr 2026", s:"Antara Surabaya", j:"Pasar Loak Dupak Kebakaran, Kerugian Ditaksir Capai Ratusan Juta Rupiah", st:"neg", url:"https://jatim.antaranews.com"},
      {tgl:"09 Apr 2026", s:"Jawapos", j:"Genangan Air Setinggi 30cm Muncul di Citraland Akibat Hujan Intensitas Tinggi", st:"neg", url:"https://www.jawapos.com"},
      {tgl:"07 Apr 2026", s:"Detik.com", j:"Ditemukan Kerusakan Fasilitas Mainan Anak di Alun-Alun Surabaya Kurang Terawat", st:"neg", url:"https://www.detik.com/jatim"},
      {tgl:"05 Apr 2026", s:"Antara Surabaya", j:"Instalasi IPAL Komunal Kampung Sememi Rusak, Air Limbah Meluap ke Got", st:"neg", url:"https://jatim.antaranews.com"},
      {tgl:"03 Apr 2026", s:"Jawapos", j:"Sengketa Lahan Parkir Ruko Wonokromo Picu Keributan Antar Kelompok Pemuda", st:"neg", url:"https://www.jawapos.com"},
      {tgl:"01 Apr 2026", s:"Detik.com", j:"Aksi Klitih Remaja Meresahkan, Warga Minta Patroli Malam Ditingkatkan", st:"neg", url:"https://www.detik.com/jatim"},
      {tgl:"29 Mar 2026", s:"Antara Surabaya", j:"Kelangkaan Gas Elpiji 3 Kg Bersubsidi Terjadi di Wilayah Tambaksari", st:"neg", url:"https://jatim.antaranews.com"},
      {tgl:"27 Mar 2026", s:"Jawapos", j:"Akses Trotoar Rusak di Jalan Basuki Rahmat Dinilai Bahayakan Difabel", st:"neg", url:"https://www.jawapos.com"},
      {tgl:"25 Mar 2026", s:"Detik.com", j:"Saluran Air Tersumbat Sampah Plastik, Kawasan Klampis Kembali Tergenang", st:"neg", url:"https://www.detik.com/jatim"},

      // === DATA NETRAL (30 ITEMS) ===
      {tgl:"21 Mei 2026", s:"Detik.com", j:"DPRD Surabaya Gelar Rapat Paripurna Pembahasan Raperda Transportasi Publik", st:"net", url:"https://www.detik.com/jatim"},
      {tgl:"19 Mei 2026", s:"Antara Surabaya", j:"KPU Surabaya Mulai Lakukan Pemetaan TPS untuk Pilkada Serentak 2026", st:"net", url:"https://jatim.antaranews.com"},
      {tgl:"16 Mei 2026", s:"Jawapos", j:"Badan Pusat Statistik (BPS) Rilis Data Inflasi Bulanan Kota Surabaya", st:"net", url:"https://www.jawapos.com"},
      {tgl:"14 Mei 2026", s:"Detik.com", j:"Dinas Perhubungan Uji Coba Perubahan Arah Arus Lalu Lintas di Bundaran Dolog", st:"net", url:"https://www.detik.com/jatim"},
      {tgl:"12 Mei 2026", s:"Antara Surabaya", j:"Sidang Kasus Sengketa Tanah Kalisari Kembali Digelar di PN Surabaya", st:"net", url:"https://jatim.antaranews.com"},
      {tgl:"10 Mei 2026", s:"Jawapos", j:"Pertamina Melakukan Penyesuaian Harga BBM Non-Subsidi Berkala", st:"net", url:"https://www.jawapos.com"},
      {tgl:"08 Mei 2026", s:"Detik.com", j:"BMKG Juanda Prakirakan Cuaca Surabaya Cerah Berawan Sepanjang Hari Ini", st:"net", url:"https://www.detik.com/jatim"},
      {tgl:"06 Mei 2026", s:"Antara Surabaya", j:"Dinas Kesehatan Lakukan Fogging Rutin Antisipasi DBD di Pemukiman Tambak Wedi", st:"net", url:"https://jatim.antaranews.com"},
      {tgl:"04 Mei 2026", s:"Jawapos", j:"Pendaftaran PPDB Jalur Zonasi SMP Negeri Surabaya Segera Dibuka Bulan Depan", st:"net", url:"https://www.jawapos.com"},
      {tgl:"02 Mei 2026", s:"Detik.com", j:"Polrestabes Surabaya Lakukan Pengalihan Arus Terkait Demo Hari Buruh", st:"net", url:"https://www.detik.com/jatim"},
      {tgl:"30 Apr 2026", s:"Antara Surabaya", j:"Kunjungan Kerja Komisi C DPRD Kota Samarinda Pelajari Tata Ruang Surabaya", st:"net", url:"https://jatim.antaranews.com"},
      {tgl:"28 Apr 2026", s:"Jawapos", j:"Dinas Lingkungan Hidup Lakukan Perantingan Pohon Rawan Tumbang di Tegalsari", st:"net", url:"https://www.jawapos.com"},
      {tgl:"26 Apr 2026", s:"Detik.com", j:"Universitas Airlangga (Unair) Kukuhkan Tiga Guru Besar Baru Bidang Kesehatan", st:"net", url:"https://www.detik.com/jatim"},
      {tgl:"24 Apr 2026", s:"Antara Surabaya", j:"Kemenag Surabaya Sosialisasikan Jadwal Keberangkatan Kloter Haji Pertama", st:"net", url:"https://jatim.antaranews.com"},
      {tgl:"22 Apr 2026", s:"Jawapos", j:"Pemeriksaan Kelaikan Jalan (Ramp Check) Bus AKDP Digelar di Terminal Purabaya", st:"net", url:"https://www.jawapos.com"},
      {tgl:"20 Apr 2026", s:"Detik.com", j:"Manajemen Persebaya Gelar Rapat Evaluasi Peforma Tim Menuju Akhir Musim", st:"net", url:"https://www.detik.com/jatim"},
      {tgl:"18 Apr 2026", s:"Antara Surabaya", j:"Polda Jatim Musnahkan Barang Bukti Narkotika Hasil Operasi Pekat Pekan Lalu", st:"net", url:"https://jatim.antaranews.com"},
      {tgl:"16 Apr 2026", s:"Jawapos", j:"Pembangunan Box Culvert Babat Jerawat Memasuki Tahap Pemasangan Tulangan", st:"net", url:"https://www.jawapos.com"},
      {tgl:"14 Apr 2026", s:"Detik.com", j:"Dinas Ketahanan Pangan Gelar Gerakan Pangan Murah Berkala di Lapangan THOR", st:"net", url:"https://www.detik.com/jatim"},
      {tgl:"12 Apr 2026", s:"Antara Surabaya", j:"Pemkot Surabaya Gelar Seleksi Terbuka Jabatan Kepala Dinas Perindustrian", st:"net", url:"https://jatim.antaranews.com"},
      {tgl:"10 Apr 2026", s:"Jawapos", j:"Studi Banding Pemkab Badung Pelajari Pengelolaan Sampah Berbasis Energi di Benowo", st:"net", url:"https://www.jawapos.com"},
      {tgl:"08 Apr 2026", s:"Detik.com", j:"Klinik Pratama Pemkot Surabaya Beralih Ke Sistem Rekam Medis Elektronik Penuh", st:"net", url:"https://www.detik.com/jatim"},
      {tgl:"06 Apr 2026", s:"Antara Surabaya", j:"Dinas Sosial Lakukan Pemutakhiran Data Kemiskinan Terpadu Tingkat RT/RW", st:"net", url:"https://jatim.antaranews.com"},
      {tgl:"04 Apr 2026", s:"Jawapos", j:"Uji Coba Pembatasan Truk Masuk Jalur Protokol Jam Kerja Mulai Disosialisasikan", st:"net", url:"https://www.jawapos.com"},
      {tgl:"02 Apr 2026", s:"Detik.com", j:"Puskesmas Ketabang Buka Layanan Konseling Psikologi Remaja Dua Kali Seminggu", st:"net", url:"https://www.detik.com/jatim"},
      {tgl:"31 Mar 2026", s:"Antara Surabaya", j:"Kantor Imigrasi Tanjung Perak Deteksi Kenaikan Pembuatan Paspor Liburan", st:"net", url:"https://jatim.antaranews.com"},
      {tgl:"29 Mar 2026", s:"Jawapos", j:"Pemerintah Pusat Kaji Rencana Penambahan Koridor Commuter Line Surabaya Raya", st:"net", url:"https://www.jawapos.com"},
      {tgl:"27 Mar 2026", s:"Detik.com", j:"Dinas Pemadam Kebakaran Evakuasi Sarang Tawon Vespa di Atap Rumah Warga Ngagel", st:"net", url:"https://www.detik.com/jatim"},
      {tgl:"25 Mar 2026", s:"Antara Surabaya", j:"Satgas Kebersihan Lakukan Pengerukan Lumpur Rutin Saluran Air Blauran", st:"net", url:"https://jatim.antaranews.com"},
      {tgl:"23 Mar 2026", s:"Jawapos", j:"Rapat Koordinasi Lintas Sektor Bahas Pengamanan Jalur Protokol Surabaya", st:"net", url:"https://www.jawapos.com"}
    ];

    let currentFilter = 'all';
    let currentSearch = '';
    let currentPage = 1;
    const pageSize = 10; // Menampilkan 10 baris per halaman

    // INTERACTIVE TABS SIDEBAR
    const pageTitles = {
      'section-dashboard': 'Dashboard',
      'section-ai-chat': 'AI Chat',
      'section-settings': 'Settings'
    };
    window.switchTab = function(el, id) {
      document.querySelectorAll('.nav-item').forEach(x => x.classList.remove('active'));
      el.classList.add('active');
      document.querySelectorAll('.page-section').forEach(x => x.classList.remove('active'));
      document.getElementById(id).classList.add('active');
      document.getElementById('topbar-page-title').textContent = pageTitles[id] || id;
    }

    // EXPORT PDF
    function exportPDF() {
      const btn = document.querySelector('[onclick="exportPDF()"]');
      btn.textContent = 'Menyiapkan...';
      btn.disabled = true;
      setTimeout(() => {
        window.print();
        btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg> Export PDF';
        btn.disabled = false;
      }, 300);
    }
    window.exportPDF = exportPDF;

    // ANIMATE KPI BARS
    setTimeout(() => {
      document.getElementById("kb-total").style.width = "100%";
      document.getElementById("kb-pos").style.width = "49%";
      document.getElementById("kb-net").style.width = "24.8%";
      document.getElementById("kb-neg").style.width = "26.2%";
    }, 300);

    // RENDER MEDIA SOURCE BREAKDOWN DIAGRAM 
    const maxVol = Math.max(...SOURCES.map(s => s.p + s.nt + s.ng));
    document.getElementById("source-list").innerHTML = SOURCES.map(s => {
      const tot = s.p + s.nt + s.ng;
      const pctP = (s.p / tot * 100).toFixed(0);
      const pctNt = (s.nt / tot * 100).toFixed(0);
      const pctNg = (s.ng / tot * 100).toFixed(0);
      return `<div class="source-item">
        <div class="source-item-header">
          <span class="source-name">${s.n}</span>
          <span class="source-total">${tot.toLocaleString()} art</span>
        </div>
        <div class="source-bar">
          <div class="source-seg" style="width:${pctP}%;background:#3b82f6" title="Positif"></div>
          <div class="source-seg" style="width:${pctNt}%;background:#64748b" title="Netral"></div>
          <div class="source-seg" style="width:${pctNg}%;background:#ef4444" title="Negatif"></div>
        </div>
      </div>`;
    }).join('');

    // FILTER TABLE MANAGEMENT
    function filterTable(el, filter) {
      document.querySelectorAll(".filter-tab").forEach(x => x.classList.remove("active"));
      el.classList.add("active");
      currentFilter = filter;
      currentPage = 1; // Reset ke halaman pertama saat filter berubah
      renderTable();
    }
    window.filterTable = filterTable;

    document.getElementById("searchInput").addEventListener("input", function() {
      currentSearch = this.value.toLowerCase();
      currentPage = 1; // Reset ke halaman pertama saat melakukan pencarian
      renderTable();
    });

    // SISTEM PAGINATION AKTIF (FUNGSI UTAMA)
    function renderPagination(totalRows) {
      const pagContainer = document.getElementById("tablePagination");
      const totalPages = Math.ceil(totalRows / pageSize) || 1;
      
      let html = "";
      for (let i = 1; i <= totalPages; i++) {
        let activeClass = i === currentPage ? "active" : "";
        html += `<div class="pg ${activeClass}" onclick="goToPage(${i})">${i}</div>`;
      }
      pagContainer.innerHTML = html;
    }

    window.goToPage = function(pageNumber) {
      currentPage = pageNumber;
      renderTable();
    }

    // RE-RENDER TABLE BERDASARKAN FILTER, PENCARIAN & HALAMAN AKTIF
    function renderTable() {
      const tbody = document.getElementById("tableBody");
      
      // 1. Lakukan Filter Kategori dan Pencarian Teks
      const filteredRows = ROWS.filter(r => {
        const mFilter = currentFilter === 'all' || r.st === currentFilter;
        const mSearch = r.j.toLowerCase().includes(currentSearch) || r.s.toLowerCase().includes(currentSearch);
        return mFilter && mSearch;
      });

      // 2. Potong Data Sesuai Halaman Aktif (Pagination Slice)
      const start = (currentPage - 1) * pageSize;
      const end = start + pageSize;
      const paginatedRows = filteredRows.slice(start, end);

      // 3. Render Baris ke Dalam DOM Tabel
      if (paginatedRows.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; color:var(--text-muted); padding:20px;">Data berita tidak ditemukan</td></tr>`;
      } else {
        tbody.innerHTML = paginatedRows.map((r, index) => {
          let bc = r.st === 'pos' ? 'badge-pos' : (r.st === 'neg' ? 'badge-neg' : 'badge-net');
          let bl = r.st === 'pos' ? 'Positif' : (r.st === 'neg' ? 'Negatif' : 'Netral');
          let rowNum = start + index + 1; // Penomoran urut berkelanjutan
          return `<tr>
            <td class="td-id" style="text-align:center;font-weight:600">${rowNum}</td>
            <td style="font-size:11px;color:var(--text-muted);white-space:nowrap">${r.tgl}</td>
            <td>
              <a href="${r.url}" target="_blank" class="td-title-link" title="${r.j} — ${r.s}">
                <span class="td-source-inline">${r.s}</span>
                ${r.j}
              </a>
            </td>
            <td><span class="badge ${bc}"><span class="badge-dot"></span>${bl}</span></td>
          </tr>`;
        }).join("");
      }

      // 4. Update Informasi Entri di Footer Tabel Berdasarkan Total Data Riil
      let displayTotal = currentFilter === 'all' ? '12,854' : (currentFilter === 'pos' ? '6,305' : (currentFilter === 'net' ? '3,186' : '3,363'));
      document.getElementById("tableInfo").textContent = `Menampilkan ${start + 1}-${Math.min(end, filteredRows.length)} dari ${filteredRows.length} entri terfilter (Dataset Sistem: ${displayTotal})`;
      
      // 5. Bangun Kembali Navigasi Tombol Angka Pagination
      renderPagination(filteredRows.length);
    }
    
    // Inisialisasi awal tabel saat sistem load pertama kali
    renderTable();

    // CHART.JS PROJECTION LINE TREND BULANAN
    const labels = TREND.map(r => {
      const [y,m] = r.b.split("-");
      const nm = ["","Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"];
      return nm[+m] + (y==="2026" ? " '26" : "");
    });
    const lineCtx = document.getElementById("lineChart").getContext("2d");
    new Chart(lineCtx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          { label: "Positif", data: TREND.map(r=>r.p), borderColor: "#3b82f6", backgroundColor: "transparent", borderWidth: 2, tension: 0.35, pointRadius: 2 },
          { label: "Netral", data: TREND.map(r=>r.nt), borderColor: "#64748b", backgroundColor: "transparent", borderWidth: 1.5, tension: 0.35, pointRadius: 0 },
          { label: "Negatif", data: TREND.map(r=>r.ng), borderColor: "#ef4444", backgroundColor: "transparent", borderWidth: 2, tension: 0.35, pointRadius: 2 }
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false }, ticks: { font: { size: 9 }, color: "#64748b" } },
          y: { grid: { color: "#e2e8f0" }, ticks: { font: { size: 9 }, color: "#64748b" } }
        }
      }
    });

    // CHART.JS DONUT COMPOSITION
    const donutCtx = document.getElementById("donutChart").getContext("2d");
    new Chart(donutCtx, {
      type: "doughnut",
      data: {
        datasets: [{
          data: [6305, 3186, 3363],
          backgroundColor: ["#3b82f6", "#64748b", "#ef4444"],
          borderWidth: 2, borderColor: "#ffffff"
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false, cutout: "78%",
        plugins: { tooltip: { enabled: true }, legend: { display: false } }
      }
    });

    // INTEGRASI GROQ AI CHAT LIVE
    const chatBox = document.getElementById('chatBox');
    const chatInput = document.getElementById('chatInput');
    let GROQ_API_KEY = "INPUT_API_KEY_ANDA_DISINI"; 
    
    document.getElementById('settingApiKey').value = GROQ_API_KEY;

    function appendBubble(sender, text) {
      const bubble = document.createElement('div');
      bubble.className = `chat-bubble ${sender}`;
      bubble.innerHTML = text.split('\\n').join('<br>');
      chatBox.appendChild(bubble);
      chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function getGroqResponse(userPrompt) {
      const url = "https://api.groq.com/openai/v1/chat/completions";

      if (!GROQ_API_KEY || GROQ_API_KEY.trim() === "" || GROQ_API_KEY.includes("GANTI_DENGAN")) {
        return "⚠️ API Key Groq belum diatur atau tidak valid. Silakan buka menu System Settings untuk mengaturnya.";
      }

      const RingkasanMedia = SOURCES.map(s => `- ${s.n}: Positif ${s.p}, Netral ${s.nt}, Negatif ${s.ng}`).join('\\n');
      const RingkasanTabel = ROWS.slice(0, 10).map(r => `- [${r.s}] ${r.j} (Sentimen: ${r.st})`).join('\\n');

      const systemContext = `Kamu adalah SuraMedia AI, analis media profesional Kota Surabaya. Jawab pertanyaan user dengan sangat akurat berdasarkan data LIVE dari Dashboard berikut:\\n\\n[RINGKASAN UTAMA DASHBOARD]\\n- Total Artikel: 12.854 berita\\n- Komposisi Sentimen: Positif 49% (6.305), Netral 24.8% (3.186), Negatif 26.2% (3.363)\\n- Sumber Media: Hanya 3 platform — Detik.com, Jawapos, dan Antara Surabaya\\n- Isu Utama saat ini: Infrastruktur kota, kemacetan, fasilitas publik, dan layanan air bersih.\\n\\n[DATA SENTIMEN PER MEDIA]\\n${RingkasanMedia}\\n\\n[SAMPEL BEBERAPA ARTIKEL BERITA DI TABEL]\\n${RingkasanTabel}\\n\\nInstruksi: Jawablah secara analitis, profesional, dan ringkas dalam Bahasa Indonesia. Jika user bertanya tentang angka, perbandingan media, atau judul berita di tabel, berikan jawaban spesifik berdasarkan data di atas. Sumber berita HANYA dari Detik.com, Jawapos, dan Antara Surabaya — jangan menyebut media lain. Jika di luar data dashboard, gunakan wawasan analitis pintarmu sebagai AI.`;

      const payload = {
        model: "llama-3.1-8b-instant",
        messages: [
          { role: "system", content: systemContext },
          { role: "user", content: userPrompt }
        ],
        temperature: 0.7,
        max_tokens: 1024
      };

      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + GROQ_API_KEY
          },
          body: JSON.stringify(payload)
        });
        const data = await response.json();

        if (data.choices && data.choices.length > 0) {
          return data.choices[0].message.content;
        } else if (data.error) {
          return "⚠️ API Error dari Groq: " + data.error.message;
        } else {
          return "⚠️ Maaf, respons dari server Groq tidak terbaca.";
        }
      } catch (error) {
        return "⚠️ Terjadi kesalahan jaringan. Cek koneksi internet.";
      }
    }

    async function handleSendMessage(customText) {
      const text = customText || chatInput.value.trim();
      if (!text) return;

      appendBubble('user', text);
      if (!customText) chatInput.value = '';

      const loadingBubble = document.createElement('div');
      loadingBubble.className = 'chat-bubble assistant';
      loadingBubble.innerHTML = '<i>🤖 SuraMedia AI sedang menganalisis data...</i>';
      chatBox.appendChild(loadingBubble);
      chatBox.scrollTop = chatBox.scrollHeight;

      const reply = await getGroqResponse(text);

      chatBox.removeChild(loadingBubble);
      appendBubble('assistant', reply);
    }

    // FAQ ACCORDION TOGGLE
    window.toggleFaq = function(item) {
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(el => el.classList.remove('open'));
      if (!isOpen) item.classList.add('open');
    }

    // SIMPAN PENGATURAN (SETTINGS ACTION)
    window.saveSettings = function() {
      const inputKey = document.getElementById('settingApiKey').value.trim();
      if(inputKey === "") {
        alert("Gagal menyimpan: API Key tidak boleh kosong.");
        return;
      }
      GROQ_API_KEY = inputKey;
      alert("Konfigurasi Berhasil Disimpan! Kredensial AI runtime diperbarui.");
    }

    document.getElementById('btnSendChat').addEventListener('click', () => handleSendMessage());

    chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') handleSendMessage();
    });

    document.querySelectorAll('.feature-pill').forEach(pill => {
      pill.addEventListener('click', function() {
        const prompt = this.getAttribute('data-prompt');
        handleSendMessage(prompt);
      });
    });
  </script>
</body>
</html>
"""

# 3. Merender kode HTML secara aman ke dalam layout web Streamlit menggunakan st.iframe terbaru
encoded_html = base64.b64encode(html_code.encode('utf-8')).decode('utf-8')
st.iframe(f"data:text/html;base64,{encoded_html}", height=900)