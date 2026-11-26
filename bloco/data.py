import json
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

APP_DATA = Path(__file__).resolve().parent.parent / 'app_data'
LAUNCH_ASSETS = 100_000_000
SHARES_OUTSTANDING = 10_000_000
NAV_START = LAUNCH_ASSETS / SHARES_OUTSTANDING
BENCHMARK = 'sp500'

FUNDS = {
    'early_growth': {
        'name': 'Global Equity Early Growth',
        'code': 'GEEG',
        'path': 'global-equity-early-growth',
        'why': [
            'Invests early in fast-growing companies: names in the top quartile of 12-month price momentum that also sit in the top half of the universe by price-to-book.',
            'Holds each company until its growth matures and sells on clear signals: debt-to-equity doubling year on year, or price-to-book growing by 10% or less over a year.',
            'Diversifies across 50 large and mid-cap companies listed in dollars in the United States and in euros in Europe, equally weighted, with dollar exposure hedged to euros.',
        ],
        'philosophy': (
            'The Fund seeks long-term capital growth by buying companies early in their growth phase and selling them as they mature. '
            'Each month it screens every dollar-listed United States company and euro-listed European company with a market value of at least '
            '€1.5 billion at launch. Free slots go first to companies in the top quartile of 12-month momentum (excluding the most recent month) '
            'that are also in the top half by price-to-book, then to the best combined rank. A holding is sold when its debt-to-equity ratio '
            'doubles year on year or its price-to-book ratio grows by 10% or less over twelve months. The Fund holds 50 companies at equal '
            'weights and rebalances monthly.'
        ),
    },
    'momentum_growth': {
        'name': 'Global Equity Momentum Growth',
        'code': 'GEMG',
        'path': 'global-equity-momentum-growth',
        'why': [
            'Follows the strongest movers among growth stocks: each month, every company in the top quartile of 12-month price momentum that is also in the top half of the universe by price-to-book.',
            'Rebuilt from scratch every month, with no holding period and no exit signals, so the portfolio moves with momentum as it shifts.',
            'Equal weights across large and mid-cap companies listed in dollars in the United States and in euros in Europe, with dollar exposure hedged to euros.',
        ],
        'philosophy': (
            'The Fund seeks long-term capital growth by following price momentum among growth companies. Each month it screens every '
            'dollar-listed United States company and euro-listed European company with a market value of at least €1.5 billion at launch, '
            'and holds every company that ranks in the top quartile of 12-month momentum (excluding the most recent month) and in the top '
            'half by price-to-book. Holdings are equally weighted and the portfolio is rebuilt monthly. Unlike Global Equity Early Growth, '
            'it applies no exit signals and does not keep a company once it leaves the screen.'
        ),
    },
}

CLASS_LABELS = {'E': 'Class E (Accumulating, EUR)', 'F': 'Class F (Accumulating, EUR)', 'G': 'Class G (Accumulating, EUR)'}

SIC_GROUPS = {
    1: 'Agricultural Production (Crops)', 2: 'Agricultural Production (Livestock)', 7: 'Agricultural Services', 8: 'Forestry',
    9: 'Fishing, Hunting and Trapping', 10: 'Metal Mining', 12: 'Coal Mining', 13: 'Oil and Gas Extraction',
    14: 'Nonmetallic Minerals Mining', 15: 'Building Construction', 16: 'Heavy Construction', 17: 'Special Trade Construction',
    20: 'Food and Kindred Products', 21: 'Tobacco Products', 22: 'Textile Mill Products', 23: 'Apparel',
    24: 'Lumber and Wood Products', 25: 'Furniture and Fixtures', 26: 'Paper and Allied Products', 27: 'Printing and Publishing',
    28: 'Chemicals and Allied Products', 29: 'Petroleum Refining', 30: 'Rubber and Plastics', 31: 'Leather Products',
    32: 'Stone, Clay and Glass', 33: 'Primary Metals', 34: 'Fabricated Metal Products',
    35: 'Industrial Machinery and Computer Equipment', 36: 'Electronic and Electrical Equipment', 37: 'Transportation Equipment',
    38: 'Instruments and Related Products', 39: 'Miscellaneous Manufacturing', 40: 'Railroad Transportation',
    41: 'Local and Suburban Transit', 42: 'Trucking and Warehousing', 44: 'Water Transportation', 45: 'Air Transportation',
    46: 'Pipelines', 47: 'Transportation Services', 48: 'Communications', 49: 'Electric, Gas and Sanitary Services',
    50: 'Wholesale Trade (Durable Goods)', 51: 'Wholesale Trade (Nondurable Goods)', 52: 'Building Materials and Garden Supplies',
    53: 'General Merchandise Stores', 54: 'Food Stores', 55: 'Auto Dealers and Gas Stations', 56: 'Apparel and Accessory Stores',
    57: 'Home Furniture and Equipment Stores', 58: 'Eating and Drinking Places', 59: 'Miscellaneous Retail',
    60: 'Depository Institutions', 61: 'Nondepository Credit Institutions', 62: 'Security and Commodity Brokers',
    63: 'Insurance Carriers', 64: 'Insurance Agents and Brokers', 65: 'Real Estate', 67: 'Holding and Investment Offices',
    70: 'Hotels and Lodging', 72: 'Personal Services', 73: 'Business Services', 75: 'Auto Repair and Services',
    76: 'Miscellaneous Repair Services', 78: 'Motion Pictures', 79: 'Amusement and Recreation', 80: 'Health Services',
    81: 'Legal Services', 82: 'Educational Services', 83: 'Social Services', 86: 'Membership Organizations',
    87: 'Engineering and Management Services', 89: 'Miscellaneous Services', 99: 'Nonclassifiable',
}
SIC_DETAIL = {
    283: 'Pharmaceuticals and Biotechnology', 357: 'Computer and Office Equipment', 367: 'Semiconductors and Electronic Components',
    737: 'Software and Computer Services', 384: 'Medical Instruments and Supplies', 481: 'Telephone Communications',
}

TAX = {
    'Austria': {'rate': 0.275, 'note': 'Flat 27.5% capital gains tax (KESt) on investment fund gains.'},
    'Belgium': {'rate': 0.10, 'allowance': 10_000, 'note': '10% on capital gains from financial assets above an annual exemption of €10,000 (from 1 January 2026).'},
    'France': {'rate': 0.314, 'note': 'Flat tax (PFU) of 31.4% from 1 January 2026: 12.8% income tax plus 18.6% social levies.'},
    'Germany': {'rate': 0.26375 * 0.70, 'note': '25% flat tax plus 5.5% solidarity surcharge (26.375%); 30% of gains on equity funds are exempt, so the effective rate is 18.46%. Church tax and the €1,000 annual allowance are ignored.'},
    'Ireland': {'rate': 0.38, 'note': 'Exit tax of 38% on gains from Irish and equivalent EU funds from 1 January 2026. The 8-year deemed disposal rule is ignored here.'},
    'Italy': {'rate': 0.26, 'note': 'Flat 26% substitute tax on capital gains from financial assets.'},
    'Luxembourg': {'rate': 0.0, 'note': 'Gains on securities held for more than six months by non-substantial investors are exempt.'},
    'Portugal': {'rate': 0.196, 'note': '28% standard rate; for holdings of more than 8 years only 70% of the gain is taxed, an effective 19.6%.'},
    'Spain': {'brackets': [(6_000, 0.19), (50_000, 0.21), (200_000, 0.23), (300_000, 0.27), (np.inf, 0.30)], 'note': 'Savings income scale: 19% up to €6,000, 21% to €50,000, 23% to €200,000, 27% to €300,000 and 30% above.'},
}


@st.cache_data
def load():
    nav = pd.read_csv(APP_DATA / 'nav.csv', index_col=0, parse_dates=True)
    holdings = pd.read_csv(APP_DATA / 'holdings.csv', parse_dates=['date'])
    securities = pd.read_csv(APP_DATA / 'securities.csv').set_index('ticker')
    classes = pd.read_csv(APP_DATA / 'classes.csv', index_col=0)
    meta = json.loads((APP_DATA / 'meta.json').read_text())
    if 'sic' in securities:
        securities['industry'] = securities['sic'].map(industry)
    for col in ('name', 'sector', 'industry'):
        if col not in securities:
            securities[col] = None
    securities[['sector', 'industry']] = securities[['sector', 'industry']].fillna('Unclassified')
    return nav, holdings, securities, classes, meta


def industry(sic):
    if pd.isna(sic):
        return 'Unclassified'
    sic = int(sic)
    if sic // 10 in SIC_DETAIL:
        return SIC_DETAIL[sic // 10]
    group = sic // 100
    if 91 <= group <= 97:
        return 'Public Administration'
    return SIC_GROUPS.get(group, 'Unclassified')


def series(nav, fund, cls):
    return nav[f'{fund}_{cls}']


def value_at(level, date):
    return level.loc[:date].iloc[-1]


def period_return(level, start, end):
    return value_at(level, end) / value_at(level, start) - 1


def month_end(level):
    return pd.offsets.MonthEnd().rollback(level.index[-1].normalize())


def calendar_years(level, n=10):
    yearly = level.resample('YE').last()
    out = yearly.pct_change().dropna()
    out = out[out.index.year < level.index[-1].year]
    out.index = out.index.year
    return out.tail(n)


def annual_periods(level, n=5):
    end = pd.offsets.QuarterEnd().rollback(level.index[-1].normalize())
    rows = {}
    for i in range(n):
        e = end - pd.DateOffset(years=i)
        s = e - pd.DateOffset(years=1)
        if s >= level.index[0]:
            rows[f'{s:%b %Y} – {e:%b %Y}'] = period_return(level, s, e)
    return pd.Series(rows).iloc[::-1]


def average_annual(level):
    end = month_end(level)
    rows = {}
    for label, years in (('1 year', 1), ('3 years', 3), ('5 years', 5), ('10 years', 10)):
        s = end - pd.DateOffset(years=years)
        if s >= level.index[0]:
            rows[label] = (1 + period_return(level, s, end)) ** (1 / years) - 1
    t = (end - level.index[0]).days / 365.25
    rows['Since launch'] = (1 + period_return(level, level.index[0], end)) ** (1 / t) - 1
    return pd.Series(rows)


def cumulative(level):
    end = month_end(level)
    rows = {'Year to date': period_return(level, pd.Timestamp(end.year - 1, 12, 31), end)}
    for label, months in (('1 month', 1), ('3 months', 3), ('6 months', 6), ('1 year', 12), ('3 years', 36), ('5 years', 60), ('10 years', 120)):
        s = end - pd.DateOffset(months=months)
        if s >= level.index[0]:
            rows[label] = period_return(level, s, end)
    rows['Since launch'] = period_return(level, level.index[0], end)
    return pd.Series(rows)


def monthly_returns(level):
    return level.resample('ME').last().pct_change().dropna()


def beta_3y(level, bench):
    m = pd.concat([monthly_returns(level), monthly_returns(bench)], axis=1).dropna().tail(36)
    return m.iloc[:, 0].cov(m.iloc[:, 1]) / m.iloc[:, 1].var()


def std_3y(level):
    return monthly_returns(level).tail(36).std() * np.sqrt(12)


def max_drawdown(level):
    return (level / level.cummax() - 1).min()


def vev(level, years=20):
    x = np.log(level).diff().dropna()
    s, m1, m2, n = x.std(), x.skew(), x.kurt(), 256 * years
    var = s * np.sqrt(n) * (-1.96 + 0.474 * m1 / np.sqrt(n) - 0.0687 * m2 / n + 0.146 * m1 ** 2 / n) - 0.5 * s ** 2 * n
    return (np.sqrt(3.842 - 2 * var) - 1.96) / np.sqrt(years)


def sri(v):
    for cls, upper in enumerate((0.005, 0.05, 0.12, 0.20, 0.30, 0.80), start=1):
        if v < upper:
            return cls
    return 7


def cornish_fisher(z, sigma, m1, m2, n, drift=0.0):
    return np.exp(drift * n + sigma * np.sqrt(n) * (z + (z ** 2 - 1) / 6 * m1 / np.sqrt(n) + (z ** 3 - 3 * z) / 24 * m2 / n
                                                    - (2 * z ** 3 - 5 * z) / 36 * m1 ** 2 / n) - 0.5 * sigma ** 2 * n)


def scenarios(level, entry, exit_fee, horizons=(1, 10, 20), amount=10_000):
    x = np.log(level).diff().dropna()
    mu, sigma, m1, m2 = x.mean(), x.std(), x.skew(), x.kurt()
    out = {}
    for t in horizons:
        n = 256 * t
        w = 21 if t == 1 else 63
        stressed = x.rolling(w).std().dropna().quantile(0.99 if t == 1 else 0.90)
        growth = {
            'Stress': cornish_fisher(-2.326 if t == 1 else -1.645, stressed, m1, m2, n),
            'Unfavorable': cornish_fisher(-1.28, sigma, m1, m2, n, mu),
            'Moderate': np.exp(mu * n - sigma * m1 / 6 - 0.5 * sigma ** 2 * n),
            'Favorable': cornish_fisher(1.28, sigma, m1, m2, n, mu),
        }
        out[t] = {k: amount * (1 - entry) * g * (1 - exit_fee) for k, g in growth.items()}
    return pd.DataFrame(out)


def tax_due(country, gain):
    rule = TAX[country]
    if gain <= 0:
        return 0.0
    if 'brackets' in rule:
        tax, lower = 0.0, 0.0
        for upper, rate in rule['brackets']:
            tax += max(min(gain, upper) - lower, 0) * rate
            lower = upper
        return tax
    return max(gain - rule.get('allowance', 0), 0) * rule['rate']


def portfolio_pb(h):
    h = h.dropna(subset=['price_to_book'])
    h = h[h['price_to_book'] > 0]
    return h['weight'].sum() / (h['weight'] / h['price_to_book']).sum() if len(h) else np.nan
