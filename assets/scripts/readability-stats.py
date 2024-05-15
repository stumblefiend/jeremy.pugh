import nltk
nltk.download('punkt')
nltk.download('cmudict')
from nltk.tokenize import sent_tokenize, word_tokenize #, syllable_count
from nltk.corpus import cmudict

def flesch_reading_ease(text):
    words = word_tokenize(text)
    sentences = sent_tokenize(text)
    num_words = len(words)
    num_sentences = len(sentences)
    #num_syllables = syllable_count(words)
    num_syllables = sum([len([y for y in x if y[-1].isdigit()]) for word in words for x in cmudict.dict().get(word, [])])
    #num_syllables = sum([len([y for y in x if y[-1].isdigit()]) for x in cmudict.dict().values() for x in words])
    reading_ease = 206.835 - 1.015 * (num_words / num_sentences) - 84.6 * (num_syllables / num_words)
    # Debugging: print out intermediate values
    print("Number of words:", num_words)
    print("Number of sentences:", num_sentences)
    print("Number of syllables:", num_syllables)
    return reading_ease

def average_sentence_length(text):
    sentences = sent_tokenize(text)
    total_words = sum(len(word_tokenize(sentence)) for sentence in sentences)
    avg_length = total_words / len(sentences)
    return avg_length

# Function to read text from a file
def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Example usage
file_path = 'your_file.txt'  # Update with your file path
text = read_text_from_file(file_path)
reading_ease = flesch_reading_ease(text)
avg_sentence_length = average_sentence_length(text)
print("Flesch Reading Ease:", reading_ease)
print("Average Sentence Length:", avg_sentence_length)
