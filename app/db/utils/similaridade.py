import jellyfish as jf
import re

stop_words = set(
    """
    de a o que e do da em um para é com não uma os no se na por mais as dos como mas foi ao ele das tem à
    seu sua ou ser quando muito há nos já está eu também só pelo pela até isso ela entre era depois sem mesmo
    aos ter seus quem nas me esse eles estão você tinha foram essa num nem suas meu às minha têm numa pelos
    elas havia seja qual será nós tenho lhe deles essas esses pelas este fosse dele tu te vocês vos lhes meus minhas
    teu tua teus tuas nosso nossa nossos nossas dela delas esta estes estas aquele aquela aqueles aquelas isto aquilo
    estou está estamos estão estive esteve estivemos estiverames tava estávamos estavames tivera estivéramos esteja
    """.split()
)


def pre_processing(text):

    # conversão para letras minúsculas
    letras_min = re.findall(r'\b[A-zÀ-úü]+\b', text.lower())

    # remoção de stopwords
    # stopwords = nltk.corpus.stopwords.words('portuguese')
    stop = set(stop_words)
    no_stopwords = [w for w in letras_min if w not in stop]

    # tokennização
    text_clean = " ".join(no_stopwords)
    return text_clean


def calcula_similaridade_vaga_pessoa(caracteristicas_vaga, caracteristicas_pessoa):

  caracteristicas_vaga_concatenada = " ".join(caracteristicas_vaga)
  caracteristicas_pessoa_concatenada = " ".join(caracteristicas_pessoa)


  texto_vaga = pre_processing(caracteristicas_vaga_concatenada)
 
  texto_pessoa = pre_processing(caracteristicas_pessoa_concatenada)
  
  similaridade = jf.levenshtein_distance(texto_vaga, texto_pessoa)

  return similaridade