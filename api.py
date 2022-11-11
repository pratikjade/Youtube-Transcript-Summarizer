import flask  # flask app is a micro web framework 
from flask import request, jsonify  # jsonify serializes data to JavaScript Object Notation (JSON) format
from flask_cors import CORS  # resources on a web page
import re  # Re A regular expression or regex is a special text string used for describing a search pattern.
import nltk  # Natural Language Toolkit
import heapq  # Heap queue algorithm finding the shortest path
from youtube_transcript_api import YouTubeTranscriptApi  # Youtube Transcript API

# A route to return all of the available entries in our catalog.
app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


# Get Youtube Transcript
def get_ytdata(id):
    transcript_list = YouTubeTranscriptApi.get_transcript(id)                        # Get Transcript
    full_transcript = ""                                                             # Empty String to store transcript
    for transcript in transcript_list:                                               # Loop through transcript list and add to string
        timestamp = transcript['text'].split()                                       # Split text into words
        full_transcript += " "+" ".join(timestamp)                                   # Add words to string
    return full_transcript                                                           # Return transcript summary

# A route to return all of the available entries in our catalog.


def get_text_summary(id=None):                                                      # Get Text Summary
    if not id:                                                                      # If no id is provided
        return "No ID Was Provided"                                                 # Return error message
    # Download Punkt Sentence Tokenizer
    nltk.download('punkt')                                                     #punkt Sentence Tokenizer. This tokenizer divides a text into a list of sentences by using an unsupervised algorithm to build a model for abbreviation words, collocations, and words that start sentences. It must be trained on a large collection of plaintext in the target language before it can be used.
    nltk.download('stopwords')                                                      # Stop Words: A stop word is a commonly used word (such as “the”, “a”, “an”, “in”) that a search engine has been programmed to ignore, both when indexing entries for searching and when retrieving them as the result of a search query.
    full_transcript = get_ytdata(id)                                                # Get Youtube Transcript
    # file = open('transcript.txt','w')
    # file.write(full_transcript)
    # file.close()

    # cleaning data (removes brackets , special characters etc)
    # Remove numbers in brackets
    full_transcript = re.sub(r'\[[0-9]*\]', ' ', full_transcript)
    # Remove extra spaces
    full_transcript = re.sub(r'\s+', ' ', full_transcript)
    formatted_transcript_text = re.sub(
        '[^a-zA-Z]', ' ', full_transcript)                                               # Remove special characters
    formatted_transcript_text = re.sub(
        r'\s+', ' ', formatted_transcript_text)                                          # Remove extra spaces
    # print(formatted_transcript_text)

    # converting text to sentences
    sentence_list = nltk.sent_tokenize(
        full_transcript)                                                             # Tokenize sentences

    # find weighted frequency of occurence
    stopwords = nltk.corpus.stopwords.words(
        'english')                                                                   # Get stopwords from NLTK corpus
    # Empty dictionary to store word frequencies
    word_frequencies = {}
    # Loop through each word in the transcript
    for word in nltk.word_tokenize(formatted_transcript_text):
        if word not in stopwords:                                                      # If word is not a stopword
            if word not in word_frequencies.keys():                                  # If word is not already in dictionary
                # Add word to dictionary with a frequency of 1
                word_frequencies[word] = 1
            else:                                                                     # If word is already in dictionary
                word_frequencies[word] += 1                                            # Increment count of word by 1

    # Get maximum word frequency
    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():                                               # Loop through each word in dictionary
        # Divide each word frequency by the maximum frequency
        word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

    # calculate the sentence score
    sentence_scores = {}                                                                 # Empty dictionary to store sentence scores
    for sent in sentence_list:                                                           # Loop through each sentence in the transcript
        # Loop through each word in the sentence
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():                                         # If word is in the word frequency dictionary
                if len(sent.split(' ')) < 30:                                           # If sentence is less than 30 words
                    if sent not in sentence_scores.keys():                              # If sentence is not already in dictionary
                        # Add sentence to dictionary with a score equal to the word frequency
                        sentence_scores[sent] = word_frequencies[word]
                    else:                                                               # If sentence is already in dictionary
                                                                                        # Increment score of sentence by word frequency
                        sentence_scores[sent] += word_frequencies[word]

    # getting summary
    # Get top 7 sentences with highest scores
    summary_sentences = heapq.nlargest(
        7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)                                                # Join sentences into string
    # Return summary
    return summary


# Route to return all of the available entries in our catalog.
@app.route('/', methods=['GET'])
def home():                                                                                  # Home page
    id = None                                                                                # Empty id
    if 'id' in request.args:                                                                 # If id is provided
        id = request.args['id']                                                              # Set id to provided id
    else:                                                                                    # If no id is provided
        print("Error : No id was provided")                                                  # Print error message
    return jsonify({'text': get_text_summary(id)})                                             # Return summary


app.run()  
