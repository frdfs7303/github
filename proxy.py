from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # 启用CORS

@app.route('/api/wzry', methods=['GET'])
def get_wzry_data():
    try:
        url = 'https://pvp.zxso.net/wzry_online.php'
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({'code': 500, 'msg': '获取数据失败', 'error': str(e)})

if __name__ == '__main__':
    app.run(port=5000, debug=True)