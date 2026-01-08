# rika
# py 3.10

import os, json

def to_json(o, s, aslist=False):
    if isinstance(s, str):
        s = get_schema(s, listdef=True)

    if aslist:
        s = [s]

    if isinstance(s, list):
        return [to_json(o[i*len(s[0]):(i+1)*len(s[0])], s[0]) for i in range(int(len(o) / len(s[0])))]

    elif isinstance(s, dict):
        new = s.copy()
        for k, v in s.items():
            if isinstance(v, int):
                new[k] = o[v] if len(o) > v else False # default to False
            elif isinstance(v, dict):
                new[k] = to_json(o, v)
            elif isinstance(v, list): # v[0] is the index and v[1] is the actual schema bit for that list
                new[k] = to_json(o[v[0]], [v[1]]) if len(o) > v[0] else [] # default to []
        return new

    raise Exception(f"schema should be list/dict or name of pre-defined schema, not {type(s)}")

def to_proto(o, s, aslist=False):
    if isinstance(s, str):
        s = get_schema(s, listdef=True)

    if aslist:
        s = [s]

    if isinstance(o, list):
        new = []
        for obj in o:
            if isinstance(obj, dict):
                new += to_proto(obj, s)
            else:
                new.append(to_proto(obj, s))
        return new

    if isinstance(s, dict):
        new = []
        i = 0
        while i < len(s.items()):
            k, v = list(s.items())[i]
            if isinstance(v, int):
                new += [False] * (v - len(new) + 1) # kys rika
                if k in o: # default to False
                    new[v] = o[k]
            elif isinstance(v, dict):
                if k not in o:
                    o[k] = dict(zip(v, to_proto({}, v))) # default dictionary stuff to False/[]
                s.update(v)
                o.update(o[k])
                del s[k] # rahhhhhhh
                del o[k]
                i -= 1
            elif isinstance(v, list):
                new += [False] * (v[0] - len(new) + 1) # x2
                if k not in o: # default to []
                    new[v[0]] = []
                else:
                    new[v[0]] = to_proto(o[k], v[1])
            i += 1
        return new

    raise Exception("one of your types is wrong or the object doesn't match the schema")

def get_schema(name, listdef=False):
    path = f"{os.path.dirname(__file__)}/shoddyproto/{name.replace('.', '/')}.json"

    if not os.path.exists(path):
        raise Exception(f"{name} schema doesn't exist.. [{path}]")

    with open(path, "r", encoding="windows-1252", errors="ignore") as f:
        schema = json.loads(f.read().strip())

    if listdef:
        return schema

    def remove_lists(d):
        for k, v in d.items():
            if isinstance(v, list):
                d[k] = []
            elif isinstance(v, dict):
                d[k] = remove_lists(v)
            elif isinstance(v, int):
                d[k] = False
        return d

    return remove_lists(schema)

