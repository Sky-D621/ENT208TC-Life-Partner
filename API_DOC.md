# 内部接口调用文档 (给前端看的)

## 1. 获取 AI 教练建议
**函数：** `get_micro_task(emotion: str, mode: str) -> str`
**所在文件：** `ai_coach.py`
**如何调用：**
```
from ai_coach import get_micro_task

# 前端按钮被点击后调用：
ai_reply = get_micro_task(emotion="太难了", mode="empathetic")
st.write(ai_reply)
```

## 2. 写入分心日志
**函数：** `log_distraction(duration: int, emotion: str, mode: str)`
**所在文件：** `logger.py`
**如何调用：**
```
from logger import log_distraction

# 计时器暂停时，存入数据：
log_distraction(duration=1200, emotion="手机诱惑", mode="strict")
```