from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler, CallbackQueryHandler, TypeHandler
import utils
from utils import t
from io import BytesIO
from telegramMenus import menu_emisor, menu_final, menu_opciones, menu_tags, menu_tipos
import yaml

async def recibir_documento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizado(update):
        return
    doc_type=""
    if update.message.photo:
        context.user_data["document"] = update.message.photo[-1]
        context.user_data["doc_type"]="image/jpg"
    if update.message.document:
        if update.message.document.mime_type == "application/pdf":
            await update.message.reply_text("📄 Has enviado un archivo PDF.")
            context.user_data["document"] = update.message.document
            context.user_data["doc_type"]="application/pdf"
        else:
            await update.message.reply_text( f"📁 Has enviado un documento ({update.message.document.mime_type}).")
            return
    context.user_data["name"] = update.message.caption if update.message.caption else context.user_data["document"].file_id
    context.user_data["tags"] = []
    context.user_data["correspondent"] = None
    context.user_data["type"] = None
    context.user_data["fecha"] = None



    # Información del documento
    file_id = context.user_data["document"].file_id
    file_size = context.user_data["document"].file_size

    await update.message.reply_text(t("file_recieved", lang=lang, name=context.user_data["name"],file_size=file_size))

    context.user_data["estado"]="menu"

    await update.message.reply_text(t("menu_title", lang=lang),
        reply_markup=menu_opciones(lang)
    )

async def manejar_opcion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizado(update):
        return
    query = update.callback_query
    await query.answer()

    opcion = query.data
    estado = context.user_data.get("estado")

    ######################################################
    ######              Final Check                 ######
    ######################################################
    if estado == "last_check":
        if opcion=="si":
            archivo = await context.bot.get_file(context.user_data["document"].file_id)
            buffer = BytesIO()
            await archivo.download_to_memory(buffer)

            buffer.seek(0)

            utils.upload_document(buffer,
                                  context.user_data["name"],
                                  context.user_data["fecha"],
                                  context.user_data["correspondent"],
                                  context.user_data["type"],
                                  context.user_data["tags"],
                                  context.user_data["doc_type"])
            await query.message.reply_text(t("successful_upload", lang=lang))
            context.user_data.clear()
        
        else:
            await query.message.reply_text(t("operation_cancelled", lang=lang))
            context.user_data.clear()

    ######################################################
    ######                 Tags                     ######
    ######################################################
    if estado == "esperando_tag":

        if opcion == "add_tag":
            await query.message.reply_text(t("new_name", lang=lang))
            context.user_data["estado"]="add_tag"


        else:
            context.user_data["tags"].append(opcion)
            context.user_data["estado"]="menu"
            await query.message.reply_text(t("tag_added", lang=lang))
            await query.message.reply_text(
            t("menu_title", lang=lang),
            reply_markup=menu_opciones(lang)
            )

    ######################################################
    ######              DocumentType                ######
    ######################################################
    if estado == "esperando_tipo":

        if opcion == "add_type":
            await query.message.reply_text(t("new_name", lang=lang))
            context.user_data["estado"]="add_type"


        else:
            context.user_data["type"] = int(opcion)
            context.user_data["estado"]="menu"
            await query.message.reply_text(t("doc_type_added", lang=lang))
            await query.message.reply_text(
            t("menu_title", lang=lang),
            reply_markup=menu_opciones(lang)
            )

    ######################################################
    ######              Correspondent               ######
    ######################################################
    if estado == "add_emisor":

        if opcion == "añadir":
            emisor = context.user_data["emisor_tmp"]
            utils.add_correspondent(emisor)
            dict_emisores = utils.get_correspondents()
            if emisor in dict_emisores:
                context.user_data["correspondent"]=dict_emisores[emisor]
                await query.message.reply_text(
                t("new_correspondent", lang=lang, emisor=emisor)
        )
                context.user_data["estado"]="menu"
                await query.message.reply_text(
                t("menu_title", lang=lang),
                reply_markup=menu_opciones(lang)
                )


            else:
                await update.message.reply_text(
                t("new_correspondent_error", lang=lang, emisor=emisor)
                )
                context.user_data["estado"]="menu"
                await update.message.reply_text(
                t("menu_title", lang=lang),
                reply_markup=menu_opciones(lang)
                )

    ######################################################
    ######              Start Menu                  ######
    ######################################################
    if estado == "menu":
        if opcion == "edit_name":
            context.user_data["estado"] = "esperando_nombre"
            await query.message.reply_text(t("new_name", lang=lang))

        if opcion == "add_tag":
            context.user_data["estado"] = "esperando_tag"
            context.user_data["last_message"] = await query.message.reply_text(t("choose_tag", lang=lang),
                                        reply_markup=menu_tags(lang))
        
        if opcion == "edit_date":
            context.user_data["estado"] = "esperando_fecha"
            await query.message.reply_text(t("write_date", lang=lang))


        if opcion == "edit_type":
            context.user_data["estado"] = "esperando_tipo"
            context.user_data["last_message"] = await query.message.reply_text(t("choose_doc_type", lang=lang),
                                        reply_markup=menu_tipos(lang))

        if opcion == "edit_emisor":
            context.user_data["estado"] = "esperando_emisor"
            await query.message.reply_text(t("write_correspondent", lang=lang))  


        if opcion == "cancel":
            context.user_data.clear()
            await query.message.reply_text(t("operation_cancelled_menu", lang=lang))

        if opcion == "enviar":
            dict_tags=utils.get_tags()
            dict_types = utils.get_documentType()
            dict_emisores = utils.get_correspondents()


            tags  = [k for k, v in dict_tags.items() if str(v) in context.user_data["tags"]]
            doc_type  = next((k for k, v in dict_types.items() if v == context.user_data["type"]), None)
            emisor = next((k for k, v in dict_emisores.items() if v == context.user_data["correspondent"]), None)
            
            await query.message.reply_text(t("check_message_before_send", lang=lang, name=str(context.user_data["name"]),correspondent=str(emisor), tags=str(tags),doc_type=str(doc_type),date=str(context.user_data["fecha"])))
            context.user_data["estado"] = "last_check"
            await query.message.reply_text(t("last_check", lang=lang),
                                           reply_markup=menu_final(lang))


async def recibir_texto(update, context: ContextTypes.DEFAULT_TYPE):
    if not autorizado(update):
        return
    estado = context.user_data.get("estado")

    ######################################################
    ######              Change Name                 ######
    ######################################################
    if estado == "esperando_nombre":
        nuevo_nombre = update.message.text
        context.user_data["name"] = nuevo_nombre
        await update.message.reply_text(
            t("name_changed", lang=lang, nuevo_nombre=nuevo_nombre)
        )
        context.user_data["estado"]="menu"
        await update.message.reply_text(
            t("menu_title", lang=lang),
            reply_markup=menu_opciones(lang)
            )

    ######################################################
    ######                New Tag                   ######
    ######################################################
    if estado == "add_tag":
        nuevo_tag = update.message.text
        utils.add_tag(nuevo_tag)

        await update.message.reply_text(
            t("new_tag", lang=lang, nuevo_tag=nuevo_tag)
        )
        context.user_data["estado"]="menu"
        await update.message.reply_text(
            t("menu_title", lang=lang),
            reply_markup=menu_opciones(lang)
            )
        
    ######################################################
    ######              New Date                    ######
    ######################################################
    if estado == "esperando_fecha":
        nueva_fecha = update.message.text
        context.user_data["fecha"] = nueva_fecha
        await update.message.reply_text(
            t("new_date", lang=lang, nueva_fecha=nueva_fecha)
        )
        context.user_data["estado"]="menu"
        await update.message.reply_text(
            t("menu_title", lang=lang),
            reply_markup=menu_opciones(lang)
            )

    ######################################################
    ######            New Document Type             ######
    ######################################################
    if estado == "add_type":
        nuevo_type = update.message.text
        utils.add_documenType(nuevo_type)
        await update.message.reply_text(
            t("new_doc_type", lang=lang, nuevo_type=nuevo_type))
        context.user_data["estado"]="menu"
        await update.message.reply_text(
            t("menu_title", lang=lang),
            reply_markup=menu_opciones(lang)
            )

    ######################################################
    ######              Correspondent               ######
    ######################################################
    if estado == "esperando_emisor":
        emisor = update.message.text.lower()
        dict_emisores = utils.get_correspondents()
        if emisor in dict_emisores:
            context.user_data["correspondent"]=dict_emisores[emisor]
            await update.message.reply_text(
            t("correspondent_registered", lang=lang, emisor=emisor)
        )
            context.user_data["estado"]="menu"
            await update.message.reply_text(
            t("menu_title", lang=lang),
            reply_markup=menu_opciones(lang)
            )
        else:
            context.user_data["estado"]="add_emisor"
            context.user_data["emisor_tmp"]=emisor
            await update.message.reply_text(
            t("correspondent_not_found", lang=lang),
            reply_markup=menu_emisor(lang)
        )
        
        


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not autorizado(update):
        return
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')



def autorizado(update: Update) -> bool:
    print(update.effective_user.id)
    return update.effective_user.id in utils.WHITELIST_USERS



with open("config.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

bot_token = data["telegram"]["token_bot"]
lang = data["lang"]

try:        
    app = ApplicationBuilder().token(bot_token).build()
    handler_documentos = MessageHandler(
        filters.Document.ALL,
        recibir_documento
    )


    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(handler_documentos)
    app.add_handler(CallbackQueryHandler(manejar_opcion))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_texto))

    
    app.run_polling()

except Exception as e:
    print(e)
    app.shutdown()