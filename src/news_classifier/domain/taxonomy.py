"""Category taxonomy the classifier's output is interpreted with."""

from pydantic import BaseModel, Field


class Taxonomy(BaseModel):
    """Category names plus the categories and channels the bot ignores."""

    categories: dict[int, str] = Field(default_factory=dict)
    exclude_categories: list[int] = Field(default_factory=list)
    exclude_channels: list[int] = Field(default_factory=list)

    def wanted_categories(self) -> dict[int, str]:
        """Return the categories a topic should exist for.

        Returns:
            dict[int, str]: Category index mapped to its topic name.
        """
        return {
            index: name
            for index, name in self.categories.items()
            if index not in self.exclude_categories
        }
