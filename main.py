# main.py
import tweepy
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
from config import api_key, api_secret, access_token, access_token_secret

# Configurar API do Twitter
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Função para coletar tweets
def coletar_tweets(termo_busca, quantidade=100):
    tweets = tweepy.Cursor(api.search_tweets, q=termo_busca, lang="pt", tweet_mode="extended").items(quantidade)
    lista_tweets = [[tweet.full_text] for tweet in tweets]
    return pd.DataFrame(lista_tweets, columns=["Tweet"])

# Função para analisar sentimentos
def analisar_sentimento(texto):
    analise = TextBlob(texto)
    if analise.sentiment.polarity > 0:
        return "Positivo"
    elif analise.sentiment.polarity == 0:
        return "Neutro"
    else:
        return "Negativo"

# Main
def main():
    termo = input("Digite o termo para busca no Twitter: ")
    quantidade = int(input("Digite a quantidade de tweets a serem coletados: "))

    # Coletar tweets
    print("Coletando tweets...")
    dados = coletar_tweets(termo, quantidade)

    # Analisar sentimentos
    print("Analisando sentimentos...")
    dados["Sentimento"] = dados["Tweet"].apply(lambda x: analisar_sentimento(x))

    # Exibir distribuição
    sentimentos_contagem = dados["Sentimento"].value_counts()
    print(sentimentos_contagem)

    # Visualização
    plt.figure(figsize=(8, 5))
    sns.barplot(x=sentimentos_contagem.index, y=sentimentos_contagem.values, palette="coolwarm")
    plt.title("Distribuição de Sentimentos", fontsize=16)
    plt.xlabel("Sentimento", fontsize=12)
    plt.ylabel("Frequência", fontsize=12)
    plt.show()

if __name__ == "__main__":
    main()
