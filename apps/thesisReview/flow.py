""" Test Flow Definition"""

from apps.thesisReview.models import Upload, Distribution, Review
from apps.thesisReview.rules import Upload_to_Distribution, Distribution_to_Review



FLOW = {
    'upload_activity': {
        'name': '论文上传',
        'model': Upload,
        'role': 'Submitter',
        'transitions': {
            'distribution_activity': Upload_to_Distribution,
        }
    },
    'distribution_activity': {
        'name': '分配评审',
        'model': Distribution,
        'role': 'Editor',
        'transitions': {
            'review_activity': Distribution_to_Review,
        }
    },
    'review_activity': {
        'name': '论文审核',
        'model': Review,
        'role': 'Review',
        'transitions': None
    },
}

INITIAL = 'upload_activity'

TITLE = 'Thesis Review'
DESCRIPTION = ''
