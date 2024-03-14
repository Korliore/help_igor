from fastapi import APIRouter, Request, HTTPException
from src.services.utils import clear_data
from src.web.api.contacts.schema import ContactCreate, ContactInfo
from src.db.repo import ContactsRepository

router = APIRouter()


@router.post("/", response_model=ContactInfo)
async def create_new_contact(
    request: Request,
    contact_data: ContactCreate,
):
    """
    Create new contact.

    :param contact_data: contact_data to create.
    :returns: new contact.
    """
    insert_params_clear = await clear_data(dict_=contact_data.dict())
    all_data = await ContactsRepository(request).insert_one(data=insert_params_clear)
    return all_data


@router.get("/{id}", response_model=ContactInfo)
async def get_contact(
    request: Request,
    id: int,
):
    """
    Get contact by id.

    :param id: contact id.
    :returns: contact.
    """
    contact = await ContactsRepository(request).find_one(filter_by={"id": id})
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.get(
    "/",
)
async def get_contacts(
    request: Request,
) -> list[ContactInfo]:
    """
    Get all contacts.

    :returns: contacts.
    """
    contacts = await ContactsRepository(request).find_all(filter_by={})
    return contacts


@router.delete("/{id}")
async def delete_contact(
    request: Request,
    id: int,
):
    """
    Delete contact by id.

    :param id: contact id.
    :returns: deleted contact.
    """
    contact = await ContactsRepository(request).delete_one(id_=id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact
