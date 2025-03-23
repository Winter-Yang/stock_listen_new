import requests
import time
import threading
from limitUpClass import LimitUpStock
from limitUpNotice import LimitUpNotice
from stockDailyLines import StockKlineRquest
from stockDailyLines import StockKline

class LimitUpPool:
    def __init__(self):
        self.limit_up_stocks = {}  # 用字典存储涨停股票数据，key为symbol
        self.api_url = 'https://flash-api.xuangubao.com.cn/api/pool/detail?pool_name=limit_up'
        self.is_running = False
        self.thread = None

    def fetch_limit_up_stocks(self):
        try:
            print("正在获取数据...")
            response = requests.get(self.api_url)
            if response.status_code == 200:
                data = response.json()
                
                # 过滤ST股票并处理新数据
                for item in data['data']:
                    if 'st' not in item['stock_chi_name'].lower():
                        symbol = item['symbol']
                        # 比对并添加新数据
                        if symbol not in self.limit_up_stocks:
                            stock = LimitUpStock(item)
                            self.limit_up_stocks[symbol] = LimitUpStock(item)
                            print(f"新增股票: {symbol} 涨停, 名称: {item['stock_chi_name']}")
                            stockLine = StockKlineRquest.get_kline_data(symbol)
                            stock.is_break_60_high = stockLine.is_break_60_high
                            stock.is_break_125_high = stockLine.is_break_125_high
                            LimitUpNotice.wxpusher_notice(stock)
                    time.sleep(0.3)
                return self.limit_up_stocks
            else:
                print(f'请求失败，状态码: {response.status_code}')

        except Exception as error:
            print('获取涨停池数据失败:', str(error))

    def start_monitoring(self):
        """开始监控"""
        if self.is_running:
            print("监控已经在运行中")
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._monitor_task)
        self.thread.daemon = True
        self.thread.start()
        print("开始监控涨停池数据...")

    def stop_monitoring(self):
        """停止监控"""
        self.is_running = False
        if self.thread:
            self.thread.join()
        print("停止监控涨停池数据")

    def _monitor_task(self):
        """监控任务"""
        while self.is_running:
            self.fetch_limit_up_stocks()
            time.sleep(5)  # 每30秒请求一次


# 使用示例
if __name__ == "__main__":
    pool = LimitUpPool()
    try:
        # 开始监控
        pool.start_monitoring()
        
        # 保持程序运行
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        # 当按下Ctrl+C时停止监控
        pool.stop_monitoring()
        print("程序已停止")