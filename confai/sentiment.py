import re
import heapq
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class SentimentAnalyzer:
    def __init__(self, text):
        self.sentences = re.split(r'(?<=[.!?]) +', text)
        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        self.labels = {0: 'positive', 1: 'negative', 2: 'neutral', }
        self.softmax = torch.nn.Softmax(dim=0)  # Softmax function for converting logits to probabilities
        self.results = self.run_model()

    def run_model(self):
        print("Running the model...")
        inputs = self.tokenizer(self.sentences, return_tensors="pt", padding=True, truncation=True)
        outputs = self.model(**inputs)
        results = []
        for idx, _ in enumerate(self.sentences):
            logits = outputs.logits[idx].detach()
            probabilities = self.softmax(logits).numpy()  # Convert logits to probabilities
            results.append((probabilities, self.sentences[idx]))
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

        print(avg_scores)

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

    def get_analysis(self):
        avg_scores = self.get_average_scores().tolist()
        extreme_sentences = self.find_extreme_sentences()
        overall_score = self.get_overall_score()

        return {
            'average_scores': avg_scores,
            'extreme_sentences': {
                'negative': [sent for score, sent in extreme_sentences[0]],
                'positive': [sent for score, sent in extreme_sentences[1]],
            },
            'overall_score': overall_score,
        }