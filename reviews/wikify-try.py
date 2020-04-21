import spacy
import  pprint

from spacy.pipeline import EntityRuler

nlp = spacy.load('D:\\Projects-intellij\\funny-reviews\\data\\entity-linking-model\\nlp')

ruler = EntityRuler(nlp)
patterns = [{"label": "ORG", "pattern": "kimchi"}, {"label": "ORG", "pattern": "cold"}]
ruler.add_patterns(patterns)
nlp.add_pipe(ruler)

doc = nlp("""
I'd like to personally shake Mr Tofu's hand.  While I cannot medically prove it, I am 100% certain that their soondubu contains undefined healing properties.  Some how some way, I always feel better after a meal here.  
Got a cold?  Screw the Nyquil and get the spicy kimchi soondubu.
""")

# document level

ents = [(e.text, e.label_, e.kb_id_) for e in doc.ents]
pprint.pprint(ents, indent=2)
