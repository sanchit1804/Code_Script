import nltk
nltk.download('punkt_tab')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string


def summarize_text_nltk(text, num_sentences=3):
    """
    Summarizes the input text using a frequency-based method with NLTK.

    Args:
        text (str): The text to be summarized.
        num_sentences (int): The desired number of sentences in the summary.

    Returns:
        str: The summarized text.
    """
    if not text:
        return ""
    text = " ".join(text.split()) 
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text
    stop_words = set(stopwords.words('english'))
    punctuations = string.punctuation
    words = word_tokenize(text.lower())
    clean_words = [word for word in words if word.isalnum() and word not in stop_words]
    word_freq = {}
    for word in clean_words:
        word_freq[word] = word_freq.get(word, 0) + 1
    max_freq = max(word_freq.values())
    for word in word_freq:
        word_freq[word] = word_freq[word] / max_freq
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_freq[word]
                else:
                    sentence_scores[sentence] += word_freq[word]
    sorted_sentences = sorted(sentence_scores.items(), key=lambda item: item[1], reverse=True)
    summary_sentences = [sentence for sentence, score in sorted_sentences[:num_sentences]]
    final_summary = []
    selected_sentences_set = set(summary_sentences)
    
    for sentence in sentences:
        if sentence.strip() in selected_sentences_set:
             final_summary.append(sentence)

    return " ".join(final_summary)

input_text = """
Hacktoberfest is a month-long celebration of open source software, where developers from around 
the world contribute to various projects. It encourages participation in the open source community 
and helps improve software quality through collaborative efforts. Participants can earn rewards by 
making contributions, such as pull requests, to eligible repositories on GitHub.
"""

summary = summarize_text_nltk(input_text, num_sentences=1)

print(input_text)

print(summary)