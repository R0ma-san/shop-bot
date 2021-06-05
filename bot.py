import telebot
import pandas

class ShopBot:
    __categories = pandas.read_csv('kivano.csv')
    categoriset = set(__categories.categori.to_list())
    productset = set(__categories.name.to_list())
    help_text = '''
/categories - выдать названия всех категорий.
/categories {название категории} - выдать товары этой категории.
/product {название продукта} выдать информацию о данном товаре.
                ''' 
    
    def show_categori(self, a):
            if len(a)<=0:
                return '\n'.join(self.categoriset)
            else:
                if a not in self.categoriset:
                    return f'Категории {a} не существует!'
                else:
                    cat = self.__categories[self.__categories.categori == a]
                    cat = cat[['name', 'url']][:10].to_string()
                    return cat
                    

    def show_item_info(self, args):
        if len(args)<=0:
                return 'Введите название продукта'
        else:
            if args not in self.productset:
               return f'Продукта {args} не существует!'
            else:
                prd = self.__categories[self.__categories.name == args]
                prd = prd[['name', 'categori', 'url']].to_string()    
                return prd        

TOKEN = '1732637874:AAEJUz2wwM7cWUV2oTMtFpIuXNdgWwvz05Y'
 
bot = telebot.TeleBot(TOKEN)
sbot = ShopBot()

@bot.message_handler(commands=['start', 'help'])
def show(message):
     bot.send_message(message.chat.id, sbot.help_text)

@bot.message_handler(commands=['categories'])
def categories(message):
    a = message.text[12:]
    bot.send_message(message.chat.id, sbot.show_categori(a))

@bot.message_handler(commands=['product'])
def categories(message):
    args = message.text[9:]
    bot.send_message(message.chat.id, sbot.show_item_info(args))


if __name__ == '__main__':
    bot.polling()
