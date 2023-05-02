counts = {}


def make_key(cls, part: str):
    model_prefix = getattr(cls._meta, "model_key_prefix", "").strip(":")
    return f"{model_prefix}:{part}"


def get_id_creator(key: str):
    global counts

    if key not in counts:
        counts[key] = 0

    class PrimaryKeyCreator:
        def create_pk(self, *args, **kwargs) -> str:
            """Create a new primary key"""
            global counts
            counts[key] += 1
            return str(counts[key])

    return PrimaryKeyCreator


def get_meta(key: str):
    class Meta:
        model_key_prefix = key
        index_name = f"{key}:index"
        primary_key_creator_cls = get_id_creator(key)

    return Meta


def Base(key: str):
    class Base:
        @classmethod
        def make_key(cls, part: str):
            return make_key(cls, part)

        Meta = get_meta(key)

    return Base