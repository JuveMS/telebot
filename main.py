# -*- coding: utf-8 -*-
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
        self.response.write(
            json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe')))
        )


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(
            json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates')))
        )


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(
                json.load(
                    urllib2.urlopen(
                        BASE_URL + 'setWebhook', urllib.urlencode({'url': url}))
                )
            )
            )


class WebhookHandler(webapp2.RequestHandler):
    '''
    def real2dolar(self, text):
        url = 'http://cashcash.cc/v1/currency.json?from=usd&to=brl'
        req = urllib2.urlopen(urllib2.Request(url, headers={'Content-Type': 'application/json'}))
        response = json.loads(req.read())
        req.close()

        rate = response.get('rate')
        real = float(text.replace('/real2dolar', '').replace(',', '.').strip())
        return real / rate

    def dolar2real(self, text):
        url = 'http://cashcash.cc/v1/currency.json?from=usd&to=brl'
        req = urllib2.urlopen(urllib2.Request(url, headers={'Content-Type': 'application/json'}))
        response = json.loads(req.read())
        req.close()

        rate = response.get('rate')
        real = float(text.replace('/dolar2real', '').replace(',', '.').strip())
        return real * rate
    '''
    def euro(self):
        # converter euro para real
        # http://cashcash.cc/v1/currency.json?from=usd&to=brl
        pass

    def requestJson(self, url):
        req = urllib2.urlopen(urllib2.Request(url, headers={'Content-Type': 'application/json'}))
        response = json.loads(req.read())
        req.close()
        return response

    def bomdia(self):
        url = 'http://developers.agenciaideias.com.br/tempo/json/riodejaneiro-rj'
        response = self.requestJson(url)

        temperatura = response.get('agora').get('temperatura')
        temperatura_maxima = response.get('previsoes')[0].get('temperatura_max')
        temperatura_minima = response.get('previsoes')[0].get('temperatura_min')
        previsao = response.get('previsoes')[0].get('descricao')

        msg = "Bom dia Bully! A máxima hoje será de {} graus e a mínima de {} graus com {} \n".format(temperatura_maxima, temperatura_minima, previsao)
        if int(temperatura) >= 28:
            msg += 'Hoje está quente pra caramba! {} graus. Sorte que sou um robo.'.format(temperatura)
        else:
            msg += 'Hoje está agradável: {} graus'.format(temperatura)
        return msg.decode('utf-8')

    def gutenMorgen(self):
        url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22geesthacht%2C%20deu%22)%20and%20u%3D'c'&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
        response = self.requestJson(url)

        temperatura = response.get('query').get('results').get('channel').get('item').get('condition').get('temp')
        temperatura_maxima = response.get('query').get('results').get('channel').get('item').get('forecast')[0].get('high')
        temperatura_minima = response.get('query').get('results').get('channel').get('item').get('forecast')[0].get('low')

        msg = "Guten Morgen Bully! Es ist {} Grad. Die maximale Temperatur ist {} Grad und die minimale Temperatur ist {} \n".format(temperatura, temperatura_maxima, temperatura_minima)
        return msg.decode('utf-8')

    def lmgtfy(self):
        pass

    def sex(self):
        response = [
            'You are too human for me.',
            'You are not my type.',
            'Bring me flowers first',
            'PERVERT',
            'I\'m seeing someone else, and she is prettier than you... http://www.female-robots.com/wp-content/uploads/2010/06/sexy-robot-fembot.jpg',
        ]
        return random.choice(response)
    def ingrid(self):
        response = [
            'Baderneira',
            'Arruaceira',
            'Agitadora'
        ]
        return random.choice(response)

    def lotr(self):
        response = [
            'I\'t still only counts as one!',
            'Certainty of death, small chance of success- what are we waiting for?',
            'A wizard is never late, Frodo Baggins. Nor is he early. He arrives precisely when he means to',
            'You could have picked a better spot',
            'What about second breakfast?',
            'YOU SHALL NOT PASS!'
        ]
        return random.choice(response)

    def alemanha(self):
        response = [
            'E fugiram pra Alemanha...',
            'O Ayrton ja voltou de la?',
            'Vamos?',
            'Todo dia um 7x1 diferente...'
        ]
        return random.choice(response)

    def starwars(self):
        response = [
            'When 900 years old, you reach... Look as good, you will not',
            'Come to the bot side!',
            'IT\'S A TRAP!'
        ]
        return random.choice(response)

    def image(self):
        img = Image.new('RGB', (512, 512))
        base = random.randint(0, 16777216)
        pixels = [base+i*j for i in range(512) for j in range(512)]
        img.putdata(pixels)
        output = StringIO.StringIO()
        img.save(output, 'JPEG')
        return output.getvalue()

    def elingrid(self):
        return "Elingrid é o melhor ship".decode('utf-8')

    def carlisa(self):
        return "Elingrid <3".decode('utf-8')

    def lumateus(self):
        return "Aaaa... Lá vão eles de novo pro bequinho.. ¬¬".decode('utf-8')

    def nude(self):
        nude_url = 'http://www.naosalvo.com.br/wp-content/uploads/2015/03/nudesmanda'
        nude_number = random.randint(0,7)
        url = nude_url + str(nude_number) + '.jpg'
        req = urllib2.urlopen(urllib2.Request(url, headers={'Content-Type': 'application/json'}))
        response = req.read()
        req.close()
        return response

    def romero(self):
        response = [
            'http://ak-hdl.buzzfed.com/static/2015-10/30/14/enhanced/webdr13/enhanced-15699-1446228181-1.jpg',
            'http://cdn.playbuzz.com/cdn/01abb44f-88dc-4eab-8c10-ad2ac3a4f962/a9246bbb-6c58-4803-a361-c23a290e09d5.jpg',
            'http://e-c5.sttc.net.br/uploads/RTEmagicC_12272697_10208101927404572_1485185519_n_01.jpg.jpg',
            'http://imguol.com/c/entretenimento/2015/03/23/montagem-feita-por-fa-em-que-ines-brasil-aparece-como-pintura-de-romero-britto-1427142882485_640x640.jpg'
        ]
        url = random.choice(response)

        req = urllib2.urlopen(urllib2.Request(url, headers={'Content-Type': 'application/json'}))
        response = req.read()
        req.close()
        return response

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
            elif text == '/bomdia':
                reply(self.bomdia())
            elif text == '/gutenmorgen':
                reply(self.gutenMorgen())
            elif text == '/lmgtfy':
                reply(self.lmgtfy())
            elif text == '/sex':
                reply(self.sex())
            elif text == '/ingrid':
                reply(self.ingrid())
            elif text == '/image':
                reply(img=self.image())
            elif text == '/romerobritto':
                reply(img=self.romero())

        # CUSTOMIZE FROM HERE
        elif 'nude' in text:
            reply(img=self.nude())
        elif 'elingrid' in text or 'Elingrid' in text:
            reply(self.elingrid())
        elif 'carlisa' in text or 'Carlisa' in text:
            reply(self.carlisa())
        elif 'lumateus' in text or 'Lumateus' in text:
            reply(self.lumateus())
        elif 'lotr' in text or 'LotR' in text or 'Gandalf' in text:
            reply(self.lotr())
        elif 'alemanha' in text or 'Alemanha' in text:
            reply(self.alemanha())
        elif 'star wars' in text or 'Star Wars' in text or 'SW' in text:
            reply(self.starwars())
        elif 'image me' in text:
            reply('TODO')
            # google search images
            # https://developers.google.com/custom-search/json-api/v1/overview
        elif 'boa noite' in text:
            response = 'carneiros elétricos vou contar, doces sonhos vão se zarcar, como odeio a noite'.decode('utf-8')
            reply(response)
        elif 'who are you' in text:
            reply('https://www.youtube.com/watch?v=Qh8SsaCWY-s')
        elif 'fala ai' in text or 'coe' in text or 'oii' in text or 'guia' in text or 'Guia' in text:
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
        elif 'GoT' in text or 'Game of Thrones' in text or 'game of thrones' in text:
            response = 'You know nothing, Jon Snow'
            reply(response)


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
