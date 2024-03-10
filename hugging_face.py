from transformers import pipeline, AutoTokenizer
import torch


def generate_text(question, model):
    torch.manual_seed(0)
    tokenizer = AutoTokenizer.from_pretrained(model)
    generator = pipeline(
        "text-generation",
        #"question-answering",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        max_length=1000
    )
    
    result = generator(question)
    return result[0]['generated_text'].split('\n')

model = "tiiuae/falcon-7b-instruct"
#question = 'Make a short, concise and easy to understand sentence using the English noun "bank" that has the meaning "a financial institution that accepts deposits and channels the money into lending activities. Your answer should only contain the generated sentence."'
question = 'The english verb "house" has the meaning "contain or cover". A more general meaning of this verb "house" would be "admit" or "hold". Write a short, explanitory text to explain the linguistic relationship between the verb "house" and the aforementioned relationships with other words.'
generate_text(question, model)
