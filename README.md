# Youtube-transcript-summarizer
This code snippet is a Flask application designed to summarize transcripts of Youtube videos using their video IDs. It uses the youtube_transcript_api package to first get a transcript of a video, and then uses the Natural Language Toolkit (NLTK) library to process the text of the transcript. 
Sanitize text using regular expressions to remove numbers, special characters, and extra spaces in parentheses. 
The text is then tokenized into sentences with stop words removed.

The code then creates a dictionary to store word frequencies and loops through each word in the transcription. 
If a word is not a stop word and not in the dictionary, it is added with a frequency of 1. If the word is already in the dictionary, its frequency is increased.

The code also uses the heapq algorithm to find the most important points in the video transcript. The app has an endpoint /get_text_summary that takes a youtube video's id parameter and returns a summary of the transcript.

Additionally, it uses requests-jsonify and the CORS module to handle HTTP requests and enable cross-origin resource sharing. 
This code is part of a chrome extension that helps users quickly and easily summarize the transcript of any Youtube video. 
It's perfect for anyone looking to save time and Get the most out of their video viewing experience. It's also great for students who want to summarize educational videos for study or professionals who want to quickly review videos of meetings or presentations.
