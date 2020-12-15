#signup v5
from database import db
import logging
import re
from typing import Dict

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Global Variable 
email_validator = '^[a-z]+[.]2[0-9]{3}[@][a-z]{3,4}[.][s][m][u][.][e][d][u][.][s][g]' # For email validation

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

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

def signup(update: Update, context: CallbackContext) -> int:
    context.bot.send_message(chat_id=update.effective_chat.id, text='Full name (according to matriculation):',)
    return NAME


def name(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["name"] = update.message.text
    logger.info("User <%s> Matriculated name: %s", user.first_name, update.message.text)
    reply_keyboard = [['Male', 'Female']]
    update.message.reply_text(
        'Select gender:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return GENDER

def gender(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["gender"] = update.message.text
    logger.info("User <%s> Gender: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Matriculation number (e.g. 01234567):',
        reply_markup=ReplyKeyboardRemove(),
    )

    return MATNUM

def matnum(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    for i in update.message.text:
        if not i.isdigit() or len(update.message.text) != 8:
            update.message.reply_text(
                'Enter a valid 8-digit matriculation number (e.g. 01234567):',
                reply_markup=ReplyKeyboardRemove(),
            )
            return MATNUM
    userinfo["matnum"] = update.message.text
    logger.info("User <%s> Matriculation number: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Contact number (e.g.: 91234567):',
        reply_markup=ReplyKeyboardRemove(),
    )

    return HPNUM

def hpnum(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["hpnum"] = update.message.text
    logger.info("User <%s> Contact number: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'SMU email address (e.g. johntan.2020@sis.smu.edu.sg):',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EMAIL

def email(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['O+', 'O-'], ['AB+', 'AB-'], ['A+', 'A-'], ['B+', 'B-']]
    user = update.message.from_user
    if not re.search(email_validator, update.message.text):
        logger.info(False)
        update.message.reply_text("Please enter a vaild SMU email address (e.g. johntan.2020@sis.smu.edu.sg):")
        return EMAIL
    userinfo["email"] = update.message.text
    logger.info("User <%s> Email: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Blood Type:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return BLOODTYPE

def bloodtype(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["bloodtype"] = update.message.text
    logger.info("User <%s> Blood type: %s", user.first_name, update.message.text)
    update.message.reply_text(
        "Enter your prevailing medical conditions, or '/skip' if you have none.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return MEDICAL

def medical(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["medical"] = update.message.text
    logger.info("User <%s> Medical conditions: %s", user.first_name, update.message.text)
    update.message.reply_text(
        "Enter your dietary requirements, or '/skip' if you have none.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return DIETARY

def skip_medical(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["medical"] = "NA"
    logger.info("User <%s> has no medical conditions.", user.first_name)
    update.message.reply_text(
        "Enter your dietary requirements, or '/skip' if you have none.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return DIETARY

def dietary(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["dietary"] = update.message.text
    logger.info("User <%s> Dietary requirements: %s", user.first_name, update.message.text)
    update.message.reply_text("Please check if your information entered is correct.\n\n" + edituserinfo_message(), reply_markup=ReplyKeyboardRemove())

    return EDIT

def skip_dietary(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["dietary"] = "NA"
    logger.info("User <%s> has no dietary requirements", user.first_name)
    update.message.reply_text("Please check if your information entered is correct.\n\n" + edituserinfo_message(), reply_markup=ReplyKeyboardRemove())

    return EDIT

#==============================================================================================#
                            #  _______  ______  __________________ #
                            # (  ____ \(  __  \ \__   __/\__   __/ #
                            # | (    \/| (  \  )   ) (      ) (    #
                            # | (__    | |   ) |   | |      | |    #
                            # |  __)   | |   | |   | |      | |    #
                            # | (      | |   ) |   | |      | |    #
                            # | (____/\| (__/  )___) (___   | |    #
                            # (_______/(______/ \_______/   )_(    #
                            #                                      #
#==============================================================================================#

def edit_self_entry(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    data = db.child("Users").child(user.id).child("Personal Particulars").child("Self").get().val()
    userinfo["name"] = data["name"]
    userinfo["gender"] = data["gender"]
    userinfo["matnum"] = data["matnum"]
    userinfo["hpnum"] = data["hpnum"]
    userinfo["email"] = data["email"]
    userinfo["bloodtype"] = data["bloodtype"]
    userinfo["medical"] = data["medical"]
    userinfo["dietary"] = data["dietary"]
    logger.info("User <%s> Self data received.", user.first_name)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())

    return EDIT

def edit_name_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Full name (according to matriculation):',
    )

    return EDIT_NAME_END

def edit_name_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["name"] = update.message.text
    logger.info("User <%s> edited their matriculated name to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_gender_start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Male', 'Female']]
    update.message.reply_text(
        'Select gender:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return EDIT_GENDER_END

def edit_gender_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["gender"] = update.message.text
    logger.info("User <%s> edited their gender to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_matnum_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Matriculation number:',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_MATNUM_END

def edit_matnum_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    for i in update.message.text:
        if not i.isdigit() or len(update.message.text) != 8:
            update.message.reply_text(
                'Enter a valid 8-digit matriculation number (e.g. 01234567):',
                reply_markup=ReplyKeyboardRemove(),
            )
            return EDIT_MATNUM_END
    userinfo["matnum"] = update.message.text
    logger.info("User <%s> edited their matriculation number to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_hpnum_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Contact number (e.g.: 91234567):',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_HPNUM_END

def edit_hpnum_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["hpnum"] = update.message.text
    logger.info("User <%s> edited their contact number to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_email_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'SMU email address (e.g. johntan.2020@sis.smu.edu.sg):',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_EMAIL_END

def edit_email_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    if not re.search(email_validator, update.message.text):
        logger.info(False)
        update.message.reply_text("Please enter a vaild SMU email address (e.g. johntan.2020@sis.smu.edu.sg):")
        return EDIT_EMAIL_END
    userinfo["email"] = update.message.text
    logger.info("User <%s> edited their email to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_bloodtype_start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['O+', 'O-'], ['AB+', 'AB-'], ['A+', 'A-'], ['B+', 'B-']]
    update.message.reply_text(
        'Blood Type:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return EDIT_BLOODTYPE_END

def edit_bloodtype_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["bloodtype"] = update.message.text
    logger.info("User <%s> edited their blood type to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_medical_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Update your medical conditions. If there are none, please enter "NA".',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_MEDICAL_END

def edit_medical_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["medical"] = update.message.text
    logger.info("User <%s> edited their medical condition to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_dietary_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Update your dietary requirements. If there are none, please enter "NA".',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_DIETARY_END

def edit_dietary_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["dietary"] = update.message.text
    logger.info("User <%s> edited their dietary requirements to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edituserinfo_message() -> str:
    output = "Click the fields below to edit or /done if everything is correct.\n"
    output += f"/Name: {userinfo['name']}\n"
    output += f"/Gender: {userinfo['gender']}\n"
    output += f"/Matriculation_Number: {userinfo['matnum']}\n"
    output += f"/HP_Number: {userinfo['hpnum']}\n"
    output += f"/Email: {userinfo['email']}\n"
    output += f"/Blood_Type: {userinfo['bloodtype']}\n"
    output += f"/Medical_Conditions: {userinfo['medical']}\n"
    output += f"/Dietary_Restrictions: {userinfo['dietary']}\n"
    
    return output

def done(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    info = db.child("Users").child(user.id).child("Personal Particulars").child("NOK").get().val()

    if info: #check if existing user
        update.message.reply_text(
            "Information updated.",
            reply_markup=ReplyKeyboardRemove(),
        )
    else: #new user
        #segue into NOK for first time user
        keyboard = [[InlineKeyboardButton("Continue", callback_data="callback_noknew")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "The following section requires your Next-of-Kin (NOK) details.",
            reply_markup=reply_markup,
        )

    #odd/even calculator
    if int(userinfo["matnum"]) % 2 == 0:
        oddeven = "Even"
    else:
        oddeven = "Odd"
    #database push!
    data_db_new = {
        "name" : userinfo["name"],
        "gender" : userinfo["gender"],
        "matnum" : userinfo["matnum"],
        "hpnum" : userinfo["hpnum"],
        "email" : userinfo["email"],
        "bloodtype" : userinfo["bloodtype"],
        "medical" : userinfo["medical"],
        "dietary" : userinfo["dietary"],
        "telehandle" : user.username,
        "oddeven": oddeven,
    }

    db.child("Users").child(user.id).child("Personal Particulars").child("Self").set(data_db_new)
    logger.info("User <%s> confirmed their self details. Uploaded to database.", user.first_name)
    #database done pushing
    #how to integrate back into main menu

    return ConversationHandler.END


#==============================================================================================#

# Fallback commands (return to all other menus), remember to integrate with main functions

def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User <%s> canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bot successfully cancelled.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

