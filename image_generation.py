import os
import shutil
from gtts import gTTS
from imaginairy.schema import ImaginePrompt
from imaginairy.api import imagine

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import wn
from imageCreation.CombinedImageWrapper import main

from video_generation_consts import *
from moviepy.editor import AudioClip, VideoFileClip, VideoClip, ImageClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx import resize

def merge_images(background_image, foreground_image, result_image):
    background = Image.open(background_image)
    foreground = Image.open(foreground_image)    
    if foreground.size > background.size:
        background = background.resize(foreground.size, Image.LANCZOS)
    else:
        foreground = foreground.resize(background.size, Image.LANCZOS)            
    result = Image.alpha_composite(background.convert('RGBA'), foreground.convert('RGBA'))    
    result.save(result_image)

def make_overlay_image(image_path, output_path, transparency=204):
    original_image = Image.open(image_path)    
    overlay = Image.new('RGBA', original_image.size, (255, 255, 255, transparency))
    result = Image.alpha_composite(original_image.convert('RGBA'), overlay)
    result.save(output_path)

def make_title_image(image_path, synset, output_path):
    def chunk(lst, chunk_size):    
        return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]
    image = Image.open(image_path)        
    image_adjusted = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image_adjusted)    
    font = ImageFont.truetype("arial.ttf", 24)        
    font_sub = ImageFont.truetype("arial.ttf", 16)        
    text_color = (0, 0, 0)  
    lemmas = synset.lemmas()
    text1 = f"{lemmas[0]} [{get_pos(synset.pos, synset.lexicon().language)}]"              
    text_x = 20
    text_y = 10    
    definition_parts = chunk(synset.definition().split(' '), 8)    
    synonym_parts = []
    if len(lemmas) > 1:
        synonym_parts = chunk(f"Synonyms: {', '.join(lemmas[1:])}".split(' '), 8)        
    rectangle_coords = [0, 0, image.width, 40 + 20*len(definition_parts) + 20*len(synonym_parts)]
    fill_color = (255, 255, 255, 196) 
    draw.rectangle(rectangle_coords, fill=fill_color)

    draw.text((text_x, text_y), text1, fill=text_color, font=font)        
    text_y += 10    
    for part in synonym_parts:
        text_y += 20
        draw.text((text_x, text_y), ' '.join(part), fill=text_color, font=font_sub)            
    for part in definition_parts:
        text_y += 20
        draw.text((text_x, text_y), ' '.join(part), fill=text_color, font=font_sub)        

    result = Image.alpha_composite(image.convert("RGBA"), image_adjusted)
    result.save(output_path)

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

def make_title_page_audio(synset, lang, output_file):
    lemmas = synset.lemmas()
    definition = synset.definition()
    title_page_template = get_title_page_text(lang)
    synonym_text_template = get_synonym_text(lang)
    audio_text = title_page_template.replace('{LEMMAS}', lemmas[0]).replace('{POS}', get_pos(synset.pos, lang)).replace('{LANG}', get_full_lang(lang)).replace('{DEFINITION}', definition)    
    if len(lemmas) > 1:
        audio_text += synonym_text_template.replace('{LEMMA}', lemmas[0]).replace('{SYNONYMS}', ', '.join(lemmas[1:]))
    tts = gTTS(audio_text, lang=synset.lexicon().language)    
    tts.save(output_file)

def make_example_page_audio(synset, lang, output_file):
    examples = synset.examples()
    if len(examples) > 0:            
        example_text_template = get_example_text(lang)
        example_text = example_text_template.replace('{SENTENCE}', examples[0])        
        tts = gTTS(example_text, lang=synset.lexicon().language)    
        tts.save(output_file)

def make_example_sentence_image(synset, input_file, output_file):
    def chunk(lst, chunk_size):    
        return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]
    image = Image.open(input_file)        
    image_adjusted = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image_adjusted)    
    font = ImageFont.truetype("arial.ttf", 24)        
    font_sub = ImageFont.truetype("arial.ttf", 16)        
    text_color = (0, 0, 0)  
    examples = synset.examples()
    if len(examples) == 0:
       shutil.copyfile(input_file, output_file) 
       return
    
    text1 = f"{examples[0]}"              
    text_x = 20
    text_y = 10    
    example_parts = chunk(examples[0].split(' '), 8)        
    rectangle_coords = [0, 0, image.width, 40 + 20*len(example_parts)]
    fill_color = (255, 255, 255, 196) 
    draw.rectangle(rectangle_coords, fill=fill_color)
    draw.text((text_x, text_y), text1, fill=text_color, font=font)                
    
    result = Image.alpha_composite(image.convert("RGBA"), image_adjusted)
    result.save(output_file)

# def make_zoom_video_from_image(image_input_file, video_output_file, audio_input_file=None, zoom_duration=5.00):        
#     def zoom_in_on_image(t):
#         image = ImageClip(image_input_file)    
#         zoom_factor = 1 + 0.1 * t 
#         width, height = image.size    
#         image = image.resize((int(width)/2, int(height)/2))        
#         return image            

#     video_clip = VideoClip(zoom_in_on_image, duration=zoom_duration)    
#     audio = AudioClip(audio_input_file) if audio_input_file else None
#     if audio_input_file:
#         video_clip = video_clip.set_audio(audio_input_file)
#         video_clip = video_clip.set_duration(audio.duration)
#     else:
#         video_clip = video_clip.set_duration(zoom_duration)            
#     video_clip = video_clip.set_position(('center', 'center'))    
#     video_clip.write_videofile(video_output_file, codec='libx264', fps=24)    

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
    
def make_image(woi, lang, filterLangs, pos):
    def check_files_exist(file_names):
        for file_name in file_names:
            if not os.path.exists(file_name):    
                return False        
        return True
    
    for synset in wn.synsets(woi, lang=lang, pos=pos):
        args_dict = {}        
        args_dict['fileName'] = f"hierarchy_partwhole_{str(datetime.now().timestamp()).replace('.', '')}_{lang}_2_5_1"
        args_dict['level'] = '2'
        args_dict['filterLangs'] = filterLangs
        args_dict['maxLeafNodes'] = '5'
        args_dict['ili'] = synset.ili.id
        args_dict['synonymCount'] = '2'
        args_dict['synsetId'] = synset.id        
        args_dict['hierarchy'] = 'True'
        args_dict['partWhole'] = 'True'
        result = main(args_dict)        
        base_path = f"synset_media/{synset.ili.id}/"        
        lang_path = f"{base_path}{lang}/"
        if not os.path.exists(f"{base_path}"):    
                os.makedirs(f"{base_path}")
        if not os.path.exists(f"{lang_path}"):                    
                os.makedirs(f"{lang_path}")

        lemmas = synset.lemmas()
        prompts = []
        image_files = []
        make_white_transparent(result['filePath'], f"{lang_path}{synset.ili.id}.png")
        
        tiled_output_file = f'{base_path}{synset.ili.id}_tiled.png'    
        tiled_transparent_output_file = f'{base_path}{synset.ili.id}_tiled_transparent.png'    
        title_page_audio_file = f"{lang_path}{synset.ili.id}_title_page.mp3"
        title_page_video_file = f"{lang_path}{synset.ili.id}_title_page.mp4"
        example_sentence_audio_file = f"{lang_path}{synset.ili.id}_example.mp3"
        example_sentence_video_file = f"{lang_path}{synset.ili.id}_example.mp4"

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

        merge_images(tiled_transparent_output_file, f"{lang_path}{synset.ili.id}.png", f"{lang_path}{synset.ili.id}_composite.png")
        make_title_image(image_files[0], synset, f"{lang_path}{synset.ili.id}_title.png")
        make_title_page_audio(synset, lang, title_page_audio_file)
        make_title_page_video(f"{lang_path}{synset.ili.id}_title.png", title_page_audio_file, title_page_video_file)

        make_example_sentence_image(synset, image_files[1], f"{lang_path}{synset.ili.id}_example.png")        
        make_example_page_audio(synset, lang, example_sentence_audio_file)
        make_video_from_image(f"{lang_path}{synset.ili.id}_example.png", example_sentence_video_file, example_sentence_audio_file)
        
        make_video_from_image(image_files[2], image_files[2].replace('.jpg', '.mp4'))
        make_video_from_image(image_files[3], image_files[3].replace('.jpg', '.mp4'))
        make_video_from_image(f"{lang_path}{synset.ili.id}_composite.png", f"{lang_path}{synset.ili.id}_composite.mp4", duration=10.00)
        
        all_clips = [
                VideoFileClip(title_page_video_file),
                VideoFileClip(example_sentence_video_file),
                VideoFileClip(image_files[2].replace('.jpg', '.mp4')),
                VideoFileClip(image_files[3].replace('.jpg', '.mp4')),
                VideoFileClip(f"{lang_path}{synset.ili.id}_composite.mp4")
            ]
                    
        final_vid = concatenate_videoclips(
            all_clips, method="compose"
        )                
        final_vid.write_videofile(f"{lang_path}{synset.ili.id}.mp4", codec="libx264", fps=24)
        break

#make_title_image("i23198/i23198_0.jpg", 'produce or yield flowers', ['flower', 'blossom', 'bloom'], "i23198/i23198_title.png")
#make_image('flower', 'en', 'en', 'v')
#make_image('house', 'en', 'en', 'v')
make_image('huisvesten', 'nl', 'nl', 'v')
#make_image('Familienbande', 'de', 'de', 'n')
#make_image('Dachshund', 'en', 'en', 'n')

#make_image('traffic', 'en', 'en', 'n')
#proc1()
#overlay_with_transparent_white("input_images/wisski_crud.png", "input_images/wisski_crud_2.png", transparency=196)
#make_white_transparent("input_images/Sauerstoff_1.png", "input_images/output_image.png")

