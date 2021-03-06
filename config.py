import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CMD_PREFIX = "!"
TIMEZONE = "Europe/Lisbon"

EMBED_COLOUR = 0xf1c40f
POEM_SELEC = 0x206694
COLOUR_CIRCLES = ["π΄", "π ", "π‘","π’"]
SUPPORTED_WRITERS = [("Fernando Pessoa", "π΄"), ("Γlvaro de Campos","π "), ("Alberto Caeiro","π‘"), ("Ricardo Reis","π’")]


OBRA_EDITA = "http://arquivopessoa.net/"
HETERONIMOS_ICON = "https://feed.jeronimomartins.com/wp-content/uploads/2020/06/jeronimo-martins-sketch-fernando-pessoa.jpg"
PESSOA_ICON = "https://plataformacidadaniamonarquica.files.wordpress.com/2013/07/pessoa.jpg"
