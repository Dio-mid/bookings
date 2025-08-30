import shutil

from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_image(file: UploadFile): # , background_tasks: BackgroundTasks
    image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file: # wb+ запись бинарных файлов
        shutil.copyfileobj(file.file, new_file)

    resize_image.delay(image_path)
    # background_tasks.add_task(resize_image, image_path) # Из resize_image нужно убрать декоратор celery