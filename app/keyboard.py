from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


# Ichki klavituralar
main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Katalog').add('Savat').add("Kontakt")


main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Katalog').add('Savat').add('Kontakt').add('Admin-panel')


admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Tovar qoshish').add('Tovarni ochirish').add('Havola qilish')

# Inline tugmalar
katalog_list = InlineKeyboardMarkup(row_width=2)
katalog_list.add(InlineKeyboardButton(text='Futbolkalar', callback_data='t-shirt'),
                 InlineKeyboardButton(text='Shortiklar', callback_data='shorts'),
                 InlineKeyboardButton(text='Krossovkalar', callback_data='sneakers'))


cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add('bekor qilish')