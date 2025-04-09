from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Language(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        verbose_name='Language Name',
        )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        verbose_name='Tag Name',
        )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class Country(models.Model):
    name = models.CharField(
        max_length=70,
        unique=True,
        null=False,
        blank=False,
        verbose_name='Country name',
        )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class Author(models.Model):
    fname = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name='Name',
    )
    lname = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name='Last name',
    )
    country = models.ForeignKey(
        Country,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='authors'
    )

    def __str__(self):
        return self.fname + ' ' + self.lname

    class Meta:
        ordering = ['fname', 'lname']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Book(models.Model):
    title = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='Title',
    )
    image = models.ImageField(
        upload_to='books_images/%Y/%m/%d',
        blank=True, null=True,
        verbose_name='Book Image',
    )
    description = models.TextField(
        null=False, blank=False,
        verbose_name='Description'
    )
    slug = models.SlugField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Upload author',
        related_name='books',
        on_delete=models.CASCADE,
        blank=False, null=False
    )
    language = models.ForeignKey(
        Language,
        blank=True, null=True,
        related_name='books',
        verbose_name='Book language',
        on_delete=models.SET_NULL
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='books'
    )
    authors = models.ManyToManyField(
        Author,
        blank=True, null=True,
        related_name='books',
        verbose_name='Authors',
    )

    def __str__(self):
        authors = ", ".join([str(author) for author in self.authors.all()])
        if authors:
            return f'{self.title} by {authors}'
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
