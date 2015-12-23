# -*- coding: utf-8 -*-
import StringIO
import json
import logging
import random
import urllib
import urllib2

from bot import resposta

# for sending images
from PIL import Image
import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

TOKEN = '168191309:AAEdER88qh8Q34Hdt-yUZSBNhiU_mMfMUOw'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

def requestJson(url):
    req = urllib2.urlopen(
        urllib2.Request(
            url, headers={
                'Content-Type': 'application/json'}))
    response = json.loads(req.read())
    req.close()
    return response


def urlToImage(url):
    req = urllib2.urlopen(
        urllib2.Request(
            url, headers={
                'Content-Type': 'application/json'}))
    response = req.read()
    req.close()
    return response

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

    def bomdia(self):
        url = 'http://developers.agenciaideias.com.br/tempo/json/riodejaneiro-rj'
        response = requestJson(url)

        temperatura = response.get('agora').get('temperatura')
        temperatura_maxima = response.get('previsoes')[0].get('temperatura_max')
        temperatura_minima = response.get('previsoes')[0].get('temperatura_min')
        previsao = response.get('previsoes')[0].get('descricao')

        msg = "Bom dia Bully! A máxima hoje será de {} graus e a mínima de {} graus com {} \n".format(
            temperatura_maxima, temperatura_minima, previsao)
        if int(temperatura) >= 28:
            msg += 'Hoje está quente pra caramba! {} graus. Sorte que sou um robo.'.format(
                temperatura)
        else:
            msg += 'Hoje está agradável: {} graus'.format(temperatura)
        return msg.decode('utf-8')

    def gutenMorgen(self):
        url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22geesthacht%2C%20deu%22)%20and%20u%3D'c'&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
        response = requestJson(url)

        temperatura = response.get('query').get('results').get(
            'channel').get('item').get('condition').get('temp')
        temperatura_maxima = response.get('query').get('results').get(
            'channel').get('item').get('forecast')[0].get('high')
        temperatura_minima = response.get('query').get('results').get(
            'channel').get('item').get('forecast')[0].get('low')

        msg = "Guten Morgen Bully! Es ist {} Grad. Die maximale Temperatur ist {} Grad und die minimale Temperatur ist {} \n".format(
            temperatura, temperatura_maxima, temperatura_minima)
        return msg.decode('utf-8')

    def drawImage(self):
        img = Image.new('RGB', (512, 512))
        base = random.randint(0, 16777216)
        pixels = [base+i*j for i in range(512) for j in range(512)]
        img.putdata(pixels)
        output = StringIO.StringIO()
        img.save(output, 'JPEG')
        return output.getvalue()

    def nude(self):
        nude_url = 'http://www.naosalvo.com.br/wp-content/uploads/2015/03/nudesmanda'
        nude_number = random.randint(0, 7)
        url = nude_url + str(nude_number) + '.jpg'
        return urlToImage(url)

    def romero(self):
        response = [
            'http://ak-hdl.buzzfed.com/static/2015-10/30/14/enhanced/webdr13/enhanced-15699-1446228181-1.jpg',
            'http://cdn.playbuzz.com/cdn/01abb44f-88dc-4eab-8c10-ad2ac3a4f962/a9246bbb-6c58-4803-a361-c23a290e09d5.jpg',
            'http://e-c5.sttc.net.br/uploads/RTEmagicC_12272697_10208101927404572_1485185519_n_01.jpg.jpg',
            'http://imguol.com/c/entretenimento/2015/03/23/montagem-feita-por-fa-em-que-ines-brasil-aparece-como-pintura-de-romero-britto-1427142882485_640x640.jpg']
        url = random.choice(response)
        return urlToImage(url)

    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        message = body['message']
        message_id = message.get('message_id')
        text = message.get('text')
        chat = message['chat']
        chat_id = chat['id']

        if not text:
            logging.info('no text')
            return

        def reply(msg=None, img=None):
            if msg:
                resp = urllib2.urlopen(
                    BASE_URL + 'sendMessage',
                    urllib.urlencode(
                        {
                            'chat_id': str(chat_id),
                            'text': msg.encode('utf-8'),
                            'disable_web_page_preview': 'true',
                            'reply_to_message_id': str(message_id),
                        }
                    )
                ).read()
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

        # CUSTOMIZE FROM HERE
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
            elif text == '/ingrid':
                reply(random.choice(MESSAGES.get('ingrid')))
            elif text == '/image':
                reply(img=self.drawImage())
        else:
            text_search = {
                'romero britto': {'img': self.romero()},
                'Romero Britto': {'img': self.romero()},
                'nude': {'img': self.nude()},
                'sex': resposta('sex'),
                'elingrid': resposta('elingrid'),
                'Elingrid': resposta('elingrid'),
                'carlisa': resposta('carlisa'),
                'Carlisa': resposta('carlisa'),
                'lumateus': resposta('lumateus'),
                'Lumateus': resposta('lumateus'),
                'lotr': resposta('lotr'),
                'LotR': resposta('lotr'),
                'Gandalf': resposta('lotr'),
                'Gimili': resposta('lotr'),
                'alemanha': resposta('alemanha'),
                'Alemanha': resposta('alemanha'),
                'starwars': resposta('starwars'),
                'SW': resposta('starwars'),
                'Star Wars': resposta('starwars'),
                'boa noite': resposta('boanoite'),
                'who are you': 'https://www.youtube.com/watch?v=Qh8SsaCWY-s',
                'guia': resposta('guia'),
                'Guia': resposta('guia'),
                'what time': resposta('hora'),
                'GoT': resposta('got'),
                'Game of Thrones': resposta('got'),
                'game of thrones': resposta('got'),
            }

            for key, value in text_search.iteritems():
                if key in text:
                    reply(msg=value.get('msg'), img=value.get('img'))

app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
