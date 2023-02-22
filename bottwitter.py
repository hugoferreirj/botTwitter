import os
import tweepy
import time
import random
import json
from apiclient.discovery import build
from apiclient.errors import HttpError

# api twitter

auth = tweepy.OAuthHandler(os.environ.get('API_KEY'), os.environ.get('API_SECRET_KEY'))
auth.set_access_token(os.environ.get('ACESS_KEY'), os.environ.get('ACESS_SECRET'))

api = tweepy.API(auth, wait_on_rate_limit=True)

# api youtube
keyYT = os.environ.get('YOUTUBE_KEY')


# abre e lê arquivo json
arq = open('letrasDasMusicas.json',  encoding='utf-8')
data = json.load(arq)


def sorteiaMusica():
    musicaEscolhida = random.choice(data['Musicas'])
    return musicaEscolhida

# elimina estrofes repetidas e escolhe uma estrofe para se postada
def sorteiaEstrofe(musicaEscolhida):
    estrofesComRepeticao = musicaEscolhida["Letra"].split("\n\n")
    estrofesUnicas = list(set(estrofesComRepeticao))
    estrofeEscolhida = random.choice(estrofesUnicas)
    return estrofeEscolhida

# escolhe a qual amigo o tweet será direcionado
def escolheAmigo():
    amigos = ['bottopaloma', 'sohguimesmo', 'torvicbz', 'kaorii_mari', 'gigimoeller', 'ji_piton', 'kathleenjbo', 'lrpoec', 'lah_quaggio',
              'nelisa_pb', 'lulisa_a', 'willrodx', 'mazeto__ana', 'lari_biazon', 'isacrts', 'ju_francaa', 'dudaaaaaaaf', 'mafelomba', 'aaaaanlee', 'ribe3iro']
    return random.choice(amigos)

# pega o id do ultimo tweet feito pela conta para responder em thread

def pegaIdUltimoTweet():
    tweets_list = api.user_timeline(screen_name="botdohugo", count=1)
    tweet = tweets_list[0]
    return tweet.id

# posta um tweet com o link da musica no youtube em resposta
def postaLinkYoutube(musica):
    id = pegaIdUltimoTweet()
    buscaYoutube = musica["Nome"] + " " + musica["Cantor"]
    try:
        linkYoutube = pegaVideo(buscaYoutube)
        tweet = "Você pode escutar essa música aqui: " + linkYoutube
        api.update_status(status=tweet, in_reply_to_status_id=id)
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

def postaTweet():
    user = escolheAmigo()
    musica = sorteiaMusica()
    estrofe = sorteiaEstrofe(musica)
    tweet = "." + user + " " + estrofe
    tamanhoTweet = len(tweet)
    if (tamanhoTweet > 279):
        api.update_status(tweet[0:279])  # posta primeiro tweet, sem ser uma reply
        time.sleep(3)
        i = 279
        while i < tamanhoTweet:
            id = pegaIdUltimoTweet()
            api.update_status(status=tweet[i:i+279], in_reply_to_status_id=id)
            time.sleep(3)
            i += 279
    else:
        api.update_status(tweet)
    postaLinkYoutube(musica)
    


# procura musica no youtube e retorna o link
def pegaVideo(busca):
    youtube = build('youtube', 'v3',
    developerKey=keyYT)

    search_response = youtube.search().list(
    q=busca,
    part="id,snippet",
    maxResults=1,
    type="video",
    videoEmbeddable="true").execute()

    videos = search_response.get("items", [])
    link = "https://youtu.be/" + videos[0]["id"]["videoId"]
    return link


while True:
    postaTweet()
    time.sleep(6*82800)
