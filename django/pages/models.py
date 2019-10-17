from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):

    def with_nm_posts(self):
        user_meta = self.model._meta
        post_meta = Post._meta  # pylint: disable=no-member

        query = f"""
            select u.*, ifnull(c.nm_posts, 0) as nm_posts
            from {user_meta.db_table} u
            left join (
                select count(*) as nm_posts, author_id
                from {post_meta.db_table} p
                group by p.author_id
            ) c on u.id = c.author_id
        """

        return self.raw(query)

        # playing around
        # from django.db import connection
        # with connection.cursor() as cursor:
        #     cursor.execute(query)
        #     results = []
        #     for row in cursor.fetchall():
        #         values = { p[0][0]: p[1] for p in zip(cursor.description, row) if p[0][0] != 'nm_posts' }
        #         p = self.model(**values)
        #         p.nm_posts = row[-1]
        #         results.append(p)
        # return results


class CustomUser(AbstractUser):
    objects = CustomUserManager()
    birthDate = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=False, null=False, default=0)

    class Meta(AbstractUser.Meta):
        db_table = 'users'


class Post(models.Model):
    name = models.CharField(max_length=200, blank=True)
    text = models.TextField()
    author = models.ForeignKey(
        'pages.CustomUser', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Post named '{self.name}'"

    def get_absolute_url(self):
        return reverse('post-details', kwargs={"post_id": self.pk})
