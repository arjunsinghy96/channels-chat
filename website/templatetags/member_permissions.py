from django import template

register = template.Library()

@register.simple_tag
def permission_level(member, league):
    return member.membership_set.get(league=league).get_permissions_display()