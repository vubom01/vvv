import logging
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.helpers.login_manager import PermissionRequired, login_required
from app.schemas.sche_pet import PetInfoRequest, Url
from app.services.srv_pet import PetService

logger = logging.getLogger()
router = APIRouter()


@router.post('', dependencies=[Depends(PermissionRequired('admin'))])
def create_pet(pet_info: PetInfoRequest):
    exist_pet = PetService.is_exist_pet(name=pet_info.name)
    if exist_pet:
        raise HTTPException(status_code=400, detail='Pet name is already exist')
    PetService.create_pet(data=pet_info)
    pet_id = PetService.is_exist_pet(name=pet_info.name)['id']
    return {
        "pet_id": pet_id
    }

@router.get('', dependencies=[Depends(login_required)])
def get_list_pets():
    pets = PetService.get_list_pets()
    for pet in pets:
        images = PetService.get_pet_images(pet_id=pet.get('id'))
        pet['images'] = images
    return {
        'pets': pets
    }

@router.get('/cats', dependencies=[Depends(login_required)])
def get_list_cats():
    pets = PetService.get_pet_by_species(species='cat')
    for pet in pets:
        images = PetService.get_pet_images(pet_id=pet.get('id'))
        pet['images'] = images
    return {
        'cats': pets
    }

@router.get('/dogs', dependencies=[Depends(login_required)])
def get_list_cats():
    pets = PetService.get_pet_by_species(species='dog')
    for pet in pets:
        images = PetService.get_pet_images(pet_id=pet.get('id'))
        pet['images'] = images
    return {
        'dogs': pets
    }

@router.get('/{pet_id}', dependencies=[Depends(login_required)])
def get_pet_by_id(pet_id: int):
    pet = PetService.get_pet_by_id(pet_id=pet_id)
    if pet is None:
        raise HTTPException(status_code=400, detail='Pet not found')
    pet['images'] = PetService.get_pet_images(pet_id=pet_id)
    return pet

@router.put('/{pet_id}', dependencies=[Depends(PermissionRequired('admin'))])
def update_pet_info(pet_id: int, pet_info: PetInfoRequest):
    pet = get_pet_by_id(pet_id=pet_id)

    if pet_info.name is None:
        pet_info.name = pet.get('name')
    else:
        exist_pet = PetService.is_exist_pet(name=pet_info.name)
        if exist_pet:
            raise HTTPException(status_code=400, detail='Pet name is already exist')

    if pet_info.age is None:
        pet_info.age = pet.get('age')
    if pet_info.color is None:
        pet_info.color = pet.get('color')
    if pet_info.health_condition is None:
        pet_info.health_condition = pet.get('health_condition')
    if pet_info.weight is None:
        pet_info.weight = pet.get('weight')
    if pet_info.description is None:
        pet_info.description = pet.get('description')
    if pet_info.species is None:
        pet_info.species = pet.get('species')

    PetService.update_pet_info(pet_id=pet_id, data=pet_info)

@router.post('/{pet_id}/images', dependencies=[Depends(PermissionRequired('admin'))])
def upload_list_pet_images(pet_id: int, images: List[UploadFile] = File(...)):
    get_pet_by_id(pet_id=pet_id)
    urls = []
    for image in images:
        file_name = " ".join(image.filename.strip().split())
        file_ext = file_name.split('.')[-1]
        if file_ext.lower() not in ('jpg', 'png', 'jpeg'):
            raise HTTPException(status_code=400, detail='Can not upload file ' + image.filename)
        urls.append(PetService.upload_pet_image(pet_id=pet_id, image=image.file))
    return {
        'urls': urls
    }

@router.delete('/{pet_id}/images', dependencies=[Depends(PermissionRequired('admin'))])
def delete_image(pet_id: int, req: Url):
    PetService.delete_image(pet_id=pet_id, url=req.url)
