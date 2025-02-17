import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔑 Tokenni o'zingizning bot tokeningizga almashtiring
TOKEN = "7925929707:AAE_NeRoegYWfIIqW-g0NQfaNnljIG0tijE"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# 📝 Logger qo'shamiz
logging.basicConfig(level=logging.INFO)

# ❓ 500 ta savol va javoblar (tasodifiy tanlanadi)
questions = [
     {"savol": "🇺🇿 O‘zbekiston poytaxti qaysi shahar?", "javob": "Toshkent", "variantlar": ["Samarqand", "Buxoro", "Toshkent", "Andijon"]},
    {"savol": "🌑 Yerning sun’iy yo‘ldoshi nima?", "javob": "Oy", "variantlar": ["Mars", "Oy", "Yupiter", "Venera"]},
    {"savol": "🌊 Eng katta okean qaysi?", "javob": "Tinch okeani", "variantlar": ["Atlantika", "Hind", "Tinch okeani", "Shimoliy Muz"]},
    {"savol": "🚗 Tesla kompaniyasining asoschisi kim?", "javob": "Ilon Mask", "variantlar": ["Jeff Bezos", "Ilon Mask", "Bill Gates", "Steve Jobs"]},
    {"savol": "🏔️ Dunyodagi eng baland tog‘ qaysi?", "javob": "Everest", "variantlar": ["Elbrus", "Everest", "Kilimanjaro", "Mak-Kinli"]},
    {"savol": "🌍 Yerning eng katta qit’asi qaysi?", "javob": "Osiyo", "variantlar": ["Afrika", "Osiyo", "Yevropa", "Janubiy Amerika"]},
    {"savol": "🔬 Kim tortishish kuchini kashf qilgan?", "javob": "Isaac Newton", "variantlar": ["Albert Einstein", "Galileo Galilei", "Isaac Newton", "Nikola Tesla"]},
    {"savol": "🕰 Eng uzun sutka qaysi sayyorada?", "javob": "Venera", "variantlar": ["Mars", "Yupiter", "Venera", "Saturn"]},
    {"savol": "🎨 Mona Liza asarining muallifi kim?", "javob": "Leonardo da Vinci", "variantlar": ["Pablo Picasso", "Leonardo da Vinci", "Vincent van Gogh", "Claude Monet"]},
    {"savol": "🎼 Qaysi nota eng baland chastotaga ega?", "javob": "Si", "variantlar": ["Do", "Fa", "Sol", "Si"]},
    {"savol": "🗼 Eifel minorasi qaysi shahar joylashgan?", "javob": "Parij", "variantlar": ["Rim", "London", "Berlin", "Parij"]},
    {"savol": "🦅 Qaysi qush eng tez ucha oladi?", "javob": "Lochin", "variantlar": ["Qirg‘iy", "Burgut", "Lochin", "Qarg‘a"]},
    {"savol": "💎 Eng qimmatbaho tosh qaysi?", "javob": "Oltin", "variantlar": ["Brilliant", "Zumrad", "Oltin", "Yashma"]},
    {"savol": "⚽️ FIFA Jahon chempionatini eng ko‘p yutgan jamoa?", "javob": "Braziliya", "variantlar": ["Germaniya", "Braziliya", "Argentina", "Fransiya"]},
    {"savol": "🦈 Dunyodagi eng katta baliq qaysi?", "javob": "Kit akula", "variantlar": ["Delfin", "Kit akula", "Qizil losos", "Skat"]},
    {"savol": "🔢 7 × 8 natijasi nechiga teng?", "javob": "56", "variantlar": ["54", "56", "58", "60"]},
    {"savol": "🌗 Oyda tortishish kuchi Yerdagiga nisbatan qanday?", "javob": "6 marta kam", "variantlar": ["10 marta ko‘p", "6 marta kam", "Teng", "2 marta ko‘p"]},
    {"savol": "🔥 Suvning qaynash harorati nechaga teng?", "javob": "100°C", "variantlar": ["90°C", "100°C", "110°C", "120°C"]},
    {"savol": "💡 Elektr lampochkasini kim ixtiro qilgan?", "javob": "Thomas Edison", "variantlar": ["Nikola Tesla", "Albert Einstein", "Thomas Edison", "Isaac Newton"]},
    {"savol": "🔭 Quyosh tizimining eng katta sayyorasi qaysi?", "javob": "Yupiter", "variantlar": ["Mars", "Venera", "Yupiter", "Saturn"]},
    {"savol": "🛤 Dunyoning eng uzun temir yo‘li qaysi mamlakatda joylashgan?", "javob": "Rossiya", "variantlar": ["Xitoy", "AQSh", "Rossiya", "Kanada"]},
    {"savol": "🎭 Shekspirning qaysi asari mashhur Romeo va Julietaga tegishli?", "javob": "Romeo va Julieta", "variantlar": ["Hamlet", "Otello", "Romeo va Julieta", "Makbet"]},
    {"savol": "🦒 Dunyodagi eng baland hayvon qaysi?", "javob": "Jirafa", "variantlar": ["Fil", "Jirafa", "Begemot", "O‘rdak"]},
    {"savol": "📅 Bir yilda nechta oy 31 kundan iborat?", "javob": "7", "variantlar": ["5", "6", "7", "8"]},
    {"savol": "🌪 Dunyoning eng kuchli shamollari qayerda kuzatiladi?", "javob": "Antarktida", "variantlar": ["Sibir", "Sahroi Kabir", "Antarktida", "Amazonka"]},
    {"savol": "🚀 Inson birinchi marta qaysi yilda Oyga qadam qo‘ygan?", "javob": "1969", "variantlar": ["1959", "1965", "1969", "1972"]},
    {"savol": "📖 Dunyodagi eng ko‘p sotilgan kitob qaysi?", "javob": "Bibliya", "variantlar": ["Qur'on", "Don Kixot", "Bibliya", "Harry Potter"]},
    {"savol": "🎤 Michael Jacksonning eng mashhur qo‘shig‘i qaysi?", "javob": "Thriller", "variantlar": ["Billie Jean", "Thriller", "Bad", "Smooth Criminal"]},
    {"savol": "⚖️ Nima og‘irroq, 1 kg paxta yoki 1 kg temir?", "javob": "Teng", "variantlar": ["Paxta", "Temir", "Teng", "Bilmadim"]},
    {"savol": "💰 Dunyodagi eng qadimgi valyuta qaysi?", "javob": "Funt sterling", "variantlar": ["Dollar", "Yevro", "Funt sterling", "Yen"]},
    {"savol": "🐘 Filning burni qanday nomlanadi?", "javob": "Xartum", "variantlar": ["Xartum", "Tumshuq", "Burun", "Dum"]},
    {"savol": "🦸‍♂️ Qaysi superqahramon o‘rgimchak tarmog‘idan foydalanadi?", "javob": "Spider-Man", "variantlar": ["Batman", "Iron Man", "Superman", "Spider-Man"]},
    {"savol": "📡 Qaysi texnologiya mobil internet uchun ishlatiladi?", "javob": "4G", "variantlar": ["3G", "4G", "Wi-Fi", "Ethernet"]},
    {"savol": "🎬 Dunyodagi eng mashhur film mukofoti?", "javob": "Oskar", "variantlar": ["Oskar", "Grammy", "Nobel", "Emmy"]},
    {"savol": "🔮 Qaysi moddiy jismlar yorug‘likni o‘tkazmaydi?", "javob": "Qora jism", "variantlar": ["Shisha", "Oyna", "Qora jism", "Plastik"]},
    {"savol": "🌞 Quyosh qaysi gazlardan tashkil topgan?", "javob": "Vodorod va geliy", "variantlar": ["Azot va kislorod", "Vodorod va geliy", "Uglerod va kislorod", "Temir va nikel"]},
    {"savol": "🛸 Qaysi mamlakat NASA kosmik agentligiga ega?", "javob": "AQSh", "variantlar": ["Rossiya", "Xitoy", "AQSh", "Hindiston"]},
    {"savol": "🥣 O‘zbekistonning mashhur shirinligi 'Navruz' uchun tayyorlanadigan milliy taom nima?", "javob": "Sumalak", "variantlar": ["Palov", "Norin", "Sumalak", "Manti"]},
    {"savol": "⚽ FIFA Jahon chempionatini eng ko‘p yutgan jamoa?", "javob": "Braziliya", "variantlar": ["Germaniya", "Braziliya", "Argentina", "Fransiya"]},
    {"savol": "🏀 NBA tarixidagi eng ko‘p chempionlikka ega klub?", "javob": "Boston Celtics", "variantlar": ["Chicago Bulls", "Los Angeles Lakers", "Boston Celtics", "Golden State Warriors"]},
    {"savol": "🎾 Tennischi Rafael Nadal qaysi mamlakatdan?", "javob": "Ispaniya", "variantlar": ["Fransiya", "Ispaniya", "AQSh", "Argentina"]},
    {"savol": "🏁 Formula 1 tarixidagi eng ko‘p chempion bo‘lgan haydovchi?", "javob": "Michael Schumacher", "variantlar": ["Lewis Hamilton", "Ayrton Senna", "Michael Schumacher", "Sebastian Vettel"]},
    {"savol": "🥊 Muhammad Ali qanday sport turi bilan shug‘ullangan?", "javob": "Boks", "variantlar": ["Dzyudo", "Boks", "Karate", "Kurash"]},
    {"savol": "⚾ Beysbol qaysi davlatda ixtiro qilingan?", "javob": "AQSh", "variantlar": ["Yaponiya", "Kanada", "AQSh", "Meksika"]},
    {"savol": "🏌️ Golf sportida bitta maydonda nechta teshik (hole) bo‘ladi?", "javob": "18", "variantlar": ["9", "12", "18", "21"]},
    {"savol": "🏊 Olimpiya o‘yinlarida eng ko‘p oltin medal olgan sportchi kim?", "javob": "Michael Phelps", "variantlar": ["Usain Bolt", "Michael Phelps", "Carl Lewis", "Serena Williams"]},
    {"savol": "🏒 Xokkey qaysi davlatda paydo bo‘lgan?", "javob": "Kanada", "variantlar": ["Rossiya", "AQSh", "Kanada", "Shvetsiya"]},
    {"savol": "⚽ Lionel Messi qaysi yili tug‘ilgan?", "javob": "1987", "variantlar": ["1985", "1986", "1987", "1988"]},
    {"savol": "🏀 Basketbol to‘pining rangi qanday?", "javob": "To‘q sariq", "variantlar": ["Qizil", "Ko‘k", "To‘q sariq", "Yashil"]},
    {"savol": "🏆 Olimpiya o‘yinlari har necha yilda bir marta o‘tkaziladi?", "javob": "4 yil", "variantlar": ["2 yil", "3 yil", "4 yil", "5 yil"]},
    {"savol": "⚽ Qaysi futbolchi «Oltin to‘p» mukofotini eng ko‘p yutgan?", "javob": "Lionel Messi", "variantlar": ["Cristiano Ronaldo", "Lionel Messi", "Pele", "Maradona"]},
    {"savol": "🎯 Dart sportida maksimal ochko nechta?", "javob": "180", "variantlar": ["100", "150", "180", "200"]},
    {"savol": "🚴 Tour de France musobaqasi qaysi sport turi bilan bog‘liq?", "javob": "Velosport", "variantlar": ["Poyga", "Velosport", "Regbi", "Basketbol"]},
    {"savol": "⚽ Ronaldoni 'Fenomen' deb kim atashgan?", "javob": "Braziliyalik Ronaldo", "variantlar": ["Cristiano Ronaldo", "Braziliyalik Ronaldo", "Ronaldinho", "Neymar"]},
    {"savol": "🏆 Olimpiya bayrog‘ida nechta halqa bor?", "javob": "5", "variantlar": ["3", "4", "5", "6"]},
    {"savol": "🏉 Regbi qaysi davlatda paydo bo‘lgan?", "javob": "Angliya", "variantlar": ["Avstraliya", "Yangi Zelandiya", "Angliya", "AQSh"]},
    {"savol": "🏓 Stol tennisi qaysi davlatda ixtiro qilingan?", "javob": "Angliya", "variantlar": ["Xitoy", "Germaniya", "Angliya", "Yaponiya"]},
    {"savol": "🏋️‍♂️ Og‘ir atletika bo‘yicha eng mashhur sportchilardan biri kim?", "javob": "Ilya Ilyin", "variantlar": ["Usain Bolt", "Ilya Ilyin", "Michael Phelps", "Yuriy Vlasov"]},
    {"savol": "⚽ Eng ko‘p gol urgan futbolchi kim?", "javob": "Cristiano Ronaldo", "variantlar": ["Lionel Messi", "Pele", "Cristiano Ronaldo", "Diego Maradona"]},
    {"savol": "🏇 Ot sportining yana bir nomi qanday?", "javob": "Konkur", "variantlar": ["Polo", "Konkur", "Derbi", "Skijoring"]},
    {"savol": "🚣 Kanoe sportida necha kishi ishtirok etadi?", "javob": "1 yoki 2", "variantlar": ["1 yoki 2", "3", "4", "5"]},
    {"savol": "🏆 Jahon chempionatining birinchi g‘olibi kim bo‘lgan?", "javob": "Urugvay", "variantlar": ["Braziliya", "Italiya", "Urugvay", "Germaniya"]},
    {"savol": "🏀 Qaysi basketbolchi 100 ta ochko bitta o‘yinda urgan?", "javob": "Wilt Chamberlain", "variantlar": ["Michael Jordan", "Wilt Chamberlain", "LeBron James", "Kobe Bryant"]},
    {"savol": "🏌️ Golf maydonida eng mashhur musobaqa?", "javob": "Masters Tournament", "variantlar": ["Ryder Cup", "Masters Tournament", "The Open Championship", "US Open"]},
    {"savol": "⚽ Qaysi futbol klubi 'El Clasico' da ishtirok etadi?", "javob": "Real Madrid va Barcelona", "variantlar": ["Liverpool va Manchester United", "Real Madrid va Barcelona", "PSG va Marseille", "Bayern Munich va Borussia Dortmund"]},
    {"savol": "🏏 Kriket eng mashhur bo‘lgan davlat?", "javob": "Hindiston", "variantlar": ["Avstraliya", "Hindiston", "Angliya", "Yangi Zelandiya"]},
    {"savol": "🥋 Dzyudo qaysi davlatda paydo bo‘lgan?", "javob": "Yaponiya", "variantlar": ["Xitoy", "Koreya", "Yaponiya", "Rossiya"]},
    {"savol": "🥊 Boks ringining shakli qanday?", "javob": "Kvadrat", "variantlar": ["Dumaloq", "Kvadrat", "Uchburchak", "To‘g‘ri to‘rtburchak"]},
    {"savol": "🏐 Voleybol qaysi mamlakatda ixtiro qilingan?", "javob": "AQSh", "variantlar": ["Braziliya", "Italiya", "AQSh", "Fransiya"]},
    {"savol": "🚴 Olimpiya o‘yinlarida nechta sport turi bo‘ladi?", "javob": "40 dan ortiq", "variantlar": ["20", "30", "40 dan ortiq", "50"]},
    {"savol": "🎳 Bovlingda eng yuqori ball nechaga teng?", "javob": "300", "variantlar": ["100", "200", "250", "300"]},
    {"savol": "O‘zbekistonning milliy me’moriy yodgorligi 'Hazrat Imom Majmuasi' qaysi shaharda joylashgan?", "javob": "Toshkent", "variantlar": ["Samarqand", "Toshkent", "Namangan", "Andijon"]},
    {"savol": "Oqsoqolning boshidagi nechta tosh bor, agar u uchtasini tashlab yuborsa?", "javob": "Ikki tosh", "variantlar": ["Bir tosh", "Ikki tosh", "Uch tosh", "To'rtta tosh"]} ,
    {"savol": "Qaerda 'Yangi yil' avval boshlandi?", "javob": "Sharqda", "variantlar": ["Sharqda", "G‘arbda", "Shimolda", "Janubda"]} ,
    {"savol": "Qaysi hayvonning nomi birinchi boshlangan?", "javob": "Bug‘u", "variantlar": ["Bug‘u", "Suvqurbaqa", "To‘ng‘iz", "Chumchuq"]} ,
    {"savol": "Eng uzoq vaqtda tutilib turadigan gap nima?", "javob": "Sukunat", "variantlar": ["Kulgi", "Gap", "Sukunat", "Uyqu"]} ,
    {"savol": "Qaysi hayvon o‘z o‘rnida qoladi?", "javob": "Mol", "variantlar": ["Eshak", "Tulki", "Mol", "Mushuk"]} ,
    {"savol": "Qaysi o‘zbekcha so‘z doimo aqlni charxlaydi?", "javob": "Kitob", "variantlar": ["Kitob", "Radio", "Televizor", "Telefon"]} ,
    {"savol": "Qaysi shaharni dunyo bo‘ylab tanishadi, lekin u yerda hech kim yashamaydi?", "javob": "Xotira", "variantlar": ["Samarqand", "Buxoro", "Xotira", "Toshkent"]} ,
    {"savol": "Qaysi so‘zda uchta 'o' bor?", "javob": "Olov", "variantlar": ["Qovoq", "Olov", "Tomosha", "Osh"]} ,
    {"savol": "Qaysi hayvon doimo yolg‘iz yuradi?", "javob": "Tulk", "variantlar": ["Tulk", "Sher", "Ot", "Qoplon"]} ,
    {"savol": "Eng katta joyda nima joylashgan?", "javob": "Bo‘sh joy", "variantlar": ["Uy", "Do‘kon", "Bo‘sh joy", "Bozor"]} ,
    {"savol": "Qaerda butun dunyo harakatsiz qoladi?", "javob": "Xotira", "variantlar": ["Hayot", "Xotira", "Chuqur", "Ko‘z"]} ,
    {"savol": "Qaysi so‘zda uchta 's' bor?", "javob": "Assalom", "variantlar": ["Tennis", "Assalom", "Soss", "Sovuq"]} ,
    {"savol": "Qaysi hayvon bir vaqtning o‘zida uchadi va yuradi?", "javob": "Eshak", "variantlar": ["Ot", "It", "Eshak", "Echki"]} ,
    {"savol": "Qaerda suv to‘ldirish mumkin, lekin hech qachon kam emas?", "javob": "Daryo", "variantlar": ["Ko‘l", "Hovuz", "Daryo", "Chashma"]} ,
    {"savol": "Qaerda shamollar hech qachon to‘xtamaydi?", "javob": "Chorrahada", "variantlar": ["Chorrahada", "Bog‘da", "Uyda", "Hovlida"]} ,
    {"savol": "Qaerda quyosh chiqadi va botadi?", "javob": "Osmonda", "variantlar": ["Yerda", "Osmonda", "Dengizda", "Chorrahada"]} ,
    {"savol": "Qaysi joyda dengiz hech qachon suvsiz qolmaydi?", "javob": "Xayol", "variantlar": ["Daryo", "Ko‘l", "Xayol", "Chashma"]} ,
    {"savol": "Qaysi so‘z uchta 'q' bilan yoziladi?", "javob": "Qovoq", "variantlar": ["Quloq", "Qiyin", "Qovoq", "Qaldirg‘och"]} ,
    {"savol": "Qaerda olov hech qachon o‘chmaydi?", "javob": "Ko‘ngil", "variantlar": ["Uyda", "Ko‘ngil", "Bog‘da", "Dengizda"]} ,
    {"savol": "Qaysi so‘zda uchta 'b' bor?", "javob": "Boboqol", "variantlar": ["Boboqol", "Bobo", "Bubbik", "Balbob"]} ,
    {"savol": "Dunyodagi eng uzun daryo qaysi?", "javob": "Nil", "variantlar": ["Amazonka", "Nil", "Misisipi", "Yangtze"]} ,
    {"savol": "Yer yuzining nechta qismi suv bilan qoplangan?", "javob": "70%", "variantlar": ["50%", "60%", "70%", "80%"]} ,
    {"savol": "Qaysi davlat aholisi eng ko‘p?", "javob": "Xitoy", "variantlar": ["Hindiston", "Xitoy", "AQSh", "Indoneziya"]} ,
    {"savol": "Dunyodagi eng baland tog‘ qaysi?", "javob": "Everest", "variantlar": ["K2", "Everest", "Denali", "Makalu"]} ,
    {"savol": "Qaysi dengiz O‘zbekiston hududida joylashgan?", "javob": "Orol dengizi", "variantlar": ["Qora dengiz", "Orol dengizi", "Aral dengizi", "Kaspiy dengizi"]} ,
    {"savol": "Dunyodagi eng katta sahro qaysi?", "javob": "Sahroi Kabir", "variantlar": ["Gobi", "Kalahari", "Sahroi Kabir", "Arabiston sahrosi"]} ,
    {"savol": "Qaysi mamlakatning poytaxti Uashington?", "javob": "AQSh", "variantlar": ["Kanada", "Meksika", "AQSh", "Braziliya"]} ,
    {"savol": "Qaysi davlat 2020 yilda yozgi Olimpiada o‘yinlariga mezbonlik qilgan?", "javob": "Yaponiya", "variantlar": ["Yaponiya", "Braziliya", "Xitoy", "Angliya"]} ,
    {"savol": "Dunyodagi eng katta qit’a qaysi?", "javob": "Osiyo", "variantlar": ["Osiyo", "Afrika", "Yevropa", "Amerika"]} ,
    {"savol": "O‘zbekistonning rasmiy tili qaysi?", "javob": "O‘zbek tili", "variantlar": ["Rus tili", "Tojik tili", "O‘zbek tili", "Qirg‘iz tili"]} ,
    {"savol": "O‘zbekiston Respublikasi mustaqilligini qachon e’lon qilgan?", "javob": "1991 yil", "variantlar": ["1989 yil", "1991 yil", "1994 yil", "1998 yil"]} ,
    {"savol": "Dunyodagi eng katta ko‘l qaysi?", "javob": "Kaspiy dengizi", "variantlar": ["Kaspiy dengizi", "Baykal ko‘li", "Yuqori ko‘l", "Viktoriya ko‘li"]} ,
    {"savol": "Dunyodagi eng ko‘p aholisi bo‘lgan shahar qaysi?", "javob": "Tokyo", "variantlar": ["Shanghai", "Mumbai", "New York", "Tokyo"]} ,
    {"savol": "Yer kurrasida nechta qit’a bor?", "javob": "7", "variantlar": ["5", "6", "7", "8"]}
]
# 🌀 Savollarni har safar aralashtiramiz
random.shuffle(questions)

# 🏆 Foydalanuvchilar ma'lumotlari
players = {}

@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    chat_id = message.chat.id
    players[chat_id] = {"score": 0, "current_question": 0}
    total_players = len(players)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("📢 Bizning Telegram kanal", url="https://t.me/webstormers"))
    await message.answer(
        "🎮 <b>Aqilni Sinov o‘yini boshlandi!</b> \n\n👥 Jami foydalanuvchilar: {}".format(total_players),
        parse_mode="HTML",
        reply_markup=keyboard
    )
    await ask_question(message)


async def ask_question(message):
    chat_id = message.chat.id
    player = players.get(chat_id)

    if player and player["current_question"] < len(questions):
        question_data = questions[player["current_question"]]
        savol = question_data["savol"]
        variantlar = question_data["variantlar"]
        random.shuffle(variantlar)  # 🌀 Variantlarni ham aralashtiramiz
        
        keyboard = InlineKeyboardMarkup()
        for variant in variantlar:
            keyboard.add(InlineKeyboardButton(variant, callback_data=variant))
        
        progress = "🟩" * player["current_question"] + "⬜" * (len(questions) - player["current_question"] - 1)
        
        await message.answer(
            f"❓ <b>{savol}</b>\n\n{progress}", parse_mode="HTML", reply_markup=keyboard
        )
    else:
        await message.answer("🎉 <b>Siz barcha savollarga to‘g‘ri javob berdingiz!</b> 👏", parse_mode="HTML")
        await message.answer("🏆 <b>TABRIKLAYMIZ!</b> Siz barcha savollarga to‘g‘ri javob berdingiz va o‘yinni muvaffaqiyatli yakunladingiz! 🎉", parse_mode="HTML")
        await end_game(message)

@dp.callback_query_handler(lambda call: True)
async def check_answer(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    player = players.get(chat_id)

    if player:
        current_question = player["current_question"]
        correct_answer = questions[current_question]["javob"]
        
        if call.data == correct_answer:
            player["score"] += 1
            player["current_question"] += 1
            await call.message.edit_text("✅ <b>To‘g‘ri javob!</b> 🎉", parse_mode="HTML")
            await ask_question(call.message)
        else:
            await call.message.edit_text(
                f"❌ <b>Noto‘g‘ri!</b> ✅ To‘g‘ri javob: <b>{correct_answer}</b>\n🎯 Siz {player['score']} ball to‘pladingiz.",
                parse_mode="HTML"
            )
            await end_game(call.message)

async def end_game(message):
    chat_id = message.chat.id
    players.pop(chat_id, None)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔄 Qayta o‘ynash", callback_data="restart"))
    await message.answer("🔄 Qayta o‘ynash uchun /start tugmani bosing!", reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data == "restart")
async def restart_game(call: types.CallbackQuery):
    await start_game(call.message)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)