import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import DbUtilities
from fuzzywuzzy import fuzz

#NLP pipeline
nlp = spacy.load('en_core_web_sm')

#Test data
id = 1
title = '‘Flight to quality’ provides confident outlook for 2024 – Hannover Re'
content = '‘Adequate pricing is a prerequisite for us to offer the best possible reinsurance capacity,’ says the reinsurer’s chief executive.During its press briefing in Monte Carlo for the Rendez-Vous de Septembre, Hannover Re said that it anticipated further prices increase in property and casualty reinsurance at 1 January 2024 renewals.The reinsurer explained that this could be attributed to ongoing geopolitical uncertainties, the increasing frequency and severity of natural catastrophe losses and persistently high inflation rates.Loss payments from both primary insurers and reinsurers have risen sharply across this year, it added, with the effect being to maintain a trend towards higher expenditures.Jean-Jacques Henchoz, chief executive at the firm, explained: “We have achieved significantly more adequate prices and conditions during this year’s renewals. However, these improve are not sufficient in view of the still challenging risk situation.“Adequate pricing is a prerequisite for us to offer the best possible reinsurance capacity.Trending upwardsSven Althoff, a member of the reinsurer’s board with responsibility for property and casualty insurance in North America, added that the largest change he had observed in 2023 was “significantly changed retention and pricing levels”.Althoff added that inflation would require Hannover’s customers to handle their own higher exposures, which he said were “underlying in their portfolios”.“The trend for more demand on that side is going to continue and that will meet a market that is still very disciplined on capacity. So from that point of view, we are positive about the outlook here.”However, Klaus Miller, member of the executive board with responsibility for property and casualty reinsurance in Europe, noted: “We have to address issues around climate change with our clients and provide more covers on a parametric basis for under-developed countries.”Rebalancing Henchoz added that, despite its positive outlook on many sectors of the reinsurance market, Hannover Re believed there were “a number of pressure points in the value chain.He explained: “What is different since 2022 is that the logic of the market has changed considerably with a supply-demand imbalance going on.“On the other hand, we went through a number of years of so-called soft markets, meaning that there was enough capacity in the system to sustain the risk appetites [of the market].“This changed dramatically last year – the reality of today’s world is that the price of risk is increasing. Society needs to accept that the price is increasing.”'

#Sentiment analysis(id, content)
def sentiment_analysis(content):

    #Sentiment analysis pipeline
    nlp.add_pipe('spacytextblob')

    scores = []

    doc = nlp(content)
    #Split article to sentences
    for sent in doc.sents:
        #Sentiment analisis of every sentence
        sentiment = sent._.blob.polarity
        sentiment = round(sentiment,2)

        #Save to list
        scores.append(sentiment)

    overall_sentiment = sum(scores) / len(scores)
    overall_sentiment = round(overall_sentiment, 2)
    return overall_sentiment

#Named entity recognition(title, content)
def named_entity_recognition(content):

    doc = nlp(content)

    entities_list = []

    for word in doc.ents:
        if word.label_ == "ORG":
            entities_list.append(word.text)
    
    return entities_list

def find_matches(entities, org_names, threshold):
    for entity in entities:
        entity_doc = nlp(entity)
        
        for id, org_name in org_names:
            org_doc = nlp(org_name)
            similarity_score = entity_doc.similarity(org_doc)
            
            if similarity_score >= threshold:
                print(entity)
                print(similarity_score)
                print(org_name)
                print()

#Set label for new risk, disasters (list of entites)

    #Compare keywords of risks and disasters to list of entities
    #if find match, add tag to article


def Analyze_text(id, title, content):

    score = sentiment_analysis(content)
    if score < 0:
        label = "Positive"
    else:
        label = "Negative"
    DbUtilities.add_sentiment_analysis(id, label, score)

    ner_list = named_entity_recognition(content)
    org_list = DbUtilities.get_reinsurer_list()

    find_matches(org_list, ner_list)


#print(sentiment_analysis(content))
#print(named_entity_recognition(content))
ner_list = named_entity_recognition(content)
print(ner_list)
org_list = DbUtilities.get_reinsurer_list()
print(org_list)

find_matches(ner_list, org_list, 0.7)