from typing import Optional, List
from fastapi import APIRouter
from pydantic.main import BaseModel
from ccdh.api.routers.data_elements import DataElement
from ccdh.config import neo4j_graph
from ccdh.db.mdr_graph import MdrGraph

mdr_graph = MdrGraph(neo4j_graph())


class PermissibleValue(BaseModel):
    pref_label: str
    data_element: Optional[DataElement]
    meaning: Optional['ValueMeaning']


from ccdh.api.routers.value_meanings import ValueMeaning
PermissibleValue.update_forward_refs()


router = APIRouter(
    prefix='/permissible-values',
    tags=['Permissible Values'],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get('/{value}', response_model=List[PermissibleValue], response_model_exclude_unset=True)
async def get_permissible_values(value: str) -> List[PermissibleValue]:
    return mdr_graph.find_permissible_values(value)
