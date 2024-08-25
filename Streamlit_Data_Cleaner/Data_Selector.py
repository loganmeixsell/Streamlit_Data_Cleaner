from collections import Counter
import pandas as pd
import sqlite3
import streamlit as st






def get_data():
    conn = sqlite3.connect('BourbonDB.db')
    df = pd.read_sql_query("SELECT * FROM to_organize", conn)
    df_barcode = df['Barcode'].sample(n=1)
    df = df[df['Barcode'].isin(df_barcode)]
    return df, df_barcode.values[0]

def new_bottle():
    st.session_state.df, st.session_state.df_barcode = get_data()
    df = st.session_state.df
    df_barcode = st.session_state.df_barcode


if 'df' not in st.session_state:
    # st.session_state.df, st.session_state.df_barcode = get_data()
    # df = st.session_state.df
    # df_barcode = st.session_state.df_barcode
    new_bottle()
# if 'df' in st.session_state:
    # df = st.session_state.df
    # df_barcode = st.session_state.df_barcode

st.title(f"Bottle Data for barcode {st.session_state.df_barcode}")

if st.button('Get New Bottle'):
    new_bottle()

col1, col2 = st.columns(2)

with col1:
    df = st.session_state.df
    title_list = df['title'].tolist()
    title_list = list(dict.fromkeys(title_list))
    distillery_list = df['Distillery'].tolist()
    distillery_list = list(dict.fromkeys(distillery_list))
    category_list = df['category'].tolist()
    category_list = list(dict.fromkeys(category_list))
    series_list = df['Bottling serie'].tolist()
    series_list = list(dict.fromkeys(series_list))
    size_list = df['Size'].tolist()
    size_list = list(dict.fromkeys(size_list))
    image_list = df['image'].tolist()
    image_list = list(dict.fromkeys(image_list))
    image_list = [sub_item for item in image_list for sub_item in item.split(',')]

    with st.form("bottle_form"):
        title = st.radio(
            "What should the title be?",
            title_list,
        )

        distillery = st.radio(
            "What's should the distillery be?",
            distillery_list,
        )

        category = st.radio(
            "What's should the category be?",
            category_list,
        )

        series = st.radio(
            "What's should the series be?",
            series_list,
        )

        size = st.radio(
            "What's should the size be?",
            size_list,
        )

        image = st.selectbox(
            "What should the image be?",
            list(range(1, len(image_list) + 1)),
        )
        submitted = st.form_submit_button("Submit")
        if submitted:
            print(st.session_state.df_barcode)
            data = {
                'Barcode': [st.session_state.df_barcode],
                'Title': [title],
                'Distillery': [distillery],
                'Category': [category],
                'Series': [series],
                'Size': [size],
                'Image': [image_list[image - 1]]
                    }
            
            # Write to Database
            df_submitted = pd.DataFrame(data)
            conn = sqlite3.connect('BourbonDB.db')
            df_submitted.to_sql('submitted_bottles', conn, if_exists='append', index=False)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM to_organize WHERE Barcode = ?", (st.session_state.df_barcode,))
            conn.commit()
            conn.close()

            st.write("title:", title, "distillery:", distillery, "category:", category, "series:", series, "size:", size, "image:", image_list[image - 1])

with col2:
    if len (image_list) == 1:
        st.image(image_list[0], caption=f"Image 1, {image_list[0]}")
    else:
        image_index = st.slider("Select Image", 1, len(image_list), 1)
        st.image(image_list[image_index - 1], caption=f"Image {image_index}, {image_list[image_index - 1]}")
        # st.image(ele, caption = f"Image {count + 1}, {ele}")

