from googletrans import Translator
import db_connector

def translate_and_upload(id, title, content):

    translator = Translator()

    translated_title = translator.translate(title, dest='zh-tw').text

    translated_content = translator.translate(content, dest='zh-tw').text

    db_connector.add_translation(id, translated_title, translated_content)