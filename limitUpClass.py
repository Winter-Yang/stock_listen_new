from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TimelineItem:
    timestamp: datetime
    status: str

@dataclass
class RelatedPlate:
    plate_id: str
    plate_name: str
    plate_reason: str

@dataclass
class SurgeReason:
    stock_reason: str
    related_plates: List[RelatedPlate]

    def __init__(self, data: dict):
        self.stock_reason = data.get('stock_reason', '')
        related_plates = data.get('related_plates', []);
        if len(related_plates) > 0:
            self.related_plates = [
                RelatedPlate(
                    plate_id=plate.get('plate_id', ''),
                    plate_name=plate.get('plate_name', ''),
                    plate_reason=plate.get('plate_reason','')
                ) for plate in related_plates
            ]
        else:
            self.related_plates = []

@dataclass
class LimitUpStock:
    buy_lock_volume_ratio: float
    change_percent: float
    first_limit_up: datetime
    last_limit_down: datetime
    last_limit_up: datetime
    limit_timeline: dict
    limit_up_days: int
    m_days_n_boards_boards: int
    m_days_n_boards_days: int
    non_restricted_capital: float
    price: float
    stock_chi_name: str
    surge_reason: SurgeReason
    symbol: str
    total_capital: float
    turnover_ratio: float
    yesterday_limit_up_days: int
    is_break_60_high: bool
    is_break_125_high: bool

    def __init__(self, data: dict):
        self.buy_lock_volume_ratio = data.get('buy_lock_volume_ratio', 0.0)
        self.change_percent = data.get('change_percent', 0.0)
        self.first_limit_up = data.get('first_limit_up')
        self.last_limit_down = data.get('last_limit_down')
        self.last_limit_up = data.get('last_limit_up')
        self.limit_timeline = {
            'items': [TimelineItem(**item) for item in data.get('limit_timeline', {}).get('items', [])]
        }
        self.limit_up_days = data.get('limit_up_days', 0)
        self.m_days_n_boards_boards = data.get('m_days_n_boards_boards', 0)
        self.m_days_n_boards_days = data.get('m_days_n_boards_days', 0)
        self.non_restricted_capital = data.get('non_restricted_capital', 0.0)
        self.price = data.get('price', 0.0)
        self.stock_chi_name = data.get('stock_chi_name', '')
        self.surge_reason = SurgeReason(data.get('surge_reason', {}))
        self.symbol = data.get('symbol', '')
        self.total_capital = data.get('total_capital', 0.0)
        self.turnover_ratio = data.get('turnover_ratio', 0.0)
        self.yesterday_limit_up_days = data.get('yesterday_limit_up_days', 0)
        self.url = ''
        self.setUrl(self.symbol)
        self.limit_up_desc = ''  # 新增涨停描述属性
        self.setLimitUpDesc()  # 初始化时设置涨停描述


    def setUrl(self, symbol: str):
        # 替换.SS为.SH
        if '.SS' in symbol:
            symbol = symbol.replace('.SS', '.SH')
        
        # 分割获取股票代码
        prefix = symbol.split('.')[-1]
        code = symbol.split('.')[0]
        # 生成雪球URL
        self.url = f"https://xueqiu.com/S/{prefix}{code}"

    def setLimitUpDesc(self):
        """设置涨停描述"""
        if (self.limit_up_days == self.m_days_n_boards_days and 
            self.m_days_n_boards_days == self.m_days_n_boards_boards):
            self.limit_up_desc = f"{self.limit_up_days}连板"
        elif self.limit_up_days == 1 and self.m_days_n_boards_days == 0:
            self.limit_up_desc = "首板"
        elif self.m_days_n_boards_days > self.m_days_n_boards_boards:
            self.limit_up_desc = f"{self.m_days_n_boards_days}天{self.m_days_n_boards_boards}板"
        else:
            self.limit_up_desc = "Error"
