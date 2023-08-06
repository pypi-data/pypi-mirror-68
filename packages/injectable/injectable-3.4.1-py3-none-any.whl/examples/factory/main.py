"""
In this example you'll see how we can use a injectable_factory function for an
injectable.
"""
# sphinx-start
from examples import Example
from injectable import injectable, autowired, Autowired, load_injection_container


@injectable  # make examples also injectable for testing
class Factory(Example):
    @autowired
    def __init__(
        self, client: Autowired("client"),
    ):
        self.client = client

    def run(self):
        print(self.client.connect())
        # ClientOne connected to https://client.endpoint/


if __name__ == "__main__":
    load_injection_container()
    example = Factory()
    example.run()
