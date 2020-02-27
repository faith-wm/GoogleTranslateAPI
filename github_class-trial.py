



import csv
import pandas as pd
import sys
import os



from google_api_translate import Translator
from google.oauth2 import service_account




class GoogleAPI_translate_text:
    def __init__(self, credentials_path,source_language, target_language,source_lang_file,translated_file):
        self.credentials_path=credentials_path
        self.source_language=source_language
        self.target_language=target_language
        self.source_lang_file=source_lang_file
        self.translated_file=translated_file


    def translate_text(self, text):
        translator = Translator(creds_path=self.credentials_path)
        translate = translator.translate(text,source_language=self.source_language, target_language=self.target_language)
        return translate.text


    def save_translated_text(self):
        read_sourceLang_file = pd.read_csv(self.source_lang_file)
        read_sourceLang_file=read_sourceLang_file.dropna()

        try:
            read_translated_file = pd.read_csv(self.translated_file)
            if len(read_sourceLang_file)-1!=len(read_translated_file):
                start_len = len(read_translated_file) + 1
            else:
                if len(read_sourceLang_file)-1==len(read_translated_file):
                    sys.exit()

        except FileNotFoundError:
            start_len = 0

        print("=====translated so far: {}/ {} sentences=====".format(start_len, len(read_sourceLang_file)))
        read_sourceLang_file = read_sourceLang_file.iloc[start_len:start_len + 5, :]              #i want to translate in  batches of 5 because sometimes the API connection stops midway
                                                                                    #this will save time as i will immediately know when connection is lost

        index=start_len
        for col in read_sourceLang_file.itertuples():
            text=str(col[1])
            translated_text=GoogleAPI_translate_text.translate_text(self,text)

            index+=1
            my_dict={index:[text,translated_text]}

            with open(self.translated_file, 'a') as outfile:
                writer = csv.writer(outfile)
                for k, v in my_dict.items():
                    writer.writerow([k] + v)

        return 0



if __name__ == '__main__':
    cred_file = "xxx.json" #path to credentials json file  # enter your API key here- for details on how to get your API key see this this link  https://developers.google.com/places/web-service/get-api-key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_file
    credentials = service_account.Credentials.from_service_account_file(cred_file)
    creds_path = os.path.join(os.path.dirname(__file__), cred_file)

    while True:
        credentials_path = creds_path
        source_lang_file = 'all-sentences.csv'
        translated_file = 'translated-file.csv'
        source_lang = 'ja'
        target_lang = 'en'

        translator=GoogleAPI_translate_text(credentials_path,source_lang,target_lang,source_lang_file,translated_file)

        translator.save_translated_text()


