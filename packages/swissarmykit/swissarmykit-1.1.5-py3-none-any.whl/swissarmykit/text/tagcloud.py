from wordcloud import WordCloud, STOPWORDS
from swissarmykit.utils.fileutils import FileUtils
import matplotlib.pyplot as plt


class TagCloud:

    def __init__(self):
        pass

    @staticmethod
    def plot_wordcloud(text='', path=None, max_font_size=None, stop_words=None, more_stopwords=None, title=''):
        '''

        :param text:
        :param path: File path
        :param max_font_size: ex: 40
        :return:
        '''
        if path:
            text = FileUtils.load_html_file(path)

        stopwords = None
        if isinstance(stop_words, set):
            stopwords = stop_words
        elif stop_words:
            stopwords = STOPWORDS

        if more_stopwords:
            if not isinstance(more_stopwords, set): raise Exception('more_stopwords must be set')
            if not stopwords: stopwords = set(STOPWORDS)
            stopwords = stopwords.union(more_stopwords)

        wordcloud = WordCloud(max_font_size=max_font_size, stopwords=stopwords).generate(text)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(title)
        plt.axis("off")
        plt.show()


if __name__ == '__main__':
    w = TagCloud()
    # w.word_cloud(path='C:/Users/Will/Desktop/code/ai_/ztest/artistfound.html')

    # lower max_font_size
    # w.word_cloud(path='C:/Users/Will/Desktop/code/ai_/ztest/artistfound.html', max_font_size=40)
    w.plot_wordcloud(path='C:/Users/Will/Desktop/code/ai_/ztest/artistfound.html', max_font_size=40, title='test')

