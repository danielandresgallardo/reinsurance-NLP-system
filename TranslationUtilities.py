from googletrans import Translator
import DbUtilities

def translate_and_upload(id, title, content):

    translator = Translator()

    translated_title = translator.translate(title, dest='zh-tw').text

    translated_content = translator.translate(content, dest='zh-tw').text

    DbUtilities.add_translation(id, translated_title, translated_content)