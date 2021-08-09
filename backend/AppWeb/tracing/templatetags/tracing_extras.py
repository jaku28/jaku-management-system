from django.template.defaulttags import register

@register.filter
def get_item(dictionary, obj):
    key = str(obj.project.id) + '-' + str(obj.criteria.id)
    return dictionary.get(key)

@register.filter
def get_item_score(dictionary,p_id):
    return dictionary, p_id

@register.filter
def get_item_for_jury(dictionary_p_id, j_id):
    dictionary, p_id = dictionary_p_id
    return dictionary.get(f'{p_id.id}-{j_id.id}')


@register.filter
def get_item_final_score(dictionary, obj):
    key = str(obj.id)
    return dictionary.get(key)
    