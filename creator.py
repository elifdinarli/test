#!/usr/bin/env python
# coding: utf-8

# In[9]:


import streamlit as st
import requests as r
import pandas as pd
from datetime import datetime
import time


# In[4]:


st.title("Offer Page Creator")


# In[11]:


#offer cards

core_offers = [{"name": "6 Months SSA with 40% VP", "contentful_id": "55rB8DBmaCBeDFrGTd6CmP"}, 
               {"name": "12 Months SSA with 60% VP", "contentful_id": "2XFp1bQltXlSVcZzw7wcK3"},
               {"name": "Lifetime with 60%", "contentful_id": "4YFFAEDbVFfG4u3pS8fRd"},
               {"name": "Lifetime with 50%", "contentful_id": "LFHguuPrYK85BSguaJN3K"},
               {"name": "24 Months with 40% VP", "contentful_id": "2pBxckHdSB2V1mrUijDgZx"}]


# In[12]:


#finding pricing plan id

def pricing_plan(name, offers):
    for offer in offers:
        if offer["name"] == name:
            return offer["contentful_id"]
    return None  # Return None if no match is found


# In[8]:


user = st.text_input("Please enter your Babbel email to start")


# In[ ]:


if user:
  st.write('thanks')
elif not user:
    st.warning('Please input your email')
    st.stop()


# In[ ]:


offer_tab, content_tab = st.tabs(["Offers Tab", "Content Tab"])
offer_tab.write("This tab is for setting up the offers")
content_tab.write("This tab is for the page body")


# In[12]:


with offer_tab:
    nbr_offer = st.slider("How many offers do you want to show?", 1, 5)
    if not nbr_offer:
        st.warning('Please select')
        st.stop()
    elif nbr_offer == 1:
        with st.form("single_offer"):
            offer_1 = st.selectbox("Select the first offer:", ["6 Months SSA with 40% VP","12 Months SSA with 60% VP", "Lifetime with 60%", "Lifetime with 50%","24 Months with 40% VP"])
            offer_1_code = st.text_input("Please enter the offer code for the first offer")
            submit_button = st.form_submit_button(label='Done')
            if submit_button:
                st.write("Thank you! Now you can proceed to the content tab.")
                selected_offers= [dict({'offer': offer_1 ,'offer_code': offer_1_code})]
    elif nbr_offer == 2:
        with st.form("2_offers"):
            offer_1 = st.selectbox("Select the first offer:", ["6 Months SSA with 40% VP","12 Months SSA with 60% VP", "Lifetime with 60%", "Lifetime with 50%","24 Months with 40% VP"])
            offer_1_code = st.text_input("Please enter the offer code for the first offer")
            offer_2 = st.selectbox("Select the second offer:", ["6 Months SSA with 40% VP","12 Months SSA with 60% VP", "Lifetime with 60%", "Lifetime with 50%","24 Months with 40% VP"])
            offer_2_code = st.text_input("Please enter the offer code for the second offer")
            submit_button = st.form_submit_button(label='Done')
            if submit_button:
                st.write("Thank you! Now you can proceed to the content tab.")
                selected_offers= [dict({'offer': offer_1 ,'offer_code': offer_1_code}), dict({'offer': offer_2 ,'offer_code': offer_2_code})]
    else:
        "for now you can only use up to 2 offers"


# In[22]:


def offer_card(offer, offer_code):
    plan = pricing_plan(offer, core_offers)
    plan = {'fields': {'entryTitle': {'en-US': "offer card test"},
            'pricingPlan': {'en-US': {'sys': {'type': 'Link',
           'linkType': 'Entry',
           'id': plan}}},      
          'offerName': {'en-US': offer_code}}}
    create = r.post("https://api.contentful.com/spaces/zuzqvf4m2o58/environments/master/entries", headers=headers, json=plan)
    result = create.json()
    return(result['sys']['id'])


# In[ ]:


with content_tab:
    st.write("I will decide what to show on the content for now")
    with st.form("page_details"):
        language = st.selectbox("Please select the display language", ["en_gb"])
        slug = st.text_input("Please enter a slug for your page")
        content = st.multiselect("What do you want to highlight on the page body?", ["Babbel Live", "Babbel Core", "User reviews"])
        submit_button = st.form_submit_button(label='Create')
        if submit_button:
            st.write('Thank you for your input! Your page is ready: please preview, make the changes if necessary and then publish')
            st.link_button("Preview the page", "https://content-hub-gatsby-preview.babbel.com/de/pages/de-de/elif-rebranding-testing/")
            st.link_button("Go to Contentful editor", "https://app.contentful.com/spaces/zuzqvf4m2o58/entries/4ixOoqr0hyWKnh1kK7nvkW?focusedField=entryTitle")

