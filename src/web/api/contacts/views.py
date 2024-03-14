from fastapi import APIRouter, Request
from src.services.utils import clear_data
from src.web.api.contacts.schema import ContactCreate
from src.db.repo import ContactsRepository

router = APIRouter()


@router.post("/", response_model=ContactCreate)
async def send_echo_message(
    request: Request,
    contact_data: ContactCreate,
) -> ContactCreate:
    """
    Sends echo back to user.

    :param incoming_message: incoming message.
    :returns: message same as the incoming.
    """
    insert_params_clear = await clear_data(dict_=contact_data.dict())
    all_data = await ContactsRepository(request).insert_one(data=insert_params_clear)
    return all_data
