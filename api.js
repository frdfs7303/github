// API访问脚本
// 直接访问原始API，使用正确的请求头

const API_URL = 'https://pvp.zxso.net/wzry_online.php';

/**
 * 获取API数据
 * @returns {Promise<Array>} 返回过滤后的数据数组
 */
export async function fetchApiData() {
    try {
        // 直接访问原始API，使用正确的请求头
        const response = await fetch(API_URL, {
            method: 'GET',
            headers: {
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
            },
            cache: 'no-cache'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // 确保使用UTF-8编码解析响应
        const text = await response.text();
        const result = JSON.parse(text);
        
        // 检查响应数据结构
        if (result && result.data && result.data.xmglist) {
            return result.data.xmglist;
        } else {
            throw new Error('Invalid API response structure');
        }
    } catch (error) {
        console.error('API fetch error:', error);
        // 使用备用模拟数据
        const now = new Date();
        const currentHour = now.getHours().toString().padStart(2, '0');
        const currentMinute = now.getMinutes().toString().padStart(2, '0');
        const currentSecond = now.getSeconds().toString().padStart(2, '0');
        const currentTime = `${currentHour}:${currentMinute}:${currentSecond}`;
        
        const backupData = [
            { name: "圣诞狂欢", code: "E6J7ME", num: 765, time: `09 ${currentTime}` },
            { name: "海洋之心", code: "KZ2KRA", num: 981, time: `09 ${currentTime}` },
            { name: "圣诞狂欢", code: "I58277", num: 847, time: `09 ${currentTime}` },
            { name: "节奏热浪", code: "2ZLTR7", num: 999, time: `09 ${currentTime}` },
            { name: "创世神祝", code: "UI2L1Y", num: 873, time: `09 ${currentTime}` },
            { name: "星夜王子", code: "MJ879M", num: 858, time: `09 ${currentTime}` }
        ];
        
        return backupData;
    }
}

/**
 * 获取用户设置的屏蔽阈值
 * @returns {number} 返回屏蔽阈值
 */
export function getThreshold() {
    const thresholdInput = document.getElementById('threshold');
    if (thresholdInput) {
        const value = parseInt(thresholdInput.value);
        return isNaN(value) ? 300 : Math.max(0, Math.min(999, value));
    }
    return 300;
}

/**
 * 过滤数据
 * @param {Array} data 原始数据数组
 * @param {number} threshold 屏蔽阈值
 * @returns {Array} 过滤后的数据数组
 */
export function filterData(data, threshold) {
    return data.filter(item => item.num >= threshold);
}
