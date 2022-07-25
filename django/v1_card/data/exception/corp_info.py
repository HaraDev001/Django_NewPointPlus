class CorpInfoDoesNotExist(Exception):
    def __str__(self):
        return 'リクエストされたホストで一致するサービス情報がない'