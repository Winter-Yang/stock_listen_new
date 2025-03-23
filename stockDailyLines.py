from typing import List, Dict, Any
from dataclasses import dataclass
import requests

@dataclass
class KlineData:
    open_px: float
    close_px: float
    high_px: float
    low_px: float
    average_px: float
    px_change: float
    px_change_rate: float
    turnover_volume: int
    turnover_value: float
    tick_at: int
    avg_px: float
    ma5: float
    ma10: float
    ma20: float
    ma60: float
    turnover_ratio: float

class StockKline:
    symbol:str
    lines: List[KlineData]
    is_break_60_high: bool
    is_break_125_high: bool

    def __init__(self, data: dict):
        self.symbol = list(data['candle'].keys())[0]
        
        # 转换并倒序排列lines数据
        self.lines = [
            KlineData(*line) for line in data['candle'][self.symbol]['lines']
        ]
        self.lines.reverse()  # 倒序排列
        
        # 计算是否60日和125日新高
        self.is_break_60_high = self._is_break_high(60)
        self.is_break_125_high = self._is_break_high(125)

    def _calculate_max_close(self, days: int) -> float:
        """计算指定天数内的最高收盘价"""
        if len(self.lines) < days:
            return 0.0
        
        return max(line.close_px for line in self.lines[1:days])  # 不包含最新一天

    def _is_break_high(self, days: int) -> bool:
        """判断最新收盘价是否突破指定天数的最高价"""
        if len(self.lines) < days:
            return False
        max_close = self._calculate_max_close(days)
        current_close = self.lines[0].close_px if self.lines else 0.0
        return current_close >= max_close

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> 'StockKline':
        """从JSON数据创建实例"""
        return cls(json_data['data'])






class StockKlineRquest:
    # BASE_URL = "https://api-ddc-wscn.xuangubao.com.cn/market/kline"
    @staticmethod
    def get_kline_data(symbol: str, tick_count: int = 250) -> StockKline:
        """
        获取股票K线数据
        :param symbol: 股票代码（如：002278.SZ）
        :param tick_count: 获取的K线数量
        :return: StockKline对象
        """
        try:
            params = {
                "tick_count": tick_count,
                "prod_code": symbol,
                "adjust_price_type": "forward",
                "period_type": 86400,
                "fields": ",".join([
                    "tick_at", "open_px", "close_px", "high_px", "low_px",
                    "turnover_volume", "turnover_value", "turnover_ratio",
                    "average_px", "px_change", "px_change_rate", "avg_px",
                    "business_amount", "business_balance",
                    "ma5", "ma10", "ma20", "ma60"
                ])
            }
            
            response = requests.get("https://api-ddc-wscn.xuangubao.com.cn/market/kline", params=params)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 20000:
                    return StockKline(data['data'])
                else:
                    raise Exception(f"API返回错误: {data.get('message')}")
            else:
                raise Exception(f"请求失败，状态码: {response.status_code}")
                
        except Exception as e:
            print(f"获取K线数据失败: {str(e)}")
            return None