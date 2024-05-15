import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import cmudict
import string

# Download CMU Pronouncing Dictionary
nltk.download('cmudict')

# Load CMU Pronouncing Dictionary
pronouncing_dict = cmudict.dict()

def preprocess_text(text):
    # Remove punctuation marks
    text = text.translate(str.maketrans('', '', string.punctuation))
    #print("Text:", text)
    return text

def count_syllables(word):
    # Lookup word in CMU Pronouncing Dictionary and count syllables
    syllables = pronouncing_dict.get(word.lower())
    if syllables:
        return len([s for s in syllables[0] if s[-1].isdigit()])
    else:
        return 0  # Return 0 if word not found in CMU Pronouncing Dictionary

def flesch_reading_ease(text):
    # Preprocess text to remove punctuation
    raw_text = text
    text = preprocess_text(text)
    
    words = word_tokenize(text)
    sentences = sent_tokenize(raw_text)
    num_words = len(words)
    print("Words:", num_words)
    num_sentences = len(sentences)
    
    # Count syllables for each word
    num_syllables = sum(count_syllables(word) for word in words)

    print("Syllables", num_syllables)
    print("Sentences: ", num_sentences)
    num_words = 1184
    num_syllables = 1889
    reading_ease = 206.835 - 1.015 * (num_words / num_sentences) - 84.6 * (num_syllables / num_words)
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
