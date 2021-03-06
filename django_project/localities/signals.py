# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType


from .models import (
    Domain, DomainArchive,
    Attribute, AttributeArchive,
    Specification, SpecificationArchive,
    Locality, LocalityArchive,
    Value, ValueArchive
)


def archive_basic_info(archive, instance, content_type):
    """
    Helper function for handling archival of basic information
    """
    archive.content_type = content_type
    archive.object_id = instance.pk

    archive.version = instance.version
    archive.changeset = instance.changeset


@receiver(post_save, sender=Domain)
def domain_archive_handler(sender, instance, created, raw, **kwargs):
    ct = ContentType.objects.get(app_label='localities', model='domain')
    archive = DomainArchive()

    archive_basic_info(archive, instance, ct)

    archive.name = instance.name
    archive.description = instance.description
    archive.template_fragment = instance.template_fragment

    archive.save()


@receiver(post_save, sender=Attribute)
def attribute_archive_handler(sender, instance, created, raw, **kwargs):
    ct = ContentType.objects.get(app_label='localities', model='attribute')
    archive = AttributeArchive()

    archive_basic_info(archive, instance, ct)

    archive.key = instance.key
    archive.description = instance.description

    archive.save()


@receiver(post_save, sender=Specification)
def specification_archive_handler(sender, instance, created, raw, **kwargs):
    ct = ContentType.objects.get(app_label='localities', model='specification')
    archive = SpecificationArchive()

    archive_basic_info(archive, instance, ct)

    archive.domain_id = instance.domain.pk
    archive.attribute_id = instance.attribute.pk
    archive.required = instance.required

    archive.save()


@receiver(post_save, sender=Locality)
def locality_archive_handler(sender, instance, created, raw, **kwargs):
    ct = ContentType.objects.get(app_label='localities', model='locality')
    archive = LocalityArchive()

    archive_basic_info(archive, instance, ct)

    archive.domain_id = instance.domain.pk
    archive.uuid = instance.uuid
    archive.upstream_id = instance.upstream_id
    archive.geom = instance.geom

    archive.save()


@receiver(post_save, sender=Value)
def value_archive_handler(sender, instance, created, raw, **kwargs):
    ct = ContentType.objects.get(app_label='localities', model='value')
    archive = ValueArchive()

    archive_basic_info(archive, instance, ct)

    archive.locality_id = instance.locality.pk
    archive.specification_id = instance.specification.pk
    archive.data = instance.data

    archive.save()
