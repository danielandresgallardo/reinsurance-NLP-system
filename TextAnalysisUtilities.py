import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import DbUtilities
from fuzzywuzzy import fuzz

#NLP pipeline
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')

words =['reinsurance', 'insurance', 'group', 'limited', 'mutual', 'company', 'ltd', 'ltd.', 'inc', 'holdings', 'co', 'capital', 'international']

#Sentiment analysis(id, content)
def sentiment_analysis(content):

    #Sentiment analysis pipeline

    scores = []
    subjectivity_scores = []

    doc = nlp(content)
    #Split article to sentences
    for sent in doc.sents:
        #Sentiment analisis of every sentence
        sentiment = sent._.blob.polarity
        subjectivity = doc._.blob.subjectivity                        
        sentiment = round(sentiment,2)

        #Save to list
        scores.append(sentiment)
        subjectivity_scores.append(subjectivity)

    overall_sentiment = sum(scores) / len(scores)
    overall_sentiment = round(overall_sentiment, 2)


    overall_subjectivity = sum(subjectivity_scores) / len(subjectivity_scores)
    overall_subjectivity = round(overall_subjectivity, 2)
    return (overall_sentiment, overall_subjectivity)

#Named entity recognition(title, content)
def named_entity_recognition(content):

    doc = nlp(content)

    entities_list = []

    for word in doc.ents:
        if word.label_ == "ORG":
            entities_list.append(word.text)
    
    return entities_list

# Function to remove specified words from text using SpaCy
def remove_words_from_text(text, words):
    doc = nlp(text)
    cleaned_text = " ".join([token.text for token in doc if token.text.lower() not in words])
    return cleaned_text



def find_matches(article_id, entities, org_names, threshold):
    for entity in entities:
        entity = remove_words_from_text(entity, words)

        for reinsurer_id, org_name in org_names:
            org_name = remove_words_from_text(org_name, words)

            similarity_score = fuzz.ratio(entity.lower(), org_name.lower())

            if similarity_score >= threshold:
                print("Similarity found: ")
                print(entity)
                print(org_name)
                DbUtilities.link_reinsurer_to_article(article_id, reinsurer_id)

def extract_keywords(title, article_content):
    # Process the title and article content using spaCy's NLP pipeline
    doc = nlp(title + "\n" + article_content)

    # Initialize a set to store unique keywords
    keywords = set()

    # Define a set of part-of-speech tags that you want to consider as keywords (e.g., NOUN, ADJ)
    keyword_pos_tags = {"NOUN", "ADJ"}

    # Iterate through the processed tokens
    for token in doc:
        if token.pos_ in keyword_pos_tags:
            keywords.add(token.text)

    return list(keywords)

def calculate_category_probability(article_keywords, category_keywords_list):
    # Initialize an empty dictionary to store category probabilities
    category_probabilities = {}

    # Iterate through each category and its keywords
    for category_id, category_name, category_keywords in category_keywords_list:

        # Use spaCy to tokenize the keywords for more accurate matching
        article_keywords_tokens = nlp(" ".join(article_keywords))
        category_keywords_tokens = nlp(" ".join(category_keywords))

        # Calculate the probability score based on the number of matching tokens
        matching_tokens = len(set(token.text for token in article_keywords_tokens) & set(token.text for token in category_keywords_tokens))
        probability = matching_tokens / len(category_keywords_tokens)

        # Store the category probability
        category_probabilities[category_id] = probability

    return category_probabilities

def select_top_categories(category_probabilities):
    # Find the maximum probability value
    max_probability = max(category_probabilities.values())

    # Filter categories with the maximum probability
    top_categories = [category for category, probability in category_probabilities.items() if probability == max_probability]

    return top_categories

def set_categories(article_id, title, content):

    category_keywords_list = DbUtilities.get_categories()
    article_keywords = extract_keywords(title, content)
    category_probabilities = calculate_category_probability(article_keywords, category_keywords_list)
    top_categories = select_top_categories(category_probabilities)
    for category_id in top_categories:
        DbUtilities.link_category_to_article(article_id, category_id)


def Analyze_text(id, title, content):

    sentiment, subjectivity = sentiment_analysis(content)

    DbUtilities.add_sentiment_analysis(id, sentiment, subjectivity)

    ner_list = named_entity_recognition(content)
    org_list = DbUtilities.get_reinsurer_list()

    find_matches(id, ner_list, org_list, 70)

    set_categories(id, title, content)


#print(sentiment_analysis(content))
#print(named_entity_recognition(content))
#ner_list = named_entity_recognition(content)
#org_list = DbUtilities.get_reinsurer_list()

#find_matches(id, ner_list, org_list, 70)