# -*- coding: utf-8 -*-
"""Telegram 机器人通知模块，供夸克网盘自动签到脚本调用"""
import os
import html

import httpx
from loguru import logger

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")


def send_tg(message: str) -> bool:
    """
    通过 Telegram Bot API 发送消息
    :param message: 消息文本（支持 HTML 标签，如 <b>加粗</b>）
    :return: 发送成功返回 True，失败返回 False（不影响主流程）
    """
    if not TG_BOT_TOKEN or not TG_CHAT_ID:
        logger.warning("未配置 TG_BOT_TOKEN / TG_CHAT_ID，跳过 Telegram 通知")
        return False

    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": message[:4096],  # Telegram 单条消息上限 4096 字符
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    try:
        resp = httpx.post(url, json=payload, timeout=15)
        result = resp.json()
        if result.get("ok"):
            logger.success("Telegram 通知发送成功")
            return True
        logger.error(f"Telegram 通知发送失败: {result}")
    except Exception as e:
        logger.error(f"Telegram 通知请求异常: {e}")
    return False


def escape(text) -> str:
    """转义动态内容（如用户名），防止特殊字符破坏 HTML 解析"""
    return html.escape(str(text))


if __name__ == "__main__":
    # 本地测试：设置 TG_BOT_TOKEN 和 TG_CHAT_ID 环境变量后执行 python tg_notify.py
    send_tg("<b>夸克签到</b> Telegram 通知测试 ✅")
