"""Rules"""


def Upload_to_Distribution(self):
    """Check if foo can send to corge"""
    return self.content is not None

def Distribution_to_Review(self):
    return self.review1 is not None and \
            self.review2 is not None and \
              self.review3 is not None
