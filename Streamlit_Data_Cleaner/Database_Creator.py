import pandas as pd
import sqlite3

# conn = sqlite3.connect('BourbonDB.db')
# cursor = conn.cursor()


def make_table():
    conn = sqlite3.connect('BourbonDB.db')
    cursor = conn.cursor()
    df = pd.read_csv(r'D:\Python\Files\whiskey_data_06-08-2024_grouped.csv')
    df.to_sql('to_organize', conn, if_exists='replace', index=False)

def reset_data():
    conn = sqlite3.connect('BourbonDB.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM submitted_bottles")
    conn.commit()
    cursor.execute("DELETE FROM to_organize")
    conn.commit()
    conn.close()

def drop_table(table):
    conn = sqlite3.connect('BourbonDB.db')
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE {table}")
    conn.commit()
    conn.close()

if __name__ == '__main__':  
    # reset_data()
    # make_table()
    drop_table('submitted_bottles')