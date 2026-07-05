class DuplicateWebhookEndpointError(Exception):
    """Raised when attempting to create a webhook endpoint with an existing URL."""

    def __init__(
        self,
        message: str = "A webhook endpoint with this URL already exists.",
    ):
        super().__init__(message)