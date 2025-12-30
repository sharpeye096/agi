import os

root_curriculum = "课内"
root_extra = "课外"

grades = [
    "一年级", "二年级", "三年级", "四年级", "五年级", "六年级",
    "初一", "初二", "初三",
    "高一", "高二", "高三"
]
subjects_curriculum = ["语文", "数学", "英语"]

subjects_extra = ["自然科学", "编程与AI"]

def create_dirs():
    # Curriculum
    for grade in grades:
        for subj in subjects_curriculum:
            path = os.path.join(root_curriculum, grade, subj)
            os.makedirs(path, exist_ok=True)
            print(f"Created: {path}")

    # Extracurricular
    for subj in subjects_extra:
        path = os.path.join(root_extra, subj)
        os.makedirs(path, exist_ok=True)
        print(f"Created: {path}")

if __name__ == "__main__":
    create_dirs()
