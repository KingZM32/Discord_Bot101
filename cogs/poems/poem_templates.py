import discord
import os
import random
import config


# TODO: Tornar o código mais clean
# TODO: Quebra de linha na passagem de title para value

def find_poem(writer):
    here = os.path.dirname(os.path.abspath(__file__))
    path_to_writer = os.path.join(here, 'poems_repo', writer)
    num = len([name for name in os.listdir(path_to_writer) if os.path.isfile(os.path.join(path_to_writer, name))])
    filename = os.path.join(path_to_writer, str(random.randint(1,num))+'.txt')

    with open(filename, "r") as text_file:
        title = text_file.readline() 
        verse = text_file.read()
        return open_poem_template(writer, title, verse)

def poem_selection_template():
    emb = discord.Embed(title="Poesia", colour=config.POEM_SELEC)
    for x in config.SUPPORTED_WRITERS:
        writer, colour = x 
        emb.add_field(name=writer, value=f"Reage com {colour} a esta mensagem para um poema de {writer}.")
    
    return emb

def open_poem_template(author, poem_title, poem_text):
    l = [x.capitalize() for x in author.split(" ")]
    author = l[0] + " " + l[-1]
    
    emb = discord.Embed(title="Poema", colour=config.EMBED_COLOUR)
    emb.set_author(name=author, url=config.OBRA_EDITA, icon_url=config.PESSOA_ICON)
    emb.add_field(name=poem_title, value=poem_text)
    emb.set_footer(text=author)

    return emb