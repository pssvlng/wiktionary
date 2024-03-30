import json
from transformers import pipeline, AutoTokenizer
from huggingface_hub import get_inference_endpoint, list_inference_endpoints
import torch
import requests
from secret import LANGUAGE_QUESTIONS_TOKEN

hard_wired_answers = {}
hard_wired_answers['en'] = """

"""

hard_wired_answers['de'] = """

"""

hard_wired_answers['nl'] = """

"""

hugging_face_models = {}
#hugging_face_models['en'] = "tiiuae/falcon-7b-instruct"
hugging_face_models['en'] = "openchat/openchat-3.5-0106"
#hugging_face_models['de'] = "Tanhim/gpt2-model-de"
#hugging_face_models['de'] = "svalabs/infoxlm-german-question-answering"
hugging_face_models['nl'] = "Pyjay/gpt2-medium-dutch-finetuned-text-generation"

hugging_face_models_api = {}
#hugging_face_models_api['en'] = "https://api-inference.huggingface.co/models/gpt2"
hugging_face_models_api['en'] ="https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
#hugging_face_models_api['en'] = "https://api-inference.huggingface.co/models/openchat/openchat-3.5-0106"
#hugging_face_models_api['en'] ="https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
#hugging_face_models_api['en'] = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
#hugging_face_models_api['en'] = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
hugging_face_models_api['de'] ="https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
hugging_face_models_api['nl'] ="https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
#hugging_face_models_api['de'] = "https://api-inference.huggingface.co/models/gpt2"
#hugging_face_models_api['nl'] = "https://api-inference.huggingface.co/models/gpt2"

#tokenizer_en = AutoTokenizer.from_pretrained("tiiuae/falcon-7b-instruct")
#tokenizer_de = AutoTokenizer.from_pretrained("Tanhim/gpt2-model-de")
#tokenizer_nl = AutoTokenizer.from_pretrained("Pyjay/gpt2-medium-dutch-finetuned-text-generation")

# hugging_face_models['en'] = pipeline(
    # "text-generation",
    # model="tiiuae/falcon-7b-instruct",
    # tokenizer=tokenizer_en,
    # torch_dtype=torch.bfloat16,
    # device_map="auto",
    # max_length=2000
# )
# hugging_face_models['de'] = pipeline(
    # "text-generation",
    # model="Tanhim/gpt2-model-de",
    # tokenizer=tokenizer_de,
    # torch_dtype=torch.bfloat16,
    # device_map="auto",
    # max_length=2000
# )
# hugging_face_models['nl'] = pipeline(
    # "text-generation",
    # model="Pyjay/gpt2-medium-dutch-finetuned-text-generation",
    # tokenizer=tokenizer_nl,
    # torch_dtype=torch.bfloat16,
    # device_map="auto",
    # max_length=2000
# )

def generate_text_from_hard_wired(paylaod, lang):
    return hard_wired_answers[lang]

def generate_text_from_api(question, lang):
    headers = {"Authorization": f"Bearer {LANGUAGE_QUESTIONS_TOKEN}"}
    payload = {     
        "inputs": question,
        #"task": "text-generation",        
        "task": "question-answering",
        "parameters": {"max_new_tokens": 5000} #"truncation": True}
    }
    response = requests.post(hugging_face_models_api[lang], headers=headers, json=payload)
    result_dict = response.json()[0]
    result_text = result_dict['generated_text']
    result_text = result_text.replace(question, '').replace('\n', ' ').strip()    
    return result_text

def generate_text_from_model(question, lang):    
    torch.manual_seed(0)
    tokenizer = AutoTokenizer.from_pretrained(hugging_face_models[lang])
    generate_pipeline = pipeline(
        "text-generation",
        #"question-answering",
        #"question-answering"
        model=hugging_face_models[lang],
        tokenizer=tokenizer,
        #torch_dtype=torch.bfloat16,
        device_map="auto",
        max_length=512,     
    )

    result = generate_pipeline(question)
    #return result[0]['generated_text'].split('\n')[1]
    return result[0]['generated_text']

#model = "tiiuae/falcon-7b-instruct"
#question = 'Make a short, concise and easy to understand sentence using the English noun "bank" that has the meaning "a financial institution that accepts deposits and channels the money into lending activities. Your answer should only contain the generated sentence."'
#question = 'The english verb "house" has the meaning "contain or cover". A more general meaning of this verb "house" would be "admt" or "hold". Write a short, explanitory text to explain the linguistic relationship between the verb "house" and the aforementioned relationships with other words.'
#generate_text(question, model)

question = """
<|system|>
 You are a system for answering long, linguistic related questions in the German language. Generate explanatory text in German for the given question.
<|user|>
'fahrbarer Untersatz' ist ein Substantiv in Deutsch, und es bedeutet von einem Motor angetriebenes Fahrzeug, dessen Bauart überwiegend zur Personenbeförderung bestimmt ist. Synonyme für fahrbarer Untersatz sind: Pkw, Personenwagen, Motorwagen, PKW, Auto, Automobil, Blechbüchse, Personenkraftwagen, Wagen Wort(e) mit einer verwandten, aber allgemeineren Bedeutung des deutschen Substantivs 'fahrbarer Untersatz' sind 'Mfz, Kfz, Motorfahrzeug, Kraftfahrzeug'. Wort(e) mit einer verwandten, aber spezifischeren Bedeutung des deutschen Substantivs 'fahrbarer Untersatz' sind 'Krankentransportwagen, Krankenkraftwagen, Rettungswagen, Krankenwagen, Kombiwagen, Kombinationskraftwagen, Variant, Kombilimousine, Kombinationswagen, Kombi, Autobus, Bus, Omnibus, Fährmann, hol över, hallo, Taxi, Taxi, Kleinwagen, Kompakt'. Das deutsche Substantiv 'fahrbarer Untersatz' ist Teil des/der Wortes/Wörter 'Dashcam'. Wort(e), die Teil des deutschen Substantivs 'fahrbarer Untersatz' sind, sind 'Fahrpedal, Gaspedal, Airbag, Autozubehör, Kraftfahrzeugmotor, Autohupe, Hupe, Motorhupe'. Schreiben Sie einen kurzen erklärenden Text, um die sprachliche Beziehung zwischen dem Substantiv 'fahrbarer Untersatz' und den oben genannten Beziehungen zu anderen Wörtern zu erläutern.
<|assistant|>
"""

question_2 = "'fahrbarer Untersatz' ist ein Substantiv in Deutsch, und es bedeutet von einem Motor angetriebenes Fahrzeug, dessen Bauart überwiegend zur Personenbeförderung bestimmt ist. Synonyme für fahrbarer Untersatz sind: Pkw, Personenwagen, Motorwagen, PKW, Auto, Automobil, Blechbüchse, Personenkraftwagen, Wagen Wort(e) mit einer verwandten, aber allgemeineren Bedeutung des deutschen Substantivs 'fahrbarer Untersatz' sind 'Mfz, Kfz, Motorfahrzeug, Kraftfahrzeug'. Wort(e) mit einer verwandten, aber spezifischeren Bedeutung des deutschen Substantivs 'fahrbarer Untersatz' sind 'Krankentransportwagen, Krankenkraftwagen, Rettungswagen, Krankenwagen, Kombiwagen, Kombinationskraftwagen, Variant, Kombilimousine, Kombinationswagen, Kombi, Autobus, Bus, Omnibus, Fährmann, hol över, hallo, Taxi, Taxi, Kleinwagen, Kompakt'. Das deutsche Substantiv 'fahrbarer Untersatz' ist Teil des/der Wortes/Wörter 'Dashcam'. Wort(e), die Teil des deutschen Substantivs 'fahrbarer Untersatz' sind, sind 'Fahrpedal, Gaspedal, Airbag, Autozubehör, Kraftfahrzeugmotor, Autohupe, Hupe, Motorhupe'. Schreiben Sie einen kurzen erklärenden Text in Deutsch, um die sprachliche Beziehung zwischen dem Substantiv 'fahrbarer Untersatz' und den oben genannten Beziehungen zu anderen Wörtern zu erläutern."
question_3 = 'The english verb "house" has the meaning "contain or cover". A more general meaning of this verb "house" would be "admit" or "hold". Write a short, explanitory text to explain the linguistic relationship between the verb "house" and the aforementioned relationships with other words.'
question_4 = "The engilish noun 'bank' has the meaning 'a long ridge or pile'. "


#print(generate_text_from_api(question_3, 'en'))
#payload = {
        #"inputs": 'The english verb "house" has the meaning "contain or cover". A more general meaning of this verb "house" would be "admit" or "hold". Write a short, explanitory text to explain the linguistic relationship between the verb "house" and the aforementioned relationships with other words.',
        #'inputs': "'fahrbarer Untersatz' ist ein Substantiv in Deutsch, und es bedeutet von einem Motor angetriebenes Fahrzeug, dessen Bauart überwiegend zur Personenbeförderung bestimmt ist. Synonyme für fahrbarer Untersatz sind: Pkw, Personenwagen, Motorwagen, PKW, Auto, Automobil, Blechbüchse, Personenkraftwagen, Wagen Wort(e) mit einer verwandten, aber allgemeineren Bedeutung des deutschen Substantivs 'fahrbarer Untersatz' sind 'Mfz, Kfz, Motorfahrzeug, Kraftfahrzeug'. Wort(e) mit einer verwandten, aber spezifischeren Bedeutung des deutschen Substantivs 'fahrbarer Untersatz' sind 'Krankentransportwagen, Krankenkraftwagen, Rettungswagen, Krankenwagen, Kombiwagen, Kombinationskraftwagen, Variant, Kombilimousine, Kombinationswagen, Kombi, Autobus, Bus, Omnibus, Fährmann, hol över, hallo, Taxi, Taxi, Kleinwagen, Kompakt'. Das deutsche Substantiv 'fahrbarer Untersatz' ist Teil des/der Wortes/Wörter 'Dashcam'. Wort(e), die Teil des deutschen Substantivs 'fahrbarer Untersatz' sind, sind 'Fahrpedal, Gaspedal, Airbag, Autozubehör, Kraftfahrzeugmotor, Autohupe, Hupe, Motorhupe'. Schreiben Sie einen kurzen erklärenden Text, um die sprachliche Beziehung zwischen dem Substantiv 'fahrbarer Untersatz' und den oben genannten Beziehungen zu anderen Wörtern zu erläutern.",
        #"inputs": question_3,
        #"task": "image-generation",
        #"parameters": {"task": "image-generation"} #"truncation": True}
        #"parameters": {"max_new_tokens": 5000} #"truncation": True}
    #}

