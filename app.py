import streamlit as st

from bloco import fund_page
from bloco.data import FUNDS
from bloco.pages import about, products

st.set_page_config(page_title='BlocoRocha', page_icon='assets/favicon.svg', layout='wide')


def early_growth():
    fund_page.render('early_growth')


def momentum_growth():
    fund_page.render('momentum_growth')


pages = [
    st.Page(products, title='Products | BlocoRocha', url_path='products', default=True),
    st.Page(early_growth, title=f"{FUNDS['early_growth']['name']} | BlocoRocha", url_path=FUNDS['early_growth']['path']),
    st.Page(momentum_growth, title=f"{FUNDS['momentum_growth']['name']} | BlocoRocha", url_path=FUNDS['momentum_growth']['path']),
    st.Page(about, title='About us | BlocoRocha', url_path='about-us'),
]
st.navigation(pages, position='hidden').run()


