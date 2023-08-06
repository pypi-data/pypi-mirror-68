from django.db import models

from cabot.cabotapp.alert import AlertPlugin
from cabot.cabotapp.alert import AlertPluginUserData
from django.template import Context, Template

import requests
import json

alert_template = """{{ service.name }} {% if service.overall_status != service.PASSING_STATUS %} alerting with status: {{ service.overall_status }}{% else %} is back to normal{% endif %}.
{% if service.overall_status != service.PASSING_STATUS %}
Alerting:{% for check in service.all_failing_checks %}
  {{ check.check_category }} - {{ check.name }} {% endfor %}
{% endif %}
"""

class DingdingAlert(AlertPlugin):
    name = "Dingding"
    slug = "cabot_alert_dingding"
    author = "hanliangfeng"

    def send_alert(self, service, users, duty_officers):
        c = Context({
            'service': service,
        })
        t = Template(alert_template)
        message = t.render(c)
        payload = {
            "msgtype": "text", 
            "text": {
                "content": message
            }, 
            "at": {
                "atMobiles": [
                  service.name
                ], 
                "isAtAll": True
            }
        }
        dingding_urls = [u.dingding_url for u in DingdingAlertUserData.objects.filter(user__user__in=users)]
        headers = {'Content-Type': 'application/json'}
        for url in dingding_urls:
            if url:
                try:
                    requests.post(url,data=json.dumps(payload),headers=headers)
                except Exception as r:
                    print "send dingding failed as "+'%s' % r
        return True


class DingdingAlertUserData(AlertPluginUserData):
    name = "Dingding Plugin"
    dingding_url = models.URLField(max_length=200, blank=True)