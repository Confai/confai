import re
import heapq
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from gensim.summarization import summarize

class SentimentAnalyzer:
    def __init__(self, text):
        print("Initializing SentimentAnalyzer...")
        print("splitting text into sentences...")
        cleaned_text = re.sub(r'(Operator|\\nOperator)[^\\n]*', '', text)
        self.sentences = re.split(r'(?<=[.!?])\s+', cleaned_text)
        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")

        if torch.cuda.is_available():
            print("using GPU!")
            self.device = torch.device('cuda')
        else:
            self.device = torch.device('cpu')

        self.model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(self.device)
        self.labels = {0: 'positive', 1: 'negative', 2: 'neutral', }
        self.softmax = torch.nn.Softmax(dim=0)  # Softmax function for converting logits to probabilities
        self.results = self.run_model()

    def run_model(self):
        print("Running the model...")
        results = []
        print("Loaded! Processing sentences...")
        with torch.no_grad():  # Disable gradient computation
            for idx, sentence in enumerate(self.sentences):
                inputs = self.tokenizer(sentence, return_tensors="pt", padding=True, truncation=True).to(self.device)
                outputs = self.model(**inputs)
                logits = outputs.logits[0].detach().cpu()  # Move tensor to CPU memory
                probabilities = self.softmax(logits).numpy()  # Convert logits to probabilities
                results.append((probabilities, sentence))
                torch.cuda.empty_cache()  # Free up GPU memory
        return results

    def get_average_scores(self):
        total_scores = np.zeros(3)
        for probabilities, _ in self.results:
            total_scores += probabilities
        # Calculate the average sentiment scores for the document
        avg_scores = total_scores / len(self.sentences)
        return [str(score) for score in avg_scores.tolist()]  # Convert float32 to string

    def find_extreme_sentences(self):
        highest_negative = []  # heap to keep track of the top 3 negative sentences
        highest_positive = []  # heap to keep track of the top 3 positive sentences

        for probabilities, sent in self.results:
            sentiment_label = self.labels[np.argmax(probabilities)]

            # Check if this sentence is among the top 3 negative or positive sentences
            if sentiment_label == 'negative':
                heapq.heappush(highest_negative, (str(probabilities[1]), sent))  # Convert float32 to string
                if len(highest_negative) > 3:
                    heapq.heappop(highest_negative)  # remove the sentence with the lowest negative score
            elif sentiment_label == 'positive':
                heapq.heappush(highest_positive, (str(probabilities[0]), sent))  # Convert float32 to string
                if len(highest_positive) > 3:
                    heapq.heappop(highest_positive)  # remove the sentence with the lowest positive score

        return highest_negative, highest_positive

    def get_overall_score(self):
        avg_scores = self.get_average_scores()
        overall_sentiment_score = np.argmax([float(score) for score in avg_scores])  # Convert string back to float for argmax
        overall_sentiment_label = self.labels[overall_sentiment_score]

        if overall_sentiment_label == 'positive':
            if float(avg_scores[0]) > 0.6:  # Convert string back to float for comparison
                return 'overwhelmingly positive'
            elif float(avg_scores[0]) > 0.4:  # Convert string back to float for comparison
                return 'positive'
            else:
                return 'somewhat positive'
        elif overall_sentiment_label == 'negative':
            if float(avg_scores[1]) > 0.6:  # Convert string back to float for comparison
                return 'overwhelmingly negative'
            elif float(avg_scores[1]) > 0.4:  # Convert string back to float for comparison
                return 'negative'
            else:
                return 'somewhat negative'
        else:
            return 'neutral'

    def get_weighted_average_sentiment(self):
        weights = {'positive': 1, 'neutral': 0, 'negative': -1}
        weighted_sentiments = []

        for probabilities, _ in self.results:
            sentiment_scores = {self.labels[i]: prob for i, prob in enumerate(probabilities)}
            weighted_sentiment = sum(prob * weights[sent] for sent, prob in sentiment_scores.items())
            weighted_sentiments.append(weighted_sentiment)

        total_sent = np.mean(weighted_sentiments)

        print("Total sentiment: ", total_sent)

        return total_sent

    def summarize(self):
        text = ' '.join(self.sentences)
        summary = summarize(text, ratio=0.05)
        return summary

    def get_analysis(self):
        avg_scores = self.get_average_scores()
        extreme_sentences = self.find_extreme_sentences()
        overall_score = self.get_overall_score()
        weighted_average_sentiment=self.get_weighted_average_sentiment()
        summary = self.summarize()

        return {
            'average_scores': avg_scores,
            'extreme_sentences': {
                'negative': extreme_sentences[0],
                'positive': extreme_sentences[1],
            },
            'overall_score': overall_score,
            'weighted_average_sentiment': weighted_average_sentiment,
            'summary': summary,
        }