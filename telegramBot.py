from telegram import Update, constants, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler, CallbackQueryHandler
from telegram.helpers import escape_markdown
import utils
from io import BytesIO
from telegramMenus import menu_emisor, menu_final, menu_opciones, menu_tags, menu_tipos
import yaml

async def recibir_documento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["document"] = update.message.photo[-1]
    context.user_data["name"] = update.message.caption if update.message.caption else context.user_data["document"].file_id
    context.user_data["tags"] = []
    context.user_data["correspondent"] = None
    context.user_data["type"] = None
    context.user_data["fecha"] = None


    # Información del documento
    file_id = context.user_data["document"].file_id
    file_size = context.user_data["document"].file_size

    await update.message.reply_text(
        f"📄 Documento recibido:\n"
        f"Nombre: {context.user_data["name"]}\n"
        f"Tamaño: {file_size} bytes\n"
        f"mensaje: {context.user_data["name"]}\n"
    )

    context.user_data["estado"]="menu"

    await update.message.reply_text(
        "📸 Imagen recibida.\n¿Qué quieres hacer?",
        reply_markup=menu_opciones()
    )

async def manejar_opcion(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
                                  context.user_data["tags"])
            await query.message.reply_text("Subida realizada con exito")
            context.user_data.clear()
        
        else:
            await query.message.reply_text("Cancelando operación, por favor, intentalo de nuevo")

    ######################################################
    ######                 Tags                     ######
    ######################################################
    if estado == "esperando_tag":

        if opcion == "add_tag":
            await query.message.reply_text("✏️ Escribe el nuevo nombre:")
            context.user_data["estado"]="add_tag"


        else:
            context.user_data["tags"].append(opcion)
            context.user_data["estado"]="menu"
            await query.message.reply_text("Tag añadido")
            await query.message.reply_text(
            "📸 Imagen recibida.\n¿Qué quieres hacer?",
            reply_markup=menu_opciones()
            )

    ######################################################
    ######              DocumentType                ######
    ######################################################
    if estado == "esperando_tipo":

        if opcion == "add_type":
            await query.message.reply_text("✏️ Escribe el nuevo nombre:")
            context.user_data["estado"]="add_type"


        else:
            context.user_data["type"] = int(opcion)
            context.user_data["estado"]="menu"
            await query.message.reply_text("Tipo de documento añadido")
            await query.message.reply_text(
            "📸 Imagen recibida.\n¿Qué quieres hacer?",
            reply_markup=menu_opciones()
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
                f"✅ nuevo emisor registrado y añadido: {emisor}"
        )
                context.user_data["estado"]="menu"
                await query.message.reply_text("Emisor añadido")
                await query.message.reply_text(
                "📸 Imagen recibida.\n¿Qué quieres hacer?",
                reply_markup=menu_opciones()
                )


            else:
                await update.message.reply_text(
                f"❌ Ha ocurrido un error al añadir el emisor: {emisor}"
                )
                context.user_data["estado"]="menu"
                await update.message.reply_text(
                "📸 Imagen recibida.\n¿Qué quieres hacer?",
                reply_markup=menu_opciones()
                )

    ######################################################
    ######              Start Menu                  ######
    ######################################################
    if estado == "menu":
        if opcion == "edit_name":
            context.user_data["estado"] = "esperando_nombre"
            await query.message.reply_text("✏️ Escribe el nuevo nombre:")

        if opcion == "add_tag":
            context.user_data["estado"] = "esperando_tag"
            context.user_data["last_message"] = await query.message.reply_text("🏷️ Elige el tag correspondiente:",
                                        reply_markup=menu_tags())
        
        if opcion == "edit_date":
            context.user_data["estado"] = "esperando_fecha"
            await query.message.reply_text("✏️ Escribe la nueva fecha (YYYY-MM-DD):")


        if opcion == "edit_type":
            context.user_data["estado"] = "esperando_tipo"
            context.user_data["last_message"] = await query.message.reply_text("📄 Elige el tipo correspondiente:",
                                        reply_markup=menu_tipos())

        if opcion == "edit_emisor":
            context.user_data["estado"] = "esperando_emisor"
            await query.message.reply_text("✏️ Escribe el emisor (sin espacios y en minuscula):")  


        if opcion == "cancel":
            context.user_data.clear()
            await query.message.reply_text("❌ Operación cancelada")

        if opcion == "enviar":
            dict_tags=utils.get_tags()
            dict_types = utils.get_documentType()
            dict_emisores = utils.get_correspondents()


            tags  = [k for k, v in dict_tags.items() if str(v) in context.user_data["tags"]]
            doc_type  = next((k for k, v in dict_types.items() if v == context.user_data["type"]), None)
            emisor = next((k for k, v in dict_emisores.items() if v == context.user_data["correspondent"]), None)
            
            await query.message.reply_text("Nombre: " + str(context.user_data["name"]) + "\n" +
                                           "emisor: " + str(emisor) + "\n" +
                                           "tags: " + str(tags) + "\n" +
                                           "tipo: " + str(doc_type) + "\n" +
                                           "fecha: " + str(context.user_data["fecha"]) + "\n")
            context.user_data["estado"] = "last_check"
            await query.message.reply_text("Es la info correcta?",
                                           reply_markup=menu_final())


async def recibir_texto(update, context: ContextTypes.DEFAULT_TYPE):
    estado = context.user_data.get("estado")

    ######################################################
    ######              Change Name                 ######
    ######################################################
    if estado == "esperando_nombre":
        nuevo_nombre = update.message.text
        context.user_data["name"] = nuevo_nombre
        await update.message.reply_text(
            f"✅ Nombre cambiado a: {nuevo_nombre}"
        )
        context.user_data["estado"]="menu"
        await update.message.reply_text(
            "📸 Imagen recibida.\n¿Qué quieres hacer?",
            reply_markup=menu_opciones()
            )

    ######################################################
    ######                New Tag                   ######
    ######################################################
    if estado == "add_tag":
        nuevo_tag = update.message.text
        utils.add_tag(nuevo_tag)

        await update.message.reply_text(
            f"✅ nuevo tag registrado: {nuevo_tag}. Por favor, no olvides añadirlo!"
        )
        context.user_data["estado"]="menu"
        await update.message.reply_text(
            "📸 Imagen recibida.\n¿Qué quieres hacer?",
            reply_markup=menu_opciones()
            )
        
    ######################################################
    ######              New Date                    ######
    ######################################################
    if estado == "esperando_fecha":
        nueva_fecha = update.message.text
        context.user_data["fecha"] = nueva_fecha
        await update.message.reply_text(
            f"✅ Fecha cambiada a: {nueva_fecha}."
        )
        context.user_data["estado"]="menu"
        await update.message.reply_text(
            "📸 Imagen recibida.\n¿Qué quieres hacer?",
            reply_markup=menu_opciones()
            )

    ######################################################
    ######            New Document Type             ######
    ######################################################
    if estado == "add_type":
        nuevo_type = update.message.text
        utils.add_documenType(nuevo_type)
        await update.message.reply_text(
            f"✅ nuevo tipo de documento registrado: {nuevo_type}. Por favor, no olvides añadirlo!"
        )
        context.user_data["estado"]="menu"
        await update.message.reply_text(
            "📸 Imagen recibida.\n¿Qué quieres hacer?",
            reply_markup=menu_opciones()
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
            f"✅ emisor registrado: {emisor}."
        )
            context.user_data["estado"]="menu"
            await update.message.reply_text(
            "📸 Imagen recibida.\n¿Qué quieres hacer?",
            reply_markup=menu_opciones()
            )
        else:
            context.user_data["estado"]="add_emisor"
            context.user_data["emisor_tmp"]=emisor
            await update.message.reply_text(
            f"❓​ Emisor no encontrado, quieres añadirlo?",
            reply_markup=menu_emisor()
        )
        
        


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')



with open("config.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

bot_token = data["telegram"]["token_bot"]
try:        
    app = ApplicationBuilder().token(bot_token).build()
    handler_documentos = MessageHandler(
        filters.PHOTO,
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