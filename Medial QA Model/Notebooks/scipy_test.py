import spacy

nlp = spacy.load("en_core_sci_sm")
doc = nlp("Tell A heart attack (myocardial infarction) and hypertension are medical emergencies.")
print([ent.text for ent in doc.ents])