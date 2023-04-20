import os
from google.cloud import language_v1

# Set Google Cloud credentials
credential_path = '/home/harisnadeem0808/sentiment-gcp-hr/sentiment-analysis-379200-2ea99281f818.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def analyze_sentiment(text):
    """Detects sentiment in the text and entities present."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detect sentiment
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # Find the score and the magnitude
    score = sentiment.score
    magnitude = sentiment.magnitude

    # Get the entity types and names
    entities = []
    for entity in client.analyze_entities(request={'document': document}).entities:
        entity_type = language_v1.Entity.Type(entity.type_).name
        if entity.metadata.get('wikipedia_url'):
            entity_name = entity.metadata.get('wikipedia_url').split('/')[-1].replace('_', ' ')
        else:
            entity_name = entity.name
        entities.append((entity_type, entity_name))

    return score, magnitude, entities

# Read the text file
with open('solar-city.txt', 'r') as f:
    lines = f.readlines()

# Analyze sentiment for each line
with open('sentiment-analysis-output.txt', 'w') as f:
    for line in lines:
        f.write(f'Line: {line}')
        score, magnitude, entities = analyze_sentiment(line)
        f.write(f'Sentiment score: {score}\n')
        f.write(f'Sentiment magnitude: {magnitude}\n')
        f.write('Entities:\n')
        for entity_type, entity_name in entities:
            f.write(f'{entity_type}: {entity_name}\n')
        f.write('\n')
