# coding: utf-8

from mylib.qiita_article import QiitaParser
from mylib.slack_webhook_app import SlackWebhookApp

# DRIVER_PATH = "/usr/local/bin/chromedriver" # local
DRIVER_PATH = '/app/.chromedriver/bin/chromedriver' # heroku

SLACK_WEBHOOK_ENDPOINT = {
    "#qiita_daily_summary": "https://hooks.slack.com/services/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",
    "#notify-youtube": "https://hooks.slack.com/services/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"
}
SLACK_USER_NAME = "retro big bot"
SLACK_USER_ICON = ":robot_face:"

qiita_parser = QiitaParser(DRIVER_PATH)
articles = qiita_parser.get_qiita_daily()
full_message = "\n".join([art.to_message() for art in articles])

slack_app = SlackWebhookApp(SLACK_WEBHOOK_ENDPOINT.get("#qiita_daily_summary"), SLACK_USER_NAME, SLACK_USER_ICON)
res = slack_app.post_message(full_message)