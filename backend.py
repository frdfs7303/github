from flask import Flask, jsonify
from flask_cors import CORS
import requests
import json
import time
import threading

app = Flask(__name__)
# 启用CORS支持，允许所有来源的请求
CORS(app, resources={r"/*": {"origins": "*"}})

# API URL
API_URL = 'https://pvp.zxso.net/wzry_online.php'

# 缓存最新的数据
latest_data = None
last_fetch_time = 0

# 使用指定的请求头
REQUEST_HEADERS = {
    'Host': 'pvp.zxso.net',
    'Connection': 'keep-alive',
    'sec-ch-ua-platform': '"Windows"',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://pvp.zxso.net/online.html',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '_pk_id.6.5811=4a288b46efd1da32.1770633748.; _pk_ses.6.5811=1'
}

# 获取API数据的函数
def fetch_api_data():
    global latest_data, last_fetch_time
    try:
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Fetching data from API...')
        print(f'Using API URL: {API_URL}')
        print(f'Using headers: {REQUEST_HEADERS}')
        
        # 使用requests库发送GET请求，使用指定的请求头
        # 注意：requests会自动处理压缩的响应，不需要手动处理
        # 移除Accept-Encoding头，让requests自动处理压缩
        headers = REQUEST_HEADERS.copy()
        headers.pop('Accept-Encoding', None)
        
        response = requests.get(API_URL, headers=headers, timeout=10, verify=True)
        response.raise_for_status()
        
        # 确保响应是UTF-8编码
        response.encoding = 'utf-8'
        
        # 打印响应状态码和头部信息
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Response status code:', response.status_code)
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Response headers:', dict(response.headers))
        
        try:
            # 尝试解析响应数据
            data = response.json()
            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] API response received:', data)
        except json.JSONDecodeError as e:
            # JSON解析失败，打印响应内容
            response_text = response.text
            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] JSON decode error:', str(e))
            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Response text:', response_text)
            raise
        
        # 验证数据结构
        if not isinstance(data, dict):
            raise ValueError('Invalid response format: expected dict')
        
        if data.get('code') != 200:
            raise ValueError(f'API returned error: {data.get("msg", "Unknown error")}')
        
        if not data.get('data') or not data['data'].get('xmglist'):
            raise ValueError('Invalid data structure: missing xmglist')
        
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Data validated successfully')
        
        # 更新缓存
        latest_data = data
        last_fetch_time = time.time()
        
        return data
    except requests.exceptions.RequestException as e:
        error_msg = f'Request error: {str(e)}'
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] {error_msg}')
        # 返回错误信息
        return {
            'code': 500,
            'msg': '获取数据失败',
            'error': error_msg
        }
    except ValueError as e:
        error_msg = f'Data validation error: {str(e)}'
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] {error_msg}')
        # 返回错误信息
        return {
            'code': 500,
            'msg': '数据验证失败',
            'error': error_msg
        }
    except Exception as e:
        error_msg = f'Unexpected error: {str(e)}'
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] {error_msg}')
        # 返回错误信息
        return {
            'code': 500,
            'msg': '获取数据失败',
            'error': error_msg
        }

# 定期更新数据的线程函数
def update_data_thread():
    while True:
        try:
            fetch_api_data()
            # 每5秒更新一次
            time.sleep(5)
        except Exception as e:
            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Error in update thread:', str(e))
            # 出错后暂停2秒再继续
            time.sleep(2)

# 初始化时获取一次数据
fetch_api_data()

# 启动后台线程定期更新数据
update_thread = threading.Thread(target=update_data_thread, daemon=True)
update_thread.start()
print('Data update thread started')

@app.route('/api/data', methods=['GET'])
def get_data():
    global latest_data
    print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Frontend request received, returning latest data')
    # 直接返回最新的缓存数据，由后台线程负责更新
    return jsonify(latest_data)

if __name__ == '__main__':
    app.run(port=5000, debug=False)  # 生产环境关闭debug模式