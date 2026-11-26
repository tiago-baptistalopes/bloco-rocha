import base64

import streamlit as st
import streamlit.components.v1 as components

from bloco.data import FUNDS

ORANGE, GOLD, BEIGE, RULE = '#E8643C', '#E5BE3B', '#F4F2EA', '#E6E5E1'
NAV_H, BAR_H = 76, 52

def svg_img(svg, width, height, alt=''):
    return f'<img src="data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}" width="{width}" height="{height}" alt="{alt}">'


SYMBOL_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><polygon points="0,0 64,0 64,22 27,35 0,28" fill="#000"/>'
              '<polygon points="0,35 27,42 64,29 64,64 0,64" fill="#000"/></svg>')
PDF_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 18 22"><path d="M1 1h10l6 6v14H1z" fill="#000"/>'
           '<path d="M11 1v6h6z" fill="#fff"/><text x="3.2" y="18" font-family="Arial" font-weight="700" font-size="5.2" fill="#fff">PDF</text></svg>')
CODE_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 18 22"><path d="M1 1h16v20H1z" fill="#000"/>'
            '<path d="M7 8l-3 3 3 3M11 8l3 3-3 3" stroke="#fff" stroke-width="1.6" fill="none"/></svg>')
REPO_URL = 'https://github.com/tiago-baptistalopes/bloco-rocha'

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Inter+Tight:wght@700;800&family=Barlow+Condensed:wght@700&display=swap');
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{ overflow-x: clip; }}
html, body, [data-testid="stAppViewContainer"], [data-testid="stMarkdownContainer"], .stApp {{ font-family: 'Inter', Helvetica, Arial, sans-serif; color: #000; }}
header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu, footer {{ display: none !important; }}
[data-testid="stMainBlockContainer"], .block-container {{ max-width: 1280px; padding: {NAV_H + 24}px 30px 0 30px !important; }}
[data-testid="stVerticalBlock"] {{ gap: 0.75rem; }}

.br-top {{ position: fixed; top: 0; left: 0; right: 0; z-index: 1000; }}
.br-nav {{ position: relative; height: {NAV_H}px; background: #fff; border-bottom: 4px solid {RULE}; box-sizing: border-box; }}
.br-nav-inner {{ max-width: 1280px; margin: 0 auto; height: 100%; display: flex; align-items: center; gap: 48px; padding: 0 30px; box-sizing: border-box; }}
.br-logo {{ display: flex; align-items: center; gap: 10px; text-decoration: none !important; color: #000 !important; }}
.br-logo span {{ font-family: 'Inter Tight', Inter, sans-serif; font-weight: 800; font-size: 27px; letter-spacing: -0.045em; }}
.br-menu {{ display: flex; gap: 32px; height: 100%; }}
.br-item {{ position: relative; height: 100%; display: flex; align-items: center; }}
.br-item > a {{ font-weight: 700; font-size: 17px; color: #000 !important; text-decoration: none !important; height: 100%; display: flex; align-items: center; }}
.br-item > a::after {{ content: ''; position: absolute; left: 0; right: 0; bottom: -4px; height: 4px; background: {ORANGE}; transform: scaleX(0); transition: transform .15s; }}
.br-item:hover > a::after {{ transform: scaleX(1); }}
.br-drop {{ display: none; position: fixed; top: {NAV_H}px; left: 0; right: 0; background: #fff; z-index: 1001; }}
.br-drop-inner {{ max-width: 1280px; margin: 0 auto; padding: 28px 30px 34px 236px; box-sizing: border-box; }}
.br-drop h6 {{ font-size: 13px; font-weight: 800; letter-spacing: .08em; margin: 0 0 14px 0; padding: 0; color: #000; }}
.br-drop a {{ display: block; font-size: 17px; color: #000 !important; text-decoration: none !important; padding: 5px 0; }}
.br-drop a:hover {{ text-decoration: underline !important; }}
.br-item.has-drop:hover .br-drop {{ display: block; }}
.br-dim {{ display: none; position: fixed; top: {NAV_H}px; left: 0; right: 0; bottom: 0; background: rgba(30, 30, 30, .45); z-index: 999; pointer-events: none; }}
.br-top:has(.has-drop:hover) .br-dim {{ display: block; }}

.br-bar {{ height: {BAR_H}px; background: #000; }}
.br-bar-inner {{ max-width: 1280px; margin: 0 auto; height: 100%; display: flex; align-items: center; gap: 30px; padding: 0 42px; box-sizing: border-box; overflow-x: auto; scrollbar-width: none; }}
.br-bar-inner::-webkit-scrollbar {{ display: none; }}
.br-bar a {{ flex: 0 0 auto; }}
.br-bar a {{ color: #fff !important; text-decoration: none !important; font-weight: 700; font-size: 16px; height: 100%; display: flex; align-items: center; border-bottom: 3px solid transparent; box-sizing: border-box; padding-top: 3px; }}
.br-bar a.active, .br-bar a:hover {{ border-bottom-color: #fff; }}
.br-sample {{ background: #FFF4D6; border: 1px solid {GOLD}; padding: 8px 14px; font-size: 14px; }}

.br-anchor {{ scroll-margin-top: {NAV_H + BAR_H + 16}px; }}
.br-eyebrow {{ font-size: 17px; letter-spacing: .04em; margin: 22px 0 10px 0; }}
.br-title {{ display: flex; align-items: center; gap: 16px; }}
.br-ticker {{ border: 3px solid #000; padding: 6px 14px; font-family: 'Barlow Condensed', 'Inter Tight', sans-serif; font-weight: 700; font-size: 38px; line-height: 1; }}
.br-fund {{ font-family: 'Barlow Condensed', 'Inter Tight', sans-serif; font-weight: 700; font-size: 32px; letter-spacing: -.01em; }}
.br-stats {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 22px 28px; max-width: 640px; margin-top: 6px; }}
.br-stat {{ border-left: 2px solid #000; padding: 2px 0 2px 16px; }}
.br-stat b {{ font-size: 15px; }} .br-stat small {{ display: block; font-size: 15px; margin: 2px 0 8px 0; }}
.br-stat .v {{ font-size: 24px; font-weight: 800; }} .br-stat .r {{ font-size: 14px; margin-left: 6px; }}
.br-docs a {{ display: flex; align-items: center; gap: 8px; color: #000 !important; text-decoration: none !important; font-size: 15px; margin: 0 0 14px 0; }}
.br-docs {{ margin-top: 34px; }}
.br-docs a:hover {{ text-decoration: underline !important; }}

.br-h2 {{ font-weight: 800; font-size: 40px; letter-spacing: -.02em; margin: 56px 0 26px 0; line-height: 1.1; }}
.br-cond {{ font-family: 'Barlow Condensed', 'Inter Tight', sans-serif; font-weight: 700; font-size: 28px; text-transform: uppercase; margin: 0 0 18px 0; }}
.br-grey {{ background: #EDEDED; padding: 30px 26px 34px 26px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 40px; }}
.br-grey ol {{ padding-left: 20px; margin: 0; }} .br-grey li {{ margin-bottom: 18px; font-size: 17px; line-height: 1.45; }}
.br-grey p {{ font-size: 17px; line-height: 1.5; margin: 0; }}
.br-p {{ font-size: 17px; line-height: 1.5; max-width: 820px; }}
.br-note {{ font-size: 14px; color: #3d3d3d; line-height: 1.5; }}

.br-facts {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 120px; }}
.br-kv {{ border: 1px solid {RULE}; }}
.br-kv div {{ display: flex; justify-content: space-between; align-items: center; gap: 20px; padding: 18px 22px; font-size: 16px; }}
.br-kv div:nth-child(even) {{ background: {BEIGE}; }}
.br-kv b {{ font-size: 19px; text-align: right; }} .br-kv small {{ display: block; font-size: 12px; margin-top: 3px; }}

.br-table {{ width: 100%; border-collapse: collapse; font-size: 16px; }}
.br-table th {{ text-align: left; font-weight: 800; padding: 14px 12px; border-bottom: 3px solid #000; }}
.br-table td {{ padding: 15px 12px; border-bottom: 1px solid {RULE}; vertical-align: middle; }}
.br-table tr:nth-child(even) td {{ background: {BEIGE}; }}
.br-table .num {{ text-align: right; white-space: nowrap; }}
.br-compact {{ table-layout: fixed; font-size: 14px; }}
.br-compact th, .br-compact td {{ padding: 10px 5px; }}
.br-compact .num {{ white-space: normal; }}
.br-compact th:first-child, .br-compact td:first-child {{ width: 22%; }}
.br-wrap {{ overflow-x: auto; max-width: 100%; }}
.br-table tfoot td {{ border-top: 3px solid {RULE}; border-bottom: none; }}
.br-bars td.bar {{ width: 58%; border-left: 1px solid {RULE}; }}
.br-bars .fill {{ height: 20px; background: #000; }}

.br-doc {{ display: flex; align-items: center; gap: 14px; font-size: 22px; margin-bottom: 22px; color: #000 !important; text-decoration: none !important; }}
.br-disclaimer {{ font-size: 14px; line-height: 1.5; margin-top: 70px; color: #222; }}
.br-footer {{ background: #000; color: #fff; width: 100vw; margin: 50px 0 0 calc(50% - 50vw); padding: 56px 30px 70px 30px; box-sizing: border-box; }}
.br-footer-inner {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 40px; max-width: 1220px; margin: 0 auto; }}
.br-footer h5 {{ color: #fff; font-size: 20px; font-weight: 800; margin: 0 0 6px 0; padding: 0; }}
.br-footer p, .br-footer a {{ color: #fff !important; font-size: 16px; line-height: 1.5; text-decoration: none !important; display: block; margin: 0 0 14px 0; }}

.st-key-cls [data-baseweb="select"] > div {{ background: {BEIGE}; border: 1px solid #9b9a97; border-radius: 0; min-height: 54px; font-size: 16px; }}
.st-key-cls {{ max-width: 380px; }}
.st-key-cls input {{ caret-color: transparent; cursor: pointer; }}
.st-key-cls [data-baseweb="select"] > div {{ cursor: pointer; }}
.st-key-perfmenu [data-testid="stElementContainer"], .st-key-perfmenu [data-testid="stRadio"] {{ width: 100% !important; }}
.st-key-perfmenu [role="radiogroup"] {{ gap: 0 !important; border-right: 2px solid #000; width: 100%; }}
.st-key-perfmenu [role="radiogroup"] > div {{ width: 100%; }}
.st-key-perfmenu [data-testid="stRadioOption"] {{ width: 100%; padding: 26px 22px; margin: 0; border: 2px solid transparent; box-sizing: border-box; cursor: pointer; }}
.st-key-perfmenu [data-testid="stRadioOption"] > div > div:first-child {{ display: none; }}
.st-key-perfmenu [data-testid="stRadioOption"] p {{ font-size: 18px; font-weight: 800; line-height: 1.3; }}
.st-key-perfmenu [data-testid="stRadioOption"][data-selected="true"] {{ border: 2px solid #000; border-right: none; margin-right: -2px; width: calc(100% + 2px); background: #fff; }}
.st-key-perfmenu label[data-baseweb="radio"] {{ width: 100%; padding: 26px 22px; margin: 0; border: 2px solid transparent; box-sizing: border-box; cursor: pointer; }}
.st-key-perfmenu label[data-baseweb="radio"] > div:first-child {{ display: none; }}
.st-key-perfmenu label[data-baseweb="radio"] p {{ font-size: 18px; font-weight: 800; line-height: 1.3; }}
.st-key-perfmenu label[data-baseweb="radio"]:has(input:checked) {{ border: 2px solid #000; border-right: none; margin-right: -2px; width: calc(100% + 2px); background: #fff; }}
.st-key-perfmenu [role="radiogroup"] {{ flex-direction: column; align-items: stretch; }}
button[data-baseweb="tab"] p {{ font-size: 19px !important; }}
[data-testid="stTab"] p {{ font-size: 19px !important; }}
[data-testid="stTab"] {{ padding: 0 10px 12px 10px; }}
[data-testid="stDataFrame"] {{ border-top: 3px solid #000; }}
</style>
"""

SCROLLSPY = """
<script>
(function () {
  var w = window;
  try { if (window.parent && window.parent.document) { w = window.parent; } } catch (e) {}
  var doc = w.document;
  function update() {
    var links = Array.prototype.slice.call(doc.querySelectorAll('.br-bar a[data-sec]'));
    var current = links.length ? links[0] : null;
    links.forEach(function (a) {
      var el = doc.getElementById(a.getAttribute('data-sec'));
      if (el && el.getBoundingClientRect().top < 160) { current = a; }
    });
    var box = doc.querySelector('[data-testid="stMain"]') || doc.scrollingElement;
    if (box && box.scrollTop + box.clientHeight >= box.scrollHeight - 4 && links.length) { current = links[links.length - 1]; }
    links.forEach(function (a) { a.classList.toggle('active', a === current); });
  }
  if (!w.__brSpy) {
    w.__brSpy = true;
    doc.addEventListener('scroll', update, true);
    w.addEventListener('resize', update);
  }
  setTimeout(update, 400);
})();
</script>
"""


READONLY_SELECT = """
<script>
(function () {
  var w = window;
  try { if (window.parent && window.parent.document) { w = window.parent; } } catch (e) {}
  var doc = w.document;
  function lock() {
    doc.querySelectorAll('.st-key-cls input').forEach(function (i) {
      i.setAttribute('readonly', 'readonly');
      i.setAttribute('inputmode', 'none');
    });
  }
  lock();
  if (!w.__brReadonly) {
    w.__brReadonly = true;
    new w.MutationObserver(lock).observe(doc.body, { childList: true, subtree: true });
  }
})();
</script>
"""


def run_js(js):
    try:
        st.html(js, unsafe_allow_javascript=True)
    except TypeError:
        components.html(js, height=0)


def page_setup(title, current, sections=None, sample=False):
    st.html(CSS)
    funds = ''.join(f'<a href="/{f["path"]}">{f["name"]}</a>' for f in FUNDS.values())
    bar = ''
    if sections:
        links = ''.join(f'<a href="#{k}" data-sec="{k}">{v}</a>' for k, v in sections.items())
        bar = f'<div class="br-bar"><div class="br-bar-inner">{links}</div></div>'
    st.html(f"""
<div class="br-top">
  <div class="br-nav">
    <div class="br-nav-inner">
      <a class="br-logo" href="/">{svg_img(SYMBOL_SVG, 30, 30)}<span>BlocoRocha</span></a>
      <div class="br-menu">
        <div class="br-item has-drop"><a href="/">Products</a>
          <div class="br-drop"><div class="br-drop-inner"><h6>OUR FUNDS</h6>{funds}</div></div>
        </div>
        <div class="br-item"><a href="/about-us">About us</a></div>
      </div>
    </div>
  </div>
  {bar}
  <div class="br-dim"></div>
</div>""")
    if sections:
        st.html(f'<style>[data-testid="stMainBlockContainer"], .block-container {{ padding-top: {NAV_H + BAR_H + 24}px !important; }}</style>')
        run_js(SCROLLSPY)
    if sample:
        st.html('<div class="br-sample"><b>Sample data.</b> These figures come from simulated inputs. '
                'Run Section 9 of the V4 notebook and commit <code>app_data/</code> to publish the backtest.</div>')


def anchor(key, title):
    st.html(f'<div id="{key}" class="br-anchor"><div class="br-h2">{title}</div></div>')


def kv(rows):
    cells = ''.join(f'<div><span>{k}{f"<small>{d}</small>" if d else ""}</span><b>{v}</b></div>' for k, v, d in rows)
    return f'<div class="br-kv">{cells}</div>'


def footer():
    st.html("""
<div class="br-disclaimer">
<p><b>Important information.</b> BlocoRocha is a fictional asset manager created for a Financial Modeling course project. The funds on
this website do not exist, are not offered to the public and cannot be bought. All performance figures are backtested: they apply
investment rules to historical market data, with the benefit of hindsight, and are not the record of an actual fund. Backtested and past
performance do not predict future returns. The value of an investment and the income from it can fall as well as rise, and investors may
not get back the amount invested. Nothing on this website is investment, tax or legal advice.</p>
<p>Data: prices from Yahoo Finance; company fundamentals from Compustat (S&amp;P Global Market Intelligence) via Wharton Research Data
Services; 12-month EURIBOR from the European Central Bank. S&amp;P 500 is a trademark of S&amp;P Dow Jones Indices; its use here is for
comparison only.</p>
</div>
<div class="br-footer"><div class="br-footer-inner">
  <div><h5>BlocoRocha</h5><p>A student-built asset manager. We design rules-based equity funds for long-term European investors
  and test them openly against the data.</p></div>
  <div><h5>Corporate</h5><a href="/about-us">About us</a></div>
  <div><h5>Legal</h5><a href="/about-us#data-sources">Data sources</a></div>
</div></div>""")


def pct(x, d=2):
    return '–' if x is None or x != x else f'{x * 100:,.{d}f}%'


def eur(x, d=2):
    return '–' if x is None or x != x else f'€{x:,.{d}f}'
