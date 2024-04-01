import os
import shutil
from gtts import gTTS
from imaginairy.schema import ImaginePrompt
from imaginairy.api import imagine

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import wn
from hugging_face import generate_text_from_api
from imageCreation.CombinedImageWrapper import main

from video_generation_consts import *
from moviepy.editor import AudioClip, VideoFileClip, VideoClip, ImageClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx import resize

def merge_images(background_image, foreground_image, result_image, image_size):
    background = Image.open(background_image)
    foreground = Image.open(foreground_image)    
    if foreground.size > background.size:
        background = background.resize(foreground.size, Image.LANCZOS)
    else:
        foreground = foreground.resize(background.size, Image.LANCZOS)            
    result = Image.alpha_composite(background.convert('RGBA'), foreground.convert('RGBA'))    
    result = result.resize(image_size, Image.LANCZOS)
    result.save(result_image)

def make_overlay_image(image_path, output_path, transparency=204):
    original_image = Image.open(image_path)    
    overlay = Image.new('RGBA', original_image.size, (255, 255, 255, transparency))
    result = Image.alpha_composite(original_image.convert('RGBA'), overlay)
    result.save(output_path)

def __chunk(phrase_dict, text, index: int = 0):
        if len(text) <= 55:
                phrase_dict[index + 1] = text
                return phrase_dict
        else:
            word_list = text.split(' ')
            while len(' '.join(word_list)) > 55:
                word_list = word_list[:len(word_list) -1]
            insert_text = text[:len(' '.join(word_list))]
            index += 1
            phrase_dict[index] = insert_text
            return __chunk(phrase_dict, text[len(' '.join(word_list)):len(text)], index)

def make_title_image(image_path, synset, lemma, output_path):    
    image = Image.open(image_path)        
    image_adjusted = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image_adjusted)    
    font = ImageFont.truetype("arial.ttf", 24)        
    font_sub = ImageFont.truetype("arial.ttf", 16)        
    text_color = (0, 0, 0)  
    lemmas = synset.lemmas()
    lemmas.remove(lemma)
    text1 = f"{lemma} [{pos_description_short[synset.lexicon().language][synset.pos]}]"              
    text_x = 20
    text_y = 10    
    definition_parts = {}    
    definition_parts = __chunk(definition_parts, synset.definition())        
    synonym_parts = {}
    if len(lemmas) > 1:
        synonym_parts = __chunk(synonym_parts, f"{synonyms[synset.lexicon().language]}: {', '.join(lemmas)}")        
    rectangle_coords = [0, 0, image.width, 40 + 20*len(definition_parts) + 20*len(synonym_parts)]
    fill_color = (255, 255, 255, 196) 
    draw.rectangle(rectangle_coords, fill=fill_color)

    draw.text((text_x, text_y), text1, fill=text_color, font=font)        
    text_y += 10    
    for key in sorted(synonym_parts):
        text_y += 20
        draw.text((text_x, text_y), synonym_parts[key].strip(), fill=text_color, font=font_sub)                
    for key in sorted(definition_parts):
        text_y += 20
        draw.text((text_x, text_y), definition_parts[key].strip(), fill=text_color, font=font_sub)            

    result = Image.alpha_composite(image.convert("RGBA"), image_adjusted)
    result.save(output_path)
    return result.size

def make_tiled_image(image_files, output_file):
    image_list = [Image.open(image_files[0])]    
    width, height = image_list[0].size    
    for image_file in image_files[1:]:
        image_list.append(Image.open(image_file).resize((width, height)))
    
    num_images = len(image_list)
    side_length = int(num_images ** 0.5) 

    tiled_image = Image.new("RGB", (width*side_length, height*side_length))    
    for i, image in enumerate(image_list):
        x = (i % side_length) * width
        y = (i // side_length) * height
        tiled_image.paste(image, (x, y))
        
    tiled_image.save(output_file)

def make_white_transparent(image_path, output_path):    
    image = Image.open(image_path)
    image = image.convert("RGBA")    
    image_data = image.getdata()
    
    new_image_data = []
    for item in image_data:
        if item[:3] == (255, 255, 255):
            new_image_data.append((255, 255, 255, 0))
        else:
            new_image_data.append(item)
    image.putdata(new_image_data)
    image.save(output_path)

def make_title_page_audio(synset, lang, lemma, output_file):
    lemmas = synset.lemmas()
    lemmas.remove(lemma)
    definition = synset.definition()
    title_page_template = title_page[lang]
    synonym_text_template = synonym_text[lang]
    audio_text = title_page_template.replace('{LEMMAS}', lemma).replace('{POS}', pos_description[lang][synset.pos]).replace('{DEFINITION}', definition)    
    if len(lemmas) > 1:
        audio_text += synonym_text_template.replace('{LEMMA}', lemma).replace('{SYNONYMS}', ', '.join(lemmas))
    tts = gTTS(audio_text, lang=synset.lexicon().language)    
    tts.save(output_file)

def make_example_page_audio(synset, lang, output_file):
    examples = synset.examples()
    if len(examples) > 0:            
        example_text_template = example[lang]
        example_text = example_text_template.replace('{SENTENCE}', examples[0])        
        tts = gTTS(example_text, lang=synset.lexicon().language)    
        tts.save(output_file)

def make_diagram_audio(synset, lemma, output_file):
    lang = synset.lexicon().language    
    lemmas = synset.lemmas()
    lemmas.remove(lemma)
    hypernyms = synset.hypernyms()
    hyponyms = synset.hyponyms()
    meronyms = synset.meronyms()
    holonyms = synset.holonyms()
    definition = synset.definition()
    text_list = []
    intro_text = title_page[lang].replace('{LEMMAS}', lemma).replace('{POS}', pos_description[lang][synset.pos]).replace('{DEFINITION}', definition)    
    text_list.append(intro_text)
    if len(lemmas) > 1:
        synonym_text_result = synonym_text[lang].replace('{LEMMA}', lemma).replace('{SYNONYMS}', ', '.join(lemmas))
        text_list.append(synonym_text_result)
    if len(hypernyms) > 0:
        hypernym_lemmas = [f'{", ".join(x.lemmas())}' for x in hypernyms[:5]]
        hypernym_text_result = hypernym_text[lang].replace('{POS}', pos_description[lang][synset.pos]).replace('{LEMMAS}', lemma).replace('{HYPERNYMS}', ', '.join(hypernym_lemmas))                
        text_list.append(hypernym_text_result)
    if len(hyponyms) > 0:
        hyponym_lemmas = [f'{", ".join(x.lemmas())}' for x in hyponyms[:5]]
        hyponym_text_result = hyponym_text[lang].replace('{POS}', pos_description[lang][synset.pos]).replace('{LEMMAS}', lemma).replace('{HYPONYMS}', ', '.join(hyponym_lemmas))                            
        text_list.append(hyponym_text_result)
    if len(holonyms) > 0:
        holonym_lemmas = [f'{", ".join(x.lemmas())}' for x in holonyms[:5]]
        holonym_text_result = holonym_text[lang].replace('{POS}', pos_description[lang][synset.pos]).replace('{LEMMAS}', lemma).replace('{HOLONYMS}', ', '.join(holonym_lemmas))    
        text_list.append(holonym_text_result)
    if len(meronyms) > 0:
        meronym_lemmas = [f'{", ".join(x.lemmas())}' for x in meronyms[:5]]
        meronym_text_result = meronym_text[lang].replace('{POS}', pos_description[lang][synset.pos]).replace('{LEMMAS}', lemma).replace('{MERONYMS}', ', '.join(meronym_lemmas))    
        text_list.append(meronym_text_result)
    prompt_instruction_result = prompt_instruction[lang].replace('{POS}', pos_description[lang][synset.pos]).replace('{LEMMAS}', lemma)
    text_list.append(prompt_instruction_result)
    text_prompt = ' '.join(text_list).replace('\n', '')    
    result_text = generate_text_from_api(text_prompt, lang)    
    tts = gTTS(result_text, lang=lang)    
    tts.save(output_file)

def make_example_sentence_image(synset, input_file, output_file):    
    image = Image.open(input_file)        
    image_adjusted = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image_adjusted)    
    font = ImageFont.truetype("arial.ttf", 20)            
    text_color = (0, 0, 0)  
    examples = synset.examples()
    if len(examples) == 0:
       shutil.copyfile(input_file, output_file) 
       return
    
    text1 = f"{examples[0]}"              
    text_x = 20
    text_y = 10  
    example_parts = {}      
    example_parts = __chunk(example_parts, text1)        
    rectangle_coords = [0, 0, image.width, 40 + 20*len(example_parts)]
    fill_color = (255, 255, 255, 196) 
    draw.rectangle(rectangle_coords, fill=fill_color)    
    for key in sorted(example_parts.items()):        
        draw.text((text_x, text_y), example_parts[key].strip(), fill=text_color, font=font)        
        text_y += 20
    
    result = Image.alpha_composite(image.convert("RGBA"), image_adjusted)
    result.save(output_file)

def make_video_from_image(image_input_file, video_output_file, audio_input_file=None, duration=3.00):        
    image = ImageClip(image_input_file)    
    audio = AudioFileClip(audio_input_file) if audio_input_file and os.path.exists(audio_input_file) else None
    if audio:
        image = image.set_audio(audio)
        image = image.set_duration(audio.duration)
    else:
        image = image.set_duration(duration)            
    image.write_videofile(video_output_file, codec='libx264', fps=24)        

def make_title_page_video(image_input_file, audio_input_file, video_output_file):            
    image_clip = ImageClip(image_input_file)
    audio_clip = AudioFileClip(audio_input_file)
    video_duration = audio_clip.duration
    video_clip = image_clip.set_duration(video_duration)
    video_clip = video_clip.set_audio(audio_clip)    
    video_clip.write_videofile(video_output_file, codec="libx264", fps=24)

def make_images_from_word_pos(woi, lang, filterLangs, pos):
    for synset in wn.synsets(woi, lang=lang, pos=pos):
        make_images(synset, lang, filterLangs)

def make_images_from_ili(ili, lang, filterLangs):
    synset = wn.synsets(ili=ili, lang=lang)
    make_images(synset[0], lang, filterLangs)

def make_images(synset, lang, filterLangs):
    def check_files_exist(file_names):
        for file_name in file_names:
            if not os.path.exists(file_name):    
                return False        
        return True
    
    args_dict = {}            
    args_dict['level'] = '2'
    args_dict['filterLangs'] = filterLangs
    args_dict['maxLeafNodes'] = '3'
    args_dict['ili'] = synset.ili.id
    args_dict['synonymCount'] = '1'
    args_dict['synsetId'] = synset.id        
    args_dict['hierarchy'] = 'True'
    args_dict['partWhole'] = 'True'
    
    base_path = f"synset_media/{synset.ili.id}/"        
    lang_path = f"{base_path}{lang}/"
    if not os.path.exists(f"{base_path}"):    
            os.makedirs(f"{base_path}")
    if not os.path.exists(f"{lang_path}"):                    
            os.makedirs(f"{lang_path}")

    lemmas = synset.lemmas()
    prompts = []
    image_files = []    
    
    tiled_output_file = f'{base_path}{synset.ili.id}_tiled.png'    
    tiled_transparent_output_file = f'{base_path}{synset.ili.id}_tiled_transparent.png'    

    file_verification_list = [f'{base_path}{synset.ili.id}_0.jpg',
                                f'{base_path}{synset.ili.id}_1.jpg', 
                                f'{base_path}{synset.ili.id}_2.jpg', 
                                f'{base_path}{synset.ili.id}_3.jpg', 
                                tiled_output_file, 
                                tiled_transparent_output_file]
    if check_files_exist(file_verification_list):
        image_files.append(f'{base_path}{synset.ili.id}_0.jpg')
        image_files.append(f'{base_path}{synset.ili.id}_1.jpg')
        image_files.append(f'{base_path}{synset.ili.id}_2.jpg')
        image_files.append(f'{base_path}{synset.ili.id}_3.jpg')
    else:            
        for i in range(4):
            lemma = lemmas[len(lemmas) - 1] if i > len(lemmas) - 1 else lemmas[i]
            prompts.append(ImaginePrompt(f"{lemma}: {synset.definition()}"))
        for index, imagine_result in enumerate(imagine(prompts)):            
            image_file = f'{base_path}{synset.ili.id}_{index}.jpg'
            image_files.append(image_file)
            imagine_result.save(image_file)            
        make_tiled_image(image_files, tiled_output_file)        
        make_overlay_image(tiled_output_file, tiled_transparent_output_file)
    
    for lemma in lemmas:        
        formatted_lemma = lemma.replace(' ', '-')
        args_dict['fileName'] = f"hierarchy_partwhole_{formatted_lemma}_{synset.pos}_{str(datetime.now().timestamp()).replace('.', '')}_{lang}_2_3_1"
        args_dict['lemma'] = lemma
        result = main(args_dict)       
        make_white_transparent(result['filePath'], f"{lang_path}{synset.ili.id}_{formatted_lemma}.png") 
        
        image_size = make_title_image(image_files[0], synset, lemma, f"{lang_path}{synset.ili.id}_{formatted_lemma}_title.png")
        title_page_audio_file = f"{lang_path}{synset.ili.id}_{formatted_lemma}_title.mp3"
        make_title_page_audio(synset, lang, lemma, title_page_audio_file)
        title_page_video_file = f"{lang_path}{synset.ili.id}_{formatted_lemma}_title.mp4"
        make_title_page_video(f"{lang_path}{synset.ili.id}_{formatted_lemma}_title.png", title_page_audio_file, title_page_video_file)
        if not check_files_exist(f"{lang_path}{synset.ili.id}_composite.png"):
            merge_images(tiled_transparent_output_file, f"{lang_path}{synset.ili.id}_{formatted_lemma}.png", f"{lang_path}{synset.ili.id}_composite.png", image_size)                    

        make_example_sentence_image(synset, image_files[1], f"{lang_path}{synset.ili.id}_{formatted_lemma}_example.png")        
        example_sentence_audio_file = f"{lang_path}{synset.ili.id}_{formatted_lemma}_example.mp3"
        make_example_page_audio(synset, lang, example_sentence_audio_file)        
        example_sentence_video_file = f"{lang_path}{synset.ili.id}_{formatted_lemma}_example.mp4"
        make_video_from_image(f"{lang_path}{synset.ili.id}_{formatted_lemma}_example.png", example_sentence_video_file, example_sentence_audio_file)
        
        make_video_from_image(image_files[2], image_files[2].replace('.jpg', '.mp4'))
        make_video_from_image(image_files[3], image_files[3].replace('.jpg', '.mp4'))
        make_diagram_audio(synset, lemma, f"{lang_path}{synset.ili.id}_{formatted_lemma}_composite.mp3")
        make_video_from_image(f"{lang_path}{synset.ili.id}_composite.png", f"{lang_path}{synset.ili.id}_{formatted_lemma}_composite.mp4", f"{lang_path}{synset.ili.id}_{formatted_lemma}_composite.mp3", duration=10.00)
        
        all_clips = [
                VideoFileClip(title_page_video_file),
                VideoFileClip(example_sentence_video_file),
                VideoFileClip(image_files[2].replace('.jpg', '.mp4')),
                VideoFileClip(image_files[3].replace('.jpg', '.mp4')),
                VideoFileClip(f"{lang_path}{synset.ili.id}_{formatted_lemma}_composite.mp4")
            ]
        
        final_vid = concatenate_videoclips(
            all_clips,
            method="compose"
        )                
        final_vid.write_videofile(f"{lang_path}{synset.ili.id}_{formatted_lemma}.mp4", codec="libx264", fps=24)
        
#make_title_image("i23198/i23198_0.jpg", 'produce or yield flowers', ['flower', 'blossom', 'bloom'], "i23198/i23198_title.png")
#make_image('construction', 'en', 'en', 'n')
make_images_from_ili('i66777', 'nl', 'nl')
make_images_from_ili('i66777', 'en', 'en')
make_images_from_ili('i66777', 'de', 'de')
#make_image('Occident', 'en', 'en', 'n')
#make_image('huisvesten', 'nl', 'nl', 'v')
#make_image('Abendland', 'de', 'de', 'n')
#make_image('Dachshund', 'en', 'en', 'n')

#make_image('traffic', 'en', 'en', 'n')
#proc1()
#overlay_with_transparent_white("input_images/wisski_crud.png", "input_images/wisski_crud_2.png", transparency=196)
#make_white_transparent("input_images/Sauerstoff_1.png", "input_images/output_image.png")

