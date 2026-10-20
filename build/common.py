import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data")


class Topic:
    def __init__(self, id, he, name, family, source, summary, tags=()):
        self.d = dict(id=id, he=he, name=name, family=family, source=source,
                      summary=summary.strip(), tags=list(tags), cards=[])

    def _add(self, card):
        card["id"] = f"{self.d['id']}{len(self.d['cards']) + 1}"
        self.d["cards"].append({k: v for k, v in card.items() if v is not None})
        return self

    def F(self, q, a, e=None):
        return self._add(dict(t="flash", q=q, a=a, e=e))

    def M(self, q, options, correct, e=None):
        return self._add(dict(t="mcq", q=q, o=options, c=correct, e=e))

    def N(self, q, v, tol=0, u="", e=None):
        return self._add(dict(t="num", q=q, v=v, tol=tol, u=u, e=e))


def write(exam, version, topics):
    os.makedirs(OUT, exist_ok=True)
    data = dict(exam=exam, version=version, topics=[t.d for t in topics])
    with open(os.path.join(OUT, f"{exam}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    n = sum(len(t.d["cards"]) for t in topics)
    print(f"{exam}: {len(topics)} topics, {n} cards")
