from confai.stanalysis import sentiment
import os
def read_file():
    while True:
        # Prompt the user for a ticker name, year, and quarter
        ticker_name = input("Enter a ticker name: ")
        year = input("Enter a year: ")
        quarter = input("Enter a quarter: ")

        # Construct the filename
        filename = f"{ticker_name}{year}Q{quarter}.txt"

        # Check if the file exists in the 'calls' directory
        file_path = os.path.join('calls', filename)
        if os.path.isfile(file_path):
            # If the file exists, read and return its content
            with open(file_path, 'r') as file:
                text = file.read()
            return text
        else:
            # If the file does not exist, inform the user and reprompt
            print("File not found. Please try again.")
# Use the function
text = read_file()

# Use the SentimentAnalyzer class
def print_sentiment(text):
    analyzer = sentiment.SentimentAnalyzer(text)
    average_scores = analyzer.get_average_scores()
    highest_negative, highest_positive = analyzer.find_extreme_sentences()

    print(f"Average sentiment scores: {average_scores}")
    print("Sentences with highest negative probabilities:")
    for score, sentence in highest_negative:
        print(f"Score: {score}, Sentence: {sentence}")
    print("Sentences with highest positive probabilities:")
    for score, sentence in highest_positive:
        print(f"Score: {score}, Sentence: {sentence}")
    print(f"Overall sentiment of the document: {analyzer.get_overall_score()}")
