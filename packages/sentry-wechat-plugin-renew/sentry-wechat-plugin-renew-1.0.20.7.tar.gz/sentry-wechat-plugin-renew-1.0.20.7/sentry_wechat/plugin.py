# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
sentry_wechat.models
~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by cxt, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import json
import requests
from datetime import datetime
from pytz import timezone

from sentry.plugins.bases.notify import NotificationPlugin
import sentry_wechat
from django import forms
from django.utils.translation import ugettext_lazy as _

class WechatForm(forms.Form):
   urls = forms.CharField(
        label=_('Wechat robot url'),
        widget=forms.Textarea(attrs={
            'class': 'span6', 'placeholder': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx-xxx-xxx-xxx-xxx'}),
        help_text=_('Enter wechat robot url.'))

class WechatPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to WeChat.
    """
    author = 'cxt'
    author_url = 'https://github.com/susujs/sentry-wechat-plugin'
    version = sentry_wechat.VERSION
    description = "Integrates wechat robot."
    resource_links = [
        ('Bug Tracker', 'https://github.com/susujs/sentry-wechat-plugin/issues'),
        ('Source', 'https://github.com/susujs/sentry-wechat-plugin'),
    ]

    slug = 'wechat'
    title = 'wechat'
    conf_title = title
    conf_key = 'wechat'
    project_conf_form = WechatForm

    def get_webhook_urls(self, project):
        url = self.get_option('urls', project)
        if not url:
            return ''
        return url
        
    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('urls', project))

    def notify_users(self, group, event, *args, **kwargs):
        if not self.is_configured(group.project):
            self.logger.info('wechat urls config error')
            return None

        if self.should_notify(group, event):
            self.logger.info('send msg to wechat robot yes')
            self.post_base_process(group, event, *args, **kwargs)
        else:
            self.logger.info('send msg to wechat robot no')
            return None

    def post_base_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """
        send_url = self.get_webhook_urls(group.project)
        title = "[{}]发生错误，请尽快查看处理!".format(event.project.slug)
        description = event.title or event.message
        url="{}events/{}/".format(group.get_absolute_url(),event.event_id)

        data = {
          "msgtype": "news",
                "news": {
                "articles" : [
                        {
                            "title" : title or "",
                            "url" : url or "",
                            "description" : description or "",
                            "picurl" : "https://i.loli.net/2020/04/28/xZqCELKHhBSeY9t.png"
                        }
                    ]
                }
        }

        main_data = {
                "msgtype": "markdown",
                "markdown": {
                    "content": u"#### {title} \n > 环境: <font color=\"info\">{environment}</font> \n > 等级: <font color=\"warning\">{level}</font> \n > 版本: <font color=\"comment\">{release}</font> \n > 浏览器: <font color=\"comment\">{browser}</font> \n > 操作系统: <font color=\"comment\">{os}</font> \n > 域名: <font color=\"comment\">{domain}</font> \n > 用户: <font color=\"comment\">{user}</font> \n > 报错信息: <font color=\"comment\">{message}</font> \n > 触发点: <font color=\"comment\">{culprit}</font> \n > 创建日期: <font color=\"comment\">{dateCreated}</font> \n > [怼我看BUG!]({url})".format(
                        title="详情",
                        environment=event.get_tag("environment") or "",
                        level=event.get_tag("level") or "",
                        release=event.get_tag("release") or "",
                        browser=event.get_tag("browser") or "",
                        os=event.get_tag("os") or "",
                        domain=event.get_tag("url") or "",
                        user=event.get_tag("user") or "",
                        message=description or "",
                        culprit=event.culprit or "",
                        dateCreated=datetime.now(timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S") or "",
                        url=url or "",
                    )
                }
        }

        req_list = [data,main_data]
        for val in req_list:
            requests.post(send_url,headers={"Content-Type": "application/json"},data=json.dumps(val)),