
class Target:
    def request(self) -> str:
        return "Target: Дефолтна поведінка (очікує JSON)."


class Adaptee:
    def specific_request(self) -> str:
        return ".LMX тамроф у інаД"

class Adapter(Target):
    def __init__(self, adaptee: Adaptee) -> None:
        self.adaptee = adaptee

    def request(self) -> str:
        translated_data = self.adaptee.specific_request()[::-1]
        return f"Adapter: (Адаптовано) {translated_data}"

if __name__ == "__main__":
    adaptee = Adaptee()
    print(f"Adaptee: {adaptee.specific_request()}")
    
    adapter = Adapter(adaptee)
    print(adapter.request()) 