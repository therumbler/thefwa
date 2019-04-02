import hashlib

class Case():
    def __init__(self, id_, title, slug, description):
        self.id = id_
        self.title = title
        self.slug = slug
        self.description = description


class Update():
    """an instance of an FWA update"""
    def __init__(self, id, title, points, voteCount, win, rank, **kwargs):
        """set it all up"""
        self.id = id
        self.title = title
        self.points = points
        self.vote_count = voteCount
        self.win = win
        self.rank = rank

    def __repr__(self):
        return f'''
        <Update
        id={self.id}
        title="{self.title}"
        points={self.points}
        vote_count={self.vote_count}
        win={self.win}
        rank={self.rank}>
        '''.strip().replace('\n', ' ').replace('         ', ' ')


    def hash(self):
        """a sha256 hash of the object"""

        string = repr(self)
        m = hashlib.sha256()
        m.update(string.encode())
        return m.hexdigest()




