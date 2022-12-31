import openai

openai.api_key = "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"


def opai(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["？"]
    )
    return response.choices[0].text


# print(opai('北京天气？'))
sist = {
    'error_code': 0,
    'error_msg': 'SUCCESS',
    'log_id': 2153555723,
    'timestamp': 1672403753,
    'cached': 0,
    'result': {
        'face_num': 1,
        'face_list': [{
            'face_token': '3722bdb44c718cdaa4c24954ad359195',
            'location': {
                'left': 204.35,
                'top': 184.51,
                'width': 186,
                'height': 132,
                'rotation': 7
            },
            'face_probability': 1,
            'angle': {
                'yaw': -9.38,
                'pitch': 18.25,
                'roll': 7.21},
            'gender': {
                'type': 'female',
                'probability': 0.99
            },
            'beauty': 56.13}]}}
