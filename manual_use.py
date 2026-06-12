from services.quality_service import llm_select_best, score_image
from services.similarity_service import find_similar_photos

EXSAMPLE_GROUP = [['D:\\clean_my_pic_dir\\example pics\\2026-06-01 16.22.18-1.jpg', 'D:\\clean_my_pic_dir\\example pics\\2026-06-01 16.22.18.jpg'], ['D:\\clean_my_pic_dir\\example pics\\2026-06-01 17.31.03-1.jpg', 'D:\\clean_my_pic_dir\\example pics\\2026-06-01 17.31.03.jpg', 'D:\\clean_my_pic_dir\\example pics\\2026-06-01 17.31.07-1.jpg', 'D:\\clean_my_pic_dir\\example pics\\2026-06-01 17.31.07.jpg'], ['D:\\clean_my_pic_dir\\example pics\\2026-06-01 19.25.00-1.jpg', 'D:\\clean_my_pic_dir\\example pics\\2026-06-01 19.25.00-2.jpg', 'D:\\clean_my_pic_dir\\example pics\\2026-06-01 19.25.00.jpg'], ['D:\\clean_my_pic_dir\\example pics\\2026-06-01 19.25.42-1.jpg', 'D:\\clean_my_pic_dir\\example pics\\2026-06-01 19.25.42.jpg'], ['D:\\clean_my_pic_dir\\example pics\\2026-06-01 19.25.48.jpg', 'D:\\clean_my_pic_dir\\example pics\\2026-06-01 19.26.20.jpg', 'D:\\clean_my_pic_dir\\example pics\\2026-06-01 19.26.25.jpg', 'D:\\clean_my_pic_dir\\example pics\\2026-06-01 19.26.29.jpg', 'D:\\clean_my_pic_dir\\example pics\\2026-06-01 19.27.00.jpg'], ['D:\\clean_my_pic_dir\\example pics\\2026-06-01 19.26.06-1.jpg', 'D:\\clean_my_pic_dir\\example pics\\2026-06-01 19.26.06.jpg'], ['D:\\clean_my_pic_dir\\example pics\\2026-06-01 19.26.29-1.jpg', 'D:\\clean_my_pic_dir\\example pics\\2026-06-01 19.27.00.jpg'], ['D:\\clean_my_pic_dir\\example pics\\2026-06-01 19.26.56-1.jpg', 'D:\\clean_my_pic_dir\\example pics\\2026-06-01 19.26.56.jpg', 'D:\\clean_my_pic_dir\\example pics\\2026-06-01 19.27.00-1.jpg', 'D:\\clean_my_pic_dir\\example pics\\2026-06-01 19.27.00.jpg']]
if 1:
     result = EXSAMPLE_GROUP
else:
     result = find_similar_photos(
        r"D:\clean_my_pic_dir\example pics",
        0.9
    )
     print(result)

for group in result:
    group_scores = []
    for path in group:
        print(path)
        quality = score_image(path)
        group_scores.append({
            "path": path,
            **quality
        })
    llm_result = llm_select_best(group_scores)
    print(group_scores)
    print(llm_result)