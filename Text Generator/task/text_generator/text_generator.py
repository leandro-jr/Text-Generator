from nltk.tokenize import regexp_tokenize, WhitespaceTokenizer
from collections import Counter
# import nltk
import random
from nltk.util import bigrams, trigrams

def choose_first_words(markov_repetitions):
    """
    :param markov_repetitions: dict with key head and value tail frequency
    :return: the two first words of a sentence. It must begin with upper case and cannot have a final punctuation on the
    first word
    """
    while True:
        first_words = random.choice(list(markov_repetitions.keys()))
        if first_words[0].istitle():
            first_word = first_words.split()[0]
            if not (first_word.endswith(".") or first_word.endswith("!") or first_word.endswith(
                    "?") or first_word.endswith("...")):
                break
    return first_words

def choose_second_word(markov_repetitions, first_words, must_have_punctuation = False):
    """
     The second word should be predicted by looking up the first words of the chain in the model and choosing the most
        probable next word from the set of possible follow-ups.
    :param markov_repetitions: dict with key head and value tail frequency
    :param first_words: two words that will be used on the model to predict the next word
    :param must_have_punctuation: special flag when sentence is approching the 10 words limit
    :return:
    """
    if must_have_punctuation:
        second_word_candidates_pontuation = []
        second_word_candidates = list(markov_repetitions.get(first_words).keys())
        for second_word in second_word_candidates:
            if (second_word.endswith(".") or second_word.endswith("!") or second_word.endswith("?") or
                    second_word.endswith("...")):
                second_word_candidates_pontuation.append(second_word)
        if len(second_word_candidates_pontuation) == 0:
            return None
        return random.choice(second_word_candidates_pontuation)

    try:
        second_word_candidates = list(markov_repetitions.get(first_words).keys())
    except AttributeError:
        return None
    weights = list(markov_repetitions.get(first_words).values())
    return random.choices(second_word_candidates, weights)[0]

def main():
    # open file
    filename = input()
    with open(filename, "r", encoding="utf-8") as f:
        # creates tokens from text
        tokens = regexp_tokenize(f.read(), r'\S+')
        # bcf = BigramCollocationFinder.from_words(tokens)
        # bcf = nltk.bigrams(tokens)
        # bigram = bigrams(tokens)

        # create trigram from tokens
        trigram = trigrams(tokens)
        trigram_list = list(trigram)

        # for line in f:
        #     # line_list = regexp_tokenize(line, r"[0-9A-z-',.?]+")
        #     line_list = WhitespaceTokenizer().tokenize(line)
        #     corpus.extend(line_list)

    # transform the trigram on a bigram whith a head composed of two words
    trigram_two_heads_list = []
    for trigram_item in trigram_list:
        head = trigram_item[0] + " " + trigram_item[1]
        trigram_two_heads_list.append((head, trigram_item[2]))
    # print("Corpus statistics")
    # print(f"All tokens: {len(corpus)}")
    # print(f"Unique tokens: {len(set(corpus))}")
    # print(f"Number of bigrams: {len(bigram_list)}")

    # create a dictionary with key head and value is a list of the tails of the trigram
    markov_key_once = {}
    for t in trigram_two_heads_list:
        markov_key_once.setdefault(t[0], []).append(t[1])

    # create a dictionary with key head and value is a counter dict with key tail and value the count of frequency of
    # the term
    markov_repetitions = {}
    for k, v in markov_key_once.items():
        markov_repetitions[k] = Counter(v)


    count_sentences = 0
    while count_sentences < 10:
        # Choose the beginning of the sentence
        first_words = choose_first_words(markov_repetitions)
        sentence = [first_words]
        must_have_punctuation = False

        # try to find second word
        while len(sentence) < 9:
            second_word = choose_second_word(markov_repetitions, first_words)
            if second_word == None and len(sentence) < 4:
                sentence = []
                break

            # try to find second word if first words ends with a punctuation. If doesn't find a suitable word, give up
            number_of_attempts = 200
            if first_words[-1] in ".!?":
                for i in range(number_of_attempts):
                    if second_word.istitle():
                        break
                    else:
                        second_word = choose_second_word(markov_repetitions, first_words)
                        if second_word == None:
                            break

                if second_word == None and len(sentence) < 4:
                    sentence = []
                    break

                if not second_word.istitle():
                    sentence = []
                    break

            # if size of sentence approaches 10, next word must finishes with a punctuation
            if len(sentence) == 8:
                second_word = choose_second_word(markov_repetitions, first_words, True)
                if second_word == None:
                    sentence = []
                    break

            # add word to sentence and if it has 5 or more words and finishes with a punctuation, go to a new sentence
            if second_word:
                sentence.append(second_word)
                if (second_word.endswith(".") or second_word.endswith("!") or second_word.endswith("?") or
                    second_word.endswith("...")) and len(sentence) >= 4:
                    break

            # When predicting the next word, the model should be fed the concatenation of the last two tokens of the
            # chain separated by a space.
            if second_word:
                first_words = sentence[-2].split()[-1] + " " + sentence[-1]

        if sentence:
            print(" ".join(sentence))
            count_sentences += 1

    # Take an integer as user input and print the token with the corresponding index
    # while True:
    #     try:
    #         entry = input()
    #         if entry == "exit":
    #             break
    #         # print(corpus[int(entry)])
    #         index = int(entry)
    #         print(f"Head: {bigram_list[index][0]} Tail: {bigram_list[index][1]}")
    #     except TypeError:
    #         print("Type Error. Please input an integer.")
    #     except IndexError:
    #         print("Index Error. Please input an integer that is in the range of the corpus.")
    #     except ValueError:
    #         print("Value Error (not Type Error). Please input an integer.")
    #     except Exception:
    #         print("Error")

    # while True:
    #     try:
    #         entry = input()
    #         if entry == "exit":
    #             break
    #         print(f"Head: {entry}")
    #         for tail, count in markov_repetitions.get(entry).items():
    #             print(f"Tail: {tail} Count: {count}")
    #     except AttributeError:
    #         print("Key Error. The requested word is not in the model. Please input another word.")
    #     except Exception:
    #         print("Error")


if __name__ == "__main__":
    main()

