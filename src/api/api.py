import os
from dotenv import load_dotenv
from typing import Optional, List
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

from bson import ObjectId
#import motor.motor_asyncio
from pymongo import ReturnDocument

os.chdir("../")
load_dotenv()

app = FastAPI(
    title="dataset API",
    summary="An application for amharic dataset",
)

from database.mongodb import MongoDB

mongo = MongoDB()
db_name = os.getenv("MONGO_DB_NAME")
collection_name = os.getenv("MONGO_COLLECTION_NAME")
collection = mongo.get_collection(db_name. collection_name)

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class DatasetModel(BaseModel):
    """
    Container for a single record.
    """
    # The primary key for the StudentModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    image_url: str = Field(...)
    title: str = Field(...)
    article_url: str = Field(...)
    highlight: str = Field(...)
    time_published: str = Field(...)
    catagory: str = Field(...)
    date_published: str = Field(...)
    publisher_name: str = Field(...)
    detail_content: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                'image_url': 'https://cdn.al-ain.com/sm/images/2024/5/23/273-173204-1_1664f45543a6b0_700x400.jpg',
                'title': 'ኢራን ፕሬዝዳንታዊ ምርጫ መቼና እንዴት ታካሂዳለች?',
                'article_url': 'https://am.al-ain.com/article/crash-to-race-iranian-presidency-path',
                'highlight': 'የሹራ ምክርቤት የምርጫው እጩ ተፎካካሪዎችና የምርጫው ሂደትን በተመለከተ ውሳኔዎችን ያሳልፋል',
                'time_publish': '18 hours ago',
                'category': 'politics',
                'date_published': '2024/5/23 11:52 GMT',
                'publisher_name': 'አል-ዐይን',
                'detail_content': 'የሹራ ምክርቤት የምርጫው እጩ ተፎካካሪዎችና የምርጫው ሂደትን በተመለከተ ውሳኔዎችን ያሳልፋል\nኢራን በሄሊኮፕተር አደጋ ህይወታቸው ያለፈውን ኢብራሂም ራይሲ ስርአተ ቀብር ፈጽማለች።\nየ68 ሀገራት መሪዎች እና ከፍተኛ ባለስልጣናት ፕሬዝዳንት ራይሲ ቀብር ላይ ለመገኘት ቴህራን ገብተዋል።\nየቀድሞ የተባሉት ፕሬዝዳንት ህይወታቸው ማለፉን ተከትሎ የፖለቲካ የስልጣን ክፍተት እንዳይፈጠር የሀገሪቱ ህገመንግስት የሚተካቸው ማን እንደሚሆን አስቀምጧል።\n\nየኢራን ህገመንግስት ስለጊዜያዊ ፕሬዝዳንት ሹመት ምን ይላል?\n\nጊዜያዊ ፕሬዝዳንቱ ስራቸውን መቀጠል የማያስችል ሁኔታ ከገጠማቸው የሀገሪቱ የበላይ መሪ አዲስ መሪ ይሾማሉ።\n\nየኢራን ፕሬዝዳንታዊ ምርጫ መቼ ይካሄዳል?\n\nየሹራ ምክርቤት ፕሬዝዳንታዊ ምርጫ የሚካሄድበትን ቀን ይወስናል፤ እጩ ተፎካካሪዎቹን በተመለከተም ውሳኔውን ያሳልፋል።\n\nምርጫው ግልጽና ተአማኒ ሆኖ እንዲካሄድ ዝግጅት የተለያዩ አካላት ሚና\n\nበምርጫው አሸናፊ ለመሆን ከ50 በመቶ በላይ መራጭ ማግኘት ይጠበቃል። እጩ ተፎካካሪዎች አሸናፊ የሚያደርግ ድምጽ ካላገኙ ከፍተኛ ድምጽ ያገኙት በሁለተኛ ዙር ምርጫ ይፎካከራሉ።\n\nየምርጫ ቅስቀሳና ክርክር\n\nበምርጫው ለመሳተፍ ቅድመሁኔታዎቹ ምንድን ናቸው?'},
            }
    )

class UpdateDatasetModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """
    name: Optional[str] = None
    image_url: Optional[str] = None
    title: Optional[str] = None
    article_url: Optional[str] = None
    highlight: Optional[str] = None
    time_published: Optional[str] = None
    catagory: Optional[str] = None
    date_published: Optional[str] = None
    publisher_name: Optional[str] = None
    detail_content: Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                'image_url': 'https://cdn.al-ain.com/sm/images/2024/5/23/273-173204-1_1664f45543a6b0_700x400.jpg',
                'title': 'ኢራን ፕሬዝዳንታዊ ምርጫ መቼና እንዴት ታካሂዳለች?',
                'article_url': 'https://am.al-ain.com/article/crash-to-race-iranian-presidency-path',
                'highlight': 'የሹራ ምክርቤት የምርጫው እጩ ተፎካካሪዎችና የምርጫው ሂደትን በተመለከተ ውሳኔዎችን ያሳልፋል',
                'time_publish': '18 hours ago',
                'category': 'politics',
                'date_published': '2024/5/23 11:52 GMT',
                'publisher_name': 'አል-ዐይን',
                'detail_content': 'የሹራ ምክርቤት የምርጫው እጩ ተፎካካሪዎችና የምርጫው ሂደትን በተመለከተ ውሳኔዎችን ያሳልፋል\nኢራን በሄሊኮፕተር አደጋ ህይወታቸው ያለፈውን ኢብራሂም ራይሲ ስርአተ ቀብር ፈጽማለች።\nየ68 ሀገራት መሪዎች እና ከፍተኛ ባለስልጣናት ፕሬዝዳንት ራይሲ ቀብር ላይ ለመገኘት ቴህራን ገብተዋል።\nየቀድሞ የተባሉት ፕሬዝዳንት ህይወታቸው ማለፉን ተከትሎ የፖለቲካ የስልጣን ክፍተት እንዳይፈጠር የሀገሪቱ ህገመንግስት የሚተካቸው ማን እንደሚሆን አስቀምጧል።\n\nየኢራን ህገመንግስት ስለጊዜያዊ ፕሬዝዳንት ሹመት ምን ይላል?\n\nጊዜያዊ ፕሬዝዳንቱ ስራቸውን መቀጠል የማያስችል ሁኔታ ከገጠማቸው የሀገሪቱ የበላይ መሪ አዲስ መሪ ይሾማሉ።\n\nየኢራን ፕሬዝዳንታዊ ምርጫ መቼ ይካሄዳል?\n\nየሹራ ምክርቤት ፕሬዝዳንታዊ ምርጫ የሚካሄድበትን ቀን ይወስናል፤ እጩ ተፎካካሪዎቹን በተመለከተም ውሳኔውን ያሳልፋል።\n\nምርጫው ግልጽና ተአማኒ ሆኖ እንዲካሄድ ዝግጅት የተለያዩ አካላት ሚና\n\nበምርጫው አሸናፊ ለመሆን ከ50 በመቶ በላይ መራጭ ማግኘት ይጠበቃል። እጩ ተፎካካሪዎች አሸናፊ የሚያደርግ ድምጽ ካላገኙ ከፍተኛ ድምጽ ያገኙት በሁለተኛ ዙር ምርጫ ይፎካከራሉ።\n\nየምርጫ ቅስቀሳና ክርክር\n\nበምርጫው ለመሳተፍ ቅድመሁኔታዎቹ ምንድን ናቸው?'},
            }
    )

class DatasetCollection(BaseModel):
    """
    A container holding a list of `DatasetModel` instances.
    """
    datasets: List[DatasetModel]

@app.post(
    "/datasets/",
    response_description="Add new dataset",
    response_model=DatasetModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)

async def create_dataset(dataset: DatasetModel = Body(...)):
    """
    Insert a new dataset record.
    A unique `id` will be created and provided in the response.
    """
    new_dataset = await collection.insert_one(
        dataset.model_dump(by_alias=True, exclude=["id"])
    )
    created_dataset = await collection.find_one(
        {"_id": new_dataset.inserted_id}
    )
    return created_dataset

@app.get(
    "/datasets/",
    response_description="List all datasets",
    response_model=DatasetCollection,
    response_model_by_alias=False,
)

async def list_students():
    """
    List all of the dataset data in the database.
    The response is unpaginated and limited to 1000 results.
    """
    return DatasetCollection(datasets=await collection.find().to_list(1000))

@app.get(
    "/datasets/{id}",
    response_description="Get a single dataset",
    response_model=DatasetModel,
    response_model_by_alias=False,
)
async def show_dataset(id: str):
    """
    Get the record for a specific dataset, looked up by `id`.
    """
    if (
        dataset := await collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return dataset
    raise HTTPException(status_code=404, detail=f"dataset {id} not found")

@app.put(
    "/datasets/{id}",
    response_description="Update a dataset",
    response_model=DatasetModel,
    response_model_by_alias=False,
)
async def update_dataset(id: str, student: UpdateDatasetModel = Body(...)):

    """
    Update individual fields of an existing dataset record.
    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.

    """

    dataset = {

        k: v for k, v in dataset.model_dump(by_alias=True).items() if v is not None

    }
    if len(dataset) >= 1:

        update_result = await collection.find_one_and_update(

            {"_id": ObjectId(id)},

            {"$set": dataset},

            return_document=ReturnDocument.AFTER,

        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"dataset {id} not found")
    # The update is empty, but we should still return the matching document:
    if (existing_dataset := await collection.find_one({"_id": id})) is not None:
        return existing_dataset
    raise HTTPException(status_code=404, detail=f"dataset {id} not found")

@app.delete("/datasets/{id}", response_description="Delete a dataset")

async def delete_dataset(id: str):

    """

    Remove a single dataset record from the database.

    """

    delete_result = await collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"dataset {id} not found")


