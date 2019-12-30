from pandas import read_csv, DataFrame
import pandas as pd
import requests
import json
import urllib
import time

OCP_ACIM_SUBSCRIPTION_KEY = ''
LUIS_APP_ID = ''
LUIS_SUBSCRIPTION_KEY = ''

# windows
# file = r''
# data = pd.read_csv(file, delimiter=',')

# unix
file = 'TranslateIntents.xlsx'
data = pd.read_excel(file, delimiter=',')

data
# print(data)

azure_language_codes = {"EN":"en","MY":"ms","ZH":"zh-Hans"}

def translate_utterance(utterance, from_lang):
    url = "https://api-apc.cognitive.microsofttranslator.com/translate"

    from_lang = azure_language_codes[from_lang]

    querystring = {"api-version":"3.0","from":from_lang,"to":"en","":""}

    payload = "[{\"Text\": \""+str(utterance)+"\"}]"
    headers = {
        'Ocp-Apim-Subscription-Key': OCP_ACIM_SUBSCRIPTION_KEY,
        'Content-Type': "application/json",
        }

    response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers, params=querystring)
    return response, json.loads(response.text)[0]['translations'][0]['text']

def get_intent(utterance):
    url = f"https://southeastasia.api.cognitive.microsoft.com/luis/v2.0/apps/{LUIS_APP_ID}"

    querystring = {
        "staging":"true",
        "verbose":"true",
        "timezoneOffset":"-360",
        "subscription-key":LUIS_SUBSCRIPTION_KEY,
        "q":utterance
        }

    payload = ""

    response = requests.request("GET", url, data=payload, params=querystring)

    intent = ""
    entities = {}
    try:
        intent = json.loads(response.text)['topScoringIntent']['intent']
        for entity in json.loads(response.text)['entities']:
            entities[entity['type']] = entity['entity']
    except:
        return "Intent error"

    return (intent, entities)

def get_intents(lang):
    print("========== "+lang+" Intents ==========")
    if 'EN' in lang:
        for row in data[lang]:
                intent = get_intent(row)
                print(intent)
                time.sleep(0.2)
    else:
        for row in data[lang]:
            translated_utterance = translate_utterance(row, lang)
            intent = get_intent(translated_utterance)
            print(intent)
            time.sleep(0.2)

def get_translations(lang):
    print("========== "+lang+" Translations ==========")
    for row in data[lang]:
        print(translate_utterance(row, lang))

if __name__ == '__main__':
    res, json = translate_utterance("hello world", "EN")
    type(res.json())
    # translate
    # get_translations('MY')
    # get_translations('ZH')

    # get intents for untranslated utterances
    # get_intents('EN')
    # get_intents('MY')
    # get_intents('ZH')

    # get intents for translated utterances
    # get_intents('MY->EN')
    get_intents('ZH->EN')
