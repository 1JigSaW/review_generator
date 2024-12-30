import random
import re


def add_human_like_noise(text):
    sentences = text.split('.')
    humanized_sentences = []

    for sentence in sentences:
        words = sentence.split()

        if random.random() < 0.1:
            sentence = sentence.replace(",", "").replace(".", "")

        if random.random() < 0.15:
            sentence = sentence.replace("the", "").replace("in", "on")

        if random.random() < 0.1:
            sentence = re.sub(r'(\w)(,|\.)', r'\1 \2', sentence)

        if random.random() < 0.2:
            if words:
                sentence = sentence + " " + words[0]

        if random.random() < 0.2:
            sentence = sentence + " Well... it's kind of like, you know?"

        if random.random() < 0.1:
            words = words[::-1]
            sentence = " ".join(words)

        sentence = ' '.join(words)
        humanized_sentences.append(sentence)

    humanized_text = '. '.join(humanized_sentences)
    if humanized_text and humanized_text[-1] not in ['.', '!', '?']:
        humanized_text += '.'

    return humanized_text
