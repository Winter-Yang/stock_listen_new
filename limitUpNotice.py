# from dingtalkchatbot.chatbot import DingtalkChatbot
from limitUpClass import LimitUpStock
import requests
class LimitUpNotice:
    # 钉钉机器人的 webhook 地址
    WEBHOOK = "你的钉钉机器人Webhook地址"


    @staticmethod
    def wxpusher_notice(stock: LimitUpStock):
        """
        通过WxPusher发送涨停股票通知
        """
        try:
            # WxPusher配置
            app_token = "你的APP_TOKEN"
            topic_ids = [123]  # 你的主题ID
            
            # 构建HTML内容
            content = f"""
<h3>{stock.stock_chi_name}({stock.symbol})涨停</h3>

<ul>
    <li style=\"color:red;\">涨跌幅：{stock.change_percent * 100:.2f}%</li>
    <li style=\"color:red;\">换手率：{stock.turnover_ratio * 100:.2f}%</li>
    <li style=\"color:red;\">连续涨停天数：{stock.limit_up_desc}</li>
    <li style=\"color:{"red" if stock.is_break_60_high else ""}\">是否60日新高：{"是" if stock.is_break_60_high else "否"}</li>
    <li style=\"color:{"red" if stock.is_break_125_high else ""}\">是否125日新高：{"是" if stock.is_break_125_high else "否"}</li>
    <li >当前价格：{stock.price}</li>
    <li >封单率：{stock.buy_lock_volume_ratio * 100:.2f}%</li>
    <li >总市值：{stock.total_capital/100000000:.2f}亿</li>
</ul>

<h4>涨停原因</h4>
<p>{stock.surge_reason.stock_reason}</p>

<h4>相关板块</h4>
<ul>
"""
            # 添加相关板块信息
            for plate in stock.surge_reason.related_plates:
                content += f"<li style=\"color:red;\">{plate.plate_name}"
                if plate.plate_reason:
                    content += f"<br/>原因：{plate.plate_reason}"
                content += "</li>"
            
            content += "</ul>"

            # 构建请求数据
            data = {
                "appToken": "AT_qMIL5otiWGB5XSMnPfqfjf9rnnfbI0be",
                "content": content,
                "summary": f"{stock.stock_chi_name} 涨停通知",
                "contentType": 2,
                "topicIds": topic_ids,
                "verifyPayType": 0,
                "uids":[
                    "UID_oD9256GbIWa2fE53QkA3fIHPAlcL"
                ],
                "url": f"{stock.url}"
            }

            # 发送请求
            response = requests.post(
                "http://wxpusher.zjiecode.com/api/send/message",
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print(f"WxPusher通知发送成功：{stock.stock_chi_name}")
                    print("")
                else:
                    print(f"WxPusher通知发送失败：{result.get('msg')}")
            else:
                print(f"WxPusher请求失败，状态码：{response.status_code}")

        except Exception as e:
            print(f"发送WxPusher通知失败: {str(e)}")











#     @staticmethod
#     def dingtalk_robot(title: str,content:str):
#         webhook = 'https://oapi.dingtalk.com/robot/send?access_token=d05f3d9ae31963dd0f6d2dcd9b103bf70886611419607f9127daacc176012bec'
#         secrets = 'SEC1b7f4a01121185daf824f007361bfe03f95f8c12e08964dd2b7b44c6077cef1d'
#         dogBOSS = DingtalkChatbot(webhook, secrets)
#         dogBOSS.send_markdown(title=title, text=content)

#     @staticmethod
#     def send_limit_up_notice(stock: LimitUpStock):
#         """
#         发送涨停股票通知到钉钉群
#         """
#         try:
#             # 创建钉钉机器人实例
#             ding = DingtalkChatbot(LimitUpNotice.WEBHOOK)
            
#             # 构建 markdown 格式的消息
#             title = f"新涨停股票通知 - {stock.stock_chi_name}"
            
#             # 构建消息内容
#             content = f"""
# ### {stock.stock_chi_name}（{stock.symbol}）涨停

# - 当前价格：{stock.price}
# - 涨跌幅：{stock.change_percent:.2f}%
# - 换手率：{stock.turnover_ratio:.2f}%
# - 封单率：{stock.buy_lock_volume_ratio:.2f}%
# - 连续涨停天数：{stock.limit_up_days}天
# - 总市值：{stock.total_capital/100000000:.2f}亿

# #### 涨停原因
# {stock.surge_reason.stock_reason}

# #### 相关板块
# """
#             # 添加相关板块信息
#             for plate in stock.surge_reason.related_plates:
#                 content += f"- {plate.plate_name}\n"
#                 if plate.plate_reason:
#                     content += f"  - 原因：{plate.plate_reason}\n"
            
#             # 发送消息
#             # ding.send_markdown(title=title, text=content)
#             print(f"已发送 {stock.stock_chi_name} 的涨停通知 {content}")
            
#         except Exception as e:
#             print(f"发送钉钉通知失败: {str(e)}")