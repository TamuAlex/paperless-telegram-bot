from telegram import Update, constants, InlineKeyboardMarkup, InlineKeyboardButton

def menu_opciones():
    teclado = [
        [
            InlineKeyboardButton("✏️ Editar nombre", callback_data="edit_name"),
            InlineKeyboardButton("🏷️ Añadir tag", callback_data="add_tag"),
        ],
        [
            InlineKeyboardButton("🗓️​ Editar fecha", callback_data="edit_date"),
            InlineKeyboardButton("📄​ Editar tipo documento", callback_data="edit_type")
        ],
        [
            InlineKeyboardButton("📤​ Editar emisor", callback_data="edit_emisor"),
        ],
        [
            InlineKeyboardButton("❌ Cancelar", callback_data="cancel")
        ],
        [
            InlineKeyboardButton("✅​ Enviar", callback_data="enviar"),
        ]
    ]
    return InlineKeyboardMarkup(teclado)

def menu_emisor():
    teclado = [

        [
            InlineKeyboardButton("❌ Cancelar", callback_data="cancel"),
            InlineKeyboardButton("✅​ Añadir", callback_data="añadir")
        ]
    ]
    return InlineKeyboardMarkup(teclado)

def menu_final():
    teclado = [

        [
            InlineKeyboardButton("❌ No", callback_data="no"),
            InlineKeyboardButton("✅​ Si", callback_data="si")
        ]
    ]
    return InlineKeyboardMarkup(teclado)

def menu_tags():
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

    teclado.append([InlineKeyboardButton("➕​ Añadir Tag", callback_data="add_tag")])
    
    return InlineKeyboardMarkup(teclado)

def menu_tipos():
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

    teclado.append([InlineKeyboardButton("➕​ Añadir tipo", callback_data="add_type")])
    
    return InlineKeyboardMarkup(teclado)