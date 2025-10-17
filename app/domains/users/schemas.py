from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=30)

class EmailMixin(BaseModel):
    email: EmailStr

class PasswordValidatorMixin(BaseModel):
    password: str

    @classmethod
    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        return value

class UserCreate(UserBase, EmailMixin, PasswordValidatorMixin):
    pass

class UserLogin(EmailMixin, PasswordValidatorMixin):
    pass

class User(UserBase, EmailMixin):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
    )

