import altair as alt
import pandas as pd
import streamlit as st

from bloco import data as D
from bloco.ui import CODE_SVG, GOLD, PDF_SVG, READONLY_SELECT, REPO_URL, anchor, run_js, eur, footer, kv, page_setup, pct, svg_img

SECTIONS = {'overview': 'Overview', 'performance': 'Performance', 'risks': 'Key Risks', 'key-facts': 'Key Facts',
            'portfolio': 'Portfolio', 'taxes': 'Taxes', 'holdings': 'Holdings', 'scenarios': 'Scenarios',
            'literature': 'Literature'}
PDF = svg_img(PDF_SVG, 18, 22)
PDF_BIG = svg_img(PDF_SVG, 40, 49)
CODE = svg_img(CODE_SVG, 18, 22)
CODE_BIG = svg_img(CODE_SVG, 40, 49)


def chart_style(chart, height=320):
    return (chart.properties(height=height, padding={'left': 5, 'right': 10, 'top': 5, 'bottom': 25})
            .configure_axis(labelFont='Inter', titleFont='Inter', labelFontSize=13, titleFontSize=13, gridDash=[3, 3],
                            gridColor='#BDBDBD', domainColor='#9B9A97', tickColor='#9B9A97', labelColor='#333')
            .configure_legend(labelFont='Inter', labelFontSize=13, orient='top', symbolType='circle', title=None, labelLimit=0)
            .configure_view(strokeWidth=0))


def bars(values, fund_label):
    df = values.rename_axis('index').reset_index().melt(id_vars='index', var_name='series', value_name='return')
    order = list(values.index.astype(str))
    df['index'] = df['index'].astype(str)
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('index:N', sort=order, title=None, axis=alt.Axis(labelAngle=0)),
        xOffset=alt.XOffset('series:N', sort=[fund_label, 'S&P 500 total return']),
        y=alt.Y('return:Q', title=None, axis=alt.Axis(format='%')),
        color=alt.Color('series:N', scale=alt.Scale(domain=[fund_label, 'S&P 500 total return'], range=['#000000', GOLD])),
        tooltip=[alt.Tooltip('index:N', title='Period'), alt.Tooltip('series:N', title=' '), alt.Tooltip('return:Q', format='.2%')])
    st.altair_chart(chart_style(chart), use_container_width=True)
    head = ''.join(f'<th class="num">{c}</th>' for c in values.index.astype(str))
    rows = ''.join(f'<tr><td>{name}</td>' + ''.join(f'<td class="num">{pct(v)}</td>' for v in values[name]) + '</tr>'
                   for name in values.columns)
    st.html(f'<table class="br-table br-compact"><thead><tr><th></th>{head}</tr></thead><tbody>{rows}</tbody></table>')


def render(fund):
    nav, holdings, securities, classes, meta = D.load()
    info = D.FUNDS[fund]
    page_setup(info['name'], 'products', SECTIONS, meta.get('sample', False))

    left, right = st.columns([3, 1])
    with left:
        st.html(f'<div class="br-eyebrow">EQUITY</div><div class="br-title"><div class="br-ticker">{info["code"]}</div>'
                f'<div class="br-fund">{info["name"]}</div></div>')
        with st.container(key='cls'):
            cls = st.selectbox('Share class', list(D.CLASS_LABELS), format_func=D.CLASS_LABELS.get, label_visibility='collapsed')
        run_js(READONLY_SELECT)
    level = D.series(nav, fund, cls)
    bench = nav[D.BENCHMARK]
    fee = classes.loc[cls]
    ps = level * D.NAV_START
    last, prev = ps.index[-1], ps.index[-2]
    year = ps.loc[ps.index >= last - pd.DateOffset(weeks=52)]
    change = ps.iloc[-1] - ps.iloc[-2]
    ytd = D.period_return(level, pd.Timestamp(last.year - 1, 12, 31), last)
    with left:
        st.html(f"""<div class="br-stats">
<div class="br-stat"><b>NAV as of</b><small>{last:%b %d, %Y}</small><span class="v">{eur(ps.iloc[-1])}</span>
<span class="r">52 WK: {eur(year.min())} – {eur(year.max())}</span></div>
<div class="br-stat"><b>NAV daily change</b><small>{last:%b %d, %Y}</small><span class="v">{'▲' if change >= 0 else '▼'} {eur(change)}</span>
<span class="r">({pct(change / ps.iloc[-2])})</span></div>
<div class="br-stat"><b>NAV total return</b><small>{last:%b %d, %Y}</small><span class="v">YTD: {pct(ytd)}</span></div>
</div>""")
    with right:
        st.html(f'<div class="br-docs"><a href="#literature">{PDF} Prospectus</a>'
                f'<a href="{REPO_URL}" target="_blank" rel="noopener">{CODE} Repository</a></div>')

    anchor('overview', '')
    st.html(f"""<div class="br-grey">
<div><div class="br-cond">Why {info["code"]}?</div><ol>{''.join(f'<li>{w}</li>' for w in info['why'])}</ol></div>
<div><div class="br-cond">Investment philosophy</div><p>{info['philosophy']}</p></div></div>""")

    anchor('performance', 'Performance')
    menu, body = st.columns([1, 3])
    with menu, st.container(key='perfmenu'):
        view = st.radio('View', ['Performance', 'Hypothetical growth of €10,000', 'Historical NAV'], label_visibility='collapsed')
    label = f'{info["name"]} (before fees)'
    years = (level.index - level.index[0]).days / 365.25
    before_fees = level / (1 - fee['management fee']) ** years
    with body:
        if view == 'Performance':
            tabs = st.tabs(['Calendar year', 'Annual', 'Average annual', 'Cumulative'])
            texts = ['the fund return in each of the last 10 calendar years',
                     'the fund return over each of the last five 12-month periods ending at the latest quarter end',
                     'the annualized fund return over standard periods ending at the latest month end',
                     'the total fund return over standard periods ending at the latest month end']
            makers = [D.calendar_years, D.annual_periods, D.average_annual, D.cumulative]
            for tab, text, make in zip(tabs, texts, makers):
                with tab:
                    st.html(f'<p class="br-p"><b>This chart shows {text}, against the S&amp;P 500 total return. Returns are before '
                            f'all fees (entry, management and exit) and after transaction costs.</b></p>')
                    bars(pd.DataFrame({label: make(before_fees), 'S&P 500 total return': make(bench)}), label)
        elif view == 'Hypothetical growth of €10,000':
            growth = pd.DataFrame({label: before_fees * 10_000, 'S&P 500 total return': bench * 10_000}).resample('W').last()
            df = growth.reset_index(names='date').melt(id_vars='date', var_name='series', value_name='value')
            chart = alt.Chart(df).mark_line(strokeWidth=2).encode(
                x=alt.X('date:T', title=None, axis=alt.Axis(format='%Y', labelAngle=0, tickCount='year', labelOverlap=True)),
                y=alt.Y('value:Q', title=None, axis=alt.Axis(format=',.0f')),
                color=alt.Color('series:N', scale=alt.Scale(domain=[label, 'S&P 500 total return'], range=['#000000', GOLD])),
                tooltip=[alt.Tooltip('date:T'), alt.Tooltip('series:N', title=' '), alt.Tooltip('value:Q', title='Value (EUR)', format=',.0f')])
            st.html(f'<p class="br-p"><b>Value of €10,000 invested at launch on {level.index[0]:%b %d, %Y}, before fees and after transaction costs.</b></p>')
            st.altair_chart(chart_style(chart, 380), use_container_width=True)
        else:
            m = ps.resample('ME').last()
            if st.toggle('Show as chart', key='nav_chart'):
                df = pd.DataFrame({'date': m.index, 'NAV (EUR)': m.values})
                chart = alt.Chart(df).mark_line(strokeWidth=2, color='#000000').encode(
                    x=alt.X('date:T', title=None, axis=alt.Axis(format='%Y', labelAngle=0, tickCount='year', labelOverlap=True)),
                    y=alt.Y('NAV (EUR):Q', title=None, axis=alt.Axis(format=',.2f')),
                    tooltip=[alt.Tooltip('date:T', title='Month end', format='%b %Y'), alt.Tooltip('NAV (EUR):Q', format=',.2f')])
                st.html(f'<p class="br-p"><b>Month-end net asset value per {cls} share, in euros.</b></p>')
                st.altair_chart(chart_style(chart, 380), use_container_width=True)
            else:
                m = m.iloc[::-1]
                st.dataframe(pd.DataFrame({'Month end': m.index.strftime('%b %Y'), 'NAV (EUR)': m.values.round(2),
                                           'Monthly return': (m / m.shift(-1) - 1).values}),
                             hide_index=True, height=420,
                             column_config={'Monthly return': st.column_config.NumberColumn(format='percent')})

    anchor('risks', 'Key Risks')
    st.html("""<div class="br-p">
<p><b>Equity risk.</b> The Fund invests only in shares. Share prices move daily with company results, economic and political news, and
market sentiment, and can fall sharply.</p>
<p><b>Style risk.</b> Momentum and growth strategies can suffer sudden reversals, when past winners fall faster than the market. The
Fund may underperform broad indices for long periods.</p>
<p><b>Currency hedging risk.</b> Dollar positions are hedged to euros with derivatives. Hedging is imperfect and exposes the Fund to the
insolvency of derivative counterparties.</p>
<p><b>Backtest risk.</b> Performance shown is simulated with today's knowledge of which companies survived and with accounting data
used before its publication date. Real results would likely have been lower.</p></div>""")

    anchor('key-facts', 'Key Facts')
    v = D.vev(level)
    latest = holdings[(holdings['fund'] == fund) & (holdings['date'] == holdings.loc[holdings['fund'] == fund, 'date'].max())]
    hold_years = meta.get('hold_years', 20)
    st.html('<div class="br-facts">' + kv([
        ('Total net assets', eur(D.SHARES_OUTSTANDING * ps.iloc[-1], 0), f'as of {last:%b %d, %Y}'),
        ('Shares outstanding', f'{D.SHARES_OUTSTANDING:,}', f'€{D.LAUNCH_ASSETS / 1e6:,.0f} million at launch'),
        ('Fund launch date', f'{pd.Timestamp(meta["fund_launch"]):%b %d, %Y}', None),
        ('Share class currency', 'EUR', None),
        ('Asset class', 'Equity', None),
        ('Summary Risk Indicator', f'{D.sri(v)} of 7', f'volatility equivalent {pct(v, 1)}'),
        ('Entry fee', pct(fee['entry fee']), None),
        ('Management fee (per year)', pct(fee['management fee'], 3), None),
        ('Exit fee', pct(fee['exit fee']), None),
        ('Use of income', 'Accumulating', None),
    ]) + kv([
        ('Base currency', 'EUR', None),
        ('Benchmark', 'S&amp;P 500 Total Return', 'dollar returns, hedged to euros'),
        ('Rebalance frequency', 'Monthly', None),
        ('Number of holdings', f'{len(latest)}', f'as of {latest["date"].max():%b %d, %Y}'),
        ('Recommended holding period', f'{hold_years} years', None),
        ('Currency hedging', 'USD hedged to EUR', None),
        ('Product structure', 'Physical', None),
        ('Domicile', 'Luxembourg (illustrative)', None),
    ]) + '</div>')

    anchor('portfolio', 'Portfolio Characteristics')
    asof = f'as of {last:%b %d, %Y}'
    st.html('<div class="br-facts">' + kv([
        ('Number of holdings', f'{len(latest)}', f'as of {latest["date"].max():%b %d, %Y}'),
        ('Beta (3 years)', f'{D.beta_3y(level, bench):.3f}', 'against the S&amp;P 500, monthly returns'),
        ('Maximum drawdown since launch', pct(D.max_drawdown(level)), asof),
    ]) + kv([
        ('P/B ratio', f'{D.portfolio_pb(latest):.2f}', f'weighted harmonic average, {latest["date"].max():%b %d, %Y}'),
        ('Standard deviation (3 years)', pct(D.std_3y(level)), 'annualized, monthly returns'),
        ('Volatility equivalent (VaR-based)', pct(v), 'key information document method, 20 years'),
    ]) + '</div>')

    anchor('taxes', 'Tax Domicile')
    st.html(f'<p class="br-p">Choose your country of tax residence to see what a €10,000 investment in {cls} shares would have been '
            f'worth after {hold_years} years from launch, after fees and capital gains tax on redemption.</p>')
    c1, c2 = st.columns([1, 2])
    with c1:
        country = st.selectbox('Tax domicile', sorted(D.TAX), index=sorted(D.TAX).index('Portugal'))
    end = level.index[0] + pd.DateOffset(years=hold_years)
    invested = 10_000.0
    gross_value = invested * (1 - fee['entry fee']) * D.value_at(level, end) * (1 - fee['exit fee'])
    tax = D.tax_due(country, gross_value - invested)
    after = gross_value - tax
    with c2:
        st.html(kv([
            ('Value at redemption, after fees', eur(gross_value, 0), f'{level.index[0]:%b %d, %Y} to {end:%b %d, %Y}'),
            ('Capital gain', eur(gross_value - invested, 0), None),
            ('Capital gains tax', eur(tax, 0), f'effective rate {pct(tax / max(gross_value - invested, 1e-9), 1)}'),
            ('Value after tax', eur(after, 0), f'{pct((after / invested) ** (1 / hold_years) - 1)} a year'),
        ]) + f'<p class="br-note" style="margin-top: 20px">{D.TAX[country]["note"]} Rates as of 2026, applied to the whole gain at redemption. '
             f'Illustrative only; not tax advice.</p>')

    anchor('holdings', 'Holdings')
    fh = holdings[holdings['fund'] == fund]
    dates = sorted(fh['date'].unique(), reverse=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        when = st.selectbox('As of', dates, format_func=lambda d: f'{pd.Timestamp(d):%b %d, %Y}')
    with c2:
        query = st.text_input('Filter list by keyword', placeholder='Type to search')
    h = fh[fh['date'] == when].join(securities, on='ticker')
    table = pd.DataFrame({'Ticker': h['ticker'], 'Name': h['name'], 'Sector': h['sector'], 'Industry': h['industry'],
                          'Region': h['region'].map({'US': 'United States', 'EU': 'Europe'}),
                          'Weight (%)': h['weight'] * 100, 'P/B ratio': h['price_to_book']}).sort_values('Weight (%)', ascending=False)
    if query:
        table = table[table.apply(lambda r: query.lower() in ' '.join(map(str, r.values)).lower(), axis=1)]
    st.dataframe(table, hide_index=True, height=440,
                 column_config={'Weight (%)': st.column_config.NumberColumn(format='%.2f'),
                                'P/B ratio': st.column_config.NumberColumn(format='%.2f')})

    st.html('<div class="br-h2" style="margin-top:40px">Exposure Breakdowns</div>')
    latest_h = latest.join(securities, on='ticker')
    for tab, col in zip(st.tabs(['Sector', 'Industry', 'Region']), ['sector', 'industry', 'region']):
        with tab:
            w = latest_h.groupby(col)['weight'].sum().sort_values(ascending=False) * 100
            if len(w) > 16:
                w = pd.concat([w.iloc[:15], pd.Series({'Other': w.iloc[15:].sum()})])
            if col == 'region':
                w.index = w.index.map({'US': 'United States', 'EU': 'Europe'})
            rows = ''.join(f'<tr><td>{k}</td><td class="num">{x:.2f}</td><td class="bar"><div class="fill" '
                           f'style="width:{x / w.max() * 100:.1f}%"></div></td></tr>' for k, x in w.items())
            st.html(f'<p class="br-p"><b>% of market value as of</b> {latest["date"].max():%b %d, %Y}</p>'
                    f'<table class="br-table br-bars"><thead><tr><th>Type</th><th class="num">Fund</th><th></th></tr></thead>'
                    f'<tbody>{rows}</tbody></table>')

    anchor('scenarios', 'Performance Scenarios')
    sc = D.scenarios(level, fee['entry fee'], fee['exit fee'], horizons=(1, hold_years // 2, hold_years))
    st.html(f"""<div class="br-p"><p>The EU regulation on key information documents for packaged retail and insurance-based investment
products (PRIIPs) sets the method for four hypothetical scenarios of how the product could perform. The figures include all costs of
the product, including the {cls} entry and exit fees, but may not include costs you pay to an advisor or distributor, and do not take
your personal tax situation into account. What you get will depend on how the market performs, which is uncertain and cannot be
predicted. The stress scenario uses stressed volatility from the backtest; the other scenarios use the distribution of its daily
returns.</p><p>Recommended holding period: <b>{hold_years} years</b></p><p>Example investment: <b>€10,000</b></p></div>""")
    head = ''.join(f'<th class="num">If you exit after {t} year{"s" if t > 1 else ""}</th>' for t in sc.columns)
    body = ('<tr><td><b>Minimum</b></td><td colspan="' + str(len(sc.columns) + 1) +
            '"><b>⚠ There is no minimum guaranteed return. You could lose some or all of your investment.</b></td></tr>')
    for name, row in sc.iterrows():
        cells = ''.join(f'<td class="num"><b>{eur(val, 0)}</b><br>{pct((val / 10_000) ** (1 / t) - 1, 1)}</td>' for t, val in row.items())
        body += f'<tr><td><b>{name}</b></td><td><b>What you might get back after costs</b><br>Average return each year</td>{cells}</tr>'
    st.html(f'<div class="br-wrap"><table class="br-table"><thead><tr><th>SCENARIOS</th><th></th>{head}</tr></thead><tbody>{body}</tbody></table></div>'
            '<p class="br-p">The stress scenario shows what you might get back in extreme market circumstances.</p>')

    anchor('literature', 'Literature')
    st.html(f'<div class="br-doc">{PDF_BIG}<span>{info["name"]}: Prospectus '
            f'<span class="br-note">(coming soon)</span></span></div>'
            f'<a class="br-doc" href="{REPO_URL}" target="_blank" rel="noopener">{CODE_BIG}<span>Repository: code and data on GitHub</span></a>')
    footer()
