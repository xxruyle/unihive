# Filename: post.py
# Description: This module contains post related objects and methods
# Inputs: N/A
# Output: N/A
# Authors: Xavier Ruyle, Andrew Ward
# Creation Date: 10/24/2024

import datetime

from course import Course
from db import query
from university import University
from user import User


class Post: 
    def __init__(self, id, created, title, content, author, course_id): 
        self.id      = id                                 # Database ID       
        self.created = created                            # Date Created  
        self.title   = title                              # Title of post        
        self.content = content                            # Post body  
        self.author  = User.get_user_by_id(author)        # Author of post
        self.course  = Course.get_course_by_id(course_id) # Course post belongs to  

    @property
    def replies(self):
        """
        Post replies getter. Returns a list of all
        the replies that belong to a post. This is
        not recursive (sub-replies not shown).
        """

        # Get the top-level replies from the database.
        return [Post(*params) for params in query(
            """
                SELECT id, created, title, content, author_id, course FROM posts
                WHERE parent = ?
                ORDER BY created DESC;
            """,
            (self.id,)
        )]
    
    @property
    def likes(self):
        """Post like count getter."""

        num_likes = query(
            """
                SELECT COUNT(*) FROM user_post_likes 
                WHERE is_like = TRUE AND post = ?;
            """,
            (self.id,),
            count = 1
        )[0]


        # quick hack for adding likes to a post in the posts table 
        # TODO: this sucks :/
        query(
            """
            UPDATE posts 
            SET likes = ?
            WHERE id = ?
            """,
            (num_likes, self.id)
        )

        # Another quick hack for updating course popularity score lol
        # TODO: this sucks :/
        popularity_score = query(
            """
                SELECT COUNT(*) FROM courses 
                WHERE id = ?;
            """,
            (self.course.id,)
        )[0][0]

        # BUG: User could just keep liking and unliking to boost popularity_score
        query(
            """
            UPDATE courses 
            SET popularity_score = ?
            WHERE id = ?
            """,
            (popularity_score+1, self.id)
        )

        # DEBUG: can remove 
        # print(query(
        #     """
        #     select * FROM courses
        #     WHERE id = ?
        #     """,
        #     (self.course.id, )))
        # print(query(
        #     """
        #     select * FROM posts 
        #     WHERE id = ?
        #     """,
        #     (self.id, )))

        return num_likes

    @property
    def dislikes(self):
        """Post dislike count getter."""
        return query(
            """
                SELECT COUNT(*) FROM user_post_likes 
                WHERE is_like = FALSE AND post = ?;
            """,
            (self.id,),
            count = 1
        )[0]
    
    @property
    def is_reply(self):
        """Is post or reply getter."""
        return query(
            """
                SELECT is_reply FROM posts
                WHERE id = ?
            """,
            (self.id,),
            count = 1
        )[0]
    
    def edit(self, new_content):
        """Edit an existing post with the new content."""
        query(
            """
                UPDATE posts SET content = ?
                WHERE id = ?;
            """,
            (new_content, self.id)
        )
        self.content = new_content

    def delete(self):
        """Delete calling post from the database."""
        query(
            """DELETE FROM posts WHERE id = ?""",
            (self.id,)
        )
    
    def authored_by(self, user):
        """Simply return if user is the author."""
        return self.author.id == (user if type(user) is int else user.id)
    
    def liked_by(self, user: User):
        """
        Return if the calling user liked the given post.
        :param user: Check if this user liked the post.
        :return: True if user liked the post, else False.
        """
        return bool(query(
            """
            SELECT COUNT(*) FROM user_post_likes
            WHERE is_like = TRUE AND user = ? AND post = ?;
            """,
            (user.id, self.id),
            count = 1
        )[0])
    
    def disliked_by(self, user: User):
        """
        Return if the calling user disliked the given post.
        :param user: Check if this user disliked the post.
        :return: True if user disliked the post, else False.
        """
        return bool(query(
            """
            SELECT COUNT(*) FROM user_post_likes
            WHERE is_like = FALSE AND user = ? AND post = ?;
            """,
            (user.id, self.id),
            count = 1
        )[0]) 
    
    def _toggle_like_or_dislike(self, user: User, is_like: bool):
        """
        Insert either a like or a dislike into the database.

        :param user: The user that supplies the like/dislike.
        :param is_like: True if is like. False if is dislike.
        """

        # If the user already liked/disliked the post,
        # remove that like/dislike instead (i.e. toggle).
        if (is_like and self.liked_by(user)) or \
            (not is_like and self.disliked_by(user)):
            query(
                """
                DELETE FROM user_post_likes
                WHERE is_like = ? AND user = ? AND post = ?;
                """,
                (is_like, user.id, self.id)
            )
            return

        # The database will automatically deal with duplicates.
        # It will replace old like/dislike status with new one.
        query(
            """
            INSERT INTO user_post_likes (is_like, user, post)
            VALUES (?, ?, ?)
            """,
            (is_like, user.id, self.id)
        )

    def toggle_like(self, user):
        """
        Add a like to the calling post.
        :param user: User that liked.
        """
        self._toggle_like_or_dislike(user, True)
    
    def toggle_dislike(self, user):
        """
        Add a dislike to the calling post.
        :param user: User that disliked.
        """
        self._toggle_like_or_dislike(user, False)

    def add_reply(self, user, content):
        """
        Add a reply to the calling post.

        :param user: Author of reply.
        :param body: Content of reply.
        """
        query(
            """
            INSERT INTO posts (title, content, author, author_id, course, parent, is_reply)
            VALUES ('', ?, ?, ?, ?, ?, TRUE);
            """,
            (content, user.id, user.id, self.course.id, self.id,)
        )

    @staticmethod
    def get_post_by_id(id: int):
        """
        Get a post by its database id.
        Return None if post not found.
        """

        params = query(
            """
                SELECT id, created, title, content, author_id, course FROM posts
                WHERE id = ?;
            """,
            (id,),
            count = 1
        )
        if not params: return None # Post not found
        return Post(*params)       # Construct Post object

    @staticmethod
    def get_post_by_title(title: str, course: Course = None):
        """
        Get a post by its verbatim title string.

        :param title: Title string of the desired post.
        :param course: Course that the post belongs to.
        :returns: Post object or None if post was not found.
        """

        where_clauses = ["title = ?"] # SQL where statement clauses.
        where_params  = [title]       # SQL query parameters.

        # Append the optional course parameter
        # to the query if it provided as arg.
        if course is not None: 
            where_clauses.append("course = ?")
            where_params.append(course.id)

        # Conduct the database query.
        params = query(
            f"""
                SELECT id, created, title, content, author_id, course FROM posts
                WHERE {' AND '.join(where_clauses)};
            """,
            tuple(where_params),
            count = 1
        )

        if not params: return None # Post not found
        return Post(*params)       # Construct Post object

class Reply(Post): 
    def __init__(self):
        super().__init__()



