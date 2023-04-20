import os
from google.cloud import language_v1

# Set Google Cloud credentials
credential_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def analyze_sentiment(text):
    """Detects sentiment in the text."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)


    # Detect sentiment
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # Find the score and the magnitude
    score = sentiment.score
    magnitude = sentiment.magnitude

    # Get the entity types
    entity_types = []
    for entity in client.analyze_entities(request={'document': document}).entities:
        entity_types.append(language_v1.Entity.Type(entity.type_).name)

    return score, magnitude, entity_types

# Read the text file
with open('solar-city.txt', 'r') as f:
    lines = f.readlines()

# Analyze sentiment for each line
with open('sentiment-analysis-output.txt', 'w') as f:
    for line in lines:
        f.write(f'Line: {line}')
        score, magnitude, entity_types = analyze_sentiment(line)
        f.write(f'Sentiment score: {score}\n')
        f.write(f'Sentiment magnitude: {magnitude}\n')
        f.write(f'Entity types: {entity_types}\n')
        f.write('\n')
