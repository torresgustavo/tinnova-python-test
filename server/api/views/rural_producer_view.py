from typing import List
from uuid import UUID
from ninja import Router
from ninja.responses import Response

from django.db import transaction
from django.http.request import HttpRequest

from api.schemas.rural_producers_schemas import EditRuralProducerSchema, NewRuralProducerSchema, ViewRuralProducersSchema

from api.repositories.rural_producer_repository import RuralProducerRepository
from api.repositories.farm_culture_types_repository import FarmCultureTypesRepository

from api.validators.rural_producer_validator import RuralProducerValidator

from api.services.add_rural_producer_service import AddRuralProducerService
from api.services.edit_rural_producer_service import EditRuralProducerService

__rural_producers_repository = RuralProducerRepository()
__culture_types_repository = FarmCultureTypesRepository()

__rural_producers_validator = RuralProducerValidator(
    rural_producer_repository=__rural_producers_repository,
    culture_types_repository=__culture_types_repository
)

router = Router(tags=['Rural Producer Management'])

@router.get(
    "", 
    response=List[ViewRuralProducersSchema],
    summary='List all rural producer',
    description='List all rural producer registered'
)
def list(request: HttpRequest):
    rural_producers = __rural_producers_repository.get_all()
    if len(rural_producers) == 0:
        return Response([])

    data = [ViewRuralProducersSchema.from_orm(producer) for producer in rural_producers]
    return Response(data)

@router.post(
    '/management',
    summary='Register new rural producer',
    response={
        201: ViewRuralProducersSchema
    }
)
@transaction.atomic
def add_producer(request: HttpRequest, new_rural_producer: NewRuralProducerSchema):
    service = AddRuralProducerService(
        rural_producer_repository=__rural_producers_repository,
        rural_producer_validator=__rural_producers_validator,
        rural_producer_schema=new_rural_producer
    )
    rural_producer_added = service.execute()

    data = ViewRuralProducersSchema.from_orm(rural_producer_added)
    return Response(data, status=201)

@router.get(
    '/{document_number}', 
    response=ViewRuralProducersSchema,
    summary='Get rural producer by documento',
    description='Get rural producer by document number'
)
def get_by_document(request: HttpRequest, document_number: str):

    rural_producer = __rural_producers_repository.get_by_document(document_number)

    data = ViewRuralProducersSchema.from_orm(rural_producer)

    return Response(data)

@router.patch(
    '/management/{rural_producer_id}',
    summary='Edit rural producer data',
    response={
        200: ViewRuralProducersSchema
    }
)
@transaction.atomic
def edit_producer(request: HttpRequest, rural_producer_to_edit: EditRuralProducerSchema, rural_producer_id: UUID):
    service = EditRuralProducerService(
        rural_producer_repository=__rural_producers_repository,
        rural_producer_validator=__rural_producers_validator,
        rural_producer_schema=rural_producer_to_edit
    )
    rural_producer_edited = service.execute(rural_producer_id)

    data = ViewRuralProducersSchema.from_orm(rural_producer_edited)
    return Response(data)