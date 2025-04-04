from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('Relatorio_Cadop')  
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/search', methods=['GET'])
def search_operadoras():
    query = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Relatorio_Cadop
        WHERE Razao_Social LIKE ? OR Nome_Fantasia LIKE ? OR Modalidade LIKE ?
        LIMIT 10
    """, (f'%{query}%', f'%{query}%', f'%{query}%'))
    
    results = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in results])

if __name__ == '__main__':
    app.run(debug=True)