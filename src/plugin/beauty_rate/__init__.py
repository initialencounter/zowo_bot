import re
import base64
from io import BytesIO

from httpx import AsyncClient
from nonebot.plugin import on_command
from nonebot.adapters import Message
from nonebot.params import EventMessage
from nonebot.adapters.onebot.v11 import MessageSegment

from .utils import FaceRecognition


API_KEY = "8kawU4KnlvCMIZNW7wgi7rvp"
SECRET_KEY = "DdSCPGAe3100DybVWoq1BbdPsvrFLIic"
face_val = on_command("人脸", priority=50, aliases={"face"})


@face_val.got("faces_pic", prompt="请发送人脸照片！")
async def beauty_score(msg: Message = EventMessage()):
    pic_CQcode = str(msg)
    if "CQ:image" not in pic_CQcode:
        await face_val.finish("发送的不是图片，请重新触发指令~", at_sender=True)
    pic_url = re.findall(r"url=[^,]+", pic_CQcode)[0].rstrip(']')[4:]
    async with AsyncClient() as client:
        resp = await client.get(pic_url)
    pic_b64_str = base64.b64encode(resp.content).decode()

    faces = FaceRecognition(pic_b64_str, API_KEY, SECRET_KEY)
    result = await faces.face_beauty()
    if result['error_msg'] == 'pic not has face':
        await face_val.finish("未从图片中识别到人脸~", at_sender=True)
    elif result['error_msg'] == 'image size is too large':
        await face_val.finish("图片太大啦~", at_sender=True)

    faces_gender = []
    gender_probability = []
    faces_pos = []
    faces_beauty = []
    try:
        print(result)
        for face in result['result']['face_list']:
            faces_gender.append('男' if face['gender']['type'] == 'male' else '女')
            gender_probability.append(face['gender']['probability'])
            faces_pos.append(face['location'])
            faces_beauty.append(face['beauty'])
    except (KeyError, TypeError):
        await face_val.finish("请重新检查指令~", at_sender=True)

    pic = resp.content
    pic_bytes_stream = BytesIO(pic)
    buf = BytesIO()
    await faces.draw_face_rects(pic_bytes_stream, buf, faces_pos)

    msg = MessageSegment.image(buf.getvalue())
    for i in range(len(faces_beauty)):
        msg += f"Face{i + 1}:\n" \
               f"性别: {faces_gender[i]}，概率：{gender_probability[i]}\n" \
               f"颜值: {faces_beauty[i]}/100\n"
    await face_val.send(msg)

    pic_bytes_stream.close()
    buf.close()
