"""Tiny SQL writer.

Every INSERT is checked against the column list of the target world database (SCHEMA, filled by build.py from
information_schema of the pristine world DB, which must be built from the *server's own core*). Rows are written
with the converter's column names; ALIASES maps them to older/newer AzerothCore spellings (creature.id1 vs id).
A table or column the target does not have stops the build instead of producing SQL the DB updater rejects
(ERROR 1054 aborts the whole update and the worldserver does not start).
"""
SCHEMA = {}          # table -> [columns] of the target world DB; empty = no check
# (table, converter column) -> column in a core that spells it differently; None = column absent there, only
# allowed when the value is 0/NULL (e.g. creature.id2/id3 on a core with a single creature.id)
ALIASES = {('creature', 'id1'): 'id', ('creature', 'id2'): None, ('creature', 'id3'): None}


def col(table, c):
    """converter column name -> the target's name (for raw SQL)"""
    if not SCHEMA or c in SCHEMA.get(table, ()):
        return c
    a = ALIASES.get((table, c), c)
    if a is None or a not in SCHEMA.get(table, ()):
        raise KeyError(f'{table}.{c}: no such column in the target world DB')
    return a


def _adapt(table, cols, rows):
    if not SCHEMA:
        return cols
    if table not in SCHEMA:
        raise KeyError(f'table {table} does not exist in the target world DB')
    have = SCHEMA[table]
    out = []
    for c in cols:
        if c in have:
            out.append((c, c))
            continue
        if (table, c) in ALIASES:
            a = ALIASES[(table, c)]
            if a is None:
                bad = [r.get(c) for r in rows if r.get(c) not in (None, 0)]
                if bad:
                    raise ValueError(f'{table}.{c} does not exist in the target DB but rows use it: {bad[:5]}')
                continue
            if a in have:
                out.append((c, a))
                continue
        raise KeyError(f'{table}.{c}: no such column in the target world DB')
    return out


def lit(v):
    if v is None:
        return 'NULL'
    if isinstance(v, bool):
        return '1' if v else '0'
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return repr(round(v, 6))
    s = str(v).replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n').replace('\r', '')
    return "'" + s + "'"


def in_list(ids):
    ids = sorted(set(ids))
    return ','.join(map(str, ids)) if ids else 'NULL'


class Sql:
    def __init__(self):
        self.parts = []

    def comment(self, c):
        self.parts.append('\n-- ' + c)

    def raw(self, t):
        self.parts.append(t)

    def insert(self, table, rows, cols=None, chunk=500):
        rows = [r for r in rows if r]
        if not rows:
            return
        cols = cols or list(rows[0].keys())
        m = _adapt(table, cols, rows) if SCHEMA else [(c, c) for c in cols]
        for i in range(0, len(rows), chunk):
            part = rows[i:i + chunk]
            self.parts.append('INSERT INTO `%s` (%s) VALUES' % (table, ', '.join('`%s`' % t for _, t in m)))
            self.parts.append(',\n'.join('(' + ', '.join(lit(r.get(c)) for c, _ in m) + ')' for r in part) + ';')

    def text(self):
        return '\n'.join(self.parts) + '\n'
