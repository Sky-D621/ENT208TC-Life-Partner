import csv
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


# 数据文件保存到当前脚本所在目录，便于项目内直接使用
CSV_FILE = Path(__file__).resolve().parent / "focus_data.csv"

# 当前版本使用的 CSV 表头
CSV_HEADERS = ["Timestamp", "Duration_Seconds", "Emotion", "Mode_Used"]


def get_default_report() -> dict:
    """返回无数据或异常场景下的默认分析结果。"""
    return {
        "Total Interruptions": 0,
        "Top Emotion Trigger": "",
        "Average Focus Duration By Mode": {
            "strict": 0,
            "empathetic": 0,
        },
    }


def log_distraction(study_duration_seconds, emotion, mode_used="empathetic") -> None:
    """
    记录一次分心事件到本地 CSV 文件中。

    参数：
        study_duration_seconds: 用户已专注时长，单位为秒，例如 720
        emotion: 本次触发分心的情绪原因，例如“😰 焦虑”
        mode_used: 本次使用的干预模式，默认是 empathetic
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = CSV_FILE.exists()

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.writer(csv_file)

        if not file_exists:
            writer.writerow(CSV_HEADERS)

        writer.writerow([timestamp, study_duration_seconds, emotion, mode_used])


def generate_analytics_report() -> dict:
    """
    读取 focus_data.csv，并生成基础统计报告。

    返回：
        一个包含以下信息的字典：
        - Total Interruptions: 总计打断次数
        - Top Emotion Trigger: 最常见的分心原因
        - Average Focus Duration By Mode: strict 与 empathetic 模式下的平均专注时长
    """
    default_report = get_default_report()

    try:
        if not CSV_FILE.exists():
            return default_report

        with open(CSV_FILE, mode="r", newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)

            # 文件为空、没有表头，或者表头字段不完整时，直接返回默认值
            if not reader.fieldnames:
                return default_report

            required_fields = {"Timestamp", "Duration_Seconds", "Emotion", "Mode_Used"}
            if not required_fields.issubset(set(reader.fieldnames)):
                return default_report

            emotion_counter = Counter()
            mode_duration_map = defaultdict(list)
            total_interruptions = 0

            for row in reader:
                duration_text = (row.get("Duration_Seconds") or "").strip()
                emotion = (row.get("Emotion") or "").strip()
                mode_used = (row.get("Mode_Used") or "").strip().lower()

                # 跳过完全空行
                if not duration_text and not emotion and not mode_used:
                    continue

                try:
                    duration_seconds = int(float(duration_text))
                except (ValueError, TypeError):
                    # 单行数据异常时跳过，不影响整体报表生成
                    continue

                total_interruptions += 1

                if emotion:
                    emotion_counter[emotion] += 1

                if mode_used in ("strict", "empathetic"):
                    mode_duration_map[mode_used].append(duration_seconds)

            if total_interruptions == 0:
                return default_report

            top_emotion = ""
            if emotion_counter:
                top_emotion = emotion_counter.most_common(1)[0][0]

            strict_durations = mode_duration_map.get("strict", [])
            empathetic_durations = mode_duration_map.get("empathetic", [])

            strict_average = (
                round(sum(strict_durations) / len(strict_durations), 2)
                if strict_durations
                else 0
            )
            empathetic_average = (
                round(sum(empathetic_durations) / len(empathetic_durations), 2)
                if empathetic_durations
                else 0
            )

            return {
                "Total Interruptions": total_interruptions,
                "Top Emotion Trigger": top_emotion,
                "Average Focus Duration By Mode": {
                    "strict": strict_average,
                    "empathetic": empathetic_average,
                },
            }

    except (FileNotFoundError, PermissionError, OSError, csv.Error):
        return default_report


if __name__ == "__main__":
    # 直接运行此文件时，打印当前统计结果，便于本地快速验证
    print(generate_analytics_report())
