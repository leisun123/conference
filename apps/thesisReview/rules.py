"""Rules"""


def Upload_to_Distribution(self):
    """Check if foo can send to corge"""
    return self.content is not None

def Distribution_to_Review(self):
    return self.reviewer1 is not None and \
            self.reviewer2 is not None and \
              self.reviewer3 is not None
