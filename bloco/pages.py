import streamlit as st

from bloco import data as D
from bloco.ui import footer, page_setup, pct


def products():
    nav, holdings, securities, classes, meta = D.load()
    page_setup('Products', 'products', sample=meta.get('sample', False))
    st.html('<div class="br-h2" style="margin-top:30px">Products</div>'
            '<p class="br-p">Rules-based global equity funds for long-term investors in euros. Each fund is available in three share '
            'classes with different fee structures and the same 20-year outcome per euro invested.</p>')
    rows = ''
    for key, f in D.FUNDS.items():
        level = D.series(nav, key, 'E')
        avg = D.average_annual(level)
        rows += (f'<tr><td><a href="/{f["path"]}" style="color:#000;font-weight:800;font-size:18px">{f["name"]}</a>'
                 f'<br><span class="br-note">{f["code"]} · Equity · Classes E, F and G</span></td>'
                 f'<td class="num">{pct(avg.get("1 year"))}</td><td class="num">{pct(avg.get("10 years"))}</td>'
                 f'<td class="num">{pct(avg["Since launch"])}</td><td class="num">{D.sri(D.vev(level))} of 7</td></tr>')
    st.html('<table class="br-table"><thead><tr><th>Fund</th><th class="num">1 year</th><th class="num">10 years (annualized)</th>'
            '<th class="num">Since launch (annualized)</th><th class="num">Risk indicator</th></tr></thead>'
            f'<tbody>{rows}</tbody></table><p class="br-note">Class E, net of management fees and transaction costs, '
            'excluding entry fees, to the latest month end.</p>')
    footer()


def about():
    meta = D.load()[4]
    page_setup('About us', 'about', sample=False)
    st.html('<div class="br-h2" style="margin-top:30px">About us</div>'
            '<div class="br-cond" style="margin-top:10px">Our team</div>'
            '<p class="br-p">A description of the BlocoRocha team will be added here.</p>'
            '<div id="data-sources" class="br-anchor"><div class="br-cond" style="margin-top:40px">Data sources</div></div>'
            '<div class="br-p"><p><b>Prices and exchange rates:</b> Yahoo Finance, via the yfinance library.</p>'
            '<p><b>Company fundamentals</b> (book equity, debt, shares outstanding): Compustat North America and Compustat Global, '
            'S&amp;P Global Market Intelligence, via Wharton Research Data Services.</p>'
            '<p><b>Company names, sectors and industries:</b> Yahoo Finance.</p>'
            '<p><b>Risk-free rate:</b> 12-month EURIBOR, European Central Bank Data Portal.</p>'
            '<p><b>Benchmark:</b> S&amp;P 500 Total Return index, S&amp;P Dow Jones Indices, via Yahoo Finance.</p></div>')
    footer()
