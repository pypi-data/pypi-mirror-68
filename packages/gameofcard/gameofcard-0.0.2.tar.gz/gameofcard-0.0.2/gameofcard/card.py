class Card():

    def __init__(self, value, color):
        self.color = color
        self.value = value

    def __str__(self):
        return "{v} of {c}".format(v=self.value, c=self.color)
