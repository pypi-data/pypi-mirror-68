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
            self.post_process(group, event, *args, **kwargs)

        else:
            self.logger.info('send msg to wechat robot no')
            return None

    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """
        send_url = self.get_webhook_urls(group.project)
        title = "[{}]发生({})错误，请尽快查看处理!".format(event.project.slug,event.title)
        url="{}events/{}/".format(group.get_absolute_url(),event.event_id)

        data = {
          "msgtype": "news",
                "news": {
                "articles" : [
                        {
                            "title" : title,
                            "description" : event.message,
                            "url" : url,
                            "picurl" : "https://i.loli.net/2020/04/28/xZqCELKHhBSeY9t.png"
                        }
                    ]
                }
        }
        requests.post(
            url=send_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )
