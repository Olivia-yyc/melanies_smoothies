# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd



# Write directly to the app
# st.title("Example Streamlit App :balloon:")
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)


# option = st.selectbox(
#     'What is your favorite fruit?',
#     ('Banana', 'Strawberries', 'Peaches'),
# )

# st.write('Your favorite fruit is:', option)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
'Choose up to 5 ingredients:'
,my_dataframe
    ,max_selections=5
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    # st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(INGREDIENTS,NAME_ON_ORDER)
            values ('""" + ingredients_string + """',
                    '""" + name_on_order+ """')"""

    time_to_insert = st.button('Submit Order')
    # st.write(my_insert_stmt)
    # st.stop()
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'+ name_on_order+'!', icon="✅")



