from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg

import random
from datetime import date
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
import openai
openai.api_key = "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"

ai = on_command("ai", priority=0)
@ai.handle()
async def aiqa(args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：st 60 3 3
    resp = await opai(plain_text)
    await ai.finish(resp, at_sender=True)
    
atttt = on_command('pp',aliases={"皮皮",'老婆'}, priority=0)


@atttt.handle()
async def at():
    await atttt.finish(Message(
        f'[CQ:at,qq={2507216537}]皮皮贴贴'))

att = on_command('qzl',aliases={'权志龙'}, priority=0)


@att.handle()
async def att():
    await atttt.finish(Message(
        f'[CQ:at,qq={2743836019}]有人找你'))

hlp = on_command('使用说明',aliases={'说明'}, priority=0)


@hlp.handle()
async def hlpe():
    await hlp.finish("功能1:    \n扫雷\n示例：@zowo 扫雷，@zowo 扫雷初/中/高级；\n\n\n功能2:    \n21点\n示例：签到，21点，积分对战\n\n\n功能3:    \nopenai提问\n示例：ai 你好，ai 晚餐吃什么？\n\n\n功能4:    \n扫雷stnb计算\n示例：s+time+bvs+mode 例：“s 60 3 3”\n\n\n功能5:    \n今日人品\n示例：jrrp，今日人品\n\n\
\n\n功能6:    \n魔方\n示例：mf|cube|c|魔方\n\n\n功能7:    \n数字华容道\n示例：pz8|puzzle15|华容道24\n\n\n\n咨询QQ群399899914")

jrrp = on_command('jrrp', aliases={'今日人品'}, priority=50)


@jrrp.handle()
async def jrrp_handle(event: Event):
    rnd = random.Random()
    rnd.seed(int(date.today().strftime("%y%m%d")) + int(event.get_user_id()))
    lucknum = rnd.randint(1, 100)
    await jrrp.finish(Message(
        f'[CQ:at,qq={event.get_user_id()}]您今日的幸运指数是{lucknum}/100（越低越好），为"{luck_simple(lucknum)}"'))




stnb = on_command("st", aliases={"s", "stnb"}, priority=60)


@stnb.handle()
async def handle_first_receive(args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：st 60 3 3
    num = await compute(plain_text)
    await stnb.finish(num, at_sender=True)


async def compute(city: str) -> str:
    time = city.split(' ')[0]
    bvs = city.split(' ')[1]
    grade = city.split(' ')[2]

    if grade == '1':
        cont = 47.229
    elif grade == '2':
        cont = 153.73
    else:
        cont = 435.001
    return str(cont / ((float(time) ** 1.7) / (float(time) * float(bvs))))[:5]



def luck_simple(num):
    if num < 18:
        return '大吉'
    elif num < 53:
        return '吉'
    elif num < 58:
        return '半吉'
    elif num < 62:
        return '小吉'
    elif num < 65:
        return '末小吉'
    elif num < 71:
        return '末吉'
    else:
        return '凶'


async def opai(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["？"]
    )
    return response.choices[0].text