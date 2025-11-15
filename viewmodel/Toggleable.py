class Toggleable:
    """Interface for objects that support a toggle action.

    Classes inheriting from ``Toggleable`` are expected to implement
    the :meth:`toggle` method to change their internal state.
    """

    def toggle(self):
        """Toggle the object's internal state.

        This method should be overridden by subclasses to define
        what toggling means for that specific object.
        """
        pass