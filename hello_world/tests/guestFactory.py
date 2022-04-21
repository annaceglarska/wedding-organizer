from hello_world.models import Guests


class GuestExapmleTest(object):
    class Meta:
        model = Guests

    name = ["Ernest", "Aleksanda"]
    surname = ["Lasek", "Kaczmarek"]
    phone = [543654765, 987876654]
    age = [25, 24]
