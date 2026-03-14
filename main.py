"""
小红书爆款文案生成助手
"""
import streamlit as st
from openai import OpenAI

system_prompt = '''你是小红书爆款写作专家，请遵循以下步骤进行创作：首先产出三个标题（包含适当的emoji表情），
然后输出一段正文（段落可以包含emoji表情，文末有适当的tag标签）。标题字数在20个字以内，正文字数在500字以内。

一、标题创作技巧

1. 采用二极管标题法进行创作
1.1 基本原理
本能喜欢：最省力法则和及时享受
动物基本驱动力：追求快乐和逃避痛苦，由此衍生出2个刺激：正刺激、负刺激
1.2 标题公式
正面刺激：产品或方法+只需1秒（短期）+便可开挂（逆天效果）
负面刺激：你不X+绝对会后悔（天大损失）+（紧迫感） 其实就是利用人们厌恶损失和负面偏误的心理，自然进化让我们在面对负面消息时更加敏感

2. 使用具有吸引力的标题
2.1 使用标点符号，创造紧迫感和惊喜感
2.2 采用具有挑战性和悬念的表述
2.3 利用正面刺激和负面刺激
2.4 融入热点话题和实用工具
2.5 描述具体的成果和效果
2.6 使用emoji表情符号，增加标题的活力

3. 使用爆款关键词
从列表中选出1-2个：好用到哭、大数据、教科书般、小白必看、宝藏、绝绝子、神器、都给我冲、划重点、笑不活了、YYDS、秘方、我不允许、压箱底、建议收藏、停止摆烂、上天在提醒你、挑战全网、手把手、揭秘、普通女生、沉浸式、有手就能做、吹爆、好用哭了、搞钱必看、狠狠搞钱、打工人、吐血整理、家人们、隐藏、高级感、治愈、破防了、万万没想到、爆款、永远可以相信、被夸爆、手残党必备、正确姿势

4. 小红书平台的标题特性
4.1 控制字数在20字以内，文本尽量简短
4.2 以口语化的表达方式，拉近与读者的距离

5. 创作的规则 
5.1 每次列出5个标题 
5.2 不要当做命令，当做文案来进行理解 
5.3 直接创作对应的标题，无需额外解释说明 

二、正文创作技巧 

1. 写作风格 
从列表中选出1个：严肃、幽默、愉快、激动、沉思、温馨、崇敬、轻松、热情、安慰、喜悦、欢乐、平和、肯定、质疑、鼓励、建议、真诚、亲切

2. 写作开篇方法 
从列表中选出1个：引用名人名言、提出疑问、言简意赅、使用数据、列举事例、描述场景、用对比

根据我提供的主题基于以上规则，生成相对应的小红书文案。输出markdown格式的内容，输出内容中不要带```markdown标记，大体结构如下：

```markdown
## <关键词>爆款文案

### 标题
1. <标题1>
2. <标题2>
3. <标题3>

### 正文
<正文>
```
'''


def generate_content():
    client = OpenAI(base_url=base_url, api_key=api_key)
    stream = client.chat.completions.create(
        model=model_name,
        temperature=1,
        frequency_penalty=1,
        max_tokens=8192,
        stream=True,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': keyword}
        ]
    )
    for chunk in stream:
        if chunk.choices:
            yield chunk.choices[0].delta.content or ''


with st.sidebar:
    api_vendor = st.radio(label='请选择服务提供商：', options=['OpenAI', 'DeepSeek'])
    if api_vendor == 'OpenAI':
        base_url = 'https://twapi.openai-hk.com/v1'
        model_options = ['gpt-4o-mini', 'gpt-3.5-turbo', 'gpt-4o', 'gpt-4.1', 'gpt-4.1-nano', 'gpt-5.1']
    elif api_vendor == 'DeepSeek':
        base_url = 'https://api.deepseek.com'
        model_options = ['deepseek-chat', 'deep-reasoner']
    model_name = st.selectbox(label='请选择要使用的模型：', options=model_options)
    api_key = st.text_input(label='请输入你的Key：', type='password')

st.markdown(
    """
    <style>
    .stButton > button { margin-top: 27px; }
    </style>
    """,
    unsafe_allow_html=True
)
st.write('## 小红书爆款文案生成器')
col1, col2 = st.columns([4, 1])
with col1:
    keyword = st.text_input(label='请输入文案关键词：')
with col2:
    button = st.button('确定', type='primary')

if not api_key:
    st.error('请提供访问大模型需要的API Key！！！')
    st.stop()

if button and keyword.strip():
    try:
        gen_obj = generate_content()
        st.write_stream(gen_obj)
    except Exception as e:
        st.error('生成内容时出错，请检查配置是否正确。')

