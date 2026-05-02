from pydantic import BaseModel, ConfigDict


class PaymentMethodBase(BaseModel):
    name: str


class PaymentMethodCreate(PaymentMethodBase):
    pass


class PaymentMethodUpdate(BaseModel):
    name: str | None = None


class PaymentMethodRead(PaymentMethodBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
