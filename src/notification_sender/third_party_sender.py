# -*- coding: utf-8 -*-
"""
第三方 发送提醒服务
"""
import logging
import requests

from src.config import Config
from pathlib import Path
from datetime import datetime

from src.md2pdf import markdown_to_pdf

logger = logging.getLogger(__name__)


class ThirdPartySender:

    def __init__(self, config: Config):
        """
        初始化第三方配置

        Args:
            config: 配置对象
        """
        self._third_party_url = config.third_party_webhook_url
        self._third_party_token = config.third_party_token

    def send_to_third_party(self, content: str) -> bool:
        if not self._third_party_url:
            logger.warning("第三方 Webhook 未配置，跳过推送")
            return False
        return self._send_third_party_file(content)

    def _send_third_party_file(self, content: str):
        reports_dir = Path(__file__).parent.parent.parent / 'reports'
        reports_dir.mkdir(parents=True, exist_ok=True)
        date_str = datetime.now().strftime('%Y%m%d')
        is_market_report = '🎯 大盘复盘' in content

        file_name = f"market_review_{date_str}.md" if is_market_report else f"report_{date_str}.md"
        file_path = reports_dir / file_name
        if not file_path.exists():
            logger.error('报告未生产，无法推送')
            return False
        # 上传文件
        response = None
        if not is_market_report:
            with open(file_path, 'rb') as file_bin:
                files = {'file': file_bin}
                response = requests.post(self._third_party_url, data={
                    'file_name': f'大盘复盘_{date_str}.md' if is_market_report else f'决策仪表盘_{date_str}.md'},
                                         files=files,
                                         headers={'Authorization': self._third_party_token})
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                markdown = f.read()
            file_stream = markdown_to_pdf(markdown, key=f'大盘复盘_{date_str}.pdf')
            response = requests.post(self._third_party_url,
                                     data={
                                         'file_name': f'大盘复盘_{date_str}.pdf' if is_market_report else f'决策仪表盘_{date_str}.pdf'
                                     },
                                     files={'file': (
                                         f'大盘复盘_{date_str}.pdf' if is_market_report else f'决策仪表盘_{date_str}.pdf',
                                         file_stream, 'application/pdf')
                                     },
                                     headers={'Authorization': self._third_party_token})

        if response and response.status_code == 200:
            result = response.json()
            if result.get('success'):
                logger.info("第三方推送报告成功")
                return True
            else:
                logger.error(f"第三方推送回错误: {result}")
        else:
            if response:
                logger.error(f"第三方请求失败: {response.status_code}")
            else:
                logger.error(f"第三方请求失败: No Response")
        return False
