from imdbpie import Imdb
import string

imdb = Imdb()
reviews = imdb.get_title_user_reviews("tt0245429")

# pprint.pprint(reviews.keys())
# pprint.pprint(reviews["reviews"])

# print(reviews['reviews'][0]['author']['displayName'])
# print(reviews['reviews'][0]['reviewText'])
# print(type(reviews['totalReviews']))


def reviews_to_list(reviews):
    """
    input: dictionary from imdb
    output: list of reviews
    """
    l = []
    for item in reviews['reviews']:
        content = item['reviewText']
        l.append(content)
    return l

def words_to_list(text):
    """
    input: string of a single review
    output: list of words from a single review
    """
    l = []
    for item in text.split():
        n = item
        n = n.strip(string.whitespace + string.punctuation)
        n = n.lower()
        l.append(n)
    return l

def count_words(text):
    """
    input: list of reviews
    ouput: dictonary with counter
    """
    counter = {}
    for review in text:
        review_words = words_to_list(review)
        for word in review_words:
            if word not in counter:
                counter[word] = 1
            else:
                counter[word] += 1
    return counter

def most_common(dict, n):
    """
    input: dictionary of counter
    output: most used words
    """
    # Find the most common words:
    l = []
    for item in dict.items():
        l.append(item)
    l.sort(key = lambda x: x[1], reverse=True)

    # Print the most common words:
    print('The most used words are:')
    for i in range(n):
        print(f'{i+1}. {l[i][0]}')
 
def main():
    all_reviews = reviews_to_list(reviews)
    dict_counter = count_words(all_reviews)

    most_common(dict_counter, 10)

if __name__ == '__main__':
    main()