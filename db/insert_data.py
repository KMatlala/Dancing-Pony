import psycopg2
import json
import os
import base64
from loguru import logger



json_file_path = ('examples/dishes.json')

img_dir = ('examples/img')

with open(json_file_path, 'r') as file:
    logger.info("Loading dishes.json file...")
    try:
        dishes = json.load(file)
        if dishes:
            logger.success(f"Dishes.json file loaded successfully and contains {len(dishes)} dishes.")
        else:
            logger.warning("Dishes.json file is empty.")
    except Exception as e:
        logger.critical(f"Error loading dishes.json file: {e}")
        exit(-1)
        
for dish in dishes:
    image_path = os.path.join(img_dir, f"{dish['name'].replace(' ', '_')}.png")
    try:
        logger.info(f"Encoding image for {image_path}...")
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            dish['image'] = encoded_string
            logger.success(f"Image for {dish['name']} encoded successfully.")
    except Exception as e:
        logger.warning(f"Warning: Image for {dish['name']} not found: {e}")

try:
    conn = psycopg2.connect(
        dbname="dancingpony",
        user="dancingponysvc",
        password="password",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    insert_query = """
    INSERT INTO dish (name, description, price, image, rating)
    VALUES (%s, %s, %s, %s, %s)
    """

    for dish in dishes:
        cur.execute(insert_query, (dish['name'], dish['description'], dish['price'], dish['image'], dish['rating']))

    conn.commit()

    cur.close()
    conn.close()

    logger.success("Data inserted successfully")

except Exception as e:
    logger.error(f"Error: {e}")
