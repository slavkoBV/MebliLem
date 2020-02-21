from shop.utils import slugify


file_storage_mapping = {
    "Catalog": "catalogs/",
    "ProductImage": "products/",
    "Manufacturer": "manufacturers/",
    "Category": "categories/"
}


def update_filename(instance, filename):
    path = file_storage_mapping[instance._meta.object_name]
    filename, file_ext = filename.split('.')
    if not is_ascii(filename):
        filename = slugify(filename)
    return '{}/{}.{}'.format(path, filename, file_ext)


def is_ascii(a_string):
    return all(ord(c) < 128 for c in a_string)
