try:
    import google
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    import urllib.request
    import urllib.parse
    import urllib.error
    import re
except ImportError:
    raise ImportError("You don't have packages whose are required to run this program. Install it with pip. "
                      "Required: google, vaderSentiment, urllib, re")


# positivity to czy wprowadzone sentence jest pozytywne czy negatywne 1 / -1
def source_sentence_verify(sentence, positivity):
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(sentence)

    compound = vs.__getitem__('compound')
    if compound > 0:
        return 1 * positivity
    if compound < 0:
        return -1 * positivity
    return 0


def in_string(sentence, string):

    words = sentence.split()
    word_counter = len(words)

    for word in words:
        if string.find(word) != -1:
            word_counter -= 1

    if word_counter == 0:
        return 1
    else:
        return 0


def verify_source(sentence, page_sentences, positivity):
    result = 0
    for single_sen in page_sentences:
        if in_string(sentence, single_sen) == 1:
            result += source_sentence_verify(single_sen, positivity)
    return result


def verify_input(sentence, precision, positivity):

    url_generator = google.search(sentence, tld='com', lang='en', num=precision, start=0, stop=1, pause=0.5)
    correctness_index = 0

    for url in url_generator:
        page = parse_page(url)
        if page != -1:
            correctness_index = correctness_index + verify_source(sentence, page, positivity)

    if correctness_index > 0:
        if positivity == 1:
            print("Sentence: \"{}\" is true".format(sentence))
        else:
            print("Sentence: \"NOT {}\" is true".format(sentence))
        return 1
    elif correctness_index < 0:
        if positivity == 1:
            print("Sentence: \"{}\" is false".format(sentence))
        else:
            print("Sentence: \"NOT {}\" is false".format(sentence))
        return -1
    else:
        print("Nothing confirming the truth of the sentence \"{}\" was found.".format(sentence))
        return 0


def parse_page(url):

    try:
        values = {'s': 'basics',
                  'submit': 'search'}
        data = urllib.parse.urlencode(values)
        data = data.encode('utf-8')
        req = urllib.request.Request(url, data)
        resp = urllib.request.urlopen(req)
        resp_data = resp.read()

        paragraphs = re.findall(r'<p>(.*?)</p>', str(resp_data))

        page_sentences = []
        for each_sen in paragraphs:
            each_sen = re.sub('<[^<]+?>', '', each_sen)
            page_sentences.append(each_sen)

        return page_sentences

    except urllib.error.HTTPError:
        return -1
