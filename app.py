import streamlit as st

from bloco import fund_page
from bloco.data import FUNDS
from bloco.pages import about, products


def early_growth():
    fund_page.render('early_growth')


def momentum_growth():
    fund_page.render('momentum_growth')


pages = [
    st.Page(products, title='Products', url_path='products', default=True),
    st.Page(early_growth, title=FUNDS['early_growth']['name'], url_path=FUNDS['early_growth']['path']),
    st.Page(momentum_growth, title=FUNDS['momentum_growth']['name'], url_path=FUNDS['momentum_growth']['path']),
    st.Page(about, title='About us', url_path='about-us'),
]
st.navigation(pages, position='hidden').run()
