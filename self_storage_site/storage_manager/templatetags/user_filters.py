from django import template
register = template.Library()


@register.filter(name='get_free')
def get_free_for_all(all_boxes, occup_boxes):
    return all_boxes - occup_boxes