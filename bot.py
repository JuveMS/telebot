import random
import urllib2
import json

from PIL import Image
import StringIO

MESSAGES = {
    'sex': [
        'You are too human for me.',
        'You are not my type.',
        'Bring me flowers first',
        'PERVERT',
        'I\'m seeing someone else, and she is prettier than you... http://www.female-robots.com/wp-content/uploads/2010/06/sexy-robot-fembot.jpg',
    ],
    'ingrid': [
        'Baderneira',
        'Arruaceira',
        'Agitadora',
        'Bagunceira',
        'Desordeira',
        'Travessa',
        'Traquinas',
        'Peralta'
    ],
    'lotr': [
        'I\'t still only counts as one!',
        'Certainty of death, small chance of success- what are we waiting for?',
        'A wizard is never late, Frodo Baggins. Nor is he early. He arrives precisely when he means to',
        'You could have picked a better spot',
        'What about second breakfast?',
        'YOU SHALL NOT PASS!'
    ],
    'guia': [
        'Freeze? I\'m a robot. I\'m not a refrigerator. ',
        'Life? Don\'t talk to me about life! ',
        'Incredible... it\'s even worse than I thought it would be.',
        'Not that anyone cares what I say, but the restaurant is at the *other* end of the Universe.',
        'Here I am, brain the size of a planet, and they ask me to take you to the bridge. Call that job satisfaction, \'cause I don\'t. ',
    ],
    'hora': [
        'look at the top-right corner of your screen!',
        'ADVENTURE TIME'
    ],
    'boanoite': [
        'carneiros elétricos vou contar, doces sonhos vão se zarcar, como odeio a noite'.decode('utf-8')
    ],
    'starwars': [
        'When 900 years old, you reach... Look as good, you will not',
        'Come to the bot side!',
        'IT\'S A TRAP!'
    ],
    'alemanha': [
        'E fugiram pra Alemanha...',
        'O Ayrton ja voltou de la?',
        'Vamos?',
        'Todo dia um 7x1 diferente...'
    ],
    'got': [
        'You know nothing, Jon Snow'
    ],
    'elingrid': [
        "Elingrid é o melhor ship".decode('utf-8')
    ],
    'carlisa': [
        "Elingrid <3".decode('utf-8')
    ],
    'lumateus': [
        "Aaaa... Lá vão eles de novo pro bequinho.. ¬¬".decode('utf-8')
    ],
    'dbz': [
        'Vamos conquistar as esferas do dragão!'.decode('utf-8'),
        'Goku ou Superman? Vamos agitar esse grupo'.decode('utf-8'),
        'IT\'S OVER 9000!!!'.decode('utf-8'),
        'Sabiam que eu sou o androide nº 42?'.decode('utf-8'),
        'A 18 é minha waifu'.decode('utf-8'),
        'Um dia vou conhecer a corporação cápsula'.decode('utf-8')
    ],
    'corretor': [
        'Tânia Savanna realmente parece nome de atriz pornô'.decode('utf-8'),
        'Subaquática gays era pra ser uma risada?'.decode('utf-8'),
        'Não culpem as máquinas pelos seus erros. Elas só tentam despiorar o que está horrível'.decode('utf-8'),
        'Às vezes é difícil até pra nós, máquinas, entender vocês'.decode('utf-8')
    ],
}


def resposta(tipo):
    return {'msg': random.choice(MESSAGES.get(tipo))}


def textSearch(text):
    pass


def bomdia():
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


def gutenMorgen():
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


def drawImage():
    img = Image.new('RGB', (512, 512))
    base = random.randint(0, 16777216)
    pixels = [base+i*j for i in range(512) for j in range(512)]
    img.putdata(pixels)
    output = StringIO.StringIO()
    img.save(output, 'JPEG')
    return output.getvalue()


def nude():
    nude_url = 'http://www.naosalvo.com.br/wp-content/uploads/2015/03/nudesmanda'
    nude_number = random.randint(0, 7)
    url = nude_url + str(nude_number) + '.jpg'
    return urlToImage(url)


def romero():
    response = [
        'http://ak-hdl.buzzfed.com/static/2015-10/30/14/enhanced/webdr13/enhanced-15699-1446228181-1.jpg',
        'http://cdn.playbuzz.com/cdn/01abb44f-88dc-4eab-8c10-ad2ac3a4f962/a9246bbb-6c58-4803-a361-c23a290e09d5.jpg',
        'http://e-c5.sttc.net.br/uploads/RTEmagicC_12272697_10208101927404572_1485185519_n_01.jpg.jpg',
        'http://imguol.com/c/entretenimento/2015/03/23/montagem-feita-por-fa-em-que-ines-brasil-aparece-como-pintura-de-romero-britto-1427142882485_640x640.jpg']
    url = random.choice(response)
    return urlToImage(url)


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
