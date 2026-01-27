from telegram import Update, constants, InlineKeyboardMarkup, InlineKeyboardButton
import utils
from utils import t
def menu_opciones(lang):
    teclado = [
        [
            InlineKeyboardButton(t("menu_options_edit_name", lang=lang), callback_data="edit_name"),
            InlineKeyboardButton(t("menu_options_add_tag", lang=lang), callback_data="add_tag"),
        ],
        [
            InlineKeyboardButton(t("menu_options_edit_date", lang=lang), callback_data="edit_date"),
            InlineKeyboardButton(t("menu_options_edit_document_type", lang=lang), callback_data="edit_type")
        ],
        [
            InlineKeyboardButton(t("menu_options_edit_correspondent", lang=lang), callback_data="edit_emisor"),
        ],
        [
            InlineKeyboardButton(t("menu_options_cancel", lang=lang), callback_data="cancel")
        ],
        [
            InlineKeyboardButton(t("menu_options_send", lang=lang), callback_data="enviar"),
        ]
    ]
    return InlineKeyboardMarkup(teclado)

def menu_emisor(lang):
    teclado = [

        [
            InlineKeyboardButton(t("menu_correspondent_cancel", lang=lang), callback_data="cancel"),
            InlineKeyboardButton(t("menu_correspondent_add", lang=lang), callback_data="añadir")
        ]
    ]
    return InlineKeyboardMarkup(teclado)

def menu_final(lang):
    teclado = [

        [
            InlineKeyboardButton(t("last_menu_no", lang=lang), callback_data="no"),
            InlineKeyboardButton(t("last_menu_yes", lang=lang), callback_data="si")
        ]
    ]
    return InlineKeyboardMarkup(teclado)

def menu_tags(lang):
    tag_dictionary = utils.get_tags()
    teclado = []
    fila = []
    for position, (tag, id) in enumerate(tag_dictionary.items()):
        if position % 2 != 1:
            fila.append(InlineKeyboardButton(tag, callback_data=id))
        else:
            fila.append(InlineKeyboardButton(tag, callback_data=id))
            teclado.append(fila)
            fila=[]
    if len(fila)>0:
        teclado.append(fila)

    teclado.append([InlineKeyboardButton(t("menu_tags_add_tag", lang=lang), callback_data="add_tag")])
    
    return InlineKeyboardMarkup(teclado)

def menu_tipos(lang):
    type_dictionary = utils.get_documentType()
    teclado = []
    fila = []
    for position, (type, id) in enumerate(type_dictionary.items()):
        if position % 2 != 1:
            fila.append(InlineKeyboardButton(type, callback_data=id))
        else:
            fila.append(InlineKeyboardButton(type, callback_data=id))
            teclado.append(fila)
            fila=[]
    if len(fila)>0:
        teclado.append(fila)

    teclado.append([InlineKeyboardButton(t("menu_doc_type_add_type", lang=lang), callback_data="add_type")])
    
    return InlineKeyboardMarkup(teclado)