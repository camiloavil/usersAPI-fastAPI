from fastapi import APIRouter, status, File, UploadFile

files_router = APIRouter()

@files_router.post('/uploadFile/', tags=['files'], 
                   #response_model=ResponseModel, 
                   status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename,
            "format": file.content_type,
            "size": file.size}
