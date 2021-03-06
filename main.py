import StringIO
import json
import logging
import random
import urllib
import urllib2

# for sending images
from PIL import Image
import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

TOKEN = '168191309:AAEdER88qh8Q34Hdt-yUZSBNhiU_mMfMUOw'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'


# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False


# ================================

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        message = body['message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']

        if not text:
            logging.info('no text')
            return

        def reply(msg=None, img=None):
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode('utf-8'),
                    'disable_web_page_preview': 'true',
                    'reply_to_message_id': str(message_id),
                })).read()
            elif img:
                resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
                    ('chat_id', str(chat_id)),
                    ('reply_to_message_id', str(message_id)),
                ], [
                    ('photo', 'image.jpg', img),
                ])
            else:
                logging.error('no msg or img specified')
                resp = None

            logging.info('send response:')
            logging.info(resp)

        if text.startswith('/'):
            if text == '/start':
                reply('Bot enabled')
                setEnabled(chat_id, True)
            elif text == '/stop':
                reply('Bot disabled')
                setEnabled(chat_id, False)
            elif text == '/dolar':
                reply('TODO not done yet')
                # converter dolar para real
                # http://cashcash.cc/v1/currency.json?from=usd&to=brl
            elif text == '/euro':
                reply('TODO not done yet')
                # converter dolar para euro
            elif text == '/bomdia':
                reply('TODO not done yet')
                # bom dia + previsao do tempo de forma engracada
            elif text == '/lmgtfy':
                reply('TODO not done yet')
                # let me google that for you
            elif text == '/sex':
                response = [
                    'You are too human for me.',
                    'You are not my type.',
                    'Bring me flowers first',
                    'PERVERT',
                    'I\'m seeing someone else, and she is prettier than you... http://www.female-robots.com/wp-content/uploads/2010/06/sexy-robot-fembot.jpg',
                ]
                reply(random.choice(response))
            elif text == '/image':
                img = Image.new('RGB', (512, 512))
                base = random.randint(0, 16777216)
                pixels = [base+i*j for i in range(512) for j in range(512)]  # generate sample image
                img.putdata(pixels)
                output = StringIO.StringIO()
                img.save(output, 'JPEG')
                reply(img=output.getvalue())
            else:
                reply('What command?')

        # CUSTOMIZE FROM HERE
        elif 'image me' in text:
            reply('TODO')
            # google search images
        elif 'boa noite' in text:
            # todo acentuacao
            response = ['carneiros eletricos vou contar, doces sonhos vao se zarcar, como odeio a noite']
            reply(random.choice(response))
        elif 'who are you' in text:
            reply('https://www.youtube.com/watch?v=Qh8SsaCWY-s')
        elif 'fala ai' in text or 'coe' in text or 'oii' in text:
            response = [
                'Freeze? I\'m a robot. I\'m not a refrigerator. ',
                'Life? Don\'t talk to me about life! ',
                'Incredible... it\'s even worse than I thought it would be.',
                'Not that anyone cares what I say, but the restaurant is at the *other* end of the Universe.',
                'Here I am, brain the size of a planet, and they ask me to take you to the bridge. Call that job satisfaction, \'cause I don\'t. ',
            ]
            reply(random.choice(response))
        elif 'what time' in text:
            response = [
                'look at the top-right corner of your screen!',
                'ADVENTURE TIME'
            ]
            reply(random.choice(response))
        else:
            if getEnabled(chat_id):
                try:
                    resp1 = json.load(urllib2.urlopen('http://www.simsimi.com/requestChat?lc=en&ft=1.0&req=' + urllib.quote_plus(text.encode('utf-8'))))
                    back = resp1.get('res').get('msg')
                except urllib2.HTTPError, err:
                    logging.error(err)
                    # back = str(err)
                    back = 'I dont know what you mean'
                if not back:
                    reply('okay...')
                elif 'I HAVE NO RESPONSE' in back:
                    reply('you said something with no meaning')
                else:
                    reply(back)
            else:
                logging.info('not enabled for chat_id {}'.format(chat_id))


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
