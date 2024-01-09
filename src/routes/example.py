from fastapi import APIRouter

router = APIRouter()


@router.get(path="/hola")
def show_example():
    return "Hola mundo"
