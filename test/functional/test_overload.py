from luxtools import overload


def test_class_types():
    class Email:
        def __init__(self, email: str):
            self.email = email

        def __str__(self) -> str:
            return self.email

    class PhoneNumber:
        def __init__(self, phone_number: str):
            self.phone_number = phone_number

        def __str__(self) -> str:
            return self.phone_number

    # problem: the function is not in global scope.
    @overload(scope=locals())
    def get_user(email: Email):
        return "email function"

    @overload(scope=locals())
    def get_user(phone_number: PhoneNumber):
        return "phone function"

    user_email = get_user(Email("test@example.com"))
    user_phone = get_user(PhoneNumber("123-456-789"))

    assert user_email == "email function", "should be sent to the email function"
    assert user_phone == "phone function", "should be sent to the phone function"
