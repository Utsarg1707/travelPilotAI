"""LangGraph Checkpointing Strategy."""


from langgraph.checkpoint.memory import MemorySaver


class CheckpointManager:
    """Manager for LangGraph workflow state persistence and thread checkpointing."""

    _checkpointer: MemorySaver | None = None

    @classmethod
    def get_checkpointer(cls) -> MemorySaver:
        """Get or initialize singleton MemorySaver checkpointer."""
        if cls._checkpointer is None:
            cls._checkpointer = MemorySaver()
        return cls._checkpointer
