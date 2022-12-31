import time
import random
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters import Message
from nonebot.params import CommandArg
from .klotsk import Klotsk
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from .rank import add_point,get_rank,get_point

group_id_list_cutm = []
obj_cutm = {}
group_id_list = []
obj_dist = {}
hrd = on_command('puzzle',aliases={'华容道','pz'},priority=32)             # 新游戏

drctn_list = ['U', 'D', 'L', 'R']
mode_list = ['8','15','24']
mode_dist = {'8':3,'15':4,'24':5}
@hrd.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    group_id = event.group_id
    uid = event.user_id

    if group_id not in group_id_list:
        if args.extract_plain_text() not in mode_list:
            await hrd.finish('模式不支持，请重新触发命令～')
        group_id_list.append(group_id)
        puzzle = Klotsk(mode_dist[args.extract_plain_text()])

        exec(f"obj_dist[{group_id}] = puzzle")

        buf = puzzle.toJson()
        img = MessageSegment.image(buf.getvalue())
        await hrd.finish(img)
        buf.close()
    if args.extract_plain_text() in mode_list:
        await hrd.finish(f"已存在游戏,请发送pz结束,结束当前游戏～")
    if args.extract_plain_text() == '结束':
        group_id_list.remove(group_id)
        await hrd.finish("游戏结束")
    puzzle = obj_dist[group_id]
    plain_texts = args.extract_plain_text().upper()  # 命令匹配

    cmd_list = []
    for i in plain_texts:
        if i in drctn_list:
            cmd_list.append(i)
    done = puzzle.move_sqnc(cmd_list)
    if done:
        add_point(group_id=group_id, uid=uid, name=event.sender.nickname,mode=puzzle.mode)
        buf = puzzle.toJson()
        points = get_point(uid=uid, group=group_id, mode=puzzle.mode)
        msg_text = f"执行操作{puzzle.cmd_strs}\n已还原,用时：{puzzle.duration()}\n获得积分1,当前积分{points}\n"
        img = MessageSegment.image(buf.getvalue())
        await hrd.finish(msg_text+img)
        group_id_list.remove(group_id)
        buf.close()
    else:

        msg_text = f"执行操作{puzzle.cmd_strs}\n用时：{puzzle.duration()}\n"
        buf = puzzle.toJson()
        img = MessageSegment.image(buf.getvalue())
        await hrd.finish(msg_text + img)
        buf.close()


rankpuzzle = on_command("rankpuzzle", aliases={'华容排名', 'rankpz'}, priority = 20)
@rankpuzzle.handle()
async def send_rank(event: GroupMessageEvent, args: Message = CommandArg()):                                     # 发送群排名
    if args.extract_plain_text() not in mode_list:
        await rankpuzzle.finish('模式不支持，请重新触发命令～')
    rank_text = get_rank(event.group_id,mode=mode_dist[args.extract_plain_text()])
    await rankpuzzle.finish(rank_text)

custom = on_command('def',aliases={'自定义'},priority=31)                      # 导入游戏
@custom.handle()
async def cutm(event: GroupMessageEvent, args: Message = CommandArg()):
    group_id = event.group_id
    uid = event.user_id
    if group_id not in group_id_list_cutm:
        plain_text = args.extract_plain_text()
        plain_text = plain_text.replace('\n', ' ')
        plain_text = plain_text.split(' ')
        mode = str(len(plain_text) - 1)
        if mode not in mode_list:
            print(mode)
            await custom.finish('导入失败,请重试～')
        new_klotsk = []
        plain_text.reverse()
        mode = mode_dist[mode]
        for i in range(mode):
            tmp = []
            for j in range(mode):
                tmp.append(int(plain_text.pop()))
            new_klotsk.append(tmp)
        group_id_list_cutm.append(group_id)
        puzzle = Klotsk(mode)
        puzzle.klotsk = new_klotsk
        exec(f"obj_cutm[{group_id}] = puzzle")

        buf = puzzle.toJson()
        img = MessageSegment.image(buf.getvalue())
        await hrd.finish(img)
        buf.close()
    if '\n' in args.extract_plain_text():
        await custom.finish(f"已存在游戏,请发送def结束,结束当前游戏～")
    if args.extract_plain_text() == '结束':
        group_id_list_cutm.remove(group_id)
        await custom.finish("游戏结束")
    puzzle = obj_cutm[group_id]
    plain_texts = args.extract_plain_text().upper()  # 命令匹配

    cmd_list = []
    for i in plain_texts:
        if i in drctn_list:
            cmd_list.append(i)
    done = puzzle.move_sqnc(cmd_list)
    if done:
        buf = puzzle.toJson()
        msg_text = f"执行操作{puzzle.cmd_strs}\n已还原,用时：{puzzle.duration()}"
        img = MessageSegment.image(buf.getvalue())
        await custom.finish(msg_text + img)
        group_id_list_cutm.remove(group_id)
        buf.close()
    else:
        msg_text = f"执行操作{puzzle.cmd_strs}\n用时：{puzzle.duration()}\n"
        buf = puzzle.toJson()
        img = MessageSegment.image(buf.getvalue())
        await custom.finish(msg_text + img)
        buf.close()

