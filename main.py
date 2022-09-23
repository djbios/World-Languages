import yaml
import jinja2


all_keys = set()


def to_flat(d: dict, a=None, parent=''):
    if a is None:
        a = []

    for k, v in d.items():
        if k not in all_keys:
            all_keys.add(k)
        else:
            k = f'{k} {parent}'

        a.append((k, parent))
        if v is not None:
            assert isinstance(v, dict)
            a = to_flat(v, a, k)

    return a


with open('./languages.yaml', 'r') as f:
    data = yaml.safe_load(f)
    res = to_flat(data)
    with open('./index.html', 'r') as t:
        env = jinja2.Environment()
        template = env.from_string(t.read())
        html = template.render(labels=[l for l, _ in res], parents=[p for _, p in res])
        with open('./result.html', 'w') as o:
            o.write(html)
