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


# Edit the team here: (name, role in the project). The page builds the table from this list.
TEAM = [
    ('Catarina Soares', 'Coordination, prospectus and submission'),
    ('Rodrigo Caldeira', 'Data pipeline and backtest'),
    ('Maria Albuquerque', 'Performance and risk measures'),
    ('Mariana Fernandes', 'Client profile, strategy rationale and risks'),
    ('Tiago Lopes', 'Website and reproducibility'),
]

PRINCIPLES = [
    ('Rules, not forecasts', 'Every buy and sell decision follows written rules on price momentum, price-to-book and leverage. '
     'No manager overrides them, so the funds behave the same way in good and bad markets.'),
    ('Evidence before promises', 'We test each rule on more than 20 years of market data, from January 2005, using only information '
     'available at each date and after trading costs and fees. We publish the results that disappoint as well as those that impress.'),
    ('Open by design', 'All code is public on GitHub, and one notebook reproduces every figure on this website and in our prospectus.'),
]


def about():
    page_setup('About us', 'about', sample=False)
    principles = ''.join(f'<li><b>{title}.</b> {text}</li>' for title, text in PRINCIPLES)
    team = ''.join(f'<tr><td><b>{name}</b></td><td>{role}</td></tr>' for name, role in TEAM)
    st.html('<div class="br-h2" style="margin-top:30px">About us</div>'
            '<div class="br-cond" style="margin-top:10px">Who we are</div>'
            '<p class="br-p">BlocoRocha is a student-built asset manager, created by five Master\'s in Finance students at Nova School '
            'of Business and Economics for the Financial Modeling course. We design rules-based equity funds for long-term investors '
            'in euros: people who already own a core of low-cost index funds and want a growth-oriented allocation they can hold for '
            '20 years.</p>'
            '<div class="br-cond" style="margin-top:40px">How we invest</div>'
            f'<ol class="br-p" style="padding-left:20px">{principles}</ol>'
            '<div class="br-cond" style="margin-top:40px">Our team</div>'
            '<table class="br-table" style="max-width:820px"><thead><tr><th>Name</th><th>Role</th></tr></thead>'
            f'<tbody>{team}</tbody></table>'
            '<div id="data-sources" class="br-anchor"><div class="br-cond" style="margin-top:40px">Data sources</div></div>'
            '<div class="br-p"><p><b>Prices and exchange rates:</b> Yahoo Finance, via the yfinance library.</p>'
            '<p><b>Company fundamentals</b> (book equity, debt, shares outstanding): Compustat North America and Compustat Global, '
            'S&amp;P Global Market Intelligence, via Wharton Research Data Services.</p>'
            '<p><b>Company names, sectors and industries:</b> Yahoo Finance.</p>'
            '<p><b>Risk-free rate:</b> 12-month EURIBOR, European Central Bank Data Portal.</p>'
            '<p><b>Benchmark:</b> S&amp;P 500 Total Return index, S&amp;P Dow Jones Indices, via Yahoo Finance.</p></div>')
    footer()
