from shared.pagination import SocchoCursorPagination


class TransactionCursorPagination(SocchoCursorPagination):
    ordering = "-created_at"
