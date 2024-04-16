from gensim.summarization import summarize

class DocumentSummarizer:
    def __init__(self, text):
        self.text = text
        self.word_count = 100

    def docsummarize(self):
        # Generate the summary
        print("Summarizing the document...")
        summary = summarize(self.text, word_count=self.word_count)

        return summary