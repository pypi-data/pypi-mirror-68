from .common import ClubhouseResource


class Stories(ClubhouseResource):
    """https://clubhouse.io/api/rest/v3/#Stories"""

    def create(self, story_id):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def search(self, criteria):
        """
        Returns the clubhouse story/stories matching the criteria
        https://clubhouse.io/api/rest/v3/#Search-Stories-Old
        EXAMPLE:
            from clubhouse_client import Client
            clubhouse = Client()
            clubhouse.stories.get({'story_type': 'feature'})
        """
        return super()._post("stories/search", payload=criteria)

    def get(self, story_public_id):
        """
        Returns the clubhouse story matching the story_public_id
        https://clubhouse.io/api/rest/v3/#Get-Story
        EXAMPLE:
            from clubhouse_client import Client
            clubhouse = Client()
            my_story = clubhouse.stories.get('13')
        """
        endpoint = f"stories/{story_public_id}"
        return super()._get(endpoint)

    def create_comment(self):
        pass

    def get_comment(self):
        pass

    def update_comment(self):
        pass

    def create_reaction(self):
        pass

    def delete_reaction(self):
        pass

    def create_task(self):
        pass

    def get_task(self):
        pass

    def update_task(self):
        pass

    def delete_task(self):
        pass
