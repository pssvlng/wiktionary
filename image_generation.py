import os
from imaginairy.schema import ImaginePrompt
from imaginairy.api import imagine
from imaginairy.api.video_sample import generate_video

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import wn
from imageCreation.CombinedImageWrapper import main
import text2music as t2m

def merge_images(background_image, foreground_image, result_image):
    background = Image.open(background_image)
    foreground = Image.open(foreground_image)    
    if foreground.size > background.size:
        background = background.resize(foreground.size, Image.LANCZOS)
    else:
        foreground = foreground.resize(background.size, Image.LANCZOS)            
    result = Image.alpha_composite(background.convert('RGBA'), foreground.convert('RGBA'))    
    result.save(result_image)

def make_overlay_image(image_path, output_path, transparency=212):
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
    text1 = f"{', '.join(synset.lemmas()[:2])} [{get_pos(synset.pos, synset.lang)}]"          
    text_x = 20
    text_y = 10    
    definition_parts = chunk(synset.definition().split(' '), 8)    
    rectangle_coords = [0, 0, image.width, 40 + 20*len(definition_parts)]
    fill_color = (255, 255, 255, 196) 
    draw.rectangle(rectangle_coords, fill=fill_color)

    draw.text((text_x, text_y), text1, fill=text_color, font=font)        
    text_y += 10
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

def get_pos_en(pos):
    if pos == 'n':
        return 'noun'
    if pos == 'v':
        return 'verb'
    if pos in ['a', 's']:
        return 'adjective'
    if pos == 'r':
        return 'adverb'
    
def get_pos(pos, lang):
    if lang == 'en':
        return get_pos_en(pos)

def make_image(woi, lang, filterLangs, pos):
    for synset in wn.synsets(woi, lang=lang, pos=pos):
        args_dict = {}        
        args_dict['fileName'] = f"hierarchy_partwhole_{str(datetime.now().timestamp()).replace('.', '')}_en_2_5_1"
        args_dict['level'] = '2'
        args_dict['filterLangs'] = filterLangs
        args_dict['maxLeafNodes'] = '5'
        args_dict['ili'] = synset.ili.id
        args_dict['synonymCount'] = '2'
        args_dict['synsetId'] = synset.id        
        args_dict['hierarchy'] = 'True'
        args_dict['partWhole'] = 'True'
        result = main(args_dict)        
        if not os.path.exists(f"{synset.ili.id}"):    
                os.makedirs(f"{synset.ili.id}")
        #transparent_output = f"{result['filePath'].replace('/tmp/', '/tmp/transparent_')}"
        make_white_transparent(result['filePath'], f"{synset.ili.id}/{synset.ili.id}.png")
        lemmas = synset.lemmas()
        prompts = []
        image_files = []
        for i in range(4):
            lemma = lemmas[len(lemmas) - 1] if i > len(lemmas) - 1 else lemmas[i]
            prompts.append(ImaginePrompt(f"{lemma}: {synset.definition()}"))
        for index, imagine_result in enumerate(imagine(prompts)):            
            image_file = f'{synset.ili.id}/{synset.ili.id}_{index}.jpg'
            image_files.append(image_file)
            imagine_result.save(image_file)    

        tiled_output_file = f'{synset.ili.id}/{synset.ili.id}_tiled.png'    
        make_tiled_image(image_files, tiled_output_file)
        tiled_transparent_output_file = f'{synset.ili.id}/{synset.ili.id}_tiled_transparent.png'    
        make_overlay_image(tiled_output_file, tiled_transparent_output_file)
        merge_images(tiled_transparent_output_file, f"{synset.ili.id}/{synset.ili.id}.png", f"{synset.ili.id}/{synset.ili.id}_composite.png")
        make_title_image(image_files[0], synset.definition(), lemmas, pos, f"{synset.ili.id}/{synset.ili.id}_title.png")

        #generate_video(f"{synset.ili.id}/{synset.ili.id}_title.png", output_folder=f'{synset.ili.id}', num_frames=6)

#make_title_image("i23198/i23198_0.jpg", 'produce or yield flowers', ['flower', 'blossom', 'bloom'], "i23198/i23198_title.png")
make_image('flower', 'en', 'en', 'v')
#make_image('bank', 'en', 'en', 'n')
#make_image('traffic', 'en', 'en', 'n')
#proc1()
#overlay_with_transparent_white("input_images/wisski_crud.png", "input_images/wisski_crud_2.png", transparency=196)
#make_white_transparent("input_images/Sauerstoff_1.png", "input_images/output_image.png")

