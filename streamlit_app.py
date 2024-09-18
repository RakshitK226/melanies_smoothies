# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched





# Write directly to the app
st.title("Customize Your Smoothie")
st.write(
    "Choose the fruits you want in your custom smoothie"
)

import streamlit as st

title = st.text_input('Movie Title', 'Life of Brian')
st.write('The current movie title is:', title)
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe,max_selections = 5)

if ingredients_list:


    ingredients_string = ''
    name_on_order = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '
        
    st.write(ingredients_string)
    st.write(name_on_order)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
    values('""" + ingredients_string + """','"""+ name_on_order + """')"""

    st.write(my_insert_stmt)
    time_to_insert = st.button('Submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
        st.success('Your Smoothie is ordered!', icon="✅")
