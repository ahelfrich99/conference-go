from json import JSONEncoder
from datetime import datetime
from django.db.models import QuerySet
from attendees.models import AccountVO


class QuerySetEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, QuerySet):
            return list(o)
        else:
            return super().default(o)

class DateEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        else:
            return super().default(o)
        # if o is an instance of datetime
        #    return o.isoformat()
        # otherwise
        #    return super().default(o)


class ModelEncoder(DateEncoder, QuerySetEncoder, JSONEncoder):
    encoders = {}

    def default(self, o):
        if isinstance(o, self.model):
            d = {}
            if hasattr(o, "get_api_url"):
                d["href"] = o.get_api_url()
            for property in self.properties:
                value = getattr(o, property)
                if property in self.encoders:
                    encoder = self.encoders[property]
                    value = encoder.default(value)
                d[property] = value
            d.update(self.get_extra_data(o))
            return d
        else:
            return super().default(o)

    def get_extra_data(self, o):
        return {}
        # count = len(AccountVO.objects.filter(email = o.email))
        # if count > 0:
        #     return {
        #         "has_account": True,
        #     }
        # else:
        #     return {
        #         "has_account": False,
        #     }

    # not sure if the has account thing is really meant to be in here or not
    # but everything is still working and I don't mind having the extra
    # information in the list attendees
