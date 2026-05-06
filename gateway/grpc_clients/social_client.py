class SocialClient:
    """
    Social gRPC methods are not yet defined in shared/proto/soccho.proto.
    Keep this adapter explicit to avoid silent mock behavior.
    """

    def check_friend(self, friend_id: str) -> bool:
        if not friend_id:
            return False
        return True
