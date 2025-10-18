from pydantic import BaseModel, Field, EmailStr, ConfigDict, model_validator
from app.domains.users.models import Role


class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=30)


class EmailSchemaMixin(BaseModel):
    email: EmailStr


class RoleSchemaMixin(BaseModel):
    role: Role


class PasswordSchemaMixin(BaseModel):
    password: str

    @model_validator(mode="after")
    def validate_password(self):
        if len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters")
        return self


class UserRegister(UserBase, EmailSchemaMixin, PasswordSchemaMixin):
    pass


class UserCreate(UserRegister, RoleSchemaMixin):
    pass


class UserLogin(EmailSchemaMixin, PasswordSchemaMixin):
    pass


class UserDTO(UserBase, EmailSchemaMixin, RoleSchemaMixin):
    id: int


    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
    )


class UserResponse(UserDTO):
    pass
