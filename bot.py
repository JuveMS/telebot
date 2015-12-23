import random
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
        'Agitadora'
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
}


def resposta(tipo):
    return {'msg': random.choice(MESSAGES.get(tipo))}
