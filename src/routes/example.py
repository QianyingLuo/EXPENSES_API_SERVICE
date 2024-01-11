from fastapi import APIRouter

router = APIRouter()


@router.get(path="/hola")
def show_example():
    return "Hola mundo"

@router.get(path="/adios")
def show_example():
    return "Adios mundo"
