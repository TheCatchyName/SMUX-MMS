#FUNCTIONAL MODULES
from start import start
from pparticulars.signup import (
    signup, name, gender, matnum, hpnum, email, bloodtype, medical, dietary, cancel,
    edit_name_start, edit_name_end, edit_gender_start, edit_gender_end, edit_matnum_start, edit_matnum_end,
    edit_hpnum_start, edit_hpnum_end, edit_email_start, edit_email_end, edit_bloodtype_start, edit_bloodtype_end,
    edit_medical_start, edit_medical_end, edit_dietary_start, edit_dietary_end, edit_self_entry,
    skip_dietary, skip_medical, done,
)
from pparticulars.nok import (
    nok, nok_done, nok_hpnum, nok_name, nok_relationship, edit_nok_entry,
    edit_nok_name_start, edit_nok_name_end, edit_nok_hpnum_start, edit_nok_hpnum_end, 
    edit_nok_relationship_start, edit_nok_relationship_end, editnokinfo_message
)
from menu.menu import (
    menu, credits, pdpa, pdpa_disposable, delete_recent, menu_return, my_profile, faq
)
from schedules import schedules, unregister

#KEY MODULES
from database import db
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
)
import logging
# from dotenv import load_dotenv
import os

#Logging Module
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#Token
updater = Updater(token=os.getenv('SMUX_BOT_TOKEN'), use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#Signup conversation handler

#==============================================================================================#

SIGNUP, NAME, GENDER, MATNUM, HPNUM, EMAIL, BLOODTYPE, MEDICAL, DIETARY, EDIT, EDIT_NAME_END, EDIT_GENDER_END, EDIT_MATNUM_END, EDIT_HPNUM_END, EDIT_EMAIL_END, EDIT_BLOODTYPE_END, EDIT_MEDICAL_END, EDIT_DIETARY_END = range(18)

userinfo = {
    "name" : "",
    "gender" : "",
    "matnum" : "",
    "hpnum" : "",
    "email" : "",
    "bloodtype" : "",
    "medical" : "",
    "dietary" : "",
}

signup_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(signup, pattern="callback_signup"),
        CommandHandler('edit_self', edit_self_entry)],
    states={
        SIGNUP:  [CommandHandler('signup', signup)],
        NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
        GENDER: [MessageHandler(Filters.regex('^(Male|Female)$'), gender)],
        MATNUM: [MessageHandler(Filters.text & ~Filters.command, matnum)],
        HPNUM: [MessageHandler(Filters.text & ~Filters.command, hpnum)],
        EMAIL: [MessageHandler(Filters.text & ~Filters.command, email)],
        BLOODTYPE: [MessageHandler(Filters.regex('^(O\+|O\-|AB\+|AB\-|A\+|A\-|B\+|B\-)$'), bloodtype)],
        MEDICAL: [
            MessageHandler(Filters.text & ~Filters.command, medical),
            CommandHandler('skip', skip_medical),
        ],
        DIETARY: [
            MessageHandler(Filters.text & ~Filters.command, dietary),
            CommandHandler('skip', skip_dietary),
        ],
        EDIT: [
            CommandHandler('done', done),
            CommandHandler('Name', edit_name_start),
            CommandHandler('Gender', edit_gender_start),
            CommandHandler('Matriculation_Number', edit_matnum_start),
            CommandHandler('HP_Number', edit_hpnum_start),
            CommandHandler('Email', edit_email_start),
            CommandHandler('Blood_Type', edit_bloodtype_start),
            CommandHandler('Medical_Conditions', edit_medical_start),
            CommandHandler('Dietary_Restrictions', edit_dietary_start),
        ],
        EDIT_NAME_END: [MessageHandler(Filters.text & ~Filters.command, edit_name_end)],
        EDIT_GENDER_END: [MessageHandler(Filters.regex('^(Male|Female)$'), edit_gender_end)],
        EDIT_MATNUM_END: [MessageHandler(Filters.text & ~Filters.command, edit_matnum_end)],
        EDIT_HPNUM_END: [MessageHandler(Filters.text & ~Filters.command, edit_hpnum_end)],
        EDIT_EMAIL_END: [MessageHandler(Filters.text & ~Filters.command, edit_email_end)],
        EDIT_BLOODTYPE_END: [MessageHandler(Filters.regex('^(O\+|O\-|AB\+|AB\-|A\+|A\-|B\+|B\-)$'), edit_bloodtype_end)],
        EDIT_MEDICAL_END: [MessageHandler(Filters.text & ~Filters.command, edit_medical_end)],
        EDIT_DIETARY_END: [MessageHandler(Filters.text & ~Filters.command, edit_dietary_end)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    )

dispatcher.add_handler(signup_conv)

#==============================================================================================#

NAME, HPNUM, RELATIONSHIP, EDIT, EDIT_NAME_END, EDIT_HPNUM_END, EDIT_RELATIONSHIP_END = range(7)

nokinfo = {
    "name" : "",
    "hpnum" : "",
    "relationship" : "",
}

nok_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(nok, pattern="callback_noknew"),
        CommandHandler('edit_nok', edit_nok_entry),
        # CommandHandler('nok', nok), #enable to test
    ],
    states={
        NAME: [MessageHandler(Filters.text & ~Filters.command, nok_name)],
        HPNUM: [MessageHandler(Filters.text & ~Filters.command, nok_hpnum)],
        RELATIONSHIP: [MessageHandler(Filters.text & ~Filters.command, nok_relationship)],
        EDIT: [
            CommandHandler('done', nok_done),
            CommandHandler('Name', edit_nok_name_start),
            CommandHandler('HP_Number', edit_nok_hpnum_start),
            CommandHandler('Relationship', edit_nok_relationship_start),
        ],
        EDIT_NAME_END: [MessageHandler(Filters.text & ~Filters.command, edit_nok_name_end)],
        EDIT_HPNUM_END: [MessageHandler(Filters.text & ~Filters.command, edit_nok_hpnum_end)],
        EDIT_RELATIONSHIP_END: [MessageHandler(Filters.text & ~Filters.command, edit_nok_relationship_end)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

dispatcher.add_handler(nok_conv)

#==============================================================================================#

#Menu CallBacks
updater.dispatcher.add_handler(CommandHandler('menu', menu))
updater.dispatcher.add_handler(CallbackQueryHandler(credits, pattern='callback_credits'))
updater.dispatcher.add_handler(CallbackQueryHandler(pdpa, pattern='callback_pdpa'))
updater.dispatcher.add_handler(CallbackQueryHandler(pdpa_disposable, pattern='callback_disposable'))
updater.dispatcher.add_handler(CallbackQueryHandler(menu_return, pattern='callback_menu_return'))
updater.dispatcher.add_handler(CallbackQueryHandler(my_profile, pattern='callback_my_profile'))
updater.dispatcher.add_handler(CallbackQueryHandler(faq, pattern='callback_faq'))
updater.dispatcher.add_handler(CallbackQueryHandler(delete_recent, pattern='callback_delete'))

#Schedule Callbacks
updater.dispatcher.add_handler(CommandHandler('schedules', schedules))
updater.dispatcher.add_handler(CallbackQueryHandler(unregister, pattern='callback_unregister'))

#Polling
updater.start_polling()


#Activites conversation handler
#==============================================================================================#

