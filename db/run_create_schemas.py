import psycopg2

sql_file_path = ('db/create_schemas.sql')

with open(sql_file_path, 'r') as file:
    sql_commands = file.read()

def execute_sql_commands(commands):
    try:
        conn = psycopg2.connect(
            dbname="dancingpony",
            user="dancingponysvc",
            password="password",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        cur.execute(commands)

        conn.commit()

        cur.close()
        conn.close()

        print("Schema created successfully")

    except Exception as e:
        print(f"Error: {e}")

execute_sql_commands(sql_commands)
