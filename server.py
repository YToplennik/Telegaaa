import logging
import random
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import ReplyKeyboardMarkup
from config import TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def status0():
    global stage, score, hp, level, effects, doors_now
    stage = 0
    score = 0
    hp = 100
    level = 1
    effects = []
    doors_now = []


results = ['nothing', 'chest', 'hole', 'poisoning', 'The ogre', 'gold', 'finish?', 'mimic']
doors = ['default', 'scratched', 'golden', 'dark', 'flower']

description_of_the_doors = {'default': 'классическая, деревянная обитая медью',
                            'scratched': 'металлическая с глубокими следами когтей, больше похожая на люк',
                            'golden': 'блестящая, отлитая из золота',
                            'dark': 'оказалассь даже не дверью, а скорее проходом в кромешную тьму, куда даже не падал'
                                    ' свет',
                            'flower': 'деревянная, окутанная цветами'}


def chanse():
    n = random.randint(0, 100)
    if n <= 65:
        doors_now.append(doors[0])
    elif 65 < n <= 77:
        doors_now.append(doors[1])
    elif 77 < n <= 83:
        doors_now.append(doors[2])
    elif 83 < n <= 85:
        doors_now.append(doors[3])
    elif 85 < n <= 100:
        doors_now.append(doors[4])


async def result(update, i):
    door_results = {'default': f'{random.choice([results[0], results[0], results[0], results[1], results[5]])}',
                    'scratched': f'{random.choice([results[0], results[0], results[4]])}',
                    'golden': f'{random.choice([results[5], results[1], results[7]])}',
                    'dark': f'{random.choice([results[0], results[2], results[4]])}',
                    'flower': f'{random.choice([results[0], results[3], results[3], results[1]])}'}
    global doors_now, hp, score, stage, effects
    if stage > 1:
        if door_results[i] == 'nothing':
            doors_now.clear()
            for i in range(3):
                chanse()
            await update.message.reply_text('За этой дверью нет ничего, кроме ещё трёх дверей\n'
                                            f'Первая дверь {description_of_the_doors[doors_now[0]]}.\n'
                                            f'Вторая - {description_of_the_doors[doors_now[1]]}.\n'
                                            f'А третья - {description_of_the_doors[doors_now[2]]}.',
                                            reply_markup=markup)
        elif door_results[i] == 'chest':
            doors_now.clear()
            for i in range(3):
                chanse()
            await update.message.reply_text('Посреди комнаты стоит сундук. Вы решаете его открыть и обнаруживаете '
                                            'большое количество золота (+50 золота)\n\n'
                                            'Впереди снова стоит 3 двери:\n'
                                            f'Первая дверь {description_of_the_doors[doors_now[0]]}.\n'
                                            f'Вторая - {description_of_the_doors[doors_now[1]]}.\n'
                                            f'А третья - {description_of_the_doors[doors_now[2]]}.',
                                            reply_markup=markup)
            score += 50
        elif door_results[i] == 'hole':
            doors_now.clear()
            for i in range(3):
                chanse()
            await update.message.reply_text('Вы прошли сквозь тёмную пустоту.\n'
                                            'Вдруг вы осознали что уже не идёте, а летите вниз.\n'
                                            'К счастью цветы, растущие на дне, смягчили ваше падение (-10 HP)\n\n'
                                            'Впереди снова стоит 3 двери:\n'
                                            f'Первая дверь {description_of_the_doors[doors_now[0]]}.\n'
                                            f'Вторая - {description_of_the_doors[doors_now[1]]}.\n'
                                            f'А третья - {description_of_the_doors[doors_now[2]]}.',
                                            reply_markup=markup)
            hp -= 10
        elif door_results[i] == 'poisoning':
            doors_now.clear()
            for i in range(3):
                chanse()
            await update.message.reply_text('Как только вы открыли дверь, вы почувствовали cебя нехорошо.\n'
                                            'А, нет. Даже хуже, чем просто нехорошо. Такое чувство, что вас '
                                            'выворачивает наизнанку. (-3 НР каждую комнату)\n\n'
                                            'Впереди снова стоит 3 двери:\n'
                                            f'Первая дверь {description_of_the_doors[doors_now[0]]}.\n'
                                            f'Вторая - {description_of_the_doors[doors_now[1]]}.\n'
                                            f'А третья - {description_of_the_doors[doors_now[2]]}.',
                                            reply_markup=markup)
            effects.append('poisoning')
        elif door_results[i] == 'The ogre':
            doors_now.clear()
            for i in range(3):
                chanse()
            await update.message.reply_text('Вы входите в комнату и видите людоеда по среди комнаты, обгладывающего '
                                            'кости. Краем глаза он замечат вас и уже бежит в вашу сторону. '
                                            'Но он успевает лишь задеть вас перед тем, как вы забегаете в случайную '
                                            'дверь. (-20 HP)\n',
                                            # 'Впереди снова стоит 3 двери:\n'
                                            # f'Первая дверь {description_of_the_doors[doors_now[0]]}.\n'
                                            # f'Вторая - {description_of_the_doors[doors_now[1]]}.\n'
                                            # f'А третья - {description_of_the_doors[doors_now[2]]}.',
                                            reply_markup=markup)
            hp -= 20
            a = random.randint(1, 4)
            if a == 1:
                await door1(update, context='')
            elif a == 2:
                await door2(update, context='')
            elif a == 3:
                await door3(update, context='')

        elif door_results[i] == 'gold':
            doors_now.clear()
            for i in range(3):
                chanse()
            await update.message.reply_text('В комнате лежит несколько горстей золота. Вы забираете золото себе '
                                            'и продолжаете путь (+10 золота)\n\n'
                                            'Впереди снова стоит 3 двери:\n'
                                            f'Первая дверь {description_of_the_doors[doors_now[0]]}.\n'
                                            f'Вторая - {description_of_the_doors[doors_now[1]]}.\n'
                                            f'А третья - {description_of_the_doors[doors_now[2]]}.',
                                            reply_markup=markup)
            score += 10
        elif door_results[i] == 'finish?':
            doors_now.clear()
            for i in range(3):
                chanse()
            await update.message.reply_text('????????????\n'
                                            f'Первая дверь {description_of_the_doors[doors_now[0]]}.\n'
                                            f'Вторая - {description_of_the_doors[doors_now[1]]}.\n'
                                            f'А третья - {description_of_the_doors[doors_now[2]]}.',
                                            reply_markup=markup)
        elif door_results[i] == 'mimic':
            doors_now.clear()
            for i in range(3):
                chanse()
            await update.message.reply_text('Посреди комнаты стоит сундук. Как только вы к нему приблизились, '
                                            'он откусил вам кусок лица, но вы успели убежать, прежде чем он ещё '
                                            'раз вас укусил. (-15 НР)\n\n'
                                            'Впереди снова стоит 3 двери:\n'
                                            f'Первая дверь {description_of_the_doors[doors_now[0]]}.\n'
                                            f'Вторая - {description_of_the_doors[doors_now[1]]}.\n'
                                            f'А третья - {description_of_the_doors[doors_now[2]]}.',
                                            reply_markup=markup)
            hp -= 15
        if 'poisoning' in effects:
            hp -= 3
        stage = 3
        if hp <= 0:
            await death(update, context='')
    else:
        await update.message.reply_text('Вы ещё не вошли в пещеру')


def stage_prow():
    global reply_keyboard, stage, markup
    if stage == 0:
        reply_keyboard = [['/start']]
    elif stage == 1:
        reply_keyboard = [['/Go']]
    elif stage == 2 or stage == 3:
        reply_keyboard = [['/1', '/2', '/3'],
                          ['/leave', '/stats']]
    elif stage == 999:
        reply_keyboard = [['/restart']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def start(update, context):
    global stage, doors_now
    if stage == 0 or stage == 999:
        doors_now = []
        stage = 1
        stage_prow()
        await update.message.reply_text('Здравствуйте!\n'
                                        'Готовы пройти сквозь пещеру, где за каждой дверью может быть что угодно?\n'
                                        'От сундуков с золотом до людоедов.\n' 
                                        'Ваша цель зайти как можно дальше вглубь пещеры и забрать с собой как можно '
                                        'больше сокровищ.\n'
                                        'Если хотите попытать свою удачу и зайти в пещеру, скажите "/Go".\n',
                                        reply_markup=markup)
    else:
        await update.message.reply_text('Вы уже начали')


async def stats(update, context):
    if stage > 1:
        await update.message.reply_text(f'Золото: {score}\n'
                                        f'Здоровье: {hp}')
    elif stage == 1:
        await update.message.reply_text('Вы ещё не в пещере')
    else:
        await update.message.reply_text('Пропишите "/start"',
                                        reply_markup=ReplyKeyboardMarkup([['/start']], one_time_keyboard=False))


async def kill(update, context):
    pass


async def naсhalo(update, context):
    global stage, doors_now
    if stage == 1:
        stage = 2
        for i in range(3):
            chanse()
        stage_prow()
        await update.message.reply_text('На удивление, войдя в пещеру вы заметили 3 двери, которых вы не видели '
                                        'до того как вошли в пещеру, хоть прошли вы не так далеко, '
                                        'чтобы их можно было не заметить.\n'
                                        'Так или иначе вам предстоит сделать выбор, который повлияет на вашу '
                                        'дальнейшую судьбу.\n\n'
                                        f'Первая дверь {description_of_the_doors[doors_now[0]]}.\n'
                                        f'Вторая - {description_of_the_doors[doors_now[1]]}.\n'
                                        f'А третья - {description_of_the_doors[doors_now[2]]}.',
                                        reply_markup=markup)
    elif stage == 0:
        await update.message.reply_text('Пропишите "/start"',
                                        reply_markup=ReplyKeyboardMarkup([['/start']], one_time_keyboard=False))
    else:
        await update.message.reply_text('Вы уже в пещере')


async def leave(update, context):
    global stage, score
    if stage == 2:
        stage = 999
        stage_prow()
        await update.message.reply_text('Несмотря на то, в глубине пещеры могли скрываться несметные богатства '
                                        'вы решили не рисковать своей жизнью и в страхе убежали из пещеры.\n'
                                        'Слухи о вашей трусливости разошлись по всей округе.\n\n'
                                        'Если хотите начать заново - скажите "/restart"',
                                        reply_markup=markup)
        status0()
    elif stage == 3:
        if score == 0:
            a = ", но собрать вам ничего так и не удалось."
        else:
            a = " вместе с " + str(score) + " золотыми"
        status0()
        stage_prow()
        await update.message.reply_text('Как только вы решили уйти из пещеры, вы сразу заметили что находитесь у её '
                                        f'выхода{a}',
                                        reply_markup=markup)
    elif stage == 0:
        await update.message.reply_text('Пропишите "/start"',
                                        reply_markup=ReplyKeyboardMarkup([['/start']], one_time_keyboard=False))


async def death(update, context):
    global stage
    status0()
    stage = 999
    stage_prow()
    await update.message.reply_text('После долгого нахождения в пещере, вы не смогли выжить и '
                                    'вам не удалось забрать себе её сокровища.',
                                    reply_markup=markup)


async def door1(update, context):
    if 5 > stage > 1:
        for i in doors:
            if doors_now[0] == i:
                await result(update, i)
                break
    elif stage == 0:
        await update.message.reply_text('Пропишите "/start"',
                                        reply_markup=ReplyKeyboardMarkup([['/start']], one_time_keyboard=False))
    else:
        await update.message.reply_text('Вы ещё не в пещере')


async def door2(update, context):
    if 4 > stage > 1:
        for i in doors:
            if doors_now[1] == i:
                await result(update, i)
                break
    elif stage == 0:
        await update.message.reply_text('Пропишите "/start"',
                                        reply_markup=ReplyKeyboardMarkup([['/start']], one_time_keyboard=False))
    else:
        await update.message.reply_text('Вы ещё не в пещере')


async def door3(update, context):
    if 5 > stage > 1:
        for i in doors:
            if doors_now[2] == i:
                await result(update, i)
                break
    elif stage == 0:
        await update.message.reply_text('Пропишите "/start"',
                                        reply_markup=ReplyKeyboardMarkup([['/start']], one_time_keyboard=False))
    else:
        await update.message.reply_text('Вы ещё не в пещере')


def main():
    status0()
    stage_prow()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('restart', start))
    app.add_handler(CommandHandler('Go', naсhalo))
    app.add_handler(CommandHandler('leave', leave))
    app.add_handler(CommandHandler('1', door1))
    app.add_handler(CommandHandler('2', door2))
    app.add_handler(CommandHandler('3', door3))
    app.add_handler(CommandHandler('stats', stats))
    app.add_handler(CommandHandler('kill', kill))
    logger.info('Бот работает')
    app.run_polling()


main()
