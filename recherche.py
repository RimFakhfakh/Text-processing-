from math import sqrt
from lxml import etree
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import nltk


dict_path = "Base/dictionnaire.xml"
docs_path = "Base/docs.xml"
inverse_file_path = "Base/inverse_final.xml"


def lire_requete():
    return input("---> ")


def traitement_requete(r):
    # Tokenization
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    keywords_with_stoplist = tokenizer.tokenize(r)
    tokens = [w.lower() for w in keywords_with_stoplist]
    # élimination des mots vides
    keywords = []
    try:
        nltk.data.find('stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
        stop_words = set(stopwords.words('english'))
        keywords = [w for w in tokens if not w in stop_words]
    # normalisation par Stemming
    porter = PorterStemmer()
    stemmed = [porter.stem(w) for w in keywords]
    return stemmed


def vecteur_dictionnaire(chemin_dict):
    vec_dict = {}
    dic = etree.parse(chemin_dict)
    root = dic.getroot()
    for child in root:
        vec_dict[child.get("name")] = 0
    return vec_dict


def vecteur_requete(vect_dic: dict, r: list):
    for key in vect_dic.keys():
        vect_dic[key] = 1 if key in r else 0
    return vect_dic


def sim(x, y):

    X_x_Y = sum([x[key]*y[key] for key in x.keys()])
    x_euclidean_norm = sqrt(sum(x[key]**2 for key in x.keys()))
    y_euclidean_norm = sqrt(sum(y[key]**2 for key in x.keys()))

    if ((x_euclidean_norm*y_euclidean_norm) > 0):
        sim = X_x_Y / (x_euclidean_norm*y_euclidean_norm)

        return round(sim, 2)

    return 0.0


def sim_req_docs(path_inverse_file, path_docs_file, vecteur_req):
    docs = etree.parse(path_docs_file)
    docs_root = docs.getroot()

    docs_names_list = [child.get("name") for child in docs_root]

    final_vect = {

        doc: {keyword: 0 for keyword in vecteur_req.keys()} for doc in docs_names_list

    }

    reversed = etree.parse(path_inverse_file)
    reversed_root = reversed.getroot()

    for child in reversed_root:
        keyword = child.get("name")
        for child2 in child:
            doc_name = child2.get("name")
            if doc_name in docs_names_list:
                w = float(child2.text)
                final_vect[doc_name][keyword] = w

    sim_dict = {
        doc: sim(final_vect[doc], vecteur_req) for doc in docs_names_list
    }

    return sim_dict


def trie_doc(sim_dict: dict):
    s = {k: v for k, v in sorted(
        sim_dict.items(), key=lambda item: item[1], reverse=True)}

    return s.keys()


def main():
    r = lire_requete()
    traited_r = traitement_requete(r)
    vect_dict = vecteur_dictionnaire(dict_path)
    vect_req = vecteur_requete(vect_dict, traited_r)
    sim_dict = sim_req_docs(inverse_file_path, docs_path, vect_req)
    s = trie_doc(sim_dict)
    print("\n".join(s))


if __name__ == '__main__':
    main()
