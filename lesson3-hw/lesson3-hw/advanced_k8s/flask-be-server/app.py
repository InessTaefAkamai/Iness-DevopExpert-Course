import os
from flask import Flask, request, jsonify
import psycopg2
import redis
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Function to get a database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB', 'dbname'),
        user=os.getenv('POSTGRES_USER', 'dbuser'),
        password=os.getenv('POSTGRES_PASSWORD', 'password'),
        host=os.getenv('POSTGRES_HOST', 'postgres-service')
    )
    return conn

# Connect to Redis
cache = redis.Redis(host=os.getenv('REDIS_HOST', 'redis-service'), port=6379)

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/data/<key>', methods=['PUT'])
def update_data(key):
    data = request.json
    value = data.get('value')

    update_query = """
    UPDATE your_table
    SET column2 = %s
    WHERE column1 = %s;
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(update_query, (value, key))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'key': key, 'value': value}), 200
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/data', methods=['POST'])
def insert_data():
    data = request.json
    column1 = data.get('column1')
    column2 = data.get('column2')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO your_table (column1, column2) 
        VALUES (%s, %s)
        ON CONFLICT (id) DO UPDATE SET column1 = EXCLUDED.column1, column2 = EXCLUDED.column2
        """, (column1, column2))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success'})
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/data', methods=['GET'])
def get_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM your_table")
        rows = cursor.fetchall()
        # Format data for JSON response
        data = [{'id': row[0], 'column1': row[1], 'column2': row[2]} for row in rows]
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
