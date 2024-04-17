# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title("Customize Your Smoothie  :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smoothie
    """
)
from snowflake.snowpark.functions import col


name_on_order = st.text_input('Name on smoothie')
st.write('Name on your smoothie will be:',name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:'
    , my_dataframe
    )
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ''    
    #st.write(ingredients_string)
    
my_insert_stmt = """ 
    INSERT INTO smoothies.public.orders(ingredients, name_on_order)
    VALUES ('""" + ingredients_string + """','""" + name_on_order + """')
"""

#st.write(my_insert_stmt)
#st.stop()
time_to_insert = st.button("SubmitOrders")
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered(name_on_order)!', icon="✅")
